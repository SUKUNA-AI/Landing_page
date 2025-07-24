import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:qwerty12345@localhost:5432/portfolio")