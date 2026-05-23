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


def main() -> int:
    parser = argparse.ArgumentParser(description="Call ERPNext/Frappe REST APIs")
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

    update_p = sub.add_parser("update")
    update_p.add_argument("doctype")
    update_p.add_argument("name")
    update_p.add_argument("--data", required=True)

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("doctype")
    delete_p.add_argument("name")

    call_p = sub.add_parser("call")
    call_p.add_argument("method")
    call_p.add_argument("--data")
    call_p.add_argument("--http-method", choices=["GET", "POST"], default="POST")

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
        result = request(
            "POST",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}",
            data=parse_json_arg(args.data, {}),
        )
    elif args.command == "update":
        result = request(
            "PUT",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}/{urllib.parse.quote(args.name, safe='')}",
            data=parse_json_arg(args.data, {}),
        )
    elif args.command == "delete":
        result = request(
            "DELETE",
            f"/api/resource/{urllib.parse.quote(args.doctype, safe='')}/{urllib.parse.quote(args.name, safe='')}",
        )
    elif args.command == "call":
        payload = parse_json_arg(args.data, {}) if args.data else None
        result = request(args.http_method, f"/api/method/{args.method}", data=payload)
    else:
        parser.error("unknown command")

    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
