r"""离线运行1.2的main，在invoke边界注入异常；不读.env、不联网。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03c_call_boundary\main.py
先阅读CASES与README；辅助函数不是新的模型服务，也不生成AI回答。
"""

import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    InternalServerError,
    RateLimitError,
)


RAW_MARKER = "OFFLINE_DETAIL_MUST_NOT_LEAK"
KEY_MARKER = "OFFLINE_PLACEHOLDER_NOT_A_KEY"


def status_error(error_class: type, status_code: int) -> Exception:
    """用SDK需要的占位字段构造异常；不是HTTP响应，不联网。"""
    response = Mock(name="offline_response_placeholder")
    response.request = Mock(name="offline_request_placeholder")
    response.status_code = status_code
    response.headers = {}
    return error_class(RAW_MARKER, response=response, body={"message": RAW_MARKER})


# 每项是一个元组：(案例名，注入的异常对象，期望的安全提示)。
# 外层[]是列表，可以增加案例；status_error调用只构造异常，不抛出它。
CASES = [
    ("auth", status_error(AuthenticationError, 401), "API认证失败"),
    ("rate-limit", status_error(RateLimitError, 429), "API请求受限"),
    ("timeout", APITimeoutError(request=Mock()), "服务端是否执行未知"),
    ("connection", APIConnectionError(message=RAW_MARKER, request=Mock()), "API连接失败"),
    ("server", status_error(InternalServerError, 500), "API返回HTTP 500"),
    # 1.3-C独立案例已完成：500由原1.2的APIStatusError兜底处理。
]


def load_lesson() -> ModuleType:
    """按明确路径导入原1.2入口；导入不会执行其main()。"""
    path = Path(__file__).resolve().parent.parent / "01_02_langchain_model" / "main.py"
    spec = importlib.util.spec_from_file_location("lesson_1_2_boundary", path)
    assert spec is not None and spec.loader is not None
    lesson = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson)
    return lesson


def check_case(
    lesson: ModuleType,
    name: str,
    error: Exception | None,
    expected: str,
    attempts: int,
    *,
    text: str = "题型全部为客观题。",
    missing_key: bool = False,
    initialization: bool = False,
) -> None:
    """核对原入口的可观察行为；输入/配置/初始化失败不允许invoke。"""
    environment = {
        "DEEPSEEK_API_KEY": "" if missing_key else KEY_MARKER,
        "DEEPSEEK_MODEL": "deepseek-flash",
        "DEEPSEEK_API_BASE": "https://api.deepseek.com",
        "LANGSMITH_TRACING": "false",
        "LANGCHAIN_TRACING_V2": "false",
    }
    output = io.StringIO()
    # patch临时替换对象属性，离开with后恢复；多个with项目一起生效。
    # side_effect=异常对象：被替换的方法一旦被调用，就抛出该异常。
    # 本测试替换ChatDeepSeek构造器，因此没有真实模型/HTTP客户端。
    with (
        patch.dict(os.environ, environment, clear=True),
        patch.object(sys, "argv", ["main.py"]),
        patch.object(Path, "read_text", return_value=text),
        patch.object(lesson, "load_dotenv", return_value=False) as dotenv,
        patch.object(lesson, "ChatDeepSeek") as constructor,
        patch.object(lesson, "show_response") as show_response,
        redirect_stdout(output),
    ):
        model = constructor.return_value
        model.invoke.side_effect = error or AssertionError("不应执行invoke")
        if initialization:
            constructor.side_effect = error
        code = lesson.main()
        if not text.strip():
            dotenv.assert_not_called()
        if not attempts and not initialization:
            constructor.assert_not_called()
        assert model.invoke.call_count == attempts, f"{name}：invoke次数不符"
        show_response.assert_not_called()
        if constructor.called:
            assert constructor.call_args.kwargs["max_retries"] == 0
    printed = output.getvalue()
    assert code == (1 if attempts else 2), f"{name}：失败退出码不符"
    assert expected in printed, f"{name}：错误分类不符"
    assert f"模型请求尝试数：{attempts}；自动重试：关闭" in printed
    assert RAW_MARKER not in printed and KEY_MARKER not in printed
    assert "真实模型正文" not in printed
    print(f"{name}：通过；{expected}；退出{code}；离线invoke {attempts}次。")


def main() -> int:
    """基础通过、TODO未完成返回1；所有检查通过才返回0。"""
    lesson = load_lesson()
    # 外层网络哨兵兜底：任何意外联网都会让检查失败。
    with (
        patch("socket.socket.connect", side_effect=AssertionError("离线检查禁止联网")),
        patch("socket.create_connection", side_effect=AssertionError("离线检查禁止联网")),
        patch("socket.getaddrinfo", side_effect=AssertionError("离线检查禁止DNS")),
    ):
        for name, error, expected in CASES:
            check_case(lesson, name, error, expected, 1)
        check_case(lesson, "empty", None, "材料须为", 0, text="  ")
        check_case(lesson, "missing-key", None, "DEEPSEEK_API_KEY 缺失", 0, missing_key=True)
        check_case(
            lesson, "initialization", ValueError(RAW_MARKER),
            "模型初始化失败", 0, initialization=True,
        )
    print(
        f"{len(CASES)}项请求异常及3项前置失败检查通过；"
        "真实请求0，未读.env，未生成模型回答。"
    )
    server = [error for name, error, _ in CASES if name == "server"]
    if not server:
        print("独立练习待完成：增加server/500案例；本脚本退出1不表示基础检查失败。")
        return 1
    assert len(server) == 1 and isinstance(server[0], InternalServerError)
    assert server[0].status_code == 500
    print("server/500边界探针通过；整体检查退出0。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
