# 1.5-B：目标参数贯通与故障定位

本步交付：复用1.5-A的目标参数和1.2的完整调用入口，观察目标到底有没有传到invoke；你独立定位并修复一个漏传故障。不新增依赖或框架。默认离线，真实模式必须显式使用--live，最多一次尝试。

1.5-A中你独立描述了解析命令行→读取材料→拼接目标/材料→HumanMessage，整体方向正确；助手补充“保存的是选项后面的值，本课没有发送模型”。空白目标的raise→except→return 2由助手讲解，不记成你的独立定位。本步不要求重做A的选项实现，而是在完整流程里检查参数和失败位置。

## 为什么现在学习

预览正确只说明预览函数拿到了目标；如果调用下一个函数时没有传目标，下游可能继续使用自己的默认值。以后API接收目标、AI模块生成消息，也有同样的边界。先能检查输入和传参，再学结构化学习卡。

本次只重点练习两个概念：函数间的关键字参数传递；按处理阶段定位故障。patch与超时未知执行是复习，诊断辅助代码无需先全部掌握。

## 输入、处理与输出

```text
命令行 --goal 的值 → argparse → args.goal
→ 预览校验 → run_call → 原1.2 main(learning_goal=...)
→ 输入：read_material
→ 配置：load_settings
→ 消息：build_messages（System约束 / Human目标与材料）
→ 请求：model.invoke
→ 响应：AIMessage
→ 展示：show_response；成功时摘取允许的用量字段
```

前三行属于输入和路由；后面六步复用原入口。读配置和创建模型不等于已发请求；invoke才进入调用边界。尝试1次不证明服务端执行或收费。消息角色正确、stop或结构检查都不能代替原文核对。

## 最小示例与关键语法

```python
def show_topic(*, topic="默认主题"):
    print(topic)

def forward_topic(topic):
    show_topic()  # 忘记传递，上游变量不会自动进入下游函数

forward_topic("福建省情")  # 输出“默认主题”
show_topic(topic="福建省情")  # 输出“福建省情”
```

把示例存到临时Python文件，用正式环境的Python运行即可，不联网。关键字调用中，左侧`topic=`是下游函数的参数名，右侧是传入的值；同名/相似名的局部变量也不会自动共享。

原1.2新增`main(..., learning_goal=LEARNING_GOAL)`，传给`build_messages(text, learning_goal=learning_goal)`；省略时保留默认目标。`*`要求写关键字参数名；`records=None`表示不收集成功记录，启用时列表由原入口填入允许字段，不保存正文/完整响应头/Key。

新课`run_call(lesson, goal, path, *, records=None)`只负责转交数据，不重复配置/异常业务。`lesson`是原课程模块，`.main`读它的函数。返回原入口退出码：0取得可展示正文，2本地输入/配置/初始化失败，1请求或响应处理失败。

## 先观察，再独立修复

在仓库根目录运行，以下全部离线：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\main.py --goal "列出原文包含的科目"
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\main.py --diagnose --goal "列出原文包含的科目"
$LASTEXITCODE
```

预览显示新目标；诊断中的“实际进入invoke的目标”却仍是默认目标。诊断还在invoke处注入APITimeoutError：原入口退出1、show_response不执行。诊断工具自身在目标未贯通时退出1；修复后，目标贯通与预期超时均符合，诊断工具退出0。工具通过不代表API请求成功。

**你的独立TODO：** 只改[main.py](main.py)的run_call调用行，使上游goal进入原main新增的learning_goal参数；保留材料路径和records。不要改默认常量、System约束、诊断/验证脚本。先用输出定位，再改一行；助手没有代做。

修复后运行诊断及检查：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\main.py --diagnose --goal "列出原文包含的科目"
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\verify_cases.py --exercise
$LASTEXITCODE
```

诊断只读取公开材料，配置与模型构造被替换，invoke替身抛SDK超时，socket/DNS被阻断；无.env读取、真实HTTP或模拟回答。检查成功链用固定AIMessage人工数据验证控制流/字段，不把它当供应商回答或事实证据。

## 正常、非法与边界

| 案例 | 应观察到的行为 |
| --- | --- |
| 无参数 | 原默认目标预览正常，无配置读取/真实请求 |
| 自定义目标 | 修复后invoke消息中目标一致，System原文不变 |
| 空白目标/缺值/未知选项 | 本地拒绝，退出2，不到配置或invoke |
| 目标300/301字符 | 去空白后300接受，301拒绝 |
| 正常/空白/超长材料 | 正常可到调用边界，空白/2001字符在输入阶段停止 |
| 不可信材料 | 命令式文本仍为Human数据；只验证角色，不证明模型服从 |
| 离线超时 | 原入口退出1，尝试1、真实HTTP0，无正文/成功记录 |
| 人工空响应 | invoke已返回，但响应处理失败，退出1，不显示成功正文 |

## 真实模式与通过条件

`--live`先用临时替换的原main检查自定义与探针目标有没有收到，不读配置或创建模型。漏传时退出2。检查通过后才读取本机配置并尝试一次真实请求；这只是防误调用保护，不是模型事实或账单验证。

离线练习通过后，你可以显式选择下面的真实运行；只使用既有公开历史材料，可能计费，助手没有运行本命令：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05b_call_flow\main.py --live --goal "列出原文包含的科目"
```

人工核对原文：科目为《综合基础知识》，正文没有列出各题型、未来安排或政策条件，不允许补造。材料出处：[福建省人社厅2023年历史说明](https://rst.fujian.gov.cn/wz/cjwt/zyjsry/zgks/202311/t20231113_6296478.htm)。不要贴Key或完整配置；只提供安全输出。一次失败不自动重跑，先定位步骤。

功能通过条件：基础检查通过，修复后目标贯通练习与诊断通过。能力通过条件：你的独立修复与运行证据，说明为什么预览正确仍可能漏传；用六步流程指出超时停在哪一步、为何没有正文。独立实际输入/配置故障可在后续证据中自然补齐，不把助手替身测试记成你掌握。

尚未通过不提前进入阶段2；协调者根据修复/解释/运行证据判断1.5收尾或补练。无并行修改，不重做已完成A。

[任务分配与实测](../../docs/tasks/1.5-b-call-flow.md) · [1.5-A复习](../01_05a_goal_argument/README.md) · [原调用入口](../01_02_langchain_model/main.py)
