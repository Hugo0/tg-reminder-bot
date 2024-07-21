import asyncio
import sys
from bot import setup_bot, load_users_from_json
from scheduler import setup_scheduler, send_daily_reminder

async def main():
    load_users_from_json()
    application = setup_bot()
    scheduler = setup_scheduler()
    
    scheduler.start()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--send-now":
        await send_daily_reminder()
        print("Sent immediate reminders to all users.")
    
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        print("Bot is running. Press Ctrl+C to stop.")
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Bot is shutting down...")
    finally:
        await application.stop()
        scheduler.shutdown()

if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())