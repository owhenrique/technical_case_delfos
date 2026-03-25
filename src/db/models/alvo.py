from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

BaseAlvo = declarative_base()


class Signal(BaseAlvo):
    """
    Mapeamento ORM da tabela de dimensao 'signal'.

    Responsavel por armazenar o dicionario das variaveis agregadas,
    vinculando o nome textual do sinal a um ID inteiro persistente.
    """

    __tablename__ = 'signal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class DataAlvo(BaseAlvo):
    """
    Mapeamento ORM da tabela fato 'data' do banco Alvo.

    Armazena os valores calculados pelo ETL de forma pivotada
    (Long Data), correlacionando o timestamp com o sinal processado.
    """

    __tablename__ = 'data'

    timestamp = Column(DateTime, primary_key=True)
    signal_id = Column(Integer, ForeignKey('signal.id'), primary_key=True)
    value = Column(Float, nullable=False)
