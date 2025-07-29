from pydantic import BaseModel
from typing import Optional
import datetime

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    status: str

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True