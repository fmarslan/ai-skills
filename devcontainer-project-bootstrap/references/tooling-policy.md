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
