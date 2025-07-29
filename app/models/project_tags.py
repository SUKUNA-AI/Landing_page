from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class ProjectTag(Base):
    __tablename__ = "projecttags"
    project_id = Column(Integer, ForeignKey("Projects.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("Tags.id"), primary_key=True)