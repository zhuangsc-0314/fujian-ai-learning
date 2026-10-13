"""2.11-A：Vue学习卡原文对照（完整参考实现）。

输入：card/material props；处理：共享业务模块；输出：安全文本视图。
语法提示：defineProps是组件输入契约；{{ }}文本绑定自动转义；不使用v-html显示原文。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def describe_view_contract() -> dict[str, str]:
    return {"component": "web/src/CardReview.vue", "input": "card/material", "output": "安全文本视图"}

from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.11-A", "Vue学习卡原文对照")


if __name__ == "__main__":
    raise SystemExit(main())
