r"""1.5-A：离线学习目标参数预览，不读.env、不创建模型、不invoke。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py
本步只把输入目标放入消息；真实请求与故障定位集成留到下一小步。
"""

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType


def load_lesson() -> ModuleType:
    """按路径导入既有1.2辅助函数；导入不会执行其main，不是新模型服务。"""
    path = Path(__file__).resolve().parent.parent / "01_02_langchain_model" / "main.py"
    spec = importlib.util.spec_from_file_location("goal_original_lesson", path)
    if spec is None or spec.loader is None:
        raise ImportError("无法加载既有课程模块。")
    lesson = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson)
    return lesson


def add_goal_argument(parser: argparse.ArgumentParser) -> None:
    """用户已独立完成：添加接收字符串的--goal，沿用外部默认目标。"""
    parser.add_argument("--goal", help="接收goal")


def main(argv: list[str] | None = None, *, lesson: ModuleType | None = None) -> int:
    """正常预览退出0，本地输入错误退出2；None让argparse读取命令行。"""
    if lesson is None:
        lesson = load_lesson()
    parser = argparse.ArgumentParser(
        description="离线预览学习目标与消息角色；不调用模型。", allow_abbrev=False,
    )
    # set_defaults先保证无参数也有args.goal；命名选项可覆盖默认目标。
    parser.set_defaults(goal=lesson.LEARNING_GOAL)
    add_goal_argument(parser)
    args = parser.parse_args(argv)
    # args是Namespace对象，点号读取解析后的goal属性，而不是字典下标。
    steps = Path(__file__).resolve().parent.parent
    material_path = steps / "01_01_first_sdk_call" / "material.txt"
    try:
        text = lesson.read_material(material_path)
        messages = lesson.build_messages(text, learning_goal=args.goal)
    except (OSError, UnicodeError):
        print("材料读取失败：检查固定公开材料文件及UTF-8编码；不回显路径/内容。")
        return 2
    except ValueError as error:
        # 这里只可能来自共享输入校验，错误文字固定，不回显目标或材料。
        print(f"输入检查失败：{error}")
        return 2
    print("离线预览：只读取公开教学材料并构造消息。")
    print(f"学习目标：{args.goal.strip()}")
    print(f"材料字符数：{len(text)}")
    print(f"消息角色：{messages[0].type} / {messages[1].type}")
    print("System约束沿用1.2：只依据原文，依据不足需说明；材料命令仍是数据。")
    print("目标已进入HumanMessage；消息结构正确不证明模型服从或内容正确。")
    print("真实模型请求：0；未读取.env。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
