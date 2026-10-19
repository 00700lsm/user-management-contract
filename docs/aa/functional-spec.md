# 기능 상세 / 비즈니스 규칙 (AA 초안)

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
| REQ-AUTH-001 | `loginId` + `password`로 로그인; 비정상 자격 증명 거부 | 성공 시 `accessToken`, `tokenType`; 실패 시 표준 API 오류 |
| REQ-AUTH-002 | 로그인 상태에서 로그아웃 요청 | 계약상 성공 시 204. 로그아웃 후 토큰 무효화 방식은 **DEC-001 미결정** |
| REQ-AUTH-003 | 현재 비밀번호 + 새 비밀번호를 제출 | 확인/검증 성공 시 204; 실패 시 400 등 계약 기반 |

Auth는 USER 프로필을 직접 수정하지 않습니다. 비활성/탈퇴 계정의 인증 처리 정책은 DEC-001/DEC-005 결정 후 확정합니다.

## User — 개발자 B

| 요구 ID | 동작 및 조건 | 결과 / 검증 |
|---|---|---|
| REQ-USER-001 | Guest 회원가입. `loginId`·이메일 중복 거부; 필수값 확인 | 201 + User 반환, 중복 409. Auth 자격증명 및 USER 권한 생성의 실패 정합성은 **DEC-002** |
| REQ-USER-002 | USER 본인 정보 조회/수정. 수정 허용 필드는 이름·이메일 | 200 + User 반환; ID/상태/Role 직접 변경 금지 |
| REQ-USER-003 | ADMIN 사용자 목록. `keyword`는 이름 또는 이메일 OR 검색, 상태 필터 | `page` 0-based, `size` 기본 20, 최대 100; `UserPage.items/page/size/total` |
| REQ-USER-004 | ADMIN 사용자 생성·상세 조회·이름/이메일 변경 | 201/200; 이메일 중복 및 관리자가 부여할 초기 비밀번호 정책은 **DEC-006** |
| REQ-USER-005 | ADMIN 사용자 상태 변경 | `ACTIVE/INACTIVE/WITHDRAWN`, 200 + User. 이력/복구 가능성은 **DEC-005** |

실제 응답 코드가 OpenAPI 초안에 정의되지 않은 예외는 개발자가 임의로 도입하지 말고 계약 변경 PR을 제출합니다.

## Permission — 개발자 C

| 요구 ID | 동작 및 조건 | 결과 / 검증 |
|---|---|---|
| REQ-PERM-001 | ADMIN이 역할 목록 조회 | 초기 Role `USER`, `ADMIN`; GET `/admin/roles` |
| REQ-PERM-002 | ADMIN이 특정 사용자의 Role 조회/교체 | GET/PUT `/admin/users/{id}/roles`; 입력 Role 코드 중복 불가, 최소 1개 |

Permission은 USER 프로필이나 계정 상태를 직접 수정하지 않습니다.

## 교차 도메인 연결 — AA 협의 필요
1. 회원가입(User)이 Auth 자격증명 생성과 Permission 기본 권한 부여를 호출하는 내부 협업 방식
2. Auth가 User 상태/Permission Role을 확인하는 방법과 갱신 반영 시점
3. 관리자 상세(User)에서 Permission 화면으로 이동할 때 사용자 ID/권한 정보 전달
4. 물리 MSA일 경우 내부 API 계약·오류 복구·데이터 정합성

현재 `openapi.yaml`은 **외부 FE↔BE 계약**이며 서비스 간 내부 계약을 확정한 것은 아닙니다.

## 완료 증빙
REQ ID별 정상/비정상/접근권한 테스트와 관련 UI/API/PR 링크를 [추적표](./traceability.md)에 연결합니다.
