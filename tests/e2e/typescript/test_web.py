"""E2E tests for the typescript-web template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.typescript_web

TEMPLATE = "typescript-web"

CORE_FILES = [
    "package.json", "tsconfig.json", "biome.json", ".npmrc",
    "next.config.ts", "tailwind.config.ts", "postcss.config.js",
    "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    "Dockerfile", ".dockerignore", "docker-compose.yml",
    "src/app/layout.tsx", "src/app/page.tsx", "src/app/globals.css",
    "src/app/api/health/route.ts",
    "src/components/.gitkeep", "src/hooks/.gitkeep",
    "src/lib/api.ts", "src/lib/config.ts", "src/lib/logging.ts", "src/lib/telemetry.ts",
    "src/services/index.ts",
    "tests/unit/.gitkeep", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]

DB_FILES = [
    "prisma/schema.prisma",
    "src/db.ts",
    "src/repositories/index.ts",
]


class TestMinimal:
    """typescript-web with no DB, no optional libs."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            include_database=False,
            include_shadcn=False,
            include_zustand=False,
            include_recharts=False,
            include_forms=False,
            include_tables=False,
            include_axios=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_conditional_files_absent(self):
        assert_files_absent(self.dest, [
            *DB_FILES,
            "src/components/ui/.gitkeep",
            "docs/technical", "docs/product",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "next" in content
        assert "react" in content
        assert "tailwindcss" in content
        assert "@opentelemetry/api" in content
        assert "vitest" in content
        assert "@playwright/test" in content
        assert "@prisma/client" not in content
        assert "zustand" not in content

    def test_npmrc_release_age(self):
        content = (self.dest / ".npmrc").read_text()
        assert "minimum-release-age=10080" in content

    def test_dockerfile_node(self):
        content = (self.dest / "Dockerfile").read_text()
        assert "node:22-slim" in content

    def test_docker_compose_empty(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content

    def test_justfile_pnpm(self):
        content = (self.dest / "justfile").read_text()
        assert "pnpm biome format" in content
        assert "pnpm vitest" in content
        assert "pnpm exec playwright" in content
        assert "pnpm next dev" in content

    def test_health_no_db(self):
        content = (self.dest / "src/app/api/health/route.ts").read_text()
        assert "prisma" not in content

    def test_no_publish_workflow(self):
        assert_files_absent(self.dest, [".github/workflows/publish.yml"])


class TestPostgres:
    """typescript-web with Postgres DB + shadcn + zustand + docs."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pg",
            include_database=True,
            database_type="postgres",
            include_shadcn=True,
            include_zustand=True,
            include_recharts=False,
            include_forms=False,
            include_tables=False,
            include_axios=False,
            include_technical_docs=True,
            include_product_docs=True,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_db_files_exist(self):
        assert_files_exist(self.dest, DB_FILES)

    def test_shadcn_dir_exists(self):
        assert_files_exist(self.dest, ["src/components/ui/.gitkeep"])

    def test_docs_dirs(self):
        assert_files_exist(self.dest, ["docs/technical/.gitkeep", "docs/product/.gitkeep"])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_postgres_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" in content
        assert "prisma" in content
        assert "zustand" in content
        assert "@shadcn/ui" in content

    def test_postgres_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"postgresql"' in content

    def test_docker_compose_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" in content

    def test_health_has_db_check(self):
        content = (self.dest / "src/app/api/health/route.ts").read_text()
        assert "prisma" in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql://" in content


class TestSqlite:
    """typescript-web with SQLite DB."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="sq",
            include_database=True,
            database_type="sqlite",
            include_shadcn=False,
            include_zustand=False,
            include_recharts=False,
            include_forms=False,
            include_tables=False,
            include_axios=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_db_files_exist(self):
        assert_files_exist(self.dest, DB_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_sqlite_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"sqlite"' in content
        assert '"postgresql"' not in content

    def test_docker_compose_no_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content


class TestAllOptionalLibs:
    """typescript-web with all optional libs, no DB."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="all-libs",
            include_database=False,
            include_shadcn=True,
            include_zustand=True,
            include_recharts=True,
            include_forms=True,
            include_tables=True,
            include_axios=True,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_all_optional_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@shadcn/ui" in content
        assert "zustand" in content
        assert "recharts" in content
        assert "react-hook-form" in content
        assert "@hookform/resolvers" in content
        assert "@tanstack/react-table" in content
        assert "axios" in content

    def test_no_db_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" not in content

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)
