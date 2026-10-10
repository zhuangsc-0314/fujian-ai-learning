r"""观察命令行参数如何进入Python；只打印演示参数，不读取材料/Key。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\args_demo.py timeout
用公开案例名、演示文件名和数字练习；API Key继续通过.env配置。
"""

import sys


def main() -> int:
    """显示脚本名、用户参数、数量和类型；不调用模型。"""
    # argv是列表。第0项是脚本名/路径，后面的项才是脚本收到的参数。
    # 列表整体打印会保留字符串的引号，便于观察数字参数也是字符串。
    print("sys.argv：", sys.argv)
    print("len(sys.argv)：", len(sys.argv))
    for value in sys.argv:
        # repr返回便于观察的表示形式，例如'3'，不解释或执行其中的文字。
        # type(value)取得类型对象，.__name__读取它的名字，例如str。
        print("值：", repr(value), "类型：", type(value).__name__)
    print("本演示真实模型请求数：0。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
