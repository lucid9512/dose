# app/auth/backend.py
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from app.core.config import settings

SECRET = settings.JWT_SECRET

bearer_transport = BearerTransport(tokenUrl=settings.JWT_TOKEN_URL)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
