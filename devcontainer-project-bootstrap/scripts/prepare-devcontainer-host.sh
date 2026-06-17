#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <project-root>" >&2
  exit 64
fi

project_root="$1"
devcontainer_dir="$project_root/.devcontainer"
compose_file="$devcontainer_dir/compose.yaml"

uname_s="$(uname -s 2>/dev/null || printf unknown)"
is_wsl=0
if [ -r /proc/version ] && grep -qi microsoft /proc/version; then
  is_wsl=1
fi

case "$uname_s" in
  Linux)
    DEV_UID="$(id -u)"
    DEV_GID="$(id -g)"
    ;;
  Darwin)
    DEV_UID="${DEV_UID:-1000}"
    DEV_GID="${DEV_GID:-1000}"
    ;;
  *)
    DEV_UID="${DEV_UID:-1000}"
    DEV_GID="${DEV_GID:-1000}"
    ;;
esac

mkdir -p "$devcontainer_dir" "$project_root/data"

if [ "$is_wsl" -eq 1 ]; then
  case "$project_root" in
    /mnt/*)
      echo "Warning: this repository is under /mnt. For WSL, prefer the Linux filesystem, such as ~/projects/my-app." >&2
      ;;
  esac
fi

if [ -f "$compose_file" ]; then
  tmp_file="$compose_file.tmp"
  sed \
    -e "s/DEV_UID: \"[0-9][0-9]*\"/DEV_UID: \"$DEV_UID\"/g" \
    -e "s/DEV_GID: \"[0-9][0-9]*\"/DEV_GID: \"$DEV_GID\"/g" \
    -e "s/user: \"[0-9][0-9]*:[0-9][0-9]*\"/user: \"$DEV_UID:$DEV_GID\"/g" \
    "$compose_file" > "$tmp_file"
  mv "$tmp_file" "$compose_file"
  echo "Updated $compose_file with DEV_UID=$DEV_UID DEV_GID=$DEV_GID"
else
  echo "Warning: $compose_file does not exist; UID/GID values were not written." >&2
fi

echo "Prepared $project_root/data"
echo "Dev Container user and group names remain dev:dev"
