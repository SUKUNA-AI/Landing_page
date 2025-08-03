from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, get_db, Base
from .endpoints import (
    users as endpoints_users,
    profiles as endpoints_profiles,
    skills as endpoints_skills,
    projects as endpoints_projects,
    blog_posts as endpoints_blog_posts,
    tags as endpoints_tags,
    post_tags as endpoints_post_tags,
    project_tags as endpoints_project_tags,
    messages as endpoints_messages,
    social_media as endpoints_social_media,
    testimonials as endpoints_testimonials,
    telegram_subscribers as endpoints_telegram_subscribers,
    subscriber_preferences as endpoints_subscriber_preferences,
    polls as endpoints_polls,
    education as endpoints_education,
    work_experience as endpoints_work_experience,
    analytics as endpoints_analytics,
    ml_predictions as endpoints_ml_predictions,
    tasks as endpoints_tasks
)
from .models import (
    user as models_user,
    profile as models_profiles,
    skills as models_skills,
    projects as models_projects,
    blog_posts as models_blog_posts,
    tags as models_tags,
    post_tags as models_post_tags,
    project_tags as models_project_tags,
    messages as models_messages,
    social_media as models_social_media,
    testimonials as models_testimonials,
    telegram_subscribers as models_telegram_subscribers,
    subscriber_preferences as models_subscriber_preferences,
    polls as models_polls,
    education as models_education,
    work_experience as models_work_experience,
    analytics as models_analytics,
    ml_predictions as models_ml_predictions,
    tasks as models_tasks
)

app = FastAPI(title="Landing Page API", version="1.0.0")

# Подключение роутеров
app.include_router(endpoints_users.router)
app.include_router(endpoints_profiles.router)
app.include_router(endpoints_skills.router)
app.include_router(endpoints_projects.router)
app.include_router(endpoints_blog_posts.router)
app.include_router(endpoints_tags.router)
app.include_router(endpoints_post_tags.router)
app.include_router(endpoints_project_tags.router)
app.include_router(endpoints_messages.router)
app.include_router(endpoints_social_media.router)
app.include_router(endpoints_testimonials.router)
app.include_router(endpoints_telegram_subscribers.router)
app.include_router(endpoints_subscriber_preferences.router)
app.include_router(endpoints_polls.router)
app.include_router(endpoints_education.router)
app.include_router(endpoints_work_experience.router)
app.include_router(endpoints_analytics.router)
app.include_router(endpoints_ml_predictions.router)
app.include_router(endpoints_tasks.router)

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