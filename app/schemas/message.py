from pydantic import BaseModel
from typing import Optional
import datetime

class MessageCreate(BaseModel):
    name: str
    email: str
    message: str
    source: str

class MessageResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    source: str
    date_sent: datetime.datetime

    class Config:
        from_attributes = True