from sqlalchemy import Column, Integer, String, ForeignKey, Date
from ..database import Base

class Education(Base):
    __tablename__ = "Education"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    institution = Column(String(100), nullable=False)
    degree = Column(String(100))
    field_of_study = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)