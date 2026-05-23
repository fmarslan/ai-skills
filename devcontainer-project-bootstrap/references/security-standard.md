# Security Standard

Security baseline:

- Never generate real secrets.
- Generate `.env.example`, not `.env`.
- Add `.env` to `.gitignore`.
- Use non-root container users.
- Do not mount host secrets or credential directories automatically.
- Do not mount `~/.ssh`, `~/.gnupg`, `.git-credentials`, token files, cloud credentials, or password manager files unless the user explicitly asks for that exact mount.
- Do not mount broad host directories.
- Do not expose extra service ports.
- Use official images and pinned stable tags.
- Avoid privileged containers.
- Keep local-only credentials clearly marked.
- Document secret handling in `docs/ENVIRONMENT.md`.

If a service requires credentials, use local placeholder values only.
