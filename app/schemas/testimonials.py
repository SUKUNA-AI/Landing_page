from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestimonialCreate(BaseModel):
    user_id: int
    content: str
    author: str

class TestimonialUpdate(BaseModel):
    content: Optional[str] = None
    author: Optional[str] = None

class TestimonialResponse(BaseModel):
    id: int
    user_id: int
    content: str
    author: str
    created_at: datetime

    class Config:
        from_attributes = True