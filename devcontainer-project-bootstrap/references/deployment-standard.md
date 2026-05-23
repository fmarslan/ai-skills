# Deployment Standard

Ask for deployment target before generating deployment-specific files.

Supported target examples:

- Container image only
- Kubernetes
- Docker Compose host
- Cloud platform
- Static hosting
- Serverless

Kubernetes:

- Generate `infra/kube/deployment.yaml`, `service.yaml`, `ingress.yaml`, and `configmap.yaml` only when Kubernetes usage is confirmed.
- Keep manifests minimal and production-aware.
- Do not generate real secrets.
- Use `ConfigMap` for non-secret configuration only.
- Document secret requirements without generating secret values.

Container deployment:

- Generate a root `Containerfile` when a production container image is required.
- Keep it separate from `.devcontainer/Containerfile`.
