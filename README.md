# 福建事业单位备考 AI 学习平台

为用户和朋友开发材料学习、政策问答、练习与错题复习平台，同时逐步学习 Python 和 LangChain。当前交付为设计、历史课程、阶段0诊断及阶段1模型调用示例，尚无可上线的多人平台。

GitHub 仓库：<https://github.com/zhuangsc-0314/fujian-ai-learning>（私有；需要仓库访问权限）。克隆不包含本机虚拟环境、`.local` 或 `.env`。

## 开发者与智能体接入

**准备新开会话：** 查看[新会话交接记录](docs/NEXT_SESSION_HANDOFF.md)顶部最新说明。续接分支`codex/2.2-instance-display`继承`codex/handoff-001-next-session`，已验收用户展示；先核实仓库状态，不把历史提示词的TODO快照当当前任务。

先阅读 [AGENTS.md](AGENTS.md)，再查看 [项目状态与任务索引](docs/PROJECT_STATUS.md)、[学习进度](docs/LEARNING_PROGRESS.md) 和 [决策记录](docs/DECISIONS.md)。当前用户练习不能由接入智能体代做。

供新智能体复制的 [协作提示词](docs/COLLABORATION_PROMPT.md)；新任务使用 [任务记录模板](docs/tasks/TEMPLATE.md)。每批次由协调者分配任务，同一文件一个负责人，并行开发使用独立分支与 checkout；通过 PR 交接。

长期复习入口：[学习笔记.md](学习笔记.md)。已整理0.1至2.2共15个功能完成小节的核心知识、代码和误区，独立掌握状态单独标明。每完成一小节更新相应条目，随该任务提交、推送并通过PR交接；笔记属于正式Git文件。

## 当前学习：2.2真实结构化学习卡

历史复习入口：[2026-10-12学习档案](docs/learning/2026-10-12.md)。2026-10-13用户已完成2.2展示，助手18项基础+2项展示检查通过/退出0；漏传层、请求位置及异常流程回答已有证据。下一步只补同课raw/parsed/error与事实边界独立解释、用户离线日志，不重做展示。最新续接分支`codex/2.2-instance-display`，main尚未包含近期课程；跨电脑见[接续指引](docs/CROSS_COMPUTER_SETUP.md)，以当前分支和任务记录为准。

打开[2.2讲义](project_steps/02_02_structured_card/README.md)和[详细入口](project_steps/02_02_structured_card/main.py)，看adapter.py的wrap_model及main的structured_model.invoke。默认预览不读.env/不请求，也不执行展示函数；verify_cases.py --exercise离线验收展示，本轮18+2项通过。助手历史一次真实生成parsed为LearningCard，470输入/140输出/610总token；本轮没有新真实请求。功能与独立展示修改通过，整课能力待证据。候选始终待人工核对，未保存/未认证，单引用不证明支持每项事实。见[实测](project_steps/02_02_structured_card/RUN_RESULTS.md)和[任务](docs/tasks/2.2-structured-card.md)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\main.py
```

助手已进行一次真实调用，不为展示修改重复付费；显式--live才会读取本机配置和再次尝试请求，可能计费，自动重试关闭。依赖保持不变。

## 上一课核心验收：2.1学习卡结构与校验

先看 [2.1讲义](project_steps/02_01_card_schema/README.md) 和 [schema.py](project_steps/02_01_card_schema/schema.py)，再看main.py的validate_card。用户独立information_gap字段/输入及修复已通过；助手20项基础和5项字段练习全部通过、退出0。用户准确定位model_validate校验及失败后不展示，并解释格式不证明事实，本课限定核心验收通过；candidate为dict由助手纠正，用户运行日志未验证。此前本地字段拼写回退已恢复为information_gap，20+5项检查重新通过；历史差异见任务，不重做已通过练习。本课人工候选不是AI回答，不读.env、不调用模型、不保存数据库；引用存在不保证摘要有据，占位归属不是真实认证。见 [任务记录](docs/tasks/2.1-card-schema.md)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_01_card_schema\main.py
```

