# app/admin/__init__.py

import inspect
from fastapi import FastAPI
from sqladmin import Admin
from app.core.db import engine
from .views import UserAdmin, RoleAdmin
from app.core.config import settings
from app.core.auth.admin_backend import AdminAuthBackend  # 세션 기반 Admin 인증 백엔드

# ------------------------------------------------------------------------
# 인증 함수(_auth_fn)
# - sqladmin AuthenticationBackend는 login 시 username/password를 넘겨줌
# - 여기서 AdminAuthService.verify()를 호출해서 실제 DB 검증을 수행
# - AdminAuthBackend 안에서도 직접 verify를 호출할 수 있지만,
#   이렇게 함수로 분리해두면 추후 다른 인증 로직(예: LDAP, OAuth)으로 교체하기 쉬움
# ------------------------------------------------------------------------
async def _auth_fn(username: str, password: str):
    from app.services.auth.admin_service import AdminAuthService
    verify = getattr(AdminAuthService, "verify", None)

    # verify가 async 함수이면 await, sync 함수면 바로 실행
    if inspect.iscoroutinefunction(verify):
        return await verify(username, password)
    return verify(username, password)


# ------------------------------------------------------------------------
# init_admin(app: FastAPI)
# - FastAPI 앱에 sqladmin Admin UI를 붙여주는 초기화 함수
# - AdminAuthBackend를 붙여서 세션 기반 로그인 활성화
# - UserAdmin, RoleAdmin 뷰를 등록하여 /admin 에서 관리 가능
# ------------------------------------------------------------------------
def init_admin(app: FastAPI):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuthBackend(
            secret_key=settings.ADMIN_SECRET_KEY,  # 세션 쿠키 서명용 키
            auth_fn=_auth_fn,                      # 관리자 인증 함수
        ),
    )
    # 실제 관리할 뷰 등록
    admin.add_view(UserAdmin)   # 사용자 관리 화면
    admin.add_view(RoleAdmin)   # 역할/권한 관리 화면

    return admin