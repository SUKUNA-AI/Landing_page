from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from datetime import datetime

class BlogPost(Base):
    __tablename__ = 'blogposts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    summary = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)