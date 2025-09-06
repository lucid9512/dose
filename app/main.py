from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.middleware import init_middleware
from app.core.events import init_events
from app.admin import init_admin
from app.api.v1 import router as api_v1_router

# FastAPI 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)

# 환경 설정
setup_logging()
init_admin(app)
init_middleware(app)
init_events(app)

# 모든 v1 API 등록
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Hello, Dose!"}