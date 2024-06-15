from pydantic import BaseModel
import uuid
from datetime import datetime


class Penalty(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    reason: str
    created_at: datetime
