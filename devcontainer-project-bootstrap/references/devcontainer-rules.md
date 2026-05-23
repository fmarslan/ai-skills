# Dev Container Rules

Every generated project must use Docker Compose based Dev Containers.

Required files:

- `.devcontainer/devcontainer.json`
- `.devcontainer/compose.yaml`
- `.devcontainer/Containerfile`

Required behavior:

- `devcontainer.json` uses `dockerComposeFile`.
- The primary service is named `workspace`.
- The workspace folder is the mounted project root.
- The project root is mounted into the container as the workspace.
- The Codex directory is mounted as `../data/.codex:/home/dev/.codex:cached`.
- Host git credentials are mounted into the container.
- The container user is the non-root `dev` user.

`../data/.codex` is resolved from `.devcontainer/compose.yaml`, so it points to `project-root/data/.codex`.

## Container User Policy

Use `dev` as the deterministic development container user.

Generation rules:

1. Start from the selected pinned base image.
2. Switch to `root` in `.devcontainer/Containerfile`.
3. Create a `dev` user with a home directory if it does not already exist.
4. Grant passwordless sudo only when development tooling installation requires it.
5. Set `USER dev` at the end of `.devcontainer/Containerfile`.
6. Set `remoteUser` to `dev` in `devcontainer.json`.
7. Set Compose `user` to `dev`.
8. Mount all home-directory paths under `/home/dev`.

`scripts/detect-container-user.sh` is kept as a diagnostic helper for inspecting selected images, not as the primary generation path.

Recommended host git credential mounts:

- `~/.gitconfig:/home/dev/.gitconfig:ro`
- `~/.ssh:/home/dev/.ssh:ro`
- `~/.gnupg:/home/dev/.gnupg:ro`

Mount host git credential paths only when they exist. If a host credential path does not exist, omit that mount and document the manual setup path in `docs/DEVELOPMENT.md`.

Use `postCreateCommand` only for safe, repeatable dependency installation.
