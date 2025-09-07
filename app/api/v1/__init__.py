# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1 import auth
from app.api.v1 import test

router = APIRouter()
router.include_router(auth.router)   # JWT
router.include_router(test.router)
