"""2.10：本机FastAPI入口与错误响应（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：本机HTTP请求 → 输入模型/本机上下文 → 业务服务 → 候选/保存/查询响应
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def map_error_status(error_code: str) -> int:
    """按开课约定返回HTTP状态码，未知错误不能映射为200。
    TODO USER：补指定错误分支；认证依赖不能由客户端owner字段替代。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.10课程TODO尚未实现")


def create_app() -> object:
    """TODO ASSISTANT：开课时创建FastAPI入口并收敛返回类型。"""
    raise NotImplementedError("2.10本机API尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.10", "本机FastAPI入口与错误响应", "map_error_status")


if __name__ == "__main__":
    raise SystemExit(main())
