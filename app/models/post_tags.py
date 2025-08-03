from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class PostTag(Base):
    __tablename__ = "posttags"
    post_id = Column(Integer, ForeignKey("blogposts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)