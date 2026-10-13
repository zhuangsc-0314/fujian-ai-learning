# 阶段2课程：从结构化学习卡到本机保存与页面

规划日期：2026-10-13。任务[PLAN-002](tasks/PLAN-002-stage2-curriculum.md)。用户要求完整课程规划，并明确要求同时创建带TODO的代码骨架。

**状态：课程设计与骨架已提供，后续功能未实现。** 已有2.1限定核心验收通过；2.2功能和独立展示通过，raw/parsed/error与本课事实边界独立解释、用户日志仍待补。规划不增加学习掌握证据，根笔记仍15个功能完成小节。

## 1. 本阶段交付目标

本机输入一份有来源/版本的材料和学习目标，生成结构化候选，逐项对照原文，明确未知信息与审核状态，保存到开发数据库，重开页面仍能读取同一卡片。

你应能独立解释并修改“输入→提示词→模型调用→解析→普通业务核对→保存→页面”，遇到错误先确定失败层，再做最小修复。LangChain集中处理提示词、模型和结构化结果；普通Python/数据库代码负责归属、事务、审核与查询。

阶段2有两个独立状态：

- **本机教学闭环**：显式本机demo上下文、公开或人工练习材料，完成生成/核对/保存/重开及业务归属查询测试。本阶段以这个里程碑验收。
- **完整产品验收**：真实身份、双账号源权限/跨用户隔离和完整F1质量集仍须取得真实证据。真实认证按原路线进入阶段3，不能因本机闭环通过就将“授权保存”或多人上线全部标完成。

当前不增加注册、分享、错题、RAG、Agent或部署，只做一个完整业务流程。生产库、删除旧资料和付费调用不由本规划自动授权。

## 2. 当前接续点

| 课程 | 已有交付 | 当前证据 |
| --- | --- | --- |
| 2.1 学习卡schema | 四字段LearningCard、人工候选、本地校验 | 用户字段修改/修复及限定核心解释通过，原练习不重做 |
| 2.2 结构化生成 | json_mode/include_raw、候选检查、实例展示 | 助手历史真实生成一次；本轮18+2项离线检查通过，用户展示通过；其余解释/用户日志待补 |

2.2继续使用原verify_cases.py --exercise，不恢复已完成TODO。下一小步先取得解释/用户日志，再进入2.3-A；用户若明确要求继续，则保留缺项并在2.3自然复习，不自动登记通过。

## 3. 全部课程与代码

阶段2细化为2.1—2.12，较大的2.3、2.8、2.9、2.11拆A/B。**共16个可分配小步：2个已有课程、14个未来骨架。** 每次只认领一个。

