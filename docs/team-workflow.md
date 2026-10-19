# 3인 수직 분할 PoC 운영

| 담당 | Backend | Frontend |
|---|---|---|
| 개발자 A | Auth (인증/비밀번호/토큰) | 로그인/비밀번호 변경/로그아웃 |
| 개발자 B | User (가입/프로필/사용자 관리) | 가입/내 정보/관리자 사용자 관리 |
| 개발자 C | Permission (Role/권한 관리) | Role 조회/사용자 권한 변경 |

## 시작 전 AA/PL 공통 핸드오프
1. [요구사항](./requirements.md) 기능 ID/완료 조건
2. [시스템 경계](./architecture.md) 책임·의존·데이터 소유
3. [DB 초안](./db-design.md) Entity/Key/상태 정책
4. [화면 IA](./ui-structure.md) route/행위/API 대응
5. [공통 UI](./ui-guidelines.md) 공통 패턴
6. [API 계약](../openapi.yaml) 요청·응답 규격

## 개발 단계
요구·설계 합의 → Contract SHA 기준선 → 담당자별 FE+BE 구현 → 도메인 테스트 → 계약 적합성 검사 → 타 도메인 연결 및 E2E → PR 리뷰/병합.

## 변경 관리
- 담당자 내부 구현만 변경: 일반 코드 PR.
- 다른 도메인/화면 공통 요소/DB 모델/API 계약 변경: 영향 분석 + 관련 담당과 협의.
- 공통 OpenAPI는 [변경 절차](./contract-governance.md)에 따라 Contract PR **선반영**.

## PoC 평가
- 계약 문서 없이 임의로 필드를 맞춘 사례가 있었는가?
- 사용자 목록/권한 변경 등 연결 화면이 계약 기준으로 통합되었는가?
- 공통 UI를 재사용했고 외관/UX가 일관적인가?
- 변경제안→계약 개정→구현→테스트 관계를 Git 이력으로 추적할 수 있는가?

이 구성은 **교차 개발 실험이 아님**을 명시합니다.
