from fastapi.testclient import TestClient
from app.main import create_app

def test_shorten_and_redirect():
    client = TestClient(create_app(), follow_redirects=False)
    created = client.post("/shorten", json={"url": "https://example.com/docs"}).json()
    response = client.get(created["short_path"])
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/docs"
