from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import messages
from ..dao import MessageDAO
from typing import List

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=messages.MessageResponse)
async def create_message(message_data: messages.MessageCreate, db: AsyncSession = Depends(get_db)):
    """Создает новое сообщение."""
    return await MessageDAO.create(db, message_data.dict())

@router.get("/", response_model=List[messages.MessageResponse])
async def get_messages(db: AsyncSession = Depends(get_db)):
    """Получает все сообщения."""
    messages_list = await MessageDAO.get_all(db)
    if not messages_list:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages_list

@router.get("/{message_id}", response_model=messages.MessageResponse)
async def get_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """Получает сообщение по ID."""
    message = await MessageDAO.get_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.delete("/{message_id}", status_code=204)
async def delete_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет сообщение по ID."""
    message = await MessageDAO.get_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    query = messages.Message.__table__.delete().where(messages.Message.id == message_id)
    await db.execute(query)
    await db.commit()