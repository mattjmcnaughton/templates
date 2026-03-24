# typescript-agent

An AI agent project. Inherits all conventions from `typescript.md`. The execution model determines the base project structure.

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `agent_framework` | choice | claude-agent-sdk | claude-agent-sdk, pi-ai (pi-coding-agent/pi-tui), or langchain-js |
| `execution_model` | choice | cli | cli, service, or web |
| `include_database` | bool | false | Include database support (Prisma) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module |
| `publish_to_npm` | bool | true | Only if `execution_model` is cli |

## Agent-Specific Structure

These modules are added on top of the chosen execution model's structure:

```
src/
  agents/
    index.ts
    <example>.ts         # AgentInput, AgentOutput, agent definition
  tools/
    index.ts             # functions/tools the agent can call
  # ... plus everything from the chosen execution model
```

## Execution Model Inheritance

- **cli** — inherits `typescript-cli` structure (Bun): `commands/`, `services/`, commander + chalk, `.env.example`. Commands invoke agents.
- **service** — inherits `typescript-service` structure (Bun): `routers/`, `controllers/`, `services/`, `dtos/`, Hono, Dockerfile, docker-compose, OpenTelemetry, `.env.example`. Endpoints invoke agents.
- **web** — inherits `typescript-web` structure (pnpm/Next.js): App Router, `services/`, Dockerfile, docker-compose, OpenTelemetry, `.env.example`. API routes invoke agents, frontend provides a UI.

## Patterns

- **Agents** define the agent's behavior, system prompt, and model configuration. Each agent has `AgentInput` and `AgentOutput` (zod schemas).
- **Tools** are functions the agent can call. Framework-agnostic where possible.
- **Prompts** are inlined in agent definitions.
- The execution model layer (commands/routers) invokes agents. Agents use services and tools.

## Decisions

- **Structured I/O:** Every agent defines `AgentInput` and `AgentOutput` via zod.
- **Prompts:** Inlined in agent definitions. No separate prompts directory.
- **`.env.example`:** Always included (API keys for LLM providers).
- **All other decisions** follow from the chosen execution model's conventions.
- **Note:** When `execution_model` is `web`, the template uses pnpm/Next.js (not Bun), matching `typescript-web` conventions.
