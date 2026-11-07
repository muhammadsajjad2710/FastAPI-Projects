from fastapi.testclient import TestClient
from app.main import create_app

def test_rate_limit():
    client = TestClient(create_app())
    assert client.get("/public").status_code == 200
    assert client.get("/public").status_code == 200
    assert client.get("/public").status_code == 200
    assert client.get("/public").status_code == 429
    assert client.get("/health").status_code == 200
