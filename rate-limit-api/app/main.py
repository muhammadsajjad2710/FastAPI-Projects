from __future__ import annotations

from time import time

from fastapi import FastAPI, HTTPException, Request

LIMIT = 3
WINDOW = 60

def create_app() -> FastAPI:
    app = FastAPI(title="Rate Limit API", version="1.0.0")
    app.state.hits: dict[str, list[float]] = {}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/public")
    def public(request: Request):
        client = request.client.host if request.client else "local"
        now = time()
        stamps = [stamp for stamp in app.state.hits.get(client, []) if now - stamp < WINDOW]
        if len(stamps) >= LIMIT:
            raise HTTPException(429, "Rate limit exceeded")
        stamps.append(now)
        app.state.hits[client] = stamps
        return {"message": "ok", "remaining": LIMIT - len(stamps)}

    return app

app = create_app()
