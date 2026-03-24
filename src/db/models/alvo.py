from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

BaseAlvo = declarative_base()


class Signal(BaseAlvo):
    __tablename__ = 'signal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class DataAlvo(BaseAlvo):
    __tablename__ = 'data'

    timestamp = Column(DateTime, primary_key=True)
    signal_id = Column(Integer, ForeignKey('signal.id'), primary_key=True)
    value = Column(Float, nullable=False)
