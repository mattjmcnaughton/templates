"""Shared fixtures for template e2e tests.

Each copier copy runs inside a Docker container for host isolation.
Templates are mounted read-only; output is docker-cp'd back to host for assertions.
"""

import subprocess
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
DOCKERFILE = Path(__file__).parent / "Dockerfile"
IMAGE_NAME = "templates-e2e-runner"


@pytest.fixture(scope="session")
def docker_image():
    """Build the test runner Docker image once per session."""
    result = subprocess.run(
        ["docker", "build", "-t", IMAGE_NAME, "-f", str(DOCKERFILE), "."],
        cwd=str(DOCKERFILE.parent),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Docker build failed:\n{result.stderr}"
    return IMAGE_NAME


@pytest.fixture
def copier_copy(tmp_path, docker_image):
    """Return a helper that runs copier copy inside a Docker container.

    Uses docker cp to retrieve output (bind mounts to macOS temp dirs are unreliable).
    """

    def _copy(template_name: str, dest_name: str = "output", **answers) -> Path:
        dest = tmp_path / dest_name
        container_name = f"copier-{uuid.uuid4().hex[:12]}"

        answer_args = []
        for key, value in answers.items():
            if isinstance(value, bool):
                answer_args.extend(["-d", f"{key}={'true' if value else 'false'}"])
            else:
                answer_args.extend(["-d", f"{key}={value}"])

        # Run copier in a named container (templates mounted read-only, output stays inside)
        run_cmd = [
            "docker", "run", "--name", container_name,
            "-v", f"{TEMPLATES_DIR}:/templates:ro",
            docker_image,
            "copier", "copy", "--trust", "--defaults",
            *answer_args,
            f"/templates/{template_name}", "/output",
        ]
        result = subprocess.run(run_cmd, capture_output=True, text=True)

        try:
            assert result.returncode == 0, (
                f"copier copy failed:\n{result.stderr}\n{result.stdout}"
            )
            # Copy output from container to host
            cp_result = subprocess.run(
                ["docker", "cp", f"{container_name}:/output/.", str(dest)],
                capture_output=True, text=True,
            )
            assert cp_result.returncode == 0, (
                f"docker cp failed:\n{cp_result.stderr}"
            )
        finally:
            # Always clean up the container
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
            )

        return dest

    return _copy


@pytest.fixture
def run_in_container(docker_image):
    """Return a helper that runs a command inside a Docker container against a generated project."""

    def _run(project_path: Path, command: str, timeout: int = 300) -> subprocess.CompletedProcess:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{project_path}:/project",
            "-w", "/project",
            docker_image,
            "bash", "-c", command,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    return _run
