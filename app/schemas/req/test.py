from app.schemas.__base__ import VaModelReq

class TestBase(VaModelReq):
    name: str

class TestCreate(TestBase):
    pass

class TestRead(TestBase):
    id: int

    class Config:
        from_attributes = True  # ORM -> Pydantic 변환 허용