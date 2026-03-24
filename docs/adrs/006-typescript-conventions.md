# ADR 006: TypeScript Conventions

## Status

Accepted

## Context

We need consistent TypeScript tooling and project structure across all TypeScript templates (lib, cli, service, web, agent) and the frontend-react template.

## Decision

### Two Runtime Contexts

TypeScript templates use different runtimes depending on context:

| Context | Runtime | Package Manager |
| ------- | ------- | --------------- |
| `typescript-lib/cli/service/agent` | Bun | Bun |
| `typescript-web` (Next.js) | Node | pnpm |
| `frontend-react` | Node (Vite) | pnpm |

### Shared Toolchain (all TypeScript/frontend templates)

| Concern | Tool |
| ------- | ---- |
| Formatting | Biome |
| Linting | Biome |
| Type checking | tsc --noEmit |
| Language | TypeScript (strict mode) |

### Bun-Based Templates (lib, cli, service, agent)

| Concern | Tool |
| ------- | ---- |
| Runtime | Bun |
| Package manager | Bun |
| Testing | bun test |
| Logging | pino |
| Config/env validation | zod |

### Framework Choices

| Template | Framework |
| -------- | --------- |
| `typescript-cli` | commander + chalk |
| `typescript-service` | Hono |
| `typescript-web` | Next.js |
| `typescript-agent` | claude-agent-sdk, pi-ai/pi-coding-agent/pi-tui, or langchain-js |

### Database

Prisma when database is enabled. Supports Postgres or SQLite (same question pattern as Python templates).

### Project Layering

TypeScript service/web templates mirror the Python layering:

```
routers → controllers → services → repositories → DB
             ↕              ↕            ↕
            DTOs          DTOs        Prisma models
```

TypeScript CLI templates mirror the Python CLI pattern:

```
commands → services → repositories → DB
    ↕          ↕
  Input/     models
  Output
```

## Rationale

- Bun provides runtime, package manager, bundler, and test runner in a single tool for backend TypeScript.
- Next.js and Vite have their own runtime expectations (Node), so pnpm is used there instead.
- Hono is fast, type-safe, uses web-standard APIs, and is portable across runtimes (not locked to Bun).
- Prisma is the most mature TypeScript ORM with the best DX for schema-first development.
- Biome is used across all TypeScript/frontend templates for consistent formatting and linting.
- Mirroring the Python layering pattern (routers/controllers/services/dtos/repositories) gives a consistent mental model across languages.

## Consequences

- Two package managers in the ecosystem (Bun for backend TS, pnpm for frontend/Next.js). This is an intentional tradeoff.
- Prisma's schema-first approach differs from Python's SQLAlchemy code-first models, but the repository pattern abstracts this.
