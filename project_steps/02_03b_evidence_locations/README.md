# 2.3-B 引用定位与逐项证据记录

## 当前小步：2.3-B1位置与切片

任务[2.3-B1](../../docs/tasks/2.3-b1-quote-slices.md)。完整参考函数保留；本次先用纯中文材料练一次独立调用，查找循环、:=、emoji和重叠情况后续逐步学习。不教学数据库或网页。

### 交付与业务原因

2.3-A记录人工核对结论；本步找出引句在原文哪里，让人可以回到具体位置核对。输入material原文、quote逐字引句→普通Python定位→所有(start,end)位置对。位置只能证明引句出现过，不能证明它支持摘要事实，也不自动改变审核状态。

阅读[domain.py](../../learning_app/domain.py)中locate_quote的函数定义与返回类型，先关注接口，不要求本次看懂全部内部实现。

### 本次三个概念

1. 字符位置从0开始：原文第一个字符是位置0，第二个是位置1。
2. 半开区间[start:end]：包含start位置，不包含end位置。end是引句后面的第一个位置，end-start是这一段的字符数。
3. list[tuple[int,int]]：外层列表包含多次出现的位置；每项是两个整数的元组(start,end)。例如[(3,9)]有一处，[(3,9),(9,15)]有两处。这是结果结构示例，不是用户调用的答案。

正常示例：

```python
material = "正文：政治和法律。"
positions = locate_quote(material, "政治和法律。")
print(positions)       # [(3, 9)]
print(material[3:9])   # 政治和法律。
```

第3位置是“政”，第8位置是“。”，第9是字符串末尾之外的边界；切片取3—8共6个字符。切片允许end等于字符串长度。这里的冒号是切片语法，不是函数参数的类型提示。

练习入口里的for start,end in positions，表示从列表每项的两个整数分别取出start和end，再用material[start:end]还原对应原文；不要求你修改这个循环。函数返回位置列表，不是引句正文、布尔判断或审核状态。

### 独立修改、运行与验收

只完成[practice.py](practice.py)的locate_my_quote，把已给定MY_MATERIAL与MY_QUOTE传给locate_quote并返回结果。可按你已学的命名参数方式调用，不直接返回固定位置列表、不改材料/共享函数/检查部分。

| 案例 | 预期 |
| --- | --- |
| 正常单次引句（参考） | 返回一对位置，切片还原原文引句 |
| 非法空白引句（参考） | 明确ValueError，不把空白当合法证据 |
| 同一句出现两次（用户） | 返回两对位置，两段切片都等于引句 |

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03b_evidence_locations\practice.py
$LASTEXITCODE
```

未完成TODO时正常/非法观察运行，但用户边界仍退出1；这不是全课通过。完成后预期两处位置/两段相同切片、退出0。功能结果与能力分列：还需核对用户确实调用函数、解释为何end不包含/为什么不能只保留第一处，以及个人运行日志。

本课人工字符串不算供应商回答，无.env/API/数据库或新增依赖。2.3-A已通过调用不重做，解释经纠正与个人日志缺项保留。

---

下文是此前完整参考课程说明；emoji/重叠迁移练习留到本课后续小步，当前只完成B1。

2026-10-13：用户要求完整代码，本课已提供可运行参考实现，替代此前骨架。功能实测见[STAGE2-001](../../docs/tasks/STAGE2-001-complete-reference.md)；用户能力仍待独立修改、解释和运行日志，不能由参考实现代替。

## 本次交付与原因

交付：所有半开区间位置。这是阶段2生成→核对→保存→重开的必要环节。完整项目入口和环境准备见[运行手册](../../docs/STAGE2_RUNBOOK.md)，课程顺序见[总表](../../docs/STAGE2_CURRICULUM.md)。

- 输入：原文和逐字引句。
- 处理：读取当前main.py导入的共享模块；配置/模型集中在learning_app/ai.py，业务事务集中在service.py。
- 输出：所有半开区间位置。默认main展示离线参考行为；数据库SQL预览不算真实数据库通过。

## 关键代码与语法

find返回-1表示没找到；[start:end]包含start、不包含end；while逐次找下一处。

先读[main.py](main.py)的中文说明，再跳到导入的实际函数。它们已完整实现，不再抛尚未实施的NotImplementedError。数据库课再读[迁移](../../migrations/versions/0001_materials_cards.py)，页面课再读[组件](../../web/src/CardReview.vue)、[页面](../../web/src/App.vue)和[请求](../../web/src/api.ts)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03b_evidence_locations\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03b_evidence_locations\main.py --exercise
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

独立增加含emoji及重叠引句的案例，口述每个切片。

请在当课分配时修改对应共享代码或创建独立练习文件；当前不代写这个迁移答案。验收需要你的修改、为什么这样改的中文解释、正常/非法/边界运行证据。失败先定位input/template/invoke/parse/database/review/view，再做最小修复。通过后记录能力证据，已有2.1/2.2通过练习不重做。
