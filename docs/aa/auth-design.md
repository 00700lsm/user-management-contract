# 인증·인가 공통 설계 (Accepted PoC 기준)

상태: DEC-001/002/005/007/009/010은 [Accepted](./decisions.md)입니다. 정책 승인과 실제 인증 구현·통합 테스트 완료는 구별합니다. 외부 API의 요청·응답·경로는 `openapi.yaml`이 유일한 정본입니다.

## 기존 OpenAPI가 정의한 것
- `POST /auth/login`: 익명 허용; `accessToken`, `tokenType` 응답
- `POST /auth/logout`, `POST /auth/password/change`: 보호된 Auth API
- HTTP Bearer JWT 인증 방식, Role 코드 USER/ADMIN
- 인증되지 않음(401)과 인증되었으나 권한 부족(403)의 구분
- **현재 `GET /auth/me`는 없고, `GET /users/me`의 User 응답에도 Role 필드는 없음**

## 책임
- A/Auth: 로그인, 인증 토큰 발급과 검증 경계 및 Principal 규약 설계 참여
- B/User: 사용자 상태·프로필·가입. Auth의 자격증명 자체를 임의로 관리하지 않음
- C/Permission: 역할 관리와 권한 판단. User 프로필 수정 금지
- Frontend: Auth 상태 공급자(인터페이스)로 로그인 여부·Role에 따른 화면 진입을 제어하되, **Backend 권한 검사의 대체 수단으로 사용하지 않음**
- Backend: 모든 보호 API에서 공통 인증·권한 정책을 사용. 프론트가 임의로 전달한 사용자 ID/Role을 신뢰하지 않음

## 승인된 인증 컨텍스트 (DEC-001/005/009)
| 값 | 용도 | 승인된 규칙 |
|---|---|---|
| JWT `sub` | 현재 사용자 식별 | User ID의 문자열 표현 |
| JWT `roles` | USER/ADMIN UI 표시 참고 | Role 코드 배열; Backend는 **최신 DB Role을 재조회**하여 인가 |
| accountStatus | ACTIVE/INACTIVE/WITHDRAWN | 매 보호 API에서 재확인; ACTIVE만 허용 |
| FE `authenticated` | 화면 로그인 상태 | `sessionStorage` Access Token 15분, Refresh 없음, 401 시 제거 및 로그인 이동 |
| JWT `jti` | 로그아웃 토큰 폐기 | Logout 시 남은 유효기간 동안 서버 측 폐기 목록 등록 |

JWT는 승인된 정책이나 실제 발급·검증·폐기 코드의 구현 여부는 별도 테스트로 판정합니다.

`GET /auth/me` 등의 신규 API를 도입하려면 Contract PR로 요청·응답·권한과 예외 응답까지 확정한 뒤 구현합니다.

## 병렬 개발을 위한 Mock Auth 원칙
1. FE는 Guest, USER, ADMIN, 만료·비활성 상태를 **명시적인 Mock Fixture**로 선택하여 화면을 테스트합니다.
2. FE Mock과 Real Adapter는 같은 인터페이스를 사용하며, 실제 HTTP Mock 응답은 **승인된 OpenAPI 형식만** 사용합니다.
3. BE Test fixture는 개발/테스트 환경에 한정하고 공통 인증 검증과 호환되도록 구성합니다. 운영 모드에서 인증 우회 기능을 금지합니다.
4. 실제 토큰/테스트 서명키/비밀번호를 Git에 저장하지 않습니다.
5. Mock 테스트 통과만으로 실제 Auth 연동 완료로 판정하지 않습니다.

## 단계
독립 FE Mock/BE 단위 테스트 → OpenAPI 계약검증 → A가 발급한 실제 토큰으로 B/C API 검증 → Mock을 끈 E2E.

참고: [Mock Fixture](./mock-fixtures.md), [통합 테스트 계획](./integration-test-plan.md), [설계 결정 기록](./decisions.md).
