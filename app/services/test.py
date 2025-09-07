from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.test import Test
from app.schemas.req.test import TestCreate

async def create_test(db: AsyncSession, test_in: TestCreate) -> Test:
    test = Test(name=test_in.name)
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return test

async def get_tests(db: AsyncSession) -> list[Test]:
    result = await db.execute(select(Test))
    return result.scalars().all()