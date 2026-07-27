"""E2E tests for the typescript-lib template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_suites_have_tests, assert_bootstrap_target, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.typescript_lib

TEMPLATE = "typescript-lib"


class TestMinimal:
    """typescript-lib with minimal options."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            publish_to_npm=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, [
            "package.json", "tsconfig.json", "biome.json", "bunfig.toml",
            "justfile", "CLAUDE.md", "README.md", "LICENSE",
            ".copier-answers.yml", ".editorconfig", ".gitignore",
            ".github/workflows/ci.yml",
            "src/index.ts",
            "tests/unit/.gitkeep", "tests/integration/.gitkeep", "tests/e2e/.gitkeep",
            "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
        ])

    def test_conditional_files_absent(self):
        assert_files_absent(self.dest, [
            ".github/workflows/publish.yml",
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

    def test_project_name_rendered(self):
        content = (self.dest / "package.json").read_text()
        assert '"my-test-project"' in content

    def test_biome_config(self):
        content = (self.dest / "biome.json").read_text()
        assert '"recommended"' in content

    def test_tsconfig_strict(self):
        content = (self.dest / "tsconfig.json").read_text()
        assert '"strict": true' in content

    def test_bunfig_release_age(self):
        content = (self.dest / "bunfig.toml").read_text()
        assert "minimumReleaseAge = 10080" in content

    def test_justfile_targets(self):
        content = (self.dest / "justfile").read_text()
        assert "bunx biome format" in content
        assert "bunx tsc --noEmit" in content
        assert "bun test tests/unit" in content
        assert "gate:" in content

    def test_no_env_example(self):
        assert_files_absent(self.dest, [".env.example"])


class TestFull:
    """typescript-lib with all options enabled."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="full",
            publish_to_npm=True,
            include_technical_docs=True,
            include_product_docs=True,
            **BASE_ANSWERS,
        )

    def test_publish_workflow_exists(self):
        assert_files_exist(self.dest, [".github/workflows/publish.yml"])

    def test_docs_dirs_exist(self):
        assert_files_exist(self.dest, [
            "docs/technical/.gitkeep",
            "docs/product/.gitkeep",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_publish_workflow_content(self):
        content = (self.dest / ".github/workflows/publish.yml").read_text()
        assert "npm publish" in content
