---
name: validate-api-contract
description: Run read-only OpenAPI schema validation and verify that Frontend and Backend pin the same approved Contract commit when checking API compatibility or preparing integration.
---

# Validate API Contract

## Trigger and inputs
Run when the user asks to validate the API contract, check contract SHA alignment, or verify the FE/BE integration baseline. This skill is **read-only**; it never updates `contract.sha`, fetches/pulls, installs packages automatically, or modifies a repository.

Inputs: Contract Git root; optional Frontend/Backend local repository paths (by default siblings `../user-management-frontend`, `../user-management-backend`). If running at Workspace root, Contract is `repos/user-management-contract`.

## Execution
1. Locate Contract root and `openapi.yaml`; inspect `docs/contract-governance.md` and `docs/aa/decisions.md`.
2. For OpenAPI syntax/reference validation, if `npx` exists and packages are already available or the user has authorized a package download, run from Contract root:
   ```bash
   npx --no-install @apidevtools/swagger-cli validate openapi.yaml
   ```
   If the tool is not installed, mark `WARN NOT_RUN`. Do **not** claim this check passed. The existing GitHub Actions `.github/workflows/validate-openapi.yml` can be used as independent CI evidence **only if that run's result was actually checked**.
3. Run the checked-in standard-library script:
   ```bash
   python3 scripts/validate_contract_pins.py
   ```
   Optional: `python3 scripts/validate_contract_pins.py --frontend /path/to/frontend --backend /path/to/backend`. It checks SHA format, equality, that local Contract Git has the pinned commit and `openapi.yaml` at that commit. It never fetches automatically.
4. If `contract.sha` paths are absent, local Contract Git objects are missing, or an OpenAPI validator cannot execute, report `WARN/NOT_RUN` with the reason. A valid SHA string alone is **not** proof a commit exists on GitHub.
5. Record working-branch/commit if available, pin SHA and check outputs. Never use moving Contract `dev` to silently replace pinned contracts.

## Output contract
```text
API 계약 검증
- OpenAPI validation: PASS | FAIL | NOT_RUN (command / output)
- Frontend pin format / Backend pin format: PASS | FAIL | WARN
- FE/BE pin equality: PASS | FAIL | WARN
- pinned commit + openapi.yaml existence: PASS | FAIL | WARN
- Overall: FAIL if a hard check failed; INCOMPLETE if mandatory checks cannot run; PASS only for completed checks
- Evidence: command, exit code, local paths/SHA and CI link if verified
- Required next actions (none applied)
```

OpenAPI schema validity and equal pins **do not prove a running Backend implements its contract**. Leave G2 runtime request/response and G3/G4 integration tests to their owners. Do not push, commit, merge or edit any files unless separately requested.
