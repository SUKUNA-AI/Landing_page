from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PollCreate(BaseModel):
    telegram_user_id: str
    question: str
    options: str

class PollUpdate(BaseModel):
    question: Optional[str] = None
    options: Optional[str] = None

class PollResponse(BaseModel):
    id: int
    telegram_user_id: str
    question: str
    options: str
    created_at: datetime

    class Config:
        from_attributes = True