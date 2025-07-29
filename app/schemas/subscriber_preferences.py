from pydantic import BaseModel

class SubscriberPreferenceCreate(BaseModel):
    telegram_user_id: str
    notification_type: str
    is_enabled: bool = True

class SubscriberPreferenceResponse(BaseModel):
    id: int
    telegram_user_id: str
    notification_type: str
    is_enabled: bool

    class Config:
        from_attributes = True