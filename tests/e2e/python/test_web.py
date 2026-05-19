"""E2E tests for the python-web template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.python_web

TEMPLATE = "python-web"
PKG = "my_test_project"

CORE_FILES = [
    "pyproject.toml", "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    "Dockerfile", ".dockerignore", "docker-compose.yml",
    f"src/{PKG}/__init__.py", f"src/{PKG}/py.typed",
    f"src/{PKG}/app.py", f"src/{PKG}/config.py",
    f"src/{PKG}/logging.py",
    f"src/{PKG}/routers/__init__.py", f"src/{PKG}/routers/health.py",
    f"src/{PKG}/controllers/__init__.py",
    f"src/{PKG}/services/__init__.py",
    f"src/{PKG}/dtos/__init__.py",
    f"src/{PKG}/web/__init__.py",
    f"src/{PKG}/web/serve.py",
    f"src/{PKG}/web/frontend/README.md",
    "tests/__init__.py", "tests/conftest.py",
    "tests/unit/__init__.py", "tests/integration/__init__.py", "tests/e2e/__init__.py",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md", "docs/api.md",
]

DB_FILES = [
    "alembic.ini", "alembic/env.py", "alembic/versions/.gitkeep",
    f"src/{PKG}/db.py",
    f"src/{PKG}/models/__init__.py",
    f"src/{PKG}/repositories/__init__.py",
]

CLIENT_FILES = [f"src/{PKG}/clients/__init__.py"]


class TestMinimal:
    """python-web with no DB, no clients."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            include_database=False,
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_conditional_files_absent(self):
        assert_files_absent(self.dest, [
            *DB_FILES,
            *CLIENT_FILES,
            "docs/technical", "docs/product",
        ])

    def test_no_publish_workflow(self):
        assert_files_absent(self.dest, [".github/workflows/publish.yml"])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_no_entry_point(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "[project.scripts]" not in content

    def test_deps_minimal(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "fastapi" in content
        assert "uvicorn" in content
        assert "opentelemetry" not in content
        assert "structlog" in content
        assert "sqlalchemy" not in content

    def test_telemetry_absent(self):
        assert_files_absent(self.dest, [f"src/{PKG}/telemetry.py"])

    def test_justfile_has_be_fe_targets(self):
        content = (self.dest / "justfile").read_text()
        assert "fmt-be" in content
        assert "fmt-fe" in content
        assert "gate-be" in content
        assert "gate-fe" in content
        assert "dev-be" in content
        assert "dev-fe" in content

    def test_justfile_has_frontend_dir(self):
        content = (self.dest / "justfile").read_text()
        assert f"src/{PKG}/web/frontend" in content

    def test_web_serve_exists(self):
        content = (self.dest / f"src/{PKG}/web/serve.py").read_text()
        assert "mount_frontend" in content
        assert "StaticFiles" in content

    def test_app_mounts_frontend(self):
        content = (self.dest / f"src/{PKG}/app.py").read_text()
        assert "mount_frontend" in content

    def test_frontend_readme_has_instructions(self):
        content = (self.dest / f"src/{PKG}/web/frontend/README.md").read_text()
        assert "frontend-react" in content
        assert "copier copy" in content

    def test_claude_md_mentions_frontend(self):
        content = (self.dest / "CLAUDE.md").read_text()
        assert "frontend" in content.lower()
        assert "dev-be" in content
        assert "dev-fe" in content

    def test_env_has_service_vars(self):
        content = (self.dest / ".env.example").read_text()
        assert "HOST=" in content
        assert "PORT=" in content
        assert "OTEL_EXPORTER_OTLP_ENDPOINT" not in content
        assert "DATABASE_URL" not in content

    def test_docker_compose_empty(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content


class TestPostgres:
    """python-web with Postgres DB + clients."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pg",
            include_database=True,
            database_type="postgres",
            include_clients=True,
            include_technical_docs=True,
            include_product_docs=True,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

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
        assert "aiosqlite" not in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql+asyncpg" in content

    def test_docker_compose_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" in content
        assert "pgdata" in content

    def test_health_has_db_check(self):
        content = (self.dest / f"src/{PKG}/routers/health.py").read_text()
        assert "async_session" in content
        assert "SELECT 1" in content

    def test_architecture_mentions_frontend(self):
        content = (self.dest / "docs/architecture.md").read_text()
        assert "frontend" in content.lower()
        assert "serve.py" in content

    def test_development_mentions_frontend(self):
        content = (self.dest / "docs/development.md").read_text()
        assert "pnpm" in content
        assert "dev-be" in content
        assert "dev-fe" in content


class TestSqlite:
    """python-web with SQLite DB, no clients."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="sq",
            include_database=True,
            database_type="sqlite",
            include_clients=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_db_files_exist(self):
        assert_files_exist(self.dest, DB_FILES)

    def test_no_clients(self):
        assert_files_absent(self.dest, CLIENT_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_sqlite_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "aiosqlite" in content
        assert "asyncpg" not in content

    def test_docker_compose_no_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" not in content

    def test_web_files_exist(self):
        assert_files_exist(self.dest, [
            f"src/{PKG}/web/__init__.py",
            f"src/{PKG}/web/serve.py",
            f"src/{PKG}/web/frontend/README.md",
        ])


class TestOtelEnabled:
    """python-web with enable_otel=True."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="otel",
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
        assert "opentelemetry-sdk" in content
        assert "opentelemetry-instrumentation-fastapi" in content
        assert "opentelemetry-exporter-otlp" in content
        assert "opentelemetry-instrumentation-sqlalchemy" in content

    def test_app_calls_setup_telemetry(self):
        content = (self.dest / f"src/{PKG}/app.py").read_text()
        assert "setup_telemetry(app)" in content

    def test_config_has_otel_endpoint(self):
        content = (self.dest / f"src/{PKG}/config.py").read_text()
        assert "otel_exporter_otlp_endpoint" in content

    def test_env_has_otel_endpoint(self):
        content = (self.dest / ".env.example").read_text()
        assert "OTEL_EXPORTER_OTLP_ENDPOINT=" in content

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)