| 小步 | 课程/代码讲义 | 新概念（1—3项） | 用户独立练习位置 |
| --- | --- | --- | --- |
| 2.3-A | [逐项核对事实与人工审核状态](../project_steps/02_03a_content_review/README.md) | 结构校验与语义核对；审核状态 | `decide_review_status` |
| 2.3-B | [引用定位与逐项证据记录](../project_steps/02_03b_evidence_locations/README.md) | 字符位置；半开区间；一条事实对应证据 | `locate_quote` |
| 2.4 | [ChatPromptTemplate与参数贯通](../project_steps/02_04_prompt_template/README.md) | 消息模板；模板变量；提示词版本 | `prepare_prompt_values` |
| 2.5 | [最小LCEL组合与失败定位](../project_steps/02_05_runnable_sequence/README.md) | Runnable输入输出；竖线组合；调用边界 | `build_card_chain` |
| 2.6 | [材料来源、版本与归属](../project_steps/02_06_material_context/README.md) | 可空日期；不可变版本；业务归属 | `describe_publication_date` |
| 2.7 | [生成服务与明确的结果对象](../project_steps/02_07_generation_service/README.md) | 函数职责；依赖传入；结果与错误分类 | `classify_failure_stage` |
| 2.8-A | [本机PostgreSQL连接与故障定位](../project_steps/02_08a_postgres_connection/README.md) | 连接配置；开发/测试库；参数化SQL | `describe_database_failure` |
| 2.8-B | [数据表、约束与数据库迁移](../project_steps/02_08b_schema_migration/README.md) | 表/外键；ORM映射；迁移版本 | `require_owner` |
| 2.9-A | [保存候选与事务](../project_steps/02_09a_save_transaction/README.md) | Session生命周期；提交/回滚；保存与生成分开 | `save_candidate` |
| 2.9-B | [归属查询与审核快照绑定](../project_steps/02_09b_owned_read_review/README.md) | 带归属条件的查询；审核状态；版本冲突 | `get_owned_card` |
| 2.10 | [本机FastAPI入口与错误响应](../project_steps/02_10_local_api/README.md) | 请求/响应模型；路由；依赖提供 | `map_error_status` |
| 2.11-A | [Vue学习卡与原文对照组件](../project_steps/02_11a_card_view/README.md) | 组件props；响应式状态；模板绑定 | `CardReview.vue中的信息缺口区域` |
| 2.11-B | [页面请求、失败状态与保存后重开](../project_steps/02_11b_page_flow/README.md) | fetch与Promise；async/await；请求状态 | `api.ts中的fetchCard` |
| 2.12 | [阶段2综合验收与独立调试](../project_steps/02_12_stage_acceptance/README.md) | 端到端证据；失败分层；功能与能力分别验收 | `build_acceptance_report` |

各链接已给出前置、原因、输入/处理/输出、中文语法说明、正常/非法/边界案例、双重验收和命令。未来课程中的业务案例均为**预期，尚未实测**。

## 4. 四段里程碑

| 段落 | 课程 | 预期交付 | 推进证据 |
| --- | --- | --- | --- |
| 生成与核对 | 2.1—2.5 | 候选、人工核对、引用位置、模板、小链 | 能区分格式/事实、raw/parsed/error、字典/实例；请求次数与失败位置明确 |
| 业务上下文 | 2.6—2.7 | 来源/版本/归属、共享生成服务 | 未知日期保留未知，模型不填写owner；CLI/API复用服务，失败不假报成功 |
| 本机持久化 | 2.8-A—2.9-B | 开发库、迁移、保存/读取、审核版本绑定 | 重启可读、失败回滚、重复保存不生成；归属查询通过但身份仍为demo |
| 页面闭环 | 2.10—2.12 | 本机API、原文对照、保存后重开、报告 | 完整本机流程日志，独立修改/故障定位，真实认证/完整质量门槛缺项单列 |

不承诺固定天数。一次课超过3个新概念就继续拆分，不一次补完全部代码。已通过练习不重新设为前置考试。

## 5. 教学与代码增长方式

每课固定：交付目标 → 为什么需要 → 1—3个概念与输入输出 → 最小中文示例 → 正常/一个失败演示 → 用户独立TODO → 根据代码/解释/日志决定补练或下一课。

- 新main.py默认只显示说明，退出0代表说明运行；--exercise退出2表示尚未实施。
- TODO ASSISTANT用于开课时提供必要教学框架；TODO USER保留给用户。未开课不代做后续练习。
- NotImplementedError明确表示函数尚未实现，不能用空字典/固定成功字符串占位。
- 每课开工前按[任务模板](tasks/TEMPLATE.md)分配文件、负责人和验收，不把14课同时认领为进行中。
- 2.7再提取正式共享模块，届时记录兼容影响；CLI/HTTP只接收输入与展示，生产代码保持一个共享AI边界。
- Python复杂语法按当课需要逐项解释；Vue课才讲props、响应式状态和async/await。

对应目录职责、函数契约、数据和API约定见[代码蓝图](STAGE2_CODE_BLUEPRINT.md)。

## 6. 运行与依赖计划

