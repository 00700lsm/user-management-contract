# 공통 형상관리·협업 운영 규칙 (v0.1)

이 문서는 Contract, Backend, Frontend, Workspace 4개 Repository 전체의 **공통 협업 운영 정본**입니다. 각 코드 저장소에는 로컬 실행 안내/자동화만 둡니다.

## Repository 책임

| Repository | 저장하는 것 | 변경 주체 |
|---|---|---|
| user-management-contract | OpenAPI, AA 요구사항/서비스 경계/DB·화면 초안, 공통 협업 규칙 | AA/PL 승인 + 관련 도메인 담당자의 계약 PR |
| user-management-backend | Auth / User / Permission Backend 구현 | 담당 개발자 A/B/C |
| user-management-frontend | Auth / User / Permission Frontend 구현, 공통 UI / API Client | 담당 개발자 A/B/C 및 공통 UI 리뷰어 |

도메인 책임은 **A=Auth FE+BE, B=User FE+BE, C=Permission FE+BE**입니다. 교차 개발이 아닙니다.

## 로컬 Workspace

```text
user-management-workspace/
├── user-management-contract/  # 기준 문서 / OpenAPI 정본
├── user-management-backend/   # 백엔드 코드
└── user-management-frontend/  # 프론트엔드 코드
```

3개 폴더는 각각 **독립 Git 저장소**입니다. **Workspace 루트에서는 기능 코드·설계·API 변경을 커밋하지 않습니다.** Workspace 루트 Git은 init 스크립트/에디터 설정/가이드 수정에만 사용합니다. 모든 기능과 계약 변경은 소유한 하위 Repository에서 개별 commit/push/PR합니다.

## 브랜치/커밋/PR

- `main`: 안정/릴리스 기준선. `dev` 검증 후 PR 병합합니다. 직접 push 금지 권장.
- `dev`: 팀 통합 개발 기준선. 신규 Clone은 `dev`로 체크아웃하며 기능 브랜치의 PR 대상입니다.
- 작업 브랜치: `feat/auth-login`, `feat/user-list`, `fix/permission-role`, `docs/db-model`, `contract/user-search`.
- 하나의 기능이라도 FE/BE 변경은 **각 Repository에서 별도 브랜치, 커밋, PR**을 발행합니다.
- 같은 기능의 FE/BE 두 PR에는 상호 링크와 동일한 **Contract SHA**를 적습니다.
- `git add .` 사용 전 `git status` 확인. 타 개발자 영역/생성 산출물의 불필요한 수정 금지.
- 작업 시작: 해당 저장소에서 `git switch dev && git pull --ff-only origin dev` 후 feature 브랜치 생성.
- 작업 중 기준선 동기화: `git fetch origin` 후 팀 합의한 merge 또는 rebase 사용. **공유한 브랜치를 강제 push하지 않습니다.**
- 병합: 필수 CI 통과, 관련 담당자/AA 리뷰, 주요 흐름 검증 근거를 확인합니다.
- 운영 중 긴급 수정: Issue/PR 링크로 변경 이유·영향·검증을 기록합니다.

## API 계약 기준선 고정

- 계약 정본은 이 저장소의 `openapi.yaml`입니다.
- FE/BE 각 저장소 루트에 `contract.sha` (40자리 Git commit SHA)를 둡니다.
- 스크립트는 이 SHA의 OpenAPI만 가져옵니다. `main`의 최신 파일이나 로컬 미커밋 내용을 몰래 사용하지 않습니다.
- **API 요청/응답/권한/상태코드 변경**: Contract Repo PR → 담당자+AA 승인 → Merge → 신규 Contract SHA를 FE/BE에 각각 반영 → 타입 재생성/구현 수정/테스트.
- 문서만 변경되고 `openapi.yaml`은 그대로라면 FE/BE의 `contract.sha`를 불필요하게 변경할 필요 없습니다.
- 구현 저장소에서 OpenAPI를 직접 고쳐 별도 정본을 만들지 않습니다.
- 공통 UI 규칙 변경 역시 영향받는 담당자와 리뷰하며, 공통 컴포넌트 구현은 Frontend 저장소에 둡니다.

## PR 최소 조건

1. 요구사항 ID / 화면 ID / 변경 이유
2. `contract.sha` 기준 및 계약 PR 링크 (변경이 있다면)
3. 변경 영향(다른 담당자 기능, 데이터, UI, API)
4. 테스트 결과/증거
5. FE↔BE 연결 확인(필요한 경우)

