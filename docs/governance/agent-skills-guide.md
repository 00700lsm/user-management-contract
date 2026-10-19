# 팀 Agent Skill 작성·운영 가이드 (공통 정본)

대상: Claude Code, Cursor, Codex 등 **프로젝트 로컬 Agent Skills를 지원하는 도구**. 도구·버전에 따라 탐색 경로/호출 방법이 다를 수 있으므로 실제 실행 전에 확인합니다.

## 배치 구조

```text
user-management-workspace/        # Workspace 자체 별도 Git
├── AGENTS.md
├── .agents/skills/contract-reference/SKILL.md  # Root 진입 / 공통 탐색
├── repos/
│   ├── user-management-contract/
│   │   ├── openapi.yaml
│   │   ├── docs/aa/...
│   │   ├── docs/governance/agent-skills-guide.md  # 이 문서: 정본
│   │   └── .agents/skills/contract-first/SKILL.md # 공통 Contract 확인 절차
│   ├── user-management-backend/
│   │   ├── .agents/skills/backend-workflow/SKILL.md
│   │   └── .claude/skills/backend-workflow/SKILL.md
│   └── user-management-frontend/
│       ├── .agents/skills/frontend-workflow/SKILL.md
│       └── .claude/skills/frontend-workflow/SKILL.md
```

**Contract의 문서/규칙은 별도 저장소가 정본**입니다. Frontend/Backend Skill은 해당 문서를 복사하지 않고 상대 경로 `../user-management-contract/`를 읽습니다. Workspace에서 Agent를 시작한 경우에는 `repos/user-management-contract/`를 읽습니다.

## Skill 최소 파일

`<owner-repo>/.agents/skills/<kebab-case-name>/SKILL.md`

```markdown
---
name: example-workflow
description: Use when explicitly asked to prepare or implement a specific project task while checking the shared Contract repository.
---

# Example Workflow

1. Locate the current Git repository root.
2. Locate sibling `../user-management-contract`; stop and ask for workspace initialization if absent.
3. Read shared `docs/governance/git-workflow.md`, `docs/aa/README.md`, `docs/aa/decisions.md`, and `openapi.yaml`.
4. Verify `contract.sha`; use its pinned OpenAPI for code generation/contract tests.
5. Perform only user-authorized work in the owning Git repository.
6. Run the relevant checks and report results, gaps, changes and affected PRs.
```

Claude Code 필요 시 `.claude/skills/<name>/SKILL.md`는 **공통 Skill 파일 참조 Adapter**로만 작성해 중복을 피합니다.

## 작성 원칙
1. **Scope**: 한 Skill에 하나의 명확한 업무(초기 설정, FE 개발, BE 개발, 계약 점검). 과도한 '만능' Skill 금지.
2. **Trigger**: description에 언제 실행하는지 명시. 위험하거나 상태 변경이 포함되면 명시적 호출을 권장.
3. **단일 정본**: 요구/DB/화면/API/인증/테스트 정책은 Contract Repository; Skill은 *문서의 위치와 절차*만 기술.
4. **Relative Path**: FE/BE 저장소에서 `../user-management-contract`를 우선 사용; 없으면 추측하지 않고 Init 안내. Workspace Root는 `repos/user-management-contract` 사용.
5. **Pinning**: 외부 API는 `openapi.yaml`의 **승인된 Contract Commit SHA(`contract.sha`)** 기준. `dev` 문서는 최신 설계 참고용, 고정 계약을 몰래 덮어쓰지 않음.
6. **Change Control**: 개발자에게 영향을 주는 API·DB·UI 공통 변경은 Contract 변경 PR을 먼저 제안·승인.
7. **Security**: Mock/테스트 키는 운영 환경에서 차단, Git 비밀값/토큰 커밋 금지, 기존 브랜치/작업 파일 임의 수정 금지.
8. **Evidence**: Skill은 단계별 검사/미결정 항목/실행 결과를 보고. 테스트하지 않은 동작을 '완료'라고 적지 않음.
9. **Portability**: 특정 Agent 전용 명령을 공통 Skill 본문에 강제하지 않음. 지원 도구별 Adapter/호출법은 간단히 안내.

## 새 Skill PR 리뷰 체크리스트
- [ ] Skill name/description/호출 조건이 명확함
- [ ] 공통 Contract 문서 링크와 상대 경로가 올바름
- [ ] 운영 중 계약 변경·기존 Git 변경을 자동으로 수행하지 않음
- [ ] 기술 스택 미확정 사항과 승인 필요 지점 명시
- [ ] Mock·Secrets·권한 테스트 안전장치 포함
- [ ] `main` / `dev` 두 기준선의 인계 문서를 확인하고 상대 경로 체크
- [ ] 최소 한 번 실제 Agent로 호출해 경로/의도한 작업 범위 검증

## 스킬 변경 책임
- 공통 기준/문서/contract-first: Contract 저장소에서 PR 리뷰
- FE Skill: Frontend 저장소의 PR 및 AA/관련 담당자 리뷰
- BE Skill: Backend 저장소의 PR 및 AA/관련 담당자 리뷰
- Workspace 진입 Skill: Workspace 저장소에서 PR 리뷰 (코드/업무 정본 저장 금지)

스킬 설치·발견·자동 호출 여부는 Agent 구현별로 다릅니다. `AGENTS.md`와 `CLAUDE.md`에 진입 가이드를 작성하되 **자동으로 동작한다고 보장하지 않습니다**.
