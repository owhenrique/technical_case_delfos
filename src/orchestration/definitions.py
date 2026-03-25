import os

from dagster import Definitions, ScheduleDefinition, define_asset_job
from dotenv import load_dotenv

from src.orchestration.assets import etl_daily_asset
from src.orchestration.resources import (
    APIResource,
    FonteDBResource,
    TargetDBResource,
)

load_dotenv()

api_resource = APIResource(
    api_url=os.getenv('CONECTOR_API_URL', 'http://localhost:8000')
)
target_db_resource = TargetDBResource(
    db_alvo_url=os.getenv(
        'DB_ALVO_DSN', 'postgresql://delfos:delfos@localhost:5434/alvo'
    )
)

etl_job = define_asset_job(name='etl_daily_job', selection=[etl_daily_asset])

etl_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule='0 1 * * *',
)

defs = Definitions(
    assets=[etl_daily_asset],
    resources={
        'api': api_resource,
        'target_db': target_db_resource,
        'fonte_db': FonteDBResource(
            db_fonte_url=os.getenv(
                'DB_FONTE_DSN',
                'postgresql://delfos:delfos@localhost:5433/fonte',
            )
        ),
    },
    schedules=[etl_schedule],
    jobs=[etl_job],
)
