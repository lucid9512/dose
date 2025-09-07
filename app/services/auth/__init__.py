from fastapi_users import FastAPIUsers
from app.models.user import User
from app.services.auth.manager import get_user_manager
from app.core.auth.backend import auth_backend

# FastAPIUsers 인스턴스 (Access Token 발급/검증 자동화)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# 현재 활성 사용자 (is_active=True)
current_active_user = fastapi_users.current_user(active=True)

# 현재 슈퍼유저 (is_superuser=True)
current_superuser = fastapi_users.current_user(superuser=True)
