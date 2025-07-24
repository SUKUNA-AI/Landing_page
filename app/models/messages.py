from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(String, nullable=False)
    date_sent = Column(DateTime, default=datetime.utcnow)
    source = Column(String(20), nullable=False)