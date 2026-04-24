# frontend-react

A React frontend application. Works standalone or composed into `-web` templates' `frontend/` directory.

Inspired by the Vite `react-ts` template.

## Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `project_name` | str | — | Project name (standalone) or inherited from parent (composed) |
| `project_description` | str | — | One-line description |
| `is_composed` | bool | false | Whether this frontend is composed into a parent `-web` template |
| `author_name` | str | — | Author or organization name (standalone only) |
| `author_email` | str | — | Author contact email (standalone only) |
| `license` | choice | MIT | MIT, Apache-2.0, Proprietary (standalone only) |
| `include_shadcn` | bool | false | Include shadcn/ui (Radix + Tailwind component library) |
| `include_zustand` | bool | false | Include zustand for client-side state management |
| `include_recharts` | bool | false | Include recharts for data visualization |
| `include_forms` | bool | false | Include react-hook-form + zod for form handling with schema validation |
| `include_tables` | bool | false | Include @tanstack/react-table for data tables |
| `include_technical_docs` | bool | false | Create docs/technical/ (standalone only) |
| `include_product_docs` | bool | false | Create docs/product/ (standalone only) |

## Hardcoded Dependencies

- Vite
- TypeScript
- React
- Tanstack Router + Tanstack Query
- Tailwind CSS
- Biome (formatting + linting)
- Vitest + React Testing Library + jest-dom (unit/integration)
- MSW (API mocking in tests)
- Playwright (e2e)
- pnpm (package manager)

## Structure

```
src/
  main.tsx
  index.css
  vite-env.d.ts
  routes/              # Tanstack Router file-based routes
    __root.tsx
    index.tsx
  components/
    ui/                # only if include_shadcn
  hooks/
  lib/
    api.ts             # API client utilities (plain fetch)
public/
  vite.svg
index.html
vite.config.ts         # includes API proxy config when composed into a -web template
tsconfig.json
tsconfig.app.json
tsconfig.node.json
biome.json
tailwind.config.ts
postcss.config.js
package.json
justfile
tests/
  setup.ts             # jest-dom matchers for Vitest
  integration/
  e2e/
# --- standalone only ---
.env.example
README.md
CLAUDE.md
AGENTS.md -> CLAUDE.md
LICENSE
Caddyfile
Dockerfile
docker-compose.yml
.editorconfig
.gitignore
.github/
  workflows/
    ci.yml             # runs gate-expensive (not gate-external)
docs/
  adrs/
  architecture.md
  development.md
  technical/           # only if include_technical_docs
  product/             # only if include_product_docs
```

## Justfile Target Mapping

| Target | Implementation |
| ------ | -------------- |
| `fmt` | `biome format --check .` |
| `fmt-fix` | `biome format --write .` |
| `lint` | `biome lint .` |
| `lint-fix` | `biome lint --write .` |
| `typecheck` | `tsc --noEmit` |
| `test-unit` | `vitest run src/` (co-located tests) |
| `test-integration` | `vitest run tests/integration` |
| `test-e2e` | `npx playwright test` |
| `test-external` | `vitest run -t external` (marker-based) |
| `gate` | fmt + lint + typecheck + test-unit |
| `gate-expensive` | gate + test-integration + test-e2e |
| `gate-external` | gate-expensive + test-external |

When composed into a `-web` template, these targets are invoked by the parent justfile's `-fe` suffixed targets.

## Testing Conventions

- Unit tests are co-located next to source files (`src/components/Button.test.tsx`)
- Integration tests go in `tests/integration/`
- E2e tests go in `tests/e2e/` (Playwright)
- MSW is included for API mocking in tests
- Vitest config is inline in `vite.config.ts`

## Composability

### Standalone
- Full project scaffolding (README, CLAUDE.md, LICENSE, CI, Dockerfile, etc.)
- Own justfile with all standard targets
- Runs on its own dev server

### Composed into `-web`
- No README, LICENSE, CLAUDE.md, CI, Dockerfile, docs (parent project owns these)
- Justfile targets invoked via parent's `-fe` suffixes
- `vite.config.ts` includes proxy config to route API calls to the backend

## Decisions

- **Build tool:** Vite.
- **Routing/data fetching:** Tanstack Router + Tanstack Query.
- **Linting + formatting:** Biome (single tool, Rust-based, replaces ESLint + Prettier).
- **Testing:** Vitest + React Testing Library (unit/integration), Playwright (e2e), MSW (API mocking).
- **Test location:** Co-located unit tests (`*.test.tsx` next to source).
- **Styling:** Tailwind CSS, always.
- **HTTP client:** Plain fetch via `src/lib/api.ts`.
- **Dockerfile:** Caddy (non-root, port 8080).
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
