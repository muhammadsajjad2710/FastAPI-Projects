from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    body: str = Field(min_length=1, max_length=2000)

class Note(NoteIn):
    id: int

def create_app() -> FastAPI:
    app = FastAPI(title="Notes API", version="1.0.0")
    app.state.notes: dict[int, Note] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/notes", status_code=201)
    def create_note(payload: NoteIn) -> Note:
        note = Note(id=app.state.next_id, **payload.model_dump())
        app.state.next_id += 1
        app.state.notes[note.id] = note
        return note

    @app.get("/notes")
    def list_notes() -> list[Note]:
        return list(app.state.notes.values())

    @app.get("/notes/{note_id}")
    def get_note(note_id: int) -> Note:
        if note_id not in app.state.notes:
            raise HTTPException(404, "Note not found")
        return app.state.notes[note_id]

    @app.put("/notes/{note_id}")
    def update_note(note_id: int, payload: NoteIn) -> Note:
        if note_id not in app.state.notes:
            raise HTTPException(404, "Note not found")
        note = Note(id=note_id, **payload.model_dump())
        app.state.notes[note_id] = note
        return note

    @app.delete("/notes/{note_id}", status_code=204)
    def delete_note(note_id: int) -> Response:
        if note_id not in app.state.notes:
            raise HTTPException(404, "Note not found")
        del app.state.notes[note_id]
        return Response(status_code=204)

    return app

app = create_app()