现在可以从仓库根目录运行骨架说明：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py --exercise
$LASTEXITCODE
```

完整入口见[代码导航](../project_steps/STAGE2.md)。现在没有可启动的阶段2网站、数据库迁移或HTTP应用；Vue/TypeScript文件只是后续练习骨架。

| 时机 | 依赖/工具计划 | 变更规则 |
| --- | --- | --- |
| 现在至2.7 | Python3.12.15、uv0.12.24、现有LangChain/Pydantic | 保持声明和锁；模板/组合接口已有，具体行为开课时验证 |
| 2.8-A | PostgreSQL独立本机开发/测试库，驱动候选psycopg | 先核对本机条件/官方支持版本再选安装方式，不连接历史生产库 |
| 2.8-B | SQLAlchemy 2、Alembic | 核实API与Python兼容性，自动更新锁，迁移只作用于选定开发库 |
| 2.10 | FastAPI、ASGI服务器 | 先采用可理解的同步流程，明确超时/资源边界，不提前引入队列 |
| 2.11 | Vue 3、TypeScript、Vite与相容Node版本 | 前端独立声明与锁；本轮不安装、不声称构建通过 |

新增Python依赖通过scripts/uv-project.cmd锁定.venv-py312，在对应课检查解析、兼容及最小运行。具体新包版本实施时核实，不把最新文档版本当作本机版本。

## 7. 综合验收和证据等级

2.12准备10份固定材料/案例：有来源短文、缺日期、缺定义、重复引句、中文换行、接近输入上限、空材料、超长材料、夹带指令、引用或摘要冲突。每份记录来源/版本、预期缺口，不补造未来考试事实。

分别保存：

1. 离线：字段/解析、模板、引用定位、调用次数及失败流程，人工固定结果明确标注。
2. 开发库：迁移、保存/重开、回滚、唯一约束、归属条件、审核版本冲突，仅操作专用测试数据。
3. 页面：加载/空/成功/失败状态、保存后刷新、旧请求不能覆盖新候选。
4. 真实生成：沿用已有2.2历史证据；新模板/流程需要真实验证时明确材料、次数与成本范围。本规划不自动发10次请求，未运行标not_run，不用替身顶替。
5. 人工内容：逐项事实有证据、未知保留、日期适用；模型自查不能代替。

本机验收至少取得一条“真实生成或已有可追溯真实候选→人工核对→保存→重开”的证据链，注明是否使用历史候选。完整F1的10篇真实材料质量验收保留为独立门槛，未做足不能写F1全面通过。真实账号/跨用户隔离在阶段3补接，未通过不能开放给朋友。

能力证据至少包括一次独立字段/展示修改（可复用已有）、一次参数/链路修改、一次失败定位/最小修复，以及对模型内容、业务状态、数据库记录的区分。助手和用户实测分列，课程数量不等于掌握程度。

## 8. 官方资料与核实限制

2026-10-13查阅以下资料用于规划，不等同于新依赖兼容或功能实测：

- [LangChain结构化输出](https://docs.langchain.com/oss/python/langchain/models#structured-outputs)：保留模型级结构化路径。
- [ChatPromptTemplate.from_messages](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/from_messages)、[RunnableSequence](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)：模板与小组合；本机签名读取确认接口存在。最初下划线路径失败，后找到官方连字符路径；在线版本标签与本机不同，以锁版本实测为准。
- [SQLAlchemy Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)、[Alembic教程](https://alembic.sqlalchemy.org/en/latest/tutorial.html)、[PostgreSQL事务](https://www.postgresql.org/docs/18/tutorial-transactions.html)：会话/迁移/事务的课程依据。
- [FastAPI依赖提供](https://fastapi.tiangolo.com/tutorial/dependencies/)、[Vue表单绑定](https://vuejs.org/guide/essentials/forms.html)：上下文和输入绑定的课程依据，当前未安装/运行相应环境。

下一次从2.2剩余证据接续，再进入2.3-A。顺序可按用户需求调整，状态始终按实际证据更新。
