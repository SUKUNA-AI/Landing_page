from pydantic import BaseModel
from typing import Optional

class SocialMediaCreate(BaseModel):
    user_id: int
    platform: str
    url: str

class SocialMediaUpdate(BaseModel):
    platform: Optional[str] = None
    url: Optional[str] = None

class SocialMediaResponse(BaseModel):
    id: int
    user_id: int
    platform: str
    url: str

    class Config:
        from_attributes = True