# 在另一台电脑继续学习

适用于 Windows PowerShell；需要 Git、可创建虚拟环境的 Python、网络，以及这个私有仓库的访问权限。其他操作系统的环境创建命令需要调整，尚未实测。

## 获取当前进度

2026-10-12最新进度入口为`codex/handoff-001-next-session`，继承SYNC-005、2.2及之前课程，包含[下次复习档案](learning/2026-10-12.md)和[新会话交接提示词](NEXT_SESSION_HANDOFF.md)。2.2代码已在[草稿PR #19](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/19)，归档及新会话交接也通过草稿PR交接，尚未合并main。只拉main会看不到近期课程。后续合并授权与结果以任务回执为准。

历史：2026-10-10[汇总PR #6](https://github.com/zhuangsc-0314/fujian-ai-learning/pull/6)已合并main，见[SYNC-003](tasks/SYNC-003-daily-main.md)；这不是近期课程已合并的证据。

首次获取：在你打算存放项目的父目录运行（目标文件夹不存在时）：

```powershell
git clone --branch codex/handoff-001-next-session https://github.com/zhuangsc-0314/fujian-ai-learning.git
cd fujian-ai-learning
git log -1 --oneline
```

已经克隆过：先运行 `git status`，保存并处理自己未提交的修改，不使用强制覆盖或 reset。然后：

```powershell
git fetch origin
git switch codex/handoff-001-next-session
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

用 VS Code“文件 → 打开文件夹”打开实际克隆目录，阅读README、AGENTS、PROJECT_STATUS、LEARNING_PROGRESS和[2026-10-12复习档案](learning/2026-10-12.md)。先复习，再打开project_steps/02_02_structured_card/main.py完成describe_information_gap的独立展示TODO；2.1核心验收已通过，不重做该字段修改。2.2展示/解释与用户运行待验收，不把助手真实调用当用户掌握。

本机解释器使用`.venv-py312`。在项目根目录可先运行离线预览与练习检查：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\02_02_structured_card\verify_cases.py --exercise
$LASTEXITCODE
```

TODO尚未完成时预计预览退出0、18项基础通过但练习探针退出1；修改后须看实际结果，不能仅凭预览成功判断掌握。以上命令不读.env、不请求模型；不要为复习加--live。1.1/1.2正常入口会真实请求，已通过无需重复。新电脑没有旧.venv，不假定虚拟环境随Git复制。Markdown打开后按Ctrl+Shift+V查看预览。Continue聊天历史属于本机插件数据，不随此Git仓库同步；可共享学习证据在项目文档中。

0.1默认入口已由用户恢复为正常material.json。invalid_json.json和missing_region.json均已修复；失败演示使用另存的invalid_json_trailing_comma.json或missing_region_original.json。正常验证也可显式传参：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py project_steps\00_01_material_input\cases\material.json
```

后续换电脑前提交并推送，换电脑后先拉取，再根据锁文件同步环境。新智能体也需读取进度文档，不能从程序成功运行推断你已掌握。
