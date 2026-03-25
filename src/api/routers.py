import logging
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.api.database import get_fonte_repository
from src.api.limiter import limiter
from src.api.schemas import DataFonteResponse
from src.db.repositories.fonte_repository import FonteRepository

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/data', response_model=List[DataFonteResponse])
@limiter.limit('30/minute')
def get_data(
    request: Request,
    start_time: Annotated[
        datetime, Query(..., description='Start of the interval')
    ],
    end_time: Annotated[
        datetime, Query(..., description='End of the interval')
    ],
    variables: Annotated[
        List[str],
        Query(
            ...,
            description='Variables to query, e.g. wind_speed, power',
        ),
    ],
    repo: Annotated[FonteRepository, Depends(get_fonte_repository)],
):
    """
    Recupera dados temporais do banco Fonte em um intervalo.

    Aplica rate limiting de 30 requisicoes por minuto por IP.
    Valida as datas e as variaveis solicitadas antes de consultar
    o repositorio.

    Args:
        request (Request): Objeto da requisicao (usado pelo limiter).
        start_time (datetime): Data inicial do intervalo.
        end_time (datetime): Data final do intervalo.
        variables (List[str]): Colunas de interesse.
        repo (FonteRepository): Repositorio injetado via Depends.

    Returns:
        List[dict]: Registros filtrados da serie temporal.

    Raises:
        HTTPException: Se datas ou variaveis forem invalidas.
    """
    if start_time > end_time:
        logger.warning(
            'Intervalo invalido: start=%s > end=%s',
            start_time,
            end_time,
        )
        raise HTTPException(
            status_code=400,
            detail='start_time must be before end_time',
        )

    allowed = {
        'wind_speed',
        'power',
        'ambient_temperature',
    }
    for var in variables:
        if var not in allowed:
            logger.warning('Variavel invalida solicitada: %s', var)
            raise HTTPException(
                status_code=400,
                detail=f'Invalid variable: {var}',
            )

    try:
        logger.info(
            'Consultando dados: %s a %s | vars=%s',
            start_time,
            end_time,
            variables,
        )
        data = repo.get_data(start_time, end_time, variables)
        logger.info('Retornando %d registros', len(data))
        return data
    except Exception as e:
        logger.exception('Erro ao consultar dados: %s', e)
        raise HTTPException(status_code=500, detail=str(e))
