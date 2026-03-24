# Python Conventions

Applies to all `python-*` templates. See ADR 004 for rationale.

## Toolchain

- **Package manager:** uv
- **Build backend:** hatchling
- **Config:** pyproject.toml only
- **Formatter:** ruff format
- **Linter:** ruff
- **Type checker:** ty
- **Test framework:** pytest
- **Python version:** `requires-python = ">=3.12"`

## Project Structure

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

## Test Organization

- Directory-based: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- Marker-based: `@pytest.mark.external` for tests hitting external services
- No `tests/external/` directory; external tests live in the appropriate directory and are selected by marker
