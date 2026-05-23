# Tooling Policy

Install only tooling required for the selected stack.

## PHP

- composer
- phpunit
- xdebug

## Node.js

- npm
- pnpm
- yarn
- eslint
- prettier

## Python

- pip
- poetry
- pytest

## Java

- maven
- gradle

## .NET

- nuget
- dotnet-ef

## Go

- dlv

Rules:

- Prefer tools already included in the selected official image.
- Install missing tools in `.devcontainer/Containerfile`.
- Keep installation commands deterministic and pinned when the tool supports pinning.
- Do not install tooling for unselected stacks.
- Generate stack package manifests, lockfiles, and stack-specific tool configuration under `src/`, not the repository root.
- Set VS Code tasks, launch configurations, Dev Container commands, and documentation commands to use `src/` as the working directory when the stack manifest lives there.

Manifest placement:

- Go: `src/go.mod`, `src/go.sum`
- Node.js: `src/package.json`, selected lockfile under `src/`
- Python: `src/pyproject.toml`, lockfile under `src/`
- PHP: `src/composer.json`, `src/composer.lock`
- Java Maven: `src/pom.xml`
- Java Gradle: `src/build.gradle` or `src/build.gradle.kts`
- .NET: solution and project files under `src/`
