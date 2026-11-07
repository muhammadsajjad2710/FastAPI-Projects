# File Upload API

Upload files and list their metadata.

Local FastAPI app. Open `/docs` for the interactive API.

## Run

```powershell
cd D:\AI-Agents\FastAPI-Projects\file-upload-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Tests

```powershell
python -m pytest -q
```
