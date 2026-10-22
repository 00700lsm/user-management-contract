# P0-03 보호 브랜치 및 PR 필수 CI 적용

**승인된 목표:** Contract, Frontend, Backend, Workspace의 `main`과 `dev`에 PR 필수·최소 타인 승인 1명·직접 Push/Force Push 제한·필수 CI·브랜치 삭제 금지.

## 관리자 적용 전 선행 조건

1. 각 Repository에서 PR 작성자와 **다른 Write 권한 협업자**를 확보합니다. 작성자는 본인 PR을 승인할 수 없어, 1인 저장소에 즉시 강제하면 전부 병합이 막힙니다.
2. 이 준비 작업의 **네 Repository PR을 먼저 CI 성공 후 dev에 병합**하고, main에도 릴리스 PR을 통해 CI 정의를 반영합니다. Checks가 해당 대상 브랜치에서 생성되는지 확인합니다.
3. GitHub Actions가 활성화되어 있고, 교차 저장소 G0가 FE/BE 체크아웃을 읽을 수 있는지 확인합니다.
4. 이 GitHub 연결에는 Repository Admin 쓰기 권한이 없습니다. Ruleset JSON은 `docs/governance/rulesets/` 아래에 **적용을 위한 제안 파일**로만 존재하며 적용된 보안 설정이 아닙니다.

## 저장소별 필수 검사

| Repository | 필수 Check Run Job Context |
|---|---|
| Contract | `validate-contract`, `cross-repo-baseline` |
| Backend | `build`, `contract-baseline` |
| Frontend | `build`, `contract-types` |
| Workspace | `workspace-checks` |

각 CI는 준비 PR에서 `main`/`dev` 타깃의 모든 PR마다 실행되게 구성했습니다. Workflow 전체 이름이 아니라 **실제 PR Checks 화면의 Job 이름**을 기준으로 선택하세요. GitHub Actions 출처를 지정할 수 있다면 지정합니다. GitHub Pages/외부 App이 우연히 같은 이름의 Status를 제출하지 않도록 주의합니다.

## 관리자 GitHub UI 순서

각 Repository에서 **Settings → Rules → Rulesets → New branch ruleset**으로 이동합니다. UI에서 JSON Import가 지원될 경우 해당 Repository의 JSON을 활용하고, 아니라면 직접 동일 옵션을 선택합니다.

- Rule name: `main-dev-pr-review-and-ci`, Enforcement: `Active`
- Target: Branch, Include `main` 및 `dev` 두 브랜치
- Bypass actors: 없음
- Require a pull request before merging: 켬
- Required approvals: 1
- Dismiss stale pull request approvals when new commits are pushed: 켬
- Require approval of most recent reviewable push: 켬
- Require conversation resolution before merging: 켬
- Restrict deletions / Block force pushes: 켬
- Require status checks to pass: 저장소별 해당 1~2개 job 지정
- Require branches to be up to date before merging: 초기에는 끔 (Cross-repo 검증 시점은 Artifact로 기록)
- **Restrict updates는 켜지 않음**. 정상 PR Merge에도 쓰기 제한이 걸릴 수 있으므로 PR required가 직접 Push를 제한하도록 구성

GitHub 계정의 플랜과 저장소 공개 여부에 따라 일부 기능이 지원되지 않을 수 있습니다. 사용 가능한 설정만 선택하고 미지원 항목은 이슈에 기록합니다.

## 적용 순서와 실제 통제 확인

1. 네 준비 PR CI 통과 후 **dev에 병합**. main 승격 준비가 됐는지도 확인.
2. 각 Repo에서 `dev`/ `main` Ruleset을 Active로 저장.
3. 타인 Write 권한이 있는 테스트 계정으로 직접 Push 시 거부, 미승인 PR 병합 불가, 실패 CI 병합 불가를 확인.
4. 다른 협업자 승인 + 전체 필수 CI 성공 시 정상 PR Merge 가능하고 Review Thread 미해결은 차단되는지 확인.
5. 규칙 URL/스크린샷, 시험 PR, 해당 Branch Rules 적용 상태를 [P0-03 이슈](https://github.com/00700lsm/user-management-contract/issues/4)에 기록.

비상 변경도 기본은 hotfix PR + 1인 검토 + 필수 CI입니다. 향후 관리자 우회가 꼭 필요하면 **별도 승인** 후 Bypass와 사유 기록을 도입합니다.

**중요:** Ruleset JSON은 동작을 설명하는 준비물이며, GitHub 원격 보호 상태가 자동 변경되는 것이 아닙니다.
