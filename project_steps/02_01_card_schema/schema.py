"""学习卡候选的字段规则；这里的model是数据模型，不是大语言模型。"""

from pydantic import BaseModel, ConfigDict, Field


class LearningCard(BaseModel):
    """最小候选卡：只约束字段，不保证摘要忠实或可供多人使用。"""

    # class定义一种对象的规则，LearningCard是类名。
    # (BaseModel)表示继承Pydantic的字段读取/校验/导出能力，不需要自己写__init__。
    # strict=True拒绝本课不合类型的输入，不依赖自动类型转换。
    # extra='forbid'拒绝未声明字段；str_strip_whitespace先去字符串首尾空白。
    model_config = ConfigDict(strict=True, extra="forbid", str_strip_whitespace=True)

    # 冒号后的str是字段类型；Field给出额外约束，没有默认值就必须提供。
    # 普通Python类型提示不自动校验；本类在model_validate时由Pydantic执行校验。
    summary: str = Field(min_length=1, max_length=300)
    # list[str]表示列表且各项为字符串；这里的长度约束限制列表项数。
    keywords: list[str] = Field(min_length=1, max_length=5)
    evidence_quote: str = Field(min_length=1, max_length=400)
    # 用户独立字段已通过：必填字符串，去首尾空白后1—200字符。
    information_gap: str = Field(min_length=1, max_length=200)
