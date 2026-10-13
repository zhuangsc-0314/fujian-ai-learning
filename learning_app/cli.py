"""完整程序入口；无参数只预览模板，不读取.env，不连接数据库。"""

import argparse
import json
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from learning_app.ai import build_prompt_template, prepare_prompt_values
from learning_app.domain import AppError, LearningCard, MaterialInput
from learning_app.history import historical_material


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preview", "serve", "replay", "generate", "list", "read"],
                        nargs="?", default="preview")
    parser.add_argument("--demo", action="store_true", help="显式启用本机演示身份")
    parser.add_argument("--live", action="store_true", help="允许真实模型请求，可能计费")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--material", type=Path)
    parser.add_argument("--goal", default="整理原文范围，明确未知信息。")
    parser.add_argument("--card-id")
    args = parser.parse_args()
    if args.command == "preview":
        values = prepare_prompt_values(historical_material(), args.goal,
                                       json.dumps(LearningCard.model_json_schema(), ensure_ascii=False))
        messages = build_prompt_template().invoke(values).to_messages()
        print("离线模板预览；模型请求0；未读取.env。")
        for message in messages:
            print(f"[{message.type}] {message.content}")
        return 0
    if not args.demo:
        parser.error("数据库与HTTP命令必须显式添加--demo；本阶段没有真实认证。")
    if not 1024 <= args.port <= 65535:
        parser.error("端口须为1024—65535。")
    try:
        from learning_app.api import DEMO_OWNER, create_app
        from learning_app.service import CardService
        from learning_app.storage import build_engine, database_url, session_factory

        engine = build_engine(database_url())
        service = CardService(session_factory(engine), live_enabled=args.live)
        if args.command == "serve":
            import uvicorn
            print("本机教学演示；真实生成：" + ("已允许（可能计费）" if args.live else "禁用"))
            uvicorn.run(create_app(service, demo=True, port=args.port),
                        host="127.0.0.1", port=args.port, access_log=False)
        elif args.command in {"replay", "generate"}:
            if args.command == "generate" and (not args.live or args.material is None):
                parser.error("真实生成须明确--live和--material文件。")
            material = historical_material() if args.command == "replay" else args.material.read_text(
                encoding="utf-8-sig",
            )
            context = service.add_material(MaterialInput(title="CLI学习材料", text=material), DEMO_OWNER)
            candidate = service.generate(context["id"], args.goal, DEMO_OWNER,
                                         "historical_replay" if args.command == "replay" else "live")
            saved = service.save(candidate["candidate_id"], candidate["content_hash"], DEMO_OWNER)
            print(json.dumps(saved, ensure_ascii=False, indent=2))
        elif args.command == "list":
            print(json.dumps(service.list_cards(DEMO_OWNER), ensure_ascii=False, indent=2))
        elif args.command == "read":
            if not args.card_id:
                parser.error("read需要--card-id。")
            print(json.dumps(service.read(args.card_id, DEMO_OWNER), ensure_ascii=False, indent=2))
        engine.dispose()
    except AppError as error:
        print(f"[{error.stage}/{error.code}] {error.message}")
        return 1
    except SQLAlchemyError:
        print("[database] 操作失败；检查本机连接和迁移。未自动重新生成。")
        return 1
    except OSError:
        print("[input] 材料文件读取失败；检查路径和编码。")
        return 1
    except ValidationError:
        print("[input] 材料或目标格式不合法；检查必填字段及长度。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
