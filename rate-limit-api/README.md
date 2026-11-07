# Rate Limit API

Serve a public endpoint with per-client rate limits.

Local FastAPI app. Open `/docs` for the interactive API.

## Run

```powershell
cd D:\AI-Agents\FastAPI-Projects\rate-limit-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Tests

```powershell
python -m pytest -q
```
