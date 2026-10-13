"""2.8-A：本机PostgreSQL连接与故障定位（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：专用开发库配置 → 显式连接检查 → 脱敏连接结果
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def describe_database_failure(error_code: str) -> str:
    """根据固定错误码返回安全提示，不接受或回显完整异常/连接串。
    TODO USER：补本机服务不可达的提示和可重试条件。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.8-A课程TODO尚未实现")


def probe_database(database_url: str) -> bool:
    """TODO ASSISTANT：开课时核对驱动、配置和显式连接入口。"""
    raise NotImplementedError("2.8-A数据库连接尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.8-A", "本机PostgreSQL连接与故障定位", "describe_database_failure")


if __name__ == "__main__":
    raise SystemExit(main())
