# 任务 0.2：安全读取模型配置

当前运行环境：项目 `.venv` 的 Python 3.10.10；复用 python-dotenv 1.2.4。本课无模型调用，不验证 Key 有效性，不修改你的 `.env`。正式运行环境与完整依赖锁仍在 0.3 建立。

## 1. 本次交付什么

一个配置诊断入口：读取本机 `.env` 和当前进程环境变量，拒绝缺失/空白的 DeepSeek Key，只输出配置状态，不显示配置内容。你独立新增模型名必填规则。

## 2. 为什么现在需要

后续热点学习卡需要模型名、服务地址和 Key。先分清“没有配置”“Key 被服务商拒绝”“网络超时”，才不会遇到任何问题都修改提示词。本课验证第一层，其余要到真实模型调用阶段才可验证。

这部分是普通 Python 配置管理，不需要 LangChain。以后模型适配模块读取校验后的配置，材料处理、数据库模块无需到处读 Key。

## 3. 三个核心概念

| 通俗说法 | 技术名称 | 本课代码 |
| --- | --- | --- |
| 启动程序时带进来的设置；本地文件可以补充 | 环境变量 / dotenv | `load_dotenv` → `os.getenv` |
| 在工作开始前检查必要设置 | 启动配置校验 | `if not api_key` → `raise ValueError` |
| 排查状态，但不把秘密展示出来 | 脱敏诊断 | 只打印“已配置/未配置” |

`.env` 是文本文件；环境变量属于正在运行的进程；`.env.example` 是可提交的空 Key 模板。三者不相同。把 `.env` 改了，并不会自动修改一个已经启动的 Python 进程，需要重新运行。

