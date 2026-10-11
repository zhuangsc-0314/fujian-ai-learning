"""离线核对费用公式、未知/零/非法边界；--exercise检查用户预算函数。"""

import io
import sys
from contextlib import redirect_stdout
from decimal import Decimal
from unittest.mock import patch

import main as lesson


def main() -> int:
    """基础通过返回0；独立练习未完成返回1；非法参数返回2。"""
    if sys.argv[1:] not in ([], ["--exercise"]):
        print("仅支持无参数或--exercise；真实请求0。")
        return 2
    with patch("socket.socket.connect", side_effect=AssertionError("禁止联网")):
        assert lesson.estimate_cost_range(147, 59, "off-peak") == (
            Decimal("0.000035841"), Decimal("0.00005745"),
        )
        assert lesson.estimate_cost_range(147, 59, "peak") == (
            Decimal("0.000071682"), Decimal("0.00011490"),
        )
        assert lesson.estimate_cost_range(0, 0, "off-peak") == (Decimal(0), Decimal(0))
        assert lesson.estimate_cost_range(None, 59, "off-peak") is None
        assert lesson.estimate_cost_range(147, None, "off-peak") is None
        for args in ((-1, 59, "off-peak"), (True, 59, "off-peak"), (147, 59, "bad")):
            try:
                lesson.estimate_cost_range(*args)
            except ValueError:
                pass
            else:
                raise AssertionError("非法用量/时段应拒绝")
        print("费用区间8项通过：两种价目、零值、左右未知和非法输入。")

        for price, calls in ((Decimal("NaN"), 100), (Decimal("1"), -1), (Decimal("1"), True)):
            try:
                lesson.estimate_daily_budget(price, calls)
            except ValueError:
                pass
            else:
                raise AssertionError("非法预算参数应拒绝")
        print("预算参数3项通过：非有限金额、负次数、布尔次数拒绝。")

        for args, expected in (([], 0), (["unknown"], 0), (["zero"], 0), (["bad"], 2)):
            output = io.StringIO()
            with patch.object(sys, "argv", ["main.py", *args]), redirect_stdout(output):
                assert lesson.main() == expected
            assert "真实请求0" in output.getvalue()
        print("入口4项通过；共15项基础检查通过，不读取.env、真实请求0。")

        if sys.argv[1:]:
            for calls in (100, 0, 1):
                price = Decimal("0.00005745")
                if lesson.estimate_daily_budget(price, calls) != price * calls:
                    print("独立每日预算练习未完成；基础通过，练习探针退出1。")
                    return 1
            print("独立每日预算3项通过；用户运行/解释须另记录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
