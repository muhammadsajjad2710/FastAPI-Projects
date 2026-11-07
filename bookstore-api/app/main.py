from __future__ import annotations

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    author: str = Field(min_length=1, max_length=80)
    year: int = Field(ge=1400, le=2100)

def create_app() -> FastAPI:
    app = FastAPI(title="Bookstore API", version="1.0.0")
    app.state.books: list[dict] = []
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/books", status_code=201)
    def add_book(payload: BookIn):
        book = {"id": app.state.next_id, **payload.model_dump()}
        app.state.next_id += 1
        app.state.books.append(book)
        return book

    @app.get("/books")
    def search_books(q: str = "", page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=50)):
        q_norm = q.lower().strip()
        matches = [
            book
            for book in app.state.books
            if q_norm in book["title"].lower() or q_norm in book["author"].lower()
        ]
        start = (page - 1) * size
        chunk = matches[start : start + size]
        return {"total": len(matches), "page": page, "size": size, "items": chunk}

    return app

app = create_app()
