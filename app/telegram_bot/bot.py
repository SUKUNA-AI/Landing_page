import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.config import settings
from app.telegram_bot.handlers import start, rag, channel, projects, help, rag_query
from app.services.github_service import sync_projects_with_github, close_session
from app.database import get_db, shutdown_db

logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info(f"Bot started with ID: {bot.id}")
    try:
        chat = await bot.get_chat(settings.CHANNEL_ID)
        logger.info(f"Channel accessible: {chat.id}, {chat.title}")
    except Exception as e:
        logger.error(f"Cannot access channel {settings.CHANNEL_ID}: {str(e)}")
    logger.info("Starting project sync tasks")
    try:
        async for db in get_db():
            await sync_projects_with_github(db)
            logger.info("Initial project sync completed")
            break
    except Exception as e:
        logger.error(f"Error during initial sync: {str(e)}")
    asyncio.create_task(schedule_sync_projects())

async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logger.info("Shutting down bot...")
    await bot.session.close()  # Закрываем сессию бота
    await close_session()  # Закрываем aiohttp сессию
    await shutdown_db()
    logger.info("Database engine closed.")

async def schedule_sync_projects():
    while True:
        try:
            async for db in get_db():
                await sync_projects_with_github(db)
                logger.info("Projects synced successfully")
                break
        except Exception as e:
            logger.error(f"Error syncing projects: {str(e)}")
        await asyncio.sleep(86400)  # Раз в сутки

async def main():
    print("Starting bot initialization...")
    try:
        print("Loading environment variables...")
        print(f"Bot token: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
        print("Creating logs directory...")
        os.makedirs("logs", exist_ok=True)
        print("Setting up logging...")
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("logs/bot.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logger.info("Starting bot initialization")
        print("Creating Bot instance...")
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode='MarkdownV2'))
        dp = Dispatcher()
        print("Registering handlers...")
        start.register_start_handlers(dp, bot)
        await rag.register_rag_handlers(dp, bot)
        channel.register_channel_handlers(dp, bot)
        projects.register_projects_handlers(dp, bot)
        help.register_help_handlers(dp, bot)
        rag_query.register_rag_query_handlers(dp)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        print("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Failed to start bot: {str(e)}")
        logger.error(f"Failed to start bot: {str(e)}")
        raise
    finally:
        await close_session()
        await shutdown_db()

if __name__ == "__main__":
    print("Running bot.py...")
    asyncio.run(main())