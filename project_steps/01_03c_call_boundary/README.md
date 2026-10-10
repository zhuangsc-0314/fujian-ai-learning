# 1.3-C：错误能否从invoke传到外层except？

交付目标：离线运行既有1.2入口，验证已写好的错误分支。A/B的本地raise练习通过后，现在把故障放到实际调用位置；保留原目标、提示词和配置逻辑。

当前评审：用户server/500已独立完成；助手8项案例及500探针通过，整体退出0、真实请求0。用户修改/次数解释及纠正后异常传播解释有证据，独立运行日志仍未验证。以下TODO说明保留为练习回顾，不能要求重新实现；完整证据见[任务记录](../../docs/tasks/1.3-c-call-boundary.md)。

本课两个新概念：`patch`像临时换一个零件，离开`with`就恢复；异常传播是内层函数失败后，沿调用栈寻找能接住它的`except`。不要求现在掌握辅助导入器或完整测试框架。

输入：公开短材料、无效占位配置、指定SDK异常。过程：1.2读取/校验 → 创建被替换的模型 → `invoke`抛错 → 原1.2外层`except` → `finally`。输出：安全失败提示、退出1、客户端尝试1。实际网络请求始终0；此处尝试1仅表示到达了被替换的invoke。

最小例子（不联网）：

```python
from unittest.mock import Mock, patch

model = Mock()
with patch.object(model, "invoke", side_effect=ValueError("本地练习")):
    try:
        model.invoke([])
        print("这行不会执行")
    except ValueError:
        print("外层接到了异常")
```

本课运行方法（从仓库根目录；无需Key）：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03c_call_boundary\main.py
$LASTEXITCODE
```

先读main.py的`CASES`，再看`check_case`：`side_effect=error`使调用抛异常；构造异常对象不等于抛异常。`with`管理替换的作用范围，即使抛错也会恢复。`for name, error, expected in CASES`将每个三元素元组解包。`Exception | None`表示异常或无异常的类型提示；参数里的单独`*`要求其后的参数用名称传入，如`text="  "`。

你的独立修改：只在`CASES`增加`server`项，用`InternalServerError`构造状态500，期望`API返回HTTP 500`。这是扩展调用边界覆盖，不是新增except；原1.2的APIStatusError会接住它。其余TODO、原1.2代码和断言保持不动。

案例与通过条件：

| 案例 | 预期 |
| --- | --- |
| 401、429、超时、连接异常 | 各自安全提示，原入口退出1；invoke一次，show_response零次 |
| 空材料、缺Key | 退出2；invoke零次 |
| 初始化ValueError含原始标记 | 退出2；不泄漏标记，invoke零次 |
| 你新增的500 | 通用HTTP 500提示，退出1；最终探针通过 |

骨架7项基础检查通过但脚本退出1是预期：独立server案例还没添加。完成后应看到探针通过及`$LASTEXITCODE`为0。没有正常模型回答案例，本课所有请求案例都故意失败；1.2历史正常输出不重新请求。异常原文/占位Key不可打印，材料命令仍属于HumanMessage中的数据，沿用1.2角色边界。

运行后用自己的话解释：①invoke抛错后，为什么show_response不执行？②为什么原入口报告“尝试1次”，但这个测试真实请求0，也不能推出供应商执行或收费？提供修改与实际输出后再判断补练或进入1.4用量观察。本地测试没有验证LangChain内部HTTP传递、供应商真实错误或计费；不能把模型回答的结构通过当内容有据。
