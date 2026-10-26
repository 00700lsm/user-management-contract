# 요구사항 기준선 (PoC)

상태: 기능 범위는 PoC 설계 기준이며 DEC-001~013은 [Accepted](./aa/decisions.md)입니다. 실제 구현과 테스트 완료 여부는 별개입니다.

| ID | 도메인 | 기능 / 완료 조건 |
|---|---|---|
| REQ-AUTH-001 | Auth | 로그인 ID와 비밀번호로 로그인한다. 성공 시 Access Token을 제공하고 실패 시 표준 오류를 응답한다. |
| REQ-AUTH-002 | Auth | 로그인한 사용자는 로그아웃할 수 있다. |
| REQ-AUTH-003 | Auth | 본인 확인 후 비밀번호를 변경할 수 있다. |
| REQ-USER-001 | User | 회원가입한다. 로그인 ID/이메일 중복을 거부하고 신규 사용자의 기본 권한은 USER이다. |
| REQ-USER-002 | User | 로그인한 사용자가 본인 정보를 조회·수정할 수 있다. |
| REQ-USER-003 | User | ADMIN이 사용자 목록을 검색한다. 이름 또는 이메일 OR 검색, 상태 필터, 기본 20건 페이지를 제공한다. |
| REQ-USER-004 | User | ADMIN이 사용자를 등록·상세 조회·정보 수정할 수 있다. |
| REQ-USER-005 | User | ADMIN이 상태를 ACTIVE / INACTIVE / WITHDRAWN으로 변경한다. 탈퇴는 물리 삭제하지 않는다. |
| REQ-PERM-001 | Permission | ADMIN이 사용 가능한 Role 목록을 조회한다. 초기 Role은 USER / ADMIN이다. |
| REQ-PERM-002 | Permission | ADMIN이 특정 사용자의 Role을 조회·변경할 수 있다. |

## 공통 완료 기준
1. 해당 화면과 API가 문서에 정의된 입력/출력에 일치한다.
2. ADMIN API는 일반 사용자에게 403을 반환한다.
3. 비정상 입력/중복/미인증 상태에 대한 처리가 있다.
4. BE 테스트 + FE 주요 흐름 테스트 + FE/BE 통합 테스트 근거가 남는다.
5. 변경은 관련 Requirement ID와 Contract SHA를 PR에 기록한다.

## 확정된 PoC 설계와 범위 밖 항목
- JWT 15분/Refresh 없음/sessionStorage 및 로그아웃 시 JTI 폐기: DEC-001.
- 회원가입 User/Auth/Permission 데이터 생성은 단일 DB 트랜잭션: DEC-002.
- 단일 Spring Boot 실행 앱 및 로컬 H2/Flyway: DEC-003/011.
- 비밀번호 최소 12글자·UTF-8 최대 72바이트 및 BCrypt: DEC-007. 관리자 등록 시 명시적인 초기 비밀번호: DEC-006.
- ACTIVE 사용자만 접근 가능하며 WITHDRAWN 복구는 PoC에서 제외: DEC-005.
- 표준 `ApiError.code`(로그인 실패는 원인 구분 없이 `INVALID_CREDENTIALS`): DEC-012. 비밀번호 변경 시 기존 토큰 전체 무효화: DEC-013.
- 별도 계정 잠금 정책·셀프 탈퇴 API·실제 개인정보 보존/파기 정책은 **PoC에 정의되지 않았습니다**. 필요한 경우 별도 요구와 Contract PR을 통해 합의합니다.

주의: Accepted 정책이 `openapi.yaml`의 세부 Schema 검증 항목에 아직 모두 인코딩됐다는 뜻은 아닙니다. 실제 계약 변경은 선행 Contract PR에서 승인해야 합니다.
