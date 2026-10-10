# 项目任务 0.1：环境与材料输入诊断

本任务对应平台路线的阶段0。一次只推进一个小任务；本次不调用模型、不读取API Key、不安装新依赖。数据归属是本机占位，不是多人可上线版本。

## 1. 本次交付什么

一个可以重复运行的材料入口：输出实际Python解释器，读取JSON，检查必填字段，区分文件/解析/业务错误。数据最终会成为学习卡和题目的输入，目前只验证入口。

## 2. 为什么现在学

材料还没读对时，不能把后续错误都归到模型。你要能知道问题发生在文件路径、JSON语法、字段规则还是模型调用。本次只练前面三层。

## 3. 三个必要概念

- 解释器与虚拟环境（interpreter / venv）：真正运行代码的Python及隔离依赖的目录；看sys.executable确认。
- JSON解析（parsing）：将文件文本转换成Python对象；语法不合法则无法进入后续步骤。
- 业务校验与异常（validation / exception）：JSON合法不代表字段适合材料功能。空标题要单独拒绝。

不要求重学你已会的变量、循环和函数；main.py在首次需要时解释with、类型提示、短路判断、f-string和入口语法。

## 4. 输入、处理、输出及模块关系

cases中的材料文件 → read_material读取JSON → 检查对象和必填字段 → main输出诊断或具体错误。没有模型、数据库或服务器依赖。文本中的命令式语句仍是文本。

material.json使用福建省人社厅历史说明的一句原文节选。其他案例是明确标记的输入测试，不是AI输出。[原始资料](https://rst.fujian.gov.cn/wz/cjwt/zyjsry/zgks/202311/t20231113_6296478.htm)

## 5. 最小程序和运行方式

在VS Code打开main.py，终端从项目根目录运行：

~~~powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py
~~~

不用激活虚拟环境。当前正式环境在0.3建立，为Python3.12.15；旧3.10环境保留。用户已将默认入口恢复为cases/material.json。invalid_json.json和missing_region.json均已由用户修复为合法材料；观察失败时，分别使用另存的invalid_json_trailing_comma.json和missing_region_original.json。

-X utf8仅用于统一中文输入输出编码，避免终端编码不同导致乱码，不改变校验规则。

## 6. 关键代码阅读

先读read_material，再读main，不必从头背代码：

- json.load读文件；不是直接调用模型。
- 类型提示说明意图，不执行自动校验；isinstance检查实际类型。
- get获取不存在的键会返回None；strip检查只有空格的字符串。
- raise ValueError停止不合格输入；try/except根据失败步骤分别反馈。
- JSONDecodeError是ValueError子类，异常捕获顺序有意义。

建议在material = json.load(source_file)和value = material.get(field_name)两处打断点，观察原始JSON与解析后的字典。

## 7. 你独立完成的小修改

0.1核心输入/异常验收已通过，已完成练习注释/格式收尾；下面保留原练习说明，见[最新评审](REVIEW_RESULTS.md)。不能据此登记阶段0整体或其他课掌握。

让region成为必填的非空字符串：缺失、不是字符串、只有空格都要拒绝。保留其他行为，只作最小修改。TODO已经标在main.py里；我没有代做。

完成后独立复制案例，把region改为空格或数字，检查是否被拒绝。不要把现有程序的成功运行登记为“已掌握”。

## 8. 正常、非法与边界案例

从项目根目录，替换最后一个文件名即可：

~~~powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py project_steps\00_01_material_input\cases\missing_title.json
~~~

| 文件/输入 | 教学初版 | 当前用户修改后预期 |
| --- | --- | --- |
| material.json | 成功，显示实际解释器和字段；模型请求0 | 继续成功 |
| missing_title.json | 材料校验错误，指出title | 相同 |
| blank_title.json | 材料校验错误 | 相同 |
| invalid_json.json | JSON解析错误及行列，还未进入字段校验 | 用户补region后JSON合法，成功；保留文件名和修复结果作为练习证据 |
| invalid_json_trailing_comma.json | 后续为保留解析负例另存 | JSON解析错误，尚未进入字段校验 |
| untrusted_text.json | 只显示正文预览，不执行命令 | 相同；这只验证普通程序不执行正文，不代表已实现模型提示注入防护 |
| missing_region.json | 初版缺region，原校验缺口 | 用户补region后成功；保留修复结果 |
| missing_region_original.json | 后续为保留缺字段负例另存 | 材料校验错误，指出region |
| 不存在的文件路径 | 文件错误 | 相同 |

失败退出码2，成功0。PowerShell用$LASTEXITCODE，CMD用echo %ERRORLEVEL%；有非零退出码不一定是代码崩溃，要看具体失败步骤。JSON语法异常在json.load中抛出，经read_material调用向外传播，由main中的except json.JSONDecodeError捕获；这两个步骤并不冲突。

## 9. 双重通过条件

A功能：当前已实现校验与错误分类按表工作；你补上region后，正常数据仍成功，非法region均被拒绝。

B掌握：你能指认实际解释器；解释解析错误与字段错误区别；独立完成region小修改；说出不可信正文经过了哪些步骤、为什么没有被执行。

本轮助手实测记录另存RUN_RESULTS.md。它证明已提供程序的行为，不证明你掌握；你的任务结果要另外提交。

## 10. 做完后发给我

只需要三项，不要发.env或Key：

1. 正常运行输出中的Python路径和虚拟环境结果。
2. 你改动的几行代码，以及missing_region_original和空格region的实际反馈。
3. 用自己的话解释：为什么缺标题能被json.load读出来，却还是不能作为合格材料？不可信正文为什么没有被执行？

我按实际结果决定补练或进入0.2安全配置。若你已掌握，能通过小修改和解释即可跳过重复讲解。

## 已确定的后续Embedding配置

选用百炼qwen3.7-text-embedding，初始1024维。.env和.env.example预留DASHSCOPE_API_KEY、EMBEDDING_API_BASE、EMBEDDING_MODEL、EMBEDDING_DIMENSIONS；Key留给你填写，地址按百炼业务空间和地域控制台填写。缺这两项不妨碍0.1；不在这个任务调用Embedding。

[百炼Embedding官方说明](https://help.aliyun.com/zh/model-studio/embedding?disableWebsiteRedirect=true)
