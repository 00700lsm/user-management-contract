# AA 설계 인계 패키지 — 공통 정본

**상태: Draft / 팀 합의 필요**. 이 저장소는 요구사항, 기능 책임, 외부 API 계약, DB 논리 모델, 화면 IA와 변경관리의 단일 정본입니다. 구현 저장소에는 필요한 분야별 인계/검증 문서만 두며 공통 사실을 중복 확정하지 않습니다.

## 읽는 순서
1. [요구사항/완료 기준](../requirements.md) — 범위와 요구 ID
2. [기능 상세 및 업무 규칙](./functional-spec.md) — 주요 시나리오, 예외, 접근권한
3. [시스템 아키텍처/책임 경계](../architecture.md) — Auth/User/Permission, 각 데이터 Owner
4. [DB 논리 모델](../db-design.md) — Entity/Key/관계/삭제 정책
5. [화면 IA 및 화면 ID](../ui-structure.md), [공통 UI 원칙](../ui-guidelines.md)
6. [OpenAPI 정본](../../openapi.yaml) — **실제 Request/Response/Endpoint 최종 기준**
7. [요구사항 추적표](./traceability.md) — REQ↔UI↔API↔데이터↔테스트
8. [미결정 사항/설계 결정](./decisions.md) — 개발 전 확인 항목
9. [AA 인계·승인 체크리스트](./handoff-checklist.md)

## 인증·Agent 개발 기준
- [공통 인증·인가/Mock 설계](./auth-design.md) — A/B/C 간 Auth 연결 기준
- [Mock 계정·상태 Fixture](./mock-fixtures.md) — Guest/USER/ADMIN/만료/비활성
- [독립→실제 통합/E2E 검증 계획](./integration-test-plan.md) — G1~G4 게이트 및 TC-INT ID
- [Agent Skill 작성/운영 가이드](../governance/agent-skills-guide.md), [공통 Contract-first Skill](../../.agents/skills/contract-first/SKILL.md)

## 실제 구현 저장소에서 참고할 자료
- [Backend AA 인계](https://github.com/00700lsm/user-management-backend/blob/dev/docs/aa/README.md)
- [Frontend AA 인계](https://github.com/00700lsm/user-management-frontend/blob/dev/docs/aa/README.md)
- [Workspace 시작 문서](https://github.com/00700lsm/user-management-workspace/blob/dev/docs/aa/README.md)

## 운영 원칙
- 개발자 A: Auth FE+BE, B: User FE+BE, C: Permission FE+BE. 교차 배정 아님.
- `dev` 기준 기능 브랜치 → PR → 검토; `main`은 통합 검증 후 안정 기준선.
- 계약 변경은 [공통 승인 절차](../contract-governance.md)에 따라 **Contract PR 선반영**, FE/BE `contract.sha`는 승인된 SHA로 함께 업데이트.
- OpenAPI의 필드/엔드포인트는 다른 문서의 설명이나 예시보다 우선합니다. 설계 문서 간 충돌은 AA/PL이 기준 문서 수정 PR로 해결합니다.
- 이 패키지는 구현 완료 보고서가 아니라 **AA 개발 착수 기준선 초안**입니다.
