from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

# Refresh Token 발급
def create_refresh_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": sub, "exp": expire},       # payload (sub = 사용자 식별자)
        settings.JWT_SECRET,               # 서명 비밀키
        algorithm=settings.JWT_ALGORITHM,  # 서명 알고리즘
    )

# Refresh Token 검증
def verify_refresh_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("sub")  # sub(사용자) 반환
    except JWTError:
        return None
