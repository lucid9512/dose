from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from app.models.user import User
from app.services.auth.dependencies import get_user_db
from app.core.config import settings

# fastapi-users에서 요구하는 UserManager
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

# UserManager DI (Depends에서 주입 가능)
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
