# 第二课：消息历史、多轮对话与流式输出

第一课完成了一次请求。本课让第二次请求利用第一轮的信息，并把生成中的文本实时显示出来。继续使用项目根目录的 DeepSeek `.env`，无需新依赖。

建议用 40–60 分钟完成。先看两轮演示，再进入交互模式，最后做 review。

## 本课的核心问题

**模型怎样知道你上一轮说过什么？**

在本课的调用方式中，你需要把前面的消息再次放进请求。Python 列表保存历史，提示词模板将历史插入消息序列。仅仅复用同一个 model 或 chain 对象，不会自动保存用户对话。

```text
第一轮：system → human 1 → 模型 → ai 1
第二轮：system → human 1 → ai 1 → human 2 → 模型 → ai 2
```

本课的历史仅存在程序内存中，退出或重启后消失。它不是长期记忆，也不会修改模型参数。

## 先运行两轮演示

在 VS Code 的项目根目录终端运行：

```powershell
.\.venv\Scripts\python.exe lessons\02_chat_history\main.py
```

会发起两次真实请求：第一轮告诉模型“我叫小林，正在学习 LangChain”，第二轮询问姓名和学习内容。

观察两项变化：第二轮提交的历史消息数从 0 变成 2；完成后历史总数从 2 变成 4。模型回答是实际 API 返回内容，不是写死的预期答案。检查它是否从历史中提取了“小林”和“LangChain”，不要只以程序退出成功判断回答质量。

回答会逐块显示。对简短回答或较快网络，它看起来可能接近一次显示完毕；这不代表没有使用流式接口。

## 再进入交互模式

```powershell
.\.venv\Scripts\python.exe lessons\02_chat_history\main.py --chat
```

依次输入：

```text
我叫小林，正在学习 LangChain。
我叫什么名字？我在学习什么？
/clear
我叫什么名字？
/exit
```

`/clear` 清空本地历史后，下一次请求不再携带之前的姓名。模型应说明不知道，但模型生成不能作为可靠的事实保证。清空本地列表也不等同于删除服务商可能保存的日志。

每个非空普通输入产生一次真实请求。空输入、`/clear` 和 `/exit` 不请求 API。自动重试关闭，单轮最多生成 512 个 token；历史随轮数累积，后续请求的输入量也可能增加。本课先学习手工历史，裁剪与持久化留待后续扩展。

## 按这个顺序 review main.py

### 1. MessagesPlaceholder：把消息列表插入模板

```python
MessagesPlaceholder(variable_name="history")
```

它接收消息列表并保留消息的角色和顺序。普通的 `("human", "{history}")` 会把变量格式化为一条 human 消息中的文本，语义不同。

第一课的变量主要是字符串；第二课的输入字典同时包含列表和字符串：

```python
inputs = {"history": history, "question": question}
```

模板顺序是系统规则、历史消息、本轮问题。system 每次由模板提供，不需要反复追加到 history。

### 2. history：保存完整的一轮

```python
history.extend([HumanMessage(content=question), response])
```

`HumanMessage` 保存用户输入；`AIMessage` 保存模型实际回答以及可能的元数据。只有用户问题没有 AI 回答，无法完整表达前面讨论过的内容，例如模型提出的选项。

这行放在成功收到完整回答之后。如果请求中断或失败，本轮两条消息都不会追加。请求前也不把当前问题重复放进 history，因为模板末尾已经包含它。

列表是可变对象。`run_turn()` 内的 `history.extend()` 会修改调用者持有的列表，所以下一轮会看到更新后的历史。`history.clear()` 清空的是这个列表。

### 3. 为什么没有 StrOutputParser？

第一课最后需要字符串。本课要保存消息角色及响应信息，因此使用：

```python
chain = build_prompt() | build_model()
```

`invoke()` 返回 `AIMessage`，不是解析器提取后的文本。显示正文时使用 `response.text`，保存历史时保留 response 对象。

### 4. invoke() 与 stream()

| 调用方式 | 如何获取结果 | 返回的主要对象 |
| --- | --- | --- |
| `chain.invoke(inputs)` | 等待整份结果返回 | `AIMessage` |
| `chain.stream(inputs)` | 迭代读取生成中的片段 | `AIMessageChunk` |

运行非流式版本进行对比：

```powershell
.\.venv\Scripts\python.exe lessons\02_chat_history\main.py --no-stream
```

这会重新发起两次请求，回答内容可能与之前不同。`stream()` 的循环读取同一次请求的多个片段，并不是每次循环都发送新请求。

### 5. 为什么要累加 chunk？

```python
full_chunk = chunk if full_chunk is None else full_chunk + chunk
```

每个片段只包含部分结果，还可能携带元数据。最后一个片段并不等于整份回答；有些片段甚至没有正文。累加消息片段会组合内容和相关消息信息。

流式结束后，`message_chunk_to_message(full_chunk)` 将完整消息片段转成普通消息，再写入历史。`print(chunk.text, end="", flush=True)` 不追加换行并及时刷新终端，让你看到逐步生成的正文。

### 6. 为什么第二轮会用到前面的信息？

history 是应用提供的上下文。第二轮请求再次包含第一轮的用户输入和真实 AI 回答，所以模型有机会据此作答。**对话记忆来自发送的上下文，而不是 Python 模型对象自动记住了你。**

这是当前简单链的行为。Agent、服务端会话和持久化存储可以采用其他状态管理方式，之后会再学。

## 本课涉及的 Python 特性

- `list` 与可变性：`extend()`、`clear()` 修改原列表。
- 类型注解：`list[BaseMessage]` 和 `AIMessageChunk | None`。
- 迭代器：用 `for` 消费流式响应。
- 关键字参数：`*, stream=True` 表示 stream 需要以关键字传入。
- `while` 与输入：持续接收交互问题，处理退出和空输入。
- `argparse`：通过命令行参数选择聊天或非流式模式。

先关注 build_prompt 和 run_turn；build_model 沿用第一课的配置逻辑。

## 在 VS Code 中调试

选择“第二课：两轮演示”或“第二课：交互聊天”，按 F5。建议依次设置断点：

1. `inputs = {"history": history, "question": question}`：观察第一轮和第二轮的 history。
2. `for chunk in chain.stream(inputs)`：观察 chunk 的正文；不要展开客户端认证配置。
3. `history.extend(...)`：观察消息追加前后的数量和角色。

打开本讲义后，按 `Ctrl+Shift+V` 查看 Markdown 排版预览。

## 练习与 review

打开 [exercises.md](exercises.md)，先完成“清空历史”和“观察消息序列”，再修改代码。可以把你不理解的代码行或 review 答案发到本会话。

本课完成标准：能运行真实两轮对话，解释第二轮的消息组成，理解 chunk 累加，亲自观察清空历史后的变化。

## 官方参考

- [LangChain：消息与对话历史](https://docs.langchain.com/oss/python/langchain/messages)
- [LangChain：invoke 和 stream](https://docs.langchain.com/oss/python/langchain/models#stream)
- [ChatDeepSeek](https://docs.langchain.com/oss/python/integrations/chat/deepseek)

资料核对日期：2026-10-05，代码继续使用项目现有的固定依赖版本。
