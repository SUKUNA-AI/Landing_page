from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, select
from fastapi import HTTPException
from .base_dao import BaseDAO, T
from .. import models
import datetime

class UserDAO(BaseDAO):
    model = models.user.User

class ProfileDAO(BaseDAO):
    model = models.profile.Profile

class SkillDAO(BaseDAO):
    model = models.skills.Skill

class ProjectDAO(BaseDAO):
    model = models.projects.Project

class BlogPostDAO(BaseDAO):
    model = models.blog_posts.BlogPost

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        if not data.get("date_published"):
            data["date_published"] = datetime.datetime.utcnow()
        return await super(BlogPostDAO, cls).create(db, data)

class TagDAO(BaseDAO):
    model = models.tags.Tag

class PostTagDAO(BaseDAO):
    model = models.post_tags.PostTag

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        query = insert(cls.model.__table__).values(**data)
        result = await db.execute(query)
        await db.commit()
        query = select(cls.model.__table__).where(
            (cls.model.post_id == data["post_id"]) &
            (cls.model.tag_id == data["tag_id"])
        )
        result = await db.execute(query)
        item = result.first()
        if item is None:
            raise HTTPException(status_code=404, detail="PostTag not found after creation")
        return item

class ProjectTagDAO(BaseDAO):
    model = models.project_tags.ProjectTag

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        query = insert(cls.model.__table__).values(**data)
        result = await db.execute(query)
        await db.commit()
        query = select(cls.model.__table__).where(
            (cls.model.project_id == data["project_id"]) &
            (cls.model.tag_id == data["tag_id"])
        )
        result = await db.execute(query)
        item = result.first()
        if item is None:
            raise HTTPException(status_code=404, detail="ProjectTag not found after creation")
        return item

class MessageDAO(BaseDAO):
    model = models.messages.Message

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        data["date_sent"] = datetime.datetime.utcnow()
        return await super(MessageDAO, cls).create(db, data)

class SocialMediaDAO(BaseDAO):
    model = models.social_media.SocialMedia

class TestimonialDAO(BaseDAO):
    model = models.testimonials.Testimonial

class TelegramSubscriberDAO(BaseDAO):
    model = models.telegram_subscribers.TelegramSubscriber

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        data["subscribed_at"] = datetime.datetime.utcnow()
        return await super(TelegramSubscriberDAO, cls).create(db, data)

class SubscriberPreferenceDAO(BaseDAO):
    model = models.subscriber_preferences.SubscriberPreference

class PollDAO(BaseDAO):
    model = models.polls.Poll

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        data["created_at"] = datetime.datetime.utcnow()
        return await super(PollDAO, cls).create(db, data)

class EducationDAO(BaseDAO):
    model = models.education.Education

class WorkExperienceDAO(BaseDAO):
    model = models.work_experience.WorkExperience

class AnalyticsDAO(BaseDAO):
    model = models.analytics.Analytic

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        data["visit_time"] = datetime.datetime.utcnow()
        return await super(AnalyticsDAO, cls).create(db, data)

class TaskDAO(BaseDAO):
    model = models.tasks.Task

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        return await super(TaskDAO, cls).create(db, data, set_timestamps=True)

class MLPredictionDAO(BaseDAO):
    model = models.ml_predictions.MLPrediction

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        data["created_at"] = datetime.datetime.utcnow()
        return await super(MLPredictionDAO, cls).create(db, data)