2.1把已安装Pydantic2.14.0改为第5个直接依赖，包版本未升级；新电脑同步scripts/uv-project.cmd sync --locked。下一小步才接真实结构化生成，阶段2完整闭环未完成。

## 上一课核心验收：1.5-B目标参数贯通与故障定位

[1.5-B讲义](project_steps/01_05b_call_flow/README.md)复用1.5-A参数与1.2完整入口。2026-10-12用户独立补传learning_goal=goal，助手17项基础和3项贯通练习全部通过，--diagnose目标一致、退出0；注入超时且不展示正文，真实HTTP0。功能/独立修改通过；用户已准确定位invoke超时与跳过正文展示，并在提示后正确区分诊断通过与模型成功，本课限定核心验收通过，1.5收尾。用户独立运行日志和完整六步口述仍未单独验证，不阻挡后续；阶段1不登记全部能力掌握。默认预览、离线诊断不读.env/不请求API；修复后的--live须显式选择，最多一次真实尝试，可能计费，本轮未运行。无新增依赖；见[任务记录](docs/tasks/1.5-b-call-flow.md)。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\main.py --diagnose --goal "列出原文包含的科目"
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\verify_cases.py --exercise
```

## 上一课：1.5-A学习目标命令行参数

[1.5-A讲义](project_steps/01_05a_goal_argument/README.md)提供离线目标/消息预览，用户已独立新增`--goal`。18项基础及7项练习检查全部通过、退出0；默认/自定义目标正常，空白目标本地拒绝/退出2。功能与独立修改通过，用户独立运行及消息流转/失败位置解释未验证。保留1.2默认目标和System约束，不读.env、不创建模型、不调用API、不新增依赖；真实集成留到1.5-B。修改边界和证据见[任务记录](docs/tasks/1.5-a-goal-argument.md)，通过[草稿PR #16](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/16)交接。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\verify_cases.py --exercise
```

上一课[1.4-C](project_steps/01_04c_token_budget/README.md)功能及预算修改通过，用户正确解释百万单位换算和估算不是真实账单；具体计费差异原因由助手补充，用户独立运行日志未验证。1.4限定收尾，不重做已通过TODO。旧1.4-B显式--live仍会请求，已有真实记录，不为复习重跑。

## 已完成修改：1.4-A读懂token用量

打开[1.4-A讲义](project_steps/01_04a_token_usage/README.md)与[main.py](project_steps/01_04a_token_usage/main.py)：回放1.2用户历史用量147/91/238，区分token与字符、两类元数据、输出上限与预算。用户合计展示已独立完成，助手7项基础及合计探针通过，检查脚本退出0。功能与独立修改通过，用户运行日志/3概念解释待验证。全程不读.env、不联网、不生成模型回答；人工边界样例与真实历史记录明确区分。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04a_token_usage\main.py history
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_04a_token_usage\verify_cases.py
$LASTEXITCODE
```

任务/负责人/修改边界与实测见[1.4-A记录](docs/tasks/1.4-a-token-usage.md)。1.3-C已通过8项案例及500探针，用户修改/解释有证据、独立运行日志未验证；下述骨架安排均属历史快照。真实长短文比较已在1.4-B通过，价目核对及1.4-C离线估算已完成，1.4限定收尾，独立运行缺项保留。

## 历史入口：参数补讲与1.3-A骨架

先读 [Python命令行参数讲义](project_steps/01_03_request_errors/COMMAND_LINE.md)，运行同目录 [args_demo.py](project_steps/01_03_request_errors/args_demo.py)。独立练习是新增一行“用户参数数量”输出；助手没有代做。当天累计进度与证据见 [2026-10-10学习档案](docs/learning/2026-10-10.md)。

打开 [1.3-A讲义](project_steps/01_03_request_errors/README.md) 和 [main.py](project_steps/01_03_request_errors/main.py)。本小步是明确标记的故障注入：不读取.env、不联网、不生成模型回答。用户独立TODO是在通用连接分支前增加超时分支；6项基础检查已通过，TODO探针仍待完成，见 [实测](project_steps/01_03_request_errors/RUN_RESULTS.md)。整课1.3及用户能力均未完成。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\main.py timeout
```

