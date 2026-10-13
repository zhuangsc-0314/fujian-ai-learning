# PLAN-002：阶段2课程与TODO代码骨架

## 分配

- 日期：2026-10-13；负责人/协调者：当前主智能体，无并行智能体。
- 用户本轮要求先规划整个阶段2课程与相关代码，并明确选择“同时创建带TODO的代码骨架”。仅规划及骨架，不代做未来练习。
- 基线：6ab02ab77504d4ed3e260e6261ebd35dbc07806b；开始时工作区干净，分支codex/2.2-instance-display已通过草稿PR #22交接。任务分支codex/plan-002-stage2-curriculum，PR基于codex/2.2-instance-display。
- 允许修改：本记录、docs/STAGE2_CURRICULUM.md、docs/STAGE2_CODE_BLUEPRINT.md、project_steps/STAGE2.md、project_steps/stage2_scaffold.py、规划中新建的02_03a至02_12课程目录、README.md、docs/PROJECT_STATUS.md、docs/DECISIONS.md、docs/AI_LEARNING_PLATFORM_DESIGN.md、学习笔记.md的规划导航；忽略.local可存生成/校验辅助与PR正文。
- 已有2.1/2.2代码、用户练习、LEARNING_PROGRESS、依赖/锁文件/.env保持原样。学习笔记只补规划入口，完成条目仍15，未获得新的用户能力证据。
- 目标：每课1—3个概念，提供前置、原因、输入/处理/输出、关键接口、中文语法解释、独立TODO、正常/非法/边界案例、功能与能力验收、运行方式；区分本机闭环与真实认证/多人上线。
- 依赖：正式路线/D-025/2.2验收；Python3.12.15、uv0.12.24及现有锁文件。后续数据库/Web依赖只列引入时机，实施前再核实/安装/锁定，不声称现环境具备。

## 双重验收

- 规划交付：课程及代码职责覆盖生成、核对、归属/材料版本、服务、数据库、API、页面与综合验收；全部未来目录明确骨架，业务函数主动抛NotImplementedError，不返回虚构成功；默认入口只展示说明，练习入口明确未实现。
- 学习状态：只有课程规划交付，不增加已掌握概念或已完成功能；2.2解释/用户日志仍待补，不为规划重复已通过练习。
- 骨架检查：Python语法与导入/说明入口通过；未完成函数不报告通过，未实现课程请求--exercise非零；禁止网络/.env哨兵下检查本地入口；本地文档链接与git diff --check通过。
- 不安装数据库/Node/新包，不迁移数据、不启动HTTP服务、不调用模型、不合并main或部署。实际结果待写入下节。

## 实际结果与交接

- 已提供docs/STAGE2_CURRICULUM.md、docs/STAGE2_CODE_BLUEPRINT.md和project_steps/STAGE2.md。阶段2细化为16个小步：保留2个已有课程，新建14个未来课程目录（各main.py/README.md），另有Vue组件和TypeScript请求骨架；20个未来业务函数明确抛NotImplementedError。
- project_steps/stage2_scaffold.py为可运行的说明工具，默认只预览课程；--exercise明确未实施并退出2；不提供--live。未来业务未实现，没有将骨架计为功能完成或用户能力。
- 课程覆盖事实/引用核对、消息模板、最小LCEL、材料上下文、共享服务、PG连接/迁移/事务/归属、HTTP、页面及综合验收。逐课已给出目标、前置、概念、中文语法提示、独立TODO、三类案例和双验收。
- 记录D-026并补正式设计：原“阶段2授权保存”与“阶段3才接真实认证”的范围歧义已显式区分；本机demo/业务归属测试不代表真实权限。待核对草稿、服务端候选快照、审核版本绑定、同步教学API与后续生产异步方案已明确。没有降低完整F1/多人上线验收要求。
- 官方模型、模板/组合、SQLAlchemy、PG、Alembic、FastAPI与Vue资料用于规划；最初LangChain Reference下划线路径失败，找到官方连字符路径。现有环境读取ChatPromptTemplate.from_messages和RunnableSequence.invoke签名成功；不当作后续业务实现/新依赖兼容证明。
- 实际运行：`.venv-py312/Scripts/python.exe -X utf8 .local/verify_stage2_scaffold.py`退出0。15个Python文件AST/99字符行宽通过；14个说明入口退出0、14个--exercise退出2、14个--live拒绝/退出2；20个业务TODO函数均抛NotImplementedError。运行中网络/DNS/读取.env哨兵未触发，无模型请求、数据库或HTTP服务启动。
- 文档检查：23份Markdown的273个本地链接存在；已完成功能笔记仍15节。首次暂存检查发现34个新文件末尾多余空行，已限定本任务文件移除且Python AST保持一致，git diff --cached --check再次实际通过/退出0。Git差异确认既有2.1/2.2、pyproject.toml、uv.lock、LEARNING_PROGRESS未变。根笔记只加规划导航，本任务没有新用户能力证据。
- Vue/TypeScript未构建，PostgreSQL/SQLAlchemy/Alembic/FastAPI环境未安装或运行；真实生成、新材料质量、真实认证/跨用户隔离未新增验证。临时校验辅助在忽略.local中，不作为后续课程正式功能测试。
- 本次代码/文档按分配范围精确提交并推送，草稿PR基于codex/2.2-instance-display；最终SHA/PR以Git回执核对。不合并main。
- 下一步仍为2.2剩余解释/用户日志，再进入2.3-A。未来每课单独分配，不同时启动14课；用户要求调整时保留未验证证据，不把规划误登记为掌握。
