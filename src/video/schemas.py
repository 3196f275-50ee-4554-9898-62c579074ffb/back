from datetime import datetime

from pydantic import BaseModel



class PartedResponse(BaseModel):
    status: int = 206
    message: str = "Parted"

class CreatedResponse(BaseModel):
    status: int = 201
    message: str = "Created"



class DeletedResponse(BaseModel):
    status: int = 200
    message: str = "Deleted"


class VideoResponse(BaseModel):
    video : list