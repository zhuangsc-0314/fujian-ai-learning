"""2.3-B1：引用位置与切片；人工中文练习材料，无.env/模型/数据库。

完整locate_quote已在learning_app/domain.py实现。本次先练输入输出和切片，
while/find/:=内部查找过程留到下一小步；用户只修改locate_my_quote。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from learning_app.domain import locate_quote  # noqa: E402


MY_MATERIAL = "正文：范围是常识。范围是常识。"
MY_QUOTE = "范围是常识。"


def locate_my_quote() -> list[tuple[int, int]]:
    """用户独立练习：调用现有函数，取得引句的全部位置。"""
    # TODO USER：把MY_MATERIAL和MY_QUOTE传给locate_quote，返回它的结果。
    # 不硬编码位置列表，不改两个练习字符串或共享定位函数。
    raise NotImplementedError("请独立完成重复引句的定位调用。")


def main() -> int:
    """观察正常/非法案例，再检查用户重复引句边界；未完成或结果不符退出1。"""
    print("人工材料的离线练习；模型请求0，不读取.env。")
    normal_material = "正文：政治和法律。"
    normal_positions = locate_quote(normal_material, "政治和法律。")
    print("正常：", normal_positions)
    print("正常切片还原：", normal_material[3:9])
    if normal_positions != [(3, 9)]:
        print("正常定位不符合预期，先检查共享规则。")
        return 1

    try:
        locate_quote(normal_material, " ")
        print("非法空引句没有被拒绝，先检查输入校验。")
        return 1
    except ValueError:
        print("非法：空白引句已明确拒绝。")

    try:
        positions = locate_my_quote()
    except NotImplementedError:
        print("独立重复引句案例尚未完成；参考运行不代表用户掌握。")
        return 1

    print("我的重复引句位置：", positions)
    if positions != [(3, 9), (9, 15)]:
        print("位置结果不符合预期；核对输入和返回值，不改原文凑结果。")
        return 1
    # 每次从一个(start,end)元组中分别取出起点与终点，再切原文。
    for start, end in positions:
        print("对应切片：", MY_MATERIAL[start:end])
    print("定位及切片符合预期；独立解释和个人日志仍需验收。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
