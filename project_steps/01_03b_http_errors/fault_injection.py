"""本地构造真实SDK异常；占位响应不是供应商响应，不生成AI正文。"""

from typing import NoReturn
from unittest.mock import Mock

from openai import AuthenticationError, InternalServerError, RateLimitError


RAW_ERROR_MARKER = "OFFLINE_HTTP_DETAIL_MUST_NOT_BE_PRINTED"


def raise_status_failure(case: str) -> NoReturn:
    """抛出案例对应的SDK异常；未知案例抛ValueError；不联网。"""
    # SDK构造函数需要response.request/status_code/headers。
    # Mock仅承载这些字段，创建它不会发HTTP；本课不展开测试占位细节。
    if case not in ("auth", "rate-limit", "server"):
        raise ValueError("未知教学案例。")

    status_code = {"auth": 401, "rate-limit": 429, "server": 500}[case]
    response = Mock(name="offline_response_placeholder")
    response.request = Mock(name="offline_request_placeholder")
    response.status_code = status_code
    response.headers = {"x-request-id": "offline-example"}
    body = {"message": RAW_ERROR_MARKER}

    if case == "auth":
        raise AuthenticationError(RAW_ERROR_MARKER, response=response, body=body)
    if case == "rate-limit":
        raise RateLimitError(RAW_ERROR_MARKER, response=response, body=body)
    raise InternalServerError(RAW_ERROR_MARKER, response=response, body=body)
