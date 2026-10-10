# 0.3：让项目在同一份环境中重复运行

本课不调用模型，也不需要填新 Key。先解决“我与朋友运行同一份代码，依赖版本为什么不同”，再进入真实模型调用。原来的 `.venv` 和你在 0.1/0.2 的代码保持原样。

## 1. 本次交付

建立 Python 3.12.15 的独立环境 `.venv-py312`，用 uv 0.12.24 管理依赖，提交可分享的环境声明和锁文件。提供 [main.py](main.py) 核对当前解释器和依赖版本。[实际运行记录](RUN_RESULTS.md) 是助手测试证据，你的独立练习还没有完成。

本课三个新概念：解释器与虚拟环境、直接与间接依赖、声明与锁定及同步。

## 2. 为什么现在学

下一阶段会接入 DeepSeek。如果别人使用不同依赖版本，即使提示词相同，也可能出现导入失败、接口变化等问题。先固定环境，才能判断错误来自环境、配置还是模型请求。

旧环境 Python 3.10.10 保留供历史课程使用；本课新建环境，避免直接升级它。本次只保持三个直接依赖的原版本，间接依赖经过重新解析并锁定，不能说新旧环境的所有包版本相同。

## 3. 通俗概念与技术名称

| 概念 | 在本项目中是什么 | 常见误解 |
| --- | --- | --- |
| 解释器 interpreter | 实际执行代码的 Python 程序；本课为 `.venv-py312/Scripts/python.exe` | 电脑装了 Python 不代表终端或 F5 用的就是它 |
| 虚拟环境 virtual environment | 为本项目隔离安装包的目录 | 激活环境并不安装依赖；本课直接写解释器路径，无须激活 |
| 直接依赖 direct dependency | 我们主动声明的包，如 `langchain-deepseek` | 导入得到某包不代表它一定被我们直接声明 |
| 间接依赖 transitive dependency | 直接依赖需要的其他包 | 只固定三个顶层包不会固定所有间接包 |
| 声明 manifest | `pyproject.toml` 表达项目需要什么、允许什么 Python 版本 | 文件存在不等于包已经安装 |
| 锁文件 lockfile | `uv.lock` 保存解析后的版本、平台条件和下载哈希 | 不要手工修改它；它不是当前环境的包目录 |
| 同步 sync | 根据声明和锁文件将包装入目标环境 | uv 默认操作 `.venv`，本项目用专用脚本明确目标 |

`.python-version` 固定本课 Python 补丁版本；`requires-python` 限定项目的主次版本范围。版本应按安全维护更新，锁定不是永远不升级。

TOML 是配置文本格式，和 JSON 一样需要解析；`[project]` 表示一张配置表。Python 3.12 内置 `tomllib`。解析 TOML 不会执行里面写的命令。

## 4. 输入、处理、输出和模块关系

```text
pyproject.toml（直接依赖要求） + .python-version（Python 版本）
                         ↓ uv 解析
                      uv.lock
                         ↓ uv sync --locked
                  .venv-py312 实际环境
                         ↓ main.py 读取版本与公开元数据
               解释器路径 + 包版本 + 核对结果
```

`scripts/uv-project.cmd` 固定本项目的工具、Python 下载目录、缓存和目标环境。它使用局部环境变量，不修改系统 PATH、注册表或旧 `.venv`。`uv pip check` 检查已安装包之间的版本要求；本课 `main.py` 只核对报告列表，不能替代完整兼容检查。

## 5. 最小运行方式

