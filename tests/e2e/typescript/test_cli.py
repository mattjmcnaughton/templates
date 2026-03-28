"""E2E tests for the typescript-cli template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.typescript_cli

TEMPLATE = "typescript-cli"

CORE_FILES = [
    "package.json", "tsconfig.json", "biome.json", "bunfig.toml",
    "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    "src/index.ts", "src/config.ts", "src/logging.ts",
    "src/commands/index.ts", "src/commands/example.ts",
    "src/services/index.ts",
    "tests/unit/.gitkeep", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]

DB_FILES = [
    "prisma/schema.prisma",
    "src/db.ts",
    "src/repositories/index.ts",
]

CLIENT_FILES = ["src/clients/index.ts"]


class TestMinimal:
    """typescript-cli with no DB, no clients, no publish."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            publish_to_npm=False,
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

    def test_bin_entry(self):
        content = (self.dest / "package.json").read_text()
        assert '"bin"' in content
        assert '"my-test-project"' in content

    def test_deps_minimal(self):
        content = (self.dest / "package.json").read_text()
        assert "commander" in content
        assert "chalk" in content
        assert "pino" in content
        assert "zod" in content
        assert "@prisma/client" not in content
        assert "prisma" not in content

    def test_env_no_database(self):
        content = (self.dest / ".env.example").read_text()
        assert "LOG_LEVEL" in content
        assert "DATABASE_URL" not in content

    def test_commander_setup(self):
        content = (self.dest / "src/index.ts").read_text()
        assert "commander" in content
        assert "my-test-project" in content


class TestPostgres:
    """typescript-cli with Postgres DB + clients + publish."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pg",
            publish_to_npm=True,
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
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" in content
        assert "prisma" in content

    def test_postgres_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"postgresql"' in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql://" in content

    def test_config_has_database(self):
        content = (self.dest / "src/config.ts").read_text()
        assert "DATABASE_URL" in content


class TestSqlite:
    """typescript-cli with SQLite DB, no clients."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="sq",
            publish_to_npm=False,
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

    def test_sqlite_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"sqlite"' in content
        assert '"postgresql"' not in content

    def test_sqlite_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "file:./" in content
