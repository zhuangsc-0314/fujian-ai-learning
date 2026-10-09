"""第二课：真实 DeepSeek 多轮对话与流式输出。

默认运行两轮演示；--chat 开启交互，--no-stream 改用 invoke()。
历史仅保存在本次进程内存中，每轮发送一次真实 API 请求。
"""

# ==================== 阅读顺序与运行流程 ====================
# 建议第一次阅读时按 main -> build_prompt -> run_turn -> run_demo 的顺序看。
# build_model 的配置逻辑与第一课相同，最后再复习即可。
#
# 文件从上往下加载时，import 导入模块，def 创建函数，但不会执行函数体。
# 到文件末尾的入口判断后，才调用 main()，再由 main 调用其他函数。
#
# 整体流程：
# 1. 读取命令行参数，决定演示/交互、流式/非流式。
# 2. 创建提示词模板和模型客户端，使用 | 组成一条链。
# 3. 创建 history 列表，每次请求携带已完成的历史与当前问题。
# 4. 取得本轮真实回答，成功后追加一条 human 和一条 ai 消息。
#
# 运行示例（在项目根目录的 PowerShell 终端执行）：
# .\.venv\Scripts\python.exe lessons\02_chat_history\main.py
# .\.venv\Scripts\python.exe lessons\02_chat_history\main.py --chat
# .\.venv\Scripts\python.exe lessons\02_chat_history\main.py --no-stream
#
# 这些行以 # 开头，属于注释，Python 不执行它们。
# 文件最开头的三引号文本是模块文档字符串，可通过 __doc__ 访问。
# 缩进则属于 Python 语法：同一级缩进表示同一代码块，通常每级 4 个空格。


# ==================== 一、导入需要的组件 ====================

# Python 标准库：通常随 Python 一起提供，无需单独 pip install。
import argparse  # 将 --chat 等命令行文本解析为程序可读取的参数。
import os        # 本课用 os.getenv() 读取环境变量。
import sys       # 本课配置输出编码，并处理程序输出相关对象。
from pathlib import Path  # 用 Path 对象表示路径，比手工拼接路径字符串方便。

# 第三方库：安装 requirements.txt 后才能 import。
# from 包名 import 名称：只把指定名称引入当前文件，调用时无需再写包名前缀。
from dotenv import load_dotenv  # 读取 .env，并将配置加载到进程环境变量。

