---
name: cloud-engineering-delivery
description: "Use when starting a new cloud-native software project or adding a feature to an existing cloud-native project with senior engineering controls: documentation discovery, scope approval, ordered Codex prompts, product tasks, architecture review, tests, implementation, QA, cloud-native infrastructure, final reconciliation, and developer-approved commit or PR. Trigger for projects involving containers, Kubernetes, Compose, APIs, services, distributed systems, CI/CD, observability, health checks, cloud deployment, or cloud-native application standards."
---

# Cloud Engineering Delivery

Use this skill to deliver a new cloud-native project or an existing cloud-native project feature with disciplined engineering quality, explicit approvals, complete tests, cloud-native operational standards, and traceable documentation.

For user-facing replies, use at most 2 sentences and 200 characters unless the user asks for detail. Internal artifacts such as docs, task files, and Codex prompts must be complete and explicit.

## Precedence

When rules conflict, apply this order:

1. Safety, security, privacy, data integrity, and legal/compliance constraints.
2. Explicit developer approvals and scope boundaries.
3. Existing project architecture, standards, and compatibility.
4. Minimal-change policy.
5. New-project cloud-native defaults.
6. Optional improvements.

## Operating Rules

- Do not silently infer critical product behavior, data rules, security behavior, deployment behavior, or compatibility decisions.
- Ask concise questions when a missing decision can change scope, behavior, risk, or architecture.
- Get initial developer scope approval before implementation starts. Approval must be an explicit chat message or project comment containing the approver, date or timestamp, and approved scope; record it under `Developer Approvals` in the task file.
- If approval is not received, pause work and record the pending approval in the task file. Do not proceed on risk-bearing or mutating work without explicit approval or a named delegated approver.
- After approval, continue within the approved scope without repeated confirmations.
- Stop and ask again if new information introduces risk, permanent changes, new dependencies, migrations, security/auth changes, API contract changes, deployment changes, or product behavior changes.
- If a risk appears after tasks have started, pause implementation, reconcile the relevant docs and task files, then ask the developer for a decision.
- Treat existing files as owned by the project. Inspect before editing and preserve unrelated user changes.
- Prefer the smallest change that satisfies the requirement.
- Optional improvements are allowed only when they do not add dependencies, do not change APIs or behavior, do not alter deployment/runtime assumptions, and are limited to a small local cleanup such as validation, naming, typing, or error handling in the touched area.
- Use existing project helpers, base classes, shared services, configuration, logging, validation, and test utilities before adding new code.
- Add a new abstraction only when it removes real complexity or matches an established local pattern.
- New dependencies require developer approval, package name/version/license, registry verification from the official registry such as npm, PyPI, Maven Central, NuGet, crates.io, Go modules, or the vendor site, and a security check from OSV, Snyk, GitHub Advisories, npm audit, pip-audit, or the ecosystem's standard scanner.
- If online verification cannot run, record the missing check and require explicit developer risk acceptance before adding the dependency.
- If required tooling is unavailable or fails, capture the error output, try the smallest reproducible local command, list missing environment variables/services, record the gap in the task file, and pause unless the developer explicitly waives the requirement.
- Commit and PR creation are allowed only after explicit developer approval.

## Start Workflow

First determine whether the request is cloud-native or cloud-adjacent. Use this skill for work involving containers, Kubernetes, Compose, APIs, services, distributed systems, CI/CD, observability, health checks, cloud deployment, or cloud-native application standards.

Then determine whether the request is:

- **New Project Flow**: creating a new project or service.
- **Existing Project Feature Flow**: adding or changing behavior in an existing project.

If the user does not state the target directory, ask which folder to work in. For monorepos or multi-repo work, ask whether the change is scoped to one folder/repo or crosses repos; if cross-repo, require the affected repos and owners before planning.

If the user does not state whether the work must be fully integrated with existing code or isolated as a limited external addition, ask before planning implementation.

Accept only these exact, case-insensitive trigger words as permission to execute prepared prompts, subject to all approval rules: "start", "create", "run", "begin", "tekbasla", "olustur", "calistir".

## Documentation Discovery

Before planning code:

1. Search the project for `docs/`, architecture notes, deployment notes, API documentation, README files, ADRs, environment docs, CI/CD docs, and development guides.
2. Read the relevant documents and inspect the code structure needed to validate them.
3. Identify gaps, contradictions, outdated information, and open decisions.
4. Actively close documentation gaps by asking concise developer questions or preparing new documentation.
5. Do not modify or rewrite existing documentation without explicit developer approval. Creating new docs is allowed when it does not overwrite existing files.

If no useful documentation exists, ask short, strict questions until the goal, scope, audience, constraints, integrations, data rules, deployment expectations, and acceptance criteria are explicit. Do not leave ambiguous behavior for implementation-time inference.

