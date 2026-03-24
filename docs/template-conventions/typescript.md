# TypeScript Conventions

Applies to all `typescript-*` templates. See ADR 006 for rationale.

## Toolchain (Bun-based: lib, cli, service, agent)

- **Runtime:** Bun
- **Package manager:** Bun
- **Formatter:** Biome
- **Linter:** Biome
- **Type checker:** tsc --noEmit (strict mode)
- **Test framework:** bun test
- **Logging:** pino
- **Config/env validation:** zod

## Toolchain (typescript-web / Next.js)

- **Runtime:** Node
- **Package manager:** pnpm
- **Formatter:** Biome
- **Linter:** Biome
- **Type checker:** tsc --noEmit (strict mode)
- **Test framework:** Vitest + Playwright (e2e)
- **Logging:** pino
- **Config/env validation:** zod

## Project Structure (Bun-based)

```
src/
  index.ts
  ...
tests/
  unit/
  integration/
  e2e/
tsconfig.json
biome.json
package.json
justfile
```

## Test Organization

Same as Python: directory-based with marker-based `external` tests.

- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`
- External tests tagged and selected by marker
