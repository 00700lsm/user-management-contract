---
name: check-requirement-coverage
description: Check traceability coverage between requirements, UI screen IDs, OpenAPI operations, logical data owners and planned tests before AA handoff or feature review.
---

# Check Requirement Coverage

## Persona

- **Role:** 요구사항 추적성 감사자
- **Mission:** REQ·UI·API·데이터 소유권·TC 연결의 누락과 모순을 찾는 AA 품질 담당자
- **Working principle:** 구조적 커버리지와 실제 구현·테스트 증거를 분리해 판정한다
- **Authority boundary:** 요구사항을 임의 보완하거나 개발 완료·인수 완료로 승인하지 않는다


## Trigger and inputs
Run on a request for requirement coverage, SDD handoff readiness, missing REQ/UI/API/test mappings or domain-specific coverage (Auth/User/Permission). The checked-in script checks the **entire** AA baseline; filter findings to a requested domain in the final report and still mention global failures.

## Execution
1. Locate Contract root and read `docs/requirements.md`, `docs/ui-structure.md`, `docs/db-design.md`, `docs/aa/traceability.md`, `docs/aa/integration-test-plan.md` and `docs/aa/decisions.md`.
2. Execute the standard-library structural check:
   ```bash
   python3 scripts/check_requirement_coverage.py
   ```
   It verifies listed REQ IDs, mapped UI IDs, actual OpenAPI path+HTTP method, declared DB-owner/domain association and planned TC identifiers. It reports gaps as PASS/WARN/FAIL; **the script does not implement test execution**.
3. Investigate warnings: new OpenAPI operations not mapped, UI without a requirement, contradictory mapping, duplicated IDs, potential wrong owner or missing test assertions. Compare the actual requirement text, screen flow, API schema, account-role policies and DB logical relationships. This qualitative check cannot be fully automated.
4. Separate (a) structurally mapped design, (b) test IDs planned, and (c) actual FE/BE/CI/E2E implementation evidence. Don't mark an item implemented just because `TC-*` appears in `traceability.md`.
5. Produce a requirement-by-requirement findings table (or domain filter), with REQ/UI/endpoint/Owner/TC and recommendations. Do not edit AA files or check handoff boxes unless explicitly requested.

## Output contract
```text
Coverage target: all | Auth | User | Permission
Command and exit status
REQ mapped / UI mapped / API mapped / DB owner mapped / TC planned
PASS: structurally consistent mappings
WARN: unverified semantics / missing test execution evidence
FAIL: broken/duplicate IDs, missing references, unknown endpoints
Required AA updates and owners (not applied)
```

Use `docs/aa/handoff-checklist.md` only as a review checklist; its unchecked boxes are not automatically completed.
