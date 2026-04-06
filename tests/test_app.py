from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "GitHub Cloud Connector"


def test_missing_token_returns_401() -> None:
    response = client.get("/github/me")
    assert response.status_code == 401
    assert "GitHub token missing" in response.json()["detail"]
