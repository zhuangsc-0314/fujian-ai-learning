"""专用PostgreSQL实测；未配置时明确skip，绝不换SQLite冒充。"""

from concurrent.futures import ThreadPoolExecutor
import os
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from learning_app.api import DEMO_OWNER, create_app
from learning_app.domain import AppError, MaterialInput, ReviewInput
from learning_app.history import historical_material
from learning_app.service import CardService, create_material
from learning_app.storage import CardRow, MaterialRow, build_engine, session_factory


@pytest.fixture
def service():
    url = os.environ.get("STAGE2_TEST_DATABASE_URL")
    if not url:
        pytest.skip("未配置专用PostgreSQL测试库；未实测")
    engine = build_engine(url)
    if not engine.url.database.startswith("fujian_stage2_test"):
        pytest.fail("测试只允许fujian_stage2_test前缀库")
    yield CardService(session_factory(engine))
    engine.dispose()


def make_candidate(service, owner):
    context = service.add_material(MaterialInput(title="历史验证", text=historical_material()), owner)
    return service.generate(context["id"], "整理原文", owner, "historical_replay")


def test_save_reopen_duplicate_and_owner(service):
    owner = f"test-{uuid4()}"
    candidate = make_candidate(service, owner)
    saved = service.save(candidate["candidate_id"], candidate["content_hash"], owner)
    fresh = CardService(service.sessions)
    assert fresh.read(saved["id"], owner)["payload"] == saved["payload"]
    assert fresh.save(candidate["candidate_id"], candidate["content_hash"], owner)["id"] == saved["id"]
    assert saved["review_status"] == "pending_manual_review"
    assert saved["payload"]["attempts"] == 0
    assert fresh.list_cards("other-owner") == []
    with pytest.raises(AppError): fresh.read(saved["id"], "other-owner")
    with pytest.raises(AppError): fresh.save(candidate["candidate_id"], "0" * 64, owner)


def test_concurrent_duplicate_save(service):
    owner = f"concurrent-{uuid4()}"
    candidate = make_candidate(service, owner)
    with ThreadPoolExecutor(max_workers=4) as executor:
        ids = list(executor.map(lambda _: service.save(
            candidate["candidate_id"], candidate["content_hash"], owner,
        )["id"], range(4)))
    assert len(set(ids)) == 1
    assert len(service.list_cards(owner)) == 1


def test_transaction_rollback_and_owned_foreign_key(service):
    owner = f"rollback-{uuid4()}"
    with pytest.raises(RuntimeError):
        with service.sessions.begin() as session:
            created = create_material(session, MaterialInput(title="回滚", text="原文"), owner)
            raise RuntimeError("测试事务中止")
    with service.sessions() as session:
        assert session.scalar(select(MaterialRow).where(MaterialRow.id == created["id"])) is None
    candidate = make_candidate(service, owner)
    with pytest.raises(IntegrityError):
        with service.sessions.begin() as session:
            session.add(CardRow(id=str(uuid4()), owner_user_id="different-owner",
                material_version_id=candidate["material_version_id"], candidate_id=str(uuid4()),
                content_hash=candidate["content_hash"], payload=candidate["payload"]))
            session.flush()


def test_review_exact_version_and_required_evidence(service):
    owner = f"review-{uuid4()}"
    candidate = make_candidate(service, owner)
    saved = service.save(candidate["candidate_id"], candidate["content_hash"], owner)
    base = {"expected_version": 1, "expected_content_hash": saved["content_hash"],
            "decision": "accepted", "note": "已逐项核对历史材料，未知保持未知。",
            "all_claims_checked": True, "has_time_conflict": False}
    with pytest.raises(AppError): service.review(saved["id"], ReviewInput(**base), owner)
    quote = saved["material"]["text"]
    request = ReviewInput(**base, evidence=[{"claim_text": "摘要与材料范围及题型一致",
                                            "quote": quote, "start": 0, "supported": True}])
    reviewed = service.review(saved["id"], request, owner)
    assert reviewed["review_status"] == "accepted" and reviewed["review_version"] == 2
    assert reviewed["review"]["material_version_id"] == saved["material"]["id"]
    with pytest.raises(AppError) as failure: service.review(saved["id"], request, owner)
    assert failure.value.code == "version_conflict"


def test_api_full_flow_and_error_boundaries(service):
    with TestClient(create_app(service, demo=True), base_url="http://127.0.0.1:8000") as client:
        headers = {"X-Stage2-Local": "1"}
        assert client.post("/api/v1/materials", json={}).status_code == 403
        assert client.get("/api/v1/info", headers={"Origin": "https://evil.invalid"}).status_code == 403
        assert client.get("/api/v1/info", headers={"Host": "evil.invalid"}).status_code == 403
        assert client.get("/api/v1/info", headers={"Sec-Fetch-Site": "cross-site"}).status_code == 403
        assert client.post("/api/v1/materials", headers=headers,
                           json={"title": "", "text": "", "owner_user_id": "fake"}).status_code == 422
        context = client.post("/api/v1/materials", headers=headers,
                              json={"title": "API历史材料", "text": historical_material()}).json()
        assert context["owner_user_id"] == DEMO_OWNER
        request = {"material_version_id": context["id"], "learning_goal": "复习"}
        assert client.post("/api/v1/card-candidates", headers=headers, json=request).status_code == 403
        candidate = client.post("/api/v1/card-candidates", headers=headers,
                               json={**request, "mode": "historical_replay"}).json()
        body = {"candidate_id": candidate["candidate_id"],
                "expected_content_hash": candidate["content_hash"]}
        saved = client.post("/api/v1/cards", headers=headers, json=body).json()
        assert client.get(f'/api/v1/cards/{saved["id"]}').json()["id"] == saved["id"]
        assert client.post("/api/v1/cards", headers=headers, json=body).json()["id"] == saved["id"]
        assert client.get("/api/v1/cards?limit=101").status_code == 422
        assert client.get("/api/v1/cards/not-existing").status_code == 404
        review = {"decision": "rejected", "expected_version": 1,
                  "expected_content_hash": saved["content_hash"], "note": "测试：需要更多逐项依据。"}
        assert client.patch(f'/api/v1/cards/{saved["id"]}/review', headers=headers,
                            json=review).json()["review_status"] == "rejected"
        assert client.patch(f'/api/v1/cards/{saved["id"]}/review', headers=headers,
                            json=review).status_code == 409


def test_non_demo_cannot_start(service):
    with pytest.raises(AppError): create_app(service)
