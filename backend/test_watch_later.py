import pytest
from fastapi.testclient import TestClient

import app as main
import db
from auth import get_current_user_id

client = TestClient(main.app)


@pytest.fixture
def signed_in():
    main.app.dependency_overrides[get_current_user_id] = lambda: "user-1"
    yield
    main.app.dependency_overrides.clear()


@pytest.fixture
def saved(monkeypatch):
    calls = []
    monkeypatch.setattr(db, "add_to_watch_later", lambda *args: calls.append(args))
    return calls


def test_save_requires_sign_in():
    response = client.post("/api/watch-later", json={"tmdb_id": 27205})

    assert response.status_code == 401


def test_save_uses_real_title_from_tmdb(monkeypatch, signed_in, saved):
    async def fake_details(movie_id):
        return {"title": "Inception", "poster_path": "/poster.jpg"}

    monkeypatch.setattr(main, "get_movie_details", fake_details)

    response = client.post("/api/watch-later", json={"tmdb_id": 27205})

    assert response.status_code == 200
    assert response.json() == {"saved": True, "tmdb_id": 27205}
    assert saved == [("user-1", 27205, "Inception", "/poster.jpg")]


def test_save_unknown_film_is_404(monkeypatch, signed_in, saved):
    async def fake_details(movie_id):
        return None

    monkeypatch.setattr(main, "get_movie_details", fake_details)

    response = client.post("/api/watch-later", json={"tmdb_id": 999999999})

    assert response.status_code == 404
    assert saved == []