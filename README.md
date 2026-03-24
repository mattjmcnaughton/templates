# templates

A monorepo of [Copier](https://copier.readthedocs.io/) templates for scaffolding new projects across multiple languages and frameworks.

## Available Templates

| Template | Description |
| -------- | ----------- |
| `python-lib` | pip-installable library |
| `python-cli` | Command-line tool |
| `python-service` | Backend API (FastAPI, Dockerfile) |
| `python-web` | Full-stack web app (backend + React frontend) |
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
| `frontend-react` | Standalone React app (also composable into `-web` templates) |

## Prerequisites

- [Copier](https://copier.readthedocs.io/) v9+

Install with uv:

```sh
uv tool install copier
```

## Usage

Generate a new project from a template:

```sh
copier copy gh:mattjmcnaughton/templates -a -d template_name=<template-name> /path/to/destination
```

Or from a local clone:

```sh
copier copy /path/to/repo/templates/<template-name> /path/to/destination
```

## Repository Structure

Each directory under `templates/` is a standalone Copier template containing its own `copier.yml` and template files.

```
templates/
  <template-name>/
    copier.yml       # Template configuration and questions
    {{_copier_conf.answers_file}}.jinja   # Answers file (auto-generated)
    ...              # Template files and directories
```

## Creating a New Template

1. Create a new directory under `templates/` with a descriptive name.
2. Add a `copier.yml` defining the template's questions and configuration.
3. Add template files using [Jinja](https://jinja.palletsprojects.com/) syntax.
4. Update the table in this README.

See the [Copier docs](https://copier.readthedocs.io/en/stable/creating/) for a full guide on authoring templates.

## Contributing

Contributions are welcome! Please open an issue or pull request.

## License

[MIT](LICENSE)
