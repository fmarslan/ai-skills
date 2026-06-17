---
name: devcontainer-project-bootstrap
description: Use when initializing a new software project or standardizing an existing repository with a Docker Compose based Dev Container, Containerfile, VS Code configuration, documentation, environment files, local services, and deployment-ready structure. Acts as an interactive setup wizard that asks only critical architecture questions before generating files.
---

# Devcontainer Project Bootstrap

Use this skill as a step-by-step wizard for project initialization and development environment bootstrap.

## Boundary With Cloud Engineering Delivery

This skill owns only the project skeleton and local development environment baseline. It must not create real product behavior, domain architecture, API endpoints, business logic, production test suites, delivery task files, or agent orchestration prompts.

When the requested work is a cloud-native product/project delivery, use this skill only for bootstrap artifacts, then let `cloud-engineering-delivery` own product docs, real source code, API design, tests, QA, review, final reconciliation, commit, and PR flow.

Ownership:

- This skill owns `.devcontainer/`, Dev Container `Containerfile`, `.devcontainer/compose.yaml`, VS Code config, host user mapping, local service baseline, bootstrap templates, image/version pinning, and baseline folder creation.
- `cloud-engineering-delivery` owns `docs/tasks/`, `docs/ai/`, `codex/`, product/API/test/QA docs, real application code, delivery workflow, and commit/PR approval flow.
- Shared baseline files such as `docs/DEVELOPMENT.md`, `docs/ENVIRONMENT.md`, `docs/DEPLOYMENT.md`, `.env.example`, `.gitignore`, `infra/`, and root application `Containerfile` may be created as bootstrap placeholders/templates here, but final project-specific reconciliation belongs to `cloud-engineering-delivery`.

## Wizard Behavior

Ask one critical question at a time. Keep questions short and clear. Do not generate files until all critical decisions are complete.

Critical decisions:

- Programming language
- Framework
- Database
- Queue system
- Deployment target
- Kubernetes usage
- Monolith vs service architecture

Only ask the listed critical architecture questions. Do not ask about runtime minor versions, ports, editor tooling, file names, mounts, or implementation defaults unless the user explicitly requests those choices. Use the standards in `references/` automatically.

Before generation, briefly summarize the defaults that will be applied for images, ports, mounts, user mapping, and external repository installation. Apply those defaults unless the user asks for an override.

## Required Workflow

1. Inspect the target directory if it already exists. If it does not exist, create it before generation.
2. Ask missing critical architecture questions one at a time.
3. Read the relevant references for the chosen stack and requested services.
4. Verify current stable/LTS image versions from official sources before pinning any image tag. If online verification fails, use `references/version-policy.md` as the fallback, avoid unverifiable risky tags, and report that online verification was skipped.
5. Generate `.devcontainer/Containerfile` so the development user and group are always named `dev`, while their UID and GID match the detected host user when the host provides deterministic Unix UID/GID values. Do not create duplicate UID/GID entries.
6. Generate a clean project structure using `Containerfile` and `compose.yaml`.
7. During project generation, prepare host-side writable service data paths and write detected UID/GID values directly into generated Dev Container files with this skill's bundled `scripts/prepare-devcontainer-host.sh <project-root>` when the local host supports it. Do not generate `.env` files for Dev Container configuration, do not generate project-local host init scripts, and do not rely on Dev Container lifecycle scripts for host preparation.
8. If generation would overwrite existing files, list the conflicting files and ask the user whether to overwrite, skip, or preserve them with backups.
9. Generate meaningful starter content for all required files, but keep application source under `src/` as placeholder-only content.
10. Validate JSON and YAML syntax when tools are available.
11. Summarize generated files, assumptions, overrides, and any skipped online verification.

## Conflict Handling

Apply the higher-priority rule when instructions conflict:

1. Security standards
2. Dev Container and host preparation rules
3. Image and version policy
4. Project structure and naming standards
5. Stack-specific tooling defaults

If reference files disagree, prefer `references/version-policy.md` for image pins, `references/devcontainer-rules.md` for container behavior, and `references/env-standard.md` for application environment variables. Document any deviation in the summary.

## Mandatory Standards

- Use Docker Compose based Dev Container setup for every generated project.
- Use `.devcontainer/compose.yaml`, not `docker-compose.yml`.
- Use `Containerfile`, never `Dockerfile`.
- Use non-root container users.
- Use `dev` as the development username and group name in every generated Dev Container.
- Align the container `dev` user and `dev` group UID/GID with the host user during image build when deterministic host UID/GID values are available; otherwise default both to `1000`.
- Write UID/GID values directly into `.devcontainer/compose.yaml` build args and runtime `user`; do not rely on `.env` interpolation for Dev Container user mapping.
- Mount Codex automatically with a Docker named volume at `codex-home:/home/dev/.codex`.
- Install the reusable skill repository automatically into `/home/dev/.codex/skills/fmarslan-ai-skills` from `https://github.com/fmarslan/ai-skills`.
- Do not mount host secrets or credential directories automatically.
- Mount the project root as the workspace folder.
- Prefer Microsoft official Dev Container images that match the selected programming language and major version.
- If no Microsoft image matches the selected language and major version, use official upstream images.
- Never use `:latest` tags.
- Pin explicit stable/LTS versions.
- Avoid beta, rc, edge, preview, dev, canary, and nightly versions.
- Generate application environment templates as `.env.example`, never application `.env` files. Do not generate `.devcontainer/.env`; Dev Container user mapping must be encoded directly in generated Compose and Containerfile inputs.
- Persist all local service data under `./data/<service-name>`.
- Use official default ports unless the user explicitly overrides them.
- Use healthchecks when useful.
- Put all stack-specific code, package manifests, lockfiles, and build/test configuration under `src/`.
- Under `src/`, generate only the minimum language/framework placeholder required to validate the development environment. Do not generate real application implementation, real API endpoints, business logic, domain modules, or production test suites.
- Every placeholder source file must start with a comment stating that it is a bootstrap placeholder, that real application code is owned by `cloud-engineering-delivery`, and that the file can be replaced or removed during delivery.
- Keep the repository root limited to standardized bootstrap folders and repository-level docs/config.

## Reference Map

- Decisions and wizard policy: `references/decision-policy.md`
- Project layout: `references/project-structure-standard.md`
- Image and version policy: `references/version-policy.md`
- Dev Container rules: `references/devcontainer-rules.md`
- Containerfile rules: `references/containerfile-rules.md`
- VS Code rules: `references/vscode-rules.md`
- Tooling by stack: `references/tooling-policy.md`
- Predefined services: `references/default-services.md`
- Non-predefined services: `references/dynamic-service-policy.md`
- Environment files: `references/env-standard.md`
- Documentation: `references/docs-standard.md`
- Security: `references/security-standard.md`
- Deployment: `references/deployment-standard.md`

## Template Map

Use templates from `assets/templates/` as starting points:

- `docs/`: `DEVELOPMENT.md`, `CONTRIBUTING.md`, `DEPLOYMENT.md`, `ENVIRONMENT.md`
- `vscode/`: `extensions.json`, `tasks.json`, `launch.json`
- `devcontainer/`: `devcontainer.json`, `compose.yaml`, `Containerfile`
- `infra/`: `compose.yaml` and optional `kube/` manifests
- Root templates: `README.md`, `.env.example`, `.gitignore`, optional production `Containerfile`

Adapt every template to the selected language, framework, services, ports, and deployment target before writing it into a project.
