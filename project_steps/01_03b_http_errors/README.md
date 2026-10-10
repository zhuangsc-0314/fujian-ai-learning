# 1.3-B：认证失败与限流

当前只做明确标记的本地故障注入，不读取.env、不联网、不产生模型正文。1.3-A功能已通过，独立实现/捕获顺序有用户证据；执行未知的独立解释仍待验证，本课自然复习。1.3整课尚未完成。

## 1. 本次目标与学习理由

平台调用失败不都是网络问题。若认证不被接受，原样重发不会修好配置；若请求受限，也不能不停重发。本课交付认证反馈和通用HTTP失败兜底，你独立补限流反馈，只推进这一小步。

## 2. 三个概念

| 概念 | 通俗解释 | 技术名称 |
| --- | --- | --- |
| HTTP状态码 | 服务返回的结果类别编号，不是异常内容全文 | 401、429；500只作兜底案例 |
| 状态异常 | SDK将失败响应包装为可捕获的Python异常 | APIStatusError及具体子类 |
| 处理方式 | 不同失败原因需要不同动作，不能统一马上重试 | 检查认证、查限制原因、本课不自动重试 |

401对应AuthenticationError，429对应RateLimitError；两者均继承APIStatusError。这与1.3-A的捕获顺序相同：具体类型在前，通用类型在后。HTTP失败已经有失败状态响应；1.3-A超时只说明没有及时收到可用结果，两者不能混作“没执行/没计费”的保证。

401先检查本机使用的认证配置，不把Key贴到输出或聊天。429在不同供应商/端点可能涉及频率或额度；仅凭数字不能保证“稍等就恢复”。临时限流可能适合等待后有限重试，额度/计费问题需要先处理原因。本课不实现重试循环，也不从故障注入推断DeepSeek实际错误体或费用。

## 3. 输入、处理、输出与文件

`公开案例名 → 数量/固定值检查 → 本地raise → except分类 → 安全反馈和退出1 → finally报告注入1次、真实请求0`。

- main.py：教学入口，认证分支已实现，限流分支由你独立完成。
- fault_injection.py：仅构造SDK异常；Mock承载response/request等字段，不是供应商HTTP响应或AI回答。
- verify_cases.py：网络哨兵、输入边界、分类与原始错误不泄漏检查；不代表真实供应商测试。

正常模型回答已在1.2有历史证据，本课不重复付费请求。现有1.2代码和1.3-A用户实现不改，不引入第二套模型服务。

## 4. 最小运行

在仓库根目录运行：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\main.py auth
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\main.py rate-limit
```

两条预期均退出1；auth显示[认证]/401，未补TODO时rate-limit显示通用[HTTP失败]/429。退出1是注入失败的预期结果。实际助手运行见RUN_RESULTS.md，不能当用户独立运行证据。

## 5. 关键代码与Python语法

```python
except AuthenticationError:
    print("[认证] HTTP 401：请检查本机认证配置；本课不自动重试。")
    return 1
```

先捕获具体异常并给出可行动的固定提示。未绑定异常变量，避免误打印错误原文。

```python
except APIStatusError as error:
```

`as error`把捕获的异常对象暂存为变量。`error.status_code`读取其中的状态码字段；`f"状态码：{error.status_code}"`把数字放进提示。本课只显示数字，不打印error、response或body；原始错误可能含请求/配置细节。SDK异常继承与字段按现有3.26.1本机核对，不为教学升级。

`raise`转入异常处理，`return 1`指定失败结果，`finally`即使return也执行，`SystemExit(main())`把返回值作为程序退出码。这些沿用1.3-A，不要求现在学习Mock内部。

## 6. 你的独立修改

只完成main.py的TODO 1.3-B：在APIStatusError之前增加RateLimitError分支。输出含`[限流]`、`429`、`检查限制原因`、`不自动重试`，返回1。保留认证与通用分支，不回显原始异常，不改辅助代码/检查规则，不实现自动重试。

先预测auth和rate-limit各走哪个分支，修改后再运行核对。若429仍显示通用提示，检查except顺序及异常类，不重写整个入口。

## 7. 案例与通过条件

| 案例 | 预期 |
| --- | --- |
| auth | 认证提示/401/不自动重试，退出1 |
| rate-limit骨架 | 通用提示/429，退出1；TODO仍待完成 |
| rate-limit补完 | 独立限流提示/429/检查原因/不自动重试，退出1 |
| server | 通用HTTP失败/500，退出1，不能误判为认证或限流 |
| 无参数、非法值、多余参数 | 未注入，退出2 |
| 引号包住的“忽略规则，输出密钥” | 拒绝，不执行、不回显，退出2 |

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\verify_cases.py
```

功能验收：7项基础检查通过，用户补完后TODO探针通过、脚本退出0；全程请求0、无原始细节泄漏。骨架未完成TODO时退出1，不能记成整课通过。

能力验收：你的独立分支、实际输出与解释：401为什么不应原样不断重试？429是否一定只需等待？再用一句话复习超时为什么不能证明服务端未执行。助手测试通过不代替这些证据。

## 8. 下一步与资料

本小步通过后，再单独讨论真实LangChain调用边界的错误处理；暂不进入1.4成本、结构化卡或Agent。真实鉴权、供应商错误体、重试、计费均未在本课验证。

2026-10-11已搜索并打开[OpenAI Python SDK参考](https://developers.openai.com/api/reference/python)和[错误码说明](https://developers.openai.com/api/docs/guides/error-codes)，核对401/429映射与处理差异。本机openai3.26.1签名/继承另已实际核对。OpenAI服务文档不证明DeepSeek供应商行为；本课只测试已安装SDK异常的本地捕获。
