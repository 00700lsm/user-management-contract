# Mock 인증 Fixture 공통 기준 (PoC 테스트 계획)

Mock은 개발·테스트용 시나리오일 뿐 실제 인증을 대체하지 않습니다. 비밀번호·실제 토큰·서명 비밀키는 Git에 저장하지 않습니다.

| Fixture ID | Role | 계정 상태 | 테스트 목적 |
|---|---|---|---|
| FIX-GUEST | 없음 | 미인증 | 보호 API 401, 로그인 유도 |
| FIX-USER | USER | ACTIVE | 내 정보 허용, 관리자 API 403 |
| FIX-ADMIN | ADMIN | ACTIVE | 관리자 업무 정상 |
| FIX-EXPIRED | USER | ACTIVE | 만료 토큰 401 |
| FIX-INACTIVE | USER | INACTIVE | ACTIVE 외 보호 API 차단 (DEC-005) |
| FIX-WITHDRAWN | USER | WITHDRAWN | WITHDRAWN 보호 API 차단 및 복구 제외 (DEC-005) |

## FE/BE 규칙
- HTTP Mock Response는 `contract.sha`에 고정된 OpenAPI Schema와 일치해야 합니다.
- 로그인 API 응답에 별도 Role 필드는 없고 `GET /auth/me`도 없습니다. DEC-009의 JWT `roles` Claim은 UI 참고용이며 Backend는 DB 최신 Role로 판단합니다. Mock에서 실제 서명 토큰으로 오해할 데이터를 만들지 않습니다.
- FE Mock Auth 상태와 실제 API 응답을 구분합니다. Mock/Real Auth Adapter 인터페이스는 공통으로 합의합니다.
- BE Fixture는 격리된 테스트 환경에서 실제 인증 검증과 호환되도록 구성합니다. 운영용 인증 우회 금지.
- Auth A, User B, Permission C는 사용자 식별자/Role/상태를 공통 Fixture 기준으로 검증합니다.
- Accepted 정책은 `docs/aa/decisions.md`를 따르며 아직 구현되지 않은 실제 JWT/Auth 통합을 Mock 검증 성공으로 표현하지 않습니다.

참고: [Auth 설계](./auth-design.md), [통합 테스트](./integration-test-plan.md).
