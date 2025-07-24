from fastapi import FastAPI
from .database import engine, Base
from .models import user, profile, skills, projects, blog_posts, tags, post_tags, project_tags, messages, social_media, testimonials, telegram_subscribers, subscriber_preferences, polls, education, work_experience, analytics, tasks, ml_predictions

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Landing Page API"}