# AA 설계 결정 기록 — PoC 기준선

**상태: DEC-001~011은 2026-10-20 PoC 진행 기준으로 Accepted**(사용자 승인에 따라 추천안으로 확정). **DEC-012는 2026-10-25 AA/PL 리뷰(Contract PR #23)에서 이견 없음 확인 후 Accepted. DEC-013은 판정 규칙 보완 후 AA/PL 재검토 대기(Proposed).** **문서 승인 ≠ 기능 구현·실제 테스트 완료**입니다. 상용 서비스/실제 개인정보 운영에는 별도 보안·법무 검토가 필요합니다.

| ID | 상태 | 확정한 PoC 기준 | 확인·검증/영향 |
|---|---|---|---|
| DEC-001 | Accepted | Bearer JWT Access Token 15분; Refresh Token 없음; FE는 `sessionStorage`에 보관(새 탭/브라우저 종료 시 재로그인), 401 시 삭제·로그인 이동; Logout 시 Token `jti`를 만료까지 서버 측 폐기 목록에 추가 | 실제 Logout 폐기 목록·JWT 서명/검증 구현 필요. `sessionStorage`는 XSS에 노출될 수 있어 CSP/입력보안 검토 |
| DEC-002 | Accepted | 모듈형 단일 Backend/단일 H2 DB에서 User 가입 + Auth 자격증명 + Permission 기본 USER를 서비스 간 협업 및 **단일 트랜잭션**으로 처리; 모든 단계 실패 시 Rollback | REQ-USER-001, 가입 오류/재시도 테스트 |
| DEC-003 | Accepted | **하나의 Spring Boot 실행 앱**, Auth/User/Permission 논리 모듈 3개 + 한 개 DB; 3개 물리 서비스/Microservices는 PoC 범위 제외 | 모듈 데이터 Owner/호출 경계 유지 |
| DEC-004 | Accepted | React + TypeScript + Vite, React Router, TanStack Query, **CSS Modules + Frontend `design.md` 토큰**, 공통 Shared UI; 이번 단계에서 무거운 UI 라이브러리 추가하지 않음 | UI/IA는 Contract, 상세 비주얼은 Frontend design.md |
| DEC-005 | Accepted | `ACTIVE` 사용자만 로그인 및 보호 API 접근 가능; `INACTIVE`/ `WITHDRAWN`은 접근 차단; INACTIVE→ACTIVE는 관리자 상태 변경으로 복구 가능; WITHDRAWN은 PoC에서 되돌리지 않음/물리삭제 하지 않음 | 현재 세션 중 상태 변경도 보호 API에서 재검증. 실제 개인정보 보존·파기 규정은 PoC 외 |
| DEC-006 | Accepted | 관리자의 사용자 등록은 기존 SignupRequest의 명시적 `password`를 사용. 자동 임시 비밀번호·비밀번호 이메일 발송 기능 없음; 관리자에게 입력값 재표시/로그 출력 금지, 별도 안전 채널로 전달 | 초기 비밀번호 강제 변경 UX·API 추가는 PoC 범위 제외 |
| DEC-007 | Accepted | 비밀번호 길이 최소 12글자, UTF-8 인코딩 최대 72바이트(Bcrypt 절단 방지), 확인 정책은 FE 안내/BE 검증; BCrypt 단방향 해시, 원문 저장/로그 금지 | 기존 OpenAPI의 password 최소값·오류코드는 계약 PR로 향후 보강 가능 |
| DEC-008 | Accepted | 사용자 **목록에는 Role 컬럼을 표시하지 않음**. 관리자 상세→`/admin/users/:id/roles` 이동 후 Permission API 조회 | 현재 User 응답 Schema 그대로 |
| DEC-009 | Accepted | JWT `sub`=문자열 표현 User ID, `roles`=Role 코드 배열(UI 표시용). Backend는 JWT 서명/만료/`jti` 검증 후 **DB에서 상태·현재 Role을 재조회**하여 인가; Role 변경 다음 보호 API 호출부터 반영. 403 후 FE는 권한 UI 갱신/재로그인 안내 | `GET /auth/me` 추가하지 않음. 브라우저 JWT Payload만 보고 권한을 신뢰하지 않음 |
| DEC-010 | Accepted | FE Mock Auth Adapter + MSW는 **development/test 전용**. BE Auth Fixture/격리 H2는 test Profile에만. CI/E2E의 실제 Auth 검증 필수; 운영에는 Mock/고정 테스트 비밀값/인증 우회 없음 | G1~G4 단계별 테스트 증거 |
| DEC-011 | Accepted | 개발자별 **H2 Embedded File** 로컬 DB, 테스트별 H2 Memory DB; **Flyway SQL로 Schema/공통 테스트 Seed 재현**; 실제 DB 파일 Git 제외. PostgreSQL/공유 DB는 PoC 필수 아님 | schema migration·개발 프로필·CI 검증 |
| DEC-012 | Accepted | `ApiError.code` 표준값: `UNAUTHORIZED`(401), `FORBIDDEN`(403), `INVALID_CREDENTIALS`(401, 로그인 실패는 원인 구분 없이 단일 코드·문구 — 계정 상태 노출 방지), `INVALID_OLD_PASSWORD`(400), `PASSWORD_POLICY_VIOLATION`(400), `VALIDATION_FAILED`(400), `NOT_FOUND`(404, 매핑되지 않은 경로 등 공통 미발견 — 도메인별 대상 미발견은 각 DEC의 세부 코드 사용, 예: DEC-014 `USER_NOT_FOUND`). 로그인 입력 누락도 `INVALID_CREDENTIALS` 401 | `openapi.yaml` `ApiError.code` 설명. FE는 `code`로 문구 매핑. 타 도메인 코드 추가는 별도 PR |
| DEC-013 | Proposed | 비밀번호 변경 성공 시 **해당 사용자의 기존 Access Token 전체 무효화**(변경 요청 토큰 포함). 판정: 로그인 시 그 시점의 `auth_credential.password_updated_at`(epoch **밀리초**)을 JWT claim `pwv`로 발급하고, 보호 요청마다 `pwv`가 DB 현재값과 **정확히 일치**할 때만 허용(누락·불일치 401). 발급 시각(`iat`) 비교는 사용하지 않음 — 변경 시각과 같은 초에 발급된 기존 토큰도 거부되고, 변경 후 재로그인 토큰은 즉시 허용. FE는 204 후 안내 → 세션 삭제 → 재로그인. 기존 비밀번호 불일치는 400 `INVALID_OLD_PASSWORD` | 추가 테이블·스키마 변경 없음(기존 컬럼을 자격증명 버전으로 사용, 보호 요청마다 하는 DB 재조회에 포함). 로그아웃 `jti` 폐기(DEC-001)와 별개. **검증 계획**: ① 로그인 직후 대기 없이 비밀번호 변경 → 변경에 쓴 토큰 401 ② 변경 전 다른 로그인 토큰 401 ③ 변경 직후 같은 초 재로그인 토큰 허용 ④ `pwv` 누락·변조 토큰 401. 최초 구현(Backend #8)의 초 단위 `iat` 비교 결함은 별도 Backend 수정 PR로 교정 |

| DEC-014 | Proposed | User 오류 응답: 로그인 ID 중복 409 `DUPLICATE_LOGIN_ID`, 이메일 중복 409 `DUPLICATE_EMAIL`(가입·관리자 등록·내 정보/관리자 수정 공통, 둘 다 중복이면 `DUPLICATE_LOGIN_ID` 우선); 대상 사용자 없음 404 `USER_NOT_FOUND`; WITHDRAWN 사용자의 상태 변경 409 `INVALID_STATUS_TRANSITION`; 현재와 같은 상태로의 변경은 200(변경 없음); 형식 오류·빈 수정 요청은 400 `VALIDATION_FAILED`(DEC-012 재사용). 문자열 길이는 V1 스키마와 동일(loginId 80, email 254, name 120) | 가입 중복 응답은 계정 존재 여부를 노출하지만 REQ-USER-001(중복 거부)상 불가피하며 로그인 실패 비노출(DEC-012)과 범위가 다름. FE는 `code`로 입력칸별 오류 표시 |

## 우선순위와 구현 전제

1. 공통 요구사항·OpenAPI 정본은 `openapi.yaml`, 논리 ERD는 `docs/db-design.md`, FE 화면 IA는 `docs/ui-structure.md`입니다.
2. Backend·Frontend의 `contract.sha`가 **같은 승인된 Git SHA**를 가리켜야 합니다. 새 API를 임의 도입하지 않습니다.
3. 구현 시작 단계: Spring Boot + H2/Flyway Skeleton, React/Vite/Router/Query/CSS token Skeleton, 개발 전용 Mock·보안 Test Fixture 기반.
4. 도메인별 실제 구현 A(Auth), B(User), C(Permission)은 별도 요구사항/PR 테스트로 완료를 증빙합니다.
5. 로그아웃/Role 변경/가입 데이터 정합성은 문서 확정만으로 동작하지 않습니다. 해당 구현 및 G3/G4를 통과해야 완료입니다.
6. 별도 상용 요구로 발생할 수 있는 사항: 운영 DB(PostgreSQL), 실제 개인정보 보호·보존·파기, 토큰 쿠키 기반 저장/CSP 강화, 운영 접근 기록, Secret 회전, CI 보안 심사.

## 변경 프로세스

정책 변경은 AA/PL+관련 FE/BE 담당자의 리뷰를 받는 Contract 설계 PR로 수정합니다. API 요청·응답·HTTP 상태/경로를 변경하는 경우 `openapi.yaml` Contract PR을 먼저 승인하고, 해당 SHA를 FE/BE에 반영합니다. 이 문서의 Accepted 결정은 구현팀의 무제한 변경 권한이 아닙니다.
