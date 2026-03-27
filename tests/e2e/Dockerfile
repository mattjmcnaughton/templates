FROM python:3.12-slim AS base

# Install system deps (git required by copier)
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Add uv tools to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install just and copier via uv
RUN uv tool install rust-just && uv tool install copier
