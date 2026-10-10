"""任务 0.3：核对解释器、依赖声明、锁文件和实际安装版本。

运行：
    .\\.venv-py312\\Scripts\\python.exe -X utf8 project_steps\\00_03_reproducible_env\\main.py

本课只读取公开环境元数据，不读取 .env、不创建模型、不发请求。
先核对 Python 版本，再核对依赖；用错解释器时给出明确提示。
"""

import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


# 这里是“本次报告哪些包”，并不是安装依赖的声明。
# 真正的直接依赖在 pyproject.toml；完整解析结果在 uv.lock。
AUDIT_PACKAGES = (
    "langchain-core",
    "langchain-deepseek",
    "python-dotenv",
)
# TODO 0.3（你独立完成）：加入 langchain-openai，让报告也显示其版本。
# 不要把它添加到 pyproject.toml 的直接依赖中，也不安装/升级任何包。
# 然后用 uv tree 找出是哪个直接依赖带入它，解释两者的区别。


def read_toml(path: Path) -> dict:
    """读取 TOML：它是配置文本格式，解析不会执行里面的命令。"""
    # tomllib 从 Python 3.11 起属于标准库，本课使用 3.12。
    # 放在函数内导入：main 先拒绝旧解释器，再调用本函数。
    # 这样用 3.10 运行时得到教学错误提示，而不是导入失败的 Traceback。
    import tomllib

    # rb 表示二进制读取；tomllib.load 要求文件返回字节。
    # 和前两课 json.load 使用文本文件的接口要求不同。
    with path.open("rb") as source:
        return tomllib.load(source)


def inspect_dependencies(project_root: Path) -> None:
    """打印审核列表中包的版本，并核对声明、锁记录与实际环境。"""
    manifest = read_toml(project_root / "pyproject.toml")
    lock = read_toml(project_root / "uv.lock")

    # get 的默认 {} 和 [] 便于明确检查字段缺失，而不直接发生 KeyError。
    project = manifest.get("project", {})
    if not isinstance(project, dict):
        raise ValueError("pyproject.toml 的 project 必须是配置表。")
    direct_items = project.get("dependencies", [])
    if not isinstance(direct_items, list) or not direct_items:
        raise ValueError("pyproject.toml 缺少直接依赖声明。")
    locked_items = lock.get("package", [])
    if not isinstance(locked_items, list) or not locked_items:
        raise ValueError("uv.lock 缺少包记录，请先生成锁文件。")

    direct_versions = {}
    for item in direct_items:
        if not isinstance(item, str):
            raise ValueError("直接依赖声明必须是字符串。")
        # 本课三个直接依赖全部采用 name==version；不实现通用版本解析器。
        # partition 返回三项：左侧、分隔符、右侧，赋给三个变量叫元组解包。
        name, separator, expected = item.partition("==")
        if not separator or not name or not expected:
            raise ValueError("本课直接依赖需要使用 name==version 的精确版本声明。")
        direct_versions[name] = expected

    print(f"声明的直接依赖数：{len(direct_versions)}")
    print(f"锁文件包记录数：{len(locked_items)}（包含项目记录）")

    for name in AUDIT_PACKAGES:
        # version 根据发行包名称查询当前解释器安装的版本。
        # 不导入 LangChain，不创建模型，也不读取 API Key。
        actual = version(name)
        source = "直接依赖" if name in direct_versions else "间接依赖"
        if name in direct_versions and actual != direct_versions[name]:
            raise ValueError(f"{name} 的安装版本与直接依赖声明不一致。")

        # 锁文件可能为不同平台保存多个候选版本，逐项寻找本环境版本。
        # 找到就 break 退出这层循环；不要把它误认为退出整个程序。
        matched = False
        for item in locked_items:
            if not isinstance(item, dict):
                raise ValueError("锁文件中的包记录必须是配置表。")
            if item.get("name") == name and item.get("version") == actual:
                matched = True
                break
        if not matched:
            raise ValueError(f"{name} 的安装版本未找到对应锁记录。")
        print(f"{name}：{actual}，{source}，与锁记录一致。")


def main() -> int:
    """0：本课核对通过；2：解释器/环境/配置不符合本课要求。"""
    # version_info 是带版本字段的对象；[:2] 取主版本和次版本。
    print(f"实际解释器：{sys.executable}")
    print(f"Python 版本：{sys.version.split()[0]}")
    if sys.version_info[:2] != (3, 12):
        print("环境错误：本课需要 Python 3.12，请使用 .venv-py312 的解释器。")
        return 2
    if sys.prefix == sys.base_prefix:
        print("环境错误：当前没有进入虚拟环境，请按讲义使用项目环境。")
        return 2

    project_root = Path(__file__).resolve().parents[2]
    # 参数可用于隔离诊断副本，不要求改动真正的 pyproject.toml/uv.lock。
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1]).resolve()

    try:
        pinned = (project_root / ".python-version").read_text(encoding="utf-8").strip()
        current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if current != pinned:
            raise ValueError("当前 Python 补丁版本与 .python-version 不一致。")
        inspect_dependencies(project_root)
    except PackageNotFoundError:
        # 包缺失通常是未同步或解释器选错，不需要修改材料和模型提示词。
        print("依赖错误：核对列表中的包尚未安装，请先执行锁文件同步。")
        return 2
    except FileNotFoundError:
        print("文件错误：缺少 .python-version、pyproject.toml 或 uv.lock。")
        return 2
    except ValueError as error:
        # TOMLDecodeError 也是 ValueError；不回显可能包含任意数据的解析细节。
        import tomllib

        if isinstance(error, tomllib.TOMLDecodeError):
            print("配置错误：TOML 格式不正确；尚未完成依赖核对。")
        else:
            print(f"环境核对失败：{error}")
        return 2
    except OSError:
        print("文件错误：请检查配置读取权限或目录。")
        return 2

    print("本课核对通过；完整依赖关系另用 uv pip check 验证。")
    print("本次模型请求数：0；用户独立练习是否完成需另看新增包报告。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
