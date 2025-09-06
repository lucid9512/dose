from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def init_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: settings.ALLOW_ORIGINS 사용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
