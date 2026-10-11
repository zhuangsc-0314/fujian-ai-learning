r"""1.5-B：复用目标参数与原调用入口；默认离线，--live才可能请求。

先运行--diagnose定位目标漏传；只修改run_call的TODO，不修改诊断/检查。
"""

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType

from diagnostics import check_goal_route, diagnose


MATERIAL_PATH = Path(__file__).resolve().parent.parent / "01_01_first_sdk_call" / "material.txt"


def load_preview() -> ModuleType:
    """复用1.5-A已完成的参数与预览；导入不执行main。"""
    path = Path(__file__).resolve().parent.parent / "01_05a_goal_argument" / "main.py"
    spec = importlib.util.spec_from_file_location("goal_preview_for_flow", path)
    if spec is None or spec.loader is None:
        raise ImportError("无法加载目标参数课程。")
    preview = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preview)
    return preview


def run_call(
    lesson: ModuleType, goal: str, path: Path,
    *, records: list[dict[str, object]] | None = None,
) -> int:
    """将目标/材料交给既有1.2入口；本函数不重复配置或异常处理。"""
    # TODO 1.5-B：诊断为何预览目标与invoke收到的目标不一致。
    # 只修改下面的调用，把goal传给原入口新增的learning_goal关键字参数。
    # 保留material_path与records；不改默认常量/System或诊断脚本。
    return lesson.main(material_path=path, records=records)


def main(argv: list[str] | None = None) -> int:
    """默认预览；诊断通过0/待修复1；输入错误2；真实调用沿用原码。"""
    preview = load_preview()
    lesson = preview.load_lesson()
    parser = argparse.ArgumentParser(
        description="目标参数贯通与故障定位；默认离线。", allow_abbrev=False,
    )
    parser.set_defaults(goal=lesson.LEARNING_GOAL)
    preview.add_goal_argument(parser)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--diagnose", action="store_true", help="离线注入超时并观察目标")
    modes.add_argument("--live", action="store_true", help="路由通过后尝试一次真实请求")
    args = parser.parse_args(argv)
    # 复用A的输入检查与预览；不读配置、不创建模型，非法目标在这里停止。
    code = preview.main([f"--goal={args.goal}"], lesson=lesson)
    if code != 0:
        return code
    if args.diagnose:
        return diagnose(lesson, run_call, args.goal, MATERIAL_PATH)
    if not args.live:
        print("下一步用--diagnose观察贯通情况；预览正确还需检查invoke实际输入。")
        return 0
    # 教学骨架的防误调用检查只替换main核对参数，不读.env、不创建模型。
    if not check_goal_route(lesson, run_call, args.goal, MATERIAL_PATH):
        print("目标路由未通过：尚未读取.env或发送请求；先完成TODO并运行离线诊断。")
        return 2
    print("进入真实调用模式：读取本机配置；最多一次尝试，自动重试关闭，可能计费。")
    records: list[dict[str, object]] = []
    code = run_call(lesson, args.goal, MATERIAL_PATH, records=records)
    print(f"真实成功用量记录数：{len(records)}；未核对实际账单。")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
