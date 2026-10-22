# AA 개발 착수 인계 체크리스트

## 기준선(AA/PL 확인)
- [ ] 요구사항 ID/담당/완료 기준 확인 — [요구사항](../requirements.md)
- [ ] 각 서비스 기능/데이터 소유권 확인 — [아키텍처](../architecture.md)
- [ ] 논리 DB Entity, Key, 상태/삭제 정책 확인 — [DB](../db-design.md)
- [ ] 전체 화면 IA, UI ID, 역할, 화면 이동 확인 — [화면](../ui-structure.md)
- [ ] 공통 UI 컴포넌트와 인터랙션 정책 확인 — [UI 규칙](../ui-guidelines.md)
- [ ] FE↔BE OpenAPI v0.1 계약 검토 — [OpenAPI](../../openapi.yaml)
- [ ] DEC-001~011 Accepted 설계 준수 및 새로운 미결정/범위 밖 항목 식별 — [결정사항](./decisions.md)
- [ ] Contract Repository의 승인 커밋 SHA를 지정하고 FE/BE `contract.sha`의 일치 확인

## 각 도메인 담당자 인수 확인
- [ ] A Auth: 로그인/로그아웃·비밀번호 요구와 인증 정책
- [ ] B User: 가입/CRUD/검색·페이징/상태 정책 및 계정 생성 협업
- [ ] C Permission: Role/권한 모델, ADMIN 접근 제한
- [ ] 개발자들이 코드 내부 구현 세부사항은 자율적으로 설계하되 공통 계약은 준수한다고 합의

## 개발 / 통합의 완료 조건
- [ ] 각 FE/BE PR에 REQ/UI ID 및 Contract SHA 기재
- [ ] OpenAPI 유효성·타입 생성 및 실행 중인 서버 계약 테스트 증빙
- [ ] 공통 UI 패턴·에러/로딩·권한 접근 확인
- [ ] 가입→로그인→내 정보, 관리자 조회→상태 변경, 권한 변경 E2E 통합 검증
- [ ] 구현·테스트·PR의 증빙 링크를 [추적표](./traceability.md)에 반영

**이 파일의 체크박스는 아직 체크되지 않았습니다.** 문서 작성과 실행 검증 완료를 혼동하지 않습니다.
