"""不可变材料版本、归属外键、幂等保存及人工审核版本。"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "materials",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_user_id", sa.String(100), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.UniqueConstraint("id", "owner_user_id", name="uq_material_owner"),
        sa.CheckConstraint("length(owner_user_id) > 0", name="ck_material_owner"),
    )
    op.create_index("ix_materials_owner_user_id", "materials", ["owner_user_id"])
    op.create_table(
        "cards",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_user_id", sa.String(100), nullable=False),
        sa.Column("material_version_id", sa.String(36), nullable=False),
        sa.Column("candidate_id", sa.String(36), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("review_status", sa.String(30), nullable=False),
        sa.Column("review_version", sa.Integer(), nullable=False),
        sa.Column("review", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("owner_user_id", "candidate_id", name="uq_card_candidate"),
        sa.ForeignKeyConstraint(["material_version_id", "owner_user_id"],
                                ["materials.id", "materials.owner_user_id"],
                                name="fk_card_owned_material"),
        sa.CheckConstraint("review_version >= 1", name="ck_review_version"),
        sa.CheckConstraint("review_status IN ('pending_manual_review','accepted','rejected')",
                           name="ck_review_status"),
    )
    op.create_index("ix_cards_owner_user_id", "cards", ["owner_user_id"])


def downgrade() -> None:
    # 这是迁移能力，不由启动脚本自动执行；回退会删除本阶段两张表。
    op.drop_table("cards")
    op.drop_table("materials")
