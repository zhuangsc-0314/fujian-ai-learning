# 1.5-A：学习目标命令行参数

本次交付是离线预览骨架：公开材料 → 输入目标 → 共享消息函数 → 角色/目标摘要。你独立添加`--goal`，让用户不用改Python常量就能切换目标。本步不读.env、不创建模型、不invoke；真实请求/响应/故障定位集成放到1.5-B。沿用已安装的消息类，无新依赖。

## 两个概念与最小例子

`argparse`是Python标准库的命令行解析器。命名选项可把`--topic "福建省情"`映射为`args.topic`；它也处理`--help`、未知选项和缺值。这比手工按sys.argv位置索引更适合扩展输入。

下面是一个与练习不同的最小例子，可以保存到本机临时文件运行：

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--topic", help="本次复习主题")
args = parser.parse_args()
print(args.topic)
```

用正式Python运行该文件，再带上`--topic "福建省情"`，输出字符串`福建省情`。解析器返回Namespace对象，`.topic`读取它的属性。没有传选项时这个例子输出None；新课另用`set_defaults(goal=...)`保留你原来的目标。

第二个概念是目标与约束各有位置：本次目标进入HumanMessage，SystemMessage继续规定只依据原文、依据不足说明、历史材料不能推定未来规则。用户目标/材料中的命令不能替换System约束。消息角色保留只证明本地构造正确，不能保证模型服从或事实正确。

## 运行与关键代码

在仓库根目录运行，以下全部离线：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py --help
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\verify_cases.py
```

输入→处理→输出：解析器读取命令行 → `args.goal`保存目标 → `read_material`读取固定公开材料 → `build_messages(text, learning_goal=args.goal)`去空白并校验目标 → 构造system/human → 展示目标/字符数/角色。本步没有配置、请求和模型响应，不能说完整六步调用流程已验收。

`main(argv=None, *, lesson=None)`中的`None`让解析器读取实际命令行；测试传列表可离线检查。`*`要求后面的`lesson=`写参数名。共享函数的`learning_goal=`也是关键字参数，省略时沿用1.2目标。`list[str] | None`是类型提示，不替代运行校验。入口`raise SystemExit(main())`把返回值作为进程退出码。

动态导入只为复用既有独立课程文件：`load_lesson()`按路径加载模块，旧文件的`if __name__ == "__main__"`不会触发；导入也不会调用load_settings/invoke。这段辅助语法由助手提供，不是你的本课独立任务，不要求先掌握导入机制。

## 你的独立修改

只修改[main.py](main.py)的`add_goal_argument(parser)` TODO，给已有解析器添加接收字符串的`--goal`，写中文help。默认目标已在外部设定，保留它；无需重新读取argv或改System、材料校验、原1.2目标常量与验证脚本。参考上面的`--topic`例子自行迁移。

完成后运行：

```powershell
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py --goal "列出原文包含的科目"
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\main.py --goal "   "
.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_05a_goal_argument\verify_cases.py --exercise
$LASTEXITCODE
```

正常自定义目标应显示你输入的目标、system/human、请求0并退出0；空白目标应拒绝/退出2。带空格的参数用引号保证作为一个字符串。初始骨架不识别--goal、练习探针退出1，这是TODO未完成的预期，不表示基础失败。

## 通过条件与下一步

正常：默认/自定义目标均有效。非法：未知选项、--goal缺值、空白/301字符目标拒绝。边界：去掉首尾空白后300字符接受；材料2000字符接受、空白/2001字符拒绝；文件/编码错误定位到材料读取。目标和不可信材料只在human，system不变。

功能验收分为基础骨架和用户选项：基础检查通过后提供练习；你完成TODO并通过练习检查后才记目标选项完成。能力验收还需你的独立运行与解释：目标如何从命令行进入HumanMessage；空白目标在哪一步停止。助手验证不等于你掌握。之后协调者根据证据安排1.5-B，不提前生成阶段2。

[任务与实际验证](../../docs/tasks/1.5-a-goal-argument.md) · [官方argparse教程](https://docs.python.org/zh-cn/3.12/howto/argparse.html)（既有标准库，无新增依赖）
