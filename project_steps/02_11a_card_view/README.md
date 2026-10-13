# 2.11-A Vue学习卡原文对照

2026-10-13：用户要求完整代码，本课已提供可运行参考实现，替代此前骨架。功能实测见[STAGE2-001](../../docs/tasks/STAGE2-001-complete-reference.md)；用户能力仍待独立修改、解释和运行日志，不能由参考实现代替。

## 本次交付与原因

交付：安全文本视图。这是阶段2生成→核对→保存→重开的必要环节。完整项目入口和环境准备见[运行手册](../../docs/STAGE2_RUNBOOK.md)，课程顺序见[总表](../../docs/STAGE2_CURRICULUM.md)。

- 输入：card/material props。
- 处理：读取当前main.py导入的共享模块；配置/模型集中在learning_app/ai.py，业务事务集中在service.py。
- 输出：安全文本视图。默认main展示离线参考行为；数据库SQL预览不算真实数据库通过。

## 关键代码与语法

defineProps是组件输入契约；{{ }}文本绑定自动转义；不使用v-html显示原文。

先读[main.py](main.py)的中文说明，再跳到导入的实际函数。它们已完整实现，不再抛尚未实施的NotImplementedError。数据库课再读[迁移](../../migrations/versions/0001_materials_cards.py)，页面课再读[组件](../../web/src/CardReview.vue)、[页面](../../web/src/App.vue)和[请求](../../web/src/api.ts)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_11a_card_view\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_11a_card_view\main.py --exercise
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

独立给信息缺口新增一个可访问的提示图标，保留原字段内容。

请在当课分配时修改对应共享代码或创建独立练习文件；当前不代写这个迁移答案。验收需要你的修改、为什么这样改的中文解释、正常/非法/边界运行证据。失败先定位input/template/invoke/parse/database/review/view，再做最小修复。通过后记录能力证据，已有2.1/2.2通过练习不重做。
