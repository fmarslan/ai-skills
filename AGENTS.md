# AI Skills Repository

This repository contains reusable Codex skills for project initialization and development environment bootstrap.

## Repository Rules

- Write all documentation and code comments in English.
- Keep skills modular and self-contained.
- Do not add `scripts/` unless deterministic validation or generation becomes necessary.
- Prefer references for detailed policies and templates for reusable output files.
- Keep generated development environments minimal, reproducible, and production-aware.
- Never generate real secrets.
- Never use `Dockerfile` naming. Use `Containerfile`.
- Never use `docker-compose.yml`. Use `compose.yaml`.

## Available Skills

- `devcontainer-project-bootstrap`: Step-by-step wizard for initializing software projects with standardized Docker Compose based Dev Container environments.
