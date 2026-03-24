# python-agent

An AI agent project. Inherits all conventions from `python.md`. The execution model determines the base project structure.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `agent_framework` | choice | pydantic-ai | pydantic-ai, claude-agent-sdk, or langchain |
| `execution_model` | choice | cli | cli, service, or web |
| `include_database` | bool | false | Include database support (SQLAlchemy async, Alembic) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module |
| `publish_to_pypi` | bool | true | Only if `execution_model` is cli |

## Dependencies

- Chosen agent framework (pydantic-ai / claude-agent-sdk / langchain)
- structlog
- pydantic / pydantic-settings
- All dependencies from the chosen execution model (see `python-cli.md`, `python-service.md`, or `python-web.md`)

## Agent-Specific Structure

These modules are added on top of the chosen execution model's structure:

```
src/<package_name>/
  agents/
    __init__.py
    <example>.py       # AgentInput, AgentOutput, agent definition
  tools/
    __init__.py        # functions/tools the agent can call
  # ... plus everything from the chosen execution model
```

## Execution Model Inheritance

The `execution_model` question determines the base project structure:

- **cli** — inherits `python-cli` structure: `commands/`, `services/`, typer, `.env.example`. Commands invoke agents.
- **service** — inherits `python-service` structure: `routers/`, `controllers/`, `services/`, `dtos/`, FastAPI, Dockerfile, docker-compose, OpenTelemetry, `.env.example`. Endpoints invoke agents.
- **web** — inherits `python-web` structure: everything from service + `web/frontend/`, `-be`/`-fe` justfile suffixes, `.env.example`. Endpoints invoke agents, frontend provides a UI.

## Patterns

- **Agents** define the agent's behavior, system prompt, and model configuration. Each agent has `AgentInput` and `AgentOutput` for structured I/O.
- **Tools** are functions the agent can call. Framework-agnostic where possible.
- **Prompts** are inlined in agent definitions (no separate template system).
- The execution model layer (commands/routers) invokes agents. Agents use services and tools. Services use repositories and clients.

## Decisions

- **Structured I/O:** Every agent defines `AgentInput` and `AgentOutput` (Pydantic models).
- **Prompts:** Inlined in agent definitions. No separate prompts directory.
- **`.env.example`:** Always included (API keys for LLM providers).
- **All other decisions** (CI, Dockerfile, health checks, DB, justfile) follow from the chosen execution model's conventions.
