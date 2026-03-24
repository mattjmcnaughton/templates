# python-lib

A pip-installable Python library. Inherits all conventions from `python.md`.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `publish_to_pypi` | bool | false | Include GitHub Actions workflow for PyPI publishing |

## Structure

```
src/
  <package_name>/
    __init__.py      # exposes __version__ from importlib.metadata
    py.typed         # PEP 561 marker
tests/
  unit/
  integration/
  e2e/
pyproject.toml
justfile
README.md
CLAUDE.md
AGENTS.md -> CLAUDE.md
LICENSE
.editorconfig
.gitignore
.github/
  workflows/
    ci.yml           # runs gate-expensive (not gate-external)
    publish.yml      # only if publish_to_pypi is true
```

## Decisions

- **Documentation:** README only, no doc site.
- **`py.typed`:** Always included.
- **Versioning:** Single source of truth in `pyproject.toml`. `__version__` read via `importlib.metadata` in `__init__.py`.
- **CI:** Runs `gate-expensive` on PR and main. Does not run `gate-external`.
- **Publishing:** Optional. When enabled, includes a GitHub Actions workflow that publishes to PyPI on release.
- **No Dockerfile.**
- **No optional dependency scaffolding.**
