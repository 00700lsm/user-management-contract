# Shared Contract Repository — Agent instructions

This Repository is the **canonical AA design/API contract/skill governance** source. It is not the runtime frontend or backend project.

Read `docs/aa/README.md`, `docs/governance/git-workflow.md`, and `docs/governance/agent-skills-guide.md` before changing shared artifacts.

- Canonical skill: `.agents/skills/contract-first/SKILL.md`.
- Auth-related behavior: `docs/aa/auth-design.md`, `docs/aa/mock-fixtures.md`, `docs/aa/integration-test-plan.md`.
- Treat `openapi.yaml` as the only external FE↔BE API Schema source; do not assume role claims or a `GET /auth/me` endpoint exists.
- A=Auth FE+BE, B=User FE+BE, C=Permission FE+BE.
- Change shared API/DB/interface with reviewed Contract PR before implementing in sibling repositories.
- `main`: stable baseline, `dev`: team development; use feature branch → dev PR.
- Do not place implementation code in Workspace root, and never commit real tokens, secrets or passwords.
