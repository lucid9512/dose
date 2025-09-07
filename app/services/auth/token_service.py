from fastapi import HTTPException, status
from app.core.auth.refresh import create_refresh_token, verify_refresh_token

# Refresh Token 관련 서비스
class AuthService:
    @staticmethod
    def issue_refresh_token(username: str) -> str:
        """
        로그인 성공 시 Refresh Token 발급
        """
        return create_refresh_token(username)

    @staticmethod
    def refresh(refresh_token: str) -> dict:
        """
        Refresh Token 검증 후 새 Refresh Token 발급
        """
        username = verify_refresh_token(refresh_token)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        # 새 Refresh 발급
        new_refresh_token = create_refresh_token(username)
        return {"refresh_token": new_refresh_token}
