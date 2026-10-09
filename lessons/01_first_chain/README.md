# 第一课：从 .env 到第一条真实 DeepSeek 链

建议用 30–45 分钟完成。先配置并运行，再逐段 review，最后做练习。

## 学习目标

1. 分清 LangChain、提示词和模型的职责。
2. 用字典给提示词模板传入变量。
3. 从 `.env` 读取真实 API 配置。
4. 解释 `prompt | model | parser` 和 `invoke()`。
5. 用断点观察 API 请求发生的时机。

## 配置和运行

打开项目根目录的 `.env`，在等号后填入自己的 DeepSeek API Key 并保存：

```dotenv
DEEPSEEK_API_KEY=填入你的真实Key
DEEPSEEK_MODEL=deepseek-flash
DEEPSEEK_API_BASE=https://api.deepseek.com
```

Key 可在 [DeepSeek API 平台](https://platform.deepseek.com/api_keys) 创建。模型和地址已按官方文档填写。地址是 API 根地址，不是聊天网站网址，也不要添加 `/chat/completions`。

`.env` 已被 Git 忽略，代码不打印 Key。可分享的配置模板是 `.env.example`。VS Code 插件账号不能代替本程序的 API Key。

在项目根目录的 VS Code 终端运行：

```powershell
.\.venv\Scripts\python.exe lessons\01_first_chain\main.py
```

如果依赖尚未安装：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

你会依次看到填充后的消息、“正在请求 DeepSeek”和真实回答。回答由服务端模型生成，可能每次不同。每次运行只调用模型一次，关闭自动重试，超时 60 秒，最多生成 512 个 token。本课关闭思考模式，先观察普通文本回答。API 请求可能按用量计费。

## 理解数据流

LangChain 组织模型应用的组件；模型负责生成回答。安装 LangChain 不会下载大模型，也不会自动获得服务访问权限。本课使用 DeepSeek 托管服务。

```text
输入字典 -> Prompt -> Model（真实 API）-> Output Parser -> 字符串
```

| 组件 | 输入 | 输出 | 作用 |
| --- | --- | --- | --- |
| ChatPromptTemplate | dict | ChatPromptValue | 填入变量，构造消息 |
| ChatDeepSeek | 提示词值或消息 | AIMessage | 请求 DeepSeek |
| StrOutputParser | 模型消息 | str | 提取文本 |

## 跟着 main.py 做 review

### 1. 输入字典和模板变量

```python
inputs = {"language": "简体中文", "topic": "LangChain"}
```

字典键名对应模板中的 `{language}`、`{topic}`。缺少必需键会报错；模板没有使用的额外键不会自动出现在消息里。

模板字符串没有 `f` 前缀，变量由 LangChain 在调用时填充。要显示字面量花括号，可以写 `{{` 和 `}}`。

### 2. 消息角色

`from_messages()` 接收角色与文本组成的元组列表。`system` 说明回答方式；`human` 是用户的问题；模型响应对应 `ai` 消息。

`build_prompt()` 返回模板，`prompt.invoke(inputs)` 才填入变量。这一步在本地执行，不请求模型。

### 3. 从 .env 加载配置

`Path(__file__).resolve().parents[2]` 找到项目根目录，避免在不同目录运行时找错配置文件。

`load_dotenv(..., override=True)` 以本项目 `.env` 为准，覆盖同名环境变量。`os.getenv()` 读取值，`.strip()` 去掉首尾空白。代码先检查三项配置是否缺失，未填 Key 时不会发送请求。

Key、模型名和地址属于连接配置；inputs 提供本次问题内容。两类数据各司其职。

### 4. 组合与执行

```python
chain = prompt | model | parser
result = str(chain.invoke(inputs))
```

这些 LangChain 对象支持 Runnable 接口，`|` 表示顺序组合。前一步的输出传给后一步，类型仍须兼容。这种组合方式属于 LangChain Expression Language（LCEL）。

创建 model 和 chain 不产生一次模型回答；执行 `chain.invoke(inputs)` 才填充模板、请求模型、解析结果。`invoke()` 是统一调用接口，并不总意味着网络请求。

### 5. 消息对象与字符串

模型返回 `AIMessage`，它包含正文和可能的用量等信息。`StrOutputParser` 提取文本，因此最终结果是 `str`。

代码用 `str(...)` 将结果统一为普通字符串，便于观察类型；部分版本会返回字符串子类。解析器不判断答案是否正确，也不保证文本符合 JSON 或业务规则。结构化输出将在后续课程学习。

### 6. 相关 Python 特性

- 函数：`build_prompt()`、`build_model()` 和 `main()` 分别组织一个步骤。
- 类型注解：`-> ChatDeepSeek` 提示返回类型，Python 不会仅凭注解强制检查。
- 列表推导式：收集缺失的配置名称。
- 入口判断：直接运行文件才执行 `main()`，被 import 时不会自动请求 API。
- 异常处理：分别处理认证、额度、超时、连接和 HTTP 错误。

## 用 VS Code 设置断点

在 `result = str(chain.invoke(inputs))` 行左侧点击，选择“第一课：逐步调试”，按 `F5`。先观察 `inputs` 和 `prompt_value`；继续执行后观察 `result`。

想单独观察 `AIMessage` 时，可以临时把链调用替换为下面两行。不要与原链调用同时保留，否则会发起两次请求：

```python
response = model.invoke(prompt_value)
result = parser.invoke(response)
```

分享调试截图时避免展开包含认证配置的客户端对象。

## 动手练习

1. 将 topic 改为“Python 字典”，预测提示词，再运行观察真实回答。
2. 修改 system 消息，让老师面向没有编程经验的初学者。
3. 完成同目录 `exercises.py` 的四个 TODO。它只预览模板；需要真实回答时，将修改后的模板和输入用于 `main.py`。
4. 临时将 `.env` 中模型名留空，观察配置错误，再恢复。

练习脚本运行命令：

```powershell
.\.venv\Scripts\python.exe lessons\01_first_chain\exercises.py
```

## Review 问题

1. 哪一行构造模板，哪一行填入变量？
2. 创建 model 和 chain 时是否请求模型？
3. 移除 parser 后，最终得到什么对象？
4. `.env` 配置与 inputs 分别负责什么？
5. 什么原因可能导致“程序能运行，但 API 请求失败”？

<details>
<summary>完成 review 后，再展开参考答案</summary>

1. `from_messages(...)` 构造模板；`prompt.invoke(inputs)` 填充变量，执行整条链时也会填充。
2. 没有，请求发生在 `chain.invoke(inputs)` 的模型步骤。
3. 本课聊天模型返回 `AIMessage`。
4. `.env` 配置认证、模型与服务地址；inputs 提供本次提示词变量。
5. 无效 Key、API 余额不足、模型名或地址错误、网络或代理问题等。

</details>

## 常见问题

| 提示 | 检查方向 |
| --- | --- |
| 缺少配置 | .env 是否填写并保存 |
| 认证失败 | DeepSeek Key 是否有效 |
| 请求受限 | API 余额、额度或频率 |
| 连接失败或超时 | 服务地址、网络和代理 |
| HTTP 404 | 模型名和 API 地址 |
| ModuleNotFoundError | 是否使用项目 .venv，依赖是否安装 |

## 官方参考

- [ChatDeepSeek 集成](https://docs.langchain.com/oss/python/integrations/chat/deepseek)
- [DeepSeek API 入门与当前模型名](https://api-docs.deepseek.com/)
- [提示词模板](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

完成标准：跑通一次真实 API、完成模板练习，并解释五个 review 问题。
