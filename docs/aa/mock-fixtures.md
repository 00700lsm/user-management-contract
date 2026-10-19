# 개발·테스트용 인증 Fixture 규약 (설계 예시)

여기에 정의하는 것은 **시나리오 데이터와 기대 행위**입니다. 실제 Access Token/JWT Secret/실제 비밀번호·개인정보는 보관하지 않습니다.

| Fixture ID | 논리 사용자 | Role | User 상태 | 사용 목적 |
|---|---|---|---|---|
| FIX-GUEST | 미인증 | 없음 | N/A | 로그인/가입 및 보호 자원 401 |
| FIX-USER | test-user (임의 테스트 식별자) | USER | ACTIVE | 내 정보 접근, 관리자 403 |
| FIX-ADMIN | test-admin (임의 테스트 식별자) | ADMIN | ACTIVE | 관리자 UI/API 정상 |
| FIX-EXPIRED | test-expired | USER | ACTIVE | 만료 Token 401 |
| FIX-INACTIVE | test-inactive | USER | INACTIVE | 상태 기반 인증 정책 검증 |
| FIX-WITHDRAWN | test-withdrawn | USER | WITHDRAWN | 탈퇴 정책 검증 |

## 계약을 바꾸지 않는 방법
- 화면이 Role을 알아야 하는 경우 **Mock Auth 상태 내부**에만 `roleCodes`를 둡니다. 로그인 HTTP 응답 `TokenResponse`에 Role 필드를 임의 추가하지 않습니다.
- `GET /auth/me` 등 **현재 없는 API를 Mock 서버만 만들어 Frontend에서 실사용처럼 호출하지 않습니다**. 계약 변경 승인 후 추가합니다.
- 기존 `GET /users/me` 응답은 User Schema를 사용하며 Role을 포함하지 않습니다.
- Auth 검증 전용 fixture는 **테스트 프로파일·테스트 키/격리 환경**에서만 사용합니다. 임의로 인증을 우회하는 운영 기능을 만들지 않습니다.

## 구현 단계 체크
- [ ] 테스트 계정/Role·상태/생성순서를 담당 A/B/C 합의
- [ ] Auth Principal 식별/Role 전달 방식 결정 (DEC-009)
- [ ] FE Mock Adapter 교체 방식/운영 비활성 검증 (DEC-010)
- [ ] BE Test fixture 생성·실제 서명/검증 방식 결정 (DEC-010)
- [ ] 격리된 E2E/CI에서만 Test Secrets 공급
- [ ] Fixture 정리·테스트 간 격리 및 비밀정보 로그 마스킹

Mock은 **합의된 계약에 맞춰 독립 개발을 가능하게 하는 도구**일 뿐 실서비스 인증을 대신하지 않습니다.
