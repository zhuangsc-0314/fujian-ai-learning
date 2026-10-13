"""2.6：材料来源、版本与归属（完整参考实现）。

输入：来源/日期/正文/服务端owner；处理：共享业务模块；输出：版本及内容指纹。
语法提示：date | None保留未知；**字典展开合并字段；sha256是指纹而非认证。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import describe_publication_date, build_material_context  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.6", "材料来源、版本与归属")


if __name__ == "__main__":
    raise SystemExit(main())
