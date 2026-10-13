"""PostgreSQL表与连接。Session仅在业务事务内短暂存在。"""

from datetime import datetime, timezone
import os

from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKeyConstraint, Integer, MetaData, String,
    UniqueConstraint, create_engine, text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from learning_app.domain import AppError


class Base(DeclarativeBase):
    pass


class MaterialRow(Base):
    __tablename__ = "materials"
    __table_args__ = (
        UniqueConstraint("id", "owner_user_id", name="uq_material_owner"),
        CheckConstraint("length(owner_user_id) > 0", name="ck_material_owner"),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict] = mapped_column(JSONB)


class CardRow(Base):
    __tablename__ = "cards"
    __table_args__ = (
        UniqueConstraint("owner_user_id", "candidate_id", name="uq_card_candidate"),
        ForeignKeyConstraint(
            ["material_version_id", "owner_user_id"], ["materials.id", "materials.owner_user_id"],
            name="fk_card_owned_material",
        ),
        CheckConstraint("review_version >= 1", name="ck_review_version"),
        CheckConstraint("review_status IN ('pending_manual_review','accepted','rejected')",
                        name="ck_review_status"),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_user_id: Mapped[str] = mapped_column(String(100), index=True)
    material_version_id: Mapped[str] = mapped_column(String(36))
    candidate_id: Mapped[str] = mapped_column(String(36))
    content_hash: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSONB)
    review_status: Mapped[str] = mapped_column(String(30), default="pending_manual_review")
    review_version: Mapped[int] = mapped_column(Integer, default=1)
    review: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
    )


def build_model_metadata() -> MetaData:
    return Base.metadata


def database_url() -> str:
    """不隐式读.env；数据库入口只接受明确的开发配置。"""
    value = os.environ.get("STAGE2_DATABASE_URL", "")
    if not value:
        raise AppError("database_config", "database", "请配置STAGE2_DATABASE_URL。")
    return value


def build_engine(url: str) -> Engine:
    """本阶段限制本机专用数据库，避免误操作历史生产库。"""
    try:
        parsed = make_url(url)
    except ArgumentError as exc:
        # make_url只解析字符串；异常可能带原连接串，绝不对外打印。
        raise AppError("database_config", "database", "数据库连接配置格式不正确。") from exc
    if (parsed.drivername != "postgresql+psycopg"
            or parsed.host not in {"127.0.0.1", "localhost", "::1"}
            or not (parsed.database or "").startswith("fujian_stage2")
            or parsed.query):
        raise AppError("database_config", "database", "仅允许本机fujian_stage2前缀专用库。")
    return create_engine(url, pool_pre_ping=True, hide_parameters=True,
                         connect_args={"connect_timeout": 3})


def session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


def probe_database(url: str) -> bool:
    engine = build_engine(url)
    try:
        with engine.connect() as connection:
            return connection.scalar(text("SELECT 1")) == 1
    finally:
        engine.dispose()


def describe_database_failure(error_code: str) -> str:
    return {
        "database_config": "配置步骤失败；检查本机开发库设置。",
        "database_unavailable": "连接或事务失败；检查数据库进程和迁移，不重新生成。",
    }.get(error_code, "未知数据库错误；先定位失败步骤。")
