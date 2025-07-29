from pydantic import BaseModel
from typing import Optional
import datetime

class TestimonialCreate(BaseModel):
    user_id: int
    quote: str
    author: str
    date: Optional[datetime.date] = None

class TestimonialResponse(BaseModel):
    id: int
    user_id: int
    quote: str
    author: str
    date: Optional[datetime.date]

    class Config:
        from_attributes = True