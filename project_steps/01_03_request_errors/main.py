r"""1.3第一小步：练习材料解释请求失败后的异常分类。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03_request_errors\main.py timeout
本文件只做明确标记的教学故障注入，不读取.env，不发送API请求。
它不生成AI回答；1.2的真实调用入口及用户目标保持原样。
"""

import sys

from openai import APIConnectionError, APITimeoutError

from fault_injection import raise_request_failure


def main() -> int:
    """运行一个离线失败案例：1表示注入的请求失败，2表示参数不合法。"""
    # 命令行参数是运行时从终端传入的值，本课补讲见COMMAND_LINE.md。
    # 例如：python -X utf8 本课main.py timeout。
    # sys.argv是字符串列表：[脚本名/路径, 'timeout']，长度为2。
    # argv[0]是脚本名，argv[1]是第一个用户参数；下标从0开始。
    # python.exe和脚本名前的-X utf8由解释器处理，不进入这个列表。
    # 本轮不再读取材料/Key；案例名只控制抛哪种异常，不是用户提示词。
    # 本课要求恰好1个用户参数，加上脚本名共2项，所以检查!=2。
    # 不传timeout/connection时列表只有脚本名，长度为1，没有argv[1]。
    # 先检查数量并return，再读取argv[1]，避免下标越界IndexError。
    if len(sys.argv) != 2:
        print("用法：运行本课main.py，并传入timeout或connection。")
        print("未注入异常；真实模型请求数：0。")
        return 2

    # 赋值把第1项字符串保存为case；它不是自动传给main()的函数参数。
    # timeout和connection是由本程序自己解释的案例名，不是Python关键字。
    case = sys.argv[1]
    # 只接受两个固定值；非法输入不回显、不执行、不传给模型。
    if case not in ("timeout", "connection"):
        print("案例名不合法：只接受timeout或connection。")
        print("未注入异常；真实模型请求数：0。")
        return 2

    print("[教学故障注入] 业务场景：请求解释材料中的术语，但调用失败。")
    print(f"案例：{case}；没有真实网络调用，也不生成模型回答。")
    try:
        # 真正调用时，异常可能来自1.2的model.invoke(messages)。
        # 这里用辅助函数在同一try位置直接抛SDK异常，只练习失败分支。
        # 点进辅助文件能看到raise，没有ChatDeepSeek客户端或HTTP发送。
        raise_request_failure(case)

    # TODO 1.3-A（你独立完成）：在下方连接异常分支之前，
    # 增加一个单独捕获APITimeoutError的except分支。
    # 输出必须说明：[超时]、服务端执行状态未知、本课不自动重试；返回1。
    # 不打印原始异常/请求对象，不把失败改成成功，不改fault_injection.py。
    # 原因提示：超时是连接错误的子类，except只执行第一个匹配分支。
    # 当前通用分支的提示安全但不够具体；它没有声称超时等于没执行。
    except APIConnectionError:
        print(
            "请求失败（连接/超时）：未取得可用响应；"
            "服务端执行状态未知；本课不自动重试。"
        )
        return 1
    finally:
        # return或抛异常时都会执行；这里说的是本地教学注入次数。
        # 不把这次本地抛错登记为一次真实请求、一次扣费或供应商故障。
        print("教学异常注入次数：1；真实模型请求数：0。")


if __name__ == "__main__":
    # 运行失败案例退出1是预期行为，不意味着模型成功返回了回答。
    # 被verify_cases导入时不会自动执行；离线脚本单独检查返回值。
    raise SystemExit(main())
