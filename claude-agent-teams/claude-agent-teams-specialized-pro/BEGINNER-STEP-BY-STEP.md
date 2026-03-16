# 초보용 순서대로 따라하기

## 0. ZIP 압축 풀기
다운로드한 ZIP을 풀면 `.claude` 폴더가 들어 있습니다.

## 1. 프로젝트 폴더에 넣기
원하는 프로젝트 폴더의 루트에 `.claude` 폴더를 그대로 복사합니다.

예:
```text
my-project/
├─ .claude/
│  ├─ CLAUDE.md
│  ├─ settings.local.json
│  └─ skills/
└─ ...
```

## 2. Claude Code 실행
터미널에서 프로젝트 폴더로 이동한 뒤 Claude Code를 엽니다.

```bash
cd my-project
claude
```

버전 확인:
```bash
claude --version
```

## 3. 제일 처음엔 무조건 이것부터
```text
/route-task
나는 Claude Code가 처음이야.
내 작업은 퀀트 AI 트레이딩, 공모전 설계, 경제학 질문, 바이브 코딩이야.
지금 이 요청에 맞는 팀을 골라서 시작해줘.
```

## 4. 팀이 생기면 보는 법
기본값은 `in-process` 모드입니다.

- `Shift+Down`: 팀원 바꾸기
- `Enter`: 선택한 팀원 세션 보기
- `Esc`: 현재 팀원 턴 중단
- `Ctrl+T`: shared task list 보기

## 5. 코드 작업일 때 꼭 같이 넣기
```text
Require plan approval before any changes.
```

## 6. 리더가 혼자 너무 빨리 일하면
```text
Wait for your teammates to complete their tasks before proceeding.
```

## 7. 팀 작업 끝나면 정리
```text
Clean up the team
```

## 8. 처음 추천 시작법
### 퀀트
```text
/quant-research
중소형주 모멘텀 전략을 연구하고 싶어.
데이터 누수, 거래비용, 리밸런싱 문제까지 같이 검토해줘.
```

### 공모전
```text
/competition-design
지역 경제 활성화와 AI를 엮은 공모전 아이디어를 잡고 싶어.
대학생 3명, 6주, 발표 7분 기준으로 현실적인 주제를 골라줘.
```

### 경제학
```text
/econ-explain
최저임금 인상이 고용에 미치는 영향이 왜 연구마다 다르게 나오는지
초보도 이해하게 설명해줘.
```

### 코딩
```text
/vibe-build
파이썬으로 이벤트 드리븐 백테스트 MVP를 만들고 싶어.
전략 인터페이스, 주문/체결, 포트폴리오, 테스트까지 쪼개서 진행해줘.
```
