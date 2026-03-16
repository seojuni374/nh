# 전문화된 팀 카탈로그

이 패키지는 **한 번에 한 팀**만 운영하는 Claude Code Agent Teams 전제에 맞춰 설계되어 있습니다.
즉, 여러 팀을 쓰더라도 **순차적으로** 돌립니다.

---

## 1) `/route-task`
초보용 라우터입니다.  
내가 지금 뭘 써야 할지 모르겠을 때 가장 먼저 씁니다.

### 하는 일
- 요청을 분류
- 가장 적합한 팀/명령어 선택
- 필요하면 바로 해당 팀을 생성

### 추천 상황
- Claude Code가 처음
- 퀀트 / 공모전 / 경제학 / 코딩 중 뭐로 시작할지 모름

---

## 2) `/quant-research`
아이디어, 신호, 검증 설계, 리스크 반론까지 하는 **연구 팀**입니다.

### 팀원
- **Regime Strategist**: 시장 국면과 아이디어의 경제적 직관 검토
- **Alpha Scientist**: 시그널 / 피처 / 모델 아이디어 제안
- **Data Validation Engineer**: 데이터 가정, feature pipeline, 누수 위험 점검
- **Backtest Skeptic**: 검증 설계, bias, 통계적 착시 공격
- **Execution & Risk Officer**: 체결, 비용, 포지션, 리스크 관리 검토

### 결과물
- 전략 가설
- 데이터/피처 요구사항
- 검증 계획
- 실패 가능성
- 다음 실험 3개

---

## 3) `/quant-build`
승인된 아이디어를 **코드 / 백테스트 구조 / MVP**로 바꾸는 팀입니다.

### 팀원
- **Quant Tech Lead**: 구조 결정, 파일 분배
- **Backtest Engine Builder**: 이벤트 / 포트폴리오 / 주문 구조
- **Data Pipeline Builder**: 로더 / 정제 / feature pipeline
- **Test & Reliability Owner**: 테스트 / 회귀 체크 / 재현성
- **Risk Review Engineer**: 거래비용, 포지션 제한, 예외 처리 검토

### 결과물
- 구현 계획
- 파일별 작업 분배
- 코드 변경
- 테스트 / 실행 방법
- 남은 위험

---

## 4) `/competition-design`
공모전 문제정의와 기획 자체를 만드는 팀입니다.

### 팀원
- **Problem Strategist**: 어떤 문제를 잡아야 이길 확률이 높은지 설계
- **Novelty Scout**: 차별점, 최신성, 레퍼런스 감각 제안
- **Feasibility Architect**: 기간 / 인력 / 기술 난이도 기준으로 현실성 검토
- **Impact & Metric Designer**: 성과지표, 평가 구조, 사회적 임팩트 설계
- **Judge Skeptic**: 심사위원이 깔 부분을 공격

### 결과물
- 최종 주제 1~3개
- 왜 이 주제가 강한지
- MVP 범위
- 심사 포인트
- 탈락 리스크

---

## 5) `/competition-pitch`
이미 잡은 아이디어를 **제안서/발표/스토리라인**으로 강화하는 팀입니다.

### 팀원
- **Storyline Designer**: 발표 흐름 설계
- **Evidence Curator**: 근거 / 수치 / 비교자료 구성
- **Slide Architect**: 슬라이드 메시지 단위 구조화
- **Demo Planner**: 시연 흐름 / 프로토타입 전달력 설계
- **Judge Persona Critic**: 심사위원 질문 예상 및 반박 준비

### 결과물
- 발표 목차
- 슬라이드별 핵심 문장
- 예상 질문과 답
- 데모 흐름
- 3분 / 5분 / 10분 버전 요약

---

## 6) `/econ-explain`
경제학 질문을 **쉽고 정확하게 설명**하는 팀입니다.

### 팀원
- **Macroeconomist**
- **Microeconomist**
- **Econometrician**
- **Historical Comparator**
- **Plain-Language Explainer**

### 결과물
- 쉬운 설명
- 엄밀한 설명
- 예시
- 가정
- 헷갈리기 쉬운 반례

---

## 7) `/econ-policy`
경제학 질문을 **정책 / trade-off / 근거** 중심으로 분석하는 팀입니다.

### 팀원
- **Policy Analyst**
- **Distributional Impact Analyst**
- **Econometrician**
- **Historical Comparator**
- **Devil's Advocate Economist**

### 결과물
- 정책 선택지 비교
- 누가 이득 / 손해 보는지
- 필요한 근거
- 반대 논리
- 현실적 권고안

---

## 8) `/vibe-build`
새로운 기능 / MVP / 프로토타입을 **빨리 만들기** 위한 구현 팀입니다.

### 팀원
- **Repo Scout**: 현재 코드베이스 구조 파악
- **System Architect**: 구조와 인터페이스 설계
- **Builder A**: 핵심 구현
- **Builder B / Test Owner**: 보조 구현 + 테스트 책임
- **Reviewer / Integrator**: 합치기, 코드 품질, 최종 검토

### 결과물
- 계획
- 구현
- 테스트
- 실행법
- 다음 개선점

---

## 9) `/vibe-refactor`
기존 코드를 안전하게 정리하는 팀입니다.

### 팀원
- **Codebase Cartographer**: 의존성 지도 작성
- **Refactor Architect**: 최소 변경 원칙 설계
- **Migration Engineer**: 단계적 변경
- **Regression Test Owner**: 깨진 부분 검사
- **Reviewer**: 스타일/위험 검토

### 결과물
- 리팩터링 계획
- 변경 순서
- 영향 범위
- 테스트 기준
- 롤백 포인트

---

## 10) `/audit-final`
마지막으로 약점을 공격하는 **최종 검증 팀**입니다.

### 팀원
- **Red Team Lead**
- **Statistician / Validation Reviewer**
- **Risk or Security Reviewer**
- **Stakeholder Skeptic**
- **Operational Reviewer**

### 결과물
- 약점 목록
- 우선순위
- 치명도
- 수정 권고
- 출시 / 제출 / 실행 전 체크리스트

---

## 11) `/full-pipeline`
처음부터 끝까지 순차 운영하는 전체 파이프라인입니다.

### 기본 순서
- 라우팅
- 도메인 연구/기획
- 구현
- 최종 감사

### 예시
- 퀀트: `route-task -> quant-research -> quant-build -> audit-final`
- 공모전: `route-task -> competition-design -> competition-pitch -> audit-final`
- 경제학: `route-task -> econ-explain` 또는 `route-task -> econ-policy`
