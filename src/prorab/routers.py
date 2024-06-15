import uuid

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from typing import List
from src.prorab import schemas
from src.prorab import services

router = APIRouter(
    prefix="/object",
    tags=["object"],
    responses={404: {"description": "Not found"}},
)


@router.post("/building")
async def add_building(
        building: schemas.Building,
        db: AsyncSession = Depends(get_db),
):
    return await services.create_building(db=db, building=building)


@router.post("/task", response_model=schemas.Task)
async def add_task(

        task: schemas.Task, db: AsyncSession = Depends(get_db)):
    return await services.create_task(db=db, task=task)


@router.post("/report", response_model=schemas.Report)
async def add_report(report: schemas.Report, db: AsyncSession = Depends(get_db)):
    return await services.create_report(db=db, report=report)


sub_router = APIRouter(
    prefix="/building",
    tags=["object"],
    responses={404: {"description": "Not found"}},
)


@router.get("/building")
async def get_buildings(db: AsyncSession = Depends(get_db)):
    result = await services.get_buildings(db=db)


    return [schemas.Building.from_orm(building) for building in result]


@sub_router.get("/{building_id}/tasks", response_model=List[schemas.Task])
async def get_tasks(building_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_tasks(building_id=building_id, db=db)


@sub_router.get("/{building_id}/task/{task_id}", response_model=schemas.Task)
async def get_current_task(building_id: uuid.UUID, task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_task_by_id(building_id=building_id, db=db, task_id=task_id)


@sub_router.get("/{building_id}/reports", response_model=List[schemas.ReportWithDate])
async def get_reports(
        building_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    reports = await services.get_reports(building_id=building_id, db=db)
    return await services.get_reports(building_id=building_id, db=db)


router.include_router(sub_router)
