# Development

This project is designed to run inside a Docker Compose based Dev Container.

## Prerequisites

- Docker or a compatible container runtime
- Visual Studio Code
- Dev Containers extension

## Start the Environment

Open the project in VS Code and choose `Dev Containers: Reopen in Container`.

The Dev Container mounts the project root as the workspace and stores local service data under `./data`.

Codex state is stored in the Docker named volume `codex-home` and mounted into `/home/dev/.codex`. Host secret and credential directories are not mounted automatically.

The Dev Container installs the reusable Codex skills repository into `/home/dev/.codex/skills/fmarslan-ai-skills`.

## Bind Mount Permissions

On Linux, bind mount permissions are controlled by UID/GID. The username alone is not enough. During project generation, the bootstrap skill keeps the container username and group name as `dev`, then writes the detected host UID/GID directly into `.devcontainer/compose.yaml` build args and runtime `user`.

The generated project does not use `.devcontainer/.env` for Dev Container user mapping.

`remoteUser` remains `dev`, and `/home/dev` is the only generated development home path.

If the `codex-home` Docker volume has incorrect ownership, Codex may fail to start because it cannot write its config. Recreate the project Dev Container volume or inspect it with Docker volume tools.

Service data directories under `data/<service-name>` may be owned by the service container's UID/GID. Do not blindly chown service data to the development user. For example, RabbitMQ data may need to match the RabbitMQ image user; changing it to the development user can prevent RabbitMQ from writing.

## Host Notes

WSL projects should live under the WSL Linux filesystem, such as `~/projects/my-app`, not under `/mnt/c/Users/...`, to avoid permission and performance issues.

On macOS Docker Desktop, host file ownership does not behave exactly like native Linux bind mounts. The bootstrap prepares required directories but does not require Linux-style ownership changes.

On Windows without WSL, Linux UID/GID values are container-side values. The generated project uses default container values without running `chown`.

## Commands

Replace these commands with the selected stack commands during generation:

```sh
build-command
run-command
debug-command
```

## Debugging

Use the generated `.vscode/launch.json` configuration for the selected language and framework.
