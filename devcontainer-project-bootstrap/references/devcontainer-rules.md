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
- The Codex directory is mounted as a Docker named volume at `codex-home:/home/dev/.codex`.
- The reusable skill repository is installed into `/home/dev/.codex/skills/fmarslan-ai-skills`.
- Host secrets and credential directories are not mounted automatically.
- The container user is the non-root `dev` user produced from host-aligned UID/GID values.

Codex state must not be bind-mounted from the project tree. Use the `codex-home` named volume so Codex home data is persisted by Docker without creating `data/.codex` in the repository.

## Host-Aligned User Policy

Generated Dev Containers must use this identity:

- Username: `dev`
- Group name: `dev`

Generated Dev Containers must support these values through Compose build args and runtime `user`, with values written directly into generated files:

- `DEV_UID=1000`
- `DEV_GID=1000`

Linux and WSL Linux filesystem:

- Use the active host UID/GID values from `id -u` and `id -g`.
- Keep the container username and group name as `dev` even when the host username or group name differs.
- UID/GID bind mount permissions matter directly.

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

Do not generate `.devcontainer/.env` or require `.env` files for Dev Container configuration.

## Codex Skill Repository

Every generated project must make `https://github.com/fmarslan/ai-skills` available inside the Dev Container.

Rules:

- Use `/home/dev/.codex/skills/fmarslan-ai-skills` as the container path.
- Because `/home/dev/.codex` is mounted from the `codex-home` Docker named volume, the data is persisted by Docker rather than in `project-root/data/.codex`.
- Add a safe `postCreateCommand` that creates `/home/dev/.codex/skills` and then clones the repository if missing.
- If the repository already exists and is a git checkout, update it with `git pull --ff-only`.
- If the target path exists but is not a git checkout, leave it untouched and print a clear message.
- Do not require a GitHub token for this public repository.
- Do not store credentials inside the cloned skill repository.

## Container User Policy

Use host-aligned values where they are meaningful and deterministic defaults elsewhere.

Generation rules:

1. Start from the selected pinned base image.
2. Switch to `root` in `.devcontainer/Containerfile`.
3. Resolve or create the target group named `dev` from `DEV_GID`.
4. Resolve or create the target user named `dev` from `DEV_UID`.
5. Rename/reuse existing UID/GID entries instead of creating duplicates.
6. Grant passwordless sudo only when development tooling installation requires it.
7. Set `USER dev` at the end of `.devcontainer/Containerfile`.
8. Set Compose `user` to the generated UID/GID string, such as `"1000:1000"` or the detected host UID/GID.
9. Mount all home-directory paths under `/home/dev`.
10. Keep `remoteUser` literal as `"dev"`.

`scripts/detect-container-user.sh` is kept as a diagnostic helper for inspecting selected images, not as the primary generation path.

Do not add automatic mounts for host secrets or credential directories such as `~/.ssh`, `~/.gnupg`, `.git-credentials`, or private token files. If a project needs private repository access, document a manual, user-approved setup instead of generating secret mounts.

## Mount Source Preflight

Writable bind mount source directories for service data must exist before container startup.

- Create `data/<service-name>` before service containers start.
- On Linux and WSL Linux filesystems, user-writable mount sources must be owned by the active host UID/GID.
- Do not chown service-owned directories to the development user unless service image documentation requires that.
- RabbitMQ and similar service data directories may be owned by the service image UID/GID; this is normal.

Generated projects must include:

- No `.devcontainer/.env` or `.devcontainer/.env.example` for Dev Container configuration.
- `.gitignore` entries for local application `.env` files when application environment examples are generated.

Generated projects must not include project-local host init scripts. The skill performs host preparation during project creation using its own bundled helper, `scripts/prepare-devcontainer-host.sh`, or equivalent direct actions.

## Codex Writability Check

Add a safe post-create check for `/home/dev/.codex`.

- Verify that the directory exists.
- Verify that the active user can write to it.
- If not writable, print an actionable error:
  - Suggest removing and recreating the `codex-home` named volume if ownership was corrupted.
  - Windows/macOS: suggest checking Docker Desktop volume and runtime user configuration.

Use `postCreateCommand` only for safe, repeatable dependency installation and Codex skill repository bootstrap.
