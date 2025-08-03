from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import testimonials
from ..dao import TestimonialDAO
from typing import List

router = APIRouter(prefix="/testimonials", tags=["testimonials"])

@router.post("/", response_model=testimonials.TestimonialResponse)
async def create_testimonial(testimonial_data: testimonials.TestimonialCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый отзыв."""
    return await TestimonialDAO.create(db, testimonial_data.dict())

@router.get("/{user_id}", response_model=List[testimonials.TestimonialResponse])
async def get_testimonials(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает отзывы пользователя по его ID."""
    testimonials_list = await TestimonialDAO.get_by_user_id(db, user_id)
    if not testimonials_list:
        raise HTTPException(status_code=404, detail="Testimonials not found")
    return testimonials_list

@router.put("/{testimonial_id}", response_model=testimonials.TestimonialResponse)
async def update_testimonial(testimonial_id: int, testimonial_data: testimonials.TestimonialUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные отзыва."""
    testimonial = await TestimonialDAO.get_by_id(db, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    update_data = testimonial_data.dict(exclude_unset=True)
    query = (
        testimonials.Testimonial.__table__.update()
        .where(testimonials.Testimonial.id == testimonial_id)
        .values(**update_data)
        .returning(testimonials.Testimonial.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_testimonial = result.first()
    if not updated_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found after update")
    return updated_testimonial

@router.delete("/{testimonial_id}", status_code=204)
async def delete_testimonial(testimonial_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет отзыв по ID."""
    testimonial = await TestimonialDAO.get_by_id(db, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    query = testimonials.Testimonial.__table__.delete().where(testimonials.Testimonial.id == testimonial_id)
    await db.execute(query)
    await db.commit()