"""2.10：本机FastAPI与错误响应（完整参考实现）。

输入：受校验HTTP请求；处理：共享业务模块；输出：服务结果和HTTP状态码。
语法提示：@app.post注册路由；请求模型拒绝额外owner字段；上下文由服务端提供。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.api import map_error_status, create_app  # noqa: E402
from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.10", "本机FastAPI与错误响应")


if __name__ == "__main__":
    raise SystemExit(main())
