from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationCreate(BaseModel):
    user_id: int
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None

class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class EducationResponse(BaseModel):
    id: int
    user_id: int
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True