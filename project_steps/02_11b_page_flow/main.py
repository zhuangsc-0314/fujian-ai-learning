"""2.11-B：页面请求与保存后重开（完整参考实现）。

输入：fetch请求和用户动作；处理：共享业务模块；输出：加载/错误/保存/重开状态。
语法提示：async函数返回Promise；await等待请求；finally恢复busy；URL记录已保存ID。
本课独立迁移练习见README，不把参考代码运行当作用户已掌握。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def describe_page_contract() -> dict[str, str]:
    return {"page": "web/src/App.vue", "api": "web/src/api.ts", "reopen": "?card=ID"}

from project_steps.stage2_reference import run_reference  # noqa: E402


def main() -> int:
    """共享演示入口；业务函数已实现，可继续阅读其中文注释。"""
    return run_reference("2.11-B", "页面请求与保存后重开")


if __name__ == "__main__":
    raise SystemExit(main())
