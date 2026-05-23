# Development

This project is designed to run inside a Docker Compose based Dev Container.

## Prerequisites

- Docker or a compatible container runtime
- Visual Studio Code
- Dev Containers extension

## Start the Environment

Open the project in VS Code and choose `Dev Containers: Reopen in Container`.

The Dev Container mounts the project root as the workspace and stores local service data under `./data`.

Codex state is mounted from `./data/.codex` into the container user's home directory. Host secret and credential directories are not mounted automatically.

The Dev Container installs the reusable Codex skills repository into the container user's `.codex/skills/fmarslan-ai-skills` directory. On the host this persists under `./data/.codex/skills/fmarslan-ai-skills`.

## Bind Mount Permissions

On Linux, bind mount permissions are controlled by UID/GID. The username alone is not enough. During project generation, the bootstrap skill writes `.devcontainer/.env` with:

```text
DEV_USERNAME
DEV_GROUPNAME
DEV_UID
DEV_GID
```

On Linux and WSL Linux filesystems, the bootstrap skill also writes `remoteUser` in `.devcontainer/devcontainer.json` to the detected host username so VS Code, Compose, the Containerfile user, and the Codex home path remain consistent.

If `data/.codex` was created by Docker as root-owned, Codex may fail to start because it cannot write its config. Fix it from the project root:

```sh
sudo chown -R "$(id -u):$(id -g)" data/.codex
```

`data/.codex` should be writable by the development user. Service data directories under `data/<service-name>` may be owned by the service container's UID/GID. Do not blindly chown service data to the development user. For example, RabbitMQ data may need to match the RabbitMQ image user; changing it to the development user can prevent RabbitMQ from writing.

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
