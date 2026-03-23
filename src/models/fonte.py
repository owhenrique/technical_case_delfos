from sqlalchemy import Column, DateTime, Float
from sqlalchemy.orm import declarative_base

BaseFonte = declarative_base()


class DataFonte(BaseFonte):
    __tablename__ = 'data'

    timestamp = Column(DateTime, primary_key=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)
