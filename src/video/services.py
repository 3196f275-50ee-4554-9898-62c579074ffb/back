import shutil
from sqlalchemy import select, delete
from typing import List
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.background import BackgroundTasks
from src.statistics.models import Penalty as PenaltyModel
from src.statistics.schemas import Penalty as PenaltySchema

from src.video import schemas
from src.video import models
from sqlalchemy.ext.asyncio import AsyncSession


async def dump_penalty(db: AsyncSession, user_id: uuid4, reason: str, ):
    penalty = PenaltyModel(user_id=user_id, reason=reason)
    db.add(penalty)
    await db.commit()
