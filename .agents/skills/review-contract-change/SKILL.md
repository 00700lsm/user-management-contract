---
name: review-contract-change
description: Review proposed OpenAPI or shared AA contract changes for backward compatibility, impacted FE/BE domains, requirements and test cases before a Contract PR.
---

# Review Contract Change

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
