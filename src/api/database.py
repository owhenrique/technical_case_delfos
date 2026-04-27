import os

from src.db.repositories.fonte_repository import FonteRepository


def get_fonte_repository() -> FonteRepository:
    dsn = os.getenv(
        'DB_FONTE_DSN', 'postgresql://wind_etl:wind_etl@localhost:5433/fonte'
    )
    return FonteRepository(dsn)
