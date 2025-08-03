from pydantic import BaseModel
from typing import Optional

class SubscriberPreferenceCreate(BaseModel):
    telegram_user_id: str
    preference_key: str
    preference_value: str

class SubscriberPreferenceUpdate(BaseModel):
    preference_key: Optional[str] = None
    preference_value: Optional[str] = None

class SubscriberPreferenceResponse(BaseModel):
    id: int
    telegram_user_id: str
    preference_key: str
    preference_value: str

    class Config:
        from_attributes = True