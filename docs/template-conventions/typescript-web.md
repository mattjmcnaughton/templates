# typescript-web

A full-stack web application using Next.js. Inherits all conventions from `typescript.md` (pnpm-based, NOT Bun).

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `include_database` | bool | false | Include database support (Prisma) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_shadcn` | bool | false | Include shadcn/ui component library |
| `include_zustand` | bool | false | Include zustand for client-side state management |
| `include_recharts` | bool | false | Include recharts for data visualization |
| `include_forms` | bool | false | Include react-hook-form + zod for form handling |
| `include_tables` | bool | false | Include @tanstack/react-table |
| `include_axios` | bool | false | Include axios HTTP client |

## Dependencies

- Next.js (framework)
- React
- Tailwind CSS
- pino (logging)
- zod (validation, config/env)
- OpenTelemetry (tracing)
- Prisma (if `include_database`)
- Vitest + React Testing Library (unit/integration)
- Playwright (e2e)

## Structure

```
src/
  app/                   # Next.js App Router
    layout.tsx
    page.tsx
    api/
      health/
        route.ts         # /api/health
  components/
    ui/                  # only if include_shadcn
  hooks/
  lib/
    api.ts               # API client utilities
    config.ts            # zod-based env/config validation
    logging.ts           # pino setup
    telemetry.ts         # OpenTelemetry setup
  services/
    index.ts             # business logic
  # --- only if include_database ---
  repositories/
    index.ts
  db.ts                  # Prisma client setup
prisma/
  schema.prisma
# ---
Dockerfile
docker-compose.yml
tests/
  unit/
  integration/
  e2e/
next.config.ts
tsconfig.json
biome.json
tailwind.config.ts
postcss.config.js
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

## Justfile Target Mapping

| Target | Implementation |
| ------ | -------------- |
| `fmt` | `biome format --check .` |
| `fmt-fix` | `biome format --write .` |
| `lint` | `biome lint .` |
| `lint-fix` | `biome lint --write .` |
| `typecheck` | `tsc --noEmit` |
| `test-unit` | `vitest run tests/unit` |
| `test-integration` | `vitest run tests/integration` |
| `test-e2e` | `npx playwright test` |
| `test-external` | `vitest run -t external` |
| `gate` | fmt + lint + typecheck + test-unit |
| `gate-expensive` | gate + test-integration + test-e2e |
| `gate-external` | gate-expensive + test-external |

No `-be`/`-fe` suffixes — Next.js is a unified full-stack framework.

## Decisions

- **Framework:** Next.js with App Router.
- **Runtime:** Node + pnpm (not Bun — Next.js ecosystem).
- **Testing:** Vitest + React Testing Library (unit/integration), Playwright (e2e).
- **Styling:** Tailwind CSS.
- **Health endpoint:** Always included via API route.
- **Observability:** OpenTelemetry always included.
- **Dockerfile:** Always included.
- **docker-compose:** Always included.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **Optional libraries:** Same set as `frontend-react` (shadcn, zustand, recharts, forms, tables, axios).
