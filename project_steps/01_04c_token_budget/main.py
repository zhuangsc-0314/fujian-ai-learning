r"""1.4-C：用已有用量与官方价格快照做离线情景估算。

运行：python main.py [off-peak|peak|unknown|zero]
不读.env、不联网；输出美元估算，不代表账户实际扣费或预算强制限制。
"""

import sys
from decimal import Decimal


PRICE_CHECKED_DATE = "2026-10-11"
MILLION = Decimal("1000000")
# 官方美元/百万token快照。Decimal从字符串创建，避免先经过二进制浮点。
RATES = {
    "off-peak": {
        "input_hit": Decimal("0.003"),
        "input_miss": Decimal("0.15"),
        "output": Decimal("0.6"),
    },
    "peak": {
        "input_hit": Decimal("0.006"),
        "input_miss": Decimal("0.3"),
        "output": Decimal("1.2"),
    },
}


def estimate_cost_range(
    input_tokens: int | None, output_tokens: int | None, period: str,
) -> tuple[Decimal, Decimal] | None:
    """缓存明细未知：返回全命中/全未命中的理论费用界；缺用量返回None。"""
    if period not in RATES:
        raise ValueError("时段只支持off-peak或peak。")
    for count in (input_tokens, output_tokens):
        # bool是int的子类，这里只接受真正的非负整数或未知None。
        if count is not None and (type(count) is not int or count < 0):
            raise ValueError("token数须为非负整数或None。")
    if input_tokens is None or output_tokens is None:
        return None
    rates = RATES[period]
    output_cost = Decimal(output_tokens) * rates["output"]
    lower = (Decimal(input_tokens) * rates["input_hit"] + output_cost) / MILLION
    upper = (Decimal(input_tokens) * rates["input_miss"] + output_cost) / MILLION
    return lower, upper


def estimate_daily_budget(
    per_call_upper: Decimal, calls_per_day: int,
) -> Decimal | None:
    """固定价目与相同token规模下，计算每日全未命中情景预算。"""
    if (
        not isinstance(per_call_upper, Decimal)
        or not per_call_upper.is_finite()
        or per_call_upper < 0
    ):
        raise ValueError("单次估算须为有限非负Decimal。")
    if type(calls_per_day) is not int or calls_per_day < 0:
        raise ValueError("每日次数须为非负整数。")
    # TODO 1.4-C（你独立完成）：返回单次上界乘每日次数。
    # 校验已提供；不要硬编码100次的结果，不把预算当成真实扣费。
    return None


def main() -> int:
    """离线展示返回0；非法参数返回2；独立预算未完成仍可观察费用区间。"""
    if len(sys.argv) > 2:
        print("只接受一个案例名；真实请求0。")
        return 2
    case = sys.argv[1] if len(sys.argv) == 2 else "off-peak"
    if case not in ("off-peak", "peak", "unknown", "zero"):
        print("案例名须为off-peak/peak/unknown/zero；真实请求0。")
        return 2
    period = "peak" if case == "peak" else "off-peak"
    # 147/59来自1.4-B用户long真实记录；unknown/zero是人工边界用量。
    input_tokens, output_tokens = 147, 59
    if case == "unknown":
        input_tokens = None
    elif case == "zero":
        input_tokens, output_tokens = 0, 0
    print(f"离线估算：deepseek-flash；美元价目核对日{PRICE_CHECKED_DATE}。")
    print(f"价目情景：{period}；历史用量/人工边界，不是本次API响应。")
    costs = estimate_cost_range(input_tokens, output_tokens, period)
    if costs is None:
        print("用量未知，费用未知；不能按0估算。")
    else:
        lower, upper = costs
        print(f"单次理论区间：USD {lower:.9f}—{upper:.9f}。")
        budget = estimate_daily_budget(upper, 100)
        if budget is None:
            print("每日100次同规模预算：独立练习待完成。")
        else:
            print(f"每日100次同规模/全未命中情景预算：USD {budget:.9f}。")
    print("缓存明细/账户币种/调用时段/账单未核对；估算不是实际扣费。")
    print("本次真实请求0，不读取.env；本课不实施服务端额度限制。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
