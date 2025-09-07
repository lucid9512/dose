# app/core/middleware.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def init_middleware(app: FastAPI):
    allow_origins = getattr(settings, "ALLOW_ORIGINS", "").split(",") if hasattr(settings, "ALLOW_ORIGINS") else []
    allow_origins = [o.strip() for o in allow_origins if o.strip()]
    if not allow_origins:
        allow_origins = ["http://localhost:3000"]  # 최소 기본값

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
