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

# Install Bun
COPY --from=oven/bun:latest /usr/local/bin/bun /usr/local/bin/bun
COPY --from=oven/bun:latest /usr/local/bin/bunx /usr/local/bin/bunx

# Install Node.js and pnpm
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g pnpm && \
    rm -rf /var/lib/apt/lists/*
