"""Shared pytest fixtures and configuration."""

import pytest


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Treat an empty suite as a pass rather than a failure.

    pytest exits with code 5 (NO_TESTS_COLLECTED) when a suite matches no
    tests. The integration, e2e and external suites legitimately start out
    empty, and a bare exit 5 turns a freshly scaffolded project's CI red on its
    first commit.
    """
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
