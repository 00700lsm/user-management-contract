# FE·BE 인증 연동 / E2E 검증 계획 (AA Draft)

테스트 ID는 **계획 식별자**이며 실제 실행 증거가 아닙니다. 대상 빌드는 동일하게 승인된 `Contract SHA`를 사용합니다.

## 단계별 게이트

| 단계 | 개발 독립성 | 실행 방법 | 통과 조건 |
|---|---|---|---|
| G1 Mock UI | A 미구현이어도 B/C 화면 개발 가능 | Auth 상태/HTTP 응답 Mock(예: MSW) | Guest/USER/ADMIN·로딩/실패·보호 Route |
| G2 BE 단위/Contract | 서비스 런타임 연계 없이 각 도메인 테스트 | 격리 DB와 Test-only 인증 fixture, 명세 응답 검증 | 200·201·204 및 401·403·409 등 계약상 사례 |
| G3 실제 Auth 연결 | Auth/BE 통합 환경 필요 | A 로그인 결과를 B/C 요청에 사용 | 토큰 검증, 현재 User/Role, 계정 상태 일치 |
| G4 통합 E2E | FE+BE+데이터 준비 완료 | 브라우저 E2E(예: Playwright) | 사용자 흐름/권한/데이터 일관성, Mock 완전 비활성 |

## 최소 테스트 매트릭스

| TC ID | 행위 | 기대 |
|---|---|---|
| TC-INT-001 | Guest가 /me 접근 | Login 이동(화면), API 미인증 401 |
| TC-INT-002 | USER 로그인 → /me | 200 및 본인 정보; 다른 사용자 정보 임의 노출 금지 |
| TC-INT-003 | USER가 관리자 사용자·권한 API 호출 | 403 및 화면 접근 차단 |
| TC-INT-004 | ADMIN 로그인 → 사용자 목록/상세 | 정상 검색·페이징·상세 |
| TC-INT-005 | ADMIN이 USER Role 변경 | 재조회 일치; 현재 세션 반영 시점은 승인 정책대로 |
| TC-INT-006 | Guest 회원가입 → 신규 계정 로그인 | User·Auth·Permission 생성 정합성 |
| TC-INT-007 | 만료/변조/누락 Token | 401, Refresh/재로그인 UX는 승인 정책대로 |
| TC-INT-008 | 로그아웃 후 보호 API 재접근 | DEC-001 승인 정책에 따라 유효성/재접근 검증 |
| TC-INT-009 | INACTIVE / WITHDRAWN 사용자 로그인·보호 API | DEC-005 승인 정책에 따른 허용/차단 |
| TC-INT-010 | 가입/권한 할당 중간 실패 유발 | DEC-002 승인 정책에 따라 롤백/보상·중복 생성 방지 |
| TC-INT-011 | FE와 BE 계약 SHA 다름 | 릴리스/통합 검사 실패, 버전 차이 명시 |
| TC-INT-012 | 운영 모드에서 Mock Auth 사용 시도 | Mock Adapter·Test secret·테스트 UI 진입 불가 |

## 실행 시 필수 준비
- 동일 `Contract SHA`를 명시한 FE/BE Commit, 서버 실행 URL 및 테스트 대상 환경 기록
- Fixture: guest/user/admin/expired/inactive/withdrawn (자세한 값은 [Mock Fixture](./mock-fixtures.md))
- 격리 테스트 DB, 비밀값은 CI Secrets/런타임 환경변수. 실제 개인정보/운영 토큰 재사용 금지
- API 응답 Schemas 외에 실제 권한·세션 수명·User 상태/Role 정합성 검증
- 브라우저 테스트는 UI Route부터 시작하되 401/403 Backend API 결과도 함께 확인

## 증거 남기는 형식
```text
TC ID:
시나리오 / 성공·실패:
환경 및 FE SHA / BE SHA / Contract SHA:
사용 Fixture (비밀값 제외):
실행 명령 및 결과:
PR / 테스트 결과 링크:
해결되지 않은 불일치와 DEC 번호:
```

G1이나 타입 생성만으로 통합 완료로 표시하지 않습니다. 서버 런타임, Mock 환경, E2E 도구는 기술 스택 확정 후 실제 코드와 CI에 연결합니다.
