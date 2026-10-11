# 1.4-B：真实长短材料用量比较

本次目标：用同一模型、目标、系统约束和输出上限，比较同一公开材料的短版与完整版。用户已独立完成差值练习，13项基础及6项练习探针通过；下一步由用户运行真实观察。真实实验未运行，整节未验收。

## 为什么现在学

1.4-A已能展示用量，现在练习从记录作比较。材料长度只是输入的一部分，不能把字符差当token差；一次比较也不能证明性能规律或实际费用。

新概念只有两个：

- **控制变量**：只改变材料长度，让比较更容易解释。短版取原文最后一句，长版沿用1.1原段；目标/模型/系统约束不改。
- **调用记录**：从真实响应中摘取请求模型、返回模型、用量、耗时、请求ID和结束原因。缺字段为None，JSON显示null，含义是未知。

## 输入 → 处理 → 输出

输入：[短版](material_short.txt)与[原段](../01_01_first_sdk_call/material.txt)，来源见[官方历史说明](../01_01_first_sdk_call/SOURCE.md)。短版9字符，长版78字符；这是历史教学材料，不代表未来考试规则。

处理：比较入口按明确路径导入1.2，分别调用原main；原入口继续负责材料/配置检查、消息、ChatDeepSeek和异常处理。输出上限256、timeout30秒、max_retries=0、thinking关闭。最多两次客户端尝试；首次失败就停止，失败不会伪装成零用量记录。

输出：原入口显示回答供你核对原文，再输出两条允许字段记录及输入token差值。耗时包含invoke及正文处理，不包含材料读取/初始化；两次观察不代表稳定均值。真实回答中有关“客观题”的定义仍应说明原文依据不足。

## 先做离线练习

在仓库根目录运行默认预览与基础检查；两条均不读.env、不调用模型，预期退出0：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04b_usage_comparison\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04b_usage_comparison\verify_cases.py
```

打开[main.py](main.py)中的`input_token_difference()`，完成保留的TODO：

1. 从两条记录各取`input_tokens`。
2. 任一是None，返回None。
3. 两者都有值，返回长材料减短材料；0是合法已知用量。

不要按字符数估算，不硬编码真实结果，不修改验收规则。练习使用人工元数据，不生成模型回答：

| 短版输入token | 长版输入token | 函数预期返回 |
| --- | --- | --- |
| 10 | 20 | 10 |
| 0 | 0 | 0 |
| 0 | 5 | 5 |
| None/缺字段 | 20 | None |
| 10 | None | None |

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04b_usage_comparison\verify_cases.py --exercise
$LASTEXITCODE
```

用户差值修改已通过6项练习探针，当前退出0；最初骨架TODO未完成时退出1属于历史预期。助手检查通过不等于用户已独立运行或完成比较解释。

## 关键代码与语法

原1.2新增`collect_call_record()`摘取允许字段；只读取HTTP头中的`x-request-id`，不打印整个头。请求ID可能缺失，生成结果ID不能替代它。

```python
records.append(collect_call_record(
    reply, settings["DEEPSEEK_MODEL"], perf_counter() - started, len(text),
))
```

先构造一个记录字典，再用`.append()`加入列表。`records is not None`检查是否启用记录；不能写成`if records`，因为刚创建的空列表是假值，也应收集第一条记录。

`def main(*, material_path=None, records=None)`中的`*`要求后续参数用名称传入。`Path | None`和`int | None`表示允许两种类型的类型提示，本身不执行业务校验。按路径导入的辅助函数沿用1.3-C方式，不要求本节独立编写；导入不自动执行原main。

## 再做真实观察

离线练习完成并经评审后运行一次下面的命令。会读取本机配置，最多两次真实尝试，可能计费；不要为重复贴日志再跑，不输出.env或Key。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04b_usage_comparison\main.py --live
$LASTEXITCODE
```

正常预期：两条真实记录、差值、退出0。非法参数在配置读取前退出2；模型失败停止后续尝试并沿用原退出码。用量/请求ID缺失为未知；超时不能证明未执行。`length`可能截断；`stop`不能证明内容正确，均不自动重发。

解释实际输入为何变化，以及输出token/耗时为何不一定随材料长度同比增长。不要只说“材料长，所以所有指标都大”：输出还取决于生成结果，耗时还受网络、缓存及服务状态等影响，本次没有控制或测量所有因素。

## 双重验收与下一步

功能：13项基础离线检查及相关回归通过；真实两次观察须另记录实际结果，不以离线元数据替代。能力：你独立完成差值、提供检查结果，并解释比较现象；助手检查不算你的独立运行。

本次实际验证和Git交接见[任务记录](../../docs/tasks/1.4-b-usage-comparison.md)。真实运行失败时先定位原因，本课不反复制造付费失败；真实观察结束后再决定是否进入价目/预算小步。

接口依据：[DeepSeek对话补全](https://api-docs.deepseek.com/api/create-chat-completion/)、[LangChain响应头参数](https://reference.langchain.com/python/langchain-openai/chat_models/base/BaseChatOpenAI/include_response_headers)。沿用已安装langchain-deepseek1.1.1/langchain-openai1.6.7，本机字段核验通过，无新增依赖。
