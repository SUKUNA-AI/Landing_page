from sqlalchemy import Column, Integer, String, ForeignKey, Date
from ..database import Base

class WorkExperience(Base):
    __tablename__ = "workexperience"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)