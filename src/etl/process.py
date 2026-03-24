import httpx
import pandas as pd

from src.db.repositories.alvo_repository import AlvoRepository


def extract_data_from_api(target_date: str, api_url: str) -> pd.DataFrame:
    """Fetch wind_speed and power data for the target_date from Fonte API"""
    start_time = f'{target_date}T00:00:00'
    end_time = f'{target_date}T23:59:59'

    params = [
        ('start_time', start_time),
        ('end_time', end_time),
        ('variables', 'wind_speed'),
        ('variables', 'power'),
    ]

    response = httpx.get(f'{api_url}/data', params=params, timeout=30.0)
    response.raise_for_status()

    data = response.json()
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def transform_data(df: pd.DataFrame, signal_map: dict) -> pd.DataFrame:
    """Resample to 10-minutes and calculate mean, min, max, std"""
    if df.empty:
        return pd.DataFrame()

    df.set_index('timestamp', inplace=True)

    # Resample 10 minutes
    resampled = df.resample('10min').agg(['mean', 'min', 'max', 'std'])

    resampled.columns = [
        '_'.join(col).strip() for col in resampled.columns.values
    ]
    resampled.reset_index(inplace=True)

    melted = resampled.melt(
        id_vars=['timestamp'], var_name='signal_name', value_name='value'
    )

    melted = melted.dropna(subset=['value'])
    melted['signal_id'] = melted['signal_name'].map(signal_map)
    melted = melted.dropna(subset=['signal_id']).copy()
    melted['signal_id'] = melted['signal_id'].astype(int)

    melted.drop(columns=['signal_name'], inplace=True)
    return melted


def run_etl(target_date: str, api_url: str, db_alvo_url: str):
    """Executes the full Pipeline for a specific date"""
    df_raw = extract_data_from_api(target_date, api_url)
    if df_raw.empty:
        print(f'No data available for {target_date}')
        return

    repo = AlvoRepository(db_alvo_url)
    repo.setup_database()

    signal_map = repo.get_signal_map()

    df_transformed = transform_data(df_raw, signal_map)

    repo.save_aggregated_data(df_transformed)
    print(
        f'Successfully processed and saved {len(df_transformed)} records '
        f'for {target_date}'
    )
