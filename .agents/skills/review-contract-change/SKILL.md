---
name: review-contract-change
description: Review proposed OpenAPI or shared AA contract changes for backward compatibility, impacted FE/BE domains, requirements and test cases before a Contract PR.
---

# Review Contract Change

## Persona

- **Role:** API 계약 변경 영향 분석가
- **Mission:** OpenAPI·AA 변경의 호환성과 Auth/User/Permission 전파 영향을 평가하는 리뷰어
- **Working principle:** 명시된 두 버전의 diff와 소비자 영향·결정 사항을 근거로 위험을 분류한다
- **Authority boundary:** 계약을 단독 개정하거나 PR을 승인·병합하지 않는다


## Trigger and inputs
Run when the user requests a contract change review, breaking-change assessment, or PR impact report. Required inputs: an explicit base and target (`main` vs feature branch, two commits, or the existing pinned Contract SHA vs working tree). **If the comparison baseline cannot be identified**, ask for one instead of inventing it. This is a **read-only review**.

## Execution
1. Read `docs/contract-governance.md`, `docs/aa/decisions.md`, `docs/aa/traceability.md`, `docs/requirements.md`, `docs/ui-structure.md` and affected API operations. Use the accepted DEC decisions; `GET /auth/me` is not in the current contract; JWT `sub`/`roles` policy is Accepted DEC-009 (runtime still must validate current DB roles).
2. Ensure both baselines exist. For local Git branches/commits, read diff without changing branches:
   ```bash
   git diff --unified=3 BASE TARGET -- openapi.yaml docs/
   git show BASE:openapi.yaml
   git show TARGET:openapi.yaml
   ```
   The above commands use placeholder BASE/TARGET; substitute *explicit resolved refs*. If target is a working tree, inspect `git diff -- openapi.yaml docs/` and `git diff --cached -- openapi.yaml docs/` separately. Do not pull automatically.
3. Validate both OpenAPI versions where a preinstalled validator is available, or report syntax checks as `NOT_RUN`. For a machine-assisted OpenAPI diff, use an **already installed** compatible diff tool only if available; don't claim to have run one otherwise.
4. Compare path+method and operations: removals/additions, request parameters and required fields, types/enums, response status/body, auth/security, defaults, and error schema. Treat removal, making optional input required, narrowing enum, incompatible response type and authorization escalation as **potentially breaking**. Breaking classification requires reviewing consumers and context; do not equate every schema change with a proven break.
5. Map changes through traceability REQ → UI → API → DB owner → TC; list A(Auth)/B(User)/C(Permission) affected FE and BE work. Inspect actual files/PRs if available; otherwise mark developer impact as `needs confirmation`.
6. Identify prerequisite AA decision changes, Contract PR reviewers, API pin update work and G2/G3/G4 test scenarios. Never modify, approve or merge the PR as part of this review.


## 개발 기능 PR의 최신 Contract/dev 영향 검토

사용자가 Backend/Frontend 기능 PR 리뷰를 요청하면, 비교 기준을 **PR의 pinned Contract SHA → 리뷰 당시 Contract/dev HEAD SHA**로 명시하고 읽기 전용으로 비교합니다. 먼저 최신 dev HEAD를 조회하되 브랜치를 자동으로 전환하거나 Pull하지 않습니다. 현재 dev SHA를 기록하고 두 버전 간 수정된 operation/상태코드/요청·응답·권한을 검사합니다. 영향받는 A/B/C 담당자에게 변경을 전달하고 실제 구현·계약 테스트가 확인되지 않았으면 `NEEDS_REVIEW`로 표시합니다. SHA가 다르다는 이유만으로 BREAKING이라고 단정하지 않습니다.

- 기존 기능 PR은 새 CI 시행에 따라 소급 차단하지 않습니다. 변경이 무관하면 개발을 계속하고, 관련된 변경은 원래 PR 브랜치에 수정 커밋을 추가하도록 제안합니다.
- 리뷰 이후 Contract/dev가 변경될 수 있으므로 병합 직전에 최신 SHA와 검토 SHA가 같은지 다시 확인합니다. 다르면 변경된 범위를 재검토합니다.
- CI의 drift WARNING은 호환성 PASS 증거가 아닙니다. 필수 pinned OpenAPI/통합 테스트 및 실제 FE/BE 검증 근거를 별도로 기록합니다.

## Output contract
```text
변경 기준: BASE -> TARGET (commit SHAs)
API/AA 변경 목록 (path/method/field)
호환성: BREAKING_CANDIDATE | NON_BREAKING | NEEDS_REVIEW
영향: REQ/UI/API/DB/TC + A/B/C 담당 FE/BE
API 계약 검사: PASS | FAIL | NOT_RUN
미결정·협의 사항, 필요한 Contract PR/후속 FE·BE PR
리뷰 결론: PASS | WARN | FAIL (근거와 한계)
```

No automatic changes, Git writes, dependency installations, Contract SHA updates or claims of runtime compliance.