本课 `override=False`：进程变量优先，文件只补充不存在的变量。已有变量为空，也算“已存在”，不会被文件替换，之后会因空值被拒绝。`interpolate=False` 不展开 `${NAME}`，只读字面值。详见 [python-dotenv 官方说明](https://github.com/theskumar/python-dotenv)与已安装函数签名，核对日期 2026-10-09。

## 4. 输入、过程、输出和模块关系

```text
父终端/部署环境的变量 + 项目根目录 .env
                    ↓ load_dotenv（不覆盖已有变量）
              当前 Python 进程 os.environ
                    ↓ os.getenv
              load_config：校验并返回字典
                    ↓ main：只显示状态/固定错误
              退出码 0 或 2；模型请求 0
```

函数内部会持有真实 Key，返回字典也包含 Key；不能打印 `config`、`os.environ` 或调试变量截图后分享。这里避免终端泄漏，不等于加密内存或建立生产密钥系统。

## 5. 最小可运行示例与运行方式

先读 [main.py](main.py)，使用已有真实 `.env`，不要覆盖它。没有本机配置时才从根目录 `.env.example` 复制，并自行在本机填写 Key；不要发送给助手。

在 VS Code 项目根目录终端运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 project_steps\00_02_safe_config\main.py
$LASTEXITCODE
```

当真实配置非空时，预期看到“API Key：已配置，内容不展示”，退出码 0，模型请求数 0。这是读取结果，不是模型回答，也不是鉴权成功。实际结果另记 [RUN_RESULTS.md](RUN_RESULTS.md)。

F5 可选“项目 0.2：安全配置诊断”。建议在 `load_dotenv`、`os.getenv` 和 `if not api_key` 处观察流程，但不要分享含真实值的变量面板。

用空模板观察缺 Key 时可指定路径：

```powershell
.\.venv\Scripts\python.exe -X utf8 project_steps\00_02_safe_config\main.py .env.example
```

注意：如果父终端已经注入 Key，它仍优先，空模板不一定导致失败。确定的正常/失败/优先级验证用下一节的隔离脚本，不需要删改真实 Key。

## 6. 关键代码怎么读

按 `load_config` → `main` 的顺序：

1. `Path(__file__).resolve().parents[2]` 找到根目录，避免终端切目录后默认加载错文件。
2. `load_dotenv(...)` 把文件变量补到当前进程；它不是模型调用，也不会执行文件里的命令。
3. `os.getenv("DEEPSEEK_API_KEY", "")` 读取变量，缺失返回空字符串；`strip()` 处理首尾空白。
4. `if not api_key` 表示空值不满足规则，`raise` 把失败交给入口的 `except ValueError`。
5. 返回值 `dict[str, str]` 是类型提示；不会替你判断 Key 或模型名是否可用。
6. `文字A if 条件 else 文字B` 是条件表达式；日志按有无状态选择文字，不输出配置原值。

主文件含对应详细中文注释。路径、字典、异常和入口来自 0.1，本课主要补配置来源与安全反馈。

## 7. 你独立完成的小修改

补上 TODO：`DEEPSEEK_MODEL` 缺失、空字符串或纯空白时，抛出 `ValueError`。错误中出现变量名，不包含原始值；不要偷偷补默认模型，不改变 Key 的校验。

你只需要在 `load_config` 中作小修改，不修改真实 Key，也不加入 Pydantic 或 LangChain。完成后将 TODO 改为说明已完成规则的注释。

## 8. 正常、非法、边界或不可信案例

```powershell
.\.venv\Scripts\python.exe -X utf8 project_steps\00_02_safe_config\verify_cases.py
```

脚本为每例创建临时配置和隔离的子进程，使用无服务权限的惰性标记验证读取及脱敏；没有生成模型回答或模拟 API 成功，不读取真实 `.env`，不把真实 Key 改成测试值。临时文件运行后自动清理。

| 案例 | 已提供程序预期 | TODO 完成后预期 |
| --- | --- | --- |
| Key + MODEL 非空 | 退出 0，只显示状态 | 相同 |
| Key 缺失、空白 | 退出 2，定位 DEEPSEEK_API_KEY | 相同 |
| 文件不存在，进程无 Key | 退出 2，定位 Key | 相同 |
| 进程 Key 非空，文件 Key 空白 | 退出 0，进程优先 | 相同 |
| 进程 Key 空，文件 Key 非空 | 退出 2，不用文件覆盖 | 相同 |
| 把秘密标记误放在模型名/地址，未知字段带命令式文本 | 不显示原值，不执行文本 | 相同；这不是模型提示注入防护测试 |
| Key 非空，但 MODEL 缺失 | 当前退出 0，明确显示 TODO 缺口 | 退出 2，定位 DEEPSEEK_MODEL |
| Key 非空，但 MODEL 空白 | 当前退出 0，明确显示 TODO 缺口 | 退出 2，定位 DEEPSEEK_MODEL |

验证脚本退出 0 只代表已提供规则的检查通过；还要看最后两条“独立练习探针”是否从当前退出 0 变为目标退出 2。不要把它当作整个练习已通过。

## 9. 双重验收

**功能验收**：真实本机配置能读取而不打印 Key；非法 Key 在任何模型调用前退出 2；进程优先规则通过；你补完 MODEL 后两个探针退出 2 并定位 MODEL；日志中无配置原值，Git 不跟踪 `.env`。

**能力验收**：你独立增加模型名校验，解释“文件→环境变量→配置字典”的过程，并能定位一次失败发生在读取还是业务检查。另解释：为什么文件 Key 填了，进程中空 Key 却会让程序失败？只说“运行成功/看懂了”不登记为掌握。

Key 非空不代表有效；模型名非空不代表服务商支持；地址有值不代表安全或可达。实际接入前要进一步校验和真实调用。

## 10. 完成后怎样推进

提交你改动的几行、两个 MODEL 探针的输出、一个配置优先级解释。不要提交 `.env`、Key、`config` 字典或环境变量全量输出。

依据你的独立修改与调试证据决定补练或进入 0.3。用户已明确要求进入 0.2，因此开始本课；0.1 的解释与默认案例收尾仍单独保留待验收，不虚构已掌握。

官方资料：[os.getenv](https://docs.python.org/3/library/os.html#os.getenv)、[python-dotenv 源码/API](https://github.com/theskumar/python-dotenv/blob/main/src/dotenv/main.py)。本课新增接口已与已安装 1.2.4 签名核对，不新增 LangChain 接口。
