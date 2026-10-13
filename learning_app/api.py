"""本机同源HTTP入口：上下文由服务端提供，页面不传owner或Key。"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError

from learning_app.domain import AppError, InputModel, MaterialInput, ReviewInput
from learning_app.history import historical_material
from learning_app.service import CardService


DEMO_OWNER = "local-demo-user"


class GenerateInput(InputModel):
    material_version_id: str = Field(min_length=1, max_length=36)
    learning_goal: str = Field(min_length=1, max_length=300)
    mode: Literal["live", "historical_replay"] = "live"


class SaveInput(InputModel):
    candidate_id: str = Field(min_length=1, max_length=36)
    expected_content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")


def map_error_status(error_code: str) -> int:
    return {
        "not_found": 404, "version_conflict": 409, "candidate_expired": 409,
        "candidate_capacity": 503, "live_disabled": 403,
        "database_config": 503, "database_unavailable": 503, "config_error": 503,
        "upstream_timeout": 504, "upstream_connection": 502, "upstream_http": 502,
        "invalid_output": 502, "invalid_input": 422, "invalid_evidence": 422,
    }.get(error_code, 500)


def create_app(service: CardService, *, demo: bool = False, port: int = 8000) -> FastAPI:
    """必须显式demo；没有真实认证时不允许悄悄回退默认用户。"""
    if not demo:
        raise AppError("authentication_required", "startup", "本阶段只提供显式本机demo模式。")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        service.sessions.kw["bind"].dispose()

    app = FastAPI(title="福建备考 · 阶段2本机教学", lifespan=lifespan)
    hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
    origins = {f"http://{host}" for host in hosts}

    @app.middleware("http")
    async def local_boundary(request: Request, call_next):
        origin = request.headers.get("origin")
        if (request.headers.get("host") not in hosts
                or (origin is not None and origin not in origins)
                or request.headers.get("sec-fetch-site") == "cross-site"):
            return JSONResponse({"error": {"stage": "access", "message": "仅允许本机同源访问。"}},
                                status_code=403)
        if request.method in {"POST", "PATCH", "PUT", "DELETE"}:
            # 自定义头防跨站表单；不启用CORS，跨站JS预检也无法通过。
            if request.headers.get("x-stage2-local") != "1":
                return JSONResponse({"error": {"stage": "access", "message": "缺少本机请求标记。"}},
                                    status_code=403)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'"
        )
        return response

    @app.exception_handler(AppError)
    async def app_error(request: Request, error: AppError):
        return JSONResponse({"error": {"code": error.code, "stage": error.stage,
                                      "message": error.message}},
                            status_code=map_error_status(error.code))

    @app.exception_handler(SQLAlchemyError)
    async def db_error(request: Request, error: SQLAlchemyError):
        return JSONResponse({"error": {"code": "database_unavailable", "stage": "database",
                                      "message": "数据库操作失败；检查连接和迁移，不必重新生成。"}},
                            status_code=503)

    @app.exception_handler(RequestValidationError)
    async def input_error(request: Request, error: RequestValidationError):
        return JSONResponse({"error": {"code": "invalid_input", "stage": "input",
                                      "message": "请求字段不合法；检查必填、长度和日期格式。"}},
                            status_code=422)

    @app.get("/api/v1/info")
    def info():
        return {"demo": True, "live_enabled": service.live_enabled,
                "historical_material": historical_material(),
                "notice": "本机教学演示；尚无真实认证；2023年历史材料不代表未来规则。"}

    @app.post("/api/v1/materials", status_code=201)
    def add_material(data: MaterialInput):
        return service.add_material(data, DEMO_OWNER)

    @app.post("/api/v1/card-candidates")
    def generate(data: GenerateInput):
        return service.generate(data.material_version_id, data.learning_goal, DEMO_OWNER, data.mode)

    @app.post("/api/v1/cards")
    def save(data: SaveInput):
        return service.save(data.candidate_id, data.expected_content_hash, DEMO_OWNER)

    @app.get("/api/v1/cards")
    def list_cards(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
        return service.list_cards(DEMO_OWNER, limit, offset)

    @app.get("/api/v1/cards/{card_id}")
    def read(card_id: str):
        return service.read(card_id, DEMO_OWNER)

    @app.patch("/api/v1/cards/{card_id}/review")
    def review(card_id: str, data: ReviewInput):
        return service.review(card_id, data, DEMO_OWNER)

    dist = Path(__file__).resolve().parents[1] / "web/dist"
    if dist.is_dir():
        app.mount("/", StaticFiles(directory=dist, html=True), name="web")
    return app
