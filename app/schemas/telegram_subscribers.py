from pydantic import BaseModel
import datetime

class TelegramSubscriberCreate(BaseModel):
    telegram_user_id: str

class TelegramSubscriberResponse(BaseModel):
    id: int
    telegram_user_id: str
    subscribed_at: datetime.datetime

    class Config:
        from_attributes = True