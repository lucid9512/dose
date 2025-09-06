# app/core/admin_auth.py
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi_users.jwt import decode_jwt
from app.core.config import settings
from app.models.user import User
from app.core.db import async_session_maker

class AdminAuth(AuthenticationBackend):
    async def authenticate(self, request: Request) -> bool:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return False

        token = token.split(" ")[1]
        try:
            data = decode_jwt(token, settings.SECRET_KEY, [settings.JWT_ALGORITHM])
            user_id = data.get("sub")
            if not user_id:
                return False

            async with async_session_maker() as session:
                user = await session.get(User, int(user_id))
                if user and user.is_superuser:
                    return True
        except Exception:
            return False

        return False
