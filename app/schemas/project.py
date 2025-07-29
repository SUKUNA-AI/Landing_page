from pydantic import BaseModel
from typing import Optional
import datetime

class ProjectCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    date_completed: Optional[datetime.date] = None

class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    image_url: Optional[str]
    project_url: Optional[str]
    date_completed: Optional[datetime.date]

    class Config:
        from_attributes = True