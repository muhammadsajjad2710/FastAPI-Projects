from fastapi.testclient import TestClient
from app.main import create_app

def test_post_and_comment():
    client = TestClient(create_app())
    post = client.post("/posts", json={"title": "Hello", "body": "First post"}).json()
    comment = client.post(f"/posts/{post['id']}/comments", json={"author": "Bilal", "body": "Nice"})
    assert comment.status_code == 201
    assert client.get(f"/posts/{post['id']}").json()["comments"][0]["body"] == "Nice"
    assert client.get("/posts/99").status_code == 404
