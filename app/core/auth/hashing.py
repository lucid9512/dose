from passlib.context import CryptContext

# 비밀번호 해싱 컨텍스트 (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """평문 비밀번호 → 해시"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문과 해시 비교"""
    return pwd_context.verify(plain_password, hashed_password)
