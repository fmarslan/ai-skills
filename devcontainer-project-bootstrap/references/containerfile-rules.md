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
- Define `ARG DEV_USERNAME=dev`, `ARG DEV_GROUPNAME=dev`, `ARG DEV_UID=1000`, and `ARG DEV_GID=1000`.
- Start as `root`.
- If a group already exists with `DEV_GID`, safely rename it to `DEV_GROUPNAME` unless that name is already used by another group.
- If `DEV_GROUPNAME` already exists with a different GID, fail clearly.
- If a user already exists with `DEV_UID`, safely rename it to `DEV_USERNAME` unless that name is already used by another user.
- If `DEV_USERNAME` already exists with a different UID, fail clearly.
- If UID/GID are free, create the group and user.
- Never create a second user or group with the same UID/GID.
- Move or create the home directory at `/home/${DEV_USERNAME}`.
- Create `/home/${DEV_USERNAME}/.codex`, `.cache`, and `.config`.
- Ensure `/home/${DEV_USERNAME}` is owned by `${DEV_UID}:${DEV_GID}`.
- Switch to `USER ${DEV_USERNAME}` at the end.
- In Microsoft Dev Container images where `vscode:1000:1000` exists, rename/reuse that account instead of creating another `1000:1000` account.
- Keep the username consistent with `devcontainer.json`, `.devcontainer/compose.yaml`, and mount targets.

Production image baseline:

- Root `Containerfile` may be generated when the deployment target needs a container image.
- It must be minimal, pinned, and aligned with the selected language/framework.
- It must not contain local-only development credentials or tools.
- Do not generate a root `Containerfile` when the deployment target is unknown or does not require a container image.
