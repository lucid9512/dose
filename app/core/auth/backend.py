# app/core/auth/backend.py
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.core.config import settings

# API JWT 로그인 엔드포인트(URL은 fastapi-users 라우트와 맞춰야 함)
# /api/v1/auth/jwt/login 사용 중이므로 아래처럼 맞춘다.
bearer_transport = BearerTransport(tokenUrl="/api/v1/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    # access token 유효시간(분)을 초 단위로
    lifetime_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=lifetime_seconds)

# fastapi-users가 쓰는 백엔드
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
