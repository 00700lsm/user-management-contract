# 공통 작업 규칙

프로젝트 전체 Git/PR/계약 기준은 [Git 협업 운영 규칙](./docs/governance/git-workflow.md)과 [계약 변경 기준](./docs/contract-governance.md)에 둡니다.

## 최초 작업
1. 개발자 A=Auth FE+BE, B=User FE+BE, C=Permission FE+BE
2. 먼저 [요구사항](./docs/requirements.md)·[DB](./docs/db-design.md)·[화면 IA](./docs/ui-structure.md)·[OpenAPI](./openapi.yaml)를 확인합니다.
3. **현재 승인된 API 계약 커밋 SHA**를 Frontend/Backend의 `contract.sha`에 동일하게 고정합니다.
4. Contract 변경은 이 저장소의 PR → 리뷰/승인 → Merge 후 각 구현 저장소에 반영합니다.

브랜치 보호/필수 리뷰 설정은 GitHub Settings에서 별도로 적용해야 합니다.
