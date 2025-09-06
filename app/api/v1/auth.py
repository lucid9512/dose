from fastapi import APIRouter
from app.services.auth.manager import fastapi_users
from app.services.auth.backend import auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

# 로그인 / 로그아웃
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# 회원가입
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), 
    prefix="/auth",
    tags=["auth"],
)

# 사용자 읽기/업데이트
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
