from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import blog_posts
from ..dao import BlogPostDAO
from typing import List

router = APIRouter(prefix="/blog_posts", tags=["blog_posts"])

@router.post("/", response_model=blog_posts.BlogPostResponse)
async def create_blog_post(post_data: blog_posts.BlogPostCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый пост в блоге."""
    return await BlogPostDAO.create(db, post_data.dict())

@router.get("/{user_id}", response_model=List[blog_posts.BlogPostResponse])
async def get_blog_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает посты блога пользователя по его ID."""
    posts = await BlogPostDAO.get_by_user_id(db, user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="Blog posts not found")
    return posts

@router.put("/{post_id}", response_model=blog_posts.BlogPostResponse)
async def update_blog_post(post_id: int, post_data: blog_posts.BlogPostUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные поста в блоге."""
    post = await BlogPostDAO.get_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    update_data = post_data.dict(exclude_unset=True)
    query = (
        blog_posts.BlogPost.__table__.update()
        .where(blog_posts.BlogPost.id == post_id)
        .values(**update_data)
        .returning(blog_posts.BlogPost.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_post = result.first()
    if not updated_post:
        raise HTTPException(status_code=404, detail="Blog post not found after update")
    return updated_post

@router.delete("/{post_id}", status_code=204)
async def delete_blog_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет пост блога по ID."""
    post = await BlogPostDAO.get_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    query = blog_posts.BlogPost.__table__.delete().where(blog_posts.BlogPost.id == post_id)
    await db.execute(query)
    await db.commit()