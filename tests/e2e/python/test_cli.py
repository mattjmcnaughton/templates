"""E2E tests for the python-cli template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.python_cli

TEMPLATE = "python-cli"
PKG = "my_test_project"

CORE_FILES = [
    "pyproject.toml", "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    f"src/{PKG}/__init__.py", f"src/{PKG}/py.typed",
    f"src/{PKG}/cli.py", f"src/{PKG}/config.py", f"src/{PKG}/logging.py",
    f"src/{PKG}/commands/__init__.py", f"src/{PKG}/commands/example.py",
    f"src/{PKG}/services/__init__.py",
    "tests/__init__.py", "tests/conftest.py",
    "tests/unit/__init__.py", "tests/integration/__init__.py", "tests/e2e/__init__.py",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]

DB_FILES = [
    "alembic.ini", "alembic/env.py", "alembic/versions/.gitkeep",
    f"src/{PKG}/db.py",
    f"src/{PKG}/models/__init__.py",
    f"src/{PKG}/repositories/__init__.py",
]

CLIENT_FILES = [f"src/{PKG}/clients/__init__.py"]


class TestMinimal:
    """python-cli with no DB, no clients, no publish."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            publish_to_pypi=False,
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
            ".github/workflows/publish.yml",
            *DB_FILES,
            *CLIENT_FILES,
            "docs/technical", "docs/product",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_entry_point(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert f'{BASE_ANSWERS["project_name"]} = "{PKG}.cli:app"' in content

    def test_deps_minimal(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "typer" in content
        assert "structlog" in content
        assert "pydantic-settings" in content
        assert "sqlalchemy" not in content
        assert "asyncpg" not in content
        assert "aiosqlite" not in content

    def test_env_no_database(self):
        content = (self.dest / ".env.example").read_text()
        assert "LOG_LEVEL" in content
        assert "DATABASE_URL" not in content


class TestPostgres:
    """python-cli with Postgres DB + clients + publish."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pg",
            publish_to_pypi=True,
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

    def test_publish_workflow(self):
        assert_files_exist(self.dest, [".github/workflows/publish.yml"])

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

    def test_postgres_config(self):
        content = (self.dest / f"src/{PKG}/config.py").read_text()
        assert "database_url" in content
        assert "postgresql+asyncpg" in content


class TestSqlite:
    """python-cli with SQLite DB, no clients."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="sq",
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

    def test_no_clients(self):
        assert_files_absent(self.dest, CLIENT_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_sqlite_deps(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert "aiosqlite" in content
        assert "asyncpg" not in content

    def test_sqlite_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "sqlite+aiosqlite" in content

    def test_sqlite_config(self):
        content = (self.dest / f"src/{PKG}/config.py").read_text()
        assert "sqlite+aiosqlite" in content
