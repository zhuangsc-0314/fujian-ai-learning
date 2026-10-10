# 用户 region 练习：实际代码评审

日期：2026-10-09。评审基线：`e43e9a8` 加用户本地未提交的 main.py 修改。此前 RUN_RESULTS.md 保留为原始示例快照，本记录不覆盖它。

用户独立将 region 加入 required_fields，复用现有非空字符串校验；并将默认案例改为 missing_region.json。助手未修改用户代码。

## 实际运行

使用本机 `.venv` 的 Python 3.10.10，命令形式：

```powershell
.\.venv\Scripts\python.exe -X utf8 project_steps\00_01_material_input\main.py project_steps\00_01_material_input\cases\material.json
```

| 案例 | 预期退出码 | 实际退出码/结果 |
| --- | --- | --- |
| material.json | 0 | 0，字段通过，解释器在 .venv |
| missing_title.json | 2 | 2，定位 title |
| blank_title.json | 2 | 2，定位 title |
| invalid_json.json | 2 | 2，JSON 解析错误 |
| untrusted_text.json | 0 | 0，正文仅展示，模型请求 0 |
| missing_region.json | 2 | 2，定位 region |
| 不存在的文件路径 | 2 | 2，文件错误 |
| region 数字 123 | 2 | 2，定位 region，无 Traceback |
| region 为 null | 2 | 2，定位 region，无 Traceback |
| region 为空格、制表符和换行 | 2 | 2，定位 region |
| region 为空字符串 | 2 | 2，定位 region |
| region 为 false | 2 | 2，定位 region，无 Traceback |

新增五类 region 数据由助手复制正常案例到忽略目录下的临时文件，检查结束自动清除。没有调用模型、读取 Key 或改变用户程序。

额外检查默认无参数入口：实际退出 2，因为默认指向缺 region 的负例。建议用户完成测试后恢复 material.json，使用命令行参数选择负例。`git diff --check` 发现文件尾多余空行；这是提交整理项，不影响业务校验。required_fields 中引号/逗号空格也建议统一。

## 双重结论

- 功能：region 校验及 12 个正常/异常案例通过；默认示例路径与注释/格式仍待用户收尾。
- 能力：已看到用户独立修改证据；对 JSON 解析/业务校验、短路判断与异常传播的解释和调试能力尚待证据，不登记为阶段 0 全部掌握。
- 下一步：用户解释数字 region 为什么不会调用 strip；恢复默认正常输入并整理完成标记，再决定 0.2 或补练。
