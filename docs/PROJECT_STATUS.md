# 项目交付与协作状态

更新时间：2026-10-10。由本轮协调者维护；其他任务负责人更新各自任务文件并在 PR 中提出状态更新。

## 仓库与事实入口

- GitHub：<https://github.com/zhuangsc-0314/fujian-ai-learning>；已创建私有仓库并推送，默认分支 `main`。初始交付提交 `5ca2766` 已实测与远程 SHA 一致；本状态更新随后提交，最新状态以远程分支为准。
- 协作契约：根目录 `AGENTS.md`。
- 学习掌握事实：`LEARNING_PROGRESS.md`；架构决策：`DECISIONS.md`。
- 当前没有多人后端、前端、生产数据库迁移或平台部署。现有两课为历史学习示例；当前任务为1.2 LangChain模型接口。
- 当前1.2课程在 `codex/1-2-langchain-model`，课程提交0a42a19已推送且完整SHA与远端核对一致；[PR #4](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/4)已创建、未合并。Git交付状态见 [任务记录](tasks/1.2-langchain-model.md)；交付记录随后另行提交，跨电脑获取此分支，main合并单独处理。
- 历史1.1课程分支 `codex/1-1-first-model-call` 已推送，课程提交 `2cc6a56` 的本地/远端完整SHA实测一致；本交付记录随后另行提交，最新文档以分支远端为准。[PR #3](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/3) 未合并，含0.3用户修改/评审及此前课程；详见 [任务记录](tasks/1.1-first-sdk-call.md)。跨电脑先获取当前课程分支。
- 当前交付分支 `codex/0-3-reproducible-env` 已推送，课程提交 `ac3af79` 包含 0.1/0.2 用户修改、0.3 环境及进度记录，本地/远端完整 SHA 实测一致；本验收文档随后另行提交，最新状态以分支远端为准。详见 [SYNC-002](tasks/SYNC-002-progress-push.md)。[PR #2](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/2) 已创建、main 尚未合并；跨电脑使用该分支，不能只拉 main 后认定课程丢失。

## 任务索引

| ID | 范围 | 负责人 | 功能状态 | 学习状态 | 依赖/下一步 |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 材料输入诊断 | 当前教学智能体；用户独立修改/修复 | region历史12案例、修复/负例5项及收尾通过；AST一致 | 0.1核心输入/异常验收通过；阶段0其他课待证据 | [任务记录](tasks/0.1-material-input.md)；进入0.2配置解释验收 |
| SYNC-001 | GitHub 初始化与协作文档 | 当前主智能体/协调者 | 通过：私有 main 已推送，初始 SHA 已核实 | 不推进学习阶段 | 后续智能体先获仓库访问权限，再读 AGENTS 与任务记录 |
| SYNC-002 | 全部课程改动及学习进度云端同步 | 当前主智能体；用户直接分配 | 通过：课程已推送，远端 SHA 一致，PR #2 已创建 | 不把同步登记为学习掌握 | [任务记录](tasks/SYNC-002-progress-push.md)；[跨电脑说明](CROSS_COMPUTER_SETUP.md) |
| ENV-001 | 中文提交规范与本机 VS Code 语言修复 | 当前主智能体；用户本轮直接分配 | 通过：本机简中界面实测恢复；规范通过任务分支/PR 交接，main 待合并 | 不推进学习阶段 | 见 [任务记录](tasks/ENV-001-vscode-locale.md) |
| 0.2 | 环境变量与配置诊断 | 当前教学智能体；用户独立修改 | 通过：MODEL 校验、13 隔离案例与真实入口通过；新环境回归通过 | 独立修改、优先级/补充规则解释及失败定位说明通过；运行调试待证据 | [任务记录](tasks/0.2-safe-config.md)；运行现有隔离脚本并解释输入修复，其他练习保留 |
| 0.3 | 支持中的 Python 与依赖锁定 | 当前教学智能体；用户独立练习 | 环境通过，用户langchain-openai报告扩展实测通过 | 独立修改证据已取得；依赖解释/调试待验证 | [任务记录](tasks/0.3-reproducible-env.md)；[评审](../project_steps/00_03_reproducible_env/REVIEW_RESULTS.md) |
| 1.1 | 最小真实SDK请求对照 | 当前教学智能体；用户独立修改目标 | 原/新目标请求输出及离线检查通过，信息不足问题有据 | 独立修改/三项解释/输出核对/缺Key定位说明通过 | [任务记录](tasks/1.1-first-sdk-call.md)；[用户反馈](../project_steps/01_01_first_sdk_call/USER_RUN_RESULTS.md) |
| 1.2 | ChatDeepSeek模型接口 | 当前教学智能体；用户独立练习 | 真实AIMessage正文/元数据及10项离线检查通过 | 独立术语目标、接口解释/调试待证据 | [任务记录](tasks/1.2-langchain-model.md)；[讲义](../project_steps/01_02_langchain_model/README.md) |

“示例已提供”不等于功能阶段全部完成，“功能通过”不等于用户掌握。状态词采用：未开始、已分配、进行中、待验证、通过、阻塞；历史状态不靠覆盖运行记录来修改。

## 当前可运行内容

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_02_langchain_model\main.py
```

这条命令会尝试一次真实DeepSeek请求，可能计费，自动重试关闭；无网络验证用本课verify_cases.py。历史课程1/2也不能用于默认离线验证。

正式环境Python3.12.15、uv0.12.24；0.3双环境安装40包版本一致，1.1只将既有openai3.26.1改为显式直接声明，安装版本不变且兼容/锁检查通过。锁42条记录，直接依赖4个。旧Python3.10.10 .venv保留；本机工具/环境与.env不入仓库。DeepSeek默认公开材料调用已验证；Linux、百炼和真实异常分支未验证。

## 下一次开始工作的规则

1. `git fetch origin` 后核对当前分支、工作区和分配任务的基线 SHA；有本地改动先识别归属，不自动覆盖。
2. 阅读 `AGENTS.md` 及相关任务记录，确认自身任务和可编辑文件。
3. 1.1独立修改、解释、输出核对及缺Key定位说明通过；当前1.2用户术语目标/接口解释/调试待证据。阶段0解释/调试缺口保留，不因助手测试成功登记用户掌握。
4. 通过协调者分配不同文件的任务，再使用独立分支/worktree 并行。任务状态表不提供原子锁。

## 运维与模型状态

- 服务器资源已评估，安全缓存清理已执行；详见 `CLEANUP_EXECUTION_20261009.md`。历史候选清单不能当作本轮再次清理指令。
- 聊天模型沿用 DeepSeek；Embedding 已选择百炼 `qwen3.7-text-embedding`，初始 1024 维，Key 与业务空间端点待用户填写、连通和行为尚未验证。
- 服务器历史报告包含部署约束，不能因已创建 GitHub 仓库就上线；认证隔离、额度、备份与回滚仍未实现或验证。
