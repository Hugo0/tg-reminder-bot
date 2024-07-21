from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database import Session, User
from bot import setup_bot
from datetime import datetime, timedelta
from llm import generate_followup_message
import pytz
import sys

async def send_daily_reminder():
    application = setup_bot()
    await application.initialize()
    await application.start()
    
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            now = datetime.now(pytz.timezone(user.timezone))
            if now.strftime("%H:%M") == user.reminder_time or '--send-now' in sys.argv:
                await application.bot.send_message(chat_id=user.telegram_id, text=f"Don't forget to take your protein shake, {user.name}!")
                user.last_reminder_sent = now
                user.reminder_sent = True
        session.commit()
    
    await application.stop()

async def check_responses():
    bot = setup_bot().bot
    with Session() as session:
        users = session.query(User).filter(User.reminder_sent == True).all()
        for user in users:
            if user.last_reminder_sent and datetime.now(pytz.timezone(user.timezone)) - user.last_reminder_sent > timedelta(minutes=30):
                if not user.last_response or user.last_response.lower() != "yes":
                    followup_message = generate_followup_message(user.name, user.description)
                    await bot.send_message(chat_id=user.telegram_id, text=followup_message)
                user.reminder_sent = False
        session.commit()

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_reminder, CronTrigger(minute='*'))  # Check every minute
    scheduler.add_job(check_responses, CronTrigger(minute='*/5'))  # Check every 5 minutes
    return scheduler