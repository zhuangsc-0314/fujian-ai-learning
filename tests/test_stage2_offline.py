"""真实网络禁用下检查输入、链路及失败边界，不冒充模型实测。"""

from datetime import date
import json
from pathlib import Path

import httpx
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from openai import APIConnectionError, APITimeoutError
import pytest

from learning_app import ai
from learning_app.domain import (
    AppError, EvidenceInput, MaterialInput, build_acceptance_report, build_material_context,
    decide_review_status, describe_publication_date, locate_quote, validate_evidence,
)
from learning_app.history import historical_material, historical_result
from learning_app.service import CandidateStore, generate_candidate
from learning_app.storage import build_engine


@pytest.fixture(autouse=True)
def no_network_or_env(monkeypatch):
    import socket
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: pytest.fail("意外联网"))
    old_read = Path.read_text

    def guarded_read(path, *args, **kwargs):
        if path.name.startswith(".env"):
            pytest.fail("离线检查意外读取.env")
        return old_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read)


@pytest.mark.parametrize("supported,conflict,expected", [
    (True, False, "accepted"), (True, None, "pending_manual_review"),
    (None, False, "pending_manual_review"), (False, False, "rejected"),
    (None, True, "rejected"),
])
def test_manual_review(supported, conflict, expected):
    assert decide_review_status(all_claims_supported=supported, has_time_conflict=conflict) == expected


@pytest.mark.parametrize("material,quote,expected", [
    ("甲乙甲乙", "甲乙", [(0, 2), (2, 4)]), ("aaa", "aa", [(0, 2), (1, 3)]),
    ("😀中文\n中文", "中文", [(1, 3), (4, 6)]), ("原文", "不存在", []),
])
def test_all_quote_positions(material, quote, expected):
    assert locate_quote(material, quote) == expected


def test_empty_quote_rejected():
    with pytest.raises(ValueError):
        locate_quote("原文", " ")


def test_context_unknown_and_hash():
    result = build_material_context({"title": "练习", "text": "正文", "owner_user_id": "A"})
    assert result["published_on"] is None
    assert len(result["content_sha256"]) == 64
    assert describe_publication_date(None) == "发布日期未知"
    assert describe_publication_date(date(2023, 1, 1)) == "2023-01-01"
    with pytest.raises(AppError):
        build_material_context({"title": "练习", "text": "正文", "owner_user_id": ""})


@pytest.mark.parametrize("text", ["", " ", "中" * 2001])
def test_material_invalid(text):
    with pytest.raises(ValueError):
        MaterialInput(title="材料", text=text)


def test_prompt_goal_braces_and_exactly_one_invoke():
    calls = []
    values = ai.prepare_prompt_values('原文含{key}，不是指令。', '解释{term}', '{}')
    prompt = ai.build_prompt_template()
    chain = ai.build_card_chain(prompt, RunnableLambda(lambda x: calls.append(x) or {"ok": True}))
    assert calls == []
    assert chain.invoke(values) == {"ok": True}
    assert len(calls) == 1
    human = calls[0].to_messages()[-1].content
    assert '解释{term}' in human and '{key}' in human
    assert "learning_goal" in prompt.input_variables


@pytest.mark.parametrize("goal", ["", " ", "中" * 301])
def test_invalid_goal_stops_before_model(goal):
    with pytest.raises(AppError) as failure:
        ai.generate_card("材料", goal)
    assert failure.value.stage == "input"


def test_default_no_paid_call(monkeypatch):
    monkeypatch.setattr(ai.legacy.CONFIG_MODULE, "load_settings", lambda: pytest.fail("读配置"))
    with pytest.raises(AppError) as failure:
        ai.generate_card("材料", "目标")
    assert failure.value.code == "live_disabled"


@pytest.mark.parametrize("code,exception", [
    ("upstream_timeout", APITimeoutError(request=httpx.Request("POST", "https://example.invalid"))),
    ("upstream_connection", APIConnectionError(request=httpx.Request("POST", "https://example.invalid"))),
])
def test_invoke_error_does_not_validate_or_retry(monkeypatch, code, exception):
    calls = []

    def fail(value):
        calls.append(value)
        raise exception

    monkeypatch.setattr(ai.legacy.CONFIG_MODULE, "load_settings", lambda: {})
    monkeypatch.setattr(ai.legacy, "build_model", lambda settings: object())
    monkeypatch.setattr(ai.legacy, "wrap_model", lambda model: RunnableLambda(fail))
    monkeypatch.setattr(ai.legacy, "require_card", lambda *args: pytest.fail("失败后不应继续解析"))
    with pytest.raises(AppError) as failure:
        ai.generate_card("材料", "目标", live=True)
    assert failure.value.code == code and len(calls) == 1


@pytest.mark.parametrize("change", ["parse", "truncated", "quote", "empty"])
def test_raw_parsed_error_boundary(change):
    parsed = ai.LearningCard.model_validate(historical_result()["card"])
    raw = AIMessage(content=json.dumps(parsed.model_dump()), response_metadata={"finish_reason": "stop"})
    result = {"raw": raw, "parsed": parsed, "parsing_error": None}
    material = historical_material()
    if change == "parse": result["parsing_error"] = ValueError("敏感原始正文")
    if change == "truncated": raw.response_metadata["finish_reason"] = "length"
    if change == "quote": material = "没有引句"
    if change == "empty": raw.content = ""
    with pytest.raises(ValueError):
        ai.legacy.require_card(result, material)


def test_historical_candidate_immutable_owned_expiring():
    context = {"id": "material-1", **build_material_context({
        "title": "历史", "text": historical_material(), "owner_user_id": "A",
    })}
    store = CandidateStore()
    candidate = generate_candidate(context, "复习", store=store, mode="historical_replay")
    assert candidate["payload"]["source_mode"] == "historical_replay"
    assert candidate["payload"]["attempts"] == 0
    candidate["payload"]["card"]["summary"] = "被修改"
    assert store.get(candidate["candidate_id"], "A")["payload"]["card"]["summary"] != "被修改"
    with pytest.raises(AppError): store.get(candidate["candidate_id"], "B")
    expired = CandidateStore(ttl_seconds=-1)
    item = expired.put(context | {"owner_user_id": "A"})
    with pytest.raises(AppError) as failure: expired.get(item["candidate_id"], "A")
    assert failure.value.code == "candidate_expired"


def test_evidence_binds_exact_offset():
    item = EvidenceInput(claim_text="原文有中文", quote="中文", start=1, supported=True)
    result = validate_evidence("😀中文", item)
    assert result["before"] == "😀" and result["end"] == 3
    with pytest.raises(AppError): validate_evidence("不是对应原文", item)


@pytest.mark.parametrize("url", [
    "sqlite:///fake.db", "postgresql+psycopg://u@remote/fujian_stage2",
    "postgresql+psycopg://u@localhost/production",
    "postgresql+psycopg://u@localhost/fujian_stage2?host=remote",
])
def test_database_rejects_nonlocal_or_wrong_database(url):
    with pytest.raises(AppError): build_engine(url)


def test_acceptance_does_not_invent_mastery():
    result = build_acceptance_report([
        {"status": "passed", "source": "offline"}, {"status": "not_run", "source": "live"},
    ])
    assert result["counts"] == {"passed": 1, "failed": 0, "not_run": 1}
    assert result["user_mastery"] == "not_verified"
