from sqlalchemy import Column, DateTime, Float
from sqlalchemy.orm import declarative_base

BaseFonte = declarative_base()


class DataFonte(BaseFonte):
    """
    Mapeamento ORM da tabela 'data' no banco Fonte.

    Guarda de forma tabular e plana (Wide Data) os dados brutos
    adquiridos minuto a minuto das fontes de geracao de energia.
    """

    __tablename__ = 'data'

    timestamp = Column(DateTime, primary_key=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)
