# 阶段2完整课程与参考代码

2026-10-13：用户明确要求完整代码，已用[STAGE2-001](tasks/STAGE2-001-complete-reference.md)替代PLAN-002的骨架范围。16个教学小步均有代码：2.1/2.2沿用已通过实现，2.3—2.12提供完整参考模块、课程入口和中文讲义。根笔记29个功能/参考交付小节；新增14节全部是助手功能交付，不是用户掌握。

## 本阶段目标与实际交付

材料输入→模板/最小LCEL→真实结构化候选或明确历史回放→逐项人工核对→PostgreSQL保存/读取→本机API→Vue页面重开。实现集中在共享learning_app和web，各课导入同一套函数，不维护多套业务服务。

本机完整闭环已经通过历史候选回放验证，模型请求0。新模板的真实生成接口已实现但本轮未付费实测；不能把回放算新生成。真实认证、完整F1十篇真实材料质量及多人上线仍未验收；不跳到RAG/Agent。

## 课程顺序与代码

| 课程 | 讲义/代码入口 | 共享实现 |
| --- | --- | --- |
| 2.1 | [学习卡schema](../project_steps/02_01_card_schema/README.md) | 原用户四字段代码，限定核心能力通过 |
| 2.2 | [结构化生成/实例展示](../project_steps/02_02_structured_card/README.md) | 原逻辑保留，展示通过；独立解释/用户日志缺项保留 |
| 2.3-A | [逐项核对事实与人工审核状态](../project_steps/02_03a_content_review/README.md) | learning_app.domain |
| 2.3-B | [引用定位与逐项证据记录](../project_steps/02_03b_evidence_locations/README.md) | learning_app.domain |
| 2.4 | [ChatPromptTemplate与参数贯通](../project_steps/02_04_prompt_template/README.md) | learning_app.ai |
| 2.5 | [最小LCEL组合与失败定位](../project_steps/02_05_runnable_sequence/README.md) | learning_app.ai |
| 2.6 | [材料来源、版本与归属](../project_steps/02_06_material_context/README.md) | learning_app.domain |
| 2.7 | [生成服务与明确结果](../project_steps/02_07_generation_service/README.md) | learning_app.ai |
| 2.8-A | [本机PostgreSQL连接](../project_steps/02_08a_postgres_connection/README.md) | learning_app.storage |
| 2.8-B | [数据表约束与迁移](../project_steps/02_08b_schema_migration/README.md) | learning_app.storage |
| 2.9-A | [保存候选与事务](../project_steps/02_09a_save_transaction/README.md) | learning_app.service |
| 2.9-B | [归属查询与审核版本](../project_steps/02_09b_owned_read_review/README.md) | learning_app.service |
| 2.10 | [本机FastAPI与错误响应](../project_steps/02_10_local_api/README.md) | learning_app.api |
| 2.11-A | [Vue学习卡原文对照](../project_steps/02_11a_card_view/README.md) | web/src |
| 2.11-B | [页面请求与保存后重开](../project_steps/02_11b_page_flow/README.md) | web/src |
| 2.12 | [综合验收与独立调试](../project_steps/02_12_stage_acceptance/README.md) | learning_app.domain |

## 教学如何继续

提供完整参考代码是本轮交付范围变更，学习仍一次推进一个可验证小任务、1—3个概念。各课README含原因、输入/处理/输出、关键语法、运行命令、正常/非法/边界及独立迁移练习。参考代码不再以TODO阻挡运行；独立练习与参考实现分开，未经用户修改/解释/日志不记能力。

生成与核对：2.3-A/B讲结构与事实、引用位置；2.4/2.5讲模板变量和Runnable组合。业务上下文：2.6/2.7讲来源、版本、归属和服务结果。数据库：2.8-A/B与2.9-A/B讲连接、迁移、事务、幂等和版本冲突。页面：2.10/2.11-A/B接HTTP/Vue，2.12按证据来源验收。

下一教学小步仍从2.2缺少的独立解释/用户运行证据自然接续，再进入2.3-A；不重做已通过describe_information_gap或字段修改。助手完整实现14课不意味着用户学习已推进14课。

## 运行与验收

详细环境、数据库、网页及真实生成命令见[运行手册](STAGE2_RUNBOOK.md)。默认main/preview离线；--exercise运行参考演示，不作为用户验收。真实PG在独立本机集群实测；网页已构建并进行浏览器保存/审核/刷新联调。

测试分层：32项离线函数/模板/失败边界、10个固定离线材料边界、6项真实PG/HTTP检查，共48项通过。固定10例包括历史摘录、缺日期、缺定义、重复引句、中文/emoji、上限、空材料、超长、夹带指令和摘要冲突；人工案例显式标注，不替代十篇真实模型质量集。

功能通过与用户能力分别记录。模型超时执行状态未知，不自动重试；保存失败不invoke；待审核草稿可保存；人工审核绑定材料版本/内容指纹/预期审核版本。已有历史模型470/140/610token仍仅属于2026-10-12实测，不记成本轮新请求。

正式Python3.12.15/uv0.12.24/.venv-py312和原五个精确依赖版本不变；新增依赖按官方资料核实并锁定，兼容/构建实际结果见任务。Windows便携PostgreSQL18.6、本机Node24.19/pnpm11.25；Linux未验证。
