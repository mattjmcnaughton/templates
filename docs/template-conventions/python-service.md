# python-service

A backend API service with no frontend. Inherits all conventions from `python.md`.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `include_database` | bool | false | Include database support (SQLAlchemy async, Alembic) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module for external API/service clients |

## Dependencies

- FastAPI (async)
- uvicorn
- structlog
- pydantic / pydantic-settings
- opentelemetry (tracing)
- SQLAlchemy async + Alembic (if `include_database`)
- asyncpg (if Postgres) / aiosqlite (if SQLite)

## Structure

```
src/<package_name>/
  __init__.py
  py.typed
  app.py               # FastAPI app factory
  config.py            # pydantic-settings
  logging.py           # structlog setup
  telemetry.py         # OpenTelemetry setup
  routers/
    __init__.py
    health.py          # /healthz, /readyz
  controllers/
    __init__.py        # orchestration between services/repos
  services/
    __init__.py        # business logic
  dtos/
    __init__.py        # Pydantic request/response models
  clients/             # only if include_clients
    __init__.py
  # --- only if include_database ---
  models/
    __init__.py        # SQLAlchemy async models
  repositories/
    __init__.py        # data access layer
  db.py                # async engine/session setup
# --- only if include_database ---
alembic/
  versions/
alembic.ini
# ---
Dockerfile
docker-compose.yml     # service only, or service + postgres
tests/
  unit/
  integration/
  e2e/
pyproject.toml
justfile
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

```
routers → controllers → services → repositories → DB
             ↕              ↕            ↕
            DTOs          DTOs        models
```

- **Routers** define HTTP endpoints, parse requests into DTOs, return DTOs.
- **Controllers** orchestrate across services. Handle request-level logic.
- **Services** contain business logic. Framework-agnostic.
- **Repositories** encapsulate data access. Return/accept SQLAlchemy models.
- **DTOs** are Pydantic models for API input/output. Always separate from DB models.
- **Models** are SQLAlchemy async models. Never exposed directly via the API.
- **Clients** (optional) encapsulate external API/service calls. Used by services.

## Decisions

- **Framework:** FastAPI, async-first.
- **Health endpoints:** Always included (`/healthz`, `/readyz`). DB connectivity checked when database is enabled.
- **Observability:** OpenTelemetry always included.
- **Dockerfile:** Always included.
- **docker-compose:** Always included. Contains just the service when no DB; adds postgres container when `database_type` is postgres.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **No frontend.**
