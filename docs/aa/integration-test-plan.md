# 인증 기반 병렬 개발·통합 테스트 계획 (Draft)

테스트 ID는 계획일 뿐 실행 완료 증거가 아닙니다. FE와 BE의 `contract.sha`가 동일한 승인 OpenAPI를 가리켜야 합니다.

| 게이트 | 환경 | 합격 조건 |
|---|---|---|
| G1 FE Mock | Auth 미완성 상태의 화면 개발 | Guest/USER/ADMIN, 보호 Route, 401/403 UX |
| G2 BE 격리/계약 | 격리 DB·테스트 인증 Fixture | 명세 Body/Status, 인증·권한 검증 |
| G3 Real Auth | A가 발급한 실제 Token으로 B/C API 호출 | 사용자·Role·계정 상태 일관성 |
| G4 E2E | 통합 FE+BE, Mock 비활성 | 가입→로그인→내 정보/관리자 업무 전체 연결 |

## 통합 시나리오

| 테스트 ID | 시나리오 |
|---|---|
| TC-INT-001 | Guest /me 접근 → 로그인 안내, API 401 |
| TC-INT-002 | USER 로그인 → 본인 정보 정상 조회 |
| TC-INT-003 | USER 관리자 화면/API 접근 → 차단 및 Backend 403 |
| TC-INT-004 | ADMIN 사용자 목록·상세·검색·페이징 |
| TC-INT-005 | ADMIN 사용자 Role 변경 후 재조회, 정책에 따른 세션 반영 |
| TC-INT-006 | 회원가입→로그인, User/Auth/Permission 데이터 정합성 |
| TC-INT-007 | 토큰 누락·만료·변조 → 401 |
| TC-INT-008 | 로그아웃 후 접근: 승인된 토큰 무효화 정책대로 |
| TC-INT-009 | 비활성/탈퇴 사용자: 승인된 계정 정책대로 |
| TC-INT-010 | 가입 과정 실패 시 롤백/보상 정합성 |
| TC-INT-011 | FE/BE 계약 버전 불일치 → 통합 검증 실패 |
| TC-INT-012 | 운영 빌드에 Mock Auth·테스트 비밀값 진입 불가 |

## 테스트 증거 형식
```text
TC ID / 담당:
FE SHA, BE SHA, Contract SHA:
실행 환경, Fixture ID (비밀값 제외):
실행 명령 및 결과:
CI/E2E 로그·관련 PR:
미결정 사항과 차단 요인:
```

OpenAPI 구문 검증과 TypeScript 타입 생성 성공만으로 실제 서버 계약 준수나 E2E 완료를 주장하지 않습니다.
