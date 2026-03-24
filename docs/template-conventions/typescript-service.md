# typescript-service

A backend API service with no frontend. Inherits all conventions from `typescript.md` (Bun-based).

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `include_database` | bool | false | Include database support (Prisma) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module |

## Dependencies

- Hono (HTTP framework)
- pino (logging)
- zod (validation, config/env)
- OpenTelemetry (tracing)
- Prisma (if `include_database`)

## Structure

```
src/
  index.ts               # Hono app entry point
  app.ts                 # Hono app factory
  config.ts              # zod-based env/config validation
  logging.ts             # pino setup
  telemetry.ts           # OpenTelemetry setup
  routers/
    index.ts
    health.ts            # /healthz, /readyz
  controllers/
    index.ts             # orchestration between services/repos
  services/
    index.ts             # business logic
  dtos/
    index.ts             # zod schemas for request/response
  clients/               # only if include_clients
    index.ts
  # --- only if include_database ---
  repositories/
    index.ts
  db.ts                  # Prisma client setup
prisma/
  schema.prisma
# ---
Dockerfile
docker-compose.yml       # service only, or service + postgres
tests/
  unit/
  integration/
  e2e/
tsconfig.json
biome.json
package.json
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
    ci.yml               # runs gate-expensive (not gate-external)
```

## Layering

```
routers → controllers → services → repositories → DB
             ↕              ↕            ↕
            DTOs          DTOs      Prisma models
```

- **Routers** define HTTP endpoints using Hono, validate with zod, pass DTOs to controllers.
- **Controllers** orchestrate across services.
- **Services** contain business logic. Framework-agnostic.
- **Repositories** encapsulate data access via Prisma.
- **DTOs** are zod schemas for API input/output. Separate from Prisma models.
- **Clients** (optional) encapsulate external API/service calls.

## Decisions

- **Framework:** Hono.
- **Health endpoints:** Always included (`/healthz`, `/readyz`). DB connectivity checked when database is enabled.
- **Observability:** OpenTelemetry always included.
- **Dockerfile:** Always included.
- **docker-compose:** Always included. Service only when no DB; adds postgres when `database_type` is postgres.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **No frontend.**
