import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import MessageDAO, MLPredictionDAO
from app.database import get_db
from app.services.rag import get_rag_response
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

rag_router = APIRouter(prefix="/rag", tags=["rag"])


class RagRequest(BaseModel):
    question: str


@rag_router.post("/", response_model=dict)
async def process_rag_query(request: RagRequest, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для обработки запросов к RAG-агенту.
    Принимает вопрос и возвращает сгенерированный ответ на основе знаний из БД.
    Публичный эндпоинт, доступный без аутентификации.
    """
    try:
        logger.info(f"Received RAG query: {request.question}")
        response = await get_rag_response(request.question, db)
        return {"answer": response}
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while processing query")


# Новый эндпоинт для обработки /api/query (для обратной совместимости с закомментированным блоком)
@rag_router.post("/query", response_model=dict)
async def log_query(request: dict, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для логирования запросов и ответов RAG-агента.
    Используется в services/rag.py для сохранения данных в сторонний API (в данном случае, локальный).
    """
    try:
        query = request.get("query")
        response = request.get("response")
        if not query or not response:
            raise HTTPException(status_code=400, detail="Missing query or response in request")

        logger.info(f"Logging query: {query[:100]}...")
        async for db in get_db():
            message = await MessageDAO.create(db, {
                "name": "RAG API",
                "email": "api@portfolio.com",
                "message": query,
                "source": "rag_api",
                "date_sent": datetime.datetime.utcnow()
            })
            await MLPredictionDAO.create(db, {
                "message_id": message.id,
                "input_text": query,
                "prediction": response,
                "created_at": datetime.datetime.utcnow()
            })
            break

        return {"status": "logged", "query": query, "response": response}
    except Exception as e:
        logger.error(f"Error logging query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error logging query")