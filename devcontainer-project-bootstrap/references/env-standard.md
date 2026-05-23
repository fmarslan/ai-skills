# Environment Standard

Generate `.env.example` only.

Rules:

- Never generate `.env`.
- Never generate real secrets.
- Use uppercase snake case variable names.
- Group variables by application and service.
- Use local-safe placeholder values such as `change-me-local-only`.
- Keep service variable names consistent with service names.
- Document every variable in `docs/ENVIRONMENT.md`.

Common variables:

```text
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=<framework-default-port>
```

Service examples:

```text
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=change-me-local-only
DATABASE_URL=postgresql://app:change-me-local-only@postgresql:5432/app
```
