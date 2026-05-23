# Project Structure Standard

Generate this baseline structure for new projects:

```text
project-root/
  .devcontainer/
    devcontainer.json
    compose.yaml
    Containerfile
  .vscode/
    extensions.json
    tasks.json
    launch.json
  data/
  docs/
    DEVELOPMENT.md
    CONTRIBUTING.md
    DEPLOYMENT.md
    ENVIRONMENT.md
  infra/
    compose.yaml
  src/
  README.md
  .env.example
  .gitignore
```

Conditional structure:

```text
project-root/
  Containerfile
  infra/
    kube/
      deployment.yaml
      service.yaml
      ingress.yaml
      configmap.yaml
```

Rules:

- Create `infra/kube/` only when Kubernetes usage is confirmed.
- Create the root `Containerfile` only when a production/runtime container image is required.
- Create `infra/compose.yaml` only when local application services are needed outside the Dev Container compose file.
- Create `data/` and service subfolders for persistent local service state.
- Put all project source code under `src/`.
- Do not place application source files in the repository root.
- Root files are reserved for repository metadata, environment examples, documentation entry points, container files, and tool configuration.
- Keep generated names lowercase and deterministic.
- Do not create unnecessary infrastructure.
- Do not add placeholder lorem ipsum content.

Examples:

- Go: `src/cmd/...`, `src/internal/...`, `src/pkg/...`
- Node.js: `src/index.ts`, `src/app/...`
- Python: `src/<package_name>/...`
- PHP: `src/...`
- Java: `src/main/...`, `src/test/...`
- .NET: `src/<ProjectName>/...`
