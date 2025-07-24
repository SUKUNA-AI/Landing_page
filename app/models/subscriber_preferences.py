from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ..database import Base

class SubscriberPreference(Base):
    __tablename__ = "SubscriberPreferences"
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String(50), ForeignKey("TelegramSubscribers.telegram_user_id"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    is_enabled = Column(Boolean, default=True)