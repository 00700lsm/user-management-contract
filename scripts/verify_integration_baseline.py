#!/usr/bin/env python3
"""Strict, read-only integration baseline gate for Contract, Frontend and Backend.

Exit 0 means ONLY that all three Git repositories exist, FE/BE pin the exact
same Contract commit, and that commit contains openapi.yaml. It does NOT
mean runtime contract, JWT, or E2E tests passed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

HEX40 = re.compile(r"^[a-fA-F0-9]{40}$")


def git(repo: Path, *args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
        )
        return p.returncode, p.stdout.strip()
    except OSError:
        return 127, ""


def find_head(repo: Path, name: str, failures: list[str]) -> str | None:
    if not repo.is_dir():
        failures.append(f"{name}: repository directory missing: {repo}")
        return None
    result, sha = git(repo, "rev-parse", "--verify", "HEAD")
    if result != 0 or not HEX40.fullmatch(sha):
        failures.append(f"{name}: Git HEAD missing or invalid in {repo}")
        return None
    return sha.lower()


def load_pin(repo: Path, name: str, failures: list[str]) -> str | None:
    file = repo / "contract.sha"
    if not file.is_file():
        failures.append(f"{name}: contract.sha is missing: {file}")
        return None
    try:
        sha = file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        failures.append(f"{name}: cannot read contract.sha: {exc}")
        return None
    if not HEX40.fullmatch(sha):
        failures.append(f"{name}: contract.sha must contain exactly one 40-hex Git SHA")
        return None
    return sha.lower()


def check(contract: Path, frontend: Path, backend: Path) -> dict:
    failures: list[str] = []
    heads = {
        "contract": find_head(contract, "Contract", failures),
        "frontend": find_head(frontend, "Frontend", failures),
        "backend": find_head(backend, "Backend", failures),
    }
    pins = {
        "frontend": load_pin(frontend, "Frontend", failures),
        "backend": load_pin(backend, "Backend", failures),
    }
    approved = pins["frontend"] if pins["frontend"] == pins["backend"] else None
    if pins["frontend"] and pins["backend"] and approved is None:
        failures.append(
            "TC-INT-011: FE/BE Contract SHA mismatch: "
            f"FE={pins['frontend']} BE={pins['backend']}"
        )
    if approved:
        if heads["contract"] is None:
            failures.append("Cannot resolve pinned Contract without valid Contract Git checkout")
        else:
            result, obj = git(contract, "cat-file", "-t", approved)
            if result != 0 or obj != "commit":
                failures.append(
                    f"Pinned Contract commit {approved} not available locally; "
                    "checkout full Contract history (fetch-depth: 0)"
                )
            elif git(contract, "cat-file", "-e", f"{approved}:openapi.yaml")[0] != 0:
                failures.append(f"Pinned Contract commit {approved} has no openapi.yaml")
    if heads["contract"] and git(contract, "cat-file", "-e", "HEAD:openapi.yaml")[0]:
        failures.append("Current Contract checkout has no openapi.yaml")

    baseline = "FAIL" if failures else "PASS"
    return {
        "schema_version": 1,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_commits": heads,
        "contract_pins": pins,
        "verified_contract_sha": approved if baseline == "PASS" else None,
        "checks": {
            "TC-INT-011": baseline,
            "repository_commits": baseline,
            "approved_openapi_at_pin": baseline,
        },
        "gates": {
            "G0_cross_repo_baseline": baseline,
            "G1_frontend_mock_ui": "NOT_RUN",
            "G2_backend_runtime_contract": "NOT_RUN",
            "G3_real_auth_integration": "NOT_RUN",
            "G4_frontend_backend_e2e": "NOT_RUN",
        },
        "release_readiness": "NOT_VERIFIED",
        "limitations": [
            "G0 PASS proves only repository commits and pinned OpenAPI consistency.",
            "G1-G4 require separate actual test evidence and cannot be inferred.",
            "These commits are checkouts at execution time, not an atomic multi-repository release.",
        ],
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--contract", type=Path, default=root)
    parser.add_argument("--frontend", type=Path, default=root.parent / "user-management-frontend")
    parser.add_argument("--backend", type=Path, default=root.parent / "user-management-backend")
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    report = check(
        args.contract.resolve(), args.frontend.resolve(), args.backend.resolve()
    )
    for name, sha in report["source_commits"].items():
        print(f"[{'PASS' if sha else 'FAIL'}] {name} checkout: {sha or 'unavailable'}")
    print(f"[{report['checks']['TC-INT-011']}] FE/BE Contract SHA alignment")
    for failure in report["failures"]:
        print(f"[FAIL] {failure}")
    for gate, status in report["gates"].items():
        print(f"[{status}] {gate}")
    print("[WARN] G0 PASS is not proof of runtime OpenAPI, real JWT or browser E2E")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"[INFO] Saved integration evidence manifest: {args.report}")
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
