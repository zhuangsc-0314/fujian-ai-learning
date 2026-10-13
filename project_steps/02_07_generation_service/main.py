"""2.7：生成服务与明确的结果对象（规划骨架，尚未实现）。

本次仅提供函数契约和独立练习位置。默认运行只显示说明，不运行TODO。
输入/处理/输出：材料上下文/目标 → AI适配器生成、校验 → 候选ID、内容、用量与错误阶段
"""

import sys
from pathlib import Path


# 固定仓库路径只用于导入课程说明工具；它不会导入模型或读取配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project_steps.stage2_scaffold import preview_lesson  # noqa: E402


def classify_failure_stage(error_code: str) -> str:
    """返回固定的失败步骤名称；未知code要明确归为未知而非成功。
    TODO USER：开课时根据约定补结构化解析失败分支。
    """
    # 未实现必须明确失败，不能先返回空数据伪装业务成功。
    raise NotImplementedError("2.7课程TODO尚未实现")


def generate_candidate(
    material_context: dict[str, object], learning_goal: str,
) -> dict[str, object]:
    """TODO ASSISTANT：提取共享服务；候选在服务端保存快照，不信任客户端回传正文。"""
    raise NotImplementedError("2.7生成服务尚未实现")


def main() -> int:
    """仅供浏览未来课程说明；实际练习须在该课分配后实现。"""
    return preview_lesson("2.7", "生成服务与明确的结果对象", "classify_failure_stage")


if __name__ == "__main__":
    raise SystemExit(main())
