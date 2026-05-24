---
name: erpnext-agent
description: Connect to and operate ERPNext or Frappe sites through user-provided URL and API credentials. Use when the user says they will give ERPNext tasks, wants to do work through ERPNext, starts an ongoing ERPNext work session, or asks Codex to inspect DocTypes, query records, create/update/delete documents, submit/cancel documents, call whitelisted Frappe methods, run ERPNext data cleanup or automation tasks, or diagnose ERPNext API access with an API key/secret, bearer token, or session supplied by the user. Continue using this skill for follow-up requests in the same conversation until the user says the ERPNext work is done.
---

# ERPNext Agent

## Overview

Use this skill to complete ERPNext/Frappe tasks through the HTTP API while keeping credentials out of files, logs, and final answers. Prefer the bundled `scripts/erpnext_api.py` helper for repeatable resource and method calls.

## Session Behavior

Start an ERPNext work session when the user explicitly says one of:

- "ERPNext uzerinden gorevler verecegim"
- "ERPNext'te isler yapacagiz"
- "ERPNext agent ile devam edelim"
- "Start ERPNext session"
- "Begin ERPNext work"

Also start a session when the user asks for a concrete ERPNext/Frappe operation, such as querying DocTypes, updating records, or diagnosing ERPNext API access. If the message only mentions ERPNext without a concrete task or session-start phrase, ask whether they want to start an ERPNext work session.

Keep using this skill for follow-up tasks in the same conversation, even when the follow-up message does not repeat "ERPNext".

End the ERPNext work session only when the user says "ERPNext isimiz bitti", "ERPNext oturumunu kapat", "End ERPNext session", or "Stop ERPNext work". After that, do not assume unrelated follow-up requests are ERPNext tasks unless the user starts a new ERPNext session.

Within an active session, remember non-secret connection context already provided in the conversation, such as site URL, company, target module, DocTypes, filters, and preferred output format. Do not persist, cache, log, echo, or restate secrets. Secrets may appear only in the single terminal command or API call they were provided for. If a required secret is missing or expired later, ask only for that secret again.

## Connection Intake

Ask only for missing connection details. Required fields by authentication method:

- API key/secret: Site URL, `ERPNEXT_API_KEY`, and `ERPNEXT_API_SECRET`.
- Bearer token: Site URL and `ERPNEXT_BEARER_TOKEN`.
- Existing session cookie: Site URL and `ERPNEXT_COOKIE`.

Do not ask for credentials that are not required by the chosen method. Also ask only for task-specific context that is missing:

- Target company, doctype, document name, filters, date range, or module context needed for the task.
- If the target is ambiguous, ask for the exact missing fields, such as doctype plus document name or filters. Example: `Update Sales Invoice ACC-SINV-2026-00001 with {"remarks":"..."}`.

Never ask the user to paste credentials into a file. Prefer environment variables for commands:

```bash
export ERPNEXT_URL="https://erp.example.com"
export ERPNEXT_API_KEY="..."
export ERPNEXT_API_SECRET="..."
```

Do not echo secrets, include them in final answers, commit them, or store them in skill files.

## Workflow

Always start by clarifying the business goal and classifying the task as read-only or mutating.

For read-only tasks:

1. Verify access with a harmless call such as `GET /api/method/frappe.auth.get_logged_user`.
2. If the target DocType, document, or filters are ambiguous, ask for the missing identifier before querying.
3. List with precise `fields`, `filters`, `limit`, and `order_by`.
4. Use pagination for bulk reads.
5. Report results in the requested format. If no format is requested, use a Markdown preview table.

For mutating tasks:

1. Verify access with a harmless call before any write.
2. Inspect metadata before writing unfamiliar documents: `GET /api/resource/DocType/{doctype}` or `frappe.desk.form.load.getdoctype`.
3. Resolve ambiguous targets before previewing changes.
4. Prepare a short preview of changed documents.
5. Get required confirmation before mutating production data unless the user already gave explicit approval for the exact operation.
6. Pass `--yes` to the helper only after approval.
7. Execute the smallest necessary operation.
8. Verify the result by reading the affected record or a summary query.
9. Report what changed, what was skipped, and any ERPNext validation errors.

For large results, if output exceeds 50 rows or about 10,000 characters, show only the first 10 rows as a Markdown preview table and ask whether the user wants the full output as JSON, YAML, or CSV.

## Safety Rules

- Treat ERPNext as production unless the user explicitly says it is a test site.
- Confirm before delete, submit, cancel, bulk update, stock, accounting, payroll, payment, or permission changes.
- For high-risk production operations, require the user to reply with `CONFIRM` plus the action summary, such as `CONFIRM delete 5 Sales Invoice records`.
- Treat arbitrary `call` operations as mutating unless the method is known read-only. Confirm before calling unknown whitelisted methods, even when the HTTP verb is `GET`.
- Prefer idempotent operations. Check whether the target document already exists before creating duplicates.
- Use pagination for bulk reads and bounded batches for bulk writes.
- Preserve ERPNext workflow semantics. For submittable documents, use submit/cancel APIs or whitelisted methods instead of directly setting `docstatus`.
- Respect permissions returned by ERPNext; do not suggest bypassing them unless the user is implementing an authorized server-side customization.

## Error Handling

- If verification fails, report `Authentication failed: <HTTP status and message>` or the exact connection error. Ask the user to re-provide the chosen auth credentials or confirm the site URL. Do not proceed until verification succeeds.
- If credentials are invalid or expired, say `Authentication failed: invalid or expired credentials` and ask for a valid API key/secret, bearer token, or session cookie. Do not echo the secret.
- For network errors, timeouts, or 429 responses, retry up to 2 times with exponential backoff. If retries fail, report the error and suggest checking connectivity or reducing request rate.
- For permission-denied responses, return the exact ERPNext error. If DocType metadata is available, mention relevant roles or permissions; otherwise ask whether the user will provide credentials with sufficient permission or make an authorized server-side change.
- For bulk writes, use bounded batches. If any item fails, stop further batches, report succeeded and failed items with exact errors, and ask whether to retry failed items, skip them, continue remaining items, or roll back successful changes if ERPNext supports it.

## Bundled Helper

Use `scripts/erpnext_api.py` for common API operations:

```bash
python3 scripts/erpnext_api.py whoami
python3 scripts/erpnext_api.py list Customer --fields '["name","customer_name"]' --limit 20
python3 scripts/erpnext_api.py get "Sales Invoice" ACC-SINV-2026-00001
python3 scripts/erpnext_api.py create Customer --data '{"customer_name":"Example","customer_type":"Company"}' --yes
python3 scripts/erpnext_api.py update Customer CUST-0001 --data '{"customer_group":"Commercial"}' --yes
python3 scripts/erpnext_api.py call frappe.client.get_value --data '{"doctype":"Company","fieldname":"name"}'
```

The helper prints Markdown tables by default. Use `--output json` only when the user asks for JSON or raw structured output.

The helper reads `ERPNEXT_URL` plus one of:

- `ERPNEXT_API_KEY` and `ERPNEXT_API_SECRET`, sent as `Authorization: token key:secret`.
- `ERPNEXT_BEARER_TOKEN`, sent as `Authorization: Bearer token`.
- `ERPNEXT_COOKIE`, sent as `Cookie`.

## References

- Read `references/frappe-rest-api.md` when endpoint shape, filtering syntax, authentication headers, or document workflow details matter.
