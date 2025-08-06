import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import settings
from app.telegram_bot.handlers.start import register_start_handles
from app.telegram_bot.handlers.projects import register_projects_handles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def register_handlers():
    register_start_handles(dp)
    register_projects_handles(dp)

async def main():
    logger.info("Starting telegram bot")
    register_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
