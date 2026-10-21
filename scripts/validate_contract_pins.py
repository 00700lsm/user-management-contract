#!/usr/bin/env python3
"""Read-only FE/BE contract SHA consistency checker; Python 3 standard library only."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys


def status(level: str, code: str, explanation: str) -> None:
    print(f"[{level}] {code}: {explanation}")


def git(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(cwd), *args], capture_output=True, text=True, check=False
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--frontend", type=Path)
    parser.add_argument("--backend", type=Path)
    args = parser.parse_args()

    contract = args.contract.resolve()
    base = contract.parent
    paths = {
        "Frontend": (args.frontend or base / "user-management-frontend").resolve(),
        "Backend": (args.backend or base / "user-management-backend").resolve(),
    }
    failed = 0
    values: dict[str, str] = {}
    for name, folder in paths.items():
        sha_file = folder / "contract.sha"
        if not sha_file.is_file():
            status("WARN", f"{name.upper()}_MISSING", f"{sha_file} absent; cannot check this repository")
            continue
        sha = sha_file.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[a-fA-F0-9]{40}", sha):
            status("FAIL", f"{name.upper()}_INVALID_SHA", f"{sha_file} must contain one 40-hex SHA")
            failed += 1
            continue
        values[name] = sha.lower()
        status("PASS", f"{name.upper()}_SHA_FORMAT", f"{sha_file}: {sha.lower()}")
    if len(values) == 2:
        if len(set(values.values())) != 1:
            status("FAIL", "SHA_MISMATCH", f"Frontend={values['Frontend']} Backend={values['Backend']}")
            failed += 1
        else:
            status("PASS", "SHA_MATCH", f"Frontend/Backend both pin {values['Frontend']}")
    elif len(values) < 2:
        status("WARN", "SHA_MATCH_UNCHECKED", "Both valid FE and BE pins are required for comparison")

    if not (contract / "openapi.yaml").is_file():
        status("FAIL", "CONTRACT_OPENAPI_MISSING", f"{contract / 'openapi.yaml'} not found")
        failed += 1
    else:
        status("PASS", "CONTRACT_OPENAPI_PRESENT", str(contract / "openapi.yaml"))
    if git("rev-parse", "--is-inside-work-tree", cwd=contract).returncode != 0:
        status("WARN", "CONTRACT_GIT_UNAVAILABLE", "Contract .git not available; pinned commit cannot be checked")
    else:
        for sha in sorted(set(values.values())):
            cat = git("cat-file", "-t", sha, cwd=contract)
            if cat.returncode != 0:
                status("WARN", "PIN_NOT_LOCAL", f"{sha} is not in local Contract Git objects; do not auto-fetch")
                continue
            if cat.stdout.strip() != "commit":
                status("FAIL", "PIN_NOT_COMMIT", f"{sha} is not a commit")
                failed += 1
                continue
            show = git("cat-file", "-e", f"{sha}:openapi.yaml", cwd=contract)
            if show.returncode:
                status("FAIL", "PIN_NO_OPENAPI", f"Commit {sha} lacks openapi.yaml")
                failed += 1
            else:
                status("PASS", "PIN_HAS_OPENAPI", f"Commit {sha} contains openapi.yaml")
    if failed:
        status("FAIL", "RESULT", f"{failed} failing check(s)")
        return 1
    status("PASS", "RESULT", "No hard failures; review any WARN items before release")
    return 0


if __name__ == "__main__":
    sys.exit(main())
