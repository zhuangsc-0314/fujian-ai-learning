r"""1.3-B：只在本机注入认证/限流等HTTP失败，不读取Key或联网。

运行：.\.venv-py312\Scripts\python.exe -X utf8 project_steps\01_03b_http_errors\main.py auth
先观察已提供的认证分支，再独立完成限流TODO；没有模型回答。
"""

import sys

from openai import APIStatusError, AuthenticationError, RateLimitError

from fault_injection import raise_status_failure


def main() -> int:
    """失败案例返回1；参数非法返回2；不发送真实请求。"""
    # 参数数量和值检查沿用1.3-A，不重复引入解析框架。
    if len(sys.argv) != 2:
        print("用法：运行本课main.py，并传入auth、rate-limit或server。")
        print("未注入异常；真实模型请求数：0。")
        return 2

    case = sys.argv[1]
    if case not in ("auth", "rate-limit", "server"):
        print("案例名不合法：只接受auth、rate-limit或server。")
        print("未注入异常；真实模型请求数：0。")
        return 2

    print("[教学故障注入] 材料解释请求被上游拒绝或返回HTTP失败。")
    print(f"案例：{case}；没有真实网络调用，也不生成模型回答。")
    try:
        # 用本地raise代替真实invoke失败；不创建客户端、不检查真实Key。
        raise_status_failure(case)
    except AuthenticationError:
        # 401对应认证失败。原样重复发送无助于修复失效的认证配置。
        # 固定安全提示不包含Key、原始异常、错误正文或请求对象。
        print("[认证] HTTP 401：请检查本机认证配置；本课不自动重试。")
        return 1

    # TODO 1.3-B（你独立完成）：在通用APIStatusError之前增加限流分支。
    # 捕获已导入的RateLimitError，提示含[限流]、429、检查限制原因，
    # 并明确不自动重试；返回1，不打印原始异常/response/body。
    # 429可能涉及临时频率限制，也可能需处理额度；不能保证等一会就好。
    # 不修改辅助文件或检查规则，不把失败改成成功。
    except APIStatusError as error:
        # as error把捕获的异常对象绑定到变量，供此分支读取安全字段。
        # status_code是SDK保存的HTTP状态码；只显示数字，不打印完整对象。
        # 这是兜底：未完成TODO时429也会匹配这里；500也由这里处理。
        print(
            f"[HTTP失败] 状态码：{error.status_code}；未取得可用回答；"
            "请检查服务状态或配置；本课不自动重试。"
        )
        return 1
    finally:
        print("教学异常注入次数：1；真实模型请求数：0。")


if __name__ == "__main__":
    raise SystemExit(main())
