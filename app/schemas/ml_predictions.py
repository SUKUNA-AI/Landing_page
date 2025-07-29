from pydantic import BaseModel
from typing import Optional
import datetime

class MLPredictionCreate(BaseModel):
    message_id: Optional[int] = None
    input_text: str
    prediction: Optional[str] = None

class MLPredictionResponse(BaseModel):
    id: int
    message_id: Optional[int]
    input_text: str
    prediction: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True