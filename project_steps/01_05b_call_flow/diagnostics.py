"""教学用离线诊断；替换配置与模型边界，辅助语法不属于用户TODO。"""

import io
from collections.abc import Callable
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

from openai import APITimeoutError


Runner = Callable[..., int]
PROBE_GOAL = "离线路由检查专用目标"


def check_goal_route(lesson: ModuleType, runner: Runner, goal: str, path: Path) -> bool:
    """临时替换main，检查目标/路径是否到达；不创建客户端或执行原main。"""
    # 用不同于默认值的目标检查，避免无参数看似正常掩盖漏传。
    for target in (goal, PROBE_GOAL):
        with patch.object(lesson, "main", return_value=0) as entry:
            runner(lesson, target, path)
        if entry.call_count != 1:
            return False
        arguments = entry.call_args.kwargs
        if (
            arguments.get("learning_goal") != target
            or arguments.get("material_path") != path
        ):
            return False
    return True


def diagnose(lesson: ModuleType, runner: Runner, goal: str, path: Path) -> int:
    """执行原调用链但在invoke抛SDK超时；0表示预期诊断通过，不是API成功。"""
    settings = {
        "DEEPSEEK_API_KEY": "OFFLINE_PLACEHOLDER_NOT_A_KEY",
        "DEEPSEEK_MODEL": "deepseek-flash",
        "DEEPSEEK_API_BASE": "https://api.deepseek.com",
    }
    output = io.StringIO()
    print("\n[离线诊断] 配置为人工占位；invoke将抛超时；无真实模型回答。")
    with (
        patch("socket.socket.connect", side_effect=AssertionError("离线禁止联网")),
        patch("socket.create_connection", side_effect=AssertionError("离线禁止联网")),
        patch("socket.getaddrinfo", side_effect=AssertionError("离线禁止DNS")),
        patch.object(lesson, "load_dotenv", side_effect=AssertionError("离线禁止读.env")),
        patch.object(lesson, "load_settings", return_value=settings) as config,
        patch.object(lesson, "ChatDeepSeek") as constructor,
        patch.object(lesson, "build_messages", wraps=lesson.build_messages) as builder,
        patch.object(lesson, "show_response") as display,
        redirect_stdout(output),
    ):
        model = constructor.return_value
        model.invoke.side_effect = APITimeoutError(request=Mock())
        code = runner(lesson, goal, path)
    printed = output.getvalue()
    assert code == 1 and model.invoke.call_count == 1, "预期在invoke处超时"
    assert config.call_count == 1 and builder.call_count == 1
    display.assert_not_called()
    assert "服务端是否执行未知" in printed
    assert "模型请求尝试数：1" in printed
    assert constructor.call_args.kwargs["max_retries"] == 0
    messages = model.invoke.call_args.args[0]
    assert messages[0].content == lesson.SYSTEM_MESSAGE
    # 只摘安全的目标第一行；不打印配置、请求对象、完整日志或材料。
    actual = messages[1].content.split("\n", 1)[0]
    expected = f"学习目标：{goal.strip()}"
    print("输入：公开材料读取通过；配置：使用占位值；消息：system / human。")
    print(f"期望进入invoke的{expected}")
    print(f"实际进入invoke的{actual}")
    print("请求：离线invoke替身1次，真实HTTP请求0；响应：抛超时，未取得AIMessage。")
    print("展示：show_response未执行；执行/收费未知是超时语义，不是本地注入账单。")
    routed = check_goal_route(lesson, runner, goal, path)
    if actual != expected or not routed:
        print("目标贯通检查未通过：定位run_call到原main的参数传递，诊断退出1。")
        return 1
    print("目标贯通及预期超时边界通过；诊断退出0，不代表真实API成功。")
    return 0
