# 품질 게이트와 적용 상태

| 영역 | 즉시 자동 검증 | 구현 단계에 추가할 검증 |
|---|---|---|
| Contract | OpenAPI v0.1 스키마 유효성 (GitHub Actions) | 이전 버전 대비 Breaking Change 분석 |
| Frontend | 고정된 Contract 다운로드/타입 생성 성공 | TypeScript 빌드, 화면 테스트, Mock 기반 E2E |
| Backend | 고정된 Contract 다운로드/스키마 유효성 | **실행 서버 대상** 요청/응답 Contract Test, 권한/상태 검증 |
| 통합 | PR에 SHA/영향/관련 PR 기록 | FE/BE 실제 통합 E2E 및 릴리스 조합 기록 |

## 중요한 구분

- OpenAPI 문법 검증과 FE 타입 생성 성공만으로 **실제 Backend가 계약을 준수한다는 증거는 아닙니다.**
- Backend 런타임 계약 테스트는 서버 구현과 테스트 환경이 준비된 후 CI에 추가해야 합니다.
- FE/BE 자동화는 `contract.sha`가 가리키는 고정 계약을 대상으로 동작합니다.
- PR 리뷰/최종 Merge 결정은 개발자 또는 AA/PL 책임입니다.
