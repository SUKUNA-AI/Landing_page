from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
from datetime import datetime

class TelegramSubscriber(Base):
    __tablename__ = "TelegramSubscribers"
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String(50), unique=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)