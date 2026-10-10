# 在另一台电脑继续学习

适用于 Windows PowerShell；需要 Git、可创建虚拟环境的 Python、网络，以及这个私有仓库的访问权限。其他操作系统的环境创建命令需要调整，尚未实测。

## 获取当前进度

当前1.2课程和全部此前内容在 `codex/1-2-langchain-model` 分支，实际推送/PR状态见 [1.2任务记录](tasks/1.2-langchain-model.md)。没有合并前，仅拉 `main` 不会得到本轮内容。

首次获取：在你打算存放项目的父目录运行（目标文件夹不存在时）：

```powershell
git clone --branch codex/1-2-langchain-model https://github.com/zhuangsc-0314/fujian-ai-learning.git
cd fujian-ai-learning
git log -1 --oneline
```

已经克隆过：先运行 `git status`，保存并处理自己未提交的修改，不使用强制覆盖或 reset。然后：

```powershell
git fetch origin
git switch codex/1-2-langchain-model
git pull --ff-only
```

如果 `--ff-only` 提示分支分叉，保留两边提交，先查看历史并协调；不要强推。仓库登录失败时使用自己的 GitHub 账户授权，不把登录凭证粘贴到聊天或代码里。

## 建立本机环境

Git 同步代码与锁文件，不复制虚拟环境、本机工具或 API Key。首次在新电脑的仓库根目录运行：

```powershell
python -m venv .local\uv-tool
.\.local\uv-tool\Scripts\python.exe -m pip install --only-binary=:all: uv==0.12.24
.\scripts\uv-project.cmd python install 3.12.15 --no-bin --no-registry
.\scripts\uv-project.cmd sync --locked
.\scripts\uv-project.cmd pip check --python .venv-py312\Scripts\python.exe
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_03_reproducible_env\main.py
```

已有环境时不用重复创建：拉取后执行 `sync --locked`，再核对版本与兼容性。初次安装可能下载 Python 和依赖。这里不会调用模型；成功应输出 Python 3.12.15 和匹配的依赖报告。

本机建立配置模板（仅不存在 `.env` 时复制）：

```powershell
if (-not (Test-Path -LiteralPath .env)) {
    Copy-Item -LiteralPath .env.example -Destination .env
}
```

在新电脑自己的 `.env` 填写真实 DeepSeek Key；百炼 Key 与端点按之后的任务填写。不要提交 `.env`。0.3 核对不读取它，0.2 诊断需要配置已填写。

## 打开代码与接续进度

用 VS Code“文件 → 打开文件夹”打开克隆目录，阅读 README、AGENTS、PROJECT_STATUS 和 LEARNING_PROGRESS。1.1本课学习验收完成；当前任务1.2，独立TODO为术语解释目标及依据不足要求；0.3报告扩展已通过，阶段0各课解释/调试仍有待验收。同步环境、填写配置后运行1.2的main.py会发真实请求，可能计费。

1.2和0.3的F5调试入口明确使用 `.venv-py312`。新电脑没有旧 `.venv`，旧课程 F5 入口需要另行调整或使用新解释器的显式命令，不能假定虚拟环境跟随 Git 复制。Markdown 打开后按 `Ctrl+Shift+V` 查看预览。

当前 0.1 默认选中缺 region 的案例，是保留的用户练习状态；正常验证可显式传参，不要误判安装失败：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py project_steps\00_01_material_input\cases\material.json
```

后续换电脑前提交并推送，换电脑后先拉取，再根据锁文件同步环境。新智能体也需读取进度文档，不能从程序成功运行推断你已掌握。
