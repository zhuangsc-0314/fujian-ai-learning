"""离线验收记录字段及失败停止；--exercise额外检查用户差值TODO。

人工元数据没有AI正文；patch只替换入口，不模拟供应商HTTP或计费。
"""

import io
import json
import sys
from contextlib import redirect_stdout
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import main as comparison


def check_records(lesson: ModuleType) -> None:
    """人工元数据检查零/缺失/部分字段及敏感字段排除。"""
    marker = "OFFLINE_PRIVATE_DETAIL_MUST_NOT_LEAK"
    usages = (
        None, {}, {"input_tokens": 0}, {"input_tokens": 12, "total_tokens": 20},
    )
    for usage in usages:
        reply = SimpleNamespace(
            usage_metadata=usage,
            response_metadata={
                "model_name": "offline-model",
                "headers": {"x-request-id": "offline-request", "authorization": marker},
                "finish_reason": "stop", "private_detail": marker,
            },
            content=marker, id="completion-id-is-not-request-id",
        )
        record = lesson.collect_call_record(reply, "requested-model", 0.1234, 9)
        assert record["input_tokens"] == (usage or {}).get("input_tokens")
        assert record["output_tokens"] is None
        assert record["total_tokens"] == (usage or {}).get("total_tokens")
        assert record["request_id"] == "offline-request"
        assert record["returned_model"] == "offline-model"
        assert marker not in json.dumps(record)
    reply = SimpleNamespace(usage_metadata=None, response_metadata={}, id="completion-only")
    record = lesson.collect_call_record(reply, "requested-model", 0.0, 9)
    assert record["returned_model"] is None and record["request_id"] is None
    assert record["elapsed_seconds"] == 0.0
    print("5项元数据边界通过：缺失未知、明确零保留、无正文/完整头、请求ID不冒用。")


def check_sequence(lesson: ModuleType) -> None:
    """验证调度两次上限和失败停止，不调用模型入口。"""
    for failure_at, expected_calls in ((1, 1), (2, 2), (0, 2)):
        calls = []

        def offline_main(*, material_path, records):
            calls.append(material_path)
            if len(calls) == failure_at:
                return 1
            records.append({"input_tokens": 0})
            return 0

        with (
            patch.object(lesson, "main", side_effect=offline_main),
            redirect_stdout(io.StringIO()),
        ):
            code, records = comparison.run_comparison(lesson)
        assert len(calls) == expected_calls
        assert code == (1 if failure_at else 0)
        assert len(records) == expected_calls - (1 if failure_at else 0)
    print("3项调度检查通过：最多两次，首次/第二次失败停止，无自动重跑。")


def check_integration(lesson: ModuleType) -> None:
    """原1.2入口摘取元数据；不生成AI正文，正文展示被替换。"""
    marker = "OFFLINE_CONFIG_NOT_A_KEY"
    settings = {
        "DEEPSEEK_API_KEY": marker,
        "DEEPSEEK_MODEL": "offline-model",
        "DEEPSEEK_API_BASE": "https://api.deepseek.com",
    }
    reply = SimpleNamespace(usage_metadata={"input_tokens": 0}, response_metadata={})
    for records in (None, []):
        output = io.StringIO()
        with (
            patch.object(lesson, "load_settings", return_value=settings),
            patch.object(lesson, "ChatDeepSeek") as constructor,
            patch.object(lesson, "show_response") as show,
            redirect_stdout(output),
        ):
            constructor.return_value.invoke.return_value = reply
            code = lesson.main(material_path=comparison.MATERIALS[0][1], records=records)
        assert code == 0 and marker not in output.getvalue()
        show.assert_called_once_with(reply)
        arguments = constructor.call_args.kwargs
        assert arguments["include_response_headers"] == (records is not None)
        assert constructor.call_args.kwargs["max_retries"] == 0
        if records is not None:
            assert len(records) == 1 and records[0]["input_tokens"] == 0
            assert records[0]["total_tokens"] is None
    print("2项原入口集成通过：默认不启用头、比较摘取记录；模型/正文被替换。")


def check_exercise() -> int:
    """只检查用户函数；已知/零/缺失/部分字段，不能以0代替未知。"""
    cases = (
        (10, 20, 10), (0, 0, 0), (0, 5, 5), (None, 20, None), (10, None, None),
    )
    for short, long, expected in cases:
        actual = comparison.input_token_difference(
            {"input_tokens": short}, {"input_tokens": long},
        )
        if actual != expected:
            print("独立差值练习未通过；基础骨架通过不代表TODO已完成。")
            return 1
    assert comparison.input_token_difference({}, {"input_tokens": 20}) is None
    print("独立差值练习6项通过；不代表真实调用或完整解释已验收。")
    return 0


def main() -> int:
    """离线基础检查与可选练习探针。"""
    if sys.argv[1:] not in ([], ["--exercise"]):
        print("检查脚本仅支持无参数或--exercise；请求0。")
        return 2
    lesson = comparison.load_lesson()
    with (
        patch("socket.socket.connect", side_effect=AssertionError("禁止联网")),
        patch("socket.getaddrinfo", side_effect=AssertionError("禁止DNS")),
        patch.object(lesson, "load_settings", side_effect=AssertionError("不应读取配置")),
        patch.object(lesson, "ChatDeepSeek", side_effect=AssertionError("不应创建模型")),
    ):
        check_records(lesson)
        check_sequence(lesson)
        check_integration(lesson)
        with patch.object(comparison, "load_lesson", return_value=lesson):
            cases = (([], 0), (["--bad"], 2), (["--live", "extra"], 2))
            for args, expected in cases:
                with (
                    patch.object(sys, "argv", ["main.py", *args]),
                    redirect_stdout(io.StringIO()),
                ):
                    assert comparison.main() == expected
        print("3项入口检查通过：默认预览/非法参数不读配置、不创建模型。")
    print("共13项基础离线检查通过；真实请求0，未读取.env。")
    return check_exercise() if sys.argv[1:] else 0


if __name__ == "__main__":
    raise SystemExit(main())
