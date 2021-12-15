from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src import database


class User(database.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String)
    phone_number = Column(String)
    ig_account = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    checks = relationship('Check', order_by='Check.created_at.desc()')


class Check(database.Base):
    __tablename__ = 'checks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    registered_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chances = relationship('Chance', order_by='Chance.check_id')


class Chance(database.Base):
    __tablename__ = 'chances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_id = Column(Integer, ForeignKey('checks.id'), nullable=False)


metadata = database.Base.metadata
