import asyncio
from bot import setup_bot
from scheduler import setup_scheduler

def main():
    application = setup_bot()
    scheduler = setup_scheduler()
    
    scheduler.start()
    application.run_polling()
    
    scheduler.shutdown()

if __name__ == '__main__':
    print("Starting bot...")
    main()