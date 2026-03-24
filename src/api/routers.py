from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.database import get_fonte_repository
from src.models.schemas import DataFonteResponse
from src.repositories.fonte_repository import FonteRepository

router = APIRouter()


@router.get('/data', response_model=List[DataFonteResponse])
def get_data(
    start_time: Annotated[
        datetime, Query(..., description='Start of the interval')
    ],
    end_time: Annotated[
        datetime, Query(..., description='End of the interval')
    ],
    variables: Annotated[
        List[str],
        Query(..., description='Variables to query, e.g. wind_speed, power'),
    ],
    repo: Annotated[FonteRepository, Depends(get_fonte_repository)],
):
    if start_time > end_time:
        raise HTTPException(
            status_code=400, detail='start_time must be before end_time'
        )

    allowed_variables = {'wind_speed', 'power', 'ambient_temperature'}
    for var in variables:
        if var not in allowed_variables:
            raise HTTPException(
                status_code=400, detail=f'Invalid variable: {var}'
            )

    try:
        data = repo.get_data(start_time, end_time, variables)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
