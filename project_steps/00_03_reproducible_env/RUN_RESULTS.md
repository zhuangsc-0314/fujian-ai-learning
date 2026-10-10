# 0.3 实际运行记录

日期：2026-10-09；Windows 本机。以下为助手真实执行的环境检查，未调用模型，未模拟模型回答；用户独立 TODO 尚未完成。Linux 部署未验证。

## 环境与版本

- 工具：uv 0.12.24，隔离安装于 `.local/uv-tool`。
- 新 Python：CPython 3.12.15，Astral 管理分发，位于 `.local/python`；未注册系统解释器、修改全局 PATH 或替换旧环境。
- 主环境 `.venv-py312` 和第二个新环境 `.venv-rebuild312` 均实际安装 40 个发行包，按规范化包名排序后的版本集合完全一致。
- `uv.lock` 42 条包记录，包含项目及平台相关记录，不等于本机安装包数。

| 包 | 新环境实际版本 | 说明 |
| --- | --- | --- |
| langchain-core | 1.6.6 | 直接依赖，原版本保留 |
| langchain-deepseek | 1.1.1 | 直接依赖，原版本保留 |
| python-dotenv | 1.2.4 | 直接依赖，原版本保留 |
| langchain-openai | 1.6.7 | 间接依赖 |
| pydantic | 2.14.0 | 新锁解析出的版本；旧环境为 2.13.5 |
| openai | 3.26.1 | 新锁实际版本 |
| langsmith | 0.14.5 | 间接依赖；未开启远端追踪 |

## 命令与实测

建立时使用本地 uv 工具，显式设置 `UV_PROJECT_ENVIRONMENT`、`UV_PYTHON_INSTALL_DIR` 和 `UV_CACHE_DIR`。现可通过 `scripts/uv-project.cmd` 重复以下主环境检查：

```powershell
.\scripts\uv-project.cmd sync --locked --check --offline
.\scripts\uv-project.cmd lock --check --offline
.\scripts\uv-project.cmd pip check --python .venv-py312\Scripts\python.exe
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_03_reproducible_env\main.py
```

实际：退出 0；锁文件未过期；40 个已安装包的依赖要求兼容；主环境无需变化；程序显示 Python 3.12.15、3 个直接依赖及匹配的包版本。

第二个新环境实际执行同一锁文件的 `sync --locked`，以及 `pip check` 和本课入口，均退出 0。用 `importlib.metadata.distributions()` 比较两个新环境的包名/版本集合，40 项全部一致。这证明本次 Windows 重建结果；不承诺所有未来网络或其他操作系统必然成功。

## 错误与回归

| 检查 | 实际结果 |
| --- | --- |
| 旧解释器运行本课 | 退出 2，明确需要 Python 3.12，没有 Traceback |
| 副本缺锁文件 | 退出 2，文件错误 |
| 副本 TOML 损坏 | 退出 2，TOML 格式错误 |
| 副本补丁版本不一致 | 退出 2，补丁版本错误 |
| 副本 project 字段类型错误 | 退出 2，配置表错误 |
| 副本包含不可信普通文字字段 | 退出 0，未执行文字 |
| 副本声明改变，锁文件未更新 | `uv lock --check --offline` 退出 1，符合预期 |
| LangChain 离线冒烟 | ChatPromptTemplate 渲染与 ChatDeepSeek 对象构造通过；未 invoke 模型；使用无效标记而非真实 Key，未开启追踪 |
| 0.2 主程序在新环境运行 | 退出 0，真实本地配置读取，不输出原值 |
| 0.2 verify_cases.py 在新环境运行 | 退出 0，原有配置诊断回归通过 |
| 旧环境快照 | Python 3.10.10、Pydantic 2.13.5 保持原样 |
| .env | 检查前后内容摘要一致；未输出摘要或配置内容 |

故障注入均在临时副本完成，不修改真正的声明或锁文件。此项没有验证 Key 有效性、账户额度、DeepSeek/百炼连通性或 API 行为。实际模型请求数为 0。

收尾检查：本课 Python 语法、TOML 和 VS Code JSON/调试路径通过；`uv tree --locked --depth 2` 实际可用。Git 忽略检查确认 `.env`、本地工具、新环境和重建环境不会进入版本库。VS Code CLI 已成功执行打开讲义/代码，未验证图形调试会话。

全工作区 `git diff --check` 仍指出 0.1 用户文件末尾多一个空行，这是已记录的旧课收尾项；未自动改用户代码，不能将全工作区格式检查写成通过。

## 学习与 Git 状态

环境交付检查通过；用户的 `AUDIT_PACKAGES` 扩展、依赖路径解释及错误定位能力待验收，不能把本记录当作用户已掌握。

本轮分支 `codex/0-3-reproducible-env`，基线 `e43e9a8`。0.1/0.2 原有未提交修改保留；0.3 也尚未 commit/push。本记录生成时没有新增提交或远程同步，后续以 Git/PR 的真实状态更新。