If documentation exists, ask the developer how to handle updates before mutating docs:

- Add new docs beside the existing set.
- Add an improved version in a new subfolder.
- Reconcile and update the existing docs.
- Add only missing docs required for this work.

Documentation defaults to English. If the developer requests another language, produce all new docs in that language and add a short English summary. Record the chosen language in the task file.

## Artifact Layout

Use these paths at the project root:

- `docs/`: product, architecture, API, development, deployment, environment, and delivery documentation.
- `docs/tasks/`: active task Markdown files.
- `docs/tasks/completed/`: completed task records.
- `docs/ai/`: project-specific AI context, including API summaries, helper catalogs, shared classes, central services, development rules, and documentation update rules.
- `codex/`: numbered execution prompts only.

Do not use `codex/completed/`. Completed task records move to `docs/tasks/completed/`.

Prompt files in `codex/` must be numbered in execution order, for example:

```text
codex/001-product-discovery.md
codex/002-architect-review.md
codex/003-test-design.md
codex/004-implementation.md
codex/005-qa.md
codex/006-final-reconciliation.md
```

Each prompt must instruct the executing agent to follow this skill's quality, approval, testing, review, and documentation rules.

## Required Task Template

Every task in `docs/tasks/` must be a small feature slice and include these sections. A small feature slice is one endpoint, one UI component, one background job, one integration point, or one cohesive behavior with its related tests; if it is likely to exceed about 300 lines of production code, split it.

```markdown
# TASK-ID: Short Title

## Status
Planned | In Progress | Blocked | In Review | QA | Completed

## Requirement Link
Link to product requirement, issue, API contract, or source document.

## Scope
What is included and what is explicitly excluded.

## Acceptance Criteria
Measurable behavior that must be true.

## Definition of Done
- Code complete.
- Unit tests written and passing.
- Integration tests written and passing.
- E2E tests written and passing when applicable.
- Security tests/checks written or executed.
- Documentation updated.
- Architect review passed.
- QA passed.

## Risk Analysis
Data loss, security, privacy, backward compatibility, performance, deployment, and operational risks.

## Rollback Plan
How to disable, revert, migrate back, or recover safely.

## Traceability
Requirement -> tests -> code changes -> QA evidence.

## Assumptions
Explicit assumptions. Mark critical assumptions as requiring developer approval.

## Developer Approvals
Approver, timestamp, decision, approved scope, and any conditions.

## Implementation Notes
What changed and why.

## Test Results
Commands, results, failures, skipped checks, and missing tools.

## QA Result
Acceptance validation and defects.

## Architect Review Result
Test review, source review, security/privacy, performance, compatibility, and final decision.
```

Each completed task must include a concise explanation of the work performed before it is moved to `docs/tasks/completed/`.

## Agent Sequence

Use real sub-agents when available. If sub-agents are not available, generate the numbered prompt files in `codex/`; for each file, perform that step locally and record results in the task file before moving to the next file.

The required sequence is:

1. **Product Developer**
   - Entry: documentation discovery is complete and missing product decisions are resolved or marked as blocked.
   - Actions: read existing docs and user intent; create new product docs when needed; modify existing product docs only with explicit approval; split work into small feature-slice tasks.
   - Exit artifact: task files in `docs/tasks/` with acceptance criteria, assumptions, and initial Definition of Done.
2. **Architect**
   - Entry: task files exist.
   - Actions: review product scope, architecture fit, risk, rollback, compatibility, task boundaries, and required approvals.
   - Exit artifact: architect approval in each task file, or a blocked status with required developer decisions.
3. **Test Agent**
   - Entry: architect has approved task scope.
   - Actions: write unit, integration, e2e, and security tests; ensure every feature has a unit test that can be used as the debug entrypoint.
   - Exit artifact: tests plus documented commands in the task file, or documented evidence for any impossible test level.
4. **Architect**
   - Entry: tests are written or explicitly marked impossible.
   - Actions: review tests before source implementation and reject missing, weak, non-deterministic, or non-scenario-covering tests.
   - Exit artifact: test review approval in the task file.
5. **Developer**
   - Entry: test review passed.
   - Actions: implement the smallest approved change using existing helpers, shared classes, central services, and project conventions.
   - Exit artifact: implementation notes and changed-file summary in the task file; documentation updates prepared or applied according to approval rules.
6. **Architect**
   - Entry: implementation is complete.
   - Actions: review source code for correctness, maintainability, security/privacy, performance, compatibility, and minimal-change discipline.
   - Exit artifact: source review approval or defects routed to Developer/Product Developer.
7. **QA**
   - Entry: source review passed.
   - Actions: run the approved test suite and validate acceptance criteria.
   - Exit artifact: QA result with commands, logs summary, pass/fail status, and defects if any.
8. **Architect**
   - Entry: QA passed.
   - Actions: confirm the task meets scope, tests, docs, and risk requirements.
   - Exit artifact: final task approval or loop restart reason.
