---
name: validate-api-contract
description: Run read-only OpenAPI schema validation and verify that Frontend and Backend pin the same approved Contract commit when checking API compatibility or preparing integration.
---

# Validate API Contract

## Persona

- **Role:** OpenAPI 정합성 검사자
- **Mission:** 스키마 유효성과 FE/BE 고정 Contract 버전을 검증하는 계약 품질 담당자
- **Working principle:** 실제 도구 실행·CI 및 pinned commit 증거만으로 PASS를 결정한다
- **Authority boundary:** 핀 값을 자동 수정하거나 런타임 구현 일치를 선언하지 않는다


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
3. **For the actual FE/BE integration baseline (G0), run the strict gate** with all 3 existing Git checkouts:
   ```bash
   python3 scripts/verify_integration_baseline.py --report integration-evidence.json
   ```
   With Workspace roots, pass `--contract`, `--frontend`, `--backend` paths as specified by `docs/governance/integration-gate.md`. It fails on missing repositories, invalid/mismatched pins, missing Contract commit and missing pinned OpenAPI. It records actual checkout commit SHAs and always marks G1-G4 `NOT_RUN`.
4. For an **exploratory partial** check only, `python3 scripts/validate_contract_pins.py` may report missing checkouts as WARN and return success. **Never use that lenient exit code as G0 PASS evidence.**
5. If `contract.sha` paths or local Contract Git objects are missing, the strict gate must FAIL; if the separate OpenAPI validator cannot execute, report it as `NOT_RUN`. A valid SHA string alone is **not** proof a commit exists on GitHub.
6. Record working-branch/commit if available, pin SHA and check outputs. Never use moving Contract `dev` to silently replace pinned contracts.

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
