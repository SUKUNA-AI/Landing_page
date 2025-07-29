from pydantic import BaseModel
from typing import Optional

class SkillCreate(BaseModel):
    user_id: int
    skill_name: str
    description: Optional[str] = None
    proficiency_level: int

class SkillResponse(BaseModel):
    id: int
    user_id: int
    skill_name: str
    description: Optional[str]
    proficiency_level: int

    class Config:
        from_attributes = True