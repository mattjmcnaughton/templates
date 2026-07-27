# Template Conventions

## Copier Questions

Every template asks these questions:

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `project_name` | str | — | Project/repo name |
| `project_description` | str | — | One-line description |
| `author_name` | str | — | Author or organization |
| `author_email` | str | — | Contact email |
| `license` | choice | MIT | MIT, Apache 2.0, or Proprietary |
| `include_technical_docs` | bool | false | Create `docs/technical/` for TDDs and technical specs |
| `include_product_docs` | bool | false | Create `docs/product/` for PRDs and product briefs |

## Hardcoded Decisions

| Concern | Decision |
| ------- | -------- |
| CI | GitHub Actions, always |
| CLAUDE.md | Always generated. AGENTS.md is a symlink to CLAUDE.md. |
| Dockerfile | Included for service, web, and agent types. Not for lib or cli. |
| Pre-commit hooks | Not included |
| `.editorconfig` | Always included |
| `.gitignore` | Always included (language-specific content) |
| `.env.example` | Included for all types except lib |
| `justfile` | Always included |
| `.copier-answers.yml` | Always written, so generated projects can run `copier update` |
| Test suites | Every suite ships a replaceable smoke test, so a fresh scaffold's CI is green on the first commit |
| Minimum release age | Always configured — only allow packages released at least 7 days ago |

## Justfile Targets

Every template includes a `justfile` with these targets. The underlying tools vary by language but the target names are consistent.

For `-web` templates with separate backend/frontend directories (e.g., `python-web`), each target also has `-be` and `-fe` suffixed variants (e.g., `fmt-be`, `fmt-fe`). The unsuffixed target runs both. Next.js-based templates (`typescript-web`, `typescript-agent` web mode) are monolithic and do not use suffixed variants.

| Target | Purpose |
| ------ | ------- |
| `bootstrap` | Install dependencies and prepare the project for development |
| `fmt` | Check formatting |
| `fmt-fix` | Fix formatting |
| `lint` | Check linting |
| `lint-fix` | Fix linting |
| `typecheck` | Run type checker |
| `test-all` | Run all tests (unit + integration) |
| `test-unit` | Run unit tests only |
| `test-integration` | Run integration tests only |
| `test-e2e` | Run end-to-end tests |
| `test-external` | Run tests that hit external services |
| `gate` | Fast pre-push check: fmt + lint + typecheck + test-unit |
| `gate-expensive` | Full check: gate + test-integration + test-e2e |
| `gate-external` | Everything: gate-expensive + test-external |

## Cross-Template Consistency

The following concerns must be kept consistent across ALL templates. When modifying any of these, apply the change to every template:

- `LICENSE` — file content and `copier.yml` license question
- `.editorconfig` — shared editor settings
- `.gitignore` — common ignores (OS files, editor files); language-specific ignores are per-template
- `.env.example` — structure and variable naming conventions (all types except lib)
- `justfile` — target names must be identical; underlying tools vary by language
- Generated documentation structure — see `generated-docs.md` for CLAUDE.md template, README sections, and `docs/` layout
- CLAUDE.md + AGENTS.md symlink — generated projects should include both
- CI/CD patterns — GitHub Actions, consistent workflow structure and naming
- Docker conventions — base image selection, multi-stage build patterns, label schemas (service/web/agent types only)
- Copier question naming — use the same variable names for the same concepts
- `_answers_file` — every `copier.yml` sets it, and every template ships a
  `{{ _copier_conf.answers_file }}.jinja` file. Setting the key alone is not enough:
  Copier only writes the answers file if the template renders one.
- CI workflow shape — set up the toolchain, install `just`, run `just bootstrap`,
  then run `just gate-expensive`. Do not pass `--frozen`/`--frozen-lockfile` on the
  install: a freshly scaffolded project has no lockfile committed yet.
- Minimum release age — 7-day minimum across all package managers (see below)

## Minimum Release Age

All templates enforce a 7-day minimum release age for dependencies to reduce supply chain risk.

| Package Manager | Config File | Setting |
| --------------- | ----------- | ------- |
| uv (Python) | `pyproject.toml` | `[tool.uv] exclude-newer = "<scaffold date - 7d>T00:00:00Z"` |
| Bun (TS backend) | `bunfig.toml` | `minimumReleaseAge = 10080` |
| pnpm (frontend/Next.js) | `.npmrc` | `minimum-release-age=10080` |

Bun and pnpm express this as a relative window, so their config is static. uv's
`exclude-newer` takes a **concrete RFC 3339 timestamp** — a relative string like
`"1 week"` is not portable: uv versions without duration support fail to parse it
and silently discard the entire `[tool.uv]` table, leaving resolution completely
unpinned while the config still looks pinned.

Python templates therefore ship a `@MIN_RELEASE_AGE_CUTOFF@` placeholder in
`pyproject.toml` and stamp it with `scaffold date - 7 days` from a `_tasks` entry
in `copier.yml`. Generated projects bump the cutoff themselves when they
deliberately take newer dependencies. This requires `copier copy --trust`, which
the templates already need for the `AGENTS.md` symlink task.

## Self-Containment

- Templates should be self-contained. Do not create shared/addon templates that layer on top of others.
- Minor duplication across templates is acceptable and preferred over abstraction.
- The one exception is `frontend-react`, which is designed to be used standalone OR composed into a `-web` template's `frontend/` directory (no file overlap with the backend).
- Each template must have its own `copier.yml` at its root.
