"""2.3-B：引用定位与逐项证据记录（完整参考实现）。

输入：原文和逐字引句；处理：共享业务模块；输出：所有半开区间位置。
语法提示：find返回-1表示没找到；[start:end]包含start、不包含end；while逐次找下一处。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import locate_quote  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.3-B", "引用定位与逐项证据记录")


if __name__ == "__main__":
    raise SystemExit(main())
