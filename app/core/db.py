from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from app.models import Base 

# 반드시 asyncpg 드라이버 사용
# 예: postgresql+asyncpg://user:password@localhost:5432/dose
# 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# 세션 팩토리
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, autocommit=False
)

# 의존성 주입용 세션
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
