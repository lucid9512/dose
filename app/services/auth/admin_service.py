import logging
from sqlalchemy import select
from app.core.db import async_session_maker
from app.models.user import User
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

# CLI와 동일한 해셔 초기화 (argon2 + bcrypt 지원)
hasher = PasswordHash([Argon2Hasher(), BcryptHasher()])

class AdminAuthService:
    @staticmethod
    async def verify(identifier: str, password: str):
        async with async_session_maker() as session:
            # identifier는 사실 email
            stmt = select(User).where(User.email == identifier)
            result = await session.execute(stmt)
            user: User | None = result.scalar_one_or_none()

            if not user:
                print("DEBUG: user not found", identifier)
                return None

            if not hasher.verify(password, user.hashed_password):
                print("DEBUG: invalid password", identifier)
                return None

            if not getattr(user, "is_superuser", False):
                print("DEBUG: not superuser", identifier)
                return None

            return {
                "id": user.id,
                "is_admin": True,
                "username": getattr(user, "full_name", None) or user.email,
                "email": user.email,
            }
