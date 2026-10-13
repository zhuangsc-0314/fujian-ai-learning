"""2.8-B：数据表约束与迁移（完整参考实现）。

输入：领域数据与表约束；处理：共享业务模块；输出：两张表和Alembic版本0001。
语法提示：Mapped[str]声明ORM字段；外键限制卡片与材料owner一致，仍不是登录认证。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.storage import build_model_metadata  # noqa: E402
from learning_app.domain import require_owner  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.8-B", "数据表约束与迁移")


if __name__ == "__main__":
    raise SystemExit(main())
