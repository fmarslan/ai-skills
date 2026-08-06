# Error Handling

- Authentication failure: report the HTTP status and concise ERPNext message, then request only the selected credential type again.
- Network error, timeout, or HTTP 429: retry at most twice with exponential backoff, then stop and report the concise failure.
- Permission denial: return the ERPNext error and request authorized credentials or an authorized server-side change; never suggest bypassing permissions.
- Validation error: decode useful `_server_messages`, `exc_type`, or `exception` fields without dumping stack traces unless requested.
- Partial bulk failure: stop later batches, list concise succeeded and failed targets, and ask whether to retry, skip, continue, or use an available rollback.
