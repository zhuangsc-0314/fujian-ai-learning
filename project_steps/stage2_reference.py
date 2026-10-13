"""14课共用的离线参考演示，所有数据注明来源；不读.env、不请求模型。"""

import argparse
import json
from pathlib import Path

from langchain_core.runnables import RunnableLambda
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

from learning_app.ai import build_card_chain, build_prompt_template, prepare_prompt_values
from learning_app.domain import (
    AppError, LearningCard, build_acceptance_report, build_material_context,
    decide_review_status, describe_publication_date, locate_quote,
)
from learning_app.history import historical_material
from learning_app.service import CandidateStore, generate_candidate
from learning_app.storage import Base, database_url, probe_database


def run_reference(lesson_id: str, title: str) -> int:
    """默认演示已实现的行为；--exercise检查参考代码，不登记用户能力。"""
    parser = argparse.ArgumentParser(description=f"{lesson_id} {title}：完整参考演示")
    parser.add_argument("--exercise", action="store_true", help="运行参考案例，不等于用户独立验收")
    parser.add_argument("--database", action="store_true", help="显式检测本机开发PG连接")
    args = parser.parse_args()
    print(f"{lesson_id} {title} / 完整参考代码；助手演示不代表用户掌握。")
    if args.database:
        try:
            print("PostgreSQL连接实测：", probe_database(database_url()))
        except AppError as error:
            print(f"[{error.stage}] {error.message}")
            return 1
        return 0
    text = historical_material()
    if lesson_id == "2.3-A":
        for supported, conflict in [(True, False), (False, False), (None, None)]:
            print(supported, conflict, "→", decide_review_status(
                all_claims_supported=supported, has_time_conflict=conflict,
            ))
    elif lesson_id == "2.3-B":
        print("人工练习材料：😀中文，中文")
        print("正常/重复：", locate_quote("😀中文，中文", "中文"))
        print("不存在：", locate_quote("原文", "没有"))
        try:
            locate_quote("原文", " ")
        except ValueError:
            print("非法空引句：已明确拒绝")
    elif lesson_id in {"2.4", "2.5"}:
        values = prepare_prompt_values(text, "整理范围；未知保持未知。",
                                       json.dumps(LearningCard.model_json_schema(), ensure_ascii=False))
        prompt = build_prompt_template()
        if lesson_id == "2.4":
            print(prompt.invoke(values).to_messages()[-1].content)
            try:
                prepare_prompt_values(text, " ", "{}")
            except AppError:
                print("非法空目标：请求前拒绝")
        else:
            seen = []
            # RunnableLambda包装普通函数，下面只收集消息数量，不伪造AI回答。
            inspect = RunnableLambda(lambda messages: seen.append(messages) or len(messages.to_messages()))
            chain = build_card_chain(prompt, inspect)
            print("构建后的调用次数：", len(seen))
            print("invoke后消息数：", chain.invoke(values), "观察调用次数：", len(seen))
    elif lesson_id in {"2.6", "2.7"}:
        context = {"id": "reference-material", **build_material_context({
            "title": "2023历史摘录", "text": text, "owner_user_id": "reference-demo",
        })}
        if lesson_id == "2.6":
            print(describe_publication_date(None), "；原文版本指纹：", context["content_sha256"])
        else:
            candidate = generate_candidate(context, "整理范围", store=CandidateStore(),
                                           mode="historical_replay")
            print(json.dumps(candidate, ensure_ascii=False, indent=2))
    elif lesson_id in {"2.8-A", "2.8-B", "2.9-A", "2.9-B"}:
        # SQL编译是离线观察；真实事务见专用PostgreSQL测试，不将此处算DB通过。
        print("已实现数据库函数；以下仅离线SQL预览。真实验证：scripts/stage2-dev.ps1 test")
        print(CreateTable(Base.metadata.tables["cards"]).compile(dialect=postgresql.dialect()))
    elif lesson_id == "2.10":
        from learning_app.api import map_error_status
        for code in ["invalid_input", "not_found", "version_conflict", "upstream_timeout"]:
            print(code, "→ HTTP", map_error_status(code))
        print("完整HTTP入口：python -m learning_app.cli serve --demo")
    elif lesson_id in {"2.11-A", "2.11-B"}:
        root = Path(__file__).resolve().parents[1]
        print("完整Vue组件：", root / "web/src/CardReview.vue")
        print("完整请求和页面状态：", root / "web/src/App.vue")
        print("构建web后由同源本机API托管。页面刷新通过?card=ID恢复已保存卡片。")
    elif lesson_id == "2.12":
        print(json.dumps(build_acceptance_report([
            {"name": "演示数据", "status": "passed", "source": "offline_reference"},
            {"name": "新模板真实生成", "status": "not_run", "source": "live"},
        ]), ensure_ascii=False, indent=2))
    print("本入口模型请求0；未读取.env。数据库/页面实测与独立能力证据另行记录。")
    return 0
