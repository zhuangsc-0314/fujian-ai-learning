"""2.9-A：保存候选与事务（完整参考实现）。

输入：服务端候选快照/归属/材料版本；处理：共享业务模块；输出：已保存ID或回滚。
语法提示：with sessions.begin()成功commit、异常rollback；ON CONFLICT由唯一约束处理并发重复。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.service import save_candidate  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.9-A", "保存候选与事务")


if __name__ == "__main__":
    raise SystemExit(main())
