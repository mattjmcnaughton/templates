"""E2E tests for the golang-cli template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_bootstrap_target, assert_files_absent, assert_files_exist, assert_no_raw_jinja

pytestmark = pytest.mark.golang_cli

TEMPLATE = "golang-cli"
PROJECT = "my-test-project"
MODULE_PATH = "github.com/testauthor/my-test-project"

CORE_FILES = [
    "go.mod",
    "justfile",
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "LICENSE",
    ".copier-answers.yml", ".editorconfig",
    ".gitignore",
    ".env.example",
    ".github/workflows/ci.yml",
    f"cmd/{PROJECT}/main.go",
    "internal/cli/root.go",
    "internal/cli/example.go",
    "internal/config/config.go",
    "internal/version/version.go",
    "docs/adrs/.gitkeep",
    "docs/architecture.md",
    "docs/development.md",
]

RELEASE_FILES = [
    ".github/workflows/release.yml",
]


class TestMinimal:
    """golang-cli with no release workflow."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            publish_release=False,
            module_path=MODULE_PATH,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_release_files_absent(self):
        assert_files_absent(self.dest, RELEASE_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_bootstrap_target(self):
        assert_bootstrap_target(self.dest)

    def test_go_mod_module_path(self):
        content = (self.dest / "go.mod").read_text()
        assert f"module {MODULE_PATH}" in content

    def test_go_mod_cobra(self):
        content = (self.dest / "go.mod").read_text()
        assert "github.com/spf13/cobra" in content

    def test_go_mod_viper(self):
        content = (self.dest / "go.mod").read_text()
        assert "github.com/spf13/viper" in content

    def test_main_imports_cli(self):
        content = (self.dest / f"cmd/{PROJECT}/main.go").read_text()
        assert f"{MODULE_PATH}/internal/cli" in content

    def test_root_uses_cobra(self):
        content = (self.dest / "internal/cli/root.go").read_text()
        assert "cobra.Command" in content

    def test_root_uses_viper(self):
        content = (self.dest / "internal/cli/root.go").read_text()
        assert "viper" in content

    def test_root_uses_slog(self):
        content = (self.dest / "internal/cli/root.go").read_text()
        assert "slog" in content

    def test_example_command_exists(self):
        content = (self.dest / "internal/cli/example.go").read_text()
        assert "newExampleCmd" in content

    def test_version_package(self):
        content = (self.dest / "internal/version/version.go").read_text()
        assert 'Version = "dev"' in content

    def test_env_example_has_prefix(self):
        content = (self.dest / ".env.example").read_text()
        assert "MY_TEST_PROJECT_" in content

    def test_justfile_has_gate(self):
        content = (self.dest / "justfile").read_text()
        assert "gate:" in content

    def test_justfile_has_fmt(self):
        content = (self.dest / "justfile").read_text()
        assert "gofmt" in content

    def test_ci_workflow_uses_go(self):
        content = (self.dest / ".github/workflows/ci.yml").read_text()
        assert "setup-go" in content

    def test_claude_md_has_quick_reference(self):
        content = (self.dest / "CLAUDE.md").read_text()
        assert "Quick Reference" in content
        assert "just gate" in content


class TestWithRelease:
    """golang-cli with GoReleaser release workflow."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="release",
            publish_release=True,
            module_path=MODULE_PATH,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, CORE_FILES)

    def test_release_files_exist(self):
        assert_files_exist(self.dest, RELEASE_FILES)

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_release_workflow_on_tag(self):
        content = (self.dest / ".github/workflows/release.yml").read_text()
        assert "tags:" in content
        assert '"v*"' in content

    def test_release_workflow_cross_compiles(self):
        content = (self.dest / ".github/workflows/release.yml").read_text()
        assert "matrix" in content
        assert "linux" in content
        assert "darwin" in content

    def test_release_workflow_injects_version(self):
        content = (self.dest / ".github/workflows/release.yml").read_text()
        assert MODULE_PATH in content
        assert "version.Version" in content
