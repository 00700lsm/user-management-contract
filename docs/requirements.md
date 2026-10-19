# 요구사항 기준선 (AA 초안)

상태: Draft — 팀 합의 후 Baseline으로 전환합니다.

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

## 보류·결정 필요
- Access Token의 만료/갱신/저장 정책 및 로그아웃 무효화 방식
- 회원가입 시 User ↔ Auth ↔ Permission 내부 협업 형태와 트랜잭션/실패 보상
- 실제 물리 서비스/DB 분리 범위 (PoC는 논리 경계 우선)
- 비밀번호 정책, 계정잠금, 관리자의 초기 비밀번호 발급 정책
- 회원탈퇴를 본인도 수행할지 여부 (현재 API는 관리자 상태 변경만 정의)

미정 항목은 개발자가 임의로 확정하지 않고 변경제안/결정 기록으로 확정합니다.
