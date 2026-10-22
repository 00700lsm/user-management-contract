# Cross-repository integration baseline (G0) / release evidence

This gate addresses [P0-02](https://github.com/00700lsm/user-management-contract/issues/3).
The canonical API is Contract `openapi.yaml` at the identical FE/BE `contract.sha`. Contract's latest `dev` HEAD **need not equal** the implementation-pinned SHA.

## G0: executable version alignment (automatic)

From a Workspace with sibling repositories cloned:

```bash
python3 repos/user-management-contract/scripts/verify_integration_baseline.py \
  --contract repos/user-management-contract \
  --frontend repos/user-management-frontend \
  --backend repos/user-management-backend \
  --report integration-evidence.json
```

The read-only script requires **all 3 Git repositories**, validates SHA format and FE/BE equality, proves that the pinned SHA is an actual local Contract **commit**, and confirms that the pinned revision contains `openapi.yaml`.
It exits 1 for mismatches, absent repositories, invalid/missing SHA, or missing pinned commit. The Contract checkout must have the full history for successful commit proof (in CI `fetch-depth: 0`); no automatic Git fetch, reset, checkout or Contract SHA changes occur.
It emits checkouts' actual commit SHAs and a JSON evidence manifest.

The GitHub workflow `.github/workflows/integration-baseline.yml` checks **Contract + Frontend dev + Backend dev** from separate repositories. It runs via manual dispatch, Contract relevant PR/push, and weekdays to detect drift caused by FE/BE changes that don't trigger Contract CI directly.
This is a **latest dev integration snapshot**, not a release transaction or a check of unmerged FE/BE feature PRs. All three repos need to be accessible to the workflow; if they become private, configure read-only checkout permissions before relying on this gate.
GitHub Actions artifact retention: 30 days.

## G1–G4: runtime proof is separate, never inferred

| Gate | Scope | Evidence / acceptance |
|---|---|---|
| G0 | Git checkout + pinned OpenAPI consistency | This script and CI report **PASS** or **FAIL** |
| G1 | Frontend MSW Mock UI | Actual Playwright/Vitest G1 run with its FE SHA (not real auth) |
| G2 | Running Backend contract responses | Executed route-by-route assertions against pinned schema: statuses, error body, authentication, data |
| G3 | Real JWT from Auth A used by B/C APIs | Real signature/expiry/revocation, current DB Role/status and rollback/integration cases |
| G4 | Frontend→Backend without MSW | Real browser end-to-end signup/login/roles/ADMIN flows, environment and FE/BE commit pair |

**G0 workflow passing does not mean G1-G4 passed.** Its evidence manifest always marks G1-G4 `NOT_RUN`. Current application skeleton does not yet implement actual JWT or most business APIs, so runtime checks are **BLOCKED/NOT_RUN** until implementation and independent execution evidence exist.

## Combining feature branches and release approval

For a release candidate, record `frontend HEAD SHA + backend HEAD SHA + contract SHA + Flyway schema version + G0-G4 links`. A cross-repo `dev` snapshot is not sufficient if candidate commits differ. Do not push both FE/BE contract SHA changes as one imaginary atomic operation; coordinate Contract PR first, stage FE+BE changes, and obtain review before merging.
Breaking changes require a compatibility/migration plan. No automatic release or approval is performed by this gate.

## Troubleshooting

- `SHA_MISMATCH`: FE and BE pins differ; coordinate reviewed Contract update, do not silently sync.
- `Pinned Contract commit ... not available locally`: fetch approved history **manually** or ensure full-history clone.
- Missing sibling repository: clone the missing repository via explicit Workspace init, then rerun.
- G0 PASS but HTTP integration failing: check Controller/DTO/status/schema/security tests, not just pin equality.
