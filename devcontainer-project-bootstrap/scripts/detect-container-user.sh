#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <image-ref>" >&2
  exit 64
fi

image_ref="$1"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker command not found" >&2
  exit 69
fi

docker image inspect "$image_ref" >/dev/null 2>&1 || docker pull "$image_ref" >/dev/null

configured_user="$(docker image inspect --format '{{.Config.User}}' "$image_ref" 2>/dev/null || true)"

if [ -n "$configured_user" ] && [ "$configured_user" != "0" ] && [ "$configured_user" != "root" ]; then
  echo "$configured_user" | cut -d: -f1
  exit 0
fi

runtime_user="$(docker run --rm --entrypoint /bin/sh "$image_ref" -lc 'id -un 2>/dev/null || true' 2>/dev/null || true)"

if [ -n "$runtime_user" ] && [ "$runtime_user" != "0" ] && [ "$runtime_user" != "root" ]; then
  echo "$runtime_user"
  exit 0
fi

if docker run --rm --entrypoint /bin/sh "$image_ref" -lc 'getent passwd vscode >/dev/null 2>&1' 2>/dev/null; then
  echo "vscode"
  exit 0
fi

echo "dev"
