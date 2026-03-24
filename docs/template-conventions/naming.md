# Template Naming

Templates follow the convention `<language>-<type>`.

## Template Catalog

| Template | Description |
| -------- | ----------- |
| `python-lib` | pip-installable library |
| `python-cli` | Command-line tool |
| `python-service` | Backend API (FastAPI, Dockerfile) |
| `python-web` | Full-stack web app (backend + `frontend/` via `frontend-react`) |
| `python-agent` | AI agent (pydantic-ai, claude-agent-sdk, langchain, etc.) |
| `typescript-lib` | npm package |
| `typescript-cli` | Command-line tool |
| `typescript-service` | Backend API (Dockerfile) |
| `typescript-web` | Full-stack web app (Next.js) |
| `typescript-agent` | AI agent |
| `rust-lib` | Rust crate |
| `rust-cli` | Command-line tool (clap) |
| `rust-service` | Backend service |
| `golang-lib` | Go module |
| `golang-cli` | Command-line tool (cobra) |
| `golang-service` | Backend service |
| `frontend-react` | Standalone React app, also composable into `-web` templates' `frontend/` directory |

## Type Definitions

- **lib** — installable package/module, published to a registry
- **cli** — command-line tool with an entry point
- **service** — long-running backend process, HTTP API, Dockerfile, no frontend
- **web** — full-stack: backend + frontend. `typescript-web` uses Next.js. Other `-web` templates compose with `frontend-react` in a `frontend/` subdirectory.
- **agent** — AI agent project with choice of framework
