import asyncio
from bot import setup_bot
from database import Session, User, Base, engine
from scheduler import setup_scheduler, send_daily_reminder
from llm import generate_followup_message
from config import TELEGRAM_BOT_TOKEN
import logging
from telegram import Bot
import json
from telegram.error import TelegramError

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
        message = generate_followup_message("Test User", "This is a test description for LLM integration.")
        logger.info(f"LLM generated message: {message}")
    except Exception as e:
        logger.error(f"LLM test failed: {e}")

async def test_send_message_to_hugo():
    logger.info("Testing sending a message to Hugo...")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token not found in environment variables.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    try:
        # Load Hugo's user ID from users.json
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        hugo_id = users['hugo']['telegram_id']

        if not hugo_id:
            logger.error("Failed to get Hugo's user ID from users.json.")
            return

        message = "Hello Hugo! This is a test message from your exercise reminder bot."
        await bot.send_message(chat_id=hugo_id, text=message)
        logger.info(f"Test message sent successfully to Hugo (ID: {hugo_id})")

    except FileNotFoundError:
        logger.error("users.json file not found.")
    except KeyError:
        logger.error("Hugo's information not found in users.json.")
    except TelegramError as te:
        logger.error(f"Telegram error: {te}")
    except Exception as e:
        logger.error(f"Failed to send test message: {e}")

async def get_all_chats():
    logger.info("Getting all chats...")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token not found in environment variables.")
        return
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    chats = await bot.get_updates()
    for chat in chats:
        logger.info(f"Chat ID: {chat.message.chat_id}, Username: {chat.message.from_user.username}")

async def main():
    logger.info("Starting component tests...")
    
    # await test_database()
    # await test_telegram_bot()
    # await test_scheduler()
    # await test_llm()
    await test_send_message_to_hugo()
    # await get_all_chats()
    
    logger.info("All tests completed.")

if __name__ == "__main__":
    asyncio.run(main())