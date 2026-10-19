# User Management — Contract

사용자 관리 PoC의 **공통 API 계약 정본(Source of Truth)** 입니다.

- [Backend](https://github.com/00700lsm/user-management-backend)
- [Frontend](https://github.com/00700lsm/user-management-frontend)
- API 기준: [openapi.yaml](./openapi.yaml)
- 변경 절차: [docs/contract-governance.md](./docs/contract-governance.md)

## 담당 방식
- 개발자 A: Auth Frontend + Auth Backend
- 개발자 B: User Frontend + User Backend
- 개발자 C: Permission Frontend + Permission Backend
- AA/PL: 최초 기능/서비스/화면 경계 및 공통 계약 승인

Frontend와 Backend는 **같은 담당자가 같은 도메인을 수직 개발**하되, 인터페이스는 이 저장소의 OpenAPI와 일치해야 합니다.

## 원칙
1. 기능 정의를 먼저 합의하고 1차 OpenAPI를 고정합니다.
2. Frontend/Backend는 동일한 Contract 커밋 SHA를 기준으로 구현합니다.
3. 요청/응답, URL, 상태코드, 오류 응답이 바뀌면 **코드보다 계약 PR을 먼저** 반영합니다.
4. PR에서 API 계약 버전을 기록하고 실제 응답이 계약과 맞는지 테스트합니다.
5. 이 API는 우선 **Frontend ↔ Backend 외부 인터페이스**를 기술합니다. 서비스 간 내부 API는 분리 운영이 결정되면 추가로 명세합니다.

현재 문서는 PoC 설계 **초안**입니다. 구현/CI 검증이 완료된 상태가 아닙니다.
