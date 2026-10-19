# 공통 UI 기준 (초안)

Frontend 전원이 지켜야 할 최소 디자인 규칙입니다. 구체 색상/폰트 값은 팀 합의 후 확정합니다.

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

## 초기 결정 필요
- CSS/UI 라이브러리 및 토큰(컬러/간격/타이포)
- 전역 상태/인증 토큰 처리 전략
- 폼 유효성 검증과 알림 UX
- 공통 컴포넌트 담당/코드 리뷰 규칙

원칙: AA는 **화면의 목적·흐름·구성**을 정의하고, Frontend 담당자는 **구현·상세 스타일**을 정의합니다.
