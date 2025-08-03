from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import users
from ..dao import UserDAO
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=users.UserResponse)
async def create_user(user_data: users.UserCreate, db: AsyncSession = Depends(get_db)):
    """Создает нового пользователя."""
    return await UserDAO.create(db, user_data.dict())

@router.get("/{user_id}", response_model=users.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает пользователя по ID."""
    user = await UserDAO.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[users.UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """Получает всех пользователей."""
    return await UserDAO.get_all(db)

@router.put("/{user_id}", response_model=users.UserResponse)
async def update_user(user_id: int, user_data: users.UserUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные пользователя."""
    user = await UserDAO.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_data.dict(exclude_unset=True)
    query = (
        users.User.__table__.update()
        .where(users.User.id == user_id)
        .values(**update_data)
        .returning(users.User.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_user = result.first()
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found after update")
    return updated_user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет пользователя по ID."""
    user = await UserDAO.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = users.User.__table__.delete().where(users.User.id == user_id)
    await db.execute(query)
    await db.commit()