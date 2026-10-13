"""2.8-B：数据表、约束与数据库迁移（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：材料/卡片数据设计 → ORM与首个迁移 → 专用空开发库表结构
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def require_owner(owner_user_id: str) -> None:
    """检查业务层提供的owner非空，失败抛ValueError；成功不返回业务数据。
    TODO USER：只做本地非空检查，不能把它当身份认证。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.8-B课程TODO尚未实现")


def build_model_metadata() -> object:
    """TODO ASSISTANT：开课时实现SQLAlchemy映射与Alembic首个迁移。"""
    raise NotImplementedError("2.8-B表与迁移尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.8-B", "数据表、约束与数据库迁移", "require_owner")


if __name__ == "__main__":
    raise SystemExit(main())
