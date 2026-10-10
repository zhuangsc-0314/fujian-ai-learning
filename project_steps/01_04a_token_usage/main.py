r"""1.4-A：只读历史用量与人工边界样例，不调用模型、不读取.env。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04a_token_usage\main.py history
history来自1.2用户真实日志；其他案例是人工元数据样例，没有AI回答。
"""

import sys


# 手工摘录公开教学日志，不是本次API响应，也不是从字符数估算token。
# 原日志没有模型名/请求ID；缺失证据不能由当前配置或AI补造。
HISTORICAL_USAGE = {"input_tokens": 147, "output_tokens": 91, "total_tokens": 238}
CASES = {
    "history": (HISTORICAL_USAGE, {"finish_reason": "stop"}),
    "missing": (None, {}),
    "partial": ({"input_tokens": 147}, {}),
    "zero": ({"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}, {}),
    "length": (None, {"finish_reason": "length"}),
}


def show_count(value: int | None) -> str:
    """展示有证据的计数；None表示未知，数字0仍是已知值。"""
    # 不能写成value or '未知'：0也是假值，会被错误当成缺失。
    return "未知" if value is None else str(value)


def show_metadata(usage: dict[str, int] | None, response: dict[str, str]) -> None:
    """输入用量/响应元数据，输出允许字段；不打印正文或整个响应。"""
    # 真实1.2调用返回reply.usage_metadata与reply.response_metadata。
    # 这里仅用字典回放字段，未构造AIMessage或HTTP响应。
    counts = {} if usage is None else usage
    # .get('字段')：字段缺失时返回None，不会像counts['字段']那样抛KeyError。
    # get提供的默认值只处理缺失，不能把缺失token数设为0。
    print(f"输入token：{show_count(counts.get('input_tokens'))}")
    print(f"输出token：{show_count(counts.get('output_tokens'))}")
    print(f"合计token：{show_count(counts.get('total_tokens'))}")
    # 1.4-A独立修改已完成：读取total_tokens，缺失为未知，零值保留。
    print(f"结束原因：{response.get('finish_reason', '未知')}")
    if response.get("finish_reason") == "length":
        print("输出达到token上限，内容可能不完整；本次不自动重发。")
    print("费用：未核算；用量缺失不代表免费，计费须核对供应商价目与账单。")


def main() -> int:
    """展示案例返回0；非法参数返回2；本次真实请求始终0。"""
    if len(sys.argv) > 2:
        print("本课只接受一个案例名；真实模型请求数：0。")
        return 2
    case = sys.argv[1] if len(sys.argv) == 2 else "history"
    if case not in CASES:
        print("案例名不合法：history/missing/partial/zero/length；真实模型请求数：0。")
        return 2
    if case == "history":
        print("[历史日志回放] 来源：1.2 USER_RUN_RESULTS，2026-10-10用户提供。")
        print("材料78字符；请求及响应处理耗时0.98秒；模型名/请求ID未记录，未知。")
    else:
        print("[人工元数据边界样例] 不是供应商响应，不含模型正文。")
    usage, response = CASES[case]
    show_metadata(usage, response)
    print("本次真实模型请求数：0；未读取.env。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
