# ADR 004: Python Conventions

## Status

Accepted

## Context

We need consistent Python tooling and project structure across all Python templates (lib, cli, service, web, agent).

## Decision

### Toolchain

| Concern | Tool |
| ------- | ---- |
| Package manager | uv |
| Build backend | hatchling |
| Configuration | pyproject.toml only (no setup.cfg, setup.py) |
| Formatting | ruff format |
| Linting | ruff |
| Type checking | ty |
| Testing | pytest |

### Python Version

- `requires-python = ">=3.12"` in pyproject.toml

### Project Structure

All Python templates use src layout:

```
src/
  <package_name>/
    __init__.py
    ...
tests/
  unit/
  integration/
  e2e/
pyproject.toml
justfile
```

### Test Organization

- `tests/unit/` — unit tests
- `tests/integration/` — integration tests
- `tests/e2e/` — end-to-end tests
- Pytest markers for cross-cutting test categories:
  - `@pytest.mark.external` — tests that hit external services (used by `test-external` justfile target)
  - Expensive tests are the union of integration + e2e + external (used by `gate-expensive` and `gate-external`)
- No separate `tests/external/` directory; external tests live alongside other tests and are selected by marker

### Justfile Target Mapping

| Target | Implementation |
| ------ | -------------- |
| `fmt` | `ruff format --check` |
| `fmt-fix` | `ruff format` |
| `lint` | `ruff check` |
| `lint-fix` | `ruff check --fix` |
| `typecheck` | `ty check` |
| `test-all` | `pytest tests/unit tests/integration tests/e2e` |
| `test-unit` | `pytest tests/unit` |
| `test-integration` | `pytest tests/integration` |
| `test-e2e` | `pytest tests/e2e` |
| `test-external` | `pytest -m external` |
| `gate` | fmt + lint + typecheck + test-unit |
| `gate-expensive` | gate + test-integration + test-e2e |
| `gate-external` | gate-expensive + test-external |

## Rationale

- uv is the fastest Python package manager and handles virtualenvs, locking, and tool management.
- hatchling is uv's default build backend, lightweight and standards-compliant.
- ruff replaces black, isort, flake8, and pylint with a single fast tool.
- ty is a fast type checker built by the ruff/astral team.
- src layout prevents accidental imports of the uninstalled package during development.
- Directory-based test separation (unit/integration/e2e) matches the justfile targets naturally. Pytest markers handle the orthogonal external concern without needing a separate directory.
- Python 3.12 provides modern syntax (type parameter syntax, improved f-strings) while maintaining broad compatibility.

## Consequences

- All Python templates share the same toolchain. Language-specific tool decisions are settled once, not per-template.
- pyproject.toml is the single source of truth for project metadata, dependencies, and tool configuration (ruff, pytest).