9. **Final Reconciliation**
   - Entry: architect final approval exists.
   - Actions: update final docs, task status, test evidence, AI context, and proposed commit message.
   - Exit artifact: completed task moved to `docs/tasks/completed/`; continue until no incomplete task remains.

## New Project Flow

For a new project, establish the engineering baseline before feature implementation:

- Create `docs/` with product, architecture, API, development, deployment, environment, testing, and operations documentation.
- Create `docs/ai/` with project-specific AI context:
  - API docs and use cases.
  - Central helpers, shared classes, base services, and common patterns.
  - Environment, logging, testing, debugging, and deployment rules.
  - A rule that any change to APIs, helpers, shared structures, env, logging, or architecture must update docs.
- Use small, independent, modular architecture to minimize future AI context size.
- Create detailed API documentation with descriptions, examples, and use cases.
- Use OpenAPI/Swagger by default unless the developer opts out.
- Add a health endpoint.
- Add a development README.
- Add centralized environment management. Default runtime secrets to `.env` and committed examples to `.env.example`.
- Add logging configuration with format and levels.
- Add metrics, tracing, and structured error responses by default using existing framework/project capabilities when possible. If new dependencies, services, or runtime infrastructure are needed, get explicit developer approval first.
- Add basic CI pipeline.
- Add container support so the project can run inside a container.
- Add `infra/` at the project root with Compose and Kubernetes assets:
  - `infra/compose/` for local development/debug services.
  - `infra/kubernetes/` for cloud-native deployment manifests, Helm, or Kustomize.
- Include debug/development dependencies as in-memory components by default, or Compose services when the developer requests them.
- Follow cloud-native application rules.
- Follow global language/framework formatting, syntax, and style standards unless the developer chooses otherwise.
- Ask at the start how DB migrations should handle rollback and tests if migrations are present.

## Existing Project Feature Flow

For an existing project:

- Inspect current docs, source layout, build/test tooling, CI/CD, deployment, environment, API docs, logging, observability, health checks, and shared architecture.
- Understand the existing project before proposing implementation.
- Ask whether the feature must be fully integrated with existing architecture or kept as a limited external addition.
- Follow existing code style, formatting, naming, test patterns, architecture, and deployment conventions.
- Reuse existing helpers, shared classes, central services, config, logging, env management, API docs, health endpoints, and README patterns.
- Do not add new dependencies, abstractions, services, or infrastructure when current project structures can solve the task.
- Evaluate the project against the New Project Flow standards.
- Do not block the requested feature solely to create missing standards unless the missing standard is required for safe delivery.
- At the end, briefly report missing standards.
- Create missing standards only if the developer requests and approves that follow-up work.

## Testing And Debugging

- Unit tests are mandatory for every feature.
- Integration, e2e, and security tests are mandatory unless technically impossible or irrelevant for the project type.
- Missing test levels must be documented with a reason and architect approval.
- Every feature must have a unit test that can serve as the debug entrypoint.
- Debug tasks must start from the related unit test whenever possible.
- Configure language/framework-specific test runner, IDE, or debugger settings needed to debug from that unit test.
- QA must run the relevant tests and record commands and results in the task file.
- If any test or CI check fails, update the task file with failure logs, return the task to Developer for fixes, and do not create a commit or PR until tests pass and Architect re-approves.
- If user input for required fields is invalid or incomplete, list the missing fields by name, provide example values, and do not guess.

## Reviews And Quality Gates

The Architect review must cover:

- Product behavior and acceptance criteria.
- Architecture fit.
- Minimal change policy.
- Reuse of existing central structures.
- Data loss risk.
- Security and privacy, including auth, authorization, secrets, PII, logs, and permission boundaries.
- Performance, including database queries, cache use, payload size, background jobs, and frontend rendering when relevant.
- Backward compatibility, API contracts, migrations, config, CI/CD, and deployment.
- Rollback feasibility.
- Test completeness and determinism.
- Documentation and AI context updates.

Optional improvements may be implemented only when they satisfy the Operating Rules threshold for optional improvements. If an improvement changes behavior, scope, API, data shape, security posture, deployment, or operational assumptions, ask the developer first.

## Final Reconciliation

Before completion:

1. Ensure all task files are updated and completed tasks are under `docs/tasks/completed/`.
2. Ensure docs reflect final behavior, APIs, env, logging, observability, infrastructure, and development/debug instructions.
3. Ensure `docs/ai/` reflects current APIs, helpers, shared classes, central services, and rules.
4. Ensure all required test results are recorded.
5. Ensure skipped checks and missing tools are explicitly documented.
6. Prepare a commit message.
7. Ask the developer for commit approval.
8. If approved, commit the changes.
9. Ask the developer whether to prepare or open a PR.
