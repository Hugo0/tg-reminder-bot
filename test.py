import asyncio
from bot import setup_bot
from database import Session, User, Base, engine
from scheduler import setup_scheduler, send_daily_reminder
from llm import generate_chiding_message
from config import TELEGRAM_BOT_TOKEN
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_database():
    logger.info("Testing database connection...")
    Base.metadata.create_all(engine)
    with Session() as session:
        try:
            session.query(User).first()
            logger.info("Database connection successful.")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

async def test_telegram_bot():
    logger.info("Testing Telegram bot...")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token not found in environment variables.")
        return
    
    application = setup_bot()
    try:
        await application.initialize()
        await application.start()
        logger.info("Telegram bot initialized successfully.")
        await application.stop()
    except Exception as e:
        logger.error(f"Telegram bot initialization failed: {e}")

async def test_scheduler():
    logger.info("Testing scheduler...")
    scheduler = setup_scheduler()
    try:
        scheduler.start()
        logger.info("Scheduler started successfully.")
        scheduler.shutdown()
    except Exception as e:
        logger.error(f"Scheduler test failed: {e}")

async def test_llm():
    logger.info("Testing LLM integration...")
    try:
        message = generate_chiding_message("Run 5km every day")
        logger.info(f"LLM generated message: {message}")
    except Exception as e:
        logger.error(f"LLM test failed: {e}")

async def main():
    logger.info("Starting component tests...")
    
    await test_database()
    await test_telegram_bot()
    await test_scheduler()
    await test_llm()
    
    logger.info("All tests completed.")

if __name__ == "__main__":
    asyncio.run(main())