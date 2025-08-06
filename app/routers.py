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
    prefix="/api/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    profiles.router,
    prefix="/api/profiles",
    tags=["profiles"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    skills.router,
    prefix="/api/skills",
    tags=["skills"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    projects.router,
    prefix="/api/projects",
    tags=["projects"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    blog_posts.router,
    prefix="/api/blog_posts",
    tags=["blog_posts"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    tags.router,
    prefix="/api/tags",
    tags=["tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    post_tags.router,
    prefix="/api/post_tags",
    tags=["post_tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    project_tags.router,
    prefix="/api/project_tags",
    tags=["project_tags"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    social_media.router,
    prefix="/api/social_media",
    tags=["social_media"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    testimonials.router,
    prefix="/api/testimonials",
    tags=["testimonials"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    education.router,
    prefix="/api/education",
    tags=["education"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    work_experience.router,
    prefix="/api/work_experience",
    tags=["work_experience"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    tasks.router,
    prefix="/api/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)
router.include_router(
    ml_predictions.router,
    prefix="/api/ml_predictions",
    tags=["ml_predictions"],
    dependencies=[Depends(get_current_user)]
)

# Подключение публичных роутеров без зависимостей
router.include_router(messages.router, prefix="/api/messages", tags=["messages"])
router.include_router(
    telegram_subscribers.router,
    prefix="/api/telegram_subscribers",
    tags=["telegram_subscribers"]
)
router.include_router(
    subscriber_preferences.router,
    prefix="/api/subscriber_preferences",
    tags=["subscriber_preferences"]
)
router.include_router(polls.router, prefix="/api/polls", tags=["polls"])
router.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])