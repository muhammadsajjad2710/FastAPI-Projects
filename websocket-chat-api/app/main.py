from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

def create_app() -> FastAPI:
    app = FastAPI(title="WebSocket Chat API", version="1.0.0")
    app.state.rooms: dict[str, list[str]] = {}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/rooms/{room}/history")
    def history(room: str):
        return {"room": room, "messages": app.state.rooms.get(room, [])}

    @app.websocket("/ws/{room}")
    async def chat(websocket: WebSocket, room: str):
        await websocket.accept()
        app.state.rooms.setdefault(room, [])
        try:
            while True:
                text = await websocket.receive_text()
                app.state.rooms[room].append(text)
                await websocket.send_json({"room": room, "message": text, "count": len(app.state.rooms[room])})
        except WebSocketDisconnect:
            return

    return app

app = create_app()
