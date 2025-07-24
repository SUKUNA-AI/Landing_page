from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Создание подкласса DeclarativeBase
class Base(DeclarativeBase):
    pass

DATABASE_URL = "postgresql+asyncpg://postgres:qwerty12345@localhost:5432/portfolio"
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для отладки
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as db:
        yield db
        await db.close()