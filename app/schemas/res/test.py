from app.schemas.__base__ import VaModelRes
from datetime import datetime

class TestReadRes(VaModelRes):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM 객체 자동 변환 허용