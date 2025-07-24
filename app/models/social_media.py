from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class SocialMedia(Base):
    __tablename__ = "SocialMedia"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    platform_name = Column(String(50), nullable=False)
    profile_url = Column(String(255), nullable=False)