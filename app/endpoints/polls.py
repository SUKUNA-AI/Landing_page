from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import polls
from ..dao import PollDAO
from typing import List

router = APIRouter(prefix="/polls", tags=["polls"])

@router.post("/", response_model=polls.PollResponse)
async def create_poll(poll_data: polls.PollCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый опрос."""
    return await PollDAO.create(db, poll_data.dict())

@router.get("/{telegram_user_id}", response_model=List[polls.PollResponse])
async def get_polls(telegram_user_id: str, db: AsyncSession = Depends(get_db)):
    """Получает опросы по telegram_user_id."""
    query = (
        polls.Poll.__table__.select()
        .where(polls.Poll.telegram_user_id == telegram_user_id)
    )
    result = await db.execute(query)
    polls_list = result.fetchall()
    if not polls_list:
        raise HTTPException(status_code=404, detail="Polls not found")
    return polls_list

@router.put("/{poll_id}", response_model=polls.PollResponse)
async def update_poll(poll_id: int, poll_data: polls.PollUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные опроса."""
    poll = await PollDAO.get_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    update_data = poll_data.dict(exclude_unset=True)
    query = (
        polls.Poll.__table__.update()
        .where(polls.Poll.id == poll_id)
        .values(**update_data)
        .returning(polls.Poll.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_poll = result.first()
    if not updated_poll:
        raise HTTPException(status_code=404, detail="Poll not found after update")
    return updated_poll

@router.delete("/{poll_id}", status_code=204)
async def delete_poll(poll_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет опрос по ID."""
    poll = await PollDAO.get_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    query = polls.Poll.__table__.delete().where(polls.Poll.id == poll_id)
    await db.execute(query)
    await db.commit()