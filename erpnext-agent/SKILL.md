---
name: erpnext-agent
description: Connect to and operate ERPNext or Frappe sites through user-provided URL and API credentials. Use when the user starts ERPNext work or asks to inspect DocTypes, query records, mutate documents, submit or cancel documents, call whitelisted methods, automate data work, or diagnose API access. Continue for follow-up ERPNext requests until the user ends the session.
---

# ERPNext Agent

Complete ERPNext/Frappe work through the HTTP API with minimal conversation and without persisting or exposing credentials. Prefer `scripts/erpnext_api.py` for supported operations.

## Communication

- Ask only for missing connection data or identifiers required for the current action.
- Do not narrate routine API calls or repeat connection context.
- Preview only material writes; report results briefly.
- Show at most 10 rows by default for large results and offer JSON, YAML, or CSV only when useful.
- Provide detailed API output or diagnosis only when requested.

## Session And Credentials

- Start or continue the session for any concrete ERPNext/Frappe request.
- Retain non-secret context within the conversation; never persist, cache, log, echo, or restate secrets.
- End the session only when the user explicitly says ERPNext work is finished.
- Ask for the site URL plus exactly one authentication method: API key/secret, bearer token, or session cookie.
- Prefer environment variables: `ERPNEXT_URL` and either `ERPNEXT_API_KEY` plus `ERPNEXT_API_SECRET`, `ERPNEXT_BEARER_TOKEN`, or `ERPNEXT_COOKIE`.
- Never place credentials in repository files, generated artifacts, or final answers.

## Workflow

1. Classify the requested operation as read-only or mutating.
2. Verify access with `frappe.auth.get_logged_user` when connection validity is unknown.
3. Resolve only identifiers required for the operation.
4. For unfamiliar mutations, inspect DocType metadata first.
5. Execute the smallest precise query or mutation with explicit fields, filters, pagination, and bounded batches.
6. Verify writes by reading the affected record or a concise summary.
7. Report changed, skipped, and failed items without dumping unrelated response data.

For an exact mutation already authorized by the user's request, proceed without redundant confirmation unless the action is listed as high risk in the routed safety reference.

## Conditional Reference Routing

- Endpoint shape, filters, headers, response fields, or method semantics: `references/frappe-rest-api.md`.
- Create, update, delete, submit, cancel, bulk write, accounting, stock, payroll, payments, permissions, or unknown method calls: `references/mutation-safety.md`.
- Authentication failure, rate limiting, network failure, permission denial, validation errors, or partial bulk failure: `references/error-handling.md`.

Read only references that match the current operation.

## Helper

Use `scripts/erpnext_api.py` commands such as `whoami`, `list`, `get`, `create`, `update`, and `call`. Pass `--yes` only when the write is authorized. Use Markdown output by default and `--output json` only when raw structured output is requested or required for processing.

## Boundaries

- Treat the site as production unless explicitly identified as a test site.
- Prefer idempotent operations and preserve ERPNext workflow semantics.
- Respect ERPNext permissions; never bypass them.
- Pause on missing authorization for a high-risk write, ambiguous mutation targets, authentication failure, or an unsafe recovery choice.
