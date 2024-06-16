from typing import Literal

from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import datetime, timedelta


class Penalty(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    reason: str = Field(serialization_alias="body")
    grade: Literal["Warning", "Danger", "Success"] = Field(serialization_alias="header")
    created_at: datetime

    # @field_validator("created_at")
    # def round_to_nearest_day(cls, value):
    #     # Округляем дату до ближайшего дня
    #     if isinstance(value, datetime):
    #         rounded_value = (value + timedelta(hours=12)).replace(hour=0, minute=0, second=0, microsecond=0)
    #         return rounded_value
    #     raise ValueError("Invalid datetime format")

class PenaltyUpdate(BaseModel):
    reason: str = Field(serialization_alias="body")
    grade: Literal["Warning", "Danger", "Success"] = Field(serialization_alias="header")

