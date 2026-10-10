# 1.3-A 助手实际离线验证

日期：2026-10-10。本记录为本轮助手运行，不是用户独立练习或供应商返回。

## 环境与接口核对

Python3.12.15、openai3.26.1，依赖声明和uv.lock未改。实际打印APITimeoutError的MRO为：APITimeoutError → APIConnectionError → APIError → OpenAIError → Exception → BaseException → object。两个异常构造签名均要求request字段，辅助文件用标准库Mock作测试占位；不生成HTTP响应或AIMessage。

## 实际运行

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\main.py timeout
```

退出1；实际输出：

```text
[教学故障注入] 业务场景：请求解释材料中的术语，但调用失败。
案例：timeout；没有真实网络调用，也不生成模型回答。
请求失败（连接/超时）：未取得可用响应；服务端执行状态未知；本课不自动重试。
教学异常注入次数：1；真实模型请求数：0。
```

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\verify_cases.py
```

退出1；实际输出：

```text
连接异常安全反馈：通过，退出1，明确未知/不重试/请求0，无原始异常泄漏。
超时异常安全反馈：通过，退出1，明确未知/不重试/请求0，无原始异常泄漏。
缺案例名：通过，退出2，未注入异常，未回显不可信文本。
非法案例名：通过，退出2，未注入异常，未回显不可信文本。
多余参数：通过，退出2，未注入异常，未回显不可信文本。
不可信案例名：通过，退出2，未注入异常，未回显不可信文本。
6项基础检查通过；真实模型请求0，没有模拟AI回答。
独立TODO待完成：超时仍进入通用分支；本脚本退出1，不是假报全部通过。
```

退出1为TODO尚未完成时的预期结果，不能登记整课功能或用户能力通过。6项基础检查使用socket哨兵防止意外联网；没有读取.env、创建真实模型客户端或API调用。

三份Python文件AST解析及.vscode/launch.json的JSON解析实际通过。语法检查没有导入或执行模型调用。此次未执行用户TODO、未演练真实供应商故障/重试、未检查账单；用户完成后需核对修改与新离线结果。
