
from pydantic import EmailStr, Field
from app.schemas.__base__ import VaModelReq

class RefreshRequest(VaModelReq):
    refresh_token: str


class AdminLoginSchema(VaModelReq):
    username: EmailStr = Field(..., description="관리자 이메일")
    password: str = Field(..., min_length=8, description="관리자 비밀번호")