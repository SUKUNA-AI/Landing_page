from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from datetime import datetime

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String(50), ForeignKey("TelegramSubscribers.telegram_user_id"), nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)