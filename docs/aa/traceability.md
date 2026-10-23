# 요구사항 → 화면 → API → 데이터 → 검증 추적표

**상태: 설계상 매핑, 실제 코드·테스트 수행 증거 미등록.** `TC-*`는 예정된 테스트 식별자입니다.

| Requirement | 화면 (UI ID) | 외부 API (openapi.yaml 기준) | 데이터 Owner | 테스트 계획 ID |
|---|---|---|---|---|
| REQ-AUTH-001 | UI-AUTH-001 | POST /auth/login | AUTH_CREDENTIAL(Auth), USER(User) 참조 | TC-AUTH-001 |
| REQ-AUTH-002 | 공통 헤더 로그아웃 — 보호 화면 공통(예: UI-USER-002, UI-AUTH-002) | POST /auth/logout | Auth | TC-AUTH-002 |
| REQ-AUTH-003 | UI-AUTH-002 | POST /auth/password/change | AUTH_CREDENTIAL(Auth) | TC-AUTH-003 |
| REQ-USER-001 | UI-USER-001 | POST /users/signup | USER(User), AUTH_CREDENTIAL(Auth), USER_ROLE(Permission) | TC-USER-001 |
| REQ-USER-002 | UI-USER-002 | GET/PATCH /users/me | USER(User) | TC-USER-002 |
| REQ-USER-003 | UI-USER-003 | GET /admin/users | USER(User) | TC-USER-003 |
| REQ-USER-004 | UI-USER-003/004 | POST /admin/users, GET/PATCH /admin/users/{id} | USER(User), AUTH_CREDENTIAL(Auth) 가능 | TC-USER-004 |
| REQ-USER-005 | UI-USER-004 | PATCH /admin/users/{id}/status | USER(User) | TC-USER-005 |
| REQ-PERM-001 | UI-PERM-001 | GET /admin/roles | ROLE(Permission) | TC-PERM-001 |
| REQ-PERM-002 | UI-PERM-002 | GET/PUT /admin/users/{id}/roles | USER_ROLE(Permission), USER(User) 참조 | TC-PERM-002 |

모든 경로는 `servers.url=/api` 접두사를 고려합니다. 화면 ID/route 정본은 [UI 구조](../ui-structure.md)를 참고합니다.

## 변경 영향 추적 방법
1. 바뀌는 REQ/화면/API/Entity/업무 규칙을 확인합니다.
2. 이 표에서 연결된 담당(A/B/C)과 테스트를 확인합니다.
3. API 계약 변경이면 Contract Repository PR을 선행합니다.
4. FE/BE PR에 Requirement ID, 연결 API, Contract SHA, 실행 테스트 증거를 기재합니다.
5. 신규 기능은 새로운 REQ/UI/TC ID를 등록하고 링크를 추가합니다. 실제 파일/PR 링크가 생기기 전까지 '구현 완료'로 표시하지 않습니다.
