"""E2E tests for the typescript-agent template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.typescript_agent

TEMPLATE = "typescript-agent"

# Files present regardless of execution model
COMMON_FILES = [
    "package.json", "tsconfig.json", "biome.json",
    "justfile", "CLAUDE.md", "README.md", "LICENSE",
    ".editorconfig", ".gitignore", ".env.example",
    ".github/workflows/ci.yml",
    "src/agents/index.ts", "src/agents/example.ts",
    "src/tools/index.ts",
    "src/services/index.ts",
    "src/config.ts", "src/logging.ts",
    "tests/unit/.gitkeep", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]

CLI_FILES = [
    "src/index.ts",
    "src/commands/index.ts",
    "src/commands/example.ts",
    "bunfig.toml",
]

SERVICE_FILES = [
    "src/index.ts", "src/app.ts", "src/telemetry.ts",
    "src/routers/index.ts", "src/routers/health.ts",
    "src/controllers/index.ts",
    "src/dtos/index.ts",
    "Dockerfile", "docker-compose.yml",
    "bunfig.toml",
    "docs/api.md",
]

WEB_FILES = [
    "src/app/layout.tsx", "src/app/page.tsx",
    "src/app/api/health/route.ts",
    "src/components/.gitkeep", "src/hooks/.gitkeep",
    "src/lib/api.ts", "src/lib/telemetry.ts",
    "Dockerfile", "docker-compose.yml",
    ".npmrc",
    "next.config.ts", "tailwind.config.ts", "postcss.config.js",
]

DB_FILES = [
    "prisma/schema.prisma",
    "src/db.ts",
    "src/repositories/index.ts",
]

CLIENT_FILES = ["src/clients/index.ts"]


class TestClaudeAgentSdkCli:
    """typescript-agent with claude-agent-sdk + cli execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            agent_framework="claude-agent-sdk",
            execution_model="cli",
            publish_to_npm=False,
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
        assert_files_absent(self.dest, [
            "src/app.ts", "src/telemetry.ts",
            "src/routers/index.ts", "src/routers/health.ts",
            "Dockerfile", "docker-compose.yml",
        ])

    def test_web_files_absent(self):
        assert_files_absent(self.dest, [
            "src/app/layout.tsx", "src/app/page.tsx",
            ".npmrc", "next.config.ts",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_bin_entry(self):
        content = (self.dest / "package.json").read_text()
        assert '"bin"' in content

    def test_claude_sdk_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "claude-code-sdk" in content
        assert "commander" in content
        assert "chalk" in content
        assert "hono" not in content
        assert "next" not in content
        assert "@opentelemetry" not in content

    def test_agent_example(self):
        content = (self.dest / "src/agents/example.ts").read_text()
        assert "claude-code-sdk" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "ANTHROPIC_API_KEY" in content
        assert "HOST=" not in content

    def test_no_publish_workflow(self):
        assert_files_absent(self.dest, [".github/workflows/publish.yml"])

    def test_claude_md_mentions_agent(self):
        content = (self.dest / "CLAUDE.md").read_text()
        assert "claude-agent-sdk" in content
        assert "agents/" in content


class TestPiAiService:
    """typescript-agent with pi-ai + service execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pi-svc",
            agent_framework="pi-ai",
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
        assert_files_absent(self.dest, [
            "src/commands/index.ts",
            "src/commands/example.ts",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_pi_ai_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@mariozechner/pi-ai" in content
        assert "@mariozechner/pi-agent-core" in content
        assert "hono" in content
        assert "@opentelemetry/api" in content
        assert "commander" not in content

    def test_agent_example(self):
        content = (self.dest / "src/agents/example.ts").read_text()
        assert "pi-agent-core" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "OPENAI_API_KEY" in content
        assert "HOST=" in content

    def test_dockerfile_bun(self):
        content = (self.dest / "Dockerfile").read_text()
        assert "oven/bun" in content

    def test_docker_compose_empty(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres" not in content

    def test_justfile_has_dev(self):
        content = (self.dest / "justfile").read_text()
        assert "dev:" in content
        assert "bun --watch" in content


class TestLangchainWeb:
    """typescript-agent with langchain-js + web execution model."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="lc-web",
            agent_framework="langchain-js",
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
        assert_files_absent(self.dest, [
            "src/commands/index.ts",
            "src/commands/example.ts",
            "bunfig.toml",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_langchain_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@langchain/core" in content
        assert "langchain" in content
        assert "next" in content
        assert "react" in content
        assert "commander" not in content

    def test_agent_example(self):
        content = (self.dest / "src/agents/example.ts").read_text()
        assert "langchain" in content

    def test_justfile_pnpm(self):
        content = (self.dest / "justfile").read_text()
        assert "pnpm biome" in content
        assert "pnpm next dev" in content

    def test_npmrc_release_age(self):
        content = (self.dest / ".npmrc").read_text()
        assert "minimum-release-age=10080" in content

    def test_dockerfile_node(self):
        content = (self.dest / "Dockerfile").read_text()
        assert "node:22-slim" in content

    def test_env_has_api_key(self):
        content = (self.dest / ".env.example").read_text()
        assert "OPENAI_API_KEY" in content


class TestClaudeAgentSdkServicePostgres:
    """typescript-agent with claude-agent-sdk + service + postgres."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="claude-pg",
            agent_framework="claude-agent-sdk",
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
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" in content
        assert "claude-code-sdk" in content

    def test_postgres_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "postgresql://" in content

    def test_docker_compose_postgres(self):
        content = (self.dest / "docker-compose.yml").read_text()
        assert "postgres:16" in content


class TestClaudeAgentSdkCliPublish:
    """typescript-agent with claude-agent-sdk + cli + publish."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="claude-pub",
            agent_framework="claude-agent-sdk",
            execution_model="cli",
            publish_to_npm=True,
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

    def test_bin_entry(self):
        content = (self.dest / "package.json").read_text()
        assert '"bin"' in content


class TestPiAiCliSqlite:
    """typescript-agent with pi-ai + cli + sqlite."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="pi-sq",
            agent_framework="pi-ai",
            execution_model="cli",
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

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_sqlite_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@prisma/client" in content
        assert "@mariozechner/pi-ai" in content

    def test_sqlite_schema(self):
        content = (self.dest / "prisma/schema.prisma").read_text()
        assert '"sqlite"' in content

    def test_sqlite_env(self):
        content = (self.dest / ".env.example").read_text()
        assert "file:./" in content

    def test_no_otel_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@opentelemetry" not in content
