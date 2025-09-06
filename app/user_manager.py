# app/user_manager.py
from fastapi_users import BaseUserManager, IntegerIDMixin
from app.models.user import User
from app.core.database import async_session_maker
from app.core.config import settings

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

async def get_user_manager():
    async with async_session_maker() as session:
        yield UserManager(session)
