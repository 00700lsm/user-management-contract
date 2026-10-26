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

## TC-USER 검증 시나리오 (DEC-014, Proposed)

설계상 기대 결과입니다. 실행 증거(G2 API 테스트, G3/G4 실연동)는 각 User 구현 PR에 따로 기록합니다.

| 테스트 | 시나리오 | 기대 결과 |
|---|---|---|
| TC-USER-001 | 정상 가입 | 201 + User(`ACTIVE`). 자격증명과 기본 USER Role이 함께 생성됨 |
| TC-USER-001 | 길이 경계: loginId 80자·name 120자·email 254자 / loginId 81자·name 121자·email 255자 / 빈 loginId·name | 경계값 201, 초과·빈 값 400 `VALIDATION_FAILED` |
| TC-USER-001 | 비밀번호 11자 | 400 `PASSWORD_POLICY_VIOLATION`, 사용자 미생성 |
| TC-USER-001 | loginId 중복 / 이메일 중복 / 둘 다 중복 | 409 `DUPLICATE_LOGIN_ID` / `DUPLICATE_EMAIL` / `DUPLICATE_LOGIN_ID` |
| TC-USER-001 | 같은 loginId로 동시 가입 2건 | 1건 201, 1건 409 `DUPLICATE_LOGIN_ID`(UNIQUE 충돌 변환). 남는 부분 데이터 없음 |
| TC-USER-001 | 자격증명 또는 Role 생성 단계 실패 | 전체 Rollback(DEC-002), 사용자 미생성 |
| TC-USER-002 | 토큰 없음·무효로 GET/PATCH `/users/me` | 401 `UNAUTHORIZED` |
| TC-USER-002 | PATCH `{}` / `{"role":"ADMIN"}` / `{"name":"새 이름","status":"INACTIVE"}` | 400 `VALIDATION_FAILED`, 아무것도 변경되지 않음 |
| TC-USER-002 | 이름만 / 이메일만 변경 | 200, 보낸 필드만 변경 |
| TC-USER-002 | 본인의 현재 이메일 그대로 전송 | 200 (중복 아님) |
| TC-USER-002 | 다른 사용자의 이메일로 변경 / 두 사용자가 같은 새 이메일로 동시 변경 | 409 `DUPLICATE_EMAIL` / 1건 200, 1건 409 |
| TC-USER-003 | USER 토큰 / 토큰 없음 | 403 `FORBIDDEN` / 401 `UNAUTHORIZED` |
| TC-USER-004 | 관리자 등록: TC-USER-001의 길이·비밀번호·중복 시나리오 | 201 / 400 / 409 (가입과 같은 코드) |
| TC-USER-004 | 없는 id로 상세·수정 | 404 `USER_NOT_FOUND` |
| TC-USER-004 | 수정: 빈 객체·허용 외 필드 / 다른 사용자 이메일 / 대상 본인의 현재 이메일 | 400 `VALIDATION_FAILED` / 409 `DUPLICATE_EMAIL` / 200 |
| TC-USER-004 | USER 토큰 / 토큰 없음 | 403 `FORBIDDEN` / 401 `UNAUTHORIZED` |
| TC-USER-005 | `ACTIVE`→`INACTIVE`→`ACTIVE`, `ACTIVE`→`WITHDRAWN` | 200 |
| TC-USER-005 | 같은 상태 요청(`ACTIVE`→`ACTIVE`, `WITHDRAWN`→`WITHDRAWN`) | 200, 변경 없음 |
| TC-USER-005 | `WITHDRAWN`→`ACTIVE` / `WITHDRAWN`→`INACTIVE` | 409 `INVALID_STATUS_TRANSITION` |
| TC-USER-005 | status 누락·허용 외 값 / 없는 id | 400 `VALIDATION_FAILED` / 404 `USER_NOT_FOUND` |
| TC-USER-005 | USER 토큰 / 토큰 없음 | 403 `FORBIDDEN` / 401 `UNAUTHORIZED` |

## 변경 영향 추적 방법
1. 바뀌는 REQ/화면/API/Entity/업무 규칙을 확인합니다.
2. 이 표에서 연결된 담당(A/B/C)과 테스트를 확인합니다.
3. API 계약 변경이면 Contract Repository PR을 선행합니다.
4. FE/BE PR에 Requirement ID, 연결 API, Contract SHA, 실행 테스트 증거를 기재합니다.
5. 신규 기능은 새로운 REQ/UI/TC ID를 등록하고 링크를 추가합니다. 실제 파일/PR 링크가 생기기 전까지 '구현 완료'로 표시하지 않습니다.
