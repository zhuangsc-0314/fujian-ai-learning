"""2.9-B：归属查询与审核快照绑定（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：服务端上下文、卡片ID/预期版本 → 限定归属查询/状态变更 → 结果或冲突
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def get_owned_card(
    session: object, *, card_id: str, owner_user_id: str,
) -> dict[str, object] | None:
    """规划返回当前业务身份可读的卡片，不可读或不存在返回None。
    TODO USER：在数据库查询中加归属限制，不能查全量后仅隐藏UI。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.9-B课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.9-B", "归属查询与审核快照绑定", "get_owned_card")


if __name__ == "__main__":
    raise SystemExit(main())
