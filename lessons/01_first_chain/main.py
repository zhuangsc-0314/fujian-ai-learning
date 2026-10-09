"""第一课：从 .env 加载配置，运行真实 DeepSeek 模型。
运行：.\\.venv\\Scripts\\python.exe lessons\\01_first_chain\\main.py
每次运行发起一次真实请求，关闭自动重试。
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)


def build_prompt() -> ChatPromptTemplate:
    """创建模板；在 invoke() 时填入变量。"""
    return ChatPromptTemplate.from_messages(
        [
            ("system", "你是一位耐心的编程老师，请用{language}简洁回答。"),
            ("human", "请用一句话解释{topic}，再举一个生活中的例子。"),
        ]
    )


def build_model() -> ChatDeepSeek:
    """读取项目根目录 .env，创建真实模型客户端。"""
    # __file__ 是当前文件，parents[2] 指向项目根目录。
    project_root = Path(__file__).resolve().parents[2]
    # 本课程以 .env 为准，覆盖同名环境变量；支持 Windows 的 UTF-8 BOM。
    load_dotenv(project_root / ".env", override=True, encoding="utf-8-sig")

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    model_name = os.getenv("DEEPSEEK_MODEL", "").strip()
    base_url = os.getenv("DEEPSEEK_API_BASE", "").strip()
    required = {
        "DEEPSEEK_API_KEY": api_key,
        "DEEPSEEK_MODEL": model_name,
        "DEEPSEEK_API_BASE": base_url,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError("请先在项目根目录 .env 中填写：" + ", ".join(missing))

    # 创建客户端并不会产生模型回答；实际请求发生在 chain.invoke()。
    return ChatDeepSeek(
        model=model_name,
        api_key=api_key,
        api_base=base_url,
        timeout=60,
        max_retries=0,
        max_tokens=512,
        extra_body={"thinking": {"type": "disabled"}},
    )


def main() -> None:
    # 字典的键名与模板中的变量名对应。
    inputs = {"language": "简体中文", "topic": "LangChain"}
    prompt = build_prompt()
    model = build_model()
    parser = StrOutputParser()

    # 本地填充模板，观察消息；这里不会调用 API。
    prompt_value = prompt.invoke(inputs)
    print("[1] 填充后的提示词")
    for message in prompt_value.to_messages():
        print(f"{message.type}: {message.content}")

    # | 组合三个步骤；创建 chain 时仍然不发送请求。
    chain = prompt | model | parser

    # 推荐在下一行设置断点：执行 invoke 时发起一次真实请求。
    print("\n[2] 正在请求 DeepSeek……")
    result = str(chain.invoke(inputs))
    print("\n[3] 解析后的真实模型回答")
    print(f"结果类型：{type(result).__name__}")
    print(result)


if __name__ == "__main__":
    # Windows 终端与输出重定向统一使用 UTF-8。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except ValueError as error:
        print(f"配置或参数错误：{error}")
        raise SystemExit(2)
    except AuthenticationError:
        print("认证失败：请检查 .env 中的 DeepSeek API Key。")
        raise SystemExit(1)
    except RateLimitError:
        print("请求受限：请检查 API 余额、额度或请求频率。")
        raise SystemExit(1)
    except APITimeoutError:
        print("请求超时：请检查网络连接，稍后再试。")
        raise SystemExit(1)
    except APIConnectionError:
        print("连接失败：请检查 DeepSeek API 地址、网络和代理设置。")
        raise SystemExit(1)
    except APIStatusError as error:
        print(f"API 返回 HTTP {error.status_code}：请检查模型名、额度和接口地址。")
        raise SystemExit(1)
