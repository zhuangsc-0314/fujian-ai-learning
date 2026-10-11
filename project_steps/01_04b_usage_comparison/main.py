r"""1.4-B：固定目标和配置，比较同一公开材料的长短版本。

默认只预览、不读.env；--live最多两次真实尝试，可能计费，失败停止。
原1.2负责输入/配置/模型/异常；这里仅组织对照与展示记录。
"""

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


LESSON_DIR = Path(__file__).resolve().parent
MATERIALS = (
    ("short", LESSON_DIR / "material_short.txt"),
    ("long", LESSON_DIR.parent / "01_01_first_sdk_call" / "material.txt"),
)


def load_lesson() -> ModuleType:
    """按路径复用1.2；导入不执行其main，不创建第二套模型服务。"""
    path = LESSON_DIR.parent / "01_02_langchain_model" / "main.py"
    spec = importlib.util.spec_from_file_location("lesson_1_2_comparison", path)
    assert spec is not None and spec.loader is not None
    lesson = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson)
    return lesson


def input_token_difference(
    short_record: dict[str, object], long_record: dict[str, object],
) -> int | None:
    """返回长材料减短材料的输入token差；任一缺失时返回None。"""
    # TODO 1.4-B（你独立完成）：读取两条input_tokens，
    # 任一为None就返回None，否则返回长减短。明确的0也允许参与运算。
    # 不硬编码真实结果，不用字符差替代token差，不修改检查脚本。
    return None


def run_comparison(lesson: ModuleType) -> tuple[int, list[dict[str, object]]]:
    """最多调用原入口两次；第一次失败不继续，不自动重跑。"""
    records: list[dict[str, object]] = []
    for label, path in MATERIALS:
        print(f"\n[对照材料] {label}")
        code = lesson.main(material_path=path, records=records)
        if code != 0:
            print("本次比较停止；失败没有成功用量记录，不能据此认定未执行或免费。")
            return code, records
        records[-1]["case"] = label
    return 0, records


def main() -> int:
    """默认预览/真实成功返回0；非法参数返回2；失败沿用原入口退出码。"""
    if sys.argv[1:] not in ([], ["--live"]):
        print("只支持无参数预览或--live真实比较；本次请求0。")
        return 2
    lesson = load_lesson()
    print("固定目标：", lesson.LEARNING_GOAL)
    print("固定配置：同一进程的模型/系统约束；输出上限256；自动重试关闭。")
    if not sys.argv[1:]:
        print("预览模式：不读取.env、不创建模型、不发送请求。")
        for label, path in MATERIALS:
            print(f"{label}材料路径：{path}")
        print("真实比较请显式加--live；最多两次尝试，可能计费。")
        return 0

    code, records = run_comparison(lesson)
    print("\n[真实成功调用记录] 缺失字段null表示未知；不包含正文/完整响应头/Key。")
    # ensure_ascii=False保留中文；indent=2缩进。只序列化允许字段记录。
    print(json.dumps(records, ensure_ascii=False, indent=2))
    if code == 0:
        difference = input_token_difference(records[0], records[1])
        shown = "未知（或独立练习尚未完成）" if difference is None else str(difference)
        print(f"输入token差值（长减短）：{shown}")
        print("输出/耗时是否变化请观察实际记录；两次请求不足以证明稳定规律。")
    print("费用未核算，实际计费须另核对供应商价目与账单。")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
