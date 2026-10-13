"""2.3-A独立调用练习：只用人工输入，不读取.env或调用模型。

完整业务函数已在learning_app/domain.py实现；本文件练习如何正确调用它。
用户只修改review_unknown_time；其余部分提供正常/不合格案例及运行反馈。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import decide_review_status  # noqa: E402


def review_unknown_time() -> str:
    """用户独立练习：事实已有依据，但还没有核实时间适用性。"""
    # TODO USER：调用decide_review_status，按名字传入两个人工结论。
    # 返回业务函数给出的状态，不直接硬编码某个状态字符串。
    # 参数含义请先读README和domain.py；保留正常/不合格演示代码。
    raise NotImplementedError("请独立完成时间适用性尚未核实的调用。")


def main() -> int:
    """参考案例先运行，随后运行用户边界案例；未完成或结果不符退出1。"""
    print("人工输入的离线练习；模型请求0，不读取.env。")
    normal = decide_review_status(all_claims_supported=True, has_time_conflict=False)
    print("正常：事实有依据，已核实无时间冲突 →", normal)

    unsupported = decide_review_status(all_claims_supported=False, has_time_conflict=False)
    print("不合格：发现事实无依据 →", unsupported)

    try:
        status = review_unknown_time()
    except NotImplementedError:
        print("独立边界案例尚未完成；参考案例运行不代表用户练习通过。")
        return 1

    print("我的边界案例：事实已有依据，时间适用性尚未核实 →", status)
    if status != "pending_manual_review":
        print("边界结果不符合预期；请先判断失败在哪个条件，不自动改业务规则。")
        return 1
    print("运行结果符合预期；独立代码和解释还需评审，不自动登记已掌握。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
