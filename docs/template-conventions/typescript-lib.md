# typescript-lib

An npm package. Inherits all conventions from `typescript.md` (Bun-based).

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `publish_to_npm` | bool | false | Include GitHub Actions workflow for npm publishing |

## Structure

```
src/
  index.ts             # package entry point, exports public API
tests/
  unit/
  integration/
  e2e/
tsconfig.json
biome.json
package.json
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
    publish.yml        # only if publish_to_npm
```

## Justfile Target Mapping

| Target | Implementation |
| ------ | -------------- |
| `fmt` | `biome format --check .` |
| `fmt-fix` | `biome format --write .` |
| `lint` | `biome lint .` |
| `lint-fix` | `biome lint --write .` |
| `typecheck` | `tsc --noEmit` |
| `test-unit` | `bun test tests/unit` |
| `test-integration` | `bun test tests/integration` |
| `test-e2e` | `bun test tests/e2e` |
| `test-external` | `bun test --grep external` |
| `gate` | fmt + lint + typecheck + test-unit |
| `gate-expensive` | gate + test-integration + test-e2e |
| `gate-external` | gate-expensive + test-external |

## Decisions

- **Documentation:** README only.
- **Versioning:** Single source of truth in `package.json`.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **Publishing:** Optional. GitHub Actions workflow publishes to npm on release.
- **No Dockerfile.**
