# Blog API

Publish posts and attach comments.

Local FastAPI app. Open `/docs` for the interactive API.

## Run

```powershell
cd D:\AI-Agents\FastAPI-Projects\blog-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Tests

```powershell
python -m pytest -q
```
