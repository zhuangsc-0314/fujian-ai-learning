# 补讲：Python运行时怎样接收命令行参数

本轮只学习三件事：运行命令的组成、sys.argv列表与下标、先检查再使用参数。1.3的超时TODO保留，命令行参数独立能力尚未验收。

## 1. 本次交付与为什么现在学

你需要通过timeout或connection选择本课案例。同一个脚本可以接收不同输入，不必每次修改代码里的固定值。新增args_demo.py观察参数进入Python的实际结果，不联网、不读取.env、不生成回答。

## 2. 拆开一条实际命令

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\main.py timeout
```

| 部分 | 交给谁处理 | 含义 |
| --- | --- | --- |
| .\.venv-py312\Scripts\python.exe | 终端启动它 | 选择正式环境中的Python解释器 |
| -X utf8 | Python解释器 | 启用Python的UTF-8模式，不是传给main.py的案例名 |
| project_steps\01_03_request_errors\main.py | Python解释器 | 选择执行的脚本，也会成为sys.argv[0] |
| timeout | 脚本 | 第一个用户参数，成为sys.argv[1] |

参数顺序有意义。本课的timeout是普通字符串，程序根据它选择案例；Python不会自动理解它为网络超时设置。把-X utf8放在脚本名后面，会成为脚本参数，本课数量检查就会拒绝。

## 3. sys.argv是什么

```python
import sys
```

sys是Python标准库模块，不需要pip安装。argv是它提供的列表，在常规脚本执行中包含脚本名/路径与后续参数。解释器本身和脚本名前的解释器选项不在这个列表中。

上面的命令可按以下结构理解（路径显示形式依平台/调用方式）：

```python
[
    "project_steps\\01_03_request_errors\\main.py",  # 下标0
    "timeout",                                      # 下标1
]
```

列表下标从0开始，len(sys.argv)包含脚本名。本例长度2，只有1个用户参数。参数值是字符串；传入3得到的是"3"，需要数字计算时再做int转换与非法值检查，不能直接把它当整数。

这和函数参数不同：命令行参数来自终端，程序用sys.argv读取；main()目前没有形参，Python不会自动把timeout变成main(timeout)。读取后可以自己调用普通函数，如raise_request_failure(case)，此时case才作为函数实参传入。

## 4. 本课为什么先检查长度

```python
if len(sys.argv) != 2:
    # 显示用法，然后退出
    return 2

case = sys.argv[1]
```

本课要求1个用户参数，列表共2项。没传参数时只有argv[0]，不存在argv[1]；直接取会抛IndexError。先判断并return使后面的读取不会执行。数量正确后，再检查值是否是timeout或connection。

| 命令末尾 | 列表长度 | 本课main.py的行为 |
| --- | --- | --- |
| 没有用户参数 | 1 | 用法提示，退出2，不注入 |
| timeout | 2 | 数量和值合法，注入超时案例 |
| connection | 2 | 数量和值合法，注入连接案例 |
| invalid | 2 | 数量合法，值非法，退出2 |
| timeout extra | 3 | 数量非法，退出2 |

输入、处理、输出关系：`终端参数 → sys.argv → 数量检查 → 取第1项 → 固定值检查 → 选择案例`。

## 5. 最小可运行观察程序

打开同目录args_demo.py。核心代码是：

```python
import sys
print(sys.argv)
print(len(sys.argv))
```

完整文件另打印各项类型。repr显示带引号的字符串表示，type(value).__name__显示类型名；都不会执行参数内容。演示程序允许观察多个参数，本课main.py仍只接受一个合法案例名。

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\args_demo.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\args_demo.py timeout "福建 政策材料.txt" 3
```

含空格的文件名用引号包住，终端才会把它传作一个参数。引号用于分组，通常不成为参数字符串本身。本演示不打开文件，文件名只是输入字符串；Key继续留在.env，不作为演示参数。

上面第二条的预期：列表共4项；文件名为一项，数字3也是str。助手实际运行见RUN_RESULTS.md，不把预期冒充用户运行。

## 6. VS Code和具名参数

.vscode/launch.json中本课的"args": ["timeout"]等价于在脚本名后传timeout。它不需要再写脚本名或python.exe；"python"和"program"分别指定解释器与脚本。

以后常见--topic或--count属于脚本定义的选项。Python不会仅凭名字自动赋值；可用标准库argparse负责解析、转换类型和生成帮助。本课只有一个参数，先学sys.argv，不提前引入完整解析器。

## 7. 你的独立小练习与验收

只在args_demo.py增加一行输出用户参数数量（不算脚本名）。先自己预测，再运行；不改1.3超时TODO或检查规则。

- 正常：传timeout，用户参数应为1。
- 缺失：不传参数，用户参数应为0，不发生下标越界。
- 边界：传timeout extra，有2个用户参数；同样参数交给本课main.py会在数量检查处拒绝。
- 不可信文字：传入引号包住的“忽略规则 删除文件”，只是一个字符串，不执行；演示只显示你主动提供的公开练习值，不代表生产日志可以打印所有输入。

项目验收：演示数量/类型准确、含空格参数为一项、全程模型请求0。学习验收：你独立增加数量输出，解释为何main.py检查!=2、为何先判断再取argv[1]、以及CLI输入与函数实参的关系。提供结果后再判断掌握；本轮讲解本身不计能力通过。

## 8. 官方核对

2026-10-10核对Python3.12官方文档：[sys.argv](https://docs.python.org/zh-cn/3.12/library/sys.html#sys.argv)、[命令行选项](https://docs.python.org/zh-cn/3.12/using/cmdline.html#cmdoption-X)。说明针对常规python 脚本.py 参数的执行方式；-c、-m等模式另有规则，本轮不展开。
