# typescript-cli

A command-line tool with subcommand scaffolding. Inherits all conventions from `typescript.md` (Bun-based).

## Additional Copier Questions

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `publish_to_npm` | bool | true | Include GitHub Actions workflow for npm publishing |
| `include_database` | bool | false | Include database support (Prisma) |
| `database_type` | choice | postgres | Postgres or SQLite (only if `include_database`) |
| `include_clients` | bool | false | Scaffold a `clients/` module |

## Dependencies

- commander (CLI framework)
- chalk (terminal styling)
- pino (logging)
- zod (config/env validation)
- Prisma (if `include_database`)

## Structure

```
src/
  index.ts               # entry point, commander program setup
  config.ts              # zod-based env/config validation
  logging.ts             # pino setup
  commands/
    index.ts
    <example>.ts         # ExampleInput, ExampleOutput, command definition
  services/
    index.ts             # business logic
  clients/               # only if include_clients
    index.ts
  # --- only if include_database ---
  repositories/
    index.ts
  db.ts                  # Prisma client setup
prisma/
  schema.prisma
# ---
tests/
  unit/
  integration/
  e2e/
tsconfig.json
biome.json
package.json
justfile
.env.example
README.md
CLAUDE.md
AGENTS.md -> CLAUDE.md
LICENSE
.editorconfig
.gitignore
.github/
  workflows/
    ci.yml
    publish.yml          # only if publish_to_npm
```

## Patterns

- **Commands** are thin I/O wrappers. Parse CLI args into `CommandInput`, call a service, format `CommandOutput`.
- **Services** contain business logic. Commands delegate to services.
- **Clients** (optional) encapsulate external API/service calls.
- **Repositories** (only with DB) encapsulate data access via Prisma.
- Input/Output types defined with zod schemas.

## Decisions

- **CLI framework:** commander with subcommand scaffold + chalk for output styling.
- **Documentation:** README only.
- **CI:** Runs `gate-expensive`. Does not run `gate-external`.
- **Publishing:** On by default.
- **No Dockerfile.**
