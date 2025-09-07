from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.middleware import init_middleware
from app.core.events import init_events
from app.admin import init_admin
from app.api.v1 import router as api_v1_router
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.sessions import SessionMiddleware

# FastAPI 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    openapi_url="/openapi.json",
    docs_url=None,  # Disable default docs URL
)

# 미들웨어 (sqladmin이 request.session 쓰도록)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.ADMIN_SECRET_KEY,  # .env: ADMIN_SECRET_KEY=...
    same_site="lax",
    https_only=False,  # HTTPS면 True 권장
)

# 모든 v1 API 등록
app.include_router(api_v1_router, prefix="/api/v1")


# 환경 설정
setup_logging()
init_admin(app)
init_middleware(app)
init_events(app)

for r in app.routes:
    if "login" in r.path:
        print(r.path, "->", r.endpoint.__module__)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_ui_parameters={"persistAuthorization": True}
    )


@app.get("/")
def read_root():
    return {"message": "Hello, Dose!"}