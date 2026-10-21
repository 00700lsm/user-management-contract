# Claude Code — Contract

Read `AGENTS.md` and `docs/governance/agent-skills-guide.md` as always-on rules. This repository is the shared AA and OpenAPI authority. DEC-001~011 contain the Accepted PoC decisions; do not infer unimplemented endpoints.

Use the following **explicit skills** when the task calls for them:
- `/validate-api-contract`: check OpenAPI validity and FE/BE pinned SHA.
- `/review-contract-change`: examine a base→target change and its compatibility/impact.
- `/check-requirement-coverage`: inspect REQ→UI→API→DB→TC linkage.

Each Claude skill at `.claude/skills/<name>/SKILL.md` delegates to the canonical `.agents/skills/<name>/SKILL.md`. Do not alter branches or files in a read-only skill run.
