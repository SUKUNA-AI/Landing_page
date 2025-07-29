from pydantic import BaseModel
from typing import Optional
import datetime

class WorkExperienceCreate(BaseModel):
    user_id: int
    company: str
    position: str
    description: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

class WorkExperienceResponse(BaseModel):
    id: int
    user_id: int
    company: str
    position: str
    description: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]

    class Config:
        from_attributes = True