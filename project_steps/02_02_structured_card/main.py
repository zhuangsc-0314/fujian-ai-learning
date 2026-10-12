r"""2.2：真实结构化生成；默认仅预览，--live才读取.env并尝试一次请求。"""

import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

from langchain_core.messages import AIMessage
from openai import (
    APIConnectionError, APIStatusError, APITimeoutError, AuthenticationError, RateLimitError,
)


# 固定项目根路径供适配器复用课程定义，不读取任意外部路径。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import adapter  # noqa: E402


MATERIAL_PATH = PROJECT_ROOT / "project_steps" / "01_01_first_sdk_call" / "material.txt"


def describe_information_gap(card: adapter.LearningCard) -> str:
    """用户独立展示已解析实例中的信息缺口，不从raw正文取值。"""
    # TODO 2.2：返回“信息缺口：”加上card实例中的information_gap。
    # 不硬编码原文缺口，不使用raw.content代替字段，不修改验证脚本。
    return "信息缺口：待用户展示"


def main(argv: list[str] | None = None) -> int:
    """预览/候选成功0，本地错误2，请求或结果处理失败1。"""
    parser = argparse.ArgumentParser(description="结构化学习卡；默认不请求模型。")
    parser.add_argument("--live", action="store_true", help="尝试一次真实DeepSeek请求")
    args = parser.parse_args(argv)
    attempts = 0
    started = None
    stage = "材料/字段检查"
    try:
        text = adapter.CONFIG_MODULE.read_material(MATERIAL_PATH)
        messages = adapter.build_messages(text)
        print(f"材料{len(text)}字符；消息system/human；字段{len(adapter.EXPECTED_FIELDS)}个。")
        if not args.live:
            print("默认预览：JSON要求和字段已构造，未读取.env、未创建模型或请求。")
            print("确认后显式使用--live；公开历史材料不代表未来考试规定。")
            return 0
        stage = "配置检查"
        settings = adapter.CONFIG_MODULE.load_settings()
        stage = "模型与结构化包装器初始化"
        model = adapter.build_model(settings)
        structured_model = adapter.wrap_model(model)
        # 前面的步骤只在本机准备。包装器.invoke底层才调用模型并解析返回内容。
        stage = "模型请求/结构化解析"
        print("正在尝试一次真实结构化请求；自动重试关闭，可能计费。")
        attempts = 1
        started = perf_counter()
        result = structured_model.invoke(messages)
        # result是dict；raw是AIMessage，parsed成功时是LearningCard，错误另存字段。
        if not isinstance(result, dict):
            raise ValueError("结构化返回不是预期字典。")
        raw = result.get("raw")
        if isinstance(raw, AIMessage):
            usage = raw.usage_metadata or {}
            print(f"返回结束原因：{raw.response_metadata.get('finish_reason', '未知')}")
            print("token用量：", {
                name: usage.get(name) for name in ("input_tokens", "output_tokens", "total_tokens")
            })
            print("用量None表示未知，不等于0或免费；未核对实际账单。")
        print("本地解析状态：", "失败" if result.get("parsing_error") is not None else "完成")
        stage = "响应/字段/引用检查"
        card = adapter.require_card(result, text)
        print("解析对象类型：", type(card).__name__)
        record = {
            "owner_user_id": "local_demo_user",
            "material_version_id": "fujian_2023_exam_note_v1",
            "prompt_version": adapter.PROMPT_VERSION,
            "review_status": "pending_manual_review",
            "card": card.model_dump(),
        }
        print(json.dumps(record, ensure_ascii=False, indent=2))
        print(describe_information_gap(card))
        print("这是模型候选，须逐项核对原文；未保存，无真实认证/多人隔离。")
        return 0
    except (OSError, UnicodeError):
        print(f"{stage}读取失败：检查文件/编码/权限；不回显原始内容。")
        return 2 if not attempts else 1
    except AuthenticationError:
        print("API认证失败：检查本机Key，不自动重试。")
        return 1
    except RateLimitError:
        print("API请求受限：检查额度/频率，不自动重试。")
        return 1
    except APITimeoutError:
        print("API超时：服务端执行/收费可能未知，不自动重试。")
        return 1
    except APIConnectionError:
        print("API连接失败：检查网络/代理，不回显原始请求。")
        return 1
    except APIStatusError as error:
        print(f"API返回HTTP {error.status_code}，未完成学习卡，不自动重试。")
        return 1
    except ValueError as error:
        if stage in ("材料/字段检查", "响应/字段/引用检查"):
            print(f"{stage}失败：{error}")  # 本课固定业务提示，无原始Key/解析异常。
        else:
            print(f"{stage}失败：检查该步骤的输入；不回显原始异常。")
        return 1 if attempts else 2
    finally:
        print(f"模型调用尝试数：{attempts}；自动重试：关闭。")
        if started is not None:
            print(f"调用及结果处理耗时：{perf_counter() - started:.2f}秒。")


if __name__ == "__main__":
    raise SystemExit(main())
