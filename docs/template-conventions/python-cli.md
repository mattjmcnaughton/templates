# python-cli

A command-line tool with subcommand scaffolding. Inherits all conventions from `python.md`.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `publish_to_pypi` | bool | true | Include GitHub Actions workflow for PyPI publishing |
| `include_database` | bool | false | Include database support (SQLAlchemy async, Alembic) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module for external API/service clients |

## Dependencies

- typer (CLI framework)
- structlog (logging)
- pydantic-settings (configuration)
- SQLAlchemy async + Alembic (if `include_database`)
- asyncpg (if Postgres) / aiosqlite (if SQLite)

## Structure

```
src/<package_name>/
  __init__.py          # exposes __version__ from importlib.metadata
  py.typed
  cli.py               # typer app, registers subcommands
  config.py            # pydantic-settings based config (env vars, defaults)
  logging.py           # structlog setup
  commands/
    __init__.py
    <example>.py       # ExampleInput, ExampleOutput, typer command
  services/
    __init__.py        # business logic that commands delegate to
  clients/             # only if include_clients is true
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
    publish.yml        # only if publish_to_pypi is true
```

## Patterns

- **Commands** are thin I/O wrappers. They parse CLI args into `COMMANDInput`, call a service, and format `COMMANDOutput`.
- **Services** contain business logic. Commands delegate to services.
- **Clients** (optional) encapsulate external API/service interactions. Services call clients.
- **Config** uses pydantic-settings for structured config from env vars, dotenv files, and defaults.
- **Logging** is configured once at startup via structlog.

## Decisions

- **CLI framework:** typer (subcommand scaffold, not single-command).
- **Documentation:** README only.
- **`py.typed`:** Always included.
- **Versioning:** Single source of truth in `pyproject.toml`. `__version__` via `importlib.metadata`.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **Publishing:** On by default. GitHub Actions workflow publishes to PyPI on release.
- **No Dockerfile.**
