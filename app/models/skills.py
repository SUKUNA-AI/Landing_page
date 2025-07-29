from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    skill_name = Column(String(50), nullable=False)
    description = Column(String)
    proficiency_level = Column(Integer, nullable=False)