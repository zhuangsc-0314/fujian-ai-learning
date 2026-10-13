# 2.3-A 逐项核对事实与人工审核状态

## 当前教学：一个人工审核状态练习

2026-10-13最新评审：用户已独立完成review_unknown_time，调用现有业务函数并return结果；助手三案例accepted/rejected/pending_manual_review实际正确、退出0，无模型/数据库请求。独立修改通过，解释和用户个人日志仍待验证；以下练习要求保留用于复习，不再要求重写已通过函数。

任务[2.3-A](../../docs/tasks/2.3-a-review-status.md)。用户要求按既定流程学习，功能效果以后再构思；本课只学习候选后的人工审核状态，不教学数据库/页面。完整参考逻辑保留，独立练习在[practice.py](practice.py)，不阻挡完整应用运行。

### 做什么、为什么、输入输出

交付：根据人的两项核对结论返回审核状态。2.2已经取得结构化候选，但程序检查无法证明全部事实正确；人逐项核对原文后，普通Python业务函数汇总结论。函数不会读原文自动判断，也不调用模型。accepted只是记录人工结论。

输入两项人工结论→冲突优先/满足通过条件/其余未知→返回pending_manual_review、accepted或rejected。核心函数在[domain.py](../../learning_app/domain.py)的decide_review_status。

| 输入 | True | False | None |
| --- | --- | --- | --- |
| all_claims_supported | 所有判断都找到支持依据 | 至少一项没有依据或被反驳 | 尚未核对完 |
| has_time_conflict | 已发现时间适用冲突 | 已核实没有时间冲突 | 尚未核实时间适用性 |

None表示未知，不能当作False。未知发布日期也不自动等于“有冲突”；这里输入的是人工时间适用结论。

### 本课三个概念与关键语法

1. 审核状态：pending_manual_review待核对；accepted人工通过；rejected驳回。保存状态是另一维度，本课暂不操作保存。
2. bool | None：参数允许布尔结论或未知值；类型提示说明约定，本身不自动校验传入类型。is True/is False按明确结论判断，避免把未知误当无冲突。
3. 命名参数：函数定义中的单独星号*要求调用时写参数名，避免把两项布尔结论传反。星号在这里不表示乘法，也不是本课要求学习的可变参数。

正常调用示例：

```python
status = decide_review_status(
    all_claims_supported=True,
    has_time_conflict=False,
)
print(status)  # accepted
```

右边函数先运行，再把返回的状态字符串赋给status。业务规则先检查“事实无依据或时间冲突”返回rejected；再检查“事实都有依据且已核实无时间冲突”返回accepted；其余返回待核对。or表示任一条件成立，and表示两项都成立；return结束本次函数调用。

### 独立修改与三类案例

你只完成practice.py的review_unknown_time函数：用两项命名参数调用业务函数，表达“事实已经有依据，但还没有核实时间适用性”，返回调用结果。不要改domain.py、正常/不合格案例或直接硬编码状态。不提供这个调用的答案。

| 案例 | 人工输入情况 | 预期 |
| --- | --- | --- |
| 正常（参考） | 全部有依据，已核实无时间冲突 | accepted |
| 非法/不合格内容（参考） | 发现至少一项事实无依据 | rejected |
| 未核实边界（用户） | 事实已核实，时间适用性未核实 | pending_manual_review |

这里不合格是业务内容不合格，不是Python参数类型错误。你的代码、正常/不合格/边界实际日志和中文解释一起验收：为什么未核实不能当无冲突？为什么只满足事实有依据还不够通过？失败先定位调用参数或分支，不更改共享规则凑结果。

```powershell
# 完整参考演示；退出0不等于用户掌握
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py
# 用户独立练习；TODO未完成时退出1是已知状态
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\practice.py
$LASTEXITCODE
```

修改后预期三行状态正确、退出0；助手仍需核对调用代码与解释。两入口均离线、不读.env、不调用数据库/模型。2.2缺少的独立证据保留，按用户明确继续指令进入本课，不标2.2全面掌握。

---

以下为此前完整参考交付说明，后续数据库/页面链接是导航，不是本课教学内容。

2026-10-13：用户要求完整代码，本课已提供可运行参考实现，替代此前骨架。功能实测见[STAGE2-001](../../docs/tasks/STAGE2-001-complete-reference.md)；用户能力仍待独立修改、解释和运行日志，不能由参考实现代替。

## 本次交付与原因

交付：审核状态。这是阶段2生成→核对→保存→重开的必要环节。完整项目入口和环境准备见[运行手册](../../docs/STAGE2_RUNBOOK.md)，课程顺序见[总表](../../docs/STAGE2_CURRICULUM.md)。

- 输入：人工结论/时间冲突。
- 处理：读取当前main.py导入的共享模块；配置/模型集中在learning_app/ai.py，业务事务集中在service.py。
- 输出：审核状态。默认main展示离线参考行为；数据库SQL预览不算真实数据库通过。

## 关键代码与语法

关键字参数*使调用时明确写参数名；bool | None把未知和否区分开。

先读[main.py](main.py)的中文说明，再跳到导入的实际函数。它们已完整实现，不再抛尚未实施的NotImplementedError。数据库课再读[迁移](../../migrations/versions/0001_materials_cards.py)，页面课再读[组件](../../web/src/CardReview.vue)、[页面](../../web/src/App.vue)和[请求](../../web/src/api.ts)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py --exercise
```

--exercise现在运行完整参考演示，退出0仅说明演示执行成功，不计入用户独立验收。所有默认入口模型请求0、未读取.env。真实数据库验证使用scripts/stage2-dev.ps1 test；网页构建和启动见运行手册。

## 三类案例与通过条件

| 类型 | 输入/动作 | 应有结果 |
| --- | --- | --- |
| 正常 | 合法材料和明确参数、同归属及当前版本 | 返回对应对象/视图；保存后可读取 |
| 非法 | 空字段、错误引句、跨归属、非法HTTP字段 | 在对应步骤明确拒绝；不假报成功、不自动调用模型 |
| 边界 | 未知日期、重复引句、重复保存、旧审核版本或未运行质量集 | 未知保持未知；保留全部位置；保存幂等；版本冲突；not_run分列 |

具体已执行案例在tests/test_stage2_offline.py与tests/test_stage2_postgres_api.py。助手测试结果仅用于功能验收。后续每次教学只选本课一个小修改，先解释输入/处理/输出，再看实际日志。

## 用户独立迁移练习

新增一个时间适用未知的案例，解释为什么不能accepted。

请在当课分配时修改对应共享代码或创建独立练习文件；当前不代写这个迁移答案。验收需要你的修改、为什么这样改的中文解释、正常/非法/边界运行证据。失败先定位input/template/invoke/parse/database/review/view，再做最小修复。通过后记录能力证据，已有2.1/2.2通过练习不重做。
