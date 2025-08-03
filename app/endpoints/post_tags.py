from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import post_tags
from ..dao import PostTagDAO

router = APIRouter(prefix="/post_tags", tags=["post_tags"])

@router.post("/", response_model=post_tags.PostTagResponse)
async def create_post_tag(post_tag_data: post_tags.PostTagCreate, db: AsyncSession = Depends(get_db)):
    """Создает связь между постом блога и тегом."""
    return await PostTagDAO.create(db, post_tag_data.dict())

@router.delete("/{post_id}/{tag_id}", status_code=204)
async def delete_post_tag(post_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет связь между постом блога и тегом."""
    query = (
        post_tags.PostTag.__table__.delete()
        .where(post_tags.PostTag.post_id == post_id)
        .where(post_tags.PostTag.tag_id == tag_id)
    )
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="PostTag not found")