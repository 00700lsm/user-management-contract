# AA 설계 결정 기록 (ADR-lite)

아래는 **정의되지 않은 사항**입니다. 개발자가 스스로 확정하거나 아래 제안을 확정된 구현 요구로 간주하지 않습니다. 담당자·AA/PL이 합의 후 해당 정본을 수정해야 합니다.

| ID | 상태 | 결정이 필요한 사항 | 영향 |
|---|---|---|---|
| DEC-001 | Open | JWT 수명·갱신·브라우저 저장 및 로그아웃 토큰 무효화 방식 | Auth, FE App, 보안/테스트 |
| DEC-002 | Open | 회원가입 시 User/Auth/Permission 생성 순서, 트랜잭션/보상·롤백 | User/Auth/Permission, DB |
| DEC-003 | Open | Backend 물리 구성: 모듈형 단일 앱 vs 3개 서비스, DB 분리 여부, 내부 계약 | 아키텍처, 빌드/배포 |
| DEC-004 | Open | React UI 라이브러리/디자인 토큰/공통 컴포넌트 책임 및 반응형 기준 | 전체 FE |
| DEC-005 | Open | INACTIVE/WITHDRAWN 로그인 정책, 탈퇴 이력·개인정보 보존/마스킹, 재활성화 | Auth, User, UI |
| DEC-006 | Open | 관리자 사용자 생성 시 초기 비밀번호 전달·강제 변경 규칙 | User, Auth, 관리자 UI |
| DEC-007 | Open | Password 정책 및 비밀번호 변경 오류 응답의 구체화 | Auth, 계약 |
| DEC-008 | Open | 사용자 목록 Role 표시 여부. 현재 User 응답에 Role이 없어 추가 조회/계약 개정 필요 | User 화면, Permission API |
| DEC-009 | Open | 인증 Principal의 userId/Role/상태 확인 방법, Role 변경 반영 시점, /auth/me 도입 여부 | Auth/User/Permission, FE Route Guard, OpenAPI |
| DEC-010 | Open | 공통 FE Mock/Real Auth 경계, BE 테스트 인증 Fixture, 운영에서 Mock 비활성화 방식 | Frontend/Backend/CI |
| DEC-011 | Open | PoC 로컬 DB(H2 파일/테스트 메모리), Flyway 마이그레이션·Seed·배포 DB 정책 | Backend/테스트/통합 |

## 결정 기록 양식

```text
ID:
상태: Open / Accepted / Superseded
결정일 / 승인자:
문제/맥락:
검토한 대안:
최종 결정:
영향 범위 (REQ / UI / DB / API / Test):
관련 Contract/설계 PR:
```

**계약에 영향을 주는 결정은** 결정만 기록해서 끝내지 않고 `openapi.yaml` 변경 PR → 승인 → FE/BE `contract.sha` 업데이트까지 이어져야 합니다.

## 기술 스택 제안 (승인 전)

[PoC 기술 스택 제안서](./tech-stack-proposal.md): **Java 21 + Spring Boot 4.1.x, 단일 모듈형 Backend, Spring Data JPA(Hibernate) + H2 File 로컬/H2 Memory 테스트 + Flyway, React + TypeScript + Vite + CSS Modules + MSW**. 이는 DEC-003/004/011에 대한 제안이지 **Accepted 결정이 아닙니다**. Auth/가입/DB/운영 관련 다른 Open 항목도 계속 남아 있습니다.
