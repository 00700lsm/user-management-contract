#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 1 || ! "$1" =~ ^[a-z0-9][a-z0-9._-]*$ ]]; then
  echo "Usage: bash scripts/workspace/switch-feature.sh auth-login" >&2
  echo "Switches FE and BE to feat/auth-login (the Contract repo remains unchanged)." >&2
  exit 2
fi

FEATURE="feat/$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

for name in user-management-backend user-management-frontend; do
  repo="$ROOT/$name"
  if [[ ! -d "$repo/.git" ]]; then
    echo "[error] $repo not initialized. Run bootstrap.sh" >&2
    exit 1
  fi
  if [[ -n "$(git -C "$repo" status --porcelain)" ]]; then
    echo "[error] Uncommitted changes in $name; commit or stash before switching" >&2
    exit 1
  fi
done

for name in user-management-backend user-management-frontend; do
  repo="$ROOT/$name"
  echo "===== $name → $FEATURE ====="
  git -C "$repo" fetch --prune origin
  if git -C "$repo" show-ref --verify --quiet "refs/heads/$FEATURE"; then
    git -C "$repo" switch "$FEATURE"
  elif git -C "$repo" show-ref --verify --quiet "refs/remotes/origin/$FEATURE"; then
    git -C "$repo" switch --track -c "$FEATURE" "origin/$FEATURE"
  else
    git -C "$repo" switch main
    git -C "$repo" pull --ff-only origin main
    git -C "$repo" switch -c "$FEATURE"
  fi
done

echo "Both implementation repositories now use $FEATURE"
echo "Push each repository separately: git push -u origin $FEATURE"
