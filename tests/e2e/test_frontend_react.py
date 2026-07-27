"""E2E tests for the frontend-react template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_suites_have_tests, assert_bootstrap_target, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.frontend_react

TEMPLATE = "frontend-react"

# Files present in ALL builds (standalone and composed)
CORE_FILES = [
    "package.json", "tsconfig.json", "tsconfig.app.json", "tsconfig.node.json",
    "biome.json", ".npmrc",
    "vite.config.ts", "tailwind.config.ts", "postcss.config.js",
    "justfile", "index.html",
    "src/main.tsx", "src/index.css", "src/vite-env.d.ts",
    "src/routes/__root.tsx", "src/routes/index.tsx",
    "src/components/.gitkeep", "src/hooks/.gitkeep",
    "src/lib/api.ts",
    "public/vite.svg",
    "tests/setup.ts", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
]

# Files present ONLY in standalone builds
STANDALONE_FILES = [
    "CLAUDE.md", "README.md", "LICENSE",
    ".copier-answers.yml", ".editorconfig", ".gitignore", ".env.example",
    "Caddyfile", "Dockerfile", "docker-compose.yml",
    ".github/workflows/ci.yml",
    "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
]


class TestMinimal:
    """frontend-react standalone with no optional libs."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            is_composed=False,
            include_shadcn=False,
            include_zustand=False,
            include_recharts=False,
            include_forms=False,
            include_tables=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_standalone_files_exist(self):
        assert_files_exist(self.dest, STANDALONE_FILES)

    def test_conditional_files_absent(self):
        assert_files_absent(self.dest, [
            "src/components/ui/.gitkeep",
            "docs/technical", "docs/product",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_bootstrap_target(self):
        assert_bootstrap_target(self.dest)

    def test_every_suite_ships_tests(self):
        assert_suites_have_tests(self.dest, ['integration', 'e2e'])

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "react" in content
        assert "react-dom" in content
        assert "@tanstack/react-router" in content
        assert "@tanstack/react-query" in content
        assert "vite" in content
        assert "tailwindcss" in content
        assert "vitest" in content
        assert "@playwright/test" in content
        assert "msw" in content
        # Should NOT have optional deps
        assert "zustand" not in content
        assert "@shadcn/ui" not in content
        assert "recharts" not in content
        assert "react-hook-form" not in content
        assert "@tanstack/react-table" not in content

    def test_npmrc_release_age(self):
        content = (self.dest / ".npmrc").read_text()
        assert "minimum-release-age=10080" in content

    def test_dockerfile_caddy_nonroot(self):
        content = (self.dest / "Dockerfile").read_text()
        assert "caddy:alpine" in content
        assert "USER app" in content
        assert "EXPOSE 8080" in content

    def test_caddyfile(self):
        content = (self.dest / "Caddyfile").read_text()
        assert ":8080" in content
        assert "try_files" in content
        assert "/index.html" in content

    def test_vite_config_no_proxy(self):
        content = (self.dest / "vite.config.ts").read_text()
        assert "proxy" not in content
        assert "jsdom" in content
        assert "setup.ts" in content

    def test_justfile_targets(self):
        content = (self.dest / "justfile").read_text()
        assert "pnpm biome format" in content
        assert "pnpm vitest run src/" in content
        assert "pnpm vitest run tests/integration" in content
        assert "pnpm exec playwright" in content
        assert "pnpm vite" in content

    def test_gitignore_vite(self):
        content = (self.dest / ".gitignore").read_text()
        assert "routeTree.gen.ts" in content
        assert ".next" not in content


class TestComposed:
    """frontend-react composed into a parent -web template."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            is_composed=True,
            include_shadcn=False,
            include_zustand=False,
            include_recharts=False,
            include_forms=False,
            include_tables=False,
            project_name="my-test-project",
            project_description="A test project",
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_standalone_files_absent(self):
        assert_files_absent(self.dest, STANDALONE_FILES + ["AGENTS.md"])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_vite_config_has_proxy(self):
        content = (self.dest / "vite.config.ts").read_text()
        assert "proxy" in content
        assert "/api" in content
        assert "localhost:8000" in content

    def test_package_json_no_author(self):
        content = (self.dest / "package.json").read_text()
        assert '"author"' not in content

    def test_no_docs(self):
        assert_files_absent(self.dest, [
            "docs/architecture.md", "docs/development.md", "docs/adrs",
        ])


class TestAllOptionalLibs:
    """frontend-react with all optional libs enabled."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            is_composed=False,
            include_shadcn=True,
            include_zustand=True,
            include_recharts=True,
            include_forms=True,
            include_tables=True,
            include_technical_docs=True,
            include_product_docs=True,
            **BASE_ANSWERS,
        )

    def test_all_optional_deps(self):
        content = (self.dest / "package.json").read_text()
        assert "@shadcn/ui" in content
        assert "zustand" in content
        assert "recharts" in content
        assert "react-hook-form" in content
        assert "@hookform/resolvers" in content
        assert "zod" in content
        assert "@tanstack/react-table" in content

    def test_shadcn_dir(self):
        assert_files_exist(self.dest, ["src/components/ui/.gitkeep"])

    def test_docs_dirs(self):
        assert_files_exist(self.dest, [
            "docs/technical/.gitkeep", "docs/product/.gitkeep",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")
