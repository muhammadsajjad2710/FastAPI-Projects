from __future__ import annotations

import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

ALPHABET = string.ascii_letters + string.digits

class UrlIn(BaseModel):
    url: HttpUrl

def encode(number: int) -> str:
    if number == 0:
        return ALPHABET[0]
    chars = []
    while number:
        number, rem = divmod(number, len(ALPHABET))
        chars.append(ALPHABET[rem])
    return "".join(reversed(chars))

def create_app() -> FastAPI:
    app = FastAPI(title="URL Shortener API", version="1.0.0")
    app.state.urls: dict[str, str] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/shorten")
    def shorten(payload: UrlIn):
        code = encode(app.state.next_id)
        app.state.next_id += 1
        app.state.urls[code] = str(payload.url)
        return {"code": code, "url": str(payload.url), "short_path": f"/{code}"}

    @app.get("/{code}")
    def resolve(code: str):
        if code == "health" or code not in app.state.urls:
            raise HTTPException(404, "Unknown code")
        return RedirectResponse(app.state.urls[code], status_code=307)

    return app

app = create_app()
