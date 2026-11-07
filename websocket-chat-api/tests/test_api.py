from fastapi.testclient import TestClient
from app.main import create_app

def test_websocket_chat_and_history():
    app = create_app()
    client = TestClient(app)
    with client.websocket_connect("/ws/lobby") as ws:
        ws.send_text("hello")
        data = ws.receive_json()
        assert data["message"] == "hello"
        assert data["count"] == 1
    history = client.get("/rooms/lobby/history").json()
    assert history["messages"] == ["hello"]
