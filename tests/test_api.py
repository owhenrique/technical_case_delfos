from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


def test_get_data_invalid_time_range():
    response = client.get(
        '/data',
        params={
            'start_time': '2025-01-02T00:00:00',
            'end_time': '2025-01-01T00:00:00',
            'variables': ['wind_speed'],
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'start_time must be before end_time' in response.text
