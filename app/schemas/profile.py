from pydantic import BaseModel
from typing import Optional

class ProfileCreate(BaseModel):
    user_id: int
    name: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    resume_url: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    bio: Optional[str]
    photo_url: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    resume_url: Optional[str]

    class Config:
        from_attributes = True