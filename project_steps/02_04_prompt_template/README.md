# 2.4：ChatPromptTemplate与参数贯通

状态：**规划与TODO骨架，未实现、未验收、未分配为当前课**。当前学习仍为2.2，历史已通过练习不重做。

## 本课交付与原因

预期交付：material/learning_goal/schema_json → 模板填值 → system/human消息预览。

为什么现在学：材料、目标、schema需要稳定传入消息，便于复用与定位漏传。

前置：2.3；沿用现有langchain-core，不安装完整langchain。

新概念（最多3项）：消息模板；模板变量；提示词版本。

## 代码与独立练习

[main.py](main.py)含中文函数契约，未实现函数抛NotImplementedError。TODO USER由用户独立实现，TODO ASSISTANT由授课智能体在正式开课时补教学框架；不能一口气代做后续练习。

独立位置：`prepare_prompt_values`。

练习目标：独立贯通learning_goal并拒绝空白；材料只进入human变量，不修改system约束。

通用Python语法：参数后的冒号说明预期类型，箭头说明返回类型；类型提示本身不自动校验。签名中的单独星号表示后续参数必须按名字传入；`T | None`表示T类型或未知值None；`list[tuple[int, int]]`表示由两个整数位置组成的列表。涉及的语法只在本课用到时逐项解释，不要求提前掌握全部。

具体模块职责与后续正式代码落点见[代码蓝图](../../docs/STAGE2_CODE_BLUEPRINT.md)。

## 运行方式

现在可从仓库根目录运行说明预览：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_04_prompt_template\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_04_prompt_template\main.py --exercise
$LASTEXITCODE
```

预期：说明预览退出0；--exercise明确“尚未实施”并退出2。它们只验证说明入口能运行，不能作为本课功能通过。骨架没有--live，不读取.env、不调用模型/数据库、不启动Web服务。未来依赖、测试与实际运行命令在开课时补齐并记录实测。

## 预期案例与双重验收

| 案例 | 预期结果（尚未实测） |
| --- | --- |
| 正常 | 更换目标后human消息同步变化。 |
| 非法/失败 | 空目标或缺模板变量在请求前明确失败。 |
| 边界/不可信 | 原文含花括号或“忽略规则”时仍作为变量值；不对填入的文本再次模板化。 |

功能通过条件：以上业务案例完成实现并取得实际输出，符合输入/输出契约；说明预览不算通过。

能力通过条件：独立完成指定修改，解释输入→处理→输出，并定位本课至少一个实际或明确注入的失败步骤；用户日志与助手验证分列。未取得证据标待验证，用户明确要求收尾时保留缺项，不自动登记掌握。

开课时先用[任务模板](../../docs/tasks/TEMPLATE.md)分配唯一小任务及可编辑文件；完成后更新任务、状态和笔记，按PR交接。

[阶段2总课程](../../docs/STAGE2_CURRICULUM.md) · [骨架导航](../STAGE2.md)
