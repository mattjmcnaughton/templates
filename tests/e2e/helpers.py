"""Shared helpers and constants for template e2e tests."""

import re
from datetime import UTC, datetime
from pathlib import Path

JINJA_ARTIFACTS = ["{{", "}}", "{%", "%}", "{#", "#}"]

# Every template gets these same identity answers.
BASE_ANSWERS = {
    "project_name": "my-test-project",
    "project_description": "A test project",
    "author_name": "testauthor",
    "author_email": "test@mattjmcnaughton.com",
    "license": "MIT",
}


def assert_files_exist(path: Path, expected: list[str]):
    """Assert all expected files exist relative to path."""
    for f in expected:
        assert (path / f).exists(), f"Expected file missing: {f}"


def assert_files_absent(path: Path, absent: list[str]):
    """Assert files do NOT exist relative to path."""
    for f in absent:
        assert not (path / f).exists(), f"Unexpected file present: {f}"


def assert_no_raw_jinja(path: Path):
    """Assert no raw Jinja artifacts in generated files.

    GitHub Actions workflow files are excluded because they legitimately
    use ``${{ }}`` syntax which contains ``{{`` and ``}}``.
    """
    extensions = {".py", ".toml", ".yml", ".yaml", ".md", ".ini", ".cfg", ".ts", ".tsx", ".json", ".mjs", ".prisma"}
    extensionless_check = {"justfile", "Dockerfile", "Makefile", "Procfile"}
    for file in path.rglob("*"):
        if file.is_file() and (file.suffix in extensions or file.name in extensionless_check):
            rel = file.relative_to(path)
            # Skip GitHub Actions workflows — they legitimately use ${{ }}
            if rel.parts[:2] == (".github", "workflows"):
                continue
            content = file.read_text()
            # Justfiles legitimately use {{ }} for variable interpolation
            artifacts = JINJA_ARTIFACTS
            if file.name == "justfile":
                artifacts = [a for a in artifacts if a not in ("{{", "}}")]
            for artifact in artifacts:
                assert artifact not in content, (
                    f"Raw Jinja artifact '{artifact}' found in {rel}"
                )


def assert_exclude_newer_stamped(path: Path):
    """Assert ``[tool.uv] exclude-newer`` is a concrete RFC 3339 timestamp.

    uv silently discards the whole ``[tool.uv]`` table when it cannot parse this
    value, so a relative string like ``"1 week"`` leaves resolution unpinned.
    """
    content = (path / "pyproject.toml").read_text()
    match = re.search(r'^exclude-newer = "([^"]+)"$', content, re.MULTILINE)
    assert match, "pyproject.toml has no [tool.uv] exclude-newer setting"
    value = match.group(1)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value), (
        f"exclude-newer must be a concrete RFC 3339 timestamp, got {value!r}"
    )
    cutoff = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    assert cutoff <= datetime.now(UTC), "exclude-newer cutoff must not be in the future"


def assert_symlink(path: Path, link_name: str, target: str):
    """Assert link_name is a symlink pointing to target."""
    link = path / link_name
    assert link.is_symlink(), f"{link_name} is not a symlink"
    assert str(link.readlink()) == target, (
        f"{link_name} points to {link.readlink()}, expected {target}"
    )


def assert_bootstrap_target(path: Path):
    """Assert the justfile declares the conventional ``bootstrap`` target."""
    content = (path / "justfile").read_text()
    assert re.search(r"^bootstrap:", content, re.MULTILINE), (
        "justfile has no bootstrap target"
    )


def assert_suites_have_tests(path: Path, suites: list[str]):
    """Assert every listed test directory contains at least one test file.

    An empty suite makes pytest exit 5 and ``bun test`` exit 1, which turns a
    freshly scaffolded project's CI red on its first commit.
    """
    for suite in suites:
        directory = path / "tests" / suite
        assert directory.is_dir(), f"missing test suite: {suite}"
        found = [
            f for f in directory.iterdir()
            if f.is_file() and ("test" in f.name or "spec" in f.name) and f.name != "__init__.py"
        ]
        assert found, f"test suite {suite} ships no tests"
