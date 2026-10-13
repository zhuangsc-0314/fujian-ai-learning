"""2.3-B：引用定位与逐项证据记录（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：不可变原文、连续引句 → 查找所有出现位置 → [(start, end), ...]及人工事实关联
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def locate_quote(material: str, quote: str) -> list[tuple[int, int]]:
    """返回所有半开区间：material[start:end]应等于quote。
    TODO USER：查找多个位置与空引句处理；不存在时返回空列表。
    位置匹配不证明语义有据；必须绑定材料版本，前端不自行换算中文下标。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.3-B课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.3-B", "引用定位与逐项证据记录", "locate_quote")


if __name__ == "__main__":
    raise SystemExit(main())
