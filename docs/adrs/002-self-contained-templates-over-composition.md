# ADR 002: Self-Contained Templates Over Composition

## Status

Accepted

## Context

Multiple templates will share similar concerns (e.g., a Postgres database option requires Docker Compose config in both Python and TypeScript web templates). We need to decide whether to:

1. **Compose** — extract shared concerns into addon templates layered on top of base templates via multiple `copier copy` runs.
2. **Duplicate** — keep each template fully self-contained, accepting minor duplication of shared patterns.

## Decision

Keep templates self-contained. Accept minor duplication of shared configuration (e.g., Docker Compose postgres service definitions) across templates.

## Rationale

- Copier overwrites files; it does not merge them. Composition only works when the addon generates files the base template doesn't touch. In practice, shared concerns (databases, CI, release config) almost always need to modify files the base template owns (`docker-compose.yml`, `pyproject.toml`, CI workflows).
- The actually-shared, language-agnostic surface area is small (e.g., ~10 lines of Docker Compose YAML for a postgres service). Everything else — migrations, ORM setup, connection handling, env config — is language-specific regardless.
- Self-contained templates are simpler to understand, test, and generate from. No ordering dependencies, no implicit contracts between templates.

## Consequences

- Changes to shared conventions (e.g., postgres Docker Compose config) must be applied to each template individually.
- If drift becomes a problem, we will add CI-based drift detection (e.g., assert shared blocks are identical across templates) rather than introducing composition.
