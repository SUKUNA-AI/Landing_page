from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.rag import get_rag_response
from pydantic import BaseModel

router = APIRouter(prefix="/rag", tags=["rag"])

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QuestionRequest, db: AsyncSession = Depends(get_db)):
    response = await get_rag_response(request.question, db)
    if "Произошла ошибка" in response:
        raise HTTPException(status_code=500, detail=response)
    return {"answer": response}