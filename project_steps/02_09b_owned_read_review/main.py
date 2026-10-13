"""2.9-B：归属查询与审核版本（完整参考实现）。

输入：卡片ID/服务端owner/预期审核版本；处理：共享业务模块；输出：允许读取的记录或版本冲突。
语法提示：where的多个条件共同成立；update同时限定owner和expected_version，rowcount=0表示冲突。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.service import get_owned_card  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.9-B", "归属查询与审核版本")


if __name__ == "__main__":
    raise SystemExit(main())
