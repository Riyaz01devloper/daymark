# daymark Todo

A small full-stack todo app: React + Vite frontend, FastAPI backend, and SQLite
storage. Accounts keep their tasks private; tasks remain saved after the API
restarts.

## Run locally

Open two terminals from this project folder.

Terminal 1 — API:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Terminal 2 — React app:

```powershell
Set-Location frontend
npm run dev
```

Open <http://127.0.0.1:5173>. API documentation is at
<http://127.0.0.1:8000/docs>.

If you do not have the Python environment yet, create one and install the
dependencies listed in `requirements.txt`. Install frontend dependencies
once with `npm install` from `frontend`.

Alternatively, build the frontend (`npm run build` from `frontend`) and run
FastAPI directly:
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
You can then open <http://127.0.0.1:8000> to use the app and API from a single server.

## Project structure

```text
app/
  main.py              FastAPI app and router registration
  database.py          SQLite connection and schema initialization
  schemas.py           Request and response validation
  security.py          Password hashing and session-cookie helpers
  routers/
    auth.py            Registration, login, logout, current account
    todos.py           User-scoped todo endpoints, filtering and paging
    suggestions.py     Grade-aware Gemini study tips
frontend/
  src/
    api/client.js      Shared API client
    components/        Authentication, class setup and todo row
    App.jsx            Dashboard, task state and interactions
    styles.css         Responsive UI
tests/
  test_api.py          Authentication, privacy and todo API tests
```

## Data and deployment notes

The database defaults to `app/todos.db`. Set `TODO_DATABASE_PATH` to store it
elsewhere. The database file is local and ignored by Git. SQLite is convenient
for development and a single application instance; use a managed PostgreSQL
database before running multiple API instances or needing higher write
throughput. The routes and schemas are kept separate from storage so the
database layer can be replaced without putting SQL in the UI.

Vite proxies API requests to the local FastAPI server during development. For
production, serve the frontend and API behind the same HTTPS origin (or
configure an explicit API origin and matching CORS/cookie policies).

New accounts use a six-digit numeric PIN. Six digits are weaker than a
password, so per-email sign-in rate limiting is enabled; avoid reusing the PIN
for other services. Existing accounts with longer passwords can continue to
sign in. Credentials are stored as scrypt hashes, never as plain text.
Sessions use random tokens in HTTP-only, SameSite=Lax cookies; only token
hashes are stored in SQLite. Cookies are marked Secure when the request uses
HTTPS.

After signing in, students select their class (1–12); they can update it from
the dashboard. The dashboard can request one short study tip at a time from
Gemini. Open `.env` in the project root and add your key:

```powershell
notepad .env
```

Set `GEMINI_API_KEY` in `.env`, then start the API as usual:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The default model is `gemini-3.5-flash-lite`; set `GEMINI_MODEL` to use a
different compatible Gemini model. Each request sends the selected class and
short instructions (not the account email or task list), and caps the response
at 48 output tokens. The API loads `.env` on startup; environment variables
already set in the shell take precedence. `.env` is ignored by Git. Never put
the API key in the frontend or commit it to source control. Generated tips are
saved per account; recent tips are included in the prompt, and exact repeats
are rejected and retried before a tip is shown.

Before exposing account creation publicly, add abuse controls such as login
rate limiting and email verification, configure HTTPS and database backups,
and review the hosting platform's proxy and cookie settings.

Run the API tests with:

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_api.py
```

Build the frontend with:

```powershell
Set-Location frontend
npm run build
```
