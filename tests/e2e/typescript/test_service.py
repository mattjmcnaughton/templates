"""E2E tests for the typescript-service template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_suites_have_tests, assert_bootstrap_target, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.typescript_service

TEMPLATE = "typescript-service"

CORE_FILES = [
    "package.json", "tsconfig.json", "biome.json", "bunfig.toml",
    "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".copier-answers.yml", ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    "Dockerfile", ".dockerignore", "docker-compose.yml",
    "src/index.ts", "src/app.ts", "src/config.ts", "src/logging.ts", "src/telemetry.ts",
    "src/routers/index.ts", "src/routers/health.ts",
    "src/controllers/index.ts", "src/services/index.ts", "src/dtos/index.ts",
    "tests/unit/.gitkeep", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md", "docs/api.md",
]

DB_FILES = [
    "prisma/schema.prisma",
    "src/db.ts",
    "src/repositories/index.ts",
]

CLIENT_FILES = ["src/clients/index.ts"]


class TestMinimal:
    """typescript-service with no DB, no clients."""

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

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_bootstrap_target(self):
        assert_bootstrap_target(self.dest)

    def test_every_suite_ships_tests(self):
        assert_suites_have_tests(self.dest, ['unit', 'integration', 'e2e'])

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "hono" in content
        assert "@opentelemetry/api" in content
        assert "pino" in content
        assert "zod" in content
        assert "@prisma/client" not in content

    def test_docker_compose_empty(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content

    def test_dockerfile_bun(self):
        content = (self.dest / "Dockerfile").read_text()
        assert "oven/bun" in content
        assert "EXPOSE 3000" in content

    def test_justfile_has_dev(self):
        content = (self.dest / "justfile").read_text()
        assert "dev:" in content
        assert "bun --watch" in content

    def test_health_no_db_check(self):
        content = (self.dest / "src/routers/health.ts").read_text()
        assert "healthz" in content
        assert "prisma" not in content

    def test_env_has_service_vars(self):
        content = (self.dest / ".env.example").read_text()
        assert "HOST=" in content
        assert "PORT=" in content
        assert "OTEL_EXPORTER" in content
        assert "DATABASE_URL" not in content

    def test_no_publish_workflow(self):
        assert_files_absent(self.dest, [".github/workflows/publish.yml"])


class TestPostgres:
    """typescript-service with Postgres DB + clients + docs."""

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
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" in content
        assert "prisma" in content

    def test_postgres_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"postgresql"' in content

    def test_docker_compose_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" in content

    def test_health_has_db_check(self):
        content = (self.dest / "src/routers/health.ts").read_text()
        assert "prisma" in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql://" in content


class TestSqlite:
    """typescript-service with SQLite DB, no clients."""

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

    def test_sqlite_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"sqlite"' in content
        assert '"postgresql"' not in content

    def test_docker_compose_no_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content
