---
name: devcontainer-project-bootstrap
description: Use when initializing a new software project or standardizing an existing repository with a Docker Compose based Dev Container, Containerfile, VS Code configuration, documentation, environment files, local services, and deployment-ready structure. Acts as an interactive setup wizard that asks only critical architecture questions before generating files.
---

# Devcontainer Project Bootstrap

Create only the project skeleton and local development baseline. Do not create product behavior, real APIs, business logic, production tests, task files, or delivery orchestration.

## Communication

- Work with minimal narration.
- Ask only for missing decisions that materially affect generated files.
- Before writing, summarize only material inferred choices and file conflicts.
- Finish with at most three short bullets: generated, validated, remaining issue.
- Give detailed explanations only when requested.

## Core Rules

- Inspect the target before editing and preserve unrelated content.
- Generate the least code and fewest files that satisfy the requested bootstrap.
- Use Docker Compose Dev Containers with `.devcontainer/compose.yaml` and `.devcontainer/Containerfile`.
- Use a non-root `dev` user and align UID/GID with deterministic host values; otherwise use `1000:1000`.
- Write UID/GID directly into generated build args and runtime user settings. Do not generate `.devcontainer/.env`.
- Mount the project as the workspace and Codex through `codex-home:/home/dev/.codex`; never mount host credentials automatically.
- Install `https://github.com/fmarslan/ai-skills` safely into `/home/dev/.codex/skills/fmarslan-ai-skills`.
- Use official pinned stable/LTS images; never use `latest`, preview, RC, nightly, or unverified tags.
- Put stack code and manifests under `src/`; generate only the smallest runnable bootstrap placeholder.
- Start every placeholder source file with a comment stating that cloud engineering delivery owns real application code and may replace it.
- Generate `.env.example` placeholders, never real secrets or application `.env` files.
- Persist requested local service data under `data/<service-name>` and add health checks when useful.
- Use `Containerfile` and `compose.yaml` names. Add compatibility names only when existing tooling requires them.
- Do not add unrequested services, infrastructure, tooling, documentation, or deployment files.

## Workflow

1. Inspect repository instructions and the target directory.
2. Infer language, framework, services, deployment, and architecture only from clear existing evidence; ask one short question for each material unresolved decision.
3. Read only the references selected by the routing table below.
4. Verify image/runtime versions from official sources when generating or changing image tags.
5. Reuse templates from `assets/templates/` only for requested outputs and remove irrelevant sections.
6. Use `scripts/prepare-devcontainer-host.sh <project-root>` when host-side writable paths or deterministic UID/GID preparation is needed.
7. If existing files would be overwritten, list only those files and ask whether to preserve, skip, or overwrite them.
8. Generate the minimum coherent file set.
9. Validate changed JSON, YAML, Compose, and relevant build configuration with the narrowest available checks.

## Conditional Reference Routing

Read no reference merely because it exists.

- Missing architecture decisions: `references/decision-policy.md`.
- New project layout or repository standardization: `references/project-structure-standard.md`.
- Image selection or tag changes: `references/version-policy.md`.
- Dev Container generation or modification: `references/devcontainer-rules.md` and `references/containerfile-rules.md`.
- VS Code files: `references/vscode-rules.md`.
- Stack package manifests or development tools: `references/tooling-policy.md`.
- Known local service: `references/default-services.md`.
- Service absent from the known-service table: `references/dynamic-service-policy.md`.
- Application environment variables: `references/env-standard.md`.
- Documentation requested or operational commands changed: `references/docs-standard.md`.
- Secret, credential, permission, mount, or exposed-port concerns: `references/security-standard.md`.
- Runtime container, Kubernetes, or production deployment files: `references/deployment-standard.md`.

When references conflict, apply security first, then Dev Container behavior, version policy, project structure, and stack defaults.

## Boundaries

- Use `cloud-engineering-delivery` for real application code and product delivery after bootstrap.
- Pause only for an unsafe overwrite, a material unresolved choice, or an unavailable required dependency.
- Do not create process documentation to record decisions or validation.
