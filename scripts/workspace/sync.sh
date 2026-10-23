#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
failed=0
skipped=0

for name in user-management-contract user-management-backend user-management-frontend; do
  repo="$ROOT/$name"
  printf '\n===== %s =====\n' "$name"
  if [[ ! -d "$repo/.git" ]]; then
    echo "[missing] Run: bash user-management-contract/scripts/workspace/bootstrap.sh"
    failed=$((failed + 1))
    continue
  fi

  if ! git -C "$repo" fetch --prune origin; then
    echo "[error] Fetch failed"
    failed=$((failed + 1))
    continue
  fi

  branch="$(git -C "$repo" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  if [[ -z "$branch" ]]; then
    echo "[skip] Detached HEAD: fetched only"
    skipped=$((skipped + 1))
    continue
  fi
  upstream="$(git -C "$repo" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
  if [[ -z "$upstream" ]]; then
    echo "[skip] $branch has no remote tracking branch; fetched only"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ -n "$(git -C "$repo" status --porcelain)" ]]; then
    echo "[skip] Uncommitted changes on $branch; fetched only (your changes are safe)"
    skipped=$((skipped + 1))
    continue
  fi
  if git -C "$repo" pull --ff-only; then
    echo "[ok] Updated $name ($branch <= $upstream)"
  else
    echo "[attention] Cannot fast-forward $name/$branch. Resolve manually; no merge was attempted."
    failed=$((failed + 1))
  fi
done

printf '\nWorkspace sync: %s errors, %s skipped repositories.\n' "$failed" "$skipped"
if [[ "$failed" -gt 0 ]]; then exit 1; fi
