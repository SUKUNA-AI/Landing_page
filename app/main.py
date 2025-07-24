from fastapi import FastAPI
from database import engine
from models import user, profile, skills, projects, blog_posts, tags, post_tags, project_tags, messages, social_media, testimonials, telegram_subscribers, subscriber_preferences, polls, education, work_experience, analytics, tasks, ml_predictions

app = FastAPI()

# Создание таблиц
user.Base.metadata.create_all(bind=engine)
profile.Base.metadata.create_all(bind=engine)
skills.Base.metadata.create_all(bind=engine)
projects.Base.metadata.create_all(bind=engine)
blog_posts.Base.metadata.create_all(bind=engine)
tags.Base.metadata.create_all(bind=engine)
post_tags.Base.metadata.create_all(bind=engine)
project_tags.Base.metadata.create_all(bind=engine)
messages.Base.metadata.create_all(bind=engine)
social_media.Base.metadata.create_all(bind=engine)
testimonials.Base.metadata.create_all(bind=engine)
telegram_subscribers.Base.metadata.create_all(bind=engine)
subscriber_preferences.Base.metadata.create_all(bind=engine)
polls.Base.metadata.create_all(bind=engine)
education.Base.metadata.create_all(bind=engine)
work_experience.Base.metadata.create_all(bind=engine)
analytics.Base.metadata.create_all(bind=engine)
tasks.Base.metadata.create_all(bind=engine)
ml_predictions.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Portfolio API"}