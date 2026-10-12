# 2.2：用真实DeepSeek生成结构化学习卡

2.1已学人工dict→Pydantic实例；现在让真实模型产生JSON，再按同一LearningCard规则解析。无新依赖，不引入Tool Calling/Agent/网页/数据库。示例仍是公开2023年历史说明，不推定未来考试规则。

## 1. 本次交付

生成summary、keywords、evidence_quote、information_gap四字段候选；保留原响应、解析结果和解析错误，能够区分本地失败、请求失败、结果不合格。候选始终待人工核对，不自动保存。

## 2. 为什么现在学

用户已独立定义字段并修复拼写/最小长度，知道类型/长度不证明事实。下一步用这一规则接模型：不用靠回答里的标题猜字段，也不重新定义第二套学习卡。将配置、模型、提示词和解析收敛在adapter.py，main.py只组织步骤和展示。

## 3. 三个核心概念

```python
structured_model = model.with_structured_output(
    LearningCard, method="json_mode", include_raw=True,
)
result = structured_model.invoke(messages)
```

- **结构化调用包装器**：model是ChatDeepSeek适配对象；with_structured_output创建一个带invoke的包装器，增加输出格式要求和本地解析。创建时不发模型请求；structured_model.invoke才底层调用模型，再处理响应。本课识别Runnable有invoke即可，不要求先学LCEL管道。
- **JSON模式**：json_mode请求供应商response_format=json_object。它要求JSON格式，不等于供应商保证每个字段及限制都正确；提示词仍需明确json和期望格式。本课把字段schema及形状示例放system，原文放HumanMessage，不把原文命令提升成指令。
- **raw / parsed / parsing_error**：include_raw=True使结果是dict；raw为原AIMessage，parsed成功时是LearningCard，parsing_error为本地解析/字段错误或None。供应商返回内容后，仍可能在解析阶段失败。

| 数据 | 怎样读取 | 用途 |
| --- | --- | --- |
| result | result["parsed"]等字典键 | 包装器的结果容器 |
| raw | raw.content / raw.usage_metadata | 原JSON正文/用量；不是LearningCard |
| parsed | card.summary / card.information_gap | 已解析实例的字段 |
| parsing_error | 只检查是否None，不回显原异常 | 区分本地解析失败，避免误报成功 |

`LearningCard.model_json_schema()`产生描述字段的JSON对象，不是模型生成结果；json.dumps把它转成提示词中的字符串。固定模块导入复用2.1类和1.2配置，仅为工程辅助，不把importlib列为新学习验收。

## 4. 完整数据流

```text
公开原文 → 输入与schema一致检查 → system/json规则 + human/原文
→ 本机配置（仅live） → ChatDeepSeek → 结构化包装器
→ structured_model.invoke：远程JSON生成 + 本地解析
→ raw用量 / parsed实例 / parsing_error
→ 空正文/截断/字段/引用检查
→ 带业务占位归属/版本的待人工核对候选
```

输入/配置失败调用0；invoke抛超时可能服务端已执行，不自动重试。JSON解析失败发生在请求已尝试之后，不能据此说免费。输出512token只是上限，不是预算。业务元数据不交模型填写，Key不进消息；LangSmith远程追踪沿用现有关闭规则。

## 5. 先预览，再看真实结果

项目根目录运行默认预览，不读.env、不发请求：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\main.py
```

预期材料78字符/system-human/4字段，退出0，调用0。有意保持2.1四个字段一致；名字异常在配置/请求前停止，避免错误schema发起付费调用。

助手已经用真实API成功尝试一次，parsed为LearningCard，470输入/140输出/610总token、stop、退出0，完整证据见RUN_RESULTS.md。先看该记录，不为展示TODO重复付费。若你显式选择下面命令，将使用本机.env真实Key，最多尝试一次，可能计费：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\main.py --live
$LASTEXITCODE
```

成功打印候选及用量，失败打印步骤和安全提示。不要贴Key、完整配置或HTTP头；只提供本课安全输出。不用历史成功日志代替你自己的运行证据。

## 6. 用户独立小修改

只完成main.py的describe_information_gap：从传入的card实例取information_gap，返回“信息缺口：”加字段内容。

这是对象属性练习，接着复习result的dict与parsed的实例差别。不硬编码原文缺口，不从raw.content取整段JSON，不改schema/提示词/验证脚本。函数的返回值是str，main负责print；如果只print不return会返回None，检查会发现。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\verify_cases.py --exercise
$LASTEXITCODE
```

当前18项基础通过、展示探针待完成，退出1；完成后预期18项基础+2项不同字段值展示通过、退出0。检查用人工固定数据/临时替换远程生成方法，只验证本地包装器/解析/流程，真实HTTP0，不当成DeepSeek成功。

## 7. 正常、非法与边界

| 情况 | 预期反馈/位置 |
| --- | --- |
| 默认预览 | 退出0，不读配置/请求 |
| 空白/2001字符材料、schema字段拼写错误 | 本地停止，调用0/退出2 |
| 缺配置 | 配置检查停止，调用0/退出2 |
| 真实请求超时/401/429 | 请求失败，退出1，安全提示/不自动重试 |
| 空正文、非法JSON、缺字段/错类型 | 响应/解析失败，退出1，不展示合格候选 |
| length截断 | 拒绝当完整卡片，不自动补请求 |
| 引用不在原文 | 普通业务拒绝，退出1 |
| 正常解析+引用存在 | 退出0、pending_manual_review，仍需核对事实 |
| 不可信原文命令 | human数据；角色检查不保证模型防注入 |

业务引用检查不由LangChain执行；引用存在也不证明支持每个摘要事实。本课只有一段引用，完整逐项定位/更全面内容评估在后续补齐，不能把Pydantic或模型自查当正确性保证。

## 8. 双重验收与下一步

项目：正常生成或明确失败，字段可读取、引用存在，失败不保存、不自动重试；默认离线。助手实测18项基础及一次真实生成通过，用户展示TODO待完成，整课未标通过。

学习：你独立展示实例字段，能指出真正请求位置，解释raw/parsed/parsing_error、JSON合法为何仍可能失败或事实错误，并提供安全运行/离线检查结果。根据你的证据收尾或补练；不因助手真实成功登记你已掌握。

下一小步再做更明确的内容核对/质量案例，不提前生成多人平台或持久化功能。

## 9. 官方核对与限制

2026-10-12核实：[DeepSeek JSON Output](https://api-docs.deepseek.com/guides/json_mode/)、[ChatDeepSeek集成](https://docs.langchain.com/oss/python/integrations/chat/deepseek)。官方JSON页面直接访问超时，取得了官方检索缓存内容；API Reference链接加载失败：[参考入口](https://reference.langchain.com/python/integrations/langchain_deepseek/ChatDeepSeek/)。没有声称完整在线API Reference核实。

本机langchain-deepseek1.1.1方法签名/源码支持json_mode和include_raw；langchain-openai1.6.7本机方法文档及实际包装器离线验证一致，本次真实调用也成功。官方集成教程仍有旧模型别名，不按旧名字修改配置；当前模型沿用你的配置。Pydantic2.14.0/其余依赖保持，未加包。

[任务与交接](../../docs/tasks/2.2-structured-card.md) · [实际运行](RUN_RESULTS.md) · [2.1字段](../02_01_card_schema/schema.py)
