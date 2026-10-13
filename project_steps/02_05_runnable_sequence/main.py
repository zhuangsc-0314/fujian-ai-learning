"""2.5：最小LCEL组合与失败定位（完整参考实现）。

输入：提示词Runnable、结构化模型Runnable；处理：共享业务模块；输出：可invoke的小链。
语法提示：竖线|调用Runnable组合接口；构建对象不会调用模型，invoke才开始运行。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.ai import build_card_chain  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.5", "最小LCEL组合与失败定位")


if __name__ == "__main__":
    raise SystemExit(main())
