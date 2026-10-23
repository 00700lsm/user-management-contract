#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ROOT="$(cd "$CONTRACT_DIR/.." && pwd)"

if [[ "$(basename "$CONTRACT_DIR")" != "user-management-contract" ]]; then
  echo "Place the contract repository in user-management-workspace/user-management-contract." >&2
  exit 1
fi

clone_if_missing() {
  local name="$1"
  local path="$ROOT/$name"
  local url="https://github.com/00700lsm/$name.git"
  if [[ -d "$path/.git" ]]; then
    echo "[exists] $name"
  elif [[ -e "$path" ]]; then
    echo "[error] $path exists but is not a Git repository" >&2
    exit 1
  else
    git clone "$url" "$path"
  fi
}

clone_if_missing user-management-backend
clone_if_missing user-management-frontend
echo ""
echo "[ready] All repositories are available under: $ROOT"
echo "Open: $CONTRACT_DIR/user-management.code-workspace"
echo "For the first sync, run: bash $CONTRACT_DIR/scripts/workspace/sync.sh"
