# app/auth/manager.py
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from app.models.user import User
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth.backend import auth_backend

class UserManager(BaseUserManager[User, int]):
    user_db_model = User

    async def on_after_register(self, user: User, request=None):
        print(f"- 새 유저 등록됨: {user.email}")

async def get_user_manager(session: AsyncSession = Depends(get_db)):
    yield UserManager(session)

# FastAPI Users 초기화
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

