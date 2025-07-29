from pydantic import BaseModel
from typing import Optional
import datetime

class EducationCreate(BaseModel):
    user_id: int
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

class EducationResponse(BaseModel):
    id: int
    user_id: int
    institution: str
    degree: Optional[str]
    field_of_study: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]

    class Config:
        from_attributes = True