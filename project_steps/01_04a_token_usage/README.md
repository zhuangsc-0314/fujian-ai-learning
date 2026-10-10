# 1.4-A：token、元数据与输出上限

交付：读懂已有用量，不再请求一次正常回答。1.2已经提供真实日志：材料78字符，输入147 token、输出91、总计238，结束stop，请求及响应处理0.98秒。历史日志未记录模型名/请求ID，显示未知；本课不从现在.env反推。

本次3个概念：

- **token**是模型处理文本的单位，一个token可能对应一个字、词的一部分或符号。不同模型切分规则不同，token不等于字符。输入还包括系统约束、学习目标、材料与消息格式，不只是那78个字符。
- **usage_metadata**是LangChain归一的用量字段（input_tokens/output_tokens/total_tokens）；**response_metadata**保存finish_reason等响应信息。`reply.content`才是回答正文。字段是否提供取决于适配器和供应商；缺失表示未知。
- **max_tokens**限制输出token数量；预算限制费用。输入也可能计费，单价、缓存等会影响金额，因此输出上限256不等于预算256元，也不保证每次输出256 token。

输入→处理→输出：历史用量/人工边界字典 → show_metadata按允许字段读取 → 已知数字或“未知”，不打印正文/原始响应，不核算费用。history是历史证据摘录；missing/partial/zero/length是明确标记的人工元数据样例，不是供应商实测。

最小例子：

```python
usage = {"input_tokens": 147}
print(usage.get("input_tokens"))   # 147
print(usage.get("output_tokens"))  # None：缺失，不是0
```

主代码的`dict[str, int] | None`表示字典或None；`value is None`专门判断缺失。`value or '未知'`会错误地把0当未知。`"未知" if value is None else str(value)`是条件表达式，返回可展示文本。字典`.get()`缺字段不会抛KeyError。

你的独立修改：只在main.py的TODO处补一行“合计token：”输出，读取`total_tokens`并调用已有show_count。保留未知和零；不相加或硬编码历史数，不改检查脚本。

从仓库根目录运行：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04a_token_usage\main.py history
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04a_token_usage\verify_cases.py
$LASTEXITCODE
```

通过条件：

| 案例 | 合计展示 |
| --- | --- |
| history：真实历史日志 | 238 |
| missing：无用量；partial：缺字段 | 未知，不能推为免费 |
| zero：明确记录为零的人工样例 | 0，不能当未知 |
| length：人工截断标记 | 未知；提示可能不完整，不自动重发 |
| 非法案例/多余参数 | 本地拒绝，退出2 |

骨架7项基础检查通过，但合计探针待完成，verify_cases预期退出1；完成后应全部通过、退出0。main.py展示成功退出0，不能据此判断独立练习通过。stop不证明回答事实正确；length提示可能截断，不能自动重新计费调用。

请在完成后提供实际输出，并解释：①为何78字符对应输入147 token？②usage_metadata和response_metadata分别告诉我们什么？③为什么max_tokens=256不是费用预算？

本课能力待你的修改/运行/解释证据。下一步再分配真实长短文用量比较、完整调用记录和当前价目核对；它们本轮未运行/未实施，没有新的API响应或费用结论。沿用的LangChain字段实现可回看1.2 main.py的show_response及USER_RUN_RESULTS，依赖版本不变。
