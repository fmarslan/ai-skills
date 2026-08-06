---
name: cloud-engineering-delivery
description: "Deliver cloud-native projects and features with proportionate discovery, implementation, testing, and operational review. Use for containers, Kubernetes, Compose, APIs, services, CI/CD, observability, health checks, and cloud deployment."
---

# Cloud Engineering Delivery

Deliver working cloud-native changes with minimal code, minimal diff, minimal artifacts, and minimal conversation.

## Communication

- Work without narrating routine inspection, planning, edits, or successful commands.
- Update only for a material decision, risk, blocker, destructive action, or long-running operation.
- Ask one short grouped question only when a safe implementation cannot proceed without the answer.
- Finish with at most three short bullets: changed, validated, remaining risk. Omit empty bullets.
- Provide explanations, logs, or design rationale only when requested.

## Core Rules

- Prioritize safety and explicit constraints, existing architecture, the smallest complete change, relevant validation, then optional improvements.
- Inspect repository instructions, the affected entrypoint, its direct call path, nearby tests, and relevant configuration. Expand only when evidence requires it.
- First consider no code change, deletion, configuration, or reuse.
- Prefer the fewest edited lines and files. Reuse existing helpers, services, patterns, validation, logging, and configuration.
- Do not refactor, rename, reformat, or fix unrelated code.
- Do not add speculative flexibility, abstractions, fallbacks, feature flags, compatibility shims, dependencies, services, or infrastructure.
- Add an abstraction or dependency only when required by current behavior and simpler reuse is unavailable.
- Preserve unrelated user changes and never add real credentials.
- Do not create task files, agent comments, approval logs, `docs/tasks/`, `docs/ai/`, numbered prompts, or process diaries unless explicitly requested.
- Do not use sub-agents unless explicitly requested.

## Workflow

1. Determine whether the work is a new project or an existing-project change.
2. Trace only the affected behavior and existing tests before editing.
3. Read only the conditionally routed reference when applicable.
4. Implement the smallest coherent change that fully satisfies the request.
5. Update documentation only when interfaces, configuration, deployment, operation, or user behavior changed.
6. Run the narrowest sufficient validation: focused tests first, then only relevant integration, end-to-end, security, lint, type, build, or manifest checks.
7. Stop testing after sufficient evidence; do not run broad suites for ceremony.
8. Inspect the final diff once for correctness, scope, secrets, compatibility, migration safety, performance, rollback needs, coverage, and unrelated changes.
9. Report according to the Communication section.

For documentation-only or declarative changes, direct validation may replace unit tests. If a required check cannot run, report only the attempted command and concise reason.

## Decisions And Risk

Proceed without redundant approval for reversible work clearly authorized by the request.

Require explicit approval only before an unauthorized destructive or difficult-to-reverse data change, paid external service, material runtime-infrastructure change, authentication/authorization change, public compatibility break, production deployment strategy change, commit, push, or pull request.

For new dependencies, verify necessity, official source, version, relevant license, and available ecosystem security checks. State unavailable verification briefly instead of creating a tracking artifact.

## Conditional Reference Routing

Read `references/cloud-native-defaults.md` only for:

- new projects;
- infrastructure or production-topology work;
- schema migrations;
- public-contract or security-boundary changes;
- distributed-consistency risks.

Do not read it for ordinary feature work.

## Existing Projects

- Follow existing style, architecture, tests, health checks, observability, CI/CD, environment, API, and deployment patterns only where relevant.
- Do not block the requested feature because unrelated cloud-native standards are missing.
- Mention an important missing standard briefly; implement it only when required for safe delivery or explicitly requested.

## Escalation

Pause only for a material missing decision, unavailable required credential or service, unsafe operation, or unresolved repeated failure. Request the smallest input needed to continue.
