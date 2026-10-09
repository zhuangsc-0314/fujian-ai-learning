# 福建事业单位备考 AI 学习平台

为用户和朋友开发材料学习、政策问答、练习与错题复习平台，同时逐步学习 Python 和 LangChain。当前交付为设计、历史课程与阶段 0 诊断示例，尚无可上线的多人平台。

GitHub 仓库：<https://github.com/zhuangsc-0314/fujian-ai-learning>（私有；需要仓库访问权限）。克隆不包含本机 `.venv` 或 `.env`。

## 开发者与智能体接入

先阅读 [AGENTS.md](AGENTS.md)，再查看 [项目状态与任务索引](docs/PROJECT_STATUS.md)、[学习进度](docs/LEARNING_PROGRESS.md) 和 [决策记录](docs/DECISIONS.md)。当前用户练习不能由接入智能体代做。

供新智能体复制的 [协作提示词](docs/COLLABORATION_PROMPT.md)；新任务使用 [任务记录模板](docs/tasks/TEMPLATE.md)。每批次由协调者分配任务，同一文件一个负责人，并行开发使用独立分支与 checkout；通过 PR 交接。

## 当前项目任务：阶段0，任务0.1

从 [材料输入诊断讲义](project_steps/00_01_material_input/README.md) 和 [带详细注释的main.py](project_steps/00_01_material_input/main.py) 开始。先验证解释器、JSON读取与错误定位，再独立补上region校验。本任务不调用模型。

百炼Embedding已选定qwen3.7-text-embedding，.env与.env.example预留配置，API Key和对应业务空间接口地址由你后续填写；任务0.1不依赖这些配置。

## 从第一课开始

打开 [第一课讲义](lessons/01_first_chain/README.md)，再阅读 [main.py](lessons/01_first_chain/main.py)。

已有本机 `.venv` 使用 Python 3.10.10，VS Code 默认解释器指向该环境。这是历史课程环境快照；正式项目计划在任务 0.3 建立受支持的 Python 3.12 环境与完整依赖锁文件，当前 `requirements.txt` 只钉定顶层包。

首次克隆先将 `.env.example` 复制为 `.env`，填写 `DEEPSEEK_API_KEY` 并保存。已有 `.env` 不要覆盖。模型名和 DeepSeek 官方 API 地址已填写。Key 来自 [DeepSeek API 平台](https://platform.deepseek.com/api_keys)，聊天网站的登录状态不会自动提供 API Key。

在 VS Code 中选择 **终端 → 新建终端**，从项目根目录运行：

```powershell
.\.venv\Scripts\python.exe lessons\01_first_chain\main.py
```

每次运行发起一次真实模型请求，可能按服务商规则计费。`.env` 已被 Git 忽略；可分享的配置模板是 `.env.example`。

重新创建环境时：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

直接使用虚拟环境中的 Python，不必激活环境或修改 PowerShell 执行策略。

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
- 打开 `main.py`，选择“第一课：逐步调试”并按 `F5`。在 `chain.invoke(inputs)` 行左侧设置断点，观察输入和结果。
- 首次打开本地目录时，根据 VS Code 提示确认工作区信任后才能调试。

## 官方资料

- [LangChain 安装](https://docs.langchain.com/oss/python/langchain/install)
- [ChatDeepSeek 集成](https://docs.langchain.com/oss/python/integrations/chat/deepseek)
- [DeepSeek API 入门](https://api-docs.deepseek.com/)
- [Python 中文教程](https://docs.python.org/zh-cn/3/tutorial/)

资料核对日期：2026-10-05，实际依赖版本见 `requirements.txt`。模型名以 DeepSeek 官方 API 文档为准，部分集成教程仍使用旧模型名。