# 括号里的多行 import 只是排版方式，与单行导入多个名称语义相同。
from langchain_core.messages import (
    AIMessage,                 # 模型完整回答；包含正文、角色及可能的元数据。
    AIMessageChunk,            # 流式回答的片段；不是另一种独立请求。
    BaseMessage,               # 消息基类；HumanMessage、AIMessage 都属于消息。
    HumanMessage,              # 用户消息；用于在历史中记录本轮问题。
    message_chunk_to_message,  # 把累加后的消息片段转成普通消息。
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Runnable 是 LangChain 可运行组件的通用接口。
# 本文件用它标注 chain 参数，不是说 chain 只能是某一种具体模型。
from langchain_core.runnables import Runnable
from langchain_deepseek import ChatDeepSeek

# ChatDeepSeek 的底层客户端使用 OpenAI 兼容协议，所以请求异常来自 openai 包。
# 导入这些异常类型不会把请求改成发送给 OpenAI；目标地址仍取自 .env。
from openai import APIConnectionError, APIStatusError, APITimeoutError


# ==================== 二、读取配置并创建模型客户端 ====================

# def 定义函数；空括号表示调用这个函数时不需要传入参数。
# -> ChatDeepSeek 是返回值类型注解，帮助读者和编辑器理解函数。
# 注解本身不会让 Python 自动检查返回值类型，也不会自动转换对象。
def build_model() -> ChatDeepSeek:
    """沿用第一课配置；保留在本文件中，方便单独阅读。

    返回：
        一个配置好的 ChatDeepSeek 客户端，不是模型回答。

    副作用：
        把项目 .env 的值加载到本进程环境变量；此处不发送模型请求。

    失败情况：
        必需配置缺失时抛出 ValueError，交给文件末尾的处理代码。
    """
    # __file__ 是当前 Python 文件的路径。
    # Path(...) 创建路径对象；resolve() 将其解析为绝对路径。
    # parents 是祖先目录序列，索引从 0 开始：
    # parents[0] = 02_chat_history；parents[1] = lessons；
    # parents[2] = 项目根目录 New project 2。
    # 因此从不同终端工作目录运行本文件，也能找到同一个 .env。
    project_root = Path(__file__).resolve().parents[2]

    # Path 对象支持 / 运算符拼接路径，这里的 / 不是数值除法。
    # override=True 是关键字参数，意思是 .env 覆盖同名已有环境变量。
    # encoding="utf-8-sig" 可读取普通 UTF-8，也会处理文件开头的 UTF-8 BOM。
    # 读取 Key 不等于打印 Key；本代码不会把配置字典输出到终端。
    load_dotenv(project_root / ".env", override=True, encoding="utf-8-sig")

    # 这是“字典推导式”：对给定的三个变量名逐个计算，得到一个新字典。
    # name 是循环变量，name: 表示字典键，后面的表达式计算对应的值。
    # (...) 中逗号分隔的三个字符串组成 tuple（元组），用来列出配置名称。
    #
    # os.getenv(name, "")：读取环境变量，找不到时返回默认空字符串。
    # .strip()：返回去掉首尾空白的新字符串；字符串本身不会被原地修改。
    #
    # 这段等价于：
    # config = {}
    # for name in ("DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_API_BASE"):
    #     config[name] = os.getenv(name, "").strip()
    config = {
        name: os.getenv(name, "").strip()
        for name in ("DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_API_BASE")
    }

    # 这是“列表推导式”，得到一个只包含缺失配置名称的 list。
    # config.items() 提供 (键, 值) 对；for name, value 会把每一对解包。
    # if not value 是筛选条件：本例中的空字符串会被视为 False。
    # not "" 为 True，因此空值对应的键会被收集到 missing 中。
    missing = [name for name, value in config.items() if not value]

    # 列表的真假判断：空列表为 False，非空列表为 True。
    # if missing 表示“至少有一项配置缺失”。
    if missing:
        # ", ".join(missing) 将名称列表连接为逗号分隔的字符串。
        # + 连接字符串；raise 主动抛出异常，并停止当前正常执行流程。
        # 这里只把缺失项的名称放进错误消息，不把 Key 的值放进去。
        raise ValueError("请先在项目根目录 .env 中填写：" + ", ".join(missing))

    # return 把对象交给函数调用者，并结束本函数。
    # ChatDeepSeek(...) 调用类的构造过程，创建客户端对象。
    # config["名称"] 是字典取值语法；键不存在时会抛出 KeyError。
    # 上面已经按固定名称构造 config，并检查空值。
    #
    # 此时只是准备客户端，没有调用模型。请求在后面的 invoke/stream 中发生。
    # timeout=60：客户端网络请求超时设置，不是保证全程序在 60 秒内完成。
    # max_retries=0：关闭客户端自动重试；一轮不会因自动重试而重复发送。
    # max_tokens=512：限制最大生成 token 数，不等于限制为 512 个汉字。
    # extra_body 是额外请求字段；这里的值是一个嵌套字典。
    # thinking.type=disabled：本课关闭 DeepSeek 思考模式，先学习普通回答。
    return ChatDeepSeek(
        model=config["DEEPSEEK_MODEL"],
        api_key=config["DEEPSEEK_API_KEY"],
        api_base=config["DEEPSEEK_API_BASE"],
        timeout=60,
        max_retries=0,
        max_tokens=512,
        extra_body={"thinking": {"type": "disabled"}},
    )


# ==================== 三、构造带历史消息的提示词模板 ====================

def build_prompt() -> ChatPromptTemplate:
    """消息顺序：系统规则 -> 已完成的历史 -> 本轮问题。

    模板接收两个输入键：
        history：消息列表，第一轮可以是 []。
        question：本轮用户问题字符串。

    此函数只创建模板，不填充具体问题，也不请求模型。
    """
    # from_messages 是 ChatPromptTemplate 提供的构造模板的方法。
    # 参数是一个 list；其中既能包含 (角色, 文本) 元组，也能包含消息占位符。
    return ChatPromptTemplate.from_messages(
        [
            # 第一项是 tuple：第一个元素是角色，第二个元素是指令文本。
            # 两个相邻的字符串字面量会由 Python 自动拼接，不自动加入换行：
            # "第一段" "第二段" 等价于 "第一段第二段"。
            # system 每次由模板提供，因此不必再重复存入 history。
            ("system", "你是一位耐心的编程老师，请用简体中文简洁回答。"
             "涉及用户信息时只依据对话内容，未提及的信息不要猜测。"),

            # MessagesPlaceholder 插入多条消息，并保留每条的角色与顺序。
            # variable_name="history" 说明它从输入字典的 history 键取值。
            # 第一轮传 []，第二轮传 [HumanMessage(...), AIMessage(...)]。
            # 这与 ("human", "{history}") 不同：后者把历史格式化为一条文本。
            MessagesPlaceholder(variable_name="history"),

            # 普通文本占位符：{question} 会由 LangChain 在调用时填入。
            # 它不是 Python f-string：前面没有 f，填充发生在模板执行时。
            # 当前问题放在历史之后，让模型看到完整的对话顺序。
            ("human", "{question}"),
        ]
    )


# ==================== 四、执行一轮对话：本课最重要的函数 ====================

# 多行函数签名与单行写法一样，只是更易阅读。
# chain: Runnable、question: str 都是参数类型注解。
# list[BaseMessage] 表示“预计保存消息对象的列表”，不是运行时自动类型检查。
# 单独的 * 表示后面的 stream 是“仅限关键字参数”：
# 正确：run_turn(chain, history, question, stream=False)
# 错误：run_turn(chain, history, question, False)
# stream: bool = True 同时给出类型和默认值；不写 stream 时采用流式模式。
# -> str 表示本函数预期返回回答文本。
def run_turn(
    chain: Runnable,
    history: list[BaseMessage],
    question: str,
    *,
    stream: bool = True,
) -> str:
    """完成一轮请求后才保存用户消息和 AI 消息。

    参数：
        chain：由提示词和真实模型组成的链。
        history：调用者持有的历史列表；本函数会修改这个列表。
        question：本轮用户输入，尚未包含在 history 中。
        stream：True 逐片段读取，False 等完整回答。

    返回：
        普通字符串形式的回答正文。

    注意：
        保存历史用的是完整 AIMessage，而不是本函数返回的字符串。
        请求失败或读取流时中断，会在追加历史之前离开本函数。
    """
    # 这个新字典有两个键，恰好与模板的变量名匹配。
    # "history": history 保存对原列表的引用，并没有自动复制列表。
    # 模板会使用这些输入构造 system + 历史 + 当前 question。
    inputs = {"history": history, "question": question}

    # f"..." 是 Python 的格式化字符串，{...} 内的表达式会在此处求值。
    # len(history) 是消息条数，不是字符数、token 数，也不是对话轮数。
    # 本课每轮保存两条消息，所以两轮完整历史通常有 4 条。
    print(f"发送给模型的历史消息数：{len(history)}")

    # print 默认在末尾打印换行；end="" 改为不加换行。
    # flush=True 立即刷新 Python 输出缓冲，使终端及时显示已到达的内容。
    print("AI：", end="", flush=True)

    # if stream 判断传入的布尔值。这里的 stream 是模式开关参数。
    # 它与下面的 chain.stream 方法同名，但属于不同对象，不会相互覆盖。
    if stream:
        # 变量类型注解 + 赋值：
        # AIMessageChunk | None 表示它可以是消息片段，也可以是 None。
        # 这里的 | 是类型联合语法，不是后面组合 LangChain 链的 |。
        # None 是“尚无对象”的标记；先用它表示还没有收到第一个片段。
        full_chunk: AIMessageChunk | None = None

        # chain.stream(inputs) 提供一个可迭代的流式结果。
        # for 每次取出一个片段赋给 chunk；片段可能包含多字、空文本或元数据。
        # 消费此流时会执行模板和模型请求，并等待片段到达。
        # 循环多次是在读取同一次请求，不是每次循环都发送新请求。
        for chunk in chain.stream(inputs):
            # chunk.text 通过点号访问片段的文本。
            # 持续打印新片段正文，且不换行，组成终端中逐步出现的回答。
            print(chunk.text, end="", flush=True)

            # 这是“条件表达式”，格式为：真时的值 if 条件 else 假时的值。
            # 首个片段：full_chunk 还为 None，直接保存 chunk。
            # 后续片段：累加已有 full_chunk 和新的 chunk。
            #
            # 等价于：
            # if full_chunk is None:
            #     full_chunk = chunk
            # else:
            #     full_chunk = full_chunk + chunk
            #
            # is None 判断对象是否为 None；不要把它与 == 的一般值比较混淆。
            # + 对消息片段是类定义的合并操作，会组合正文及相关信息。
            # 不只是数字相加；同一个运算符可由不同类型定义不同的行为。
            # 单独保存最后一个 chunk，通常会丢掉之前到达的正文。
            full_chunk = chunk if full_chunk is None else full_chunk + chunk

        # for 正常结束后，才到这里。没有任何片段时仍为 None。
        # 若网络异常在循环中抛出，程序会跳出函数，走文件末尾的异常处理。
        if full_chunk is None:
            raise ValueError("模型未返回流式消息，本轮不写入历史。")

        # 合并得到的仍是片段对象；这里转换为普通消息，方便存入对话历史。
        # 对本课 AIMessageChunk，它会转换为 AIMessage。
        response = message_chunk_to_message(full_chunk)
    else:
        # 非流式模式：等待模型返回整份 AIMessage，再继续执行下一行。
        # 同一轮只进入 if 或 else 一个分支，所以不会同时发送两次请求。
        response = chain.invoke(inputs)
        print(response.text, end="", flush=True)

    # 空的 print() 打印一个换行，让后续状态消息出现在下一行。
    print()

    # isinstance(对象, 类) 是运行时类型检查，也接受该类的子类实例。
    # 与上面的类型注解不同，这条语句确实会被执行。
    # not 表示取反：不是 AIMessage 时，抛出 TypeError。
    if not isinstance(response, AIMessage):
        raise TypeError("本课需要聊天模型返回 AIMessage。")

    # 请求成功后才保存一整轮，顺序为用户问题、AI 回答。
    # 当前 question 已由模板末尾填入，请求前不重复追加，避免模型看到两遍问题。
    # HumanMessage(content=question) 创建一个带用户角色的消息对象。
    # response 直接使用真实回答消息，保留角色和可能的响应元数据。
    #
    # extend([a, b]) 向原列表追加两个元素，而不是追加一个嵌套列表。
    # 对比：append([a, b]) 只追加一个元素，这个元素本身是列表。
    # history 是可变对象，调用者和函数持有同一个列表，修改会影响下一轮。
    # 若写 history = history + [...]，只是重新绑定局部变量，不是原地修改。
    history.extend([HumanMessage(content=question), response])

    # \n 是字符串中的换行转义；print 末尾还会有它默认的换行。
    print(f"本轮完成，历史共 {len(history)} 条消息。\n")

    # 返回正文供调用者使用；副作用是 history 已经增加了两条消息。
    # str(...) 显式转为普通字符串，统一可能的字符串子类。
    return str(response.text)


# ==================== 五、自动运行两轮真实对话 ====================

# 这里 stream 没有默认值，调用时必须明确写 stream=True 或 stream=False。
# 返回值是消息列表，让调用者可以进一步观察对话历史。
def run_demo(chain: Runnable, *, stream: bool) -> list[BaseMessage]:
    """两轮真实请求：第二轮依赖第一轮的信息。"""
    # 每次调用 run_demo 都创建一个新的空列表。
    # history: list[BaseMessage] 是变量类型注解；[] 是空列表字面量。
    history: list[BaseMessage] = []

    # 这里只预先写好用户问题，回答仍由真实 DeepSeek API 生成。
    # 第一轮提供信息，第二轮提问，不再重复提供姓名和学习内容。
    questions = [
        "我叫小林，正在学习 LangChain。请用一句话向我打招呼。",
        "我叫什么名字？我正在学习什么？请用一句话回答。",
    ]

    # for 依次读取列表中的问题，不需要手工维护索引。
    # 两次 run_turn 都传入同一个 history 列表，不能在循环内部重新设为 []。
    for question in questions:
        print(f"你：{question}")
        # stream=stream 左边是被调用函数的参数名，右边是本函数的变量值。
        # 同一变量名并不表示递归，只是在把模式开关继续传下去。
        run_turn(chain, history, question, stream=stream)

    # 正常完成两轮后，列表顺序为 human1、ai1、human2、ai2。
    # 对调用者而言，此返回值和函数内部 history 指向同一个列表。
    return history


# ==================== 六、交互聊天与历史清空 ====================

# -> None 表示没有需要交给调用者的业务返回值。
# 不带值的 return 也会返回 None，但它仍然能立即结束函数。
def run_chat(chain: Runnable, *, stream: bool) -> None:
    """输入 /clear 清空历史，/exit 结束；空输入不请求模型。"""
    # 一个交互会话只创建一次 history；它位于 while 循环外。
    # 列表随会话更新，但退出进程后不会自动写入文件或数据库。
    history: list[BaseMessage] = []
    print("交互模式：每轮调用真实 API。/clear 清空历史，/exit 退出。")

    # while True 是持续循环，直到函数 return 或抛出未在此处处理的异常。
    # input 会等待用户输入，所以不是无休止占用 CPU 的空转循环。
    while True:
        try:
            # input 显示提示文字并读取一行，返回字符串，不包含行末换行。
            # strip 去掉首尾空白，使空格输入变成 ""，便于识别空输入。
            question = input("你：").strip()
        except EOFError:
            # 标准输入结束时 input 可能抛出 EOFError，例如输入流已关闭。
            # except 只处理 try 代码块中对应类型的异常。
            print("\n输入结束。")
            return

        # == 比较两个字符串的值；= 才是赋值运算，不能混用。
        if question == "/exit":
            # return 结束整个 run_chat 函数，而不是仅跳过这轮循环。
            return

        if question == "/clear":
            # clear 原地清空列表。下一轮仍使用这个列表，但它已没有历史消息。
            # 这不是要求服务商删除日志，也不是删除模型学到的知识。
            history.clear()
            print("本地历史已清空。\n")
            # continue 跳过本轮剩余代码，直接回到 while 开头。
            # 因此 /clear 不会被当作普通问题发给模型。
            continue

        # 空字符串的布尔值为 False，所以 not question 为 True。
        # 空输入不会触发真实 API 调用。
        if not question:
            continue

        # 此处只会收到非空、非命令的普通问题。
        # 请求错误在文件末尾统一处理；本例遇到该错误后会退出程序。
        # 因此 run_turn 没有写入失败轮次，但也没有实现自动留在聊天中重试。
        run_turn(chain, history, question, stream=stream)


# ==================== 七、读取命令行参数并选择模式 ====================

def main() -> None:
    """组织命令行参数、链的构造和程序运行模式。"""
    # ArgumentParser 创建命令行参数解析器。
    # __doc__ 引用本文件开头的文档字符串，用作 --help 的说明。
    arguments = argparse.ArgumentParser(description=__doc__)

    # action="store_true"：命令出现时存 True，未出现时默认为 False。
    # --chat 在 options 中对应属性 chat。
    arguments.add_argument("--chat", action="store_true", help="开启交互聊天")

    # 命令行中的连字符通常转换为属性名的下划线：
    # --no-stream 在 options 中对应 no_stream。
    arguments.add_argument("--no-stream", action="store_true", help="改用 invoke()")

    # parse_args 默认读取程序路径之后的命令行参数。
    # 返回 Namespace 对象，可用 options.chat 等点号属性访问。
    # --help 会显示说明并正常退出，不继续创建客户端或请求模型。
    options = arguments.parse_args()

    # build_prompt() 和 build_model() 分别返回模板对象和模型客户端。
    # 这里的 | 是 LangChain 对 Runnable 对象定义的“顺序组合”操作。
    # 它不是 run_turn 类型注解中表示“可以是两种类型”的 |。
    # 创建 chain 不会自动生成回答，执行 invoke 或消费 stream 才请求模型。
    #
    # 本课要保存 AIMessage，末尾不接 StrOutputParser。
    # 若直接把输出解析成字符串，会失去作为消息对象保存的便利。
    chain = build_prompt() | build_model()

    # chat 为 True 进入交互，否则使用预先定义的两轮问题。
    if options.chat:
        # not 是布尔取反：
        # 未写 --no-stream：options.no_stream 为 False，not False 为 True。
        # 写了 --no-stream：options.no_stream 为 True，not True 为 False。
        run_chat(chain, stream=not options.no_stream)
    else:
        run_demo(chain, stream=not options.no_stream)


# ==================== 八、程序入口与异常处理 ====================

# 直接运行这个文件时，Python 把本模块的 __name__ 设为 "__main__"。
# 被其他文件 import 时，__name__ 是模块名，不会执行下方入口代码。
# 因此别的文件可以导入函数，不会因为导入就自动开始聊天或请求 API。
if __name__ == "__main__":
    # stdout 是标准输出，stderr 是标准错误输出。
    # reconfigure 统一使用 UTF-8，避免 Windows 重定向或终端编码不一致。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    # try 负责正常执行；对应异常发生后，跳到第一个匹配的 except。
    # except 并不是无论如何都会执行的“后续步骤”。
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C 通常产生 KeyboardInterrupt。
        # 若是在本轮请求或读取响应时中断，因为尚未执行 extend，
        # 未完成的本轮不会写入历史。
        print("\n已停止。未完成的这一轮不会写入历史。")
        # SystemExit 请求进程退出；130 是本程序为用户中断采用的退出码。
        # 一般 0 表示正常结束，非 0 表示异常或未成功完成。
        raise SystemExit(130)
    except ValueError as error:
        # as error 将捕获的异常对象绑定到变量 error，便于输出说明。
        # 本课主动检查到缺失配置、没有流式消息时会抛出 ValueError。
        print(f"配置或输入错误：{error}")
        raise SystemExit(2)
    except APITimeoutError:
        # 更具体的超时异常放在连接异常前面；Python 只运行首个匹配分支。
        print("\n请求超时，本轮未写入历史，请检查网络后重试。")
        raise SystemExit(1)
    except APIConnectionError:
        print("\n连接失败，本轮未写入历史，请检查网络和 API 地址。")
        raise SystemExit(1)
    except APIStatusError as error:
        # APIStatusError 表示服务端返回了错误 HTTP 状态。
        # error.status_code 读取状态码；不打印完整请求、认证信息或响应正文。
        # 两个相邻字符串会自动拼接；第一个 f-string 插入状态码。
        print(f"\nAPI 返回 HTTP {error.status_code}，本轮未写入历史。"
              "请检查 Key、模型名和 API 余额。")
        raise SystemExit(1)

# 注意：本程序没有捕获所有类型的异常。
# 例如代码中检查到错误的消息类型时会抛出 TypeError，保留报错堆栈，
# 方便发现编程问题，而不是把所有错误都包装成“网络失败”。
