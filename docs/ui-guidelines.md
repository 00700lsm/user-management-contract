# 공통 UI 기준 (PoC Accepted)

Frontend 전원이 지킬 IA·공통 UI 원칙입니다. React/TS/CSS Modules 및 디자인 토큰 사용은 DEC-004 Accepted이며 구체 비주얼은 Frontend 루트 `design.md`에서 관리합니다. 새 공통 규칙 변경은 팀 리뷰를 거칩니다.

## 디자인 시스템 공통 구성
- App Shell: 공통 Header / Sidebar / Content
- UI 컴포넌트: Button, TextField, Select, DataTable, Pagination, Modal, StatusBadge, FormField
- 페이지 패턴: LoginForm, ListPage, DetailPage, EditForm
- 상태: loading / empty / error / forbidden / success를 빠짐없이 처리
- 접근성: Label 연결, 포커스 표시, 키보드 접근, 오류 메시지

## 공통 컴포넌트 사용 규칙
- 기능별로 Button/Table/Modal을 중복 구현하지 않습니다.
- 공통 컴포넌트 변경은 Frontend 공동 리뷰 또는 AA/PL 확인 후 반영합니다.
- 화면별 데이터 취득은 OpenAPI에 근거한 API Client 계층에서 수행합니다.
- Auth/User/Permission 영역 간 화면 이동은 `docs/ui-structure.md`의 route를 따릅니다.

## 현재 적용할 PoC 기준과 구현 검토 사항
- DEC-004: CSS Modules + Frontend `design.md` 토큰 및 Shared UI; 무거운 UI 라이브러리 추가 없음.
- DEC-001/009: `sessionStorage` JWT 기반 UI 상태·Role 표시는 참고용이며 서버 인가 대체 불가.
- 폼 유효성/알림 UX는 공통 오류·로딩·금지 상태를 보장하면서 컴포넌트 구현 때 함께 리뷰합니다.
- 공통 컴포넌트 변경은 FE 공동 리뷰 또는 AA/PL 확인이 필요합니다.

원칙: AA는 **화면의 목적·흐름·구성**을 정의하고, Frontend 담당자는 **구현·상세 스타일**을 정의합니다.
