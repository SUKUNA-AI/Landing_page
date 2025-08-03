from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from datetime import datetime

class MLPrediction(Base):
    __tablename__ = "mlpredictions"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    input_text = Column(String, nullable=False)
    prediction = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)