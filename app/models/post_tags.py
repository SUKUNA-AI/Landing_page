from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class PostTag(Base):
    __tablename__ = "postTags"
    post_id = Column(Integer, ForeignKey("BlogPosts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("Tags.id"), primary_key=True)