from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

Base = declarative_base()
engine = create_engine('sqlite:///exercise_bot.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
    exercise_goal = Column(String)
    last_response = Column(String)
    reminder_sent = Column(Boolean, default=False)
    reminder_time = Column(String)
    timezone = Column(String)
    description = Column(String)
    last_reminder_sent = Column(DateTime)


Base.metadata.create_all(engine)