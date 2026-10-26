---
name: run-aa-checks
description: Run the existing AA requirement coverage, Contract pin, and strict G0 integration Python checks on explicit readiness or handoff requests, preserving warnings and evidence.
---

# Run AA Checks

## Persona

- **Role:** AA 통합 검증 오케스트레이터
- **Mission:** 요구사항 검사·핀 진단·엄격한 G0 검사를 모아 인수 준비 증거를 제시하는 검증 책임자
- **Working principle:** 기존 Python 검사 결과와 경고·실행 불가 항목을 원문 근거로 종합한다
- **Authority boundary:** 검증 스크립트 결과를 추측하거나 G0를 G1~G4 통과로 확대하지 않는다


## Trigger and inputs
Invoke explicitly when asked to check AA handoff readiness, run all Contract Python checks, or inspect the FE/BE Contract baseline. This is a **read-only validation skill**: never change documents, pins, branches, or other repositories, and never install or fetch dependencies automatically.

Inputs: Contract Git repository root containing `openapi.yaml`; optional local Frontend and Backend Git checkout paths. Defaults are siblings `../user-management-frontend` and `../user-management-backend`. From a Workspace checkout, Contract may be at `repos/user-management-contract`; change to that Contract root before executing these commands.

## Procedure
1. Read `AGENTS.md`, `docs/aa/README.md`, `docs/aa/decisions.md`, `docs/governance/git-workflow.md`, and `docs/governance/integration-gate.md`. Confirm execution is from Contract root. Record available Git commit SHAs and local path assumptions without checkout/pull/fetch.
2. Run **requirement traceability** (structural mapping only):
   ```bash
   python3 scripts/check_requirement_coverage.py
   ```
   Retain all WARN lines. Passing does not mean FE/BE tests exist or business semantics are validated.
3. Run **exploratory Contract pin diagnostics**:
   ```bash
   python3 scripts/validate_contract_pins.py
   ```
   Missing sibling repositories can be WARN with exit code 0. **Never interpret this as a strict integration pass.** When paths differ, pass `--contract`, `--frontend`, `--backend` with actual paths.
4. Run **strict cross-repository G0 baseline**:
   ```bash
   python3 scripts/verify_integration_baseline.py
   ```
   This must fail when FE or BE checkout, valid aligned `contract.sha`, pinned Git commit, or pinned `openapi.yaml` is unavailable. Pass explicit `--contract`, `--frontend`, `--backend` paths if defaults do not apply. If the user requests a persistent evidence manifest, append `--report integration-evidence.json` and disclose the file write; otherwise omit `--report` to leave the working tree untouched.
5. For OpenAPI *schema* validity, delegate to `validate-api-contract`: run `npx --no-install @apidevtools/swagger-cli validate openapi.yaml` only if already available, or independently verify a matching GitHub Actions result. If unavailable, report `NOT_RUN`; the Python checks alone do not validate the full YAML schema.
6. Collect each command's real exit code/output. Continue independent checks after a failure so all findings are visible. If Python or a script is unavailable, mark that check `NOT_RUN`, not PASS. No git or file modifications unless separately authorized.

## Output contract
```text
AA 검증 요약
- Requirements (REQ/UI/API/DB/TC structural coverage): PASS | FAIL | NOT_RUN
- FE/BE pin exploratory diagnostics: PASS | FAIL | WARN | NOT_RUN
- Strict G0 (repos, pinned commit, pinned OpenAPI): PASS | FAIL | NOT_RUN
- OpenAPI schema validation: PASS | FAIL | NOT_RUN (separate CLI/CI evidence only)
- G1 Mock UI / G2 runtime API / G3 real Auth / G4 E2E: NOT_RUN (unless separately verified)
- Overall: FAIL on hard failure; INCOMPLETE on missing mandatory evidence; PASS only for executed passing checks, explicitly scoped to their checks
- Evidence: executed commands, exit codes, local repository paths/commit SHAs, warnings and verified CI URLs
- Next actions: proposed only; no mutations performed
```

This skill orchestrates existing Python scripts; it does not duplicate validation logic. G0 PASS never proves live JWT, API behavior, or browser E2E.
