# ADR 003: Cross-Template Conventions

## Status

Accepted

## Context

All templates in this monorepo need a baseline set of project scaffolding. We need to decide what is asked via copier questions versus hardcoded, and what files/tools are always included.

## Decision

### Copier Questions (all templates)

Every template asks these questions:

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `project_name` | str | — | Project/repo name |
| `project_description` | str | — | One-line description |
| `author_name` | str | — | Author or organization |
| `author_email` | str | — | Contact email |
| `license` | choice | MIT | MIT, Apache 2.0, or Proprietary |

### Hardcoded Conventions (no questions)

| Concern | Decision |
| ------- | -------- |
| CI | GitHub Actions, always |
| CLAUDE.md | Always generated. AGENTS.md is a symlink to CLAUDE.md. |
| Dockerfile | Included for service, web, and agent types. Not included for lib and cli types. |
| Pre-commit hooks | Not included |
| `.editorconfig` | Always included |
| `.gitignore` | Always included (language-specific content) |
| `justfile` | Always included |

### Justfile Targets

Every template includes a `justfile` with the following targets:

| Target | Purpose |
| ------ | ------- |
| `fmt` | Check formatting |
| `fmt-fix` | Fix formatting |
| `lint` | Check linting |
| `lint-fix` | Fix linting |
| `typecheck` | Run type checker |
| `test-all` | Run all tests (unit + integration) |
| `test-unit` | Run unit tests only |
| `test-integration` | Run integration tests only |
| `test-e2e` | Run end-to-end tests |
| `test-external` | Run tests that hit external services |
| `gate` | Fast pre-push check: fmt + lint + typecheck + test-unit |
| `gate-expensive` | Full check: gate + test-integration + test-e2e |
| `gate-external` | Everything: gate-expensive + test-external |

The underlying tools vary by language (e.g., `ruff` vs `eslint`, `pytest` vs `vitest`) but the target names are consistent across all templates.

## Rationale

- Fewer copier questions means faster project generation, especially for AI agent consumers.
- Hardcoding CI, editor config, and other scaffolding avoids conditional complexity in templates.
- License is the one convention worth asking about since it has legal implications.
- Consistent justfile targets allow agents and developers to interact with any project using the same commands regardless of language.
- Pre-commit hooks are excluded to keep the workflow simple; CI via `gate` targets serves the same purpose.

## Consequences

- All templates must implement the full set of justfile targets, even if some are no-ops for a given project type (e.g., `test-e2e` for a library).
- Adding a new cross-template concern requires updating every template. CLAUDE.md documents this expectation.
