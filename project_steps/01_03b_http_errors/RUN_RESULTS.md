# 1.3-B助手本机离线实测

日期：2026-10-11。Python3.12.15、openai3.26.1，依赖/锁文件不变。以下为助手运行，不是用户独立运行或供应商返回。

## 本机接口核对

AuthenticationError和RateLimitError构造签名含message、response、body，均继承APIStatusError；实际读取已安装APIStatusError.__init__，确认所需response.request/status_code/headers及安全字段status_code。辅助占位Mock满足构造所需字段，不是HTTP请求/响应实测。

## 实际入口运行

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\main.py auth
```

实际退出1；输出[教学故障注入]和auth案例，随后：

```text
[认证] HTTP 401：请检查本机认证配置；本课不自动重试。
教学异常注入次数：1；真实模型请求数：0。
```

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\main.py rate-limit
```

实际退出1，输出故障注入说明，随后：

```text
[HTTP失败] 状态码：429；未取得可用回答；请检查服务状态或配置；本课不自动重试。
教学异常注入次数：1；真实模型请求数：0。
```

## 安全检查与未完成项

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\verify_cases.py
```

实际退出1：auth/401、rate-limit/429、server/500安全失败检查通过；缺案例名、非法值、多余参数、不可信值共4项退出2/不注入/不回显检查通过。共7项基础检查通过，请求0、原始标记无泄漏。网络socket哨兵未触发。

实际末行：`限流TODO待完成：分类标记或原因提示未满足约定，请核对实际输出；退出1。`

这不是所有检查通过：用户RateLimitError独立分支尚未实现，TODO探针待验证。用户修改、实际运行与处理原因解释均未取得。本轮未读.env、未创建模型客户端、未调用DeepSeek或OpenAI API、未产生模拟AI正文；真实鉴权/限流、响应体与计费未验证。
