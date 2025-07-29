from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, get_db, Base
from .routers import router
from .models import (
    user, profile, skills, projects, blog_posts, tags, post_tags, project_tags,
    messages, social_media, testimonials, telegram_subscribers, subscriber_preferences,
    polls, education, work_experience, analytics, tasks, ml_predictions
)

app = FastAPI(title="Landing Page API", version="1.0.0")

# Подключение роутера
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the Landing Page API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}