目前退出1、显示通用失败是骨架预期；完成TODO后才有独立超时反馈。下一小步再做认证/限流。1.3任务与双重验收见 [记录](docs/tasks/1.3-request-errors.md)。

## 已完成任务1.2

1.2本课双重验收通过：用户独立修改LEARNING_GOAL、保留SYSTEM_MESSAGE，新目标真实回答有据，并正确定位invoke请求与空材料失败；见 [用户运行与收尾评审](project_steps/01_02_langchain_model/USER_RUN_RESULTS.md)。usage_metadata专门记录token用量的准确含义由助手补充，不计用户独立精确解释。当前已进入1.3-A，不重复要求1.2正常请求或已通过问题。

已完成课程可回看 [LangChain模型接口讲义](project_steps/01_02_langchain_model/README.md) 和 [详细注释代码](project_steps/01_02_langchain_model/main.py)。原目标实测见 [助手历史记录](project_steps/01_02_langchain_model/RUN_RESULTS.md)。下方为1.2复习命令，每次正常运行尝试一次真实请求，可能计费，完成验收后无需重跑。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_02_langchain_model\main.py
```

前一任务：[1.1 SDK对照](project_steps/01_01_first_sdk_call/README.md)，独立目标修改、请求/响应解释和缺Key定位说明均通过，见 [用户证据](project_steps/01_01_first_sdk_call/USER_RUN_RESULTS.md)。1.2不升级依赖。

更早任务：[0.3 环境讲义](project_steps/00_03_reproducible_env/README.md)。课程按用户要求已完成，剩余补验收停止；报告扩展及新旧解释器运行/切换有证据，未验证项保留在[评审](project_steps/00_03_reproducible_env/REVIEW_RESULTS.md)，不阻挡1.2。1.1曾将SDK显式直接声明增至4个；2.1再显式声明已有Pydantic，当前直接依赖5个，安装版本未变。

更早任务：[安全配置讲义](project_steps/00_02_safe_config/README.md)。本课双重验收通过：用户独立 MODEL 校验、优先级解释、9项运行日志及故障定位/输入修复说明有证据，见 [评审记录](project_steps/00_02_safe_config/REVIEW_RESULTS.md)。历史助手13隔离案例、真实配置入口及新环境回归通过；未验证真实Key有效性。

更早任务：[材料输入诊断](project_steps/00_01_material_input/README.md)。用户region规则及历史12案例通过；已恢复默认material.json并修复两份输入，另存负例后5项核验通过，见 [评审](project_steps/00_01_material_input/REVIEW_RESULTS.md)。0.1/0.2本课验收通过，0.3按用户要求收尾完成，1.1/1.2本课通过，下一任务1.3。推进课次不等于全部掌握。

本次 [SYNC-003](docs/tasks/SYNC-003-daily-main.md) 已通过 [PR #6](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/6) 将全部既有课程和今日档案合并到 `main`，统一获取入口为 `main`；跨电脑环境准备见 [拉取与环境准备](docs/CROSS_COMPUTER_SETUP.md)。旧课程分支与 [SYNC-002](docs/tasks/SYNC-002-progress-push.md) 保留为历史记录；各任务里的早期“未合并”属于当时快照，最新结果以SYNC-003及GitHub为准。

百炼Embedding已选定qwen3.7-text-embedding，.env与.env.example预留配置，API Key和对应业务空间接口地址由你后续填写；任务0.1不依赖这些配置。

## 从第一课开始

打开 [第一课讲义](lessons/01_first_chain/README.md)，再阅读 [main.py](lessons/01_first_chain/main.py)。

本机旧 `.venv` 使用 Python 3.10.10，暂留给历史课程；新正式环境 `.venv-py312` 使用 Python 3.12.15。VS Code 默认路径已更新，0.3 F5 入口明确使用新环境；历史课程 F5 仍使用旧环境。若编辑器缓存旧选择，以程序打印路径核实。

首次克隆先将 `.env.example` 复制为 `.env`，填写 `DEEPSEEK_API_KEY` 并保存。已有 `.env` 不要覆盖。模型名和 DeepSeek 官方 API 地址已填写。Key 来自 [DeepSeek API 平台](https://platform.deepseek.com/api_keys)，聊天网站的登录状态不会自动提供 API Key。

在 VS Code 中选择 **终端 → 新建终端**，从项目根目录运行：

```powershell
.\.venv-py312\Scripts\python.exe lessons\01_first_chain\main.py
```

每次运行发起一次真实模型请求，可能按服务商规则计费。`.env` 已被 Git 忽略；可分享的配置模板是 `.env.example`。

新克隆环境按 [0.3 安装步骤](project_steps/00_03_reproducible_env/README.md) 建立，正式依赖以 `pyproject.toml` + `uv.lock` 为准，`requirements.txt` 保留历史课程顶层版本。使用 `scripts/uv-project.cmd sync --locked` 同步新环境，不直接操作旧 `.venv`。直接使用环境中的 Python，不必激活或修改执行策略。历史课程在新环境的真实 API 调用未在 0.3 验证。

## 学习路线

当前项目式学习路线：[AI 学习平台设计与开发路线](docs/AI_LEARNING_PLATFORM_DESIGN.md)。面向你和朋友备考未来福建事业单位招聘，包含多人权限、部署与每阶段的功能/能力验收。当前仅设计，平台尚未实现。

学习证据与下一任务：[学习进度记录](docs/LEARNING_PROGRESS.md)。下列课程是已有示例；后续开发顺序以平台路线为准。

服务器实际巡检与部署调整：[服务器适配评估](docs/SERVER_ASSESSMENT.md)（2026-10-09，只读评估，尚未部署）。

历史清理候选和服务选型：[清理清单与 Embedding 推荐](docs/CLEANUP_AND_EMBEDDING.md)。已执行的安全清理及实测结果见 [清理执行记录](docs/CLEANUP_EXECUTION_20261009.md)；尚未调用 Embedding API。

早期构思保留：[公考热点与刷题助手方案](PROJECT_LEARNING.md)。

1. 第一课：提示词、真实 DeepSeek API、`invoke()` 和第一条链（已创建）。
2. [第二课：消息历史、连续对话与流式输出](lessons/02_chat_history/README.md)（已创建）。
3. 第三课：结构化输出与验证。
4. 第四课：工具调用与 Agent。
5. 第五课：文档加载、切分、检索与 RAG。

## 用 VS Code 做 code review

- `Ctrl+P`：按文件名打开代码。
- `Ctrl+Shift+E`：查看项目文件。
- `Ctrl+Shift+G`：查看本地 Git 改动；以提交与远程分支核对同步状态。
- 当前课选择“项目 1.3-A：超时故障注入”并按 `F5`，观察异常捕获，不联网；1.2及历史课选择对应调试入口。
- 首次打开本地目录时，根据 VS Code 提示确认工作区信任后才能调试。

## 官方资料

- [LangChain 安装](https://docs.langchain.com/oss/python/langchain/install)
- [ChatDeepSeek 集成](https://docs.langchain.com/oss/python/integrations/chat/deepseek)
- [DeepSeek API 入门](https://api-docs.deepseek.com/)
- [Python 中文教程](https://docs.python.org/zh-cn/3/tutorial/)

LangChain 课程资料原核对日期：2026-10-05；uv 环境管理资料在 0.3 于 2026-10-09 核对，链接见讲义。正式解析版本见 `uv.lock` 与运行记录。模型名以 DeepSeek 官方 API 文档为准，部分集成教程仍使用旧模型名。
