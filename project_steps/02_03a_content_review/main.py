"""2.3-A：逐项核对事实与人工审核状态（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：原文、候选及人工逐项判定 → 汇总核对结果 → pending_manual_review/accepted/rejected
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def decide_review_status(
    *, all_claims_supported: bool | None, has_time_conflict: bool | None,
) -> str:
    """输入是人工核对结论：None表示尚未核对。返回审核状态字符串。
    TODO USER：未核对、冲突和全部通过如何分别处理，独立完成。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.3-A课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.3-A", "逐项核对事实与人工审核状态", "decide_review_status")


if __name__ == "__main__":
    raise SystemExit(main())
