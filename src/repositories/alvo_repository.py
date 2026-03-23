import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.models.alvo import BaseAlvo, DataAlvo, Signal


class AlvoRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def setup_database(self):
        """Create tables if they don't exist and seed signals"""
        BaseAlvo.metadata.create_all(self.engine)
        self._seed_signals()

    def _seed_signals(self):
        expected_signals = []
        for var in ['wind_speed', 'power']:
            for agg in ['mean', 'min', 'max', 'std']:
                expected_signals.append(f'{var}_{agg}')

        with Session(self.engine) as session:
            for sig_name in expected_signals:
                existing = (
                    session.query(Signal).filter_by(name=sig_name).first()
                )
                if not existing:
                    session.add(Signal(name=sig_name))
            session.commit()

    def get_signal_map(self) -> dict:
        """Returns a mapping of signal name to signal_id"""
        with Session(self.engine) as session:
            signals = session.query(Signal).all()
            return {sig.name: sig.id for sig in signals}

    def save_aggregated_data(self, df: pd.DataFrame):
        """
        Expects a long-format DataFrame with columns: timestamp, signal_id,
        value.
        """
        if df.empty:
            return

        records = df.to_dict(orient='records')

        with Session(self.engine) as session:
            stmt = insert(DataAlvo).values(records)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=['timestamp', 'signal_id']
            )
            session.execute(stmt)
            session.commit()
