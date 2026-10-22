# 품질 게이트와 적용 상태

| 검증 | 현재 자동화 | 검증하지 못하는 내용 |
|---|---|---|
| Contract 구조 | `.github/workflows/validate-openapi.yml`: OpenAPI 문법 및 REQ/UI/API/DB/TC 구조 점검 | 구현체 HTTP 응답, 도메인 의미 및 테스트 실행 |
| G0 통합 기준선 | [Cross-repo integration baseline](./integration-gate.md): 실제 Contract/FE/BE Git checkout SHA, FE/BE `contract.sha` 동일, pinned 커밋과 OpenAPI 존재 증명 | 실제 API, 인증, E2E |
| G1 FE Mock UI | Frontend CI의 Vitest/Playwright MSW 테스트 | 실제 Backend JWT 및 업무 API |
| BE 기초 | Backend CI의 Gradle/H2/Flyway Context Test | 실제 Controller 요청/응답·JWT 권한 |
| G2 | Backend Runtime Contract Test **미구현** | 현재 G2 PASS 표시 금지 |
| G3 | 실제 Auth JWT→User/Permission 통합 **미구현** | 현재 G3 PASS 표시 금지 |
| G4 | Mock 비활성 FE→BE E2E **미구현** | 현재 G4 PASS 표시 금지 |

**판정 기준:** G0 PASS = 저장소 버전 정합성만 확인. G1 PASS = Mock UI 화면만 확인. G2/G3/G4가 미실행·미구현이면 `NOT_RUN/BLOCKED`; 릴리스 준비 완료를 주장할 수 없습니다.

## 증빙과 범위

- G0 Workflow는 Contract PR/관련 dev push/수동 실행/평일 일정으로 3개 저장소의 **그 시점 dev HEAD**를 체크하고 JSON 커밋 조합 증거를 Artifact로 저장합니다. FE/BE PR 개별 커밋을 자동 검증하지는 않습니다.
- Contract SHA가 유효해도 실제 응답과 OpenAPI가 동일하다는 근거가 아닙니다.
- FE/BE 변경이 릴리스 후보일 경우 반드시 **실제 FE SHA + BE SHA + Contract SHA + G0~G4 실행 증거**를 제출합니다.
- PR 리뷰와 최종 Merge 결정은 담당 개발자·AA/PL이 수행하며 이 Workflow는 자동 승인하지 않습니다.
