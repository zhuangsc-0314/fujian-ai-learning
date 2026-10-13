"""2.6：材料来源、版本与归属（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：用户提供的材料元数据 → 本地校验/生成版本标识 → 与卡片分离的材料上下文
"""

import sys
from datetime import date
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def describe_publication_date(published_on: date | None) -> str:
    """输入为业务层解析后的日期或None，返回展示字符串。
    TODO USER：保留未知语义，不把今天当作未知发布日期。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.6课程TODO尚未实现")


def build_material_context(metadata: dict[str, object]) -> dict[str, object]:
    """TODO ASSISTANT：开课时提供元数据schema、版本和归属边界。"""
    raise NotImplementedError("2.6材料上下文尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.6", "材料来源、版本与归属", "describe_publication_date")


if __name__ == "__main__":
    raise SystemExit(main())
