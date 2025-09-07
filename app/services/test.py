from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.test import Test
from app.schemas.req.test import TestCreate
from app.schemas.res.test import TestReadRes
import logging

async def create_test(db: AsyncSession, test_in: TestCreate) -> Test:
    test = Test(name=test_in.name)
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return TestReadRes.model_validate(test)

async def get_tests(db: AsyncSession) -> list[Test]:
    result = await db.execute(select(Test).order_by(Test.id))
    objs = result.scalars().all()
    logging.info(result)
    logging.info(type(result))
    return [TestReadRes.model_validate(o) for o in objs]