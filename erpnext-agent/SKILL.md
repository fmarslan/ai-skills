---
name: erpnext-agent
description: Connect to and operate ERPNext or Frappe sites through user-provided URL and API credentials. Use when Codex needs to inspect DocTypes, query records, create/update/delete documents, submit/cancel documents, call whitelisted Frappe methods, run ERPNext data cleanup or automation tasks, or diagnose ERPNext API access with an API key/secret, bearer token, or session supplied by the user.
---

# ERPNext Agent

## Overview

Use this skill to complete ERPNext/Frappe tasks through the HTTP API while keeping credentials out of files, logs, and final answers. Prefer the bundled `scripts/erpnext_api.py` helper for repeatable resource and method calls.

## Connection Intake

Ask only for missing connection details:

- Site URL, for example `https://erp.example.com`.
- Authentication method: API key/secret, bearer token, or existing session cookie.
- Required values for the chosen method.
- Target company, doctype, document name, filters, date range, or module context needed for the task.

Never ask the user to paste credentials into a file. Prefer environment variables for commands:

```bash
export ERPNEXT_URL="https://erp.example.com"
export ERPNEXT_API_KEY="..."
export ERPNEXT_API_SECRET="..."
```

Do not echo secrets, include them in final answers, commit them, or store them in skill files.

## Workflow

1. Clarify the business goal and identify whether the task is read-only or mutating.
2. Verify access with a harmless call such as `GET /api/method/frappe.auth.get_logged_user`.
3. Inspect metadata before writing unfamiliar documents: `GET /api/resource/DocType/{doctype}` or `frappe.desk.form.load.getdoctype`.
4. For reads, list with precise `fields`, `filters`, `limit`, and `order_by`.
5. For writes, prepare a short preview of changed documents and confirm with the user before mutating production data unless the user already gave explicit approval.
6. Execute the smallest necessary operation.
7. Verify the result by reading the affected record or a summary query.
8. Report what changed, what was skipped, and any ERPNext validation errors.

## Safety Rules

- Treat ERPNext as production unless the user explicitly says it is a test site.
- Confirm before delete, submit, cancel, bulk update, stock, accounting, payroll, payment, or permission changes.
- Prefer idempotent operations. Check whether the target document already exists before creating duplicates.
- Use pagination for bulk reads and bounded batches for bulk writes.
- Preserve ERPNext workflow semantics. For submittable documents, use submit/cancel APIs or whitelisted methods instead of directly setting `docstatus`.
- Respect permissions returned by ERPNext; do not suggest bypassing them unless the user is implementing an authorized server-side customization.

## Bundled Helper

Use `scripts/erpnext_api.py` for common API operations:

```bash
python3 scripts/erpnext_api.py whoami
python3 scripts/erpnext_api.py list Customer --fields '["name","customer_name"]' --limit 20
python3 scripts/erpnext_api.py get "Sales Invoice" ACC-SINV-2026-00001
python3 scripts/erpnext_api.py create Customer --data '{"customer_name":"Example","customer_type":"Company"}'
python3 scripts/erpnext_api.py update Customer CUST-0001 --data '{"customer_group":"Commercial"}'
python3 scripts/erpnext_api.py call frappe.client.get_value --data '{"doctype":"Company","fieldname":"name"}'
```

The helper reads `ERPNEXT_URL` plus one of:

- `ERPNEXT_API_KEY` and `ERPNEXT_API_SECRET`, sent as `Authorization: token key:secret`.
- `ERPNEXT_BEARER_TOKEN`, sent as `Authorization: Bearer token`.
- `ERPNEXT_COOKIE`, sent as `Cookie`.

## References

- Read `references/frappe-rest-api.md` when endpoint shape, filtering syntax, authentication headers, or document workflow details matter.
