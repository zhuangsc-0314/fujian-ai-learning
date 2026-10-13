"""2.11-A：Vue学习卡与原文对照组件（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：明确人工界面样例 → 组件字段绑定 → 原文/卡片/待核对标识
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def describe_view_contract() -> dict[str, str]:
    """TODO ASSISTANT：开课时提供组件输入约定和明确标注的人工界面样例。
    用户练习位于CardReview.vue，不要求先补这个工程辅助函数。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.11-A课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.11-A", "Vue学习卡与原文对照组件", "CardReview.vue中的信息缺口区域")


if __name__ == "__main__":
    raise SystemExit(main())
