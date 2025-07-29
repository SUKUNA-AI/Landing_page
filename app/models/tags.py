from sqlalchemy import Column, Integer, String
from ..database import Base

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(50), unique=True, nullable=False)