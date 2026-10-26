# 기능 상세 / 비즈니스 규칙 (PoC 기준)

요구사항 ID와 상태는 [requirements.md](../requirements.md), 네트워크 요청·응답·상태코드는 [openapi.yaml](../../openapi.yaml)을 정본으로 합니다.

## 공통 행위자와 업무 규칙
- **Guest**: 로그인, 회원가입만 가능
- **USER**: 로그인/로그아웃, 비밀번호 변경, 본인 정보 조회/수정
- **ADMIN**: USER 기능 + 사용자 목록·등록·상세·수정·상태 변경, 역할 조회·사용자 역할 변경
- 미인증은 401, 인증되었으나 권한이 없으면 403을 기본으로 합니다. 응답 상세/구현 정책은 OpenAPI와 승인된 보안 설계에 따릅니다.
- USER 상태는 `ACTIVE`, `INACTIVE`, `WITHDRAWN`; 탈퇴는 논리 상태 변경, 물리 삭제 아님.
- 사용자 계정·자격증명·권한 데이터는 각각 User/Auth/Permission 도메인이 소유합니다.

## Auth — 개발자 A

| 요구 ID | 동작 및 조건 | 결과 / 검증 |
|---|---|---|
| REQ-AUTH-001 | `loginId` + `password`로 로그인; 비정상 자격 증명 거부 | 성공 시 `accessToken`, `tokenType`; 실패(자격증명 오류·INACTIVE/WITHDRAWN·입력 누락) 시 401 `INVALID_CREDENTIALS` 단일 응답(DEC-012) |
| REQ-AUTH-002 | 로그인 상태에서 로그아웃 요청 | 성공 시 204. DEC-001에 따라 Access Token JTI를 만료까지 서버 폐기 목록에 등록 |
| REQ-AUTH-003 | 현재 비밀번호 + 새 비밀번호를 제출 | 성공 시 204 후 해당 사용자의 기존 토큰 전체 무효화(DEC-013); 기존 비밀번호 불일치 400 `INVALID_OLD_PASSWORD`, 정책 위반 400 `PASSWORD_POLICY_VIOLATION`(DEC-007/012) |

Auth는 USER 프로필을 직접 수정하지 않습니다. DEC-005에 따라 ACTIVE만 로그인/보호 API 접근을 허용하고 INACTIVE/WITHDRAWN은 차단합니다. 결정은 승인됐지만 JWT/인가 구현은 아직 완료되지 않았습니다.

## User — 개발자 B

| 요구 ID | 동작 및 조건 | 결과 / 검증 |
|---|---|---|
| REQ-USER-001 | Guest 회원가입. `loginId`·이메일 중복 거부; 필수값 확인 | 201 + User 반환, 중복 409 `DUPLICATE_LOGIN_ID`/`DUPLICATE_EMAIL`(DEC-014). DEC-002: Auth 자격증명과 기본 USER 권한까지 단일 DB 트랜잭션, 실패 시 Rollback |
| REQ-USER-002 | USER 본인 정보 조회/수정. 수정 허용 필드는 이름·이메일 | 200 + User 반환; ID/상태/Role 직접 변경 금지. 이메일 중복 409 `DUPLICATE_EMAIL`(본인 현재 이메일은 허용), 빈 객체·허용 외 필드 400 `VALIDATION_FAILED`(DEC-014) |
| REQ-USER-003 | ADMIN 사용자 목록. `keyword`는 이름 또는 이메일 OR 검색, 상태 필터 | `page` 0-based, `size` 기본 20, 최대 100; `UserPage.items/page/size/total` |
| REQ-USER-004 | ADMIN 사용자 생성·상세 조회·이름/이메일 변경 | 201/200; 등록 중복 409 `DUPLICATE_LOGIN_ID`/`DUPLICATE_EMAIL`, 수정 중복 409 `DUPLICATE_EMAIL`, 대상 없음 404 `USER_NOT_FOUND`(DEC-014); DEC-006에 따라 기존 SignupRequest의 명시적 초기 비밀번호를 입력, 자동 생성/이메일 발송 기능 없음 |
| REQ-USER-005 | ADMIN 사용자 상태 변경 | `ACTIVE/INACTIVE/WITHDRAWN`, 200 + User. INACTIVE→ACTIVE 복구 가능, WITHDRAWN 복구 및 물리 삭제는 PoC 제외(DEC-005). 같은 상태 요청은 200(변경 없음, WITHDRAWN→WITHDRAWN 포함), WITHDRAWN→ACTIVE/INACTIVE 409 `INVALID_STATUS_TRANSITION`, 대상 없음 404 `USER_NOT_FOUND`(DEC-014) |

실제 응답 코드가 OpenAPI 초안에 정의되지 않은 예외는 개발자가 임의로 도입하지 말고 계약 변경 PR을 제출합니다.

## Permission — 개발자 C

| 요구 ID | 동작 및 조건 | 결과 / 검증 |
|---|---|---|
| REQ-PERM-001 | ADMIN이 역할 목록 조회 | 초기 Role `USER`, `ADMIN`; GET `/admin/roles` |
| REQ-PERM-002 | ADMIN이 특정 사용자의 Role 조회/교체 | GET/PUT `/admin/users/{id}/roles`; 입력 Role 코드 중복 불가, 최소 1개 |

Permission은 USER 프로필이나 계정 상태를 직접 수정하지 않습니다.

## 교차 도메인 연결 — 확정된 원칙과 개발 구현 책임
1. DEC-002/003: User 가입 시 Auth 자격증명과 Permission 기본 USER Role 부여를 **단일 Spring Boot 앱의 서비스 협업 및 단일 DB 트랜잭션**으로 처리합니다. 내부 Java 인터페이스 세부 설계는 담당자가 공동 검토합니다.
2. DEC-005/009: 보호 API마다 Backend가 현재 User 상태·Permission Role을 DB에서 재검증합니다. JWT Role은 UI 표시용이며 인가의 단독 근거가 아닙니다.
3. DEC-008: 사용자 상세에서 `/admin/users/:id/roles`로 이동하고 Permission API로 Role을 조회합니다. 사용자 목록에는 Role 컬럼을 넣지 않습니다.
4. 물리 MSA와 분산 트랜잭션은 PoC 범위 밖입니다. 도입하려면 별도 AA/Contract 설계가 필요합니다.

현재 `openapi.yaml`은 **외부 FE↔BE 계약**이며 서비스 간 내부 계약을 확정한 것은 아닙니다.

## 완료 증빙
REQ ID별 정상/비정상/접근권한 테스트와 관련 UI/API/PR 링크를 [추적표](./traceability.md)에 연결합니다.
