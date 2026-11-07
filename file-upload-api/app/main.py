from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

def create_app() -> FastAPI:
    app = FastAPI(title="File Upload API", version="1.0.0")
    app.state.files: dict[int, dict] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/files", status_code=201)
    async def upload(file: UploadFile = File(...)):
        data = await file.read()
        if not data:
            raise HTTPException(400, "Empty file")
        item = {
            "id": app.state.next_id,
            "filename": file.filename or "upload.bin",
            "content_type": file.content_type or "application/octet-stream",
            "size": len(data),
            "content": data,
        }
        app.state.next_id += 1
        app.state.files[item["id"]] = item
        return {key: item[key] for key in ("id", "filename", "content_type", "size")}

    @app.get("/files")
    def list_files():
        return [{key: item[key] for key in ("id", "filename", "content_type", "size")} for item in app.state.files.values()]

    @app.get("/files/{file_id}")
    def download(file_id: int):
        item = app.state.files.get(file_id)
        if item is None:
            raise HTTPException(404, "File not found")
        return Response(content=item["content"], media_type=item["content_type"])

    return app

app = create_app()
