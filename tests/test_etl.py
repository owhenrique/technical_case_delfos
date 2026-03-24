import pandas as pd

from src.etl.process import transform_data


def test_transform_data():
    df = pd.DataFrame({
        'timestamp': pd.date_range(
            '2025-01-01 00:00:00', periods=20, freq='1min'
        ),
        'wind_speed': [10.0] * 20,
        'power': [50.0] * 20,
    })

    signal_map = {
        'wind_speed_mean': 1,
        'wind_speed_min': 2,
        'wind_speed_max': 3,
        'wind_speed_std': 4,
        'power_mean': 5,
        'power_min': 6,
        'power_max': 7,
        'power_std': 8,
    }

    transformed = transform_data(df, signal_map)

    # We have 2 bins (10 minute intervals), and 8 signals.
    # Expected rows = 2 * 8 = 16
    expected_rows = 16
    assert len(transformed) == expected_rows
    assert 'timestamp' in transformed.columns
    assert 'signal_id' in transformed.columns
    assert 'value' in transformed.columns
