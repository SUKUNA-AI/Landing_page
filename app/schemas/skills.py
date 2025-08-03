from pydantic import BaseModel
from typing import Optional

class SkillCreate(BaseModel):
    user_id: int
    name: str
    proficiency: Optional[str] = None

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    proficiency: Optional[str] = None

class SkillResponse(BaseModel):
    id: int
    user_id: int
    name: str
    proficiency: Optional[str] = None

    class Config:
        from_attributes = True