import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
class Task(BaseModel):
    id: uuid.UUID | None = None
    name: str
    start: datetime
    end: datetime
    type: str
    progress: int
    is_disabled: bool
    building: uuid.UUID
    depends_on: uuid.UUID | None = None
class Report(BaseModel):
    title: str
    employee: uuid.UUID
    location: str
    status: str
    building: uuid.UUID
    task: uuid.UUID

class ReportWithDate(Report):
    created_at: datetime

class Building(BaseModel):
    id: uuid.UUID
    name: str = Field(alias="name", serialization_alias="value")
    label: str
    class Config:
        orm_mode = True
        from_attributes = True