在 VS Code 打开项目根目录，从该目录的新终端运行：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_03_reproducible_env\main.py
```

预期：Python 3.12.15；3 个直接依赖；当前锁文件 42 条包记录（包含项目）；报告三个包的版本匹配；模型请求数 0。**42 条记录不等于 Windows 安装了 42 个发行包**，本次实际安装 40 个。

查看依赖关系与核对环境：

```powershell
.\scripts\uv-project.cmd tree --locked --depth 2
.\scripts\uv-project.cmd lock --check
.\scripts\uv-project.cmd pip check --python .venv-py312\Scripts\python.exe
```

按已有锁文件同步环境：

```powershell
.\scripts\uv-project.cmd sync --locked
```

`--locked` 要求锁文件与声明一致，过期就报错，不自动改锁文件。同步会清理目标环境中不需要的包，所以使用这个包装脚本，不直接让 uv 操作旧 `.venv`。复现安装可能联网下载，不会发起模型请求。

VS Code 左侧“运行和调试”选择 **项目 0.3：环境与依赖核对**，按 F5。该入口明确使用新解释器。默认解释器设置已更新；VS Code 如果记住了旧选择，可通过 `Ctrl+Shift+P` → “Python: 选择解释器”选择 `.venv-py312`，再用程序打印的实际路径确认。旧课程的 F5 入口继续保留旧环境。

### 朋友从干净仓库建立环境

先安装一个能创建虚拟环境的 Python，再在仓库根目录运行以下命令。已有这些目录时不要重复创建或覆盖，先检查任务记录。

```powershell
python -m venv .local\uv-tool
.\.local\uv-tool\Scripts\python.exe -m pip install --only-binary=:all: uv==0.12.24
.\scripts\uv-project.cmd python install 3.12.15 --no-bin --no-registry
.\scripts\uv-project.cmd sync --locked
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_03_reproducible_env\main.py
.\scripts\uv-project.cmd pip check --python .venv-py312\Scripts\python.exe
```

本机已经完成，不需要你重装。uv 使用 Astral 管理的 CPython 分发包；本次未使用 python.org 图形安装器或注册系统 Python。`.local`、所有虚拟环境和 `.env` 都不能提交；分享 `.python-version`、`pyproject.toml`、`uv.lock` 和代码。后续模型调用需朋友在自己的 `.env` 填 Key，不能复制你的真实 Key。

`requirements.txt` 仅保留历史课程的三个顶层版本；正式环境以 `pyproject.toml` 和 `uv.lock` 为准，不同时维护两份不同的依赖声明。

## 6. 关键代码怎么读

- `sys.executable` 是实际解释器路径；`sys.version_info[:2]` 用切片取得主版本和次版本；先检查解释器，避免旧 Python 导入 `tomllib` 失败。
- `sys.prefix != sys.base_prefix` 表示正在虚拟环境中。它不保证依赖正确，还要继续核对。
- `Path(__file__).resolve().parents[2]` 从本文件找到项目根目录，不依赖你从哪个文件夹执行。可选命令行参数仅用来核对隔离副本。
- `with path.open("rb")` 在结束时关闭文件；`rb` 返回字节，符合 `tomllib.load` 的要求。
- `name, separator, expected = item.partition("==")` 是元组解包：把返回的三项分别赋给三个变量。本课只处理精确版本声明，不实现完整版本规范解析器。
- `source = ... if ... else ...` 是条件表达式，用成员判断区分直接/间接依赖。它不会改变依赖或安装任何包。
- `version(name)` 查询当前环境的发行包元数据，不需要导入模型模块。包不存在时抛出 `PackageNotFoundError`。
- 锁记录循环找到匹配后 `break` 只退出这一层循环；`return 2` 退出当前函数；`raise SystemExit(main())` 将函数返回值交给操作系统作为进程退出码。
- 注释和函数类型提示帮助读代码，不会自动验证运行时数据，所以仍有 `isinstance` 等检查。

## 7. 你独立完成的小修改

只修改 `main.py` 的 **TODO 0.3**：

1. 将 `langchain-openai` 加入 `AUDIT_PACKAGES`，运行后多输出它的版本和“间接依赖”。
2. 用 `uv tree` 找到它由哪个直接依赖带入，写出路径。
3. 用自己的话解释：为什么仅固定 `requirements.txt` 中的三个版本，还不能固定全部依赖？`pyproject.toml`、`uv.lock`、虚拟环境分别负责什么？

不新增直接依赖，不改锁文件，不安装或升级包。这个修改只是扩展报告列表。保留元组写法，新增元素使用逗号分隔；字符串不是包模块的导入语句。

## 8. 正常、非法和不可信案例

| 案例 | 如何验证 | 预期结果 |
| --- | --- | --- |
| 正常 | 用 `.venv-py312` 运行本课 | 退出 0，版本一致 |
| 解释器错误 | 用旧 `.venv/Scripts/python.exe` 运行本课 | 退出 2，提示需要 Python 3.12，无导入 Traceback |
| 缺文件/非法 TOML | 仅在隔离副本删除锁文件或损坏 TOML，传入副本路径 | 退出 2，定位为文件或配置错误 |
| 补丁版本不同 | 仅在副本修改 `.python-version` | 退出 2，提示补丁版本不一致 |
| 锁文件过期 | 仅在副本改变直接依赖要求，执行 `uv lock --check --offline --project <副本路径>` | 非零退出，不能宣称同步完成 |
| 不可信文本 | 在副本 TOML 加入普通字符串字段 `ignored_text = "do_not_execute"` | 作为数据解析，不执行文字内容 |

后四类已由助手在临时副本验证；你不用破坏真实配置复现。需要补练时先让我提供一个独立副本。你的“没有依据修改真实锁文件”也属于正确调试选择。

## 9. 双重通过条件

**项目交付**：新环境能运行；锁文件与声明一致；兼容检查通过；第二个新环境版本集合一致；0.2 回归通过；旧环境与 `.env` 保持原样。已实测，但不代表 Linux 部署或 DeepSeek API 行为通过。

**学习掌握**：你独立扩展报告成功；能从依赖树找到来源；解释三种文件/目录的职责；遇到旧解释器错误能根据实际路径定位并切换到正确解释器。仅回复“已完成”会触发代码检查，解释和调试仍需要证据。

## 10. 完成后如何推进

修改后告诉我“0.3 已完成”，附依赖路径和第 7 节的简短解释。我检查你的代码和运行结果，决定是否需要一个补练，再进入阶段 1 的最小模型调用。0.1/0.2 尚缺的解释证据继续记录，不因为推进就登记为全部掌握。

官方依据（2026-10-09 核对）：[uv 安装](https://docs.astral.sh/uv/getting-started/installation/)、[锁定与同步](https://docs.astral.sh/uv/concepts/projects/sync/)、[项目环境路径](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path)、[管理的 Python 分发](https://docs.astral.sh/uv/concepts/python-versions/#managed-python-distributions)、[Python 维护状态](https://devguide.python.org/versions/)。
