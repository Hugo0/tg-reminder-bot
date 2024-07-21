from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from database import Session, User
from llm import generate_followup_message
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.first_name} (ID: {user.id}) started the bot")
    await update.message.reply_text(f"Hello {user.first_name}! I'm here to remind you about your protein shake. Your user ID is {user.id}.")

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) != 2:
        await update.message.reply_text("Please use the format: /setreminder HH:MM Timezone")
        return
    
    reminder_time, timezone = context.args
    
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            db_user = User(telegram_id=user.id, name=user.first_name)
        db_user.reminder_time = reminder_time
        db_user.timezone = timezone
        session.add(db_user)
        session.commit()
    
    await update.message.reply_text(f"Great! Your reminder has been set for {reminder_time} {timezone}.")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    response = update.message.text.lower()
    
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if db_user:
            db_user.last_response = response
            session.commit()
    
    if response == "yes":
        await update.message.reply_text("Great job! Keep up the good work!")
    else:
        await update.message.reply_text("I'll remind you again later.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    
    advice = generate_followup_message(user.first_name, f"{user.first_name} is asking for advice about: {message}")
    
    await update.message.reply_text(advice)

def setup_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setreminder", set_reminder))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

def load_users_from_json():
    with open('users.json', 'r') as f:
        users_data = json.load(f)
    
    with Session() as session:
        for username, data in users_data.items():
            user = session.query(User).filter_by(telegram_id=data['telegram_id']).first()
            if not user:
                user = User(
                    telegram_id=data['telegram_id'],
                    name=data['name'],
                    reminder_time=data['reminder_time'],
                    timezone=data['timezone'],
                    description=data['description']
                )
                session.add(user)
        session.commit()