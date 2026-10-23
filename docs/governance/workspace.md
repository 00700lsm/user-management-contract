# 통합 개발 Workspace 운영 (3 Repo)

3개 Repository는 유지하고, **Contract 저장소에 Workspace 설정과 일괄 동기화 스크립트**를 둡니다. 여러 Repository를 담는 하나의 Git 브랜치는 존재하지 않습니다. `workspace/auto-sync`는 이 기능을 개발하는 PR 브랜치일 뿐, 세 저장소의 통합 브랜치가 아닙니다.

## 최초 1회
```bash
mkdir -p user-management-workspace
cd user-management-workspace
git clone https://github.com/00700lsm/user-management-contract.git
bash user-management-contract/scripts/workspace/bootstrap.sh
```

이후 VS Code / Cursor에서 `user-management-contract/user-management.code-workspace` 파일을 열어 세 프로젝트를 함께 사용합니다.

## 하나의 명령으로 업데이트
```bash
bash user-management-contract/scripts/workspace/sync.sh
```

스크립트는 세 Repo에 순서대로:
1. `git fetch --prune origin`으로 원격 브랜치 갱신
2. **현재 체크아웃된 브랜치의 upstream이 있을 때만** `git pull --ff-only` 실행
3. 미커밋 변경이 있거나 tracking 정보가 없으면 Fetch만 하고 Pull은 건너뜀
4. 충돌/비-fast-forward 상황이면 자동 Merge/Rebase/Reset하지 않고 오류 표시

Workspace 설정은 `folderOpen` 자동 실행 작업을 포함합니다. **VS Code/Cursor가 해당 기능을 지원하고 사용자 신뢰/자동 작업 실행을 허용한 경우** 열 때 위 동기화가 실행됩니다. 허용하지 않거나 지원하지 않으면 명령/Task를 수동 실행하면 됩니다.

## 도메인 기능 작업 브랜치를 FE/BE 동시에 준비
```bash
bash user-management-contract/scripts/workspace/switch-feature.sh auth-login
```
위 명령은 Backend와 Frontend를 각각 `feat/auth-login` 브랜치로 전환하거나 없는 브랜치를 생성합니다. Contract Repo는 전환하지 않습니다.

**주의**: FE/BE의 동일한 브랜치 이름은 편의상 맞추는 것일 뿐 두 Repository가 같은 Git 브랜치를 공유하는 것은 아닙니다. 커밋/푸시/PR은 각각 해야 합니다.

## 일상 운영
- Workspace 동기화는 **현재 체크아웃된 각 Repo의 브랜치**만 Pull합니다. 개발 중인 feature에 main을 자동 병합하지 않습니다.
- 다른 개발자의 작업 브랜치를 최신 상태로 보고 싶다면 Fetch 후 필요할 때 명시적으로 해당 브랜치를 checkout합니다.
- feature에서 최신 main을 반영하려면 관련 저장소에서 직접 `git fetch origin` 후 팀 규칙에 맞춰 rebase 또는 merge합니다.
- `contract.sha`는 자동 동기화하지 않습니다. 계약 버전 변경은 승인된 Contract PR 이후 각각 구현 저장소에서 별도로 변경합니다.
- Fetch/Pull 실패, dirty tree, 비-fast-forward 오류는 사용자에게 출력됩니다.

## 버전 재현 주의
자동 Pull은 개발자 작업 환경을 최신화하는 기능일 뿐 **FE SHA + BE SHA + Contract SHA**를 원자적으로 고정/배포하는 도구는 아닙니다. 통합 테스트 시 세 SHA를 릴리스 기록에 남겨야 합니다.

## 역할
- 공통 Git/Contract 규칙: `docs/governance/git-workflow.md`
- Workspace 실행 스크립트와 VS Code 설정: 이 Contract Repo
- 서비스/화면 실제 구현: 각각 Backend/Frontend Repo
