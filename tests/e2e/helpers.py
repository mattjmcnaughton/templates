"""Shared helpers and constants for template e2e tests."""

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
            # Skip GitHub Actions workflows — they legitimately use ${{ }}
            rel = file.relative_to(path)
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


def assert_symlink(path: Path, link_name: str, target: str):
    """Assert link_name is a symlink pointing to target."""
    link = path / link_name
    assert link.is_symlink(), f"{link_name} is not a symlink"
    assert str(link.readlink()) == target, (
        f"{link_name} points to {link.readlink()}, expected {target}"
    )
