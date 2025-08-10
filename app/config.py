import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import model_validator

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str | None = None
    JWT_SECRET_KEY: str = "your-secret-key-change-this"  # Секретный ключ для JWT
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str
    TELEGRAM_BOT_TOKEN: str
    GEMINI_API_KEY: str
    CHANNEL_ID: int
    GITHUB_TOKEN: str
    GITHUB_USER: str
    ADMIN_TELEGRAM_ID: int

    @model_validator(mode='after')
    def get_database_url(self):
        self.DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return self

    class Config:
        env_file = os.path.join(BASE_DIR, '.env')

settings = Settings()

