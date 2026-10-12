"""本课AI边界：配置、消息、模型适配、结构化包装与结果检查。"""

import importlib
import json

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import Runnable
from langchain_deepseek import ChatDeepSeek


# 主入口先加入项目根路径；固定模块名允许复用数字开头的历史课程目录。
# import_module只导入定义，历史main的__name__保护使它不会自动调用API。
# 名称固定，不根据模型或用户输入导入任意模块；本课不要求掌握导入内部实现。
SCHEMA_MODULE = importlib.import_module("project_steps.02_01_card_schema.schema")
CONFIG_MODULE = importlib.import_module("project_steps.01_02_langchain_model.main")
LearningCard = SCHEMA_MODULE.LearningCard
PROMPT_VERSION = "card_json_v1"
EXPECTED_FIELDS = {"summary", "keywords", "evidence_quote", "information_gap"}


def build_messages(text: str) -> list[BaseMessage]:
    """本地构造JSON要求与原文消息，不读取Key或发送请求。"""
    if not isinstance(text, str) or not text.strip() or len(text.strip()) > 2000:
        raise ValueError("材料必须为1—2000个字符。")
    if set(LearningCard.model_fields) != EXPECTED_FIELDS:
        raise ValueError("学习卡字段与已验收结构不一致，先核对2.1字段名。")
    # JSON Schema是描述字段规则的JSON对象，不是模型的生成结果。
    schema_json = json.dumps(LearningCard.model_json_schema(), ensure_ascii=False)
    # 使用现有依据/历史材料约束；JSON模式需明确出现json并给出格式示例。
    instructions = (
        CONFIG_MODULE.SYSTEM_MESSAGE
        + "只输出一个json对象，不输出Markdown或额外说明。"
        + "summary概括原文事实；keywords只提取原文关键词；"
        + "evidence_quote逐字复制原文的一句完整连续文字，不能改写；"
        + "information_gap说明原文没有提供的信息，不补造定义、日期或考试安排。"
        + "来源、归属和材料版本由业务提供，不输出这些额外字段。"
        + "字段规则：" + schema_json
        + '格式示例（仅说明形状，不是原文事实）：'
        + '{"summary":"原文摘要","keywords":["原文关键词"],'
        + '"evidence_quote":"原文完整引句","information_gap":"原文未说明的信息"}'
    )
    return [
        SystemMessage(content=instructions),
        HumanMessage(content=f"请制作材料学习卡。\n<材料>\n{text.strip()}\n</材料>"),
    ]


def build_model(settings: dict[str, str]) -> ChatDeepSeek:
    """创建模型适配对象；此处不发远程请求，Key不进入消息。"""
    return ChatDeepSeek(
        model=settings["DEEPSEEK_MODEL"], api_key=settings["DEEPSEEK_API_KEY"],
        api_base=settings["DEEPSEEK_API_BASE"], timeout=30.0, max_retries=0,
        max_tokens=512, temperature=0,
        extra_body={"thinking": {"type": "disabled"}},
    )


def wrap_model(model: ChatDeepSeek) -> Runnable:
    """返回带invoke的包装器：远程JSON输出+本地Pydantic解析。"""
    # method='json_mode'请求response_format=json_object，不是供应商严格schema保证。
    # include_raw=True保留原消息/解析结果/解析错误，而不直接只返回实例。
    # Runnable只是这个包装器的接口类型；本课不写LCEL管道或Agent。
    return model.with_structured_output(LearningCard, method="json_mode", include_raw=True)


def require_card(result: dict[str, object], material: str) -> LearningCard:
    """检查响应/解析/简单业务约束；通过仍需人工核对事实。"""
    if not isinstance(result, dict):
        raise ValueError("结构化包装器返回格式异常。")
    raw = result.get("raw")
    if (
        not isinstance(raw, AIMessage)
        or not isinstance(raw.content, str)
        or not raw.content.strip()
    ):
        raise ValueError("未取得非空JSON正文。")
    if raw.response_metadata.get("finish_reason") == "length":
        raise ValueError("输出被截断，不当作完整学习卡。")
    if result.get("parsing_error") is not None:
        # 异常对象可能含原始生成内容，不直接打印它。
        raise ValueError("JSON解析或Pydantic字段校验失败，不自动重试。")
    card = result.get("parsed")
    if not isinstance(card, LearningCard):
        raise ValueError("未取得LearningCard实例。")
    for keyword in card.keywords:
        if not keyword.strip():
            raise ValueError("关键词不能只有空白。")
    if card.evidence_quote not in material:
        raise ValueError("引用没有出现在原文中，不展示为合格候选。")
    return card
