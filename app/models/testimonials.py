from sqlalchemy import Column, Integer, String, ForeignKey, Date
from ..database import Base

class Testimonial(Base):
    __tablename__ = "testimonials"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quote = Column(String, nullable=False)
    author = Column(String(100), nullable=False)
    date = Column(Date)