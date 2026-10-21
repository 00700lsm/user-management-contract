#!/usr/bin/env python3
"""Read-only structural REQ→UI→API→DB→TC traceability check; no third-party deps."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQ = re.compile(r"\bREQ-(?:AUTH|USER|PERM)-\d{3}\b")
UI = re.compile(r"\bUI-(?:AUTH|USER|PERM)-\d{3}\b")
TC = re.compile(r"\bTC-(?:AUTH|USER|PERM)-\d{3}\b")
API_CELL = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE)(?:/(GET|POST|PUT|PATCH|DELETE))*\s+(/[a-zA-Z0-9_/{}/-]+)"
)
API_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}
OWNERS = {"USER", "AUTH_CREDENTIAL", "ROLE", "USER_ROLE"}


def mark(level: str, code: str, description: str) -> None:
    print(f"[{level}] {code}: {description}")


def source(path: str) -> str:
    file = ROOT / path
    if not file.is_file():
        raise FileNotFoundError(str(file))
    return file.read_text(encoding="utf-8")


def operations(openapi: str) -> set[tuple[str, str]]:
    """Read only top-level OpenAPI paths/methods; validation of YAML is a separate skill."""
    inside_paths = False
    active_path = None
    results: set[tuple[str, str]] = set()
    for line in openapi.splitlines():
        if re.fullmatch(r"paths:\s*", line):
            inside_paths = True
            continue
        if inside_paths and re.match(r"^[a-zA-Z]", line):
            break
        if inside_paths:
            path = re.fullmatch(r"  (/[\w{}./-]+):\s*", line)
            if path:
                active_path = path.group(1)
                continue
            method = re.match(r"    ([a-z]+):\s*", line)
            if method and active_path and method.group(1) in API_METHODS:
                results.add((method.group(1).upper(), active_path))
    return results


def main() -> int:
    try:
        requirement_doc = source("docs/requirements.md")
        ui_doc = source("docs/ui-structure.md")
        db_doc = source("docs/db-design.md")
        trace_doc = source("docs/aa/traceability.md")
        openapi = source("openapi.yaml")
    except (OSError, UnicodeError) as exc:
        mark("FAIL", "INPUT_MISSING", str(exc))
        return 1

    expected_req = set(REQ.findall(requirement_doc))
    expected_ui = set(UI.findall(ui_doc))
    available_api = operations(openapi)
    available_owner = {
        owner for owner in OWNERS if re.search(rf"^\|\s*{owner}\s*\|", db_doc, flags=re.MULTILINE)
    }
    rows = [line for line in trace_doc.splitlines() if re.match(r"^\|\s*REQ-", line)]
    failures = 0
    seen = Counter()
    linked_ops: set[tuple[str, str]] = set()
    referenced_ui: set[str] = set()
    planned_tests: set[str] = set()

    for line in rows:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            mark("FAIL", "TRACE_ROW_INVALID", line)
            failures += 1
            continue
        identifier = REQ.search(cells[0])
        if not identifier:
            mark("FAIL", "TRACE_ID_INVALID", line)
            failures += 1
            continue
        identifier = identifier.group()
        seen[identifier] += 1
        row_ui = set(UI.findall(cells[1]))
        if not row_ui:
            mark("FAIL", "MISSING_UI", identifier)
            failures += 1
        for ui in row_ui:
            referenced_ui.add(ui)
            if ui not in expected_ui:
                mark("FAIL", "UNKNOWN_UI", f"{identifier}: {ui}")
                failures += 1
        row_api = API_CELL.findall(cells[2])
        if not row_api:
            mark("FAIL", "MISSING_API", identifier)
            failures += 1
        for token in re.finditer(
            r"\b((?:GET|POST|PUT|PATCH|DELETE)(?:/(?:GET|POST|PUT|PATCH|DELETE))*)\s+(/[a-zA-Z0-9_/{}/-]+)",
            cells[2],
        ):
            methods, path = token.groups()
            for method in methods.split("/"):
                pair = (method, path)
                linked_ops.add(pair)
                if pair not in available_api:
                    mark("FAIL", "UNKNOWN_API", f"{identifier}: {method} {path}")
                    failures += 1
        has_owner = any(re.search(rf"\b{x}\b", cells[3]) for x in available_owner)
        has_domain = bool(re.search(r"\b(?:Auth|User|Permission)\b", cells[3]))
        if not (has_owner or has_domain):
            mark("FAIL", "MISSING_DB_OWNER", identifier)
            failures += 1
        cases = set(TC.findall(cells[4]))
        if not cases:
            mark("FAIL", "MISSING_TC_ID", identifier)
            failures += 1
        planned_tests.update(cases)

    for item in sorted(expected_req - seen.keys()):
        mark("FAIL", "MISSING_REQ_TRACE", item)
        failures += 1
    for item, count in sorted(seen.items()):
        if item not in expected_req:
            mark("FAIL", "UNKNOWN_REQUIREMENT", item)
            failures += 1
        if count > 1:
            mark("FAIL", "DUPLICATE_REQUIREMENT", f"{item}: {count} rows")
            failures += 1

    unlinked_ui = sorted(expected_ui - referenced_ui)
    unlinked_api = sorted(available_api - linked_ops)
    if unlinked_ui:
        mark("WARN", "UI_WITHOUT_TRACE", ", ".join(unlinked_ui))
    if unlinked_api:
        mark("WARN", "API_WITHOUT_TRACE", ", ".join(f"{m} {p}" for m, p in unlinked_api))
    mark("PASS", "STRUCTURAL_COUNTS", f"REQ={len(expected_req)} traced={len(seen)} UI={len(expected_ui)} API operations={len(available_api)} TC IDs={len(planned_tests)}")
    mark("WARN", "TEST_IMPLEMENTATION_UNVERIFIED", "TC IDs are planned; this script does not search FE/BE tests or run E2E")
    mark("WARN", "SEMANTICS_UNVERIFIED", "A reviewer must confirm business meaning, DB ownership and test adequacy")
    if failures:
        mark("FAIL", "RESULT", f"{failures} structural failure(s)")
        return 1
    mark("PASS", "RESULT", "No structural failures; review WARN items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
