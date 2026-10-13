"""2.4：ChatPromptTemplate与参数贯通（完整参考实现）。

输入：材料、目标、schema；处理：共享业务模块；输出：system/human消息。
语法提示：dict[str,str]说明键和值都是字符串；模板变量只替换一次，材料中的花括号不再次执行。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.ai import prepare_prompt_values, build_prompt_template  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.4", "ChatPromptTemplate与参数贯通")


if __name__ == "__main__":
    raise SystemExit(main())
