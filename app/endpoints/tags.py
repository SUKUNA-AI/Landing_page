from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import tags
from ..dao import TagDAO
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/", response_model=tags.TagResponse)
async def create_tag(tag_data: tags.TagCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый тег."""
    return await TagDAO.create(db, tag_data.dict())

@router.get("/", response_model=List[tags.TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    """Получает все теги."""
    tags_list = await TagDAO.get_all(db)
    if not tags_list:
        raise HTTPException(status_code=404, detail="Tags not found")
    return tags_list

@router.put("/{tag_id}", response_model=tags.TagResponse)
async def update_tag(tag_id: int, tag_data: tags.TagUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные тега."""
    tag = await TagDAO.get_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    update_data = tag_data.dict(exclude_unset=True)
    query = (
        tags.Tag.__table__.update()
        .where(tags.Tag.id == tag_id)
        .values(**update_data)
        .returning(tags.Tag.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_tag = result.first()
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found after update")
    return updated_tag

@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет тег по ID."""
    tag = await TagDAO.get_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    query = tags.Tag.__table__.delete().where(tags.Tag.id == tag_id)
    await db.execute(query)
    await db.commit()