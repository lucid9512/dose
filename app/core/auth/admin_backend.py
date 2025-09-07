import logging
from typing import Optional, Callable, Awaitable
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.schemas.req.auth import AdminLoginSchema  # 스키마 분리
from app.services.auth.admin_service import AdminAuthService

AuthFn = Callable[[str, str], Awaitable[Optional[dict]]]

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str, auth_fn: AuthFn | None = None):
        super().__init__(secret_key=secret_key)
        # 기본은 AdminAuthService.verify 사용
        self.auth_fn = auth_fn

    async def login(self, request: Request) -> bool:
        form = await request.form()
        logging.error(form)
        try:
            data = AdminLoginSchema(**form)
        except Exception:
            logging.info("Data Exception")
            return False

        if self.auth_fn:
            user = await self.auth_fn(data.username, data.password)
        else:
            user = await AdminAuthService.verify(data.username, data.password)

        if not user or not user.get("is_admin", False):
            logging.info("Is Not Admin")
            return False

        # 세션 저장
        request.session.update({
            "admin_user_id": str(user.get("id", "")),
            "admin_username": user.get("username") or user.get("email") or data.email,
        })
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("admin_user_id"))
