"""2.9-A：保存候选与事务（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：服务端已校验候选快照 → 材料/归属检查 → 事务写卡片 → ID
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def save_candidate(
    session: object, candidate_snapshot: dict[str, object],
    *, owner_user_id: str, material_version_id: str,
) -> str:
    """规划返回保存后的卡片ID；session会在开课时收敛为SQLAlchemy Session。
    TODO USER：在助手提供的映射/仓储框架中补事务部分。
    candidate_snapshot来自服务端候选存储，不能直接信任HTTP请求正文。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.9-A课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.9-A", "保存候选与事务", "save_candidate")


if __name__ == "__main__":
    raise SystemExit(main())
