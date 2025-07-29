from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import (
    user, profile, skills, projects, blog_posts, tags, post_tags, project_tags,
    messages, social_media, testimonials, telegram_subscribers, subscriber_preferences,
    polls, education, work_experience, analytics, tasks, ml_predictions
)
from .schemas import (
    users, profile, skills, projects, blog_posts, tags, post_tags, project_tags,
    messages, social_media, testimonials, telegram_subscribers, subscriber_preferences,
    polls, education, work_experience, analytics, tasks, ml_predictions
)
from typing import List
import datetime

router = APIRouter(prefix="/api", tags=["landing_page"])

# User endpoints
@router.post("/users/", response_model=users.UserResponse)
async def create_user(user_data: users.UserCreate, db: AsyncSession = Depends(get_db)):
    query = user.User.__table__.insert().values(**user_data.dict())
    result = await db.execute(query)
    await db.commit()
    user_id = result.inserted_primary_key[0]
    query = user.User.__table__.select().where(user.User.id == user_id)
    new_user = await db.execute(query)
    return new_user.first()

@router.get("/users/{user_id}", response_model=users.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = user.User.__table__.select().where(user.User.id == user_id)
    result = await db.execute(query)
    db_user = result.first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Profile endpoints
@router.post("/profiles/", response_model=profile.ProfileResponse)
async def create_profile(profile_data: profile.ProfileCreate, db: AsyncSession = Depends(get_db)):
    query = profile.Profile.__table__.insert().values(**profile_data.dict())
    result = await db.execute(query)
    await db.commit()
    profile_id = result.inserted_primary_key[0]
    query = profile.Profile.__table__.select().where(profile.Profile.id == profile_id)
    new_profile = await db.execute(query)
    return new_profile.first()

@router.get("/profiles/{user_id}", response_model=profile.ProfileResponse)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    query = profile.Profile.__table__.select().where(profile.Profile.user_id == user_id)
    result = await db.execute(query)
    db_profile = result.first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

# Skill endpoints
@router.post("/skills/", response_model=skills.SkillResponse)
async def create_skill(skill_data: skills.SkillCreate, db: AsyncSession = Depends(get_db)):
    query = skills.Skills.__table__.insert().values(**skill_data.dict())
    result = await db.execute(query)
    await db.commit()
    skill_id = result.inserted_primary_key[0]
    query = skills.Skills.__table__.select().where(skills.Skills.id == skill_id)
    new_skill = await db.execute(query)
    return new_skill.first()

@router.get("/skills/{user_id}", response_model=List[skills.SkillResponse])
async def get_skills(user_id: int, db: AsyncSession = Depends(get_db)):
    query = skills.Skills.__table__.select().where(skills.Skills.user_id == user_id)
    result = await db.execute(query)
    skills_list = result.fetchall()
    return skills_list

# Project endpoints
@router.post("/projects/", response_model=projects.ProjectResponse)
async def create_project(project_data: projects.ProjectCreate, db: AsyncSession = Depends(get_db)):
    query = projects.Projects.__table__.insert().values(**project_data.dict())
    result = await db.execute(query)
    await db.commit()
    project_id = result.inserted_primary_key[0]
    query = projects.Projects.__table__.select().where(projects.Projects.id == project_id)
    new_project = await db.execute(query)
    return new_project.first()

@router.get("/projects/{user_id}", response_model=List[projects.ProjectResponse])
async def get_projects(user_id: int, db: AsyncSession = Depends(get_db)):
    query = projects.Projects.__table__.select().where(projects.Projects.user_id == user_id)
    result = await db.execute(query)
    projects_list = result.fetchall()
    return projects_list

# BlogPost endpoints
@router.post("/blog_posts/", response_model=blog_posts.BlogPostResponse)
async def create_blog_post(post_data: blog_posts.BlogPostCreate, db: AsyncSession = Depends(get_db)):
    if not post_data.date_published:
        post_data.date_published = datetime.datetime.utcnow()
    query = blog_posts.BlogPosts.__table__.insert().values(**post_data.dict())
    result = await db.execute(query)
    await db.commit()
    post_id = result.inserted_primary_key[0]
    query = blog_posts.BlogPosts.__table__.select().where(blog_posts.BlogPosts.id == post_id)
    new_post = await db.execute(query)
    return new_post.first()

@router.get("/blog_posts/{user_id}", response_model=List[blog_posts.BlogPostResponse])
async def get_blog_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    query = blog_posts.BlogPosts.__table__.select().where(blog_posts.BlogPosts.user_id == user_id)
    result = await db.execute(query)
    posts_list = result.fetchall()
    return posts_list

# Tag endpoints
@router.post("/tags/", response_model=tags.TagResponse)
async def create_tag(tag_data: tags.TagCreate, db: AsyncSession = Depends(get_db)):
    query = tags.Tags.__table__.insert().values(**tag_data.dict())
    result = await db.execute(query)
    await db.commit()
    tag_id = result.inserted_primary_key[0]
    query = tags.Tags.__table__.select().where(tags.Tags.id == tag_id)
    new_tag = await db.execute(query)
    return new_tag.first()

@router.get("/tags/", response_model=List[tags.TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    query = tags.Tags.__table__.select()
    result = await db.execute(query)
    tags_list = result.fetchall()
    return tags_list

# PostTag endpoints
@router.post("/post_tags/", response_model=post_tags.PostTagResponse)
async def create_post_tag(post_tag_data: post_tags.PostTagCreate, db: AsyncSession = Depends(get_db)):
    query = post_tags.PostTags.__table__.insert().values(**post_tag_data.dict())
    result = await db.execute(query)
    await db.commit()
    query = post_tags.PostTags.__table__.select().where(
        (post_tags.PostTags.post_id == post_tag_data.post_id) &
        (post_tags.PostTags.tag_id == post_tag_data.tag_id)
    )
    new_post_tag = await db.execute(query)
    return new_post_tag.first()

# ProjectTag endpoints
@router.post("/project_tags/", response_model=project_tags.ProjectTagResponse)
async def create_project_tag(project_tag_data: project_tags.ProjectTagCreate, db: AsyncSession = Depends(get_db)):
    query = project_tags.ProjectTags.__table__.insert().values(**project_tag_data.dict())
    result = await db.execute(query)
    await db.commit()
    query = project_tags.ProjectTags.__table__.select().where(
        (project_tags.ProjectTags.project_id == project_tag_data.project_id) &
        (project_tags.ProjectTags.tag_id == project_tag_data.tag_id)
    )
    new_project_tag = await db.execute(query)
    return new_project_tag.first()

# Message endpoints
@router.post("/messages/", response_model=messages.MessageResponse)
async def create_message(message_data: messages.MessageCreate, db: AsyncSession = Depends(get_db)):
    query = messages.Messages.__table__.insert().values(
        **message_data.dict(),
        date_sent=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    message_id = result.inserted_primary_key[0]
    query = messages.Messages.__table__.select().where(messages.Messages.id == message_id)
    new_message = await db.execute(query)
    return new_message.first()

@router.get("/messages/", response_model=List[messages.MessageResponse])
async def get_messages(db: AsyncSession = Depends(get_db)):
    query = messages.Messages.__table__.select()
    result = await db.execute(query)
    messages_list = result.fetchall()
    return messages_list

# SocialMedia endpoints
@router.post("/social_media/", response_model=social_media.SocialMediaResponse)
async def create_social_media(social_data: social_media.SocialMediaCreate, db: AsyncSession = Depends(get_db)):
    query = social_media.SocialMedia.__table__.insert().values(**social_data.dict())
    result = await db.execute(query)
    await db.commit()
    social_id = result.inserted_primary_key[0]
    query = social_media.SocialMedia.__table__.select().where(social_media.SocialMedia.id == social_id)
    new_social = await db.execute(query)
    return new_social.first()

@router.get("/social_media/{user_id}", response_model=List[social_media.SocialMediaResponse])
async def get_social_media(user_id: int, db: AsyncSession = Depends(get_db)):
    query = social_media.SocialMedia.__table__.select().where(social_media.SocialMedia.user_id == user_id)
    result = await db.execute(query)
    social_list = result.fetchall()
    return social_list

# Testimonial endpoints
@router.post("/testimonials/", response_model=testimonials.TestimonialResponse)
async def create_testimonial(testimonial_data: testimonials.TestimonialCreate, db: AsyncSession = Depends(get_db)):
    query = testimonials.Testimonials.__table__.insert().values(**testimonial_data.dict())
    result = await db.execute(query)
    await db.commit()
    testimonial_id = result.inserted_primary_key[0]
    query = testimonials.Testimonials.__table__.select().where(testimonials.Testimonials.id == testimonial_id)
    new_testimonial = await db.execute(query)
    return new_testimonial.first()

@router.get("/testimonials/{user_id}", response_model=List[testimonials.TestimonialResponse])
async def get_testimonials(user_id: int, db: AsyncSession = Depends(get_db)):
    query = testimonials.Testimonials.__table__.select().where(testimonials.Testimonials.user_id == user_id)
    result = await db.execute(query)
    testimonials_list = result.fetchall()
    return testimonials_list

# TelegramSubscriber endpoints
@router.post("/telegram_subscribers/", response_model=telegram_subscribers.TelegramSubscriberResponse)
async def create_telegram_subscriber(subscriber_data: telegram_subscribers.TelegramSubscriberCreate, db: AsyncSession = Depends(get_db)):
    query = telegram_subscribers.TelegramSubscribers.__table__.insert().values(
        **subscriber_data.dict(),
        subscribed_at=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    subscriber_id = result.inserted_primary_key[0]
    query = telegram_subscribers.TelegramSubscribers.__table__.select().where(telegram_subscribers.TelegramSubscribers.id == subscriber_id)
    new_subscriber = await db.execute(query)
    return new_subscriber.first()

# SubscriberPreference endpoints
@router.post("/subscriber_preferences/", response_model=subscriber_preferences.SubscriberPreferenceResponse)
async def create_subscriber_preference(pref_data: subscriber_preferences.SubscriberPreferenceCreate, db: AsyncSession = Depends(get_db)):
    query = subscriber_preferences.SubscriberPreferences.__table__.insert().values(**pref_data.dict())
    result = await db.execute(query)
    await db.commit()
    pref_id = result.inserted_primary_key[0]
    query = subscriber_preferences.SubscriberPreferences.__table__.select().where(subscriber_preferences.SubscriberPreferences.id == pref_id)
    new_pref = await db.execute(query)
    return new_pref.first()

# Poll endpoints
@router.post("/polls/", response_model=polls.PollResponse)
async def create_poll(poll_data: polls.PollCreate, db: AsyncSession = Depends(get_db)):
    query = polls.Polls.__table__.insert().values(
        **poll_data.dict(),
        created_at=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    poll_id = result.inserted_primary_key[0]
    query = polls.Polls.__table__.select().where(polls.Polls.id == poll_id)
    new_poll = await db.execute(query)
    return new_poll.first()

# Education endpoints
@router.post("/education/", response_model=education.EducationResponse)
async def create_education(edu_data: education.EducationCreate, db: AsyncSession = Depends(get_db)):
    query = education.Education.__table__.insert().values(**edu_data.dict())
    result = await db.execute(query)
    await db.commit()
    edu_id = result.inserted_primary_key[0]
    query = education.Education.__table__.select().where(education.Education.id == edu_id)
    new_edu = await db.execute(query)
    return new_edu.first()

@router.get("/education/{user_id}", response_model=List[education.EducationResponse])
async def get_education(user_id: int, db: AsyncSession = Depends(get_db)):
    query = education.Education.__table__.select().where(education.Education.user_id == user_id)
    result = await db.execute(query)
    edu_list = result.fetchall()
    return edu_list

# WorkExperience endpoints
@router.post("/work_experience/", response_model=work_experience.WorkExperienceResponse)
async def create_work_experience(work_data: work_experience.WorkExperienceCreate, db: AsyncSession = Depends(get_db)):
    query = work_experience.WorkExperience.__table__.insert().values(**work_data.dict())
    result = await db.execute(query)
    await db.commit()
    work_id = result.inserted_primary_key[0]
    query = work_experience.WorkExperience.__table__.select().where(work_experience.WorkExperience.id == work_id)
    new_work = await db.execute(query)
    return new_work.first()

@router.get("/work_experience/{user_id}", response_model=List[work_experience.WorkExperienceResponse])
async def get_work_experience(user_id: int, db: AsyncSession = Depends(get_db)):
    query = work_experience.WorkExperience.__table__.select().where(work_experience.WorkExperience.user_id == user_id)
    result = await db.execute(query)
    work_list = result.fetchall()
    return work_list

# Analytics endpoints
@router.post("/analytics/", response_model=analytics.AnalyticsResponse)
async def create_analytics(analytics_data: analytics.AnalyticsCreate, db: AsyncSession = Depends(get_db)):
    query = analytics.Analytics.__table__.insert().values(
        **analytics_data.dict(),
        visit_time=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    analytics_id = result.inserted_primary_key[0]
    query = analytics.Analytics.__table__.select().where(analytics.Analytics.id == analytics_id)
    new_analytics = await db.execute(query)
    return new_analytics.first()

# Task endpoints
@router.post("/tasks/", response_model=tasks.TaskResponse)
async def create_task(task_data: tasks.TaskCreate, db: AsyncSession = Depends(get_db)):
    query = tasks.Tasks.__table__.insert().values(
        **task_data.dict(),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    task_id = result.inserted_primary_key[0]
    query = tasks.Tasks.__table__.select().where(tasks.Tasks.id == task_id)
    new_task = await db.execute(query)
    return new_task.first()

@router.get("/tasks/{user_id}", response_model=List[tasks.TaskResponse])
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    query = tasks.Tasks.__table__.select().where(tasks.Tasks.user_id == user_id)
    result = await db.execute(query)
    tasks_list = result.fetchall()
    return tasks_list

# MLPrediction endpoints
@router.post("/ml_predictions/", response_model=ml_predictions.MLPredictionResponse)
async def create_ml_prediction(prediction_data: ml_predictions.MLPredictionCreate, db: AsyncSession = Depends(get_db)):
    query = ml_predictions.MLPredictions.__table__.insert().values(
        **prediction_data.dict(),
        created_at=datetime.datetime.utcnow()
    )
    result = await db.execute(query)
    await db.commit()
    prediction_id = result.inserted_primary_key[0]
    query = ml_predictions.MLPredictions.__table__.select().where(ml_predictions.MLPredictions.id == prediction_id)
    new_prediction = await db.execute(query)
    return new_prediction.first()