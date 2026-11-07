from __future__ import annotations

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, Field

class JobIn(BaseModel):
    text: str = Field(min_length=1, max_length=200)

def run_job(store: dict, job_id: int) -> None:
    job = store[job_id]
    job["status"] = "done"
    job["result"] = job["text"][::-1]

def create_app() -> FastAPI:
    app = FastAPI(title="Background Job API", version="1.0.0")
    app.state.jobs: dict[int, dict] = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/jobs", status_code=202)
    def create_job(payload: JobIn, background: BackgroundTasks):
        job_id = app.state.next_id
        app.state.next_id += 1
        app.state.jobs[job_id] = {"id" : job_id, "status": "queued", "text": payload.text, "result": None}
        background.add_task(run_job, app.state.jobs, job_id)
        return {"id": job_id, "status": "queued"}

    @app.get("/jobs/{job_id}")
    def get_job(job_id: int):
        job = app.state.jobs.get(job_id)
        if job is None:
            raise HTTPException(404, "Job not found")
        return job

    return app

app = create_app()
