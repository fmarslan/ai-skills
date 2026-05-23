# Documentation Standard

Generate:

- `README.md`
- `docs/DEVELOPMENT.md`
- `docs/CONTRIBUTING.md`
- `docs/DEPLOYMENT.md`
- `docs/ENVIRONMENT.md`

Rules:

- All documentation must be in English.
- Use realistic project standards and explanations.
- Do not use lorem ipsum.
- Keep root `README.md` concise and practical.
- Document generated commands, ports, services, environment variables, and deployment assumptions.
- Document how to open the Dev Container and how local data is persisted.
- Document that stack-specific code, package manifests, lockfiles, and build/test configuration live under `src/`.
- Document that host-side Dev Container preparation is handled during project generation by the skill.
- Explain that Linux bind mount permissions depend on UID/GID, not only username.
- Explain that service data directories may be owned by service container users and should not always be chowned to the development user.

Required content:

- Development setup
- Build/run/test/debug commands
- Environment variables
- Local service ports
- Contribution workflow
- Deployment target and open decisions
- Security expectations for secrets
