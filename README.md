# Docker Database API

A small Python REST API backed by SQLAlchemy. Docker Compose runs the API and PostgreSQL; SQLAlchemy can also use other SQL databases by changing `DATABASE_URL` and installing that database's Python driver.

## Run with Docker

1. Copy `.env.example` to `.env` and change the database password.
2. Start the services with `docker compose up --build`.
3. Open `http://localhost:8000/docs` for interactive API documentation or `http://localhost:8000/health` for the health check.

The database is persisted in the `postgres_data` Docker volume. The starter creates its tables on startup; use Alembic migrations before evolving a production schema.

## Endpoints

- `POST /items` creates an item.
- `GET /items?offset=0&limit=100` lists items.
- `GET /items/{item_id}` retrieves one item.
- `PATCH /items/{item_id}` updates supplied fields.
- `DELETE /items/{item_id}` deletes an item.

## Run locally

Python 3.12 or newer is recommended. Create and activate a virtual environment, then install dependencies and start the API:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Without `DATABASE_URL`, the local server uses `./university.db` (SQLite). For another database, set `DATABASE_URL` to a SQLAlchemy URL and install the corresponding driver. PostgreSQL uses `postgresql+psycopg://...`; MySQL/MariaDB and other engines need their respective SQLAlchemy dialect drivers.

## Test

```powershell
pytest
```