# Frappe REST API Notes

Primary official docs:

- Frappe REST API: https://docs.frappe.io/framework/user/en/api/rest
- Frappe token authentication: https://docs.frappe.io/framework/user/en/guides/integration/rest_api/token_based_authentication

## Authentication

Token authentication uses:

```text
Authorization: token <api_key>:<api_secret>
```

OAuth or other bearer tokens use:

```text
Authorization: Bearer <access_token>
```

## Resources

Most DocTypes are available under:

```text
/api/resource/{doctype}
/api/resource/{doctype}/{name}
```

Common operations:

- `GET /api/resource/{doctype}` lists documents.
- `GET /api/resource/{doctype}/{name}` reads one document.
- `POST /api/resource/{doctype}` creates a document.
- `PUT /api/resource/{doctype}/{name}` updates a document.
- `DELETE /api/resource/{doctype}/{name}` deletes a document.

Useful query parameters for list calls:

- `fields`: JSON array, for example `["name","modified"]`.
- `filters`: JSON array or object, for example `[["status","=","Active"]]`.
- `or_filters`: JSON array for OR filtering.
- `limit_start`: integer offset.
- `limit_page_length` or `limit`: page size.
- `order_by`: SQL-style ordering allowed by Frappe, for example `modified desc`.

## Methods

Whitelisted Python methods can be called with:

```text
/api/method/{dotted.path.to.method}
```

Use `GET` for read-only method calls when supported and `POST` for writes or complex payloads. Frappe commits changes after successful POST requests handled by the framework.

Common method calls:

- `frappe.auth.get_logged_user`: validate current identity.
- `frappe.client.get`: get a document.
- `frappe.client.get_list`: list records.
- `frappe.client.get_value`: read selected values.
- `frappe.desk.form.load.getdoctype`: load DocType metadata for forms.
- `frappe.client.submit`: submit a submittable document.
- `frappe.client.cancel`: cancel a submitted document.

## Response Shape

Resource and method responses commonly wrap data in `data` or `message`. Preserve the full response during debugging, but summarize only the needed fields in user-facing answers.

## Error Handling

Frappe often returns structured JSON errors with fields such as `exc_type`, `exception`, `_server_messages`, or `exc`. Decode `_server_messages` when present and present the validation message without dumping stack traces unless the user needs debugging detail.
