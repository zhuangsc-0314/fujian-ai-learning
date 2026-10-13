"""2.11-B：页面请求、失败状态与保存后重开（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：用户操作 → 本机API → loading/ready/error → 显式保存/按ID重开
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def describe_page_contract() -> dict[str, str]:
    """TODO ASSISTANT：开课时提供页面状态约定；用户练习位于api.ts。
    真实生成按钮与普通读取区分；只有明确live操作才允许模型请求。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.11-B课程TODO尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.11-B", "页面请求、失败状态与保存后重开", "api.ts中的fetchCard")


if __name__ == "__main__":
    raise SystemExit(main())
