"""E2E tests for the python-lib template."""

import pytest

from tests.e2e.helpers import BASE_ANSWERS, assert_files_absent, assert_files_exist, assert_no_raw_jinja, assert_symlink

pytestmark = pytest.mark.python_lib

TEMPLATE = "python-lib"
PKG = "my_test_project"


class TestMinimal:
    """python-lib with minimal options."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            publish_to_pypi=False,
            include_technical_docs=False,
            include_product_docs=False,
            **BASE_ANSWERS,
        )

    def test_core_files_exist(self):
        assert_files_exist(self.dest, [
            "pyproject.toml", "justfile", "CLAUDE.md", "README.md", "LICENSE",
            ".editorconfig", ".gitignore",
            ".github/workflows/ci.yml",
            f"src/{PKG}/__init__.py", f"src/{PKG}/py.typed",
            "tests/__init__.py", "tests/conftest.py",
            "tests/unit/__init__.py", "tests/integration/__init__.py", "tests/e2e/__init__.py",
            "docs/adrs/.gitkeep", "docs/architecture.md", "docs/development.md",
        ])

    def test_conditional_files_absent(self):
        assert_files_absent(self.dest, [
            ".github/workflows/publish.yml",
            "docs/technical", "docs/product",
        ])

    def test_no_raw_jinja(self):
        assert_no_raw_jinja(self.dest)

    def test_agents_symlink(self):
        assert_symlink(self.dest, "AGENTS.md", "CLAUDE.md")

    def test_project_name_rendered(self):
        content = (self.dest / "pyproject.toml").read_text()
        assert f'name = "{BASE_ANSWERS["project_name"]}"' in content

    def test_package_name_derived(self):
        content = (self.dest / f"src/{PKG}/__init__.py").read_text()
        assert f'version("{BASE_ANSWERS["project_name"]}")' in content


class TestFull:
    """python-lib with all options enabled."""

    @pytest.fixture(autouse=True)
    def setup(self, copier_copy):
        self.dest = copier_copy(
            TEMPLATE,
            dest_name="full",
            publish_to_pypi=True,
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
