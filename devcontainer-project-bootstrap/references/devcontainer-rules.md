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
- The Codex directory is mounted as `../data/.codex:/home/${DEV_USERNAME:-dev}/.codex:cached`.
- The reusable skill repository is installed into `/home/${DEV_USERNAME:-dev}/.codex/skills/fmarslan-ai-skills`.
- Host secrets and credential directories are not mounted automatically.
- The container user is the non-root user produced from `DEV_USERNAME`, `DEV_GROUPNAME`, `DEV_UID`, and `DEV_GID`.

`../data/.codex` is resolved from `.devcontainer/compose.yaml`, so it points to `project-root/data/.codex`.

## Host-Aligned User Policy

Generated Dev Containers must support these values through `.devcontainer/.env`, Compose build args, and runtime environment:

- `DEV_USERNAME`
- `DEV_GROUPNAME`
- `DEV_UID`
- `DEV_GID`

Defaults:

- `DEV_USERNAME=dev`
- `DEV_GROUPNAME=dev`
- `DEV_UID=1000`
- `DEV_GID=1000`

Linux and WSL Linux filesystem:

- Use the active host user values from `id -un`, `id -gn`, `id -u`, and `id -g`.
- UID/GID bind mount permissions matter directly.
- `data/.codex` must be owned by the active host UID/GID.

WSL on `/mnt/c/...`:

- Warn that Windows filesystem mounts may have permission and performance issues.
- Recommend keeping repositories under the WSL Linux filesystem, such as `~/projects/my-app`.

macOS Docker Desktop:

- Do not assume Linux UID/GID semantics map directly to the host filesystem.
- Keep a non-root container user.
- Defaults `1000:1000` are acceptable unless the user overrides them.
- Do not require destructive host-side `chown`.

Windows without WSL:

- Do not assume `id`, `chown`, or Unix owner checks exist.
- Use default container values `dev:dev 1000:1000`.
- Verify writability from inside the container when needed.

## Codex Skill Repository

Every generated project must make `https://github.com/fmarslan/ai-skills` available inside the Dev Container.

Rules:

- Use `/home/${DEV_USERNAME}/.codex/skills/fmarslan-ai-skills` as the container path.
- Because `/home/${DEV_USERNAME}/.codex` is mounted from `project-root/data/.codex`, the host-side persisted path is `project-root/data/.codex/skills/fmarslan-ai-skills`.
- Add a safe `postCreateCommand` that creates `/home/${DEV_USERNAME}/.codex/skills` and then clones the repository if missing.
- If the repository already exists and is a git checkout, update it with `git pull --ff-only`.
- If the target path exists but is not a git checkout, leave it untouched and print a clear message.
- Do not require a GitHub token for this public repository.
- Do not store credentials inside the cloned skill repository.

## Container User Policy

Use host-aligned values where they are meaningful and deterministic defaults elsewhere.

Generation rules:

1. Start from the selected pinned base image.
2. Switch to `root` in `.devcontainer/Containerfile`.
3. Resolve or create the target group from `DEV_GROUPNAME` and `DEV_GID`.
4. Resolve or create the target user from `DEV_USERNAME` and `DEV_UID`.
5. Rename/reuse existing UID/GID entries instead of creating duplicates.
6. Grant passwordless sudo only when development tooling installation requires it.
7. Set `USER ${DEV_USERNAME}` at the end of `.devcontainer/Containerfile`.
8. Set Compose `user` to `"${DEV_UID:-1000}:${DEV_GID:-1000}"`.
9. Mount all home-directory paths under `/home/${DEV_USERNAME:-dev}`.
10. Keep `remoteUser` literal. During project generation, write the detected username when available; otherwise use the default `"dev"`.

`scripts/detect-container-user.sh` is kept as a diagnostic helper for inspecting selected images, not as the primary generation path.

Do not add automatic mounts for host secrets or credential directories such as `~/.ssh`, `~/.gnupg`, `.git-credentials`, or private token files. If a project needs private repository access, document a manual, user-approved setup instead of generating secret mounts.

## Mount Source Preflight

Writable bind mount source directories must exist before container startup.

- Create `data/.codex` before the Dev Container starts.
- Create `data/<service-name>` before service containers start.
- On Linux and WSL Linux filesystems, user-writable mount sources must be owned by the active host UID/GID.
- Do not chown service-owned directories to the development user unless service image documentation requires that.
- RabbitMQ and similar service data directories may be owned by the service image UID/GID; this is normal.

Generated projects must include:

- `.devcontainer/.env.example` with default values.
- `.gitignore` entry for `.devcontainer/.env`.

Generated projects must not include project-local host init scripts. The skill performs host preparation during project creation using its own bundled helper, `scripts/prepare-devcontainer-host.sh`, or equivalent direct actions.

## Codex Writability Check

Add a safe post-create check for `/home/${DEV_USERNAME}/.codex`.

- Verify that the directory exists.
- Verify that the active user can write to it.
- If not writable, print an actionable error:
  - Linux/WSL Linux filesystem: suggest `sudo chown -R "$DEV_UID:$DEV_GID" data/.codex`.
  - Windows/macOS: suggest checking Docker Desktop file sharing and mount path configuration.

Use `postCreateCommand` only for safe, repeatable dependency installation and Codex skill repository bootstrap.
