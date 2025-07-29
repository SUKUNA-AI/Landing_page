from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from datetime import datetime

class BlogPost(Base):
    __tablename__ = "blogposts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    date_published = Column(DateTime, default=datetime.utcnow)