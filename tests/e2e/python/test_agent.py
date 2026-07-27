"""E2E tests for the python-agent template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_suites_have_tests, assert_bootstrap_target, assert_exclude_newer_stamped, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.python_agent

TEMPLATE = "python-agent"
PKG = "my_test_project"

# Files present regardless of execution model
COMMON_FILES = [
    "pyproject.toml", "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".copier-answers.yml", ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    f"src/{PKG}/__init__.py", f"src/{PKG}/py.typed",
    f"src/{PKG}/config.py", f"src/{PKG}/logging.py",
    f"src/{PKG}/agents/__init__.py", f"src/{PKG}/agents/example.py",
    f"src/{PKG}/tools/__init__.py",
    f"src/{PKG}/services/__init__.py",
    "tests/__init__.py", "tests/conftest.py",
    "tests/unit/__init__.py", "tests/integration/__init__.py", "tests/e2e/__init__.py",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]

CLI_FILES = [
    f"src/{PKG}/cli.py",
    f"src/{PKG}/commands/__init__.py",
]

SERVICE_FILES = [
    f"src/{PKG}/app.py",
    f"src/{PKG}/routers/__init__.py", f"src/{PKG}/routers/health.py",
    f"src/{PKG}/controllers/__init__.py",
    f"src/{PKG}/dtos/__init__.py",
    "Dockerfile", "docker-compose.yml",
    "docs/api.md",
]

WEB_FILES = [
    *SERVICE_FILES,
    f"src/{PKG}/web/__init__.py",
    f"src/{PKG}/web/serve.py",
    f"src/{PKG}/web/frontend/README.md",
]

DB_FILES = [
    "alembic.ini", "alembic/env.py", "alembic/script.py.mako", "alembic/versions/.gitkeep",
    f"src/{PKG}/db.py",
    f"src/{PKG}/models/__init__.py",
    f"src/{PKG}/repositories/__init__.py",
]

CLIENT_FILES = [f"src/{PKG}/clients/__init__.py"]


class TestPydanticAiCli:
    """python-agent with pydantic-ai + cli execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            agent_framework="pydantic-ai",
            execution_model="cli",
            publish_to_pypi=False,
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_common_files_exist(self):
        assert_files_exist(self.dest, COMMON_FILES)

    def test_cli_files_exist(self):
        assert_files_exist(self.dest, CLI_FILES)

    def test_service_files_absent(self):
        assert_files_absent(self.dest, SERVICE_FILES)

    def test_web_files_absent(self):
        assert_files_absent(self.dest, [
            f"src/{PKG}/web/__init__.py",
            f"src/{PKG}/web/serve.py",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_bootstrap_target(self):
        assert_bootstrap_target(self.dest)

    def test_every_suite_ships_tests(self):
        assert_suites_have_tests(self.dest, ['unit', 'integration', 'e2e'])

    def test_exclude_newer_is_concrete(self):
        assert_exclude_newer_stamped(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_entry_point(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "[project.scripts]" in content
        assert "my-test-project" in content

    def test_pydantic_ai_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "pydantic-ai" in content
        assert "typer" in content
        assert "fastapi" not in content
        assert "uvicorn" not in content
        assert "opentelemetry" not in content

    def test_agent_example(self):
        content = (self.dest / f"src/{PKG}/agents/example.py").read_text()
        assert "pydantic_ai" in content
        assert "Agent" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "OPENAI_API_KEY" in content
        assert "HOST=" not in content

    def test_no_publish_workflow(self):
        assert_files_absent(self.dest, [".github/workflows/publish.yml"])

    def test_claude_md_mentions_agent(self):
        content = (self.dest / "CLAUDE.md").read_text()
        assert "pydantic-ai" in content
        assert "agents/" in content


class TestClaudeAgentSdkService:
    """python-agent with claude-agent-sdk + service execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="claude-svc",
            agent_framework="claude-agent-sdk",
            execution_model="service",
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_common_files_exist(self):
        assert_files_exist(self.dest, COMMON_FILES)

    def test_service_files_exist(self):
        assert_files_exist(self.dest, SERVICE_FILES)

    def test_cli_files_absent(self):
        assert_files_absent(self.dest, CLI_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_no_entry_point(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "[project.scripts]" not in content

    def test_claude_sdk_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "claude-agent-sdk" in content
        assert "fastapi" in content
        assert "uvicorn" in content
        assert "opentelemetry" not in content
        assert "typer" not in content

    def test_agent_example(self):
        content = (self.dest / f"src/{PKG}/agents/example.py").read_text()
        assert "claude_agent_sdk" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "ANTHROPIC_API_KEY" in content
        assert "HOST=" in content

    def test_docker_compose_empty(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content

    def test_justfile_has_dev(self):
        content = (self.dest / "justfile").read_text()
        assert "dev:" in content
        assert "dev-be" not in content


class TestLangchainWeb:
    """python-agent with langchain + web execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="lc-web",
            agent_framework="langchain",
            execution_model="web",
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_common_files_exist(self):
        assert_files_exist(self.dest, COMMON_FILES)

    def test_web_files_exist(self):
        assert_files_exist(self.dest, WEB_FILES)

    def test_cli_files_absent(self):
        assert_files_absent(self.dest, CLI_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_langchain_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "langchain" in content
        assert "langchain-core" in content
        assert "fastapi" in content
        assert "typer" not in content

    def test_agent_example(self):
        content = (self.dest / f"src/{PKG}/agents/example.py").read_text()
        assert "langchain" in content
        assert "init_chat_model" in content

    def test_justfile_has_be_fe_targets(self):
        content = (self.dest / "justfile").read_text()
        assert "fmt-be" in content
        assert "fmt-fe" in content
        assert "dev-be" in content
        assert "dev-fe" in content

    def test_web_serve_exists(self):
        content = (self.dest / f"src/{PKG}/web/serve.py").read_text()
        assert "mount_frontend" in content

    def test_app_mounts_frontend(self):
        content = (self.dest / f"src/{PKG}/app.py").read_text()
        assert "mount_frontend" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "OPENAI_API_KEY" in content


class TestPydanticAiServicePostgres:
    """python-agent with pydantic-ai + service + postgres."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pai-pg",
            agent_framework="pydantic-ai",
            execution_model="service",
            include_database=True,
            database_type="postgres",
            include_clients=True,
            include_technical_docs=True,
            include_product_docs=True,
            **BASE_ANSWERS,
        )

    def test_common_files_exist(self):
        assert_files_exist(self.dest, COMMON_FILES)

    def test_service_files_exist(self):
        assert_files_exist(self.dest, SERVICE_FILES)

    def test_db_files_exist(self):
        assert_files_exist(self.dest, DB_FILES)

    def test_client_files_exist(self):
        assert_files_exist(self.dest, CLIENT_FILES)

    def test_docs_dirs(self):
        assert_files_exist(self.dest, ["docs/technical/.gitkeep", "docs/product/.gitkeep"])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_postgres_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "sqlalchemy" in content
        assert "alembic" in content
        assert "asyncpg" in content
        assert "pydantic-ai" in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql+asyncpg" in content

    def test_docker_compose_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" in content


    def test_alembic_uses_async_driver(self):
        content = (self.dest / "alembic/env.py").read_text()
        assert "async_engine_from_config" in content
        assert "run_sync" in content
        # The URL must not be downgraded to a sync driver the project lacks.
        assert 'replace("+asyncpg"' not in content

    def test_alembic_versions_are_committed(self):
        content = (self.dest / ".gitignore").read_text()
        assert "alembic/versions/*.py" not in content

class TestPydanticAiCliPublish:
    """python-agent with pydantic-ai + cli + publish_to_pypi."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pai-pub",
            agent_framework="pydantic-ai",
            execution_model="cli",
            publish_to_pypi=True,
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_publish_workflow_exists(self):
        assert_files_exist(self.dest, [".github/workflows/publish.yml"])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_entry_point(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "[project.scripts]" in content


class TestClaudeAgentSdkCliSqlite:
    """python-agent with claude-agent-sdk + cli + sqlite."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="claude-sq",
            agent_framework="claude-agent-sdk",
            execution_model="cli",
            publish_to_pypi=False,
            include_database=True,
            database_type="sqlite",
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_db_files_exist(self):
        assert_files_exist(self.dest, DB_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_sqlite_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "aiosqlite" in content
        assert "asyncpg" not in content
        assert "claude-agent-sdk" in content

    def test_sqlite_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "sqlite+aiosqlite" in content

    def test_no_otel_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "opentelemetry" not in content


class TestServiceOtelEnabled:
    """python-agent in service mode with enable_otel=True."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="svc-otel",
            agent_framework="pydantic-ai",
            execution_model="service",
            include_database=True,
            database_type="postgres",
            include_clients=False,
            enable_otel=True,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_telemetry_file_exists(self):
        assert_files_exist(self.dest, [f"src/{PKG}/telemetry.py"])

    def test_otel_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "opentelemetry-api" in content
        assert "opentelemetry-instrumentation-fastapi" in content
        assert "opentelemetry-instrumentation-sqlalchemy" in content

    def test_app_calls_setup_telemetry(self):
        content = (self.dest / f"src/{PKG}/app.py").read_text()
        assert "setup_telemetry(app)" in content

    def test_env_has_otel_endpoint(self):
        content = (self.dest / ".env.example").read_text()
        assert "OTEL_EXPORTER_OTLP_ENDPOINT=" in content

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)


class TestServiceOtelDisabledByDefault:
    """python-agent in service mode with default (enable_otel=False)."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="svc-no-otel",
            agent_framework="pydantic-ai",
            execution_model="service",
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_telemetry_absent(self):
        assert_files_absent(self.dest, [f"src/{PKG}/telemetry.py"])

    def test_no_otel_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "opentelemetry" not in content

    def test_app_no_setup_telemetry(self):
        content = (self.dest / f"src/{PKG}/app.py").read_text()
        assert "setup_telemetry" not in content

    def test_env_no_otel(self):
        content = (self.dest / ".env.example").read_text()
        assert "OTEL_EXPORTER_OTLP_ENDPOINT" not in content
