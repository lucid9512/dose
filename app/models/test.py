from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class Test(BaseModel):
    __tablename__ = "tests"

    name = Column(String(100), nullable=False)