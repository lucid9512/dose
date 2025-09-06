from fastapi import APIRouter
from app.api.v1 import auth

router = APIRouter()
router.include_router(auth.router)  # auth 라우터 포함