import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_stations():
    response = client.get('/stations')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'latitude' in data[0]
        assert 'longitude' in data[0]