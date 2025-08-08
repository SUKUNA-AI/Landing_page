import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from app.config import settings
from app.telegram_bot.handlers import start, rag, channel, projects, help, rag_query
from app.services.github_service import sync_projects_with_github

logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info(f"Bot started with ID: {bot.id}")
    try:
        chat = await bot.get_chat(settings.CHANNEL_ID)
        logger.info(f"Channel accessible: {chat.id}, {chat.title}")
    except Exception as e:
        logger.error(f"Cannot access channel {settings.CHANNEL_ID}: {str(e)}")
    logger.info("Starting project sync tasks")
    asyncio.create_task(sync_projects_with_github())
    asyncio.create_task(schedule_sync_projects())

async def schedule_sync_projects():
    while True:
        try:
            await sync_projects_with_github()
            logger.info("Projects synced successfully")
        except Exception as e:
            logger.error(f"Error syncing projects: {str(e)}")
        await asyncio.sleep(86400)

async def main():
    print("Initializing bot...")
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/bot.log"),
            logging.StreamHandler()
        ]
    )
    logger.info("Starting bot initialization")
    try:
        logger.info("Creating Bot instance")
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        logger.info("Registering handlers")
        start.register_start_handlers(dp, bot)
        rag.register_rag_handlers(dp, bot)
        channel.register_channel_handlers(dp, bot)
        projects.register_projects_handlers(dp, bot)
        help.register_help_handlers(dp, bot)
        rag_query.register_rag_query_handlers(dp, bot)
        dp.startup.register(on_startup)
        logger.info("Starting polling")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise

if __name__ == "__main__":
    print("Running bot.py...")
    asyncio.run(main())