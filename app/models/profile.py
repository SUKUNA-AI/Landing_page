from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    bio = Column(String)
    photo_url = Column(String(255))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String)
    resume_url = Column(String(255))