from fastapi.testclient import TestClient
from app.main import create_app

def test_upload_list_download():
    client = TestClient(create_app())
    created = client.post("/files", files={"file": ("hello.txt", b"hello world", "text/plain")}).json()
    assert created["size"] == 11
    listed = client.get("/files").json()
    assert listed[0]["filename"] == "hello.txt"
    downloaded = client.get(f"/files/{created['id']}")
    assert downloaded.content == b"hello world"
