# Decision Policy

The skill behaves as an interactive wizard.

## Critical Questions

Ask these only when the answer is missing:

- Programming language
- Framework
- Database
- Queue system
- Deployment target
- Kubernetes usage
- Monolith vs service architecture

Ask one question at a time and wait for the answer. Do not generate files before all critical decisions are known.

## Non-Critical Defaults

Use predefined standards automatically for:

- File and folder names
- Dev Container shape
- Compose file names
- Containerfile naming
- Service data paths
- VS Code file names
- Documentation file names
- Environment variable conventions
- Healthcheck inclusion
- Stable/LTS image preference

## Inference Rules

- Infer from existing repository files only when the signal is explicit.
- Never infer missing business or architecture decisions.
- If multiple frameworks are plausible, ask.
- If no service is requested or implied, generate no service.
- If Kubernetes usage is unknown, ask before generating `infra/kube/`.
