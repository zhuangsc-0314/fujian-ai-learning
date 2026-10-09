"""第一课练习：补全下面的提示词，再运行本文件。

运行：.\\.venv\\Scripts\\python.exe lessons\\01_first_chain\\exercises.py
这里只观察提示词内容，不调用模型。
"""

import sys

from langchain_core.prompts import ChatPromptTemplate


def build_exercise_prompt() -> ChatPromptTemplate:
    # TODO 1：在 system 消息中增加 {audience} 变量，说明目标读者。
    # TODO 2：在 human 消息中增加 {example_count}，要求给出指定数量的例子。
    return ChatPromptTemplate.from_messages(
        [
            ("system", "你是一位编程老师，请用{language}回答。目标读者是{audience}。"),
            ("human", "请解释，并给出{example_count}个例子。"),
        ]
    )


def main() -> None:
    inputs = {
        "language": "简体中文",
        #"topic": "Python 字典",
        "audience": "没有编程经验的初学者",
        "example_count": 2,
    }
    prompt = build_exercise_prompt()
    print(f"模板实际使用的变量：{prompt.input_variables}")
    print("\n发送给模型之前的消息：")
    for message in prompt.invoke(inputs).to_messages():
        print(f"{message.type}: {message.content}")

    # TODO 3：临时删除 inputs 中的 topic，观察 KeyError，再恢复它。
    # TODO 4：解释为什么输入字典里有 audience，但初始输出没有目标读者。


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
