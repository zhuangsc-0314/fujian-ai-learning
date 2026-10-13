"""CLI与HTTP共享的业务流程。生成与数据库事务严格分开。"""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, sessionmaker

from learning_app.ai import generate_card, prepare_prompt_values
from learning_app.domain import (
    AppError, LearningCard, MaterialInput, ReviewInput, build_material_context,
    content_hash, decide_review_status, locate_quote, require_owner, validate_evidence,
)
from learning_app.history import historical_material, historical_result
from learning_app.storage import CardRow, MaterialRow


class CandidateStore:
    """只存服务端创建的候选；取出深拷贝，防止调用者修改权威快照。"""

    def __init__(self, ttl_seconds: int = 1800, capacity: int = 100) -> None:
        self.ttl_seconds = ttl_seconds
        self.capacity = capacity
        self._items: dict[str, dict] = {}
        self._lock = Lock()

    def put(self, snapshot: dict) -> dict:
        now = datetime.now(timezone.utc)
        item = deepcopy(snapshot)
        item["candidate_id"] = str(uuid4())
        item["expires_at"] = (now + timedelta(seconds=self.ttl_seconds)).isoformat()
        with self._lock:
            self._items = {k: v for k, v in self._items.items()
                           if datetime.fromisoformat(v["expires_at"]) > now}
            if len(self._items) >= self.capacity:
                raise AppError("candidate_capacity", "candidate", "候选缓存已满；请保存或稍后重试。")
            self._items[item["candidate_id"]] = item
        return deepcopy(item)

    def get(self, candidate_id: str, owner: str) -> dict:
        with self._lock:
            item = self._items.get(candidate_id)
            if item is None or item["owner_user_id"] != owner:
                raise AppError("not_found", "candidate", "候选不存在或不可访问。")
            if datetime.fromisoformat(item["expires_at"]) <= datetime.now(timezone.utc):
                raise AppError("candidate_expired", "candidate", "候选已过期；未自动重新生成。")
            return deepcopy(item)


def get_material(session: Session, material_id: str, owner: str) -> dict:
    require_owner(owner)
    row = session.scalar(select(MaterialRow).where(
        MaterialRow.id == material_id, MaterialRow.owner_user_id == owner,
    ))
    if row is None:
        raise AppError("not_found", "material", "材料不存在或不可访问。")
    return {"id": row.id, **row.payload}


def create_material(session: Session, data: MaterialInput, owner: str) -> dict:
    payload = build_material_context({**data.model_dump(), "owner_user_id": owner})
    row = MaterialRow(id=str(uuid4()), owner_user_id=owner, payload=payload)
    session.add(row)
    session.flush()
    return {"id": row.id, **payload}


def generate_candidate(
    material_context: dict, learning_goal: str, *, store: CandidateStore,
    mode: str = "live", live_enabled: bool = False,
) -> dict:
    """数据库上下文已关闭后调用；失败没有可保存的快照。"""
    require_owner(material_context["owner_user_id"])
    prepare_prompt_values(material_context["text"], learning_goal, "{}")
    if mode == "historical_replay":
        if material_context["text"] != historical_material():
            raise AppError("invalid_input", "input", "历史回放只能对应仓库的同一份历史原文。")
        result = historical_result()
    elif mode == "live":
        result = generate_card(material_context["text"], learning_goal, live=live_enabled)
    else:
        raise AppError("invalid_input", "input", "不支持的生成模式。")
    card = LearningCard.model_validate(result["card"])
    positions = locate_quote(material_context["text"], card.evidence_quote)
    if not positions or any(not word.strip() for word in card.keywords):
        raise AppError("invalid_output", "parse_and_validate", "引用或关键词校验失败。")
    payload = {**result, "card": card.model_dump(), "learning_goal": learning_goal,
               "material_version_id": material_context["id"],
               "material_hash": material_context["content_sha256"]}
    return store.put({
        "owner_user_id": material_context["owner_user_id"],
        "material_version_id": material_context["id"],
        "content_hash": content_hash(payload), "payload": payload,
        "review_status": "pending_manual_review",
        "quote_locations": [{"start": start, "end": end} for start, end in positions],
    })


def get_owned_card(session: Session, *, card_id: str, owner_user_id: str) -> dict | None:
    require_owner(owner_user_id)
    row = session.scalar(select(CardRow).where(
        CardRow.id == card_id, CardRow.owner_user_id == owner_user_id,
    ))
    if row is None:
        return None
    material = get_material(session, row.material_version_id, owner_user_id)
    return {
        "id": row.id, "content_hash": row.content_hash, "payload": row.payload,
        "review_status": row.review_status, "review_version": row.review_version,
        "review": row.review, "material": material, "created_at": row.created_at.isoformat(),
    }


