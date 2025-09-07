from fastapi import APIRouter
from app.services.auth import fastapi_users, current_active_user
from app.core.auth.backend import auth_backend
from app.schemas.req.auth import RefreshRequest
from app.schemas.res.auth import RefreshResponse
from app.services.auth.token_service import AuthService
from app.schemas.user import UserRead, UserCreate, UserUpdate 

router = APIRouter()

# 로그인 / 로그아웃
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
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

# Refresh API
@router.post("/auth/jwt/refresh", response_model=RefreshResponse, tags=["auth"])
async def refresh_token(request: RefreshRequest):
    return AuthService.refresh(request.refresh_token)