from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database import Session, User
from bot import setup_bot

async def send_daily_reminder():
    bot = setup_bot().bot
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            await bot.send_message(chat_id=user.telegram_id, text=f"Don't forget your daily exercise! Your goal: {user.exercise_goal}")
            user.reminder_sent = True
        session.commit()

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_reminder, CronTrigger(hour=9, minute=0))  # Sends reminder at 9:00 AM daily
    return scheduler