def save_candidate(
    session: Session, candidate_snapshot: dict, *, owner_user_id: str, material_version_id: str,
) -> str:
    """在调用者的事务内保存可信快照；此函数不自行commit或调用AI。"""
    require_owner(owner_user_id)
    if (candidate_snapshot["owner_user_id"] != owner_user_id
            or candidate_snapshot["material_version_id"] != material_version_id):
        raise AppError("not_found", "save", "候选不存在或不可访问。")
    material = get_material(session, material_version_id, owner_user_id)
    payload = candidate_snapshot["payload"]
    if (payload["material_hash"] != material["content_sha256"]
            or content_hash(payload) != candidate_snapshot["content_hash"]):
        raise AppError("version_conflict", "save", "材料或候选内容指纹不一致。")
    # 数据库唯一约束处理同时重复提交；不只依赖页面按钮禁用。
    statement = insert(CardRow).values(
        id=str(uuid4()), owner_user_id=owner_user_id,
        material_version_id=material_version_id, candidate_id=candidate_snapshot["candidate_id"],
        content_hash=candidate_snapshot["content_hash"], payload=payload,
        review_status="pending_manual_review", review_version=1, review={},
    ).on_conflict_do_nothing(constraint="uq_card_candidate").returning(CardRow.id)
    card_id = session.scalar(statement)
    if card_id is None:
        card_id = session.scalar(select(CardRow.id).where(
            CardRow.owner_user_id == owner_user_id,
            CardRow.candidate_id == candidate_snapshot["candidate_id"],
        ))
    return card_id


class CardService:
    """with sessions.begin()成功提交、异常回滚，离开后关闭Session。"""

    def __init__(
        self, sessions: sessionmaker[Session], *, live_enabled: bool = False,
        store: CandidateStore | None = None,
    ) -> None:
        self.sessions = sessions
        self.live_enabled = live_enabled
        self.store = store if store is not None else CandidateStore()

    def add_material(self, data: MaterialInput, owner: str) -> dict:
        with self.sessions.begin() as session:
            return create_material(session, data, owner)

    def generate(self, material_id: str, goal: str, owner: str, mode: str) -> dict:
        with self.sessions() as session:
            material = get_material(session, material_id, owner)
        return generate_candidate(material, goal, store=self.store, mode=mode,
                                  live_enabled=self.live_enabled)

    def save(self, candidate_id: str, expected_hash: str, owner: str) -> dict:
        # 已保存的候选可在服务重启后重复提交，仍返回原记录，无新生成。
        with self.sessions.begin() as session:
            existing = session.scalar(select(CardRow).where(
                CardRow.owner_user_id == owner, CardRow.candidate_id == candidate_id,
            ))
            if existing is not None:
                if existing.content_hash != expected_hash:
                    raise AppError("version_conflict", "save", "候选指纹不一致。")
                return get_owned_card(session, card_id=existing.id, owner_user_id=owner)
            snapshot = self.store.get(candidate_id, owner)
            if snapshot["content_hash"] != expected_hash:
                raise AppError("version_conflict", "save", "候选指纹不一致。")
            card_id = save_candidate(session, snapshot, owner_user_id=owner,
                                     material_version_id=snapshot["material_version_id"])
            return get_owned_card(session, card_id=card_id, owner_user_id=owner)

    def read(self, card_id: str, owner: str) -> dict:
        with self.sessions() as session:
            result = get_owned_card(session, card_id=card_id, owner_user_id=owner)
        if result is None:
            raise AppError("not_found", "read", "卡片不存在或不可访问。")
        return result

    def list_cards(self, owner: str, limit: int = 20, offset: int = 0) -> list[dict]:
        require_owner(owner)
        if not 1 <= limit <= 100 or offset < 0:
            raise AppError("invalid_input", "read", "分页参数不合法。")
        with self.sessions() as session:
            rows = session.scalars(select(CardRow).join(MaterialRow,
                (CardRow.material_version_id == MaterialRow.id)
                & (CardRow.owner_user_id == MaterialRow.owner_user_id),
            ).where(CardRow.owner_user_id == owner).order_by(
                CardRow.created_at.desc(), CardRow.id,
            ).limit(limit).offset(offset))
            return [{"id": row.id, "summary": row.payload["card"]["summary"],
                     "review_status": row.review_status} for row in rows]

    def review(self, card_id: str, data: ReviewInput, owner: str) -> dict:
        with self.sessions.begin() as session:
            current = get_owned_card(session, card_id=card_id, owner_user_id=owner)
            if current is None:
                raise AppError("not_found", "review", "卡片不存在或不可访问。")
            items = [validate_evidence(current["material"]["text"], item)
                     for item in data.evidence]
            if data.decision == "accepted":
                supported = bool(items) and data.all_claims_checked and all(
                    item["supported"] for item in items
                )
                if decide_review_status(all_claims_supported=supported,
                                        has_time_conflict=data.has_time_conflict) != "accepted":
                    raise AppError("invalid_evidence", "review", "通过需逐项证据、完整核对及无时间冲突。")
            record = {**data.model_dump(), "evidence": items,
                      "material_version_id": current["material"]["id"]}
            changed = session.execute(update(CardRow).where(
                CardRow.id == card_id, CardRow.owner_user_id == owner,
                CardRow.review_version == data.expected_version,
                CardRow.content_hash == data.expected_content_hash,
            ).values(review_status=data.decision, review_version=CardRow.review_version + 1,
                     review=record))
            if changed.rowcount != 1:
                raise AppError("version_conflict", "review", "审核版本已变化，请重新读取后核对。")
            return get_owned_card(session, card_id=card_id, owner_user_id=owner)
