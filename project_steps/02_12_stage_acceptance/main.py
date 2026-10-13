"""2.12：阶段2综合验收与独立调试（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：固定材料/故障案例 → 生成或明确失败、核对、保存、重开 → 分层验收报告
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def build_acceptance_report(
    results: list[dict[str, object]],
) -> dict[str, object]:
    """输入每个案例的模式、预期、实际、退出码和证据位置，输出分类汇总。
    TODO USER：not_run与failed不能计入passed；费用未知不能填0。
    不能仅靠本函数汇总得出多人可上线结论。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.12课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.12", "阶段2综合验收与独立调试", "build_acceptance_report")


if __name__ == "__main__":
    raise SystemExit(main())
