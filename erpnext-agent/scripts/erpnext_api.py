#!/usr/bin/env python3
"""Small ERPNext/Frappe REST helper for Codex skills."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


MUTATING_COMMANDS = {"create", "update", "delete"}
READ_ONLY_METHODS = {
    "frappe.auth.get_logged_user",
    "frappe.client.get",
    "frappe.client.get_count",
    "frappe.client.get_list",
    "frappe.client.get_value",
    "frappe.desk.form.load.getdoctype",
}


def env(name: str) -> str | None:
    value = os.environ.get(name)
    return value if value else None


def require_env(name: str) -> str:
    value = env(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def auth_headers() -> dict[str, str]:
    headers = {"Accept": "application/json"}
    api_key = env("ERPNEXT_API_KEY")
    api_secret = env("ERPNEXT_API_SECRET")
    bearer = env("ERPNEXT_BEARER_TOKEN")
    cookie = env("ERPNEXT_COOKIE")

    if api_key and api_secret:
        headers["Authorization"] = f"token {api_key}:{api_secret}"
    elif bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    elif cookie:
        headers["Cookie"] = cookie
    else:
        raise SystemExit(
            "Set ERPNEXT_API_KEY and ERPNEXT_API_SECRET, or ERPNEXT_BEARER_TOKEN, or ERPNEXT_COOKIE"
        )
    return headers


def parse_json_arg(raw: str | None, default):
    if raw is None:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}") from exc


def request(method: str, path: str, *, query: dict | None = None, data=None):
    base_url = require_env("ERPNEXT_URL").rstrip("/")
    url = f"{base_url}{path}"
    if query:
        encoded = {
            key: json.dumps(value) if isinstance(value, (list, dict)) else value
            for key, value in query.items()
            if value is not None
        }
        url = f"{url}?{urllib.parse.urlencode(encoded)}"

    body = None
    headers = auth_headers()
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            parsed = payload
        print(json.dumps({"status": exc.code, "error": parsed}, indent=2, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1) from exc


def print_json(value) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def unwrap_records(value):
    if isinstance(value, dict):
        for key in ("data", "message"):
            inner = value.get(key)
            if isinstance(inner, list):
                return inner
            if isinstance(inner, dict):
                return [inner]
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    return []


def markdown_cell(value) -> str:
    if value is None:
        text = ""
    elif isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def print_table(value) -> None:
    records = unwrap_records(value)
    if not records:
        print_json(value)
        return

    if not all(isinstance(record, dict) for record in records):
        print("| value |")
        print("| --- |")
        for record in records:
            print(f"| {markdown_cell(record)} |")
        return

    columns: list[str] = []
    for record in records:
        for key in record:
            if key not in columns:
                columns.append(key)

    print("| " + " | ".join(markdown_cell(column) for column in columns) + " |")
    print("| " + " | ".join("---" for _ in columns) + " |")
    for record in records:
        print("| " + " | ".join(markdown_cell(record.get(column)) for column in columns) + " |")


def print_output(value, output_format: str) -> None:
    if output_format == "json":
        print_json(value)
    else:
        print_table(value)


def require_yes(args: argparse.Namespace, reason: str) -> None:
    if not getattr(args, "yes", False):
        raise SystemExit(f"{reason}. Re-run with --yes after explicit user approval.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Call ERPNext/Frappe REST APIs")
    parser.add_argument(
        "--output",
        choices=["table", "json"],
        default="table",
        help="Output format. Defaults to Markdown table.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami")

    list_p = sub.add_parser("list")
    list_p.add_argument("doctype")
    list_p.add_argument("--fields")
    list_p.add_argument("--filters")
    list_p.add_argument("--or-filters")
    list_p.add_argument("--limit", type=int, default=20)
    list_p.add_argument("--start", type=int, default=0)
    list_p.add_argument("--order-by")

    get_p = sub.add_parser("get")
    get_p.add_argument("doctype")
    get_p.add_argument("name")

    create_p = sub.add_parser("create")
    create_p.add_argument("doctype")
    create_p.add_argument("--data", required=True)
    create_p.add_argument("--yes", action="store_true", help="Confirm this mutating operation is approved")

    update_p = sub.add_parser("update")
    update_p.add_argument("doctype")
    update_p.add_argument("name")
    update_p.add_argument("--data", required=True)
    update_p.add_argument("--yes", action="store_true", help="Confirm this mutating operation is approved")

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("doctype")
    delete_p.add_argument("name")
    delete_p.add_argument("--yes", action="store_true", help="Confirm this mutating operation is approved")

    call_p = sub.add_parser("call")
    call_p.add_argument("method")
    call_p.add_argument("--data")
    call_p.add_argument("--http-method", choices=["GET", "POST"], default="POST")
    call_p.add_argument("--yes", action="store_true", help="Confirm this method call is approved")

    args = parser.parse_args()

    if args.command == "whoami":
        result = request("GET", "/api/method/frappe.auth.get_logged_user")
    elif args.command == "list":
        result = request(
            "GET",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}",
            query={
                "fields": parse_json_arg(args.fields, None),
                "filters": parse_json_arg(args.filters, None),
                "or_filters": parse_json_arg(args.or_filters, None),
                "limit_page_length": args.limit,
                "limit_start": args.start,
                "order_by": args.order_by,
            },
        )
    elif args.command == "get":
        result = request(
            "GET",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}/{urllib.parse.quote(args.name, safe='')}",
        )
    elif args.command == "create":
        require_yes(args, "Creating ERPNext documents changes server data")
        result = request(
            "POST",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}",
            data=parse_json_arg(args.data, {}),
        )
    elif args.command == "update":
        require_yes(args, "Updating ERPNext documents changes server data")
        result = request(
            "PUT",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}/{urllib.parse.quote(args.name, safe='')}",
            data=parse_json_arg(args.data, {}),
        )
    elif args.command == "delete":
        require_yes(args, "Deleting ERPNext documents changes server data")
        result = request(
            "DELETE",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}/{urllib.parse.quote(args.name, safe='')}",
        )
    elif args.command == "call":
        if args.http_method == "POST" or args.method not in READ_ONLY_METHODS:
            require_yes(args, "Calling this ERPNext method may change server data")
        payload = parse_json_arg(args.data, {}) if args.data else None
        result = request(args.http_method, f"/api/method/{args.method}", data=payload)
    else:
        parser.error("unknown command")

    print_output(result, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
