# ADR 001: Monorepo for Copier Templates

## Status

Accepted

## Context

We need to decide whether to host each Copier template in its own Git repository or consolidate them into a single monorepo.

Copier officially recommends one template per repo because its update mechanism (`copier update`) relies on Git tags, which are repo-wide. Multiple templates sharing tags makes version history ambiguous — a tag doesn't indicate which template changed.

## Decision

Use a single monorepo with each template in its own top-level directory, each containing an independent `copier.yml`.

## Rationale

- The primary consumers are AI agents, which will mostly run `copier copy` from a local clone rather than `copier update`. The tag ambiguity issue is largely irrelevant.
- We don't plan to use semver or per-template release workflows.
- A monorepo avoids the overhead of managing many small repos (CI configs, permissions, cross-repo convention drift).
- Conventions and shared patterns are easier to keep consistent when everything is in one place.

## Consequences

- All templates share a single Git history and tag namespace.
- `copier update` will work but version semantics are imprecise (a version bump may not reflect changes to the template in question).
- If precise per-template versioning becomes necessary, we would need to migrate to separate repos or adopt a tag convention like `<template>/v1.0.0` with explicit `--vcs-ref` usage.
