from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPostCreate(BaseModel):
    user_id: int
    title: str
    content: str
    summary: Optional[str] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None

class BlogPostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True