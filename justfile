# Run e2e tests for all templates
test-e2e:
    uv run pytest tests/e2e/ -v

# Run e2e tests for a specific template (e.g., just test-e2e-template python_cli)
test-e2e-template mark:
    uv run pytest tests/e2e/ -v -m {{ mark }}

# Run e2e tests in parallel
test-e2e-parallel:
    uv run pytest tests/e2e/ -v -n auto
