from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
from datetime import datetime

class Analytic(Base):
    __tablename__ = "Analytics"
    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String(255), nullable=False)
    visit_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(String)
    session_id = Column(String(50))
    action = Column(String(50))
    duration = Column(Integer)