# 在另一台电脑继续学习

适用于 Windows PowerShell；需要 Git、可创建虚拟环境的 Python、网络，以及这个私有仓库的访问权限。其他操作系统的环境创建命令需要调整，尚未实测。

## 获取当前进度

本次统一入口为 `main`，包含此前课程、1.3-A骨架及命令行参数补讲；使用前先确认 [SYNC-003](tasks/SYNC-003-daily-main.md) 的汇总PR已合并。此前各任务文件里的分支入口是当时的交付快照。

首次获取：在你打算存放项目的父目录运行（目标文件夹不存在时）：

```powershell
git clone --branch main https://github.com/zhuangsc-0314/fujian-ai-learning.git
cd fujian-ai-learning
git log -1 --oneline
```

已经克隆过：先运行 `git status`，保存并处理自己未提交的修改，不使用强制覆盖或 reset。然后：

```powershell
git fetch origin
git switch main
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

用 VS Code“文件 → 打开文件夹”打开克隆目录，阅读 README、AGENTS、PROJECT_STATUS、LEARNING_PROGRESS 和 [当天档案](learning/2026-10-10.md)。0.1/0.2/1.1/1.2本课核心验收通过；0.3按用户要求收尾，不重新补验收。当前先做 [命令行参数独立小练习](../project_steps/01_03_request_errors/COMMAND_LINE.md)，再补1.3-A超时except分支。两者都不读取.env、不联网。

1.3-A、1.2和0.3的F5调试入口明确使用 `.venv-py312`。1.2正常入口会发真实请求，验收已通过无需重复运行。新电脑没有旧 `.venv`，旧课程 F5 入口需要另行调整或使用新解释器的显式命令，不能假定虚拟环境跟随 Git 复制。Markdown 打开后按 `Ctrl+Shift+V` 查看预览。Continue聊天历史属于本机插件数据，不随此Git仓库同步；可共享的学习证据在项目文档中。

0.1默认入口已由用户恢复为正常material.json。invalid_json.json和missing_region.json均已修复；失败演示使用另存的invalid_json_trailing_comma.json或missing_region_original.json。正常验证也可显式传参：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py project_steps\00_01_material_input\cases\material.json
```

后续换电脑前提交并推送，换电脑后先拉取，再根据锁文件同步环境。新智能体也需读取进度文档，不能从程序成功运行推断你已掌握。
