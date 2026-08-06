# Cloud-Native Defaults

Use only the parts required by the approved scope. Do not add unused infrastructure.

## New Projects

- Add a short development README and `.env.example` with placeholders.
- Centralize configuration and provide appropriate logging and structured errors.
- Add a health endpoint for a long-running service.
- Use an API contract such as OpenAPI for an HTTP API.
- Add a basic CI pipeline for relevant build and tests.
- Add container support only when deployment or local reproducibility needs it.
- Add `infra/compose/` or `infra/kubernetes/` only when that platform is in scope.
- Prefer existing framework support for metrics and tracing. Add dependencies or services only when required.
- Document migration and rollback behavior when schema migrations exist.

Prefer a small modular architecture that minimizes code, dependencies, operational surface, and future context size.

## High-Risk Review

For migrations, security boundaries, public contracts, distributed consistency, or production topology, check only the applicable items:

- rollback and recovery;
- backward compatibility and staged deployment;
- authentication, authorization, secrets, privacy, and permissions;
- data consistency and migration failure behavior;
- resource limits, timeouts, retries, health checks, and observability;
- production validation and the narrowest safe rollout.
