from fastapi.testclient import TestClient
from app.main import create_app

def test_notes_crud():
    client = TestClient(create_app())
    created = client.post("/notes", json={"title": "Buy milk", "body": "2 liters"}).json()
    assert created["id"] == 1
    assert client.get("/notes").json()[0]["title"] == "Buy milk"
    updated = client.put("/notes/1", json={"title": "Buy milk", "body": "3 liters"}).json()
    assert updated["body"] == "3 liters"
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404
