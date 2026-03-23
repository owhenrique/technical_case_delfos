from datetime import datetime
from typing import List

from sqlalchemy import asc, create_engine, select
from sqlalchemy.orm import Session

from src.models.fonte import BaseFonte, DataFonte


class FonteRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def setup_database(self):
        """Create tables if they don't exist"""
        BaseFonte.metadata.create_all(self.engine)

    def get_data(
        self, start_time: datetime, end_time: datetime, variables: List[str]
    ) -> List[dict]:
        with Session(self.engine) as session:
            cols = [DataFonte.timestamp]
            for var in variables:
                if hasattr(DataFonte, var):
                    cols.append(getattr(DataFonte, var))

            stmt = (
                select(*cols)
                .where(
                    DataFonte.timestamp >= start_time,
                    DataFonte.timestamp <= end_time,
                )
                .order_by(asc(DataFonte.timestamp))
            )

            result = session.execute(stmt)
            return [dict(row._mapping) for row in result]
