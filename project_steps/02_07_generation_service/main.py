"""2.7：生成服务与明确结果（完整参考实现）。

输入：已读取材料上下文与目标；处理：共享业务模块；输出：成功候选或明确失败。
语法提示：with关闭Session后才invoke；raise ... from保留内部因果，页面只展示脱敏AppError。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.ai import classify_failure_stage  # noqa: E402
from learning_app.service import generate_candidate  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.7", "生成服务与明确结果")


if __name__ == "__main__":
    raise SystemExit(main())
