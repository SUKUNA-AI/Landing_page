from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .schemas import (
    users, profile, skills, projects, blog_posts, tags, post_tags, project_tags,
    messages, social_media, testimonials, telegram_subscribers, subscriber_preferences,
    polls, education, work_experience, analytics, tasks, ml_predictions
)
from .dao import (
    UserDAO, ProfileDAO, SkillDAO, ProjectDAO, BlogPostDAO, TagDAO,
    PostTagDAO, ProjectTagDAO, MessageDAO, SocialMediaDAO, TestimonialDAO,
    TelegramSubscriberDAO, SubscriberPreferenceDAO, PollDAO, EducationDAO,
    WorkExperienceDAO, AnalyticsDAO, TaskDAO, MLPredictionDAO
)
from .auth import get_current_user, create_access_token, verify_password, hash_password
from .qwen_api import generate_blog_content
from typing import List

router = APIRouter(prefix="/api", tags=["landing_page"])

# Login endpoint
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@router.post("/users/", response_model=users.UserResponse)
async def create_user(user_data: users.UserCreate, db: AsyncSession = Depends(get_db)):
    user_data.password_hash = hash_password(user_data.password_hash)  # Хешируем пароль
    return await UserDAO.create(db, user_data.dict())

@router.get("/users/{user_id}", response_model=users.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserDAO.get_by_id(db, user_id)

# Profile endpoints
@router.post("/profiles/", response_model=profile.ProfileResponse)
async def create_profile(profile_data: profile.ProfileCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await ProfileDAO.create(db, profile_data.dict())

@router.get("/profiles/{user_id}", response_model=profile.ProfileResponse)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    profiles = await ProfileDAO.get_by_user_id(db, user_id)
    if not profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profiles[0]

# Skill endpoints
@router.post("/skills/", response_model=skills.SkillResponse)
async def create_skill(skill_data: skills.SkillCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await SkillDAO.create(db, skill_data.dict())

@router.get("/skills/{user_id}", response_model=List[skills.SkillResponse])
async def get_skills(user_id: int, db: AsyncSession = Depends(get_db)):
    return await SkillDAO.get_by_user_id(db, user_id)

# Project endpoints
@router.post("/projects/", response_model=projects.ProjectResponse)
async def create_project(project_data: projects.ProjectCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await ProjectDAO.create(db, project_data.dict())

@router.get("/projects/{user_id}", response_model=List[projects.ProjectResponse])
async def get_projects(user_id: int, db: AsyncSession = Depends(get_db)):
    return await ProjectDAO.get_by_user_id(db, user_id)

# BlogPost endpoints
@router.post("/blog_posts/", response_model=blog_posts.BlogPostResponse)
async def create_blog_post(post_data: blog_posts.BlogPostCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await BlogPostDAO.create(db, post_data.dict())

@router.post("/blog_posts/generate", response_model=blog_posts.BlogPostResponse)
async def generate_blog_post(post_data: blog_posts.BlogPostCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    # Генерируем контент через API Qwen
    generated_content = await generate_blog_content(f"Write a blog post about {post_data.title}")
    post_data.content = generated_content
    return await BlogPostDAO.create(db, post_data.dict())

@router.get("/blog_posts/{user_id}", response_model=List[blog_posts.BlogPostResponse])
async def get_blog_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    return await BlogPostDAO.get_by_user_id(db, user_id)

# Tag endpoints
@router.post("/tags/", response_model=tags.TagResponse)
async def create_tag(tag_data: tags.TagCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await TagDAO.create(db, tag_data.dict())

@router.get("/tags/", response_model=List[tags.TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    return await TagDAO.get_all(db)

# PostTag endpoints
@router.post("/post_tags/", response_model=post_tags.PostTagResponse)
async def create_post_tag(post_tag_data: post_tags.PostTagCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await PostTagDAO.create(db, post_tag_data.dict())

# ProjectTag endpoints
@router.post("/project_tags/", response_model=project_tags.ProjectTagResponse)
async def create_project_tag(project_tag_data: project_tags.ProjectTagCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await ProjectTagDAO.create(db, project_tag_data.dict())

# Message endpoints
@router.post("/messages/", response_model=messages.MessageResponse)
async def create_message(message_data: messages.MessageCreate, db: AsyncSession = Depends(get_db)):
    return await MessageDAO.create(db, message_data.dict())

@router.get("/messages/", response_model=List[messages.MessageResponse])
async def get_messages(db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await MessageDAO.get_all(db)

# SocialMedia endpoints
@router.post("/social_media/", response_model=social_media.SocialMediaResponse)
async def create_social_media(social_data: social_media.SocialMediaCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await SocialMediaDAO.create(db, social_data.dict())

@router.get("/social_media/{user_id}", response_model=List[social_media.SocialMediaResponse])
async def get_social_media(user_id: int, db: AsyncSession = Depends(get_db)):
    return await SocialMediaDAO.get_by_user_id(db, user_id)

# Testimonial endpoints
@router.post("/testimonials/", response_model=testimonials.TestimonialResponse)
async def create_testimonial(testimonial_data: testimonials.TestimonialCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await TestimonialDAO.create(db, testimonial_data.dict())

@router.get("/testimonials/{user_id}", response_model=List[testimonials.TestimonialResponse])
async def get_testimonials(user_id: int, db: AsyncSession = Depends(get_db)):
    return await TestimonialDAO.get_by_user_id(db, user_id)

# TelegramSubscriber endpoints
@router.post("/telegram_subscribers/", response_model=telegram_subscribers.TelegramSubscriberResponse)
async def create_telegram_subscriber(subscriber_data: telegram_subscribers.TelegramSubscriberCreate, db: AsyncSession = Depends(get_db)):
    return await TelegramSubscriberDAO.create(db, subscriber_data.dict())

# SubscriberPreference endpoints
@router.post("/subscriber_preferences/", response_model=subscriber_preferences.SubscriberPreferenceResponse)
async def create_subscriber_preference(pref_data: subscriber_preferences.SubscriberPreferenceCreate, db: AsyncSession = Depends(get_db)):
    return await SubscriberPreferenceDAO.create(db, pref_data.dict())

# Poll endpoints
@router.post("/polls/", response_model=polls.PollResponse)
async def create_poll(poll_data: polls.PollCreate, db: AsyncSession = Depends(get_db)):
    return await PollDAO.create(db, poll_data.dict())

# Education endpoints
@router.post("/education/", response_model=education.EducationResponse)
async def create_education(edu_data: education.EducationCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await EducationDAO.create(db, edu_data.dict())

@router.get("/education/{user_id}", response_model=List[education.EducationResponse])
async def get_education(user_id: int, db: AsyncSession = Depends(get_db)):
    return await EducationDAO.get_by_user_id(db, user_id)

# WorkExperience endpoints
@router.post("/work_experience/", response_model=work_experience.WorkExperienceResponse)
async def create_work_experience(work_data: work_experience.WorkExperienceCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await WorkExperienceDAO.create(db, work_data.dict())

@router.get("/work_experience/{user_id}", response_model=List[work_experience.WorkExperienceResponse])
async def get_work_experience(user_id: int, db: AsyncSession = Depends(get_db)):
    return await WorkExperienceDAO.get_by_user_id(db, user_id)

# Analytics endpoints
@router.post("/analytics/", response_model=analytics.AnalyticsResponse)
async def create_analytics(analytics_data: analytics.AnalyticsCreate, db: AsyncSession = Depends(get_db)):
    return await AnalyticsDAO.create(db, analytics_data.dict())

# Task endpoints
@router.post("/tasks/", response_model=tasks.TaskResponse)
async def create_task(task_data: tasks.TaskCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await TaskDAO.create(db, task_data.dict())

@router.get("/tasks/{user_id}", response_model=List[tasks.TaskResponse])
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    return await TaskDAO.get_by_user_id(db, user_id)

# MLPrediction endpoints
@router.post("/ml_predictions/", response_model=ml_predictions.MLPredictionResponse)
async def create_ml_prediction(prediction_data: ml_predictions.MLPredictionCreate, db: AsyncSession = Depends(get_db), current_user: users.UserResponse = Depends(get_current_user)):
    return await MLPredictionDAO.create(db, prediction_data.dict())