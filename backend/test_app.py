from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("backend.app.requests.get")
def test_get_random_movie(mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "results": [{
            "title": "fake Movie",
            "overview": "this is a fake movie for testing.",
            "release_date": "2026-01-01"
        }
        ]
    }
    mock_get.return_value = fake_response
    response = client.get("/api/random")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "overview" in data
    assert "date" in data