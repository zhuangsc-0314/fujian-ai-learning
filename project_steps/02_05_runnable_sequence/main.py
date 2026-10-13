"""2.5：最小LCEL组合与失败定位（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：变量dict → prompt → 结构化模型 → raw/parsed/parsing_error结果dict
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def build_card_chain(prompt: object, structured_model: object) -> object:
    """规划返回RunnableSequence；本骨架object只是尚未收敛的接口占位。
    TODO USER：在开课核对两端类型后连接组件；不要在建链时invoke。
    业务引用/人工核对放在链外，不添加重试、记忆或Agent。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.5课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.5", "最小LCEL组合与失败定位", "build_card_chain")


if __name__ == "__main__":
    raise SystemExit(main())
