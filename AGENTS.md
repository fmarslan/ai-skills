# AI Skills Repository

This repository contains reusable Codex skills for project initialization and development environment bootstrap.

## Repository Rules

- Write all new documentation and code comments in English. Do not edit third-party, vendor, or legacy files only to change language.
- Keep skills modular and functional for basic use without requiring external context.
- Store each skill under its own directory with a `SKILL.md` entrypoint. Add `references/`, `assets/`, or implementation files only when the skill needs them.
- Use this priority order when rules conflict:
  1. Reproducibility: pin versions where practical and provide exact validation or run commands.
  2. Minimality: include only files, services, and dependencies required for the requested workflow.
  3. Production awareness: document production-relevant differences or provide optional production-like profiles instead of making local development heavy by default.
  4. Reference orientation: include a short inline summary for basic use, then link or point to detailed reusable policies and templates.
- Add a `scripts/` directory only when at least one script is invoked by CI, required to reproduce local build artifacts, or required by a stable generator. Document which condition requires each script.
- Never include actual credentials or secrets such as API keys, passwords, tokens, or private keys. Use explicit placeholders like `SECRET_API_KEY_PLACEHOLDER` and document how to inject real values through environment variables or a secret manager.
- If local testing requires secrets, provide a mock mode or fail with a clear message explaining the required environment variables.
- Name new container build files `Containerfile`. If existing tooling requires `Dockerfile`, keep compatibility with a symlink or a minimal forwarding file and document why.
- Name new Compose files `compose.yaml`. If existing tooling requires `docker-compose.yml`, keep compatibility with a symlink or a minimal forwarding file and document why.

## Available Skills

- `cloud-engineering-delivery`: Senior engineering workflow for cloud-native projects and features, including scope approval, architecture review, tests, QA, infrastructure, and commit or PR preparation.
- `devcontainer-project-bootstrap`: Step-by-step wizard for initializing software projects with standardized Docker Compose based Dev Container environments.
- `erpnext-agent`: Operates ERPNext or Frappe sites through user-provided URL and API credentials for querying records, inspecting DocTypes, mutating documents, and diagnosing API access.
- `prompt-refiner-agent`: Refines a raw user prompt into a safe, detailed English execution prompt, preserves the original response language requirement, prevents self-recursion, and routes execution to the appropriate skill after confirmation.
