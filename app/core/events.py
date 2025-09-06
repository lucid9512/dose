from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

def init_events(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        logger.info("Dose Application startup")
        # TODO: DB 커넥션 풀 준비, 캐시 로딩, 백그라운드 잡 시작 등

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Dose  Application shutdown")
        # TODO: DB 세션 닫기, 메시지 큐 정리, 로그 flush 등
