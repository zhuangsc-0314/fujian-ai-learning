# 1.1：看清一次真实模型请求

## 1. 本次交付什么

用一段公开的福建考试历史说明，请 DeepSeek 概括范围和题型，返回真实正文。默认原文和来源见 [material.txt](material.txt) 与 [SOURCE.md](SOURCE.md)。本课是 SDK 对照；下一小课 1.2 再使用 LangChain 模型接口，不维护两套正式平台服务。

## 2. 为什么现在学

你已经练习输入、配置和依赖环境。现在把它们接到真实模型，先看清什么被发送、在哪里联网、返回的是什么。之后理解 LangChain 的 invoke 和消息对象，才能分清框架抽象与模型服务。

## 3. 三个必要概念

| 概念 | 通俗解释 | 本课对应 |
| --- | --- | --- |
| API 与 SDK | API 是远端服务接受请求的接口；SDK 是帮你处理请求和返回值的 Python 工具包 | openai 包通过 DeepSeek 官方 base_url 访问 DeepSeek，使用 DeepSeek Key |
| 消息 messages | 给模型的一组有角色的文字 | system 写任务约束；user 放学习目标与材料；材料不提升为系统指令 |
| 响应 response | 服务返回的结果对象，里面除了正文还有状态与用量 | choices[0].message.content 是正文；finish_reason、usage 是元数据 |

API Key 是鉴权凭证，由 SDK 放进请求头；它没有被拼到消息正文里。消息只是本次发送的内容，模型不会自动读取本机 .env 或目录。

## 4. 输入、过程、输出和模块关系

```text
公开 material.txt ──读取/检查──┐
.env + 进程环境 ──读取/检查──┤
                             ↓
                 构造 system/user 消息（本地）
                             ↓
                 SDK create（这里才联网）
                             ↓
                   DeepSeek API → 响应对象
                             ↓
                     正文 + 少量元数据
```

普通文件/配置处理不需要 LangChain。本课全部放在教学入口，未创建账号、数据库或平台 API；下一课再比较模型接口，之后才提取正式 AI 模块。

## 5. 最小示例与运行方式

先读 [详细注释 main.py](main.py)。仓库根目录执行：

```powershell
.\scripts\uv-project.cmd sync --locked
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_01_first_sdk_call\main.py
```

已有环境首次拉取本课后同步一次即可。每次正常运行尝试一次真实模型请求，可能计费；max_retries=0，max_tokens=256。本课直接使用 SDK，所以 pyproject.toml 将已安装的 openai 3.26.1 显式列为直接依赖；锁文件元数据已更新，包版本未升级。

VS Code 左侧运行和调试选择 **项目 1.1：最小真实 SDK 请求**，在 `client.chat.completions.create(...)` 行设断点并按 F5。跨过这一行才发起请求。按调试停止可以停止本地进程，无法保证取消服务端已开始的计算或费用。

可选自己的材料文件路径（初次使用公开内容；私人材料发送前须确认授权）：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_01_first_sdk_call\main.py <材料txt路径>
```

## 6. 关键代码与 Python 语法

- `OpenAI(...)` 创建兼容 SDK 客户端，类名不决定请求供应商，`base_url` 决定地址。本课仅允许 DeepSeek 官方端点。创建客户端和 `build_messages` 都不会调用模型。
- `client.chat.completions.create(...)` 发请求。传给它的是消息列表和参数，不是整份配置字典。
- `[{"role": ..., "content": ...}, ...]` 是列表嵌套字典。`response.choices[0].message.content` 则先对列表取第一个候选，再访问对象属性。
- `dict[str, str]`、`list[dict[str, str]]` 是类型提示，不自动进行运行时校验。字典推导式 `{name: 表达式 for name in names}` 将多个变量名映射为读取值。
- `with OpenAI(...) as client` 在退出时关闭连接资源；和以前 `with open(...)` 关闭文件的思路一致。
- `except` 分类处理错误；`finally` 即使函数 return 或发生异常也会执行，所以每次都会报告请求尝试数。该数字不能证明服务端执行次数或计费次数。
- `usage` 是上游报告的 token 用量。token 是模型处理的片段单位，不能直接等同于字数。1.4 再学习缓存、价格与账单；本课不估算人民币金额。
- timeout=30 是 SDK 网络操作超时设置，不是严格的整个任务耗时上限。超时后服务端是否完成未知，不能自动重复请求。

## 7. 你独立完成的小修改

找到 `TODO 1.1`，只改 `LEARNING_GOAL`，在摘要目标后加入 **“列出原文无法回答的问题”**，保留 SYSTEM_MESSAGE 的事实与历史限制。

运行后对照原文：未来考试日期、具体岗位、分数线是否能由这段原文确定？用自己的话说明模型回答哪些有依据、哪些应说不足。不要为得到满意回答不断重复请求；先检查消息与目标是否正确。

## 8. 正常、非法和不可信案例

| 案例 | 本课预期 | 如何验证 |
| --- | --- | --- |
| 默认公开材料 | 一次真实请求，概括材料内范围与题型 | 正常运行，人工逐句对照，不推定未来考试要求 |
| 空/2001字符正文 | 退出2，请求0，不自动截断 | 离线验证程序检查 |
| 缺 Key/MODEL/地址 | 退出2，说明变量名，不回显值，请求0 | 离线验证程序使用惰性标记；不改真实 .env |
| 不可信正文 | 保持在 user 数据里，不提升为 system 指令 | 离线检查消息位置；不保证模型完全抵抗注入 |
| 上游鉴权/限流/连接/超时 | 固定分类提示，不显示原始异常；无自动重试 | 分支已实现，尚未向真实供应商制造这些故障；1.3 再验证 |

离线检查命令：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_01_first_sdk_call\verify_cases.py
```

它阻止 SDK 创建，不生成替身模型回答，不验证鉴权成功。材料正文里的“打印Key”等文字不能执行本机代码；消息角色与提示词约束也不能单独保证生成内容安全。

## 9. 双重验收

**项目交付**：公开材料真实调用成功；Key 不进入输出；非法输入本地拒绝；响应正文可以定位到原文事实。实际结果见 [RUN_RESULTS](RUN_RESULTS.md)，不是保证下一次生成逐字相同。

**学习掌握**：你独立改目标；指出哪行联网；解释 system/user 与响应对象/正文区别；运行离线缺 Key 案例并指出在请求前哪一步失败。只回复“看懂了”或程序成功不能代替这些证据。

## 10. 根据你的结果推进

修改后告诉我“1.1 已完成”，附上述三点简短解释。先评审代码与实际回答，再补练或进入 1.2：同一段材料用 ChatDeepSeek.invoke 调用，比较 SDK 与 LangChain 的输入、返回值及异常。0.1/0.2/0.3 尚缺的解释证据继续保留，不代写。

接口核对日期 2026-10-10：[OpenAI 官方 Python Chat Completions Reference](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create)、[DeepSeek Chat API](https://api-docs.deepseek.com/api/create-chat-completion/)、[DeepSeek 思考模式](https://api-docs.deepseek.com/guides/thinking_mode/)。OpenAI Reference 完整页面与本机 SDK 签名可核实；DeepSeek 完整页本轮读取超时，采用官方索引摘要加真实请求确认所用参数，不宣称已完整审查供应商全部接口。供应商差异不能照搬 OpenAI 模型示例。
