# python-web

A full-stack web application (FastAPI backend + React frontend). Inherits all conventions from `python.md`.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `include_database` | bool | false | Include database support (SQLAlchemy async, Alembic) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module for external API/service clients |

## Dependencies

### Backend
- FastAPI (async)
- uvicorn
- structlog
- pydantic / pydantic-settings
- opentelemetry
- SQLAlchemy async + Alembic (if `include_database`)
- asyncpg (if Postgres) / aiosqlite (if SQLite)

### Frontend
- React (via `frontend-react` template composed into `src/<package_name>/web/frontend/`)

## Structure

```
src/<package_name>/
  __init__.py
  py.typed
  app.py               # FastAPI app factory
  config.py            # pydantic-settings
  logging.py           # structlog setup
  telemetry.py         # OpenTelemetry setup
  web/
    __init__.py
    serve.py           # static file serving for production
    frontend/          # React app (from frontend-react template)
      package.json
      src/
      ...
  routers/
    __init__.py
    health.py          # /healthz, /readyz
  controllers/
    __init__.py
  services/
    __init__.py
  dtos/
    __init__.py
  clients/             # only if include_clients
    __init__.py
  # --- only if include_database ---
  models/
    __init__.py
  repositories/
    __init__.py
  db.py
# --- only if include_database ---
alembic/
  versions/
alembic.ini
# ---
Dockerfile
docker-compose.yml     # backend + frontend dev servers, optionally postgres
tests/
  unit/
  integration/
  e2e/
pyproject.toml
justfile
.env.example
README.md
CLAUDE.md
AGENTS.md -> CLAUDE.md
LICENSE
.editorconfig
.gitignore
.github/
  workflows/
    ci.yml             # runs gate-expensive (not gate-external)
```

## Layering

Same as `python-service`:

```
routers → controllers → services → repositories → DB
             ↕              ↕            ↕
            DTOs          DTOs        models
```

## Justfile Conventions

Backend and frontend targets use `-be` and `-fe` suffixes. Top-level targets (no suffix) run both.

| Target | Runs |
| ------ | ---- |
| `fmt` | `fmt-be` + `fmt-fe` |
| `fmt-be` | `ruff format --check` |
| `fmt-fe` | `prettier --check` (or similar) |
| `fmt-fix` | `fmt-fix-be` + `fmt-fix-fe` |
| `lint` | `lint-be` + `lint-fe` |
| `lint-be` | `ruff check` |
| `lint-fe` | `eslint` (or similar) |
| `typecheck` | `typecheck-be` + `typecheck-fe` |
| `typecheck-be` | `ty check` |
| `typecheck-fe` | `tsc --noEmit` (or similar) |
| `test-unit` | `test-unit-be` + `test-unit-fe` |
| `gate` | `gate-be` + `gate-fe` |
| ... | same pattern for all targets |

## Dev Process

Backend and frontend run as separate processes:
- `just dev-be` — starts FastAPI via uvicorn
- `just dev-fe` — starts React dev server
- `just dev` — starts both (via docker-compose or process manager)
- React dev server proxies API calls to FastAPI backend

## Decisions

- **Framework:** FastAPI (backend) + React (frontend).
- **Frontend composition:** `frontend-react` template generates into `src/<package_name>/web/frontend/`.
- **Static serving:** `web/serve.py` handles serving the built frontend in production.
- **Health endpoints:** Always included.
- **Observability:** OpenTelemetry always included.
- **Dockerfile:** Always included.
- **docker-compose:** Always included. Runs backend + frontend; adds postgres if enabled.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **No nginx.** Dev server proxy for local development.
