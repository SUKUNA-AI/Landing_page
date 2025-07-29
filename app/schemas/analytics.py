from pydantic import BaseModel
from typing import Optional
import datetime

class AnalyticsCreate(BaseModel):
    page_url: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    action: Optional[str] = None
    duration: Optional[int] = None

class AnalyticsResponse(BaseModel):
    id: int
    page_url: str
    visit_time: datetime.datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    session_id: Optional[str]
    action: Optional[str]
    duration: Optional[int]

    class Config:
        from_attributes = True