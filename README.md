# 福建事业单位备考 AI 学习平台

为用户和朋友开发材料学习、政策问答、练习与错题复习平台，同时逐步学习 Python 和 LangChain。当前交付为设计、历史课程、阶段0诊断及阶段1模型调用示例，尚无可上线的多人平台。

GitHub 仓库：<https://github.com/zhuangsc-0314/fujian-ai-learning>（私有；需要仓库访问权限）。克隆不包含本机虚拟环境、`.local` 或 `.env`。

## 开发者与智能体接入

先阅读 [AGENTS.md](AGENTS.md)，再查看 [项目状态与任务索引](docs/PROJECT_STATUS.md)、[学习进度](docs/LEARNING_PROGRESS.md) 和 [决策记录](docs/DECISIONS.md)。当前用户练习不能由接入智能体代做。

供新智能体复制的 [协作提示词](docs/COLLABORATION_PROMPT.md)；新任务使用 [任务记录模板](docs/tasks/TEMPLATE.md)。每批次由协调者分配任务，同一文件一个负责人，并行开发使用独立分支与 checkout；通过 PR 交接。

## 当前项目任务：阶段1，任务1.2

打开 [LangChain模型接口讲义](project_steps/01_02_langchain_model/README.md) 和 [详细注释代码](project_steps/01_02_langchain_model/main.py)。用相同材料通过ChatDeepSeek.invoke得到AIMessage，见 [原目标实测记录](project_steps/01_02_langchain_model/RUN_RESULTS.md)。用户已独立修改LEARNING_GOAL：解释“客观题”，原文没定义时明确说明依据不足，且保留SYSTEM_MESSAGE；静态检查通过。下一步提供新目标实际运行结果、接口解释与调试证据，不重复代写目标。每次正常运行尝试一次真实请求，可能计费。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_02_langchain_model\main.py
```

前一任务：[1.1 SDK对照](project_steps/01_01_first_sdk_call/README.md)，独立目标修改、请求/响应解释和缺Key定位说明均通过，见 [用户证据](project_steps/01_01_first_sdk_call/USER_RUN_RESULTS.md)。1.2不升级依赖。

更早任务：[0.3 环境讲义](project_steps/00_03_reproducible_env/README.md)。课程按用户要求已完成，剩余补验收停止；报告扩展及新旧解释器运行/切换有证据，未验证项保留在[评审](project_steps/00_03_reproducible_env/REVIEW_RESULTS.md)，不阻挡1.2。1.1 新增 SDK 的显式直接声明，当前直接依赖4个，安装版本未变。

更早任务：[安全配置讲义](project_steps/00_02_safe_config/README.md)。本课双重验收通过：用户独立 MODEL 校验、优先级解释、9项运行日志及故障定位/输入修复说明有证据，见 [评审记录](project_steps/00_02_safe_config/REVIEW_RESULTS.md)。历史助手13隔离案例、真实配置入口及新环境回归通过；未验证真实Key有效性。

更早任务：[材料输入诊断](project_steps/00_01_material_input/README.md)。用户region规则及历史12案例通过；已恢复默认material.json并修复两份输入，另存负例后5项核验通过，见 [评审](project_steps/00_01_material_input/REVIEW_RESULTS.md)。0.1/0.2本课验收通过，0.3按用户要求收尾完成，当前进行1.2。推进课次不等于全部掌握。

当前课程分支 `codex/1-2-langchain-model`，包含此前所有课程；跨电脑指令见 [拉取与环境准备](docs/CROSS_COMPUTER_SETUP.md)，本课 Git 交付状态见 [任务记录](docs/tasks/1.2-langchain-model.md)。旧课程同步记录 [SYNC-002](docs/tasks/SYNC-002-progress-push.md) 保留为历史证据；任务分支通过 PR 交接，main 合并单独处理。

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
- 当前课选择“项目 1.2：LangChain模型接口”并按 `F5`，在 invoke 行设断点观察联网位置；历史课选择对应调试入口。
- 首次打开本地目录时，根据 VS Code 提示确认工作区信任后才能调试。

## 官方资料

- [LangChain 安装](https://docs.langchain.com/oss/python/langchain/install)
- [ChatDeepSeek 集成](https://docs.langchain.com/oss/python/integrations/chat/deepseek)
- [DeepSeek API 入门](https://api-docs.deepseek.com/)
- [Python 中文教程](https://docs.python.org/zh-cn/3/tutorial/)

LangChain 课程资料原核对日期：2026-10-05；uv 环境管理资料在 0.3 于 2026-10-09 核对，链接见讲义。正式解析版本见 `uv.lock` 与运行记录。模型名以 DeepSeek 官方 API 文档为准，部分集成教程仍使用旧模型名。
