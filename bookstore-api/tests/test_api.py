from fastapi.testclient import TestClient
from app.main import create_app

def test_search_and_pagination():
    client = TestClient(create_app())
    client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965})
    client.post("/books", json={"title": "Dune Messiah", "author": "Frank Herbert", "year": 1969})
    client.post("/books", json={"title": "Neuromancer", "author": "William Gibson", "year": 1984})
    page = client.get("/books", params={"q": "dune", "page": 1, "size": 1}).json()
    assert page["total"] == 2
    assert len(page["items"]) == 1
    assert client.get("/books", params={"q": "gibson"}).json()["total"] == 1
