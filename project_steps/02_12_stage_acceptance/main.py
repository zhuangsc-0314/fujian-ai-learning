"""2.12：综合验收与独立调试（完整参考实现）。

输入：实测结果及证据来源；处理：共享业务模块；输出：passed/failed/not_run报告。
语法提示：字典计数不把not_run变成passed；报告标明source和user_mastery。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import build_acceptance_report  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.12", "综合验收与独立调试")


if __name__ == "__main__":
    raise SystemExit(main())
