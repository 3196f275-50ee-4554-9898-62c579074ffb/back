from datetime import datetime
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from src.statistics import models, schemas
from sqlalchemy import select, update, func


async def get_penalties(db: AsyncSession):
    query = select(models.Penalty)
    result = await db.execute(query)
    return result.scalars().all()


async def get_penalties_by_date(db: AsyncSession, from_date: datetime, to_date: datetime):
    query = select(models.Penalty).where(models.Penalty.created_at >= from_date, models.Penalty.created_at <= to_date)
    result = await db.execute(query)
    return result.scalars().all()


async def get_penalties_by_user(db: AsyncSession, user_id: str):
    query = select(models.Penalty).where(models.Penalty.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_penalties_by_building(db: AsyncSession, building_id: str):
    query = select(models.Penalty).join(models.PenaltyBuilding).where(models.PenaltyBuilding.building_id == building_id)
    result = await db.execute(query)
    return result.scalars().all()


async def update_penalty(penalty_id: str, penalty: schemas.PenaltyUpdate, db: AsyncSession, ):
    stmt = (
        update(models.Penalty)
        .where(models.Penalty.id == penalty_id)
        .values(reason=penalty.reason, grade=penalty.grade)
    )
    await db.execute(stmt)
    await db.commit()


async def count_penalties(db: AsyncSession, q:str, from_date: datetime, to_date: datetime):
    """
    возвращает количество по совпадающим параметрам

    """
    res = {}
    query = select(func.count( models.Penalty.id, label="count")).select_from(models.Penalty)
    if from_date:
        query = query.where(models.Penalty.created_at >= from_date)

    if to_date:
        query = query.where(models.Penalty.created_at <= to_date)

    if q:
        query = query.where(models.Penalty.grade == q)
        res = {"grade": q}

    result = await db.execute(query)

    res.setdefault("count", result.scalars().first())

    return res

async def paritionary_penalties(db: AsyncSession, from_date: datetime, to_date: datetime):
    """
    возвращает количество по совпадающим параметрам

    """
    if not from_date:
        from_date = datetime(2024, 6, 10)
    if not to_date:
        to_date = datetime.now()
    delta = timedelta(days=1)

    penalties = await get_penalties(db=db)

    daily_penalties = []

    current_date = from_date

    while current_date < to_date:
        next_date = current_date + delta

        penalties_in_interval = [p for p in penalties if current_date <= p.created_at < next_date]

        # count_dict = {"date": current_date.date(), "Warning": 0, "Danger": 0, "Success": 0}
        warnings_dict = {"date": current_date.date(),"count": 0, "header":"Warning"}
        success_dict = {"date": current_date.date(),"count": 0, "header":"Success"}
        dangers_dict = {"date": current_date.date(),"count": 0, "header":"Danger"}
        for penalty in penalties_in_interval:
            if penalty.grade == "Warning":
                warnings_dict["count"] += 1
            elif penalty.grade == "Danger":
                dangers_dict["count"] += 1
            else:
                success_dict["count"] += 1

        daily_penalties+= [warnings_dict, success_dict, dangers_dict]

        current_date = next_date

    return daily_penalties