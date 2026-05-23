# Version Policy

Image versions must be verified at generation time from official sources.

Rules:

- Never use `:latest`.
- Prefer stable or LTS ecosystems.
- Avoid beta, rc, edge, preview, dev, canary, and nightly tags.
- Use Microsoft official Dev Container images whenever available.
- If no Microsoft image exists, use official upstream images.
- Pin explicit version tags in every generated image reference.
- Prefer Debian bookworm or current stable variants when the ecosystem supports them.
- Document selected major runtime versions in `docs/DEVELOPMENT.md`.

Verification guidance:

- Check official Microsoft Dev Container image tags for supported language stacks.
- Check official upstream registry tags when using upstream images.
- Check official language release pages for LTS/stable status when registry naming is ambiguous.
- Treat an unverifiable version as a blocker and ask the user whether to proceed with a clearly stated pinned fallback.

Preferred official sources:

- Microsoft Dev Containers: Microsoft Container Registry image pages and the official `devcontainers/images` metadata.
- Node.js: official Node.js release schedule and official Node image tags.
- Python: python.org downloads/releases and official Python image tags.
- PHP: php.net supported versions and official PHP image tags.
- Java: Microsoft Dev Container Java images first; otherwise Eclipse Temurin LTS images.
- .NET: Microsoft .NET support policy and official .NET SDK image tags.
- Go: go.dev releases and official Go image tags.

If official sources disagree, prefer the language runtime support policy over a registry tag that merely exists.
