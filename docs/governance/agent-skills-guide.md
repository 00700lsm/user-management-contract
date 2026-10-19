# Agent Skill 작성 가이드 — 공통 정본

## 공통 소유권
- 공통 요구사항/AA 설계/OpenAPI/인증·테스트 규칙은 **Contract Repository**만 정본으로 유지합니다.
- Frontend/Backend에는 각각 구현 절차 Skill을 둡니다. 업무 사실을 Skill에 중복 정의하지 않고 Contract 파일을 읽도록 합니다.
- Workspace에는 초기화·문서 탐색 Skill만 둡니다. 실제 코드 변경과 Git Commit은 FE/BE/Contract 각 저장소에서 별도로 수행합니다.

## 경로 규칙
- Frontend/Backend Repository에서 Contract는 `../user-management-contract/`.
- Workspace 루트에서 Contract는 `repos/user-management-contract/`.
- 계약 기준은 구현 저장소 `contract.sha`가 지정한 커밋의 `openapi.yaml`; 현재 Contract `dev` Head로 대체하지 않습니다.

## 새 Skill 작성 순서
1. Scope 및 호출 상황을 한 문장으로 정의합니다.
2. 저장소 안 `.agents/skills/기능명/SKILL.md`에 YAML frontmatter의 `name`, `description`을 작성합니다.
3. 본문에 **선행 문서 확인 → 미결정 사항 확인 → 작업 → 검증 → 증거 보고** 순서를 적습니다.
4. Claude Code용 `.claude/skills/기능명/SKILL.md`에는 공통 Skill 참조만 둡니다.
5. `AGENTS.md`와 `CLAUDE.md`에서 발견 경로를 알려줍니다.
6. Agent별로 실제 호출·상대경로·중단 조건을 검증합니다.

## Skill 필수 규칙
- 우선 읽기: Contract `docs/aa/README.md`, `docs/aa/decisions.md`, `docs/governance/git-workflow.md`, 필요한 경우 `docs/aa/auth-design.md`, `docs/aa/integration-test-plan.md`.
- API·DB Owner·화면 공통 규칙을 바꿔야 하면 구현 전에 Contract 변경 PR을 먼저 제안합니다.
- 토큰 Role Claim이나 현재 없는 API를 멋대로 만들지 않습니다.
- Mock Auth/테스트 계정은 비운영 환경만 사용합니다.
- 사용자가 지시하지 않은 Pull·Checkout·Reset·Commit·Push를 하지 않습니다.
- 결과 보고에 REQ/UI/TC ID, Contract SHA, 실제 실행 명령과 테스트 통과/실패/미실행 상태를 구분합니다.
- 미결정 기술 스택/인증 정책을 임의 확정하지 않습니다.

## 리뷰 체크
- [ ] Skill 이름·호출 조건·범위가 명확함
- [ ] 상대 경로·공통 계약 참조가 정확함
- [ ] 독립 Git/계약 변경 선행 흐름 준수
- [ ] 운영 Mock 비활성/비밀값 유출 방지
- [ ] 실제 Agent 호출과 테스트 결과 확인
