# VS Code Rules

Generate:

- `.vscode/extensions.json`
- `.vscode/tasks.json`
- `.vscode/launch.json`

Always recommend:

- `openai.chatgpt`

Add stack-specific extensions:

- PHP: PHP language support, Composer, PHPUnit, Xdebug helpers
- Node.js: ESLint, Prettier, framework-specific extensions when known
- Python: Python, Pylance, pytest support
- Java: Extension Pack for Java, Maven or Gradle support
- .NET: C# Dev Kit, C# extensions
- Go: Go extension

Tasks and debug:

- Generate exactly the core task set first: `build`, `run`, and `debug`.
- Add `test`, `lint`, or `format` only when the generated project has reliable commands for them.
- Do not invent commands unsupported by the generated project.
- Use the current standard approach for the selected language and framework at generation time.
- Prefer package-manager or framework-native commands over custom shell wrappers.
- Use stable task labels: `build`, `run`, `debug`.
- Keep debug configurations minimal and executable.
- Generate `launch.json` configurations that match the selected stack and framework.
