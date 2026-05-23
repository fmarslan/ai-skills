# Dynamic Service Policy

If a requested service is not predefined:

- Use the official image.
- Use official default ports.
- Persist data under `./data/<service-name>`.
- Add the Compose service automatically.
- Add environment variables consistently to `.env.example`.
- Prefer stable tagged versions.
- Never use `latest`.
- Use healthchecks when possible.

Before adding the service:

- Verify the official image and stable tag from official sources.
- Verify the service's documented default ports.
- Check whether the service requires a named user, volume permissions, or initialization variables.
- Keep configuration minimal.
