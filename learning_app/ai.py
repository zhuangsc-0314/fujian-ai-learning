"""唯一正式AI边界：模板、配置、供应商、一次请求与脱敏错误。"""

from importlib import import_module
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from openai import APIConnectionError, APIStatusError, APITimeoutError

from learning_app.domain import AppError, LearningCard


legacy = import_module("project_steps.02_02_structured_card.adapter")
PROMPT_VERSION = "stage2_card_v2"


def prepare_prompt_values(material: str, learning_goal: str, schema_json: str) -> dict[str, str]:
    """变量值不再格式化一次；材料中的花括号保留为普通数据。"""
    if not isinstance(material, str) or not 1 <= len(material.strip()) <= 2000:
        raise AppError("invalid_input", "input", "材料须为1—2000字符。")
    if not isinstance(learning_goal, str) or not 1 <= len(learning_goal.strip()) <= 300:
        raise AppError("invalid_input", "input", "学习目标须为1—300字符。")
    return {"material": material.strip(), "learning_goal": learning_goal.strip(),
            "schema_json": schema_json}


def build_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", legacy.CONFIG_MODULE.SYSTEM_MESSAGE +
         "\n只输出符合以下JSON Schema的JSON对象：{schema_json}。"
         "引句必须逐字来自材料；信息缺口明确保留未知。"),
        ("human", "学习目标：{learning_goal}\n<材料>\n{material}\n</材料>"),
    ])


def build_card_chain(prompt: Runnable, structured_model: Runnable) -> Runnable:
    """竖线把上一步输出交给下一步；此处仅组合，不发送请求。"""
    return prompt | structured_model


def classify_failure_stage(error_code: str) -> str:
    return {
        "invalid_input": "input", "config_error": "configuration",
        "live_disabled": "configuration", "upstream_timeout": "invoke",
        "upstream_connection": "invoke", "upstream_http": "invoke",
        "invalid_output": "parse_and_validate",
    }.get(error_code, "unknown")


def generate_card(material: str, learning_goal: str, *, live: bool = False) -> dict:
    """只有显式live=True才读配置和调用模型；不重试、不保存。"""
    values = prepare_prompt_values(
        material, learning_goal, json.dumps(LearningCard.model_json_schema(), ensure_ascii=False),
    )
    if not live:
        raise AppError("live_disabled", "configuration", "未启用真实生成；可选择历史回放。")
    try:
        settings = legacy.CONFIG_MODULE.load_settings()
        structured_model = legacy.wrap_model(legacy.build_model(settings))
    except (ValueError, KeyError, OSError) as exc:
        raise AppError("config_error", "configuration", "模型配置失败；检查本机配置。") from exc
    chain = build_card_chain(build_prompt_template(), structured_model)
    try:
        result = chain.invoke(values)  # 唯一付费请求边界；超时不自动重试。
    except APITimeoutError as exc:
        raise AppError("upstream_timeout", "invoke", "请求超时，执行状态未知；请先检查用量。") from exc
    except APIConnectionError as exc:
        raise AppError("upstream_connection", "invoke", "连接失败；检查网络后手动决定是否重试。") from exc
    except APIStatusError as exc:
        raise AppError("upstream_http", "invoke", "供应商拒绝请求；检查配置或额度。") from exc
    try:
        card = legacy.require_card(result, material)
    except ValueError as exc:
        raise AppError("invalid_output", "parse_and_validate", "生成内容未通过结构/引用检查。") from exc
    return {"card": card.model_dump(), "usage": result["raw"].usage_metadata,
            "attempts": 1, "source_mode": "live", "prompt_version": PROMPT_VERSION}
