# ADR 007: Docker Conventions

## Status

Accepted

## Context

Templates for service, web, and agent types include Dockerfiles and docker-compose configurations. We need consistent conventions across languages.

## Decision

### Which Templates Include Docker

- **Yes:** service, web, agent
- **No:** lib, cli

### Multi-Stage Build

All Dockerfiles use a three-stage build:

1. **deps** — install dependencies only (maximizes layer caching)
2. **build** — compile/bundle the application
3. **production** — minimal runtime image, copy built artifacts only

### Base Images

| Language | Base Image |
| -------- | ---------- |
| Python | `python:3.12-slim` |
| TypeScript (Bun) | `oven/bun` |
| TypeScript (Next.js) | `node:lts-slim` |

Use `slim` variants, not distroless. Slim is a pragmatic balance of security and debuggability.

### Security

- Always run as a non-root user in the production stage.
- No `HEALTHCHECK` instruction in the Dockerfile — leave health checking to the orchestrator (Kubernetes, ECS, etc.).

### Labels

Include OCI standard labels (`org.opencontainers.image.*`) for image metadata.

### docker-compose

docker-compose is for **local development dependencies only** (Postgres, etc.). The application runs natively with hot reload, not inside a container.

- No DB: docker-compose contains no services (or is omitted)
- SQLite: no docker-compose services needed (DB is a file)
- Postgres: docker-compose runs a postgres container with a volume

## Rationale

- Multi-stage builds minimize production image size and prevent build tools from leaking into production.
- Slim over distroless: distroless images are more secure but prevent shell access for debugging. For most use cases, non-root on slim is sufficient.
- Running the app natively for local dev preserves hot reload and fast iteration. Containers add latency to the dev loop without meaningful benefit for the application process itself.
- OCI labels provide standardized metadata for container registries and tooling.

## Consequences

- All Dockerfiles across languages follow the same three-stage pattern.
- docker-compose files are simple (infrastructure only) and consistent across templates.
- Developers use `just dev` (or similar) to run the app locally, and `docker-compose up` for dependencies.
