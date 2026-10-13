# STAGE2-001：阶段2完整参考实现

- 分配：2026-10-13，用户明确要求“应该要完整的”，替代PLAN-002的骨架交付范围。
- 唯一负责人/协调者：当前主智能体；无其他智能体参与。
- 基线：20aea1ecda3d750475f2a7f6808008bb7493bb88；工作区干净。
- 分支：codex/stage2-001-complete-reference；PR基于codex/plan-002-stage2-curriculum。
- 目标：补齐2.3—2.12的完整参考代码和本机生成/核对/保存/读取/API/页面闭环；不修改2.1/2.2用户已通过逻辑。
- 文件范围：learning_app/、migrations/、alembic.ini、web/、tests/、scripts/阶段2辅助脚本、14个未来课程入口/讲义、project_steps/STAGE2.md及说明工具、pyproject.toml/uv.lock、.gitignore、README/AGENTS、阶段2设计/状态/交接/笔记、本机公开样例截图和本任务记录。
- 依赖：沿用Python3.12.15/uv0.12.24和既有精确版本；新Web/数据库依赖核对官方文档，自动解析锁文件。
- 接口确认：采用STAGE2_CODE_BLUEPRINT的同步API、服务端候选快照、owner限定查询和人工审核版本冲突；正式模块可合并细小文件，避免重复实现。
- 功能验收：纯函数/模板/结构化失败边界、PostgreSQL迁移/事务/重复保存/归属/审核冲突、HTTP和Vue构建/联调。实际与未运行分别记录，不以替身冒充真实模型或PG。
- 能力验收：仅交付参考代码，不自动认定用户已掌握；新增独立迁移练习，与可运行参考实现分开。2.2既有能力缺项保留。
- 边界：不调用付费模型、不合并main、不部署、不连接生产数据、不引入RAG/Agent/真实认证。历史候选回放显式标识来源。

## 实测与交接

完整参考实现与功能验收通过；用户能力不新增登记。根笔记由本负责人维护，新增14个助手参考交付小节，总29节。

### 实现与范围

- 七个learning_app模块实现四字段复用、模板/最小LCEL/一次请求、raw/parsed/error检查、来源/归属/内容指纹、逐项引用位置、候选快照/过期、PG事务保存/并发幂等、owner过滤、人工审核版本绑定和CLI。
- 两张PostgreSQL表及Alembic0001，JSONB、owner复合外键、唯一约束和状态/版本约束。本机API实际六类业务接口及info；同步教学流程，禁止客户端owner/任意已校验正文和跨站写入。
- 完整Vue材料输入、卡片/原文对照、信息缺口、草稿保存、逐项核对、列表/分页/详情/刷新及已保存审核证据；请求期间锁定输入，修改输入清除旧候选。14课入口导入共享模块，中文讲义及独立迁移练习已替代旧TODO。
- 2.1/2.2用户代码与LEARNING_PROGRESS未修改，既有通过练习保留。参考交付完成不计用户掌握；2.2独立解释/用户运行缺项仍保留。
- 默认预览/课入口不读.env、不联网；AI默认禁用。网页完整流程使用明确标记historical_replay、attempts=0、usage=None；历史候选来自2.2的2026-10-12实测，不能说本轮新生成或用目标重新生成。

### 环境与实际命令

- 原Python3.12.15、uv0.12.24、.venv-py312及五个精确直接依赖版本保留。新增依赖通过scripts/uv-project.cmd add --no-upgrade --bounds exact，锁文件自动解析60个条目，目标环境58个已安装包。
- 官方FastAPI/SQLAlchemy2.1/Alembic/psycopg/Vue/Vite资料核实；psycopg在线文档为3.3.7.dev1，安装3.3.6，以本机连接/事务实测为准，不混同版本标签。
- EDB官方链接便携PostgreSQL18.6解压在忽略.local，创建新集群和fujian_stage2_dev/test。SCRAM随机密码不打印/提交，仅监听127.0.0.1:55432；未安装系统服务。原其他数据库/进程不操作。
- scripts/stage2-dev.ps1 setup/start/migrate/test实际执行。最初Start-Process -Wait等待数据库常驻子进程导致助手等待，定位后改为WaitForExit仅等待pg_ctl；数据库实际就绪后start继续创建专用库。专用库迁移实际通过。
- `.venv-py312/Scripts/python.exe -X utf8 -m pytest tests/test_stage2_offline.py -q`：32项通过。随后脚本test：32项离线+10份固定离线材料边界+6项真实PostgreSQL/HTTP，共48项通过，退出0（5.79秒）。未配置PG不伪造通过，而是skip。
- 真实PG检查：新Session/服务重开读取、重复及4线程同时保存只一条、事务中止回滚、owner复合外键拒绝、跨owner读/list、人工通过要求证据、旧版本冲突、HTTP保存读取审核、非法字段/分页、live禁用、Host/Origin/跨站/写入标记边界。
- Node24.19.0/pnpm11.25.0；Vue3.5.43、Vite8.3.4、plugin-vue6.0.10、vue-tsc3.3.13。TypeScript7.0.2首次构建失败（vue-tsc读取lib/tsc接口不兼容），最小修复固定新引入的TypeScript5.9.3；pnpm锁自动更新。scripts/stage2-web.ps1 -SkipInstall最终类型检查/构建通过，15模块、JS约78.20kB。
- `scripts/uv-project.cmd pip check --python .venv-py312/Scripts/python.exe`实际目标58包全部兼容；`uv-project.cmd lock --check`60条解析通过。首次未指定解释器的pip check读到旧环境43包，仅为诊断，不计正式环境验收。
- 浏览器实测：同源本机API→历史候选→对照→保存→两个逐项依据（范围/题型）→助手人工核对→审核版本2→刷新读取同一ID/状态→展开已有依据，全部实际可见。审核说明明确“不计用户能力”。截图[阶段2参考页面](../images/stage2-reference.jpg)。本次没有新付费模型请求。
- `.local/verify_stage2_delivery.py`实际通过：14课默认及14课--exercise全部退出0，网络/DNS/.env哨兵未触发；本任务29个Python文件AST、359个本地链接存在，2.1/2.2用户代码和LEARNING_PROGRESS差异为空。临时检查脚本忽略；新加链接最终提交前再核对。
- 最终文档调整后同一交付检查再次通过，链接增至368个；`stage2-dev.ps1 replay`实际CLI历史回放→开发库保存成功、pending_manual_review、attempts=0/usage=None，退出0。提交前ls-remote核对PLAN-002仍20aea1e、main仍cfc0247，未覆盖远端更新。

### 风险、学习与下一步

本机demo身份不是认证，尚无可上线多人平台；数据库/服务原文只在专用本机库，测试记录保留不删除。未保存候选30分钟或重启失效。新模板live路径未真实调用、完整F1十篇真实质量/真实身份跨用户授权/Linux未验证；历史回放不替代这些验收。

当前本机演示服务和本任务专用PG保持可打开，地址http://127.0.0.1:8000；可按运行手册停止/重启。临时下载/集群/随机密码/日志/node_modules/dist均忽略，不入Git。原等待助手如果仍存在只允许定位并停止本任务助手，不操作其他数据库。

继续学习只推进一个小修改：2.2独立raw/parsed/parsing_error与事实边界解释、用户运行证据自然接续，再进入2.3-A；本轮未代填任何用户能力。下一课独立迁移练习在README，参考实现已完整，不再以TODO阻挡运行。

Git交接：精确提交、推送并草稿PR基于codex/plan-002-stage2-curriculum；SHA/PR按实际回执登记，不合并main。
