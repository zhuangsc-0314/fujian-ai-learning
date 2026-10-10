"""只验收用量展示：未知不补零，零不丢失，不联网或读取配置。"""

import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch

import main as lesson


def run_case(arguments: list[str]) -> tuple[int, str]:
    """捕获本课输出；辅助检查语法可复用1.3-C的patch知识。"""
    output = io.StringIO()
    with patch.object(sys, "argv", ["main.py", *arguments]), redirect_stdout(output):
        code = lesson.main()
    return code, output.getvalue()


def main() -> int:
    """基础通过而独立合计TODO未完成返回1；全部通过返回0。"""
    outputs = {}
    with (
        patch("socket.socket.connect", side_effect=AssertionError("禁止联网")),
        patch("socket.create_connection", side_effect=AssertionError("禁止联网")),
        patch("socket.getaddrinfo", side_effect=AssertionError("禁止DNS")),
        patch("builtins.open", side_effect=AssertionError("本课不应读取文件/.env")),
        patch("io.open", side_effect=AssertionError("本课不应读取文件/.env")),
    ):
        expectations = {
            "history": ("输入token：147", "输出token：91", "结束原因：stop", "0.98秒"),
            "missing": ("输入token：未知", "输出token：未知", "结束原因：未知"),
            "partial": ("输入token：147", "输出token：未知"),
            "zero": ("输入token：0", "输出token：0"),
            "length": ("结束原因：length", "可能不完整", "不自动重发"),
        }
        for case, expected in expectations.items():
            code, printed = run_case([case])
            assert code == 0 and all(item in printed for item in expected), case
            assert "真实模型请求数：0" in printed and "费用：未核算" in printed
            assert ("历史日志回放" if case == "history" else "人工元数据边界样例") in printed
            outputs[case] = printed
            print(f"{case}：基础检查通过。")
        for arguments in (["未知案例"], ["history", "多余参数"]):
            code, printed = run_case(arguments)
            assert code == 2 and "真实模型请求数：0" in printed
            assert "输入token：" not in printed
        print("5项元数据案例及2项非法输入通过；真实请求0，未读.env。")
    expected_totals = {"history": "238", "missing": "未知", "partial": "未知", "zero": "0", "length": "未知"}
    if not all(f"合计token：{total}" in outputs[case] for case, total in expected_totals.items()):
        print("独立合计展示探针待完成；基础通过，整体退出1。")
        return 1
    print("合计展示探针通过：已知/未知/零值均正确，整体退出0。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
