# frontend-react

A React frontend application. Works standalone or composed into `-web` templates' `frontend/` directory.

Inspired by the Vite `react-ts` template.

## Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `project_name` | str | — | Project name (standalone) or inherited from parent (composed) |
| `project_description` | str | — | One-line description |
| `routing_stack` | choice | tanstack | `tanstack` (Tanstack Router + Tanstack Query) or `react-router` (React Router + SWR) |
| `include_shadcn` | bool | false | Include shadcn/ui (Radix + Tailwind component library) |
| `include_zustand` | bool | false | Include zustand for client-side state management |
| `include_recharts` | bool | false | Include recharts for data visualization |
| `include_forms` | bool | false | Include react-hook-form + zod for form handling with schema validation |
| `include_tables` | bool | false | Include data table library (@tanstack/react-table if tanstack stack, react-table if react-router stack) |
| `include_axios` | bool | false | Include axios HTTP client (vs plain fetch) |

## Hardcoded Dependencies

- Vite
- TypeScript
- React
- Tailwind CSS
- Biome (formatting + linting)
- Vitest + React Testing Library (unit/integration)
- Playwright (e2e)
- pnpm (package manager)

## Routing Stack Dependencies

### `tanstack`
- @tanstack/react-router
- @tanstack/react-query
- @tanstack/react-query-devtools
- @tanstack/react-table (if `include_tables`)

### `react-router`
- react-router
- swr
- react-table (if `include_tables`)

## Structure

```
src/
  App.tsx
  main.tsx
  index.css
  routes/              # route definitions (structure varies by routing stack)
  components/
    ui/                # only if include_shadcn
  hooks/
  lib/
    api.ts             # API client utilities
public/
index.html
vite.config.ts         # includes API proxy config when composed into a -web template
tsconfig.json
biome.json
tailwind.config.ts
postcss.config.js
package.json
justfile
tests/
  unit/
  integration/
  e2e/
# --- standalone only ---
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

## Justfile Target Mapping

| Target | Implementation |
| ------ | -------------- |
| `fmt` | `biome format --check .` |
| `fmt-fix` | `biome format --write .` |
| `lint` | `biome lint .` |
| `lint-fix` | `biome lint --write .` |
| `typecheck` | `tsc --noEmit` |
| `test-unit` | `vitest run` |
| `test-integration` | `vitest run tests/integration` |
| `test-e2e` | `npx playwright test` |
| `test-external` | `vitest run -t external` (marker-based) |
| `gate` | fmt + lint + typecheck + test-unit |
| `gate-expensive` | gate + test-integration + test-e2e |
| `gate-external` | gate-expensive + test-external |

When composed into a `-web` template, these targets are invoked by the parent justfile's `-fe` suffixed targets.

## Composability

### Standalone
- Full project scaffolding (README, CLAUDE.md, LICENSE, CI, etc.)
- Own justfile with all standard targets
- Runs on its own dev server

### Composed into `-web`
- Lives at `src/<package_name>/web/frontend/`
- No README, LICENSE, CLAUDE.md, CI (parent project owns these)
- Justfile targets invoked via parent's `-fe` suffixes
- `vite.config.ts` includes proxy config to route API calls to the backend

## Decisions

- **Build tool:** Vite.
- **Linting + formatting:** Biome (single tool, Rust-based, replaces ESLint + Prettier).
- **Testing:** Vitest + React Testing Library (unit/integration), Playwright (e2e).
- **Styling:** Tailwind CSS, always.
- **HTTP client:** Plain fetch by default, axios optional.
- **Tables:** Stack-appropriate table library optional (@tanstack/react-table or react-table).
- **Routing/data fetching:** Two cohesive stacks offered as a single choice rather than mixing and matching.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
