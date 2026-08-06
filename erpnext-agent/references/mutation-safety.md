# Mutation Safety

- Confirm before delete, submit, cancel, bulk update, stock, accounting, payroll, payment, or permission changes unless the user explicitly authorized that exact operation and target.
- For high-risk production operations, require `CONFIRM` plus a concise action summary.
- Treat unknown whitelisted methods as mutating even when called with `GET`.
- Inspect metadata before writing unfamiliar DocTypes.
- Preview affected document names and changed fields; never expose secrets or unnecessary personal data.
- Check for an existing record before creating a possible duplicate.
- Use bounded batches. Stop after a failed batch and do not continue without a safe recovery decision.
- Submit or cancel submittable documents through the supported workflow; do not set `docstatus` directly.
- Verify every completed write with a read or summary query.
