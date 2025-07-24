from sqlalchemy import Column, Integer, String, ForeignKey, Date
from ..database import Base

class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String)
    image_url = Column(String(255))
    project_url = Column(String(255))
    date_completed = Column(Date)