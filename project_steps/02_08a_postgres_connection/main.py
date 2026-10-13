"""2.8-A：本机PostgreSQL连接（完整参考实现）。

输入：显式本机开发库连接配置；处理：共享业务模块；输出：连接成功或安全诊断。
语法提示：with engine.connect()管理连接；finally释放引擎，即使连接失败也执行。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.storage import describe_database_failure, probe_database  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.8-A", "本机PostgreSQL连接")


if __name__ == "__main__":
    raise SystemExit(main())
