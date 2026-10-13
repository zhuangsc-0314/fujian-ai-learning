"""阶段2未来课程的说明入口；不执行尚未实现的业务函数。"""

import argparse


def preview_lesson(lesson_id: str, title: str, exercise: str) -> int:
    """说明预览成功为0；请求尚未实现的练习为2，不当作验收通过。"""
    parser = argparse.ArgumentParser(description=f"{lesson_id} {title}（TODO骨架）")
    parser.add_argument("--exercise", action="store_true", help="查看未实施练习状态")
    args = parser.parse_args()
    print(f"{lesson_id}：{title}")
    print("状态：课程规划/TODO骨架；业务功能尚未实现，尚未验收。")
    print(f"独立练习位置：{exercise}")
    print("本入口仅显示说明；不读取.env、不连接数据库、不发模型请求。")
    if args.exercise:
        print("练习与检查尚未实施；退出2。完成课程实现后再添加实际验证入口。")
        return 2
    print("说明预览退出0；此退出码不代表功能或学习验收通过。")
    return 0
