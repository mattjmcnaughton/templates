# CLAUDE.md

This is a monorepo of [Copier](https://copier.readthedocs.io/) templates. Each directory under `templates/` is a standalone Copier template with its own `copier.yml`.

## Key References

- **Architecture Decision Records:** `docs/adrs/` — read before proposing structural changes
- **Template naming and catalog:** `docs/template-conventions/naming.md`
- **Conventions (copier questions, justfile targets, cross-template consistency):** `docs/template-conventions/conventions.md`

## Key Rules

- Templates are named `<language>-<type>` (e.g., `python-service`, `rust-cli`)
- Templates are self-contained. Do not create shared/addon templates.
- Minor duplication across templates is preferred over abstraction.
- Exception: `frontend-react` is composable into `-web` templates' `frontend/` directory.
- When modifying a cross-template concern (LICENSE, .editorconfig, justfile targets, copier questions, etc.), apply the change to ALL templates. See `docs/template-conventions/conventions.md` for the full list.
