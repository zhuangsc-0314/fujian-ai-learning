"""2.3-A：逐项核对事实与人工审核状态（完整参考实现）。

输入：人工结论/时间冲突；处理：共享业务模块；输出：审核状态。
语法提示：关键字参数*使调用时明确写参数名；bool | None把未知和否区分开。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import decide_review_status  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.3-A", "逐项核对事实与人工审核状态")


if __name__ == "__main__":
    raise SystemExit(main())
