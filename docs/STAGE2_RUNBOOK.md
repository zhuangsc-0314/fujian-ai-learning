# 阶段2完整参考实现：运行与阅读手册

任务[STAGE2-001](tasks/STAGE2-001-complete-reference.md)。参考实现已覆盖2.3—2.12；功能实测结果以任务记录为准，用户独立掌握仍单独验收。

## 1. 从哪里读

```text
learning_app/domain.py    四字段复用、材料、引句位置、人工审核规则
learning_app/ai.py        模板→最小LCEL→一次invoke→结构化检查/错误
learning_app/history.py   可追溯历史候选回放（本次生成次数0）
learning_app/storage.py   PostgreSQL表、归属外键、唯一约束和连接
learning_app/service.py   服务端候选、事务保存、读取、审核版本冲突
learning_app/api.py       本机同步API、服务端demo身份、同源请求边界
learning_app/cli.py       模板预览、回放/真实生成、列表/读取、Web启动
migrations/              Alembic 0001；不在应用启动时自动建表
web/src/                 Vue页面、原文对照组件、请求、页面状态
tests/                   离线与真实PostgreSQL/HTTP检查
project_steps/02_03*…    每课中文讲义和完整函数入口
```

依赖方向：CLI/HTTP → service → domain、storage、ai。保存和读取不invoke；AI不接收Session、连接密码或身份控制权。2.1/2.2原课用户逻辑未重写。

## 2. 离线起步

从仓库根目录运行，默认不读.env、不连接数据库、不调用模型：

```powershell
.\scripts\uv-project.cmd sync --locked
.\.venv-py312\Scripts\python.exe -X utf8 -m learning_app.cli preview
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_03a_content_review\main.py
.\.venv-py312\Scripts\python.exe -X utf8 -m pytest tests/test_stage2_offline.py -q
```

14课的main.py已导入完整函数。--exercise执行参考演示，退出0代表演示成功，不登记为用户独立通过。数据库课默认打印真实映射编译的SQL，仅是离线观察；不能把SQL预览算作PG连接/事务通过。

## 3. 本机PostgreSQL开发/测试库

Windows本轮使用EDB便携PostgreSQL18.6，位于忽略的.local；不安装系统服务。不连接生产库，不替换SQLite，不覆盖已有集群。首次准备：

1. 从[PostgreSQL Windows官方入口](https://www.postgresql.org/download/windows/)进入[EDB二进制下载](https://www.enterprisedb.com/download-postgresql-binaries)，选择Windows x86-64。本轮核实18.6链接为https://sbp.enterprisedb.com/getfile.jsp?fileid=1260609；未来下载需重新核对版本。
2. 下载到.local/stage2-postgres.zip，解压到.local/stage2-postgres，确保pgsql/bin/initdb.exe存在。不要提交二进制、配置或数据库文件。
3. 执行下面命令。setup创建新的专用集群；如目录或配置已存在就停止，改用start。

```powershell
.\scripts\stage2-dev.ps1 setup
.\scripts\stage2-dev.ps1 migrate
.\scripts\stage2-dev.ps1 test
```

setup使用随机密码和SCRAM，仅监听127.0.0.1:55432，创建fujian_stage2_dev和fujian_stage2_test。凭证留在忽略的.local/stage2-runtime.json，脚本不打印它。测试使用专用测试库，新建测试记录且不删除已有数据；重复运行会保留新的测试记录。

后续开机运行start；停止使用stop。migrate只运行upgrade，不自动执行会删表的downgrade。test对测试库迁移再运行正式tests；未配置外部测试库时直接pytest会明确skip数据库部分。

已有本机PG也可手动创建fujian_stage2前缀库，设置进程STAGE2_DATABASE_URL（完整凭证不可粘贴进聊天/PR），然后运行python -m alembic upgrade head。正式代码只允许postgresql+psycopg、本机host、专用库前缀，不允许连接串query重定向远端。手动测试变量为STAGE2_TEST_DATABASE_URL，库名必须fujian_stage2_test前缀。

## 4. 网页构建与启动

本轮Node24.19.0、pnpm11.25.0；package.json/pnpm-lock.yaml固定版本。TypeScript7首次构建与vue-tsc不兼容，已固定兼容5.9.3。不用升级现有Python/uv/LangChain。

```powershell
.\scripts\stage2-web.ps1
.\scripts\stage2-dev.ps1 start
.\scripts\stage2-dev.ps1 migrate
.\scripts\stage2-dev.ps1 serve
```

打开http://127.0.0.1:8000。FastAPI托管web/dist，页面与API同源；不启用任意CORS。Host/Origin/跨站来源和写请求标记会检查。页面明确展示“本机教学演示，尚无真实认证”。不要改监听为0.0.0.0用于多人访问。

默认真实生成禁用。正常演示：保留示例原文 → 载入历史候选 → 对照原文 → 保存待审核草稿 → 填逐项判断和逐字引句 → 人工核对 → 列表/详情 → 刷新重开。URL的?card=ID用于重开已保存记录。编辑输入会清掉旧候选，加载中锁定输入，保存和读取均不请求模型。历史回放仅对应同一份原文，学习目标不会重新生成历史答案。

人工通过需要至少一条逐项证据、完整核对确认和无时间冲突；这是人的结论，程序不判断摘要语义真伪。页面不使用v-html解释材料。Unicode引用位置按Python码点处理；服务端再次切片校验，不信任浏览器位置。

## 5. 真实生成入口（可能计费）

代码完整提供真实ChatDeepSeek/json_mode/include_raw和新模板链路；本任务没有再次发送付费请求。只有你主动选择时才运行：

```powershell
# 启动后，页面“真实生成”按钮才会启用；每次点击最多一次invoke，无自动重试。
.\scripts\stage2-dev.ps1 serve -Live
```

配置继续复用1.2的DEEPSEEK_*读取与校验。只有真实生成路径读.env；模型key不传到浏览器。失败显示input/configuration/invoke/parse_and_validate/database/review步骤。超时执行状态未知，先看供应商用量，不自动重试；保存失败不重新生成。

CLI也完整实现：python -m learning_app.cli replay --demo、list --demo、read --demo --card-id ID；真实generate需要--demo --live --material文件，并使用共享服务。脚本replay自动加载本机开发配置。数据库记录可持久保存；未保存候选只在进程内存，30分钟过期，重启丢失且不会自动再收费。

## 6. 学习与验收

完整参考交付不代表你独立掌握14课。继续学习时一次选一个小修改；各课README提供独立迁移练习、语法提示、正常/非法/边界案例和通过条件。先保留2.2缺少的独立解释/用户运行证据，再进入2.3-A自然复习。

PostgreSQL测试验证业务归属条件，demo身份不是登录认证。新模板真实生成、完整F1十篇真实材料质量、真实账号/跨用户认证、Linux和多人上线仍须独立验证。

依据：[LangChain模板/组合](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/from_messages)、[SQLAlchemy2.1 Session](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)、[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)、[psycopg安装](https://www.psycopg.org/psycopg3/docs/basic/install.html)、[FastAPI](https://fastapi.tiangolo.com/tutorial/)、[Vue](https://vuejs.org/guide/quick-start.html)、[Vite](https://vite.dev/guide/)。文档阅读不替代本机实测。
