from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src import database


class User(database.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String)
    phone_number = Column(String)
    ig_account = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
