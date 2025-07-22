from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind= engine, class_=AsyncSession, expire_on_commit=False)
Base = DeclarativeBase()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()