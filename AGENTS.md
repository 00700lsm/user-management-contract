# Contract Repository — Agent rules

This repository is the authoritative source of shared requirements, AA design, logical DB ownership, UI IA, API `openapi.yaml`, team workflow and contract decisions.

## Always-on rules
- Before changes, read `docs/aa/README.md`, `docs/aa/decisions.md`, `docs/contract-governance.md`, `docs/governance/git-workflow.md` and the relevant requirements/DB/UI docs.
- The **approved API** for Frontend and Backend is the committed `openapi.yaml` at their `contract.sha`, **not** necessarily the current Contract `dev` head.
- Domain ownership: A=Auth, B=User, C=Permission; shared API/schema/DB/UI changes require an approved Contract PR before coordinated implementations.
- Accepted PoC decision DEC-009 defines JWT `sub` and `roles` claims, but Backend **must revalidate current account status and roles from DB**. `GET /auth/me` is **not** defined by the present OpenAPI; do not invent it.
- Mock authentication and test fixtures are development/test-only (DEC-010). Never commit tokens, passwords or signing secrets.
- Keep application code in the Backend/Frontend Git repositories, not here or in Workspace root. Do not switch, pull, commit, push, merge or modify another repo automatically.
- Distinguish design acceptance, structural checks, runtime implementation, and actual CI/E2E evidence.

## Explicit callable Skills
- `.agents/skills/run-aa-checks/SKILL.md` — existing Python AA checks (coverage, pins, strict G0)
- `.agents/skills/validate-api-contract/SKILL.md` — API structure/pin checks
- `.agents/skills/review-contract-change/SKILL.md` — read-only compatibility/impact review
- `.agents/skills/check-requirement-coverage/SKILL.md` — REQ/UI/API/DB/TC mapping audit

See `docs/governance/agent-skills-guide.md`. Claude Code adapters live in `.claude/skills/`.
