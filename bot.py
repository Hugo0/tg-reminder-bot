from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from database import Session, User

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.first_name}! I'm here to help you stay motivated with your exercise goals.")

async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    goal = ' '.join(context.args)
    
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            db_user = User(telegram_id=user.id, name=user.first_name)
        db_user.exercise_goal = goal
        session.add(db_user)
        session.commit()
    
    await update.message.reply_text(f"Great! Your exercise goal has been set to: {goal}")

def setup_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setgoal", set_goal))
    return application