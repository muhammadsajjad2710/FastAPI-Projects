from fastapi.testclient import TestClient
from app.main import create_app

def test_register_login_me():
    client = TestClient(create_app())
    assert client.post("/register", json={"username": "aisha", "password": "secret1"}).status_code == 201
    token = client.post("/login", json={"username": "aisha", "password": "secret1"}).json()["access_token"]
    me = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["username"] == "aisha"
    assert client.get("/me").status_code == 401
    assert client.post("/login", json={"username": "aisha", "password": "wrong!!"}).status_code == 401
