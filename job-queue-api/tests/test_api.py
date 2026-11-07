from fastapi.testclient import TestClient
from app.main import create_app

def test_background_job_completes():
    client = TestClient(create_app())
    created = client.post("/jobs", json={"text": "FastAPI"}).json()
    job = client.get(f"/jobs/{created['id']}").json()
    assert job["status"] == "done"
    assert job["result"] == "IPAtsaF"
