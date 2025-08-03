from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkExperienceCreate(BaseModel):
    user_id: int
    company: str
    position: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None

class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class WorkExperienceResponse(BaseModel):
    id: int
    user_id: int
    company: str
    position: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True