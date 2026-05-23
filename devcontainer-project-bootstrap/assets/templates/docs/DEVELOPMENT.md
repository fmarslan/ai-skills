# Development

This project is designed to run inside a Docker Compose based Dev Container.

## Prerequisites

- Docker or a compatible container runtime
- Visual Studio Code
- Dev Containers extension

## Start the Environment

Open the project in VS Code and choose `Dev Containers: Reopen in Container`.

The Dev Container mounts the project root as the workspace and stores local service data under `./data`.

Codex state is mounted from `./data/.codex` into the container user's home directory. Host git credential mounts are added only for credential paths that exist on the host.

## Commands

Replace these commands with the selected stack commands during generation:

```sh
build-command
run-command
debug-command
```

## Debugging

Use the generated `.vscode/launch.json` configuration for the selected language and framework.
