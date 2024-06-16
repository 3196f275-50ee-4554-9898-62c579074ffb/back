import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from src.statistics import schemas
from src.statistics import services
from typing import List
router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/penalty", response_model=List[schemas.Penalty])
async def get_penalties(db: AsyncSession = Depends(get_db)):
    return await services.get_penalties(db=db)

@router.get("/penalty/user/{user_id}", response_model=List[schemas.Penalty])
async def get_penalties_by_user(user_id: uuid.UUID ,db: AsyncSession = Depends(get_db)):
    return await services.get_penalties_by_user(db=db, user_id=user_id)

@router.get("/penalty/building/{building_id}", response_model=List[schemas.Penalty])
async def get_penalties_by_building(building_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_penalties_by_building(db=db, building_id=building_id)

@router.patch("/penalty/{penalty_id}")
async def update_penalty(penalty_id: uuid.UUID, penalty: schemas.PenaltyUpdate = Depends(), db: AsyncSession = Depends(get_db)):
    return await services.update_penalty(db=db, penalty_id=penalty_id, penalty=penalty)

@router.get("/penalty/count")
async def count_penalties(q: str = None, from_date: datetime = None, to_date: datetime = None, db: AsyncSession = Depends(get_db)):
    return await services.count_penalties(db=db, q=q, from_date=from_date, to_date=to_date)

@router.get("/penalty/array")
async def penalties_array(from_date: datetime = None, to_date: datetime = None, db: AsyncSession = Depends(get_db)):
    return await services.paritionary_penalties(db=db, from_date=from_date, to_date=to_date)