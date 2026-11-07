# FastAPI Projects

Ten local **FastAPI** APIs. Each one is a complete app with tests and OpenAPI docs at `/docs`. No paid APIs.

These apps have no production authentication story unless noted. Do not expose them publicly as-is.

## Projects

| # | Project | What it does |
| --- | --- | --- |
| 1 | [notes-api](notes-api/) | CRUD notes |
| 2 | [jwt-auth-api](jwt-auth-api/) | Register, login, JWT-protected profile |
| 3 | [blog-api](blog-api/) | Posts and comments |
| 4 | [url-shortener-api](url-shortener-api/) | Short links and redirects |
| 5 | [inventory-api](inventory-api/) | Products and stock sales |
| 6 | [bookstore-api](bookstore-api/) | Book search with pagination |
| 7 | [file-upload-api](file-upload-api/) | File upload and download |
| 8 | [job-queue-api](job-queue-api/) | Background jobs |
| 9 | [websocket-chat-api](websocket-chat-api/) | WebSocket chat rooms |
| 10 | [rate-limit-api](rate-limit-api/) | Per-client rate limiting |

## Quick start

```powershell
cd D:\AI-Agents\FastAPI-Projects\notes-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs

```powershell
python -m pytest -q
```
