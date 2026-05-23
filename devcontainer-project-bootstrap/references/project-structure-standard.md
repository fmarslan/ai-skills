# Project Structure Standard

Generate this baseline structure for new projects:

```text
project-root/
  .devcontainer/
    devcontainer.json
    compose.yaml
    Containerfile
    .env.example
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
- Put all stack-specific code, package manifests, lockfiles, and build/test configuration under `src/`.
- Do not place application source files, language package manifests, lockfiles, or stack-specific tool configuration in the repository root.
- Root files are reserved for the standardized bootstrap surface only: `.devcontainer/`, `.vscode/`, `data/`, `docs/`, `infra/`, `src/`, `README.md`, `.env.example`, `.gitignore`, and optional deployment `Containerfile`.
- Ignore generated `.devcontainer/.env`; commit `.devcontainer/.env.example` when useful.
- Do not generate project-local host init scripts under `.devcontainer/`. Host preparation is done by the skill during project creation.
- Keep generated names lowercase and deterministic.
- Do not create unnecessary infrastructure.
- Do not add placeholder lorem ipsum content.

Examples:

- Go: `src/go.mod`, `src/go.sum`, `src/cmd/...`, `src/internal/...`, `src/pkg/...`
- Node.js: `src/package.json`, `src/package-lock.json` or selected lockfile, `src/index.ts`, `src/app/...`
- Python: `src/pyproject.toml`, `src/poetry.lock`, `src/<package_name>/...`
- PHP: `src/composer.json`, `src/composer.lock`, `src/...`
- Java: `src/pom.xml` or `src/build.gradle`, `src/main/...`, `src/test/...`
- .NET: `src/*.sln`, `src/<ProjectName>/...`

Command generation must set working directories accordingly. For example, Go commands should run from `src/` when `src/go.mod` is generated.
