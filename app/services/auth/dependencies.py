from app.services.auth.manager import fastapi_users

# 로그인된 "활성 사용자(active=True)"만 허용
# - is_active=True 조건 체크
# - 로그인 안 된 경우 → 401 Unauthorized
# - 비활성화된 유저(is_active=False) → 접근 차단
current_active_user = fastapi_users.current_user(active=True)

# "관리자(superuser=True)"만 허용
# - is_superuser=True 조건 체크
# - 로그인 + 관리자 권한 있어야 통과
# - 일반 유저는 → 403 Forbidden
current_superuser = fastapi_users.current_user(superuser=True)
