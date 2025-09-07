from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.test import Test
from app.schemas.req.test import TestCreate
from app.schemas.res.test import TestReadRes
from app.services.test import create_test, get_tests
from app.services.auth import current_active_user
from sqlalchemy import select

router = APIRouter(prefix="/tests", tags=["tests"])

@router.post("/", response_model=TestReadRes)
async def create_test_item(
    test_in: TestCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(current_active_user),   # JWT 필요 없으면 지워도 됨
):
    return await create_test(db, test_in)

@router.get("/", response_model=list[TestReadRes])
async def get_tests_item(
    db: AsyncSession = Depends(get_db),
    user=Depends(current_active_user),
):
    return await get_tests(db)
