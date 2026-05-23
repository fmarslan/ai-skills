#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <project-root>" >&2
  exit 64
fi

project_root="$1"
devcontainer_dir="$project_root/.devcontainer"
env_file="$devcontainer_dir/.env"
devcontainer_json="$devcontainer_dir/devcontainer.json"
codex_dir="$project_root/data/.codex"

uname_s="$(uname -s 2>/dev/null || printf unknown)"
is_wsl=0
if [ -r /proc/version ] && grep -qi microsoft /proc/version; then
  is_wsl=1
fi

case "$uname_s" in
  Linux)
    DEV_USERNAME="$(id -un)"
    DEV_GROUPNAME="$(id -gn)"
    DEV_UID="$(id -u)"
    DEV_GID="$(id -g)"
    ;;
  Darwin)
    DEV_USERNAME="${DEV_USERNAME:-dev}"
    DEV_GROUPNAME="${DEV_GROUPNAME:-dev}"
    DEV_UID="${DEV_UID:-1000}"
    DEV_GID="${DEV_GID:-1000}"
    ;;
  *)
    DEV_USERNAME="${DEV_USERNAME:-dev}"
    DEV_GROUPNAME="${DEV_GROUPNAME:-dev}"
    DEV_UID="${DEV_UID:-1000}"
    DEV_GID="${DEV_GID:-1000}"
    ;;
esac

mkdir -p "$devcontainer_dir" "$codex_dir"

if [ "$is_wsl" -eq 1 ]; then
  case "$project_root" in
    /mnt/*)
      echo "Warning: this repository is under /mnt. For WSL, prefer the Linux filesystem, such as ~/projects/my-app." >&2
      ;;
  esac
fi

if [ "$uname_s" = "Linux" ]; then
  current_owner="$(stat -c '%u:%g' "$codex_dir" 2>/dev/null || printf unknown)"
  desired_owner="$DEV_UID:$DEV_GID"
  if [ "$current_owner" != "$desired_owner" ]; then
    if chown -R "$desired_owner" "$codex_dir" 2>/dev/null; then
      :
    else
      echo "Error: $codex_dir is owned by $current_owner, expected $desired_owner." >&2
      echo "Run: sudo chown -R \"$desired_owner\" data/.codex" >&2
      exit 1
    fi
  fi
fi

cat > "$env_file" <<EOF
DEV_USERNAME=$DEV_USERNAME
DEV_GROUPNAME=$DEV_GROUPNAME
DEV_UID=$DEV_UID
DEV_GID=$DEV_GID
EOF

if [ -f "$devcontainer_json" ]; then
  tmp_file="$devcontainer_json.tmp"
  sed "s/\"remoteUser\": \"[^\"]*\"/\"remoteUser\": \"$DEV_USERNAME\"/" "$devcontainer_json" > "$tmp_file"
  mv "$tmp_file" "$devcontainer_json"
fi

echo "Prepared $codex_dir"
echo "Wrote $env_file"
echo "DEV_USERNAME=$DEV_USERNAME DEV_GROUPNAME=$DEV_GROUPNAME DEV_UID=$DEV_UID DEV_GID=$DEV_GID"
