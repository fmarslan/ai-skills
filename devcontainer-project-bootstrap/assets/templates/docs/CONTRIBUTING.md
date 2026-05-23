# Contributing

## Workflow

1. Create a branch for each change.
2. Keep changes focused.
3. Run formatting, linting, and tests before opening a pull request.
4. Document new environment variables in `.env.example` and `docs/ENVIRONMENT.md`.

## Code Quality

- Keep dependencies minimal.
- Prefer explicit configuration over hidden local setup.
- Keep application source code under `src/`.
- Do not commit generated local data from `./data`.
- Do not commit real secrets.
