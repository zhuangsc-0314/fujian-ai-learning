"""2.4：ChatPromptTemplate与参数贯通（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：material/learning_goal/schema_json → 模板填值 → system/human消息预览
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def prepare_prompt_values(
    material: str, learning_goal: str, schema_json: str,
) -> dict[str, str]:
    """返回模板需要的变量字典，字段约定见README。
    TODO USER：完成目标校验和变量贯通；不在这里创建模型或读Key。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.4课程TODO尚未实现")


def build_prompt_template() -> object:
    """TODO ASSISTANT：开课时提供ChatPromptTemplate骨架并核对版本接口。"""
    raise NotImplementedError("2.4消息模板尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.4", "ChatPromptTemplate与参数贯通", "prepare_prompt_values")


if __name__ == "__main__":
    raise SystemExit(main())
