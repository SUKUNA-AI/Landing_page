from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, insert
from fastapi import HTTPException
from typing import Any, List, TypeVar, Generic
import datetime

T = TypeVar("T")

class BaseDAO(Generic[T]):
    model = None

    @classmethod
    async def create(cls, db: AsyncSession, data: dict, set_timestamps: bool = False) -> T:
        if set_timestamps:
            data.update({
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow()
            })
        query = insert(cls.model.__table__).values(**data)
        result = await db.execute(query)
        await db.commit()
        item_id = result.inserted_primary_key[0]
        query = select(cls.model.__table__).where(cls.model.id == item_id)
        result = await db.execute(query)
        return result.first()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, item_id: int) -> T:
        query = select(cls.model.__table__).where(cls.model.id == item_id)
        result = await db.execute(query)
        item = result.first()
        if item is None:
            raise HTTPException(status_code=404, detail=f"{cls.model.__name__} not found")
        return item

    @classmethod
    async def get_by_user_id(cls, db: AsyncSession, user_id: int) -> List[T]:
        query = select(cls.model.__table__).where(cls.model.user_id == user_id)
        result = await db.execute(query)
        return result.fetchall()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List[T]:
        query = select(cls.model.__table__)
        result = await db.execute(query)
        return result.fetchall()