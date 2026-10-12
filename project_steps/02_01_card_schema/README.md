# 2.1：学习卡字段与Pydantic校验

本课先完成学习卡的结构基础，不调用模型、不读.env、不保存数据库。候选是明确标记的人工练习数据，不是模拟AI回答。原文沿用2023年公开历史考试说明，不能当作未来考试安排或当前热点。

2026-10-12最新评审：用户已独立新增information_gap和输入，修复字段拼写/非空约束；助手正常入口与20项基础/5项字段练习全部通过、退出0，真实请求0。功能/独立修改通过，核心概念解释与用户运行日志待验证。下方TODO和失败预期保留为原练习说明，当前代码已完成，不要求重做；实际结果见任务最新评审。

## 1. 本次交付

定义最小学习卡，输入一个dict，得到可读属性的候选对象或明确错误。先学会检查“装结果的容器”，下一小步再让真实LangChain调用填这个容器。这样每次只引入3个核心概念，先区分字段错误与内容错误。

| 字段 | 类型/规则 | 含义 |
| --- | --- | --- |
| summary | 非空str，最多300字符 | 原文能够支持的摘要 |
| keywords | list[str]，1—5项，业务检查拒绝空白项 | 学习关键词 |
| evidence_quote | 非空str，最多400字符 | 原文中的连续引用 |
| information_gap | 用户独立新增，必填非空str，最多200字符 | 原文不能回答的一个信息缺口 |

引用和摘要分开放。来源/日期/用户归属由业务层提供，不允许模型补造；本课只有占位归属和版本，尚未做账号或持久化。

## 2. 为什么现在学

前面的reply.content是自由文本。后续页面需要稳定地取得摘要、关键词、引用，不能依赖模型每次写相同标题。Pydantic用一份字段规则检查数据，之后这份规则也能用于结构化生成。普通业务的原文匹配、权限和保存仍有独立职责。

## 3. 必要概念与关键Python语法

先看schema.py的三个字段，再看main.py的validate_card，不用先掌握整个检查脚本。

```python
class LearningCard(BaseModel):
    summary: str = Field(min_length=1, max_length=300)
```

- **类与实例（class / instance）**：类是对象的规则；LearningCard是类，成功校验得到的card是一个具体实例。括号里的BaseModel表示继承Pydantic的校验/导出能力。这里的数据model不是大语言模型。
- **字段类型和约束（type annotation / Field）**：`summary: str`说明字段类型；Field限制长度。Field没有默认值时字段必填。`list[str]`表示列表中的每项也须是字符串；列表的min/max_length检查项数，字符串检查字符数。
- **实际校验（model_validate / ValidationError）**：普通Python类型提示不自动检查输入；LearningCard.model_validate(candidate)才按规则执行检查，失败抛ValidationError。ConfigDict是本类的配置，严格类型/拒绝额外字段/去首尾空白不需自己写循环处理每个字段。

本课配置为strict=True、extra="forbid"、str_strip_whitespace=True：summary=123不会自动变成字符串；未知键被拒绝；空白字符串去空白后不满足最小长度。关键词单项为空白由普通业务函数进一步拒绝。

```python
card = LearningCard.model_validate(candidate)
print(card.summary)          # 对象属性
print(card.model_dump())     # 导出为普通dict，不是保存数据库
```

candidate["summary"]是字典取值；card.summary是实例属性。json.dumps把dict转为展示用JSON字符串，和json.load解析文件方向不同。`model_validate`是类提供的方法，本课不要求学习它内部的类方法实现。

## 4. 数据流与模块关系

```text
人工候选dict + 公开原文
→ schema.py：类型/长度/必填/额外字段校验
→ main.py：关键词非空、引用出现在原文
→ LearningCard实例
→ model_dump
→ 外层占位owner/version + pending_manual_review
→ JSON展示（无保存）
```

main.py的ValidationError分支先于ValueError，因为前者是后者的子类。校验失败时，后面的card赋值/正常展示不会继续；finally仍显示本课请求0。错误只打印字段位置和类别，不回显候选原始值。loc是字段路径，type是错误类别，例如missing/string_type。

