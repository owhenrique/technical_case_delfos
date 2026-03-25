from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DataFonteResponse(BaseModel):
    """
    Schema Pydantic para serializar respostas da API do banco Fonte.

    Representa um unico ponto de dado na serie temporal de geracao
    de energia. Variaveis omitidas da consulta retornam como None.
    """

    timestamp: datetime
    wind_speed: Optional[float] = None
    power: Optional[float] = None
    ambient_temperature: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
