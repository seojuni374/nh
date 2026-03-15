# Claude Agent Teams Specialized Pro Kit

이 패키지는 **Claude Code Agent Teams 초보자용 + 실전용** 스타터입니다.

## 들어 있는 것
- 도메인별 전문 slash command skills
- Agent Teams 활성화용 `.claude/settings.local.json`
- 공통 운영 규칙용 `.claude/CLAUDE.md`
- 초보용 설명 문서
- 예시 화면이 들어간 시각 가이드 PDF

## 가장 쉬운 시작 방법
1. `.claude` 폴더를 프로젝트 루트에 복사
2. Claude Code 실행
3. `/route-task`부터 시작

## 주요 명령어
- `/route-task`
- `/quant-research`
- `/quant-build`
- `/competition-design`
- `/competition-pitch`
- `/econ-explain`
- `/econ-policy`
- `/vibe-build`
- `/vibe-refactor`
- `/audit-final`
- `/full-pipeline`

## 권장 사용 순서
### 퀀트
`/route-task -> /quant-research -> /quant-build -> /audit-final`

### 공모전
`/route-task -> /competition-design -> /competition-pitch -> /audit-final`

### 경제학
`/route-task -> /econ-explain` 또는 `/route-task -> /econ-policy`

## 중요한 규칙
- 한 세션에 한 팀만
- 같은 파일을 여러 팀원이 동시에 수정하지 않기
- 코드 작업은 plan approval 권장
- 끝나면 `Clean up the team`

## 문서
- `BEGINNER-STEP-BY-STEP.md`
- `TEAM-CATALOG.md`
- `PROMPT-COPYBOOK.md`
- `docs/Claude-Agent-Teams-visual-guide-ko.pdf`
