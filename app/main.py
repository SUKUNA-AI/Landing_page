from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, get_db, Base
from .routers import router
from .auth import hash_password
from .config import settings
from .dao.models_dao import UserDAO
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Landing Page API", version="1.0.0")

# Подключение общего роутера
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created or verified.")
        async for db in get_db():
            try:
                logger.info(f"Checking for admin user: {settings.ADMIN_USERNAME}")
                admin_user = await UserDAO.get_by_username(db, settings.ADMIN_USERNAME)
                if not admin_user:
                    logger.info("Admin user not found, creating...")
                    admin_data = {
                        "username": settings.ADMIN_USERNAME,
                        "password_hash": hash_password(settings.ADMIN_PASSWORD),
                        "email": settings.ADMIN_EMAIL,
                        "role": "admin"
                    }
                    await UserDAO.create(db, admin_data)
                    await db.commit()
                    logger.info("Admin user created successfully.")
                else:
                    logger.info("Admin user already exists.")
            except Exception as e:
                logger.error(f"Error during startup event: {str(e)}")
                raise
            finally:
                await db.close()
            break

@app.get("/")
async def root():
    return {"message": "Welcome to the Landing Page API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}