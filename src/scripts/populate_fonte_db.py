import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

from src.repositories.fonte_repository import FonteRepository

load_dotenv()

dsn = os.getenv('DB_FONTE_DSN')


def main():
    start_time = datetime(2025, 1, 1, 0, 0, 0)
    end_time = start_time + timedelta(days=11)

    timestamps = pd.date_range(
        start=start_time, end=end_time, freq='1min', inclusive='left'
    )
    np.random.seed(42)
    wind_speed = np.random.uniform(0, 20, size=len(timestamps))
    power = np.clip(
        wind_speed**3 / 10 + np.random.normal(0, 50, len(timestamps)), 0, None
    )
    ambient_temperature = np.random.uniform(15, 35, size=len(timestamps))

    df = pd.DataFrame({
        'timestamp': timestamps,
        'wind_speed': wind_speed,
        'power': power,
        'ambient_temperature': ambient_temperature,
    })

    records = list(df.itertuples(index=False, name=None))

    repo = FonteRepository(dsn)
    repo.setup_database()

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO data (timestamp, wind_speed, power, ambient_temperature)
        VALUES %s
        ON CONFLICT (timestamp) DO NOTHING
    """

    execute_values(cur, insert_sql, records)
    conn.commit()
    cur.close()
    conn.close()

    print(f'Inseridos {len(records)} registros de {start_time} ate {end_time}')


if __name__ == '__main__':
    main()