## 5. 最小运行

在项目根目录运行，全部离线：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\main.py --case missing_summary
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\main.py --case wrong_type
$LASTEXITCODE
```

正常候选预期退出0，显示摘要、关键词和引用；缺summary预期显示字段missing，整数summary显示string_type，均退出2。这不是生成流程，0只表示结构和本课引用检查通过。

## 6. 格式与内容分别检查

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\main.py --case unsupported_claim
```

这个人工错误候选把摘要写成“题型全部为主观题”，引用仍是原文“题型全部为客观题”。字段类型正确、引用也存在，所以程序结构检查可退出0；它会明确提示内容不能通过，并保持pending_manual_review。**Pydantic不判断摘要是不是被引用支持。** 引用存在检查也不证明引用与结论一致，人工核对仍必需，后续再补内容质量评估。

untrusted_text案例将命令式文字作为字符串展示，不执行。当前没有AI处理，不能由这个案例声称模型防注入成功。

## 7. 用户独立小修改

只完成同一个小任务的两个TODO：

1. schema.py新增必填information_gap：字符串，去首尾空白后至少1字符、最多200字符。
2. main.py的正常人工候选补同名键，用自己的话说明原文缺少什么，例如客观题具体题型没有说明。

参考已有字段的类型和Field写法；不修改原字段、默认人工事实或verify_cases.py。只加字段不补输入会在model_validate报缺字段，不是Pydantic坏了。助手保留TODO，不代写答案。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\verify_cases.py --exercise
$LASTEXITCODE
```

当前预期20项基础通过，独立字段待完成，退出1。完成后预期20项基础及5项独立字段检查通过、退出0。提供你的修改和安全输出，再判断学习验收。

## 8. 正常、非法与边界案例

| 案例 | 预期 |
| --- | --- |
| 正常人工候选 | 退出0，仍待人工核对 |
| 缺字段/123/空白摘要/301字符 | ValidationError，退出2 |
| 300字符摘要 | 结构接受，不代表这些文字有据 |
| 空关键词列表/超过5项 | 字段校验拒绝；空白单项由业务检查拒绝 |
| 引用不在原文 | 业务检查失败，退出2 |
| 候选自填owner_user_id | 额外字段拒绝，不能据此宣称多人授权实现 |
| 引用存在但结论相反 | 结构可通过，人工内容不能通过 |
| 命令式文字 | 只作为数据，不执行；不算模型安全测试 |

## 9. 双重验收与下一步

项目验收：字段/错误分类准确，引用缺失拒绝，候选带外层占位归属与版本且始终待人工核对，本课真实请求0。业务保存、网页、模型生成和阶段2完整闭环尚未实现。

学习验收：你独立新增字段和输入；能说明类与实例、类型提示为什么不等于实际校验；能定位缺字段发生在model_validate；能解释Pydantic通过为什么不等于内容正确。助手运行不是你的运行证据；按你的修改/解释/运行结果决定补练或下一小步。

后续再核实真实供应商的结构化输出接口并调用一次，不维护模拟生成服务。首次材料保存/页面将在后续小任务实现。

## 10. 官方核对与环境

2026-10-12核实：[Models](https://docs.pydantic.dev/latest/concepts/models/)、[Field API](https://docs.pydantic.dev/latest/api/fields/)、[Strict Mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)、[Error Handling](https://docs.pydantic.dev/latest/errors/errors/)。官方最新页面会更新；本课接口另在已安装2.14.0读取签名并实际运行验证，没有混用v1的parse_obj/dict接口。

正式环境Python3.12.15、Pydantic2.14.0；本课把已有Pydantic从间接使用改为显式直接依赖，安装版本未升级，锁由uv自动生成。新电脑拉取后用scripts/uv-project.cmd sync --locked同步正式环境。

[任务与实际结果](../../docs/tasks/2.1-card-schema.md) · [公开历史材料来源](../01_01_first_sdk_call/SOURCE.md)
