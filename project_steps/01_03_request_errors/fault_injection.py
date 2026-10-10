"""教学故障注入辅助：只抛真实SDK异常类型，不伪造模型回答。

本轮先读main.py。Mock只承载异常对象需要的request字段，
不是模型、HTTP响应或API Key；无需为了本课先学测试框架。
"""

from typing import NoReturn
from unittest.mock import Mock

from openai import APIConnectionError, APITimeoutError


RAW_ERROR_MARKER = "OFFLINE_ERROR_DETAIL_MUST_NOT_BE_PRINTED"


def raise_request_failure(case: str) -> NoReturn:
    """按案例抛SDK异常；未知案例抛ValueError；从不联网或正常返回。"""
    # NoReturn表示这个函数总以异常结束，没有正常返回值。
    # 真实SDK异常保存request对象；这里用明确的测试占位对象承载字段。
    # 创建Mock不会发送HTTP，也没有任何真实凭证或用户材料。
    request = Mock(name="offline_request_placeholder")
    if case == "timeout":
        raise APITimeoutError(request=request)
    if case == "connection":
        raise APIConnectionError(message=RAW_ERROR_MARKER, request=request)
    raise ValueError("未知教学案例。")
