from pydantic import BaseModel
from typing import Optional
import datetime

class BlogPostCreate(BaseModel):
    user_id: int
    title: str
    content: str
    date_published: Optional[datetime.datetime] = None

class BlogPostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date_published: datetime.datetime

    class Config:
        from_attributes = True