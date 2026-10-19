---
name: contract-first
description: Use before feature implementation or cross-repository review to read canonical AA design and pinned API contract.
---

# Contract-first

1. Locate the user-management-contract repository. Read docs/aa/README.md, docs/requirements.md, docs/architecture.md, docs/db-design.md, docs/ui-structure.md and docs/aa/decisions.md.
2. For protected pages/APIs read docs/aa/auth-design.md, docs/aa/mock-fixtures.md, docs/aa/integration-test-plan.md.
3. OpenAPI is the canonical external API. For FE/BE work use the OpenAPI **at each implementation repository's contract.sha commit**, not moving dev HEAD.
4. A=Auth FE+BE, B=User FE+BE, C=Permission FE+BE. Changes to shared API/schema/DB Owner/UI require Contract PR first.
5. Never assume JWT roles or GET /auth/me is already implemented. Escalate undecided policies to AA/PL.
6. Report impacted REQ/UI/API/TC, contract SHA, validation evidence, decisions still open.
7. Do not switch branches, commit, push, reset, or merge unless explicitly requested.
