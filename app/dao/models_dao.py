from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update
from sqlalchemy.sql import insert, select
from fastapi import HTTPException
from .base_dao import BaseDAO, T
from .. import models
import datetime
from aiogram import Bot

from ..models import Project, BlogPost, ProjectTag, Tag


class UserDAO(BaseDAO):
    model = models.user.User

    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str) -> T | None:
        query = select(cls.model).where(cls.model.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        query = insert(cls.model.__table__).values(**data)
        result = await db.execute(query)
        await db.commit()
        query = select(cls.model.__table__).where(cls.model.id == result.inserted_primary_key[0])
        result = await db.execute(query)
        item = result.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="User not found after creation")
        return item

class ProfileDAO(BaseDAO):
    model = models.profile.Profile

class SkillDAO(BaseDAO):
    model = models.skills.Skill


class ProjectDAO:
    @staticmethod
    async def create(db: AsyncSession, project_data: dict):
        stmt = insert(Project).values(**project_data)
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Project))
        return result.scalars().all()

    @staticmethod
    async def create_or_update(db: AsyncSession, project_data: dict):
        result = await db.execute(
            select(Project).filter_by(project_url=project_data["project_url"])
        )
        project = result.scalars().first()
        if project:
            await db.execute(
                update(Project)
                .where(Project.project_url == project_data["project_url"])
                .values(**project_data)
            )
            await db.commit()
            return project
        else:
            stmt = insert(Project).values(**project_data)
            await db.execute(stmt)
            await db.commit()
            return (await db.execute(
                select(Project).filter_by(project_url=project_data["project_url"])
            )).scalars().first()


class BlogPostDAO(BaseDAO):
    model = models.BlogPost

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        query = insert(cls.model.__table__).values(**data)
        result = await db.execute(query)
        await db.commit()
        query = select(cls.model.__table__).where(cls.model.id == result.inserted_primary_key[0])
        result = await db.execute(query)
        item = result.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="BlogPost not found after creation")
        return item

    @classmethod
    async def get_by_id(cls, db: AsyncSession, item_id: int) -> T | None:
        query = select(cls.model.id, cls.model.user_id, cls.model.title, cls.model.content, cls.model.summary).where(cls.model.id == item_id)
        result = await db.execute(query)
        return result.first()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List[T]:
        query = select(cls.model.id, cls.model.user_id, cls.model.title, cls.model.content, cls.model.summary)
        result = await db.execute(query)
        return result.fetchall()

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

    @classmethod
    async def get_all_with_tags(cls, db: AsyncSession) -> List[T]:
        query = select(ProjectTag.project_id, ProjectTag.tag_id, Tag.tag_name).join(Tag, ProjectTag.tag_id == Tag.id)
        result = await db.execute(query)
        return result.fetchall()

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
    async def get_by_telegram_user_id(cls, db: AsyncSession, telegram_user_id: str) -> T | None:
        query = select(cls.model).where(cls.model.telegram_user_id == telegram_user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> T:
        query = insert(cls.model.__table__).values(**data).returning(cls.model.__table__)
        result = await db.execute(query)
        await db.commit()
        item = result.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Subscriber not found after creation")
        return item

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