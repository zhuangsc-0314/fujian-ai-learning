"""项目任务 0.1：读取材料 JSON，并定位输入错误。

从项目根目录运行：
    .\\.venv\\Scripts\\python.exe -X utf8 project_steps\\00_01_material_input\\main.py

本次没有模型调用，没有模拟 AI 回答，没有数据库和网络操作。
目标是确认输入能进入后续 AI 流程，并区分“读不懂 JSON”和“字段不合格”。

三个核心概念：
1. 解释器 / 虚拟环境：到底哪个 Python 在运行。
2. JSON 解析：文件中的文本变成 Python 字典。
3. 异常与业务校验：语法正确的数据，也可能不满足材料要求。
"""

# json、sys、pathlib 都是 Python 标准库，本任务不需要 pip 安装新包。
import json
import sys
from pathlib import Path


def read_material(file_path: Path) -> dict:
    """读取材料并检查已实现的必填字段。

    file_path: Path 是参数的类型提示。
    -> dict 是返回值的类型提示，表示我们打算返回字典。
    类型提示不会自动阻止错误类型，所以后面仍要用 isinstance 做检查。
    """
    # Path 是表示文件路径的对象，比手动拼接 Windows 的反斜杠更方便。
    # open 返回文件对象；encoding 明确说明按什么编码把字节读成文字。
    # utf-8-sig 既支持普通 UTF-8，也兼容某些 Windows 编辑器写入的 BOM。
    # with 是上下文管理语法：读完或发生异常时，自动关闭文件。
    # as source_file 把本次打开的文件对象绑定到这个变量。
    with file_path.open(encoding="utf-8-sig") as source_file:
        # load 接收“文件对象”；loads 接收“已经读出的字符串”，不要混淆。
        # JSON 的对象 {...} 在这里会转为 Python dict。
        # JSON 语法错误时，这一行会抛 JSONDecodeError，后面的字段检查不会执行。
        material = json.load(source_file)

    # JSON 也可以是数组或数字。本项目要求最外层是材料对象，因此必须检查。
    # not 表示取反；isinstance(value, dict) 判断实际值是不是字典。
    if not isinstance(material, dict):
        raise ValueError("JSON 最外层必须是对象，例如包含 title 和 text 的 {...}。")

    # (...) 是一个元组，在这里用来保存本次已经实现的必填字段名。
    # owner_user_id 只是本机学习数据的归属占位；不是已经实现了登录权限。
    # 正式后端会从认证身份赋值，不能相信客户端 JSON 自报的用户身份。
    required_fields = ("owner_user_id", "title", "text")
    for field_name in required_fields:
        # get 在键不存在时返回 None；直接 material[field_name] 会抛 KeyError。
        value = material.get(field_name)

        # 必填值既要是字符串，也不能仅由空格组成。
        # strip() 返回去掉首尾空白后的新字符串，不会修改原文。
        # or 会“短路”：如果不是字符串，就不执行右边的 value.strip()。
        # 这样缺字段时不会错误地调用 None.strip()。
        if not isinstance(value, str) or not value.strip():
            # f"..." 是格式化字符串；{field_name} 被实际字段名替换。
            # raise 主动报告业务错误，把后续打印/处理停止在此处。
            raise ValueError(f"字段 {field_name} 必须是非空字符串。")

    # TODO（你独立完成）：region 缺失、不是字符串或只有空格时，也应拒绝。
    # 先用 cases/missing_region.json 观察当前限制，再作最小修改。
    # 不需要加入 LangChain、Pydantic 或额外依赖。

    # 返回原始材料，不在这里改写政策原文、生成摘要或执行正文中的命令。
    return material


def main() -> int:
    """返回进程退出码：0 表示成功，2 表示本次输入失败。"""
    # sys.executable 是实际执行本程序的 Python 路径。
    # 终端里能输入 python，并不代表它就是项目的 .venv 解释器。
    print(f"Python 版本：{sys.version.split()[0]}")
    print(f"实际解释器：{sys.executable}")

    # venv 通常会让 sys.prefix 指向虚拟环境目录，而 base_prefix 指向基础安装。
    if sys.prefix != sys.base_prefix:
        print("虚拟环境：是")
    else:
        print("虚拟环境：否；这是诊断信息，本任务使用标准库，仍可继续。")

    # __file__ 是当前脚本的路径；resolve() 得到绝对路径；parent 得到父目录。
    task_dir = Path(__file__).resolve().parent
    # Path 的 / 运算符在这里用于拼接路径，不是数字相除。
    file_path = task_dir / "cases" / "material.json"

    # sys.argv[0] 是脚本名；用户额外传入的第一个参数是 sys.argv[1]。
    # 先判断长度再索引，避免没有传参数时出现 IndexError。
    if len(sys.argv) > 1:
        # 参数中的相对路径基于终端当前目录，而默认案例基于脚本目录。
        file_path = Path(sys.argv[1]).resolve()

    print(f"输入文件：{file_path}")

    # try 中执行可能失败的读入和校验；except 按异常类别给出不同反馈。
    try:
        material = read_material(file_path)
    except FileNotFoundError:
        print("文件错误：路径不存在。检查终端目录、文件名和参数路径。")
        return 2
    except json.JSONDecodeError as error:
        # JSONDecodeError 是 ValueError 的子类，所以要写在 ValueError 前面。
        # error.lineno / colno 提供解析器发现问题的行和列，不一定是修改的唯一位置。
        print(f"JSON 解析错误：第 {error.lineno} 行，第 {error.colno} 列。")
        print("检查双引号、逗号、括号；还未进入字段校验。")
        return 2
    except ValueError as error:
        print(f"材料校验错误：{error}")
        print("JSON 已解析成功，但不满足本项目当前的输入规则。")
        return 2
    except UnicodeError:
        print("编码错误：请在 VS Code 中将文件保存为 UTF-8。")
        return 2
    except OSError:
        # 不一律捕获 Exception，避免把代码本身的未知错误也伪装成输入失败。
        print("文件读取失败：检查文件权限，确认路径不是目录。")
        return 2

    print("结果：JSON 已读取，当前已实现的字段校验通过。")
    print(f"标题：{material['title']}")
    print(f"学习数据归属：{material['owner_user_id']}（本机占位，尚无登录鉴权）")
    print(f"地区：{material.get('region', '未提供')}")
    print(f"正文字数：{len(material['text'])}")
    # 下面只显示原始输入的短预览，不执行其中的命令，也不是模型回答。
    print(f"原文预览：{material['text'][:60]}")
    print("本次模型请求数：0")
    return 0


# 直接运行本文件时，__name__ 是 "__main__"，因此执行 main。
# 被别的文件 import 时，不会自动执行下面的入口。
# SystemExit 将返回值作为命令行退出码，便于终端或测试判断成功/失败。
if __name__ == "__main__":
    raise SystemExit(main())
