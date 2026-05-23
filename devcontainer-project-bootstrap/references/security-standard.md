# Security Standard

Security baseline:

- Never generate real secrets.
- Generate `.env.example`, not `.env`.
- Add `.env` to `.gitignore`.
- Use non-root container users.
- Mount host git credentials read-only.
- Do not mount broad host directories.
- Do not expose extra service ports.
- Use official images and pinned stable tags.
- Avoid privileged containers.
- Keep local-only credentials clearly marked.
- Document secret handling in `docs/ENVIRONMENT.md`.

If a service requires credentials, use local placeholder values only.
