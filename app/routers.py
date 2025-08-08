from fastapi import APIRouter, Depends
from .endpoints import (
    users, profiles, skills, projects, blog_posts, tags, post_tags, project_tags,
    messages, social_media, testimonials, telegram_subscribers, subscriber_preferences,
    polls, education, work_experience, analytics, tasks, ml_predictions
)
from app.auth import router as auth_router
from app.auth import get_current_user

# Основной роутер для приложения
router = APIRouter()

# Подключение роутера auth для /auth/login (в самый верх)
router.include_router(auth_router, tags=["auth"])

# Подключение защищенных роутеров с зависимостью get_current_user
router.include_router(
    users.router,
    prefix="/api",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    profiles.router,
    prefix="/api",
    tags=["profiles"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    skills.router,
    prefix="/api",
    tags=["skills"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    projects.router,
    prefix="/api",
    tags=["projects"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    blog_posts.router,
    prefix="/api",
    tags=["blog_posts"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    tags.router,
    prefix="/api",
    tags=["tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    post_tags.router,
    prefix="/api",
    tags=["post_tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    project_tags.router,
    prefix="/api",
    tags=["project_tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    social_media.router,
    prefix="/api",
    tags=["social_media"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    testimonials.router,
    prefix="/api",
    tags=["testimonials"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    education.router,
    prefix="/api",
    tags=["education"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    work_experience.router,
    prefix="/api",
    tags=["work_experience"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    tasks.router,
    prefix="/api",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    ml_predictions.router,
    prefix="/api",
    tags=["ml_predictions"],
    dependencies=[Depends(get_current_user)]
)

# Подключение публичных роутеров без зависимостей
router.include_router(messages.router, prefix="/api/messages", tags=["messages"])
router.include_router(
    telegram_subscribers.router,
    prefix="/api",
    tags=["telegram_subscribers"]
)
router.include_router(
    subscriber_preferences.router,
    prefix="/api",
    tags=["subscriber_preferences"]
)
router.include_router(polls.router, prefix="/api", tags=["polls"])
router.include_router(analytics.router, prefix="/api", tags=["analytics"])