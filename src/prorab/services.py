import uuid
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.prorab import models
from src.prorab import schemas



async def get_tasks(building_id: uuid.UUID,db: AsyncSession):
    result = await db.execute(select(models.Task).where(models.Task.building == building_id))
    return result.scalars().all()


async def get_task_by_id(building_id: uuid.UUID,db: AsyncSession, task_id: uuid.UUID):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id).where(models.Task.building == building_id))
    return result.scalars().first()


async def create_task(db: AsyncSession, task: schemas.Task):
    task = task.dict()
    utc = pytz.UTC
    task["start"] = task["start"].astimezone(utc)
    task["end"] = task["end"].astimezone(utc)
    task["start"] = task["start"].replace(tzinfo=None)
    task["end"] = task["end"].replace(tzinfo=None)
    print(task)
    task = models.Task(**task)
    db.add(task)
    await db.commit()

    return task


async def get_reports(building_id: uuid.UUID,db: AsyncSession):
    result = await db.execute(select(models.Report).where(models.Report.building == building_id))

    return result.scalars().all()
async def create_report(db: AsyncSession, report: schemas.Report):
    report = report.dict()

    report = models.Report(**report)
    db.add(report)
    await db.commit()

    return report

async def create_building(db: AsyncSession, building: schemas.Building):
    building = building.dict()
    building = models.Building(**building)
    db.add(building)
    await db.commit()

    return building

async def get_buildings(db: AsyncSession):
    result = await db.execute(select(models.Building))


    return result.scalars().all()