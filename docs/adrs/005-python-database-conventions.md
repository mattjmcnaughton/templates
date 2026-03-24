# ADR 005: Python Database Conventions

## Status

Accepted

## Context

Multiple Python templates (service, cli, and potentially others) may optionally include database support. We need to decide on the ORM, migration tool, and how the presence/absence of a database affects project structure.

## Decision

### ORM: SQLAlchemy (async)

Use SQLAlchemy with async support (`AsyncSession`, `AsyncEngine`) over SQLModel or no ORM.

- SQLModel collapses the DB model and API DTO layers into one, which conflicts with our explicit layered architecture (DTOs, models, repositories).
- No ORM adds friction for common operations without meaningful benefit when the repository pattern already abstracts data access.
- SQLAlchemy async is mature, well-supported, and maps naturally to the repository pattern.

### Database Options

Copier questions:

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `include_database` | bool | false | Include database support |
| `database_type` | choice | postgres | Postgres or SQLite (only asked if `include_database` is true) |

### Migrations

Alembic, always included when `include_database` is true.

### Structure When Database Is Enabled

These are added to the base project structure:

```
src/<package_name>/
  models/           # SQLAlchemy async models
  repositories/     # data access layer
  db.py             # async engine/session setup
alembic/
  versions/
alembic.ini
```

### docker-compose Behavior

- No DB: just the service container
- SQLite: just the service container (DB is a file volume)
- Postgres: service + postgres container

### Health Check

- No DB: returns OK
- With DB: also checks DB connectivity

## Applies To

- `python-service` — database is optional
- `python-cli` — database is optional (same questions, same structure)
- `python-web` — database is optional

## Rationale

- Async-first aligns with the project-wide async priority.
- Making database support optional keeps templates lean for projects that don't need persistence.
- Sharing the same database conventions across service, cli, and web avoids per-template divergence.

## Consequences

- All Python templates that offer database support use the same copier questions, structure, and tooling.
- SQLAlchemy models and Pydantic DTOs are always separate — no shortcut of reusing one for the other.
