"""普通业务规则：这里不创建模型、不连接数据库。"""

from datetime import date
from hashlib import sha256
from importlib import import_module
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


# 复用用户已通过的四字段类型，不重写历史练习。
LearningCard = import_module("project_steps.02_01_card_schema.schema").LearningCard
ReviewStatus = Literal["pending_manual_review", "accepted", "rejected"]


class AppError(Exception):
    """只携带可公开的代码/步骤；不把SDK或数据库原始异常传到页面。"""

    def __init__(self, code: str, stage: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.stage = stage
        self.message = message


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class MaterialInput(InputModel):
    title: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=1, max_length=2000)
    source_url: HttpUrl | None = None
    published_on: date | None = None


class EvidenceInput(InputModel):
    claim_text: str = Field(min_length=1, max_length=500)
    quote: str = Field(min_length=1, max_length=2000)
    start: int = Field(ge=0, strict=True)
    supported: bool


class ReviewInput(InputModel):
    expected_version: int = Field(ge=1, strict=True)
    expected_content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    decision: Literal["accepted", "rejected", "pending_manual_review"]
    note: str = Field(min_length=1, max_length=1000)
    all_claims_checked: bool = False
    has_time_conflict: bool | None = None
    evidence: list[EvidenceInput] = Field(default_factory=list, max_length=20)

def require_owner(owner_user_id: str) -> None:
    """校验业务上下文；这不是登录认证。"""
    if not isinstance(owner_user_id, str) or not owner_user_id.strip():
        raise AppError("invalid_input", "context", "缺少服务端归属上下文。")


def content_hash(value: object) -> str:
    """排序后编码使同一JSON内容产生稳定指纹；指纹不是数字签名。"""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def locate_quote(material: str, quote: str) -> list[tuple[int, int]]:
    """返回全部出现位置（包括重叠）；[start:end]不包含end位置。"""
    if not isinstance(material, str) or not isinstance(quote, str) or not quote.strip():
        raise ValueError("材料须为字符串，引句不能空白。")
    positions = []
    cursor = 0
    while (start := material.find(quote, cursor)) != -1:
        positions.append((start, start + len(quote)))
        cursor = start + 1
    return positions


def decide_review_status(
    *, all_claims_supported: bool | None, has_time_conflict: bool | None,
) -> ReviewStatus:
    """冲突优先；尚未确认的事实/时间条件都不能提升为通过。"""
    if all_claims_supported is False or has_time_conflict is True:
        return "rejected"
    if all_claims_supported is True and has_time_conflict is False:
        return "accepted"
    return "pending_manual_review"


def describe_publication_date(published_on: date | None) -> str:
    return "发布日期未知" if published_on is None else published_on.isoformat()


def build_material_context(metadata: dict[str, object]) -> dict[str, object]:
    """创建不可变版本需要的普通数据；调用者提供已确定的owner。"""
    require_owner(metadata.get("owner_user_id"))
    data = MaterialInput.model_validate({
        key: metadata[key] for key in MaterialInput.model_fields if key in metadata
    })
    return {
        **data.model_dump(mode="json"),
        "owner_user_id": metadata["owner_user_id"],
        "content_sha256": sha256(data.text.encode("utf-8")).hexdigest(),
        "version_no": 1,
    }


def validate_evidence(material: str, evidence: EvidenceInput) -> dict:
    """服务端切片，避免浏览器UTF-16下标与Python字符下标混用。"""
    end = evidence.start + len(evidence.quote)
    if material[evidence.start:end] != evidence.quote:
        raise AppError("invalid_evidence", "review", "引句与所选原文位置不一致。")
    return {
        **evidence.model_dump(), "end": end,
        "before": material[:evidence.start], "after": material[end:],
    }


def build_acceptance_report(results: list[dict]) -> dict:
    """未运行保持not_run；离线通过不替代真实生成的质量验收。"""
    counts = {"passed": 0, "failed": 0, "not_run": 0}
    for result in results:
        if result.get("status") not in counts or not result.get("source"):
            raise ValueError("每项必须包含合法status及证据source。")
        counts[result["status"]] += 1
    return {"counts": counts, "results": results, "user_mastery": "not_verified"}
