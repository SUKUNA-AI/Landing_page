from pydantic import BaseModel
from typing import Optional
import datetime

class PollCreate(BaseModel):
    telegram_user_id: str
    question: str
    answer: Optional[str] = None

class PollResponse(BaseModel):
    id: int
    telegram_user_id: str
    question: str
    answer: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True