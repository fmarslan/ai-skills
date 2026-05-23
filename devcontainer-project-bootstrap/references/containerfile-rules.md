# Containerfile Rules

Use `Containerfile` for all container build files.

Rules:

- Never create files named `Dockerfile`.
- Prefer Microsoft Dev Container base images.
- Use official upstream images only when Microsoft does not provide an appropriate image.
- Never use `latest`.
- Keep development images minimal.
- Install only required development tooling.
- Use non-root users.
- Do not copy the full project into the Dev Container image; the workspace mount provides source code.
- Keep production `Containerfile` separate from `.devcontainer/Containerfile`.

Development image baseline:

- `.devcontainer/Containerfile` is the development image.
- Switch to `root`, create a deterministic `dev` user with a home directory, then switch to `USER dev`.
- If the base image already contains `dev`, reuse it and ensure `/home/dev` exists.
- Keep the username consistent with `devcontainer.json`, `.devcontainer/compose.yaml`, and mount targets.

Production image baseline:

- Root `Containerfile` may be generated when the deployment target needs a container image.
- It must be minimal, pinned, and aligned with the selected language/framework.
- It must not contain local-only development credentials or tools.
- Do not generate a root `Containerfile` when the deployment target is unknown or does not require a container image.
