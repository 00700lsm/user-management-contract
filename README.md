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

## AA 개발 인계 패키지

개발 착수 전에 [AA 설계 인계 목차](docs/aa/README.md)를 확인합니다. 기능 상세, 요구사항 추적표, 설계 미결정 사항, 인계 체크리스트가 있습니다. **이 저장소가 AA 설계의 정본**입니다.

## 실행형 Contract Skills

- [`validate-api-contract`](.agents/skills/validate-api-contract/SKILL.md) — OpenAPI 유효성 및 FE/BE 승인 Contract SHA 일치·존재 여부 검증
- [`review-contract-change`](.agents/skills/review-contract-change/SKILL.md) — 기준/변경안 비교, Breaking Change 후보와 FE/BE·테스트 영향 분석
- [`check-requirement-coverage`](.agents/skills/check-requirement-coverage/SKILL.md) — REQ→UI→API→DB Owner→TC 추적표의 누락·불일치 검사

모든 Skill은 요청 시 읽기 전용으로 실행하며, 사용자 명시 요청 없이 Git/문서/계약 SHA를 변경하지 않습니다. Claude Code용 동일 이름 어댑터는 `.claude/skills/`에 있습니다. 공통 설계 준수는 Skill이 아니라 `AGENTS.md`의 상시 규칙입니다.

### 로컬 검사 명령

세 Repository를 함께 Clone한 환경에서 **엄격한 교차 기준선 검사(G0)**: `python3 scripts/verify_integration_baseline.py --report integration-evidence.json` (자세한 내용: [통합 품질 게이트](docs/governance/integration-gate.md)). 부분 로컬 점검용으로 `python3 scripts/validate_contract_pins.py` (누락 Repository는 WARN), 요구사항 점검은 `python3 scripts/check_requirement_coverage.py`를 실행할 수 있습니다. OpenAPI 구조 검증은 기존 GitHub Actions(`.github/workflows/validate-openapi.yml`)를 사용하거나, 이미 설치된 CLI가 있다면 `npx --no-install @apidevtools/swagger-cli validate openapi.yaml`을 실행합니다. Python 검사는 표준 라이브러리만 사용합니다. 일부 로컬 Repository/도구가 없으면 미검증 경고를 별도로 확인해야 합니다.