## 병합 순서

- API 계약 변경이 있으면 **Contract PR이 먼저** 병합됩니다.
- 새 SHA를 가리키는 FE/BE PR은 **동일 계약 버전**을 사용해야 합니다.
- 관련 기능 PR은 각 Repo에서 독립 Merge되므로 일시적 불일치가 생길 수 있습니다. 통합 배포/테스트 시 **호환되는 FE Commit + BE Commit + Contract SHA 세트**를 함께 기록해야 합니다.
- Breaking Change라면 호환성 전략(병행 지원/동시 릴리스 등)을 승인 후 실행합니다. GitHub 저장소 세 개의 Merge는 원자적 작업이 아닙니다.


## 진행 중 Contract 변경과 기능 PR의 호환성 검토 (단계적 적용)

- Contract PR이 변경되면 AA는 변경된 path/method, 요청·응답·오류/상태코드·권한을 분류하고 REQ/UI/API/TC 및 Auth(A)·User(B)·Permission(C) 담당자를 식별해 PR 또는 Issue 링크로 통보합니다. 영향이 없는 담당자는 기존 작업을 지속합니다.
- 구현 담당자는 기능 브랜치의 `contract.sha`를 개발 기준선으로 유지할 수 있습니다. 계약이 변경됐다는 이유만으로 다른 담당자의 작업을 중단하거나 모든 브랜치에 일괄 SHA 변경을 강요하지 않습니다.
- **기능 PR → dev 병합 직전** AA는 구현 PR의 pin과 최신 **Contract/dev** 커밋 SHA를 함께 기록하고, 변경된 API의 호환성과 실제 테스트 결과를 검토합니다. 다른 SHA는 자동 실패가 아니라 영향 분석 대상입니다.
- 계약과 기능 간 불일치가 발견되면 동일한 기존 PR 브랜치에 수정 커밋·테스트를 추가합니다. 새 PR을 강제로 만들거나 진행 중인 작업 브랜치를 자동 변경하지 않습니다.
- Breaking Change 후보는 AA/PL과 영향받는 FE/BE 담당자가 대응 전략을 합의하기 전 병합하지 않습니다. OpenAPI diff·SHA 차이만으로 실제 런타임 호환성을 보장할 수 없습니다.
- Backend·Frontend CI의 **최신 Contract/dev drift 확인은 초기에는 비차단 WARNING**으로 운영합니다. 기존 pinned OpenAPI/빌드 검증은 계속 필수입니다. 충분한 사례 검증 및 팀 합의 뒤에만 필수 호환성 게이트로 승격합니다.
- 새 절차 시행 전에 생성된 PR은 소급 차단하지 않고 기존 검증 절차로 마무리합니다. Contract/dev가 리뷰 후 변경되었다면 병합 전 현재 SHA로 영향 범위를 재확인합니다.
- **주의:** 개별 기능 PR의 호환성 검토와 FE+BE+Contract의 엄격한 통합 기준선(G0)은 다릅니다. G0에서 요구하는 동일 SHA 조건을 경고 검증으로 대체하지 않습니다.
## GitHub main/dev 보호 정책 (P0-03 승인안)

Contract/Backend/Frontend/Workspace 4개 저장소의 main 및 dev 브랜치에 다음 보호 정책을 적용합니다.
- PR 필수, 다른 Write 권한 리뷰어의 승인 1명, 신규 코드 Push 시 기존 승인 무효화, 미해결 리뷰 대화가 있으면 병합 금지
- 직접 Push 및 Force Push 금지, 보호 브랜치 삭제 금지, 각 저장소 필수 CI 통과
- PR을 통해 정상 병합되어야 하므로 Restrict updates 옵션은 사용하지 않습니다.
- 세부 설정 및 관리자 적용·검증 순서는 [보호 브랜치 롤아웃 안내](./branch-protection-rollout.md) 참조
- 이 문서와 워크플로 변경만으로 GitHub Ruleset이 활성화되지는 않습니다. Admin Settings에서 별도 활성화해야 합니다.

## 명시적 dev 동기화

Workspace를 최초 Clone할 때는 세 하위 저장소를 `dev`로 받습니다. 기존 Clone은 자동 변경하지 않습니다. 직접 동기화하려면 Workspace 루트에서 `bash scripts/use-dev.sh`를 실행하며, 스크립트는 모든 하위 저장소가 깨끗할 때만 브랜치 전환과 fast-forward Pull을 시도합니다. 작업 브랜치를 자동 병합하지 않습니다.
