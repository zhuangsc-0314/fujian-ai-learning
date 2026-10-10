"""任务 0.2：安全读取 DeepSeek 配置，不调用模型。

运行：
    .\\.venv\\Scripts\\python.exe -X utf8 project_steps\\00_02_safe_config\\main.py

三个核心概念：环境变量与 .env、启动配置校验、脱敏诊断。
你独立完成的练习是检查 DEEPSEEK_MODEL，TODO 在 load_config 中。
"""

import os
import sys
from pathlib import Path

# dotenv 是已经安装的 python-dotenv 包的导入名，两者名字不同。
# 本次复用现有 1.2.4，不引入 LangChain 或 Pydantic。
from dotenv import load_dotenv


def load_config(env_path: Path) -> dict[str, str]:
    """从指定文件补充进程环境变量，再返回后续模型模块需要的配置。

    dict[str, str]：字典的键和值都打算使用字符串，这是类型提示。
    类型提示不负责校验，下面的 if 才检查本次已实现的业务规则。
    返回字典包含真实密钥，只能在进程内使用；禁止打印整个字典。
    """
    # 环境变量属于当前进程。父终端/部署平台可以在启动前注入它们。
    # .env 是本地文本文件，Python 不会自动把它当成环境变量。
    # load_dotenv 把文件内的配置补充到 os.environ，本次不修改文件。
    # 显式传 env_path，避免从不确定的上级目录搜索到另一份 .env。
    load_dotenv(
        dotenv_path=env_path,
        # 已存在的进程变量优先；即使值为空，也不会被文件替换。
        # 所以“终端里设置了空 Key”仍会触发下面的缺失检查。
        override=False,
        # 禁用 ${NAME} 展开；本课只读取字面值，不隐藏另一层来源。
        # .env 不是可执行脚本，里面的命令式内容不能作为命令执行。
        interpolate=False,
        # 与 0.1 一样兼容 Windows 编辑器可能写入的 UTF-8 BOM。
        encoding="utf-8-sig",
    )

    # getenv 读取当前进程环境，不是直接读取 .env 文件。
    # 第二个参数 "" 是变量不存在时的返回值，避免得到 None。
    # strip 去掉首尾空白，纯空白配置会变成空字符串。
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    model = os.getenv("DEEPSEEK_MODEL", "").strip()
    api_base = os.getenv("DEEPSEEK_API_BASE", "").strip()

    # 非空字符串为真，空字符串为假；not api_key 表示配置为空。
    # 这只检查“是否填写”，不能证明密钥有效、账户有额度或接口可达。
    if not api_key:
        # 报错只写变量名，不拼接原始值，避免把密钥写进日志。
        raise ValueError("DEEPSEEK_API_KEY 缺失或只有空白，请检查配置来源。")
    if not model:
        raise ValueError("DEEPSEEK_MODEL 缺失或只有空白，请检查配置来源。")
    # TODO 0.2（你独立完成）：让 DEEPSEEK_MODEL 也必须非空。
    # 缺失、空字符串、纯空白都应抛出 ValueError，只说明变量名。
    # 不给它偷偷补一个默认模型，不打印原始值，不改变 Key 的规则。

    # 字典用于把配置交给后续 AI 模块，当前没有创建或调用模型。
    # api_base 的地址校验在实际模型接入时再加入，本课不验证连通性。
    return {"api_key": api_key, "model": model, "api_base": api_base}


def main() -> int:
    """0：本课已实现规则通过；2：配置不合格；不发起网络请求。"""
    # 本文件在 project_steps/00_02_safe_config 内；parents[2] 是项目根。
    # parents[0] 是当前父目录，parents[1] 是 project_steps。
    project_root = Path(__file__).resolve().parents[2]
    env_path = project_root / ".env"

    # 可用第一个命令行参数选择练习配置；不要求修改真实 .env。
    # 相对参数路径基于终端工作目录，默认路径基于脚本所在项目。
    if len(sys.argv) > 1:
        env_path = Path(sys.argv[1]).resolve()

    print("配置优先级：已有进程环境变量优先，指定 .env 文件补充。")
    # 不打印路径和文件内容；这里只判断是否有可读取的普通文件。
    print(f"配置文件：{'存在' if env_path.is_file() else '不存在，可使用进程配置'}")

    try:
        config = load_config(env_path)
    except UnicodeError:
        print("配置读取失败：请把文件保存为 UTF-8；内容不展示。")
        return 2
    except OSError:
        print("配置读取失败：请检查文件路径和读取权限；内容不展示。")
        return 2
    except ValueError as error:
        # 当前业务异常信息只含固定说明和变量名，不含原始配置值。
        print(f"配置校验失败：{error}")
        print("本次模型请求数：0")
        return 2

    print("API Key：已配置，内容不展示。")
    # 仅显示有无状态。即使误把 Key 粘到模型名，也不回显配置值。
    # ... if ... else ... 是条件表达式：根据条件选择两种文字之一。
    print(f"模型名：{'已配置' if config['model'] else '未配置，独立 TODO 尚待补齐'}")
    print(f"API 地址：{'已配置' if config['api_base'] else '未配置，接入阶段再检查'}")
    print("结果：本课已实现的配置规则通过，不代表 API 鉴权成功。")
    print("本次模型请求数：0")
    return 0


# import 本文件时不会执行 main；直接运行才进入诊断入口。
# SystemExit 把 main 返回值传给终端，PowerShell 用 $LASTEXITCODE 查看。
if __name__ == "__main__":
    raise SystemExit(main())
