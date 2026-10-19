---
name: contract-first
description: Check the authoritative shared User Management API, AA design, auth and integration-test rules before implementing or reviewing cross-repository features or modifying a Contract.
---

# Contract-first: shared project baseline

This skill lives in **user-management-contract**, the canonical source of truth. It may be read directly by skills in sibling Backend/Frontend repositories.

1. Find the Contract root (this repository); verify `openapi.yaml`, `docs/requirements.md`, `docs/aa/README.md`, and `docs/governance/git-workflow.md` exist. If absent, stop and report.
2. Read `docs/aa/README.md`, `docs/aa/functional-spec.md`, `docs/architecture.md`, `docs/db-design.md`, `docs/ui-structure.md`, `docs/aa/decisions.md` as relevant.
3. For Auth/secured features also read `docs/aa/auth-design.md`, `docs/aa/mock-fixtures.md`, and `docs/aa/integration-test-plan.md`.
4. For an implementation repository, **do not assume the current Contract branch equals the approved contract version**. Read that implementation repository's `contract.sha` and use the matching committed `openapi.yaml` for schemas/types/tests. Ask for explicit setup or remote access if not available. Never silently update it.
5. Preserve A=Auth FE+BE, B=User FE+BE, C=Permission FE+BE ownership. If OpenAPI or common DB/UI/interface changes are needed, first propose a Contract PR and impact analysis following `docs/contract-governance.md`.
6. Classify missing decisions using `docs/aa/decisions.md`. Do not invent claims, API endpoints, JWT Role contents, or completed implementation.
7. Report requirements/UI/API/DB/test impacts, the pinned Contract SHA, the decisions pending, and validation status.

Do not run any automatic pull, branch switch, commit, push, merge, or apply breaking contract changes without an explicit task.
