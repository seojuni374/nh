# orchestrator.py — Chief Orchestrator
# 전체 파이프라인 조율: 데이터 수집 → 시그널 → 리스크 → 리포트

import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

from config import ALL_TICKERS, TICKER_NAMES, TICKER_TO_SECTOR, UNIVERSE, REPORT_DIR
from data.pipeline import fetch_all, add_technical_features
from signals.combiner import analyze_all, analyze_ticker
from risk.manager import screen_results
from report.daily_report import generate_pdf
from learning.tracker import save_predictions, evaluate_predictions, overall_accuracy
from learning.discussion import (
    load_params, save_params, apply_params_to_config,
    run_team_discussion, accuracy_trend_summary,
)


class ChiefOrchestrator:
    """
    Chief Orchestrator — 팀 전체 워크플로우 조율
    1. 데이터 수집 (Data Pipeline Builder)
    2. 시그널 계산 (Alpha Scientist)
    3. 리스크 평가 (Risk Review Engineer)
    4. PDF 보고서 생성 (Daily Report Writer)
    5. 종목 쿼리 응답
    """

    def __init__(self):
        self.last_results: List[Dict] = []
        self.last_run: Optional[str] = None
        self.data_cache: Dict = {}
        # 학습된 파라미터 로드 및 적용
        self._params = load_params()
        apply_params_to_config(self._params)

    # ─────────────────────────────────────────
    # 전체 파이프라인 실행
    # ─────────────────────────────────────────
    def run_full_pipeline(self, tickers: List[str] = None, generate_report: bool = True) -> str:
        tickers = tickers or ALL_TICKERS
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"\n{'='*60}")
        print(f"  🎼 Chief Orchestrator — 파이프라인 시작  {now}")
        print(f"{'='*60}")

        # Step 1: 데이터 수집
        print("\n[1/4] 📡 Data Pipeline Builder — OHLCV 수집 중...")
        raw_data = fetch_all(tickers)
        self.data_cache = {}
        for ticker, df in raw_data.items():
            self.data_cache[ticker] = add_technical_features(df)
        print(f"      ✓ {len(self.data_cache)}/{len(tickers)} 종목 수집 완료")

        # Step 2: 시그널 계산
        print("\n[2/4] 🧠 Alpha Scientist — 시그널 계산 중...")
        results = analyze_all(tickers, self.data_cache)
        print(f"      ✓ {len(results)} 종목 분석 완료")
        buy_n  = sum(1 for r in results if r["decision"] == "매수")
        sell_n = sum(1 for r in results if r["decision"] == "매도")
        hold_n = sum(1 for r in results if r["decision"] == "홀딩")
        print(f"      → 매수 {buy_n} | 매도 {sell_n} | 홀딩 {hold_n}")

        # Step 3: 리스크 평가
        print("\n[3/4] ⚠️  Risk Review Engineer — 리스크 스크리닝 중...")
        results = screen_results(results)
        high_risk = sum(1 for r in results if r.get("risk_level") == "HIGH")
        print(f"      ✓ 완료  (HIGH 리스크: {high_risk}종목)")

        self.last_results = results
        self.last_run = now

        # Step 4: 예측 저장 (학습용)
        print("\n[4/5] 💾 Prediction Tracker — 오늘 예측 저장 중...")
        save_predictions(results)
        print(f"      ✓ {len(results)}건 예측 기록 완료")

        # Step 5: PDF 보고서
        if generate_report:
            print("\n[5/5] 📄 Daily Report Writer — PDF 생성 중...")
            report_path = generate_pdf(results)
            print(f"      ✓ 저장 완료: {report_path}")
        else:
            report_path = None
            print("\n[5/5] 📄 PDF 생략 (--no-report)")

        print(f"\n{'='*60}")
        print(f"  ✅ 파이프라인 완료 — {now}")
        print(f"{'='*60}\n")

        return report_path or ""

    # ─────────────────────────────────────────
    # 자기학습 루프 (매일 장 마감 후 실행)
    # ─────────────────────────────────────────
    def run_learning_loop(self, days_back: int = 1) -> str:
        """
        1. N일 전 예측 vs 실제 결과 평가
        2. 팀 토의로 오답 원인 분석
        3. 파라미터 자동 조정 + 저장
        4. 다음 실행부터 조정된 파라미터 적용
        """
        print(f"\n{'='*60}")
        print(f"  🧠 팀 토의 & 자기학습 루프 시작")
        print(f"{'='*60}")

        # 평가
        print(f"\n[1/3] 📊 결과 평가 중 (D-{days_back})...")
        eval_result = evaluate_predictions(days_back=days_back)
        evaluated = eval_result.get("evaluated", 0)
        if evaluated == 0:
            msg = f"  평가할 예측 데이터 없음 (날짜: {eval_result.get('target_date','?')})"
            print(msg)
            return msg

        print(f"      적중: {eval_result['hits']}/{evaluated} = {eval_result['accuracy']:.1%}")

        # 팀 토의
        print(f"\n[2/3] 💬 팀 토의 중...")
        discussion_result = run_team_discussion(eval_result, self._params)
        print(discussion_result["discussion"])

        # 파라미터 저장 및 반영
        print(f"\n[3/3] ⚙️  파라미터 업데이트 중...")
        self._params = discussion_result["params"]
        save_params(self._params)
        apply_params_to_config(self._params)

        if discussion_result["adjusted"]:
            print(f"      ✅ 파라미터 v{self._params['version']} 저장 완료")
        else:
            print(f"      ━  변경 없음 (현 파라미터 유지)")

        print(f"\n{'='*60}")
        return discussion_result["discussion"]

    def show_learning_status(self) -> None:
        """학습 현황 출력"""
        print(f"\n{'='*60}")
        print(f"  📈 자기학습 현황")
        print(f"{'='*60}")
        stats = overall_accuracy()
        print(f"  누적 평가일: {stats['days']}일")
        print(f"  전체 적중률: {stats['avg_accuracy']:.1%}  ({stats['total_hits']}/{stats['total_evaluated']}건)")
        print(f"\n  최근 7일 추이:")
        print(accuracy_trend_summary())
        print(f"\n  현재 파라미터 (v{self._params.get('version',0)}):")
        print(f"    기술 가중치:  {self._params['weight_technical']:.2f}")
        print(f"    감성 가중치:  {self._params['weight_sentiment']:.2f}")
        print(f"    매수 임계값:  {self._params['buy_threshold']:.2f}")
        print(f"    매도 임계값:  {self._params['sell_threshold']:.2f}")
        print(f"    RSI 과매도:   {self._params['rsi_oversold']:.1f}")
        print(f"    RSI 과매수:   {self._params['rsi_overbought']:.1f}")
        print(f"{'='*60}\n")

    # ─────────────────────────────────────────
    # 종목 쿼리 응답 (사용자 요청 시)
    # ─────────────────────────────────────────
    def query_ticker(self, query: str) -> str:
        """
        자연어 또는 티커/이름으로 종목 조회
        예: "삼성전자", "NVDA", "엔비디아", "반도체 섹터"
        """
        query = query.strip()

        # 티커/이름 먼저 확인 (섹터 이름 포함 종목명 대응)
        ticker = self._resolve_ticker(query)
        if ticker:
            return self._ticker_detail(ticker)

        # 섹터 쿼리 (종목 미매칭 시)
        for sector in UNIVERSE.keys():
            if sector in query:
                return self._sector_summary(sector)

        return f"'{query}' 종목을 찾을 수 없습니다.\n사용 가능: {', '.join(TICKER_NAMES.values())}"

    def _resolve_ticker(self, query: str) -> Optional[str]:
        """이름/티커 → 티커 코드 변환"""
        q = query.upper().strip()
        # 직접 티커
        for ticker in ALL_TICKERS:
            if ticker.upper() == q or ticker.upper().replace(".KS","") == q:
                return ticker
        # 한글 이름
        for ticker, name in TICKER_NAMES.items():
            if name in query or query in name:
                return ticker
        # 영문 부분 매치
        for ticker in ALL_TICKERS:
            if q in ticker.upper():
                return ticker
        return None

    def _ticker_detail(self, ticker: str) -> str:
        """단일 종목 상세 분석 출력"""
        # 캐시 우선, 없으면 새로 분석
        df = self.data_cache.get(ticker)
        result = analyze_ticker(ticker, df)
        result = screen_results([result])[0]

        name = result.get("name", ticker)
        decision = result.get("decision", "홀딩")
        emoji = result.get("decision_emoji", "🟡")
        price = result.get("price")
        rsi = result.get("rsi")
        r1d = result.get("return_1d")
        r5d = result.get("return_5d")
        sent = result.get("sentiment_label", "-")
        score = result.get("combined_score", 0.5)
        risk_flags = result.get("risk_flags", [])
        headlines = result.get("top_headlines", [])

        def fp(p):
            if p is None: return "N/A"
            return f"₩{p:,.0f}" if ticker.endswith(".KS") else f"${p:,.2f}"

        def fpct(v):
            if v is None: return "N/A"
            return f"{'+' if v>=0 else ''}{v:.1f}%"

        lines = [
            f"{'─'*50}",
            f"  {emoji} {name}  ({ticker})",
            f"  섹터: {result.get('sector', '기타')}",
            f"{'─'*50}",
            f"  현재가    : {fp(price)}",
            f"  1일 수익률: {fpct(r1d)}",
            f"  5일 수익률: {fpct(r5d)}",
            f"  RSI       : {rsi if rsi else 'N/A'}",
            f"  뉴스 감성 : {sent}",
            f"{'─'*50}",
            f"  📊 종합점수   : {score:.3f}  (기술 {result.get('technical_score',0):.2f} | 감성 {result.get('sentiment_score',0):.2f})",
            f"  🎯 추천       : {emoji} {decision}",
        ]
        if risk_flags:
            lines.append(f"  ⚠️  리스크     : {', '.join(risk_flags)}")
        if headlines:
            lines.append(f"  📰 최근 뉴스:")
            for hl in headlines[:3]:
                if hl:
                    lines.append(f"     • {hl[:80]}")
        lines.append(f"{'─'*50}")
        return "\n".join(lines)

    def _sector_summary(self, sector: str) -> str:
        """섹터 전체 요약"""
        sector_tickers = [
            t for t, s in TICKER_TO_SECTOR.items() if s == sector
        ]
        lines = [f"\n{'─'*50}", f"  📊 [{sector}] 섹터 요약", f"{'─'*50}"]

        for ticker in sector_tickers:
            df = self.data_cache.get(ticker)
            result = analyze_ticker(ticker, df)
            name = result.get("name", ticker)
            emoji = result.get("decision_emoji", "🟡")
            decision = result.get("decision", "홀딩")
            price = result.get("price")
            r1d = result.get("return_1d")

            def fp(p):
                if p is None: return "  N/A    "
                return f"₩{p:>10,.0f}" if ticker.endswith(".KS") else f"${p:>10,.2f}"
            def fpct(v):
                if v is None: return "  N/A"
                return f"{'+' if v>=0 else ''}{v:.1f}%"

            lines.append(f"  {emoji} {name:<14} {fp(price)}  {fpct(r1d):>7}  → {decision}")

        lines.append(f"{'─'*50}")
        return "\n".join(lines)

    def print_summary(self):
        """마지막 실행 결과 콘솔 출력"""
        if not self.last_results:
            print("아직 실행 결과가 없습니다. run_full_pipeline()을 먼저 실행하세요.")
            return

        print(f"\n{'='*60}")
        print(f"  퀀트 트레이딩 시그널 요약  ({self.last_run})")
        print(f"{'='*60}")
        for sector in UNIVERSE.keys():
            items = [r for r in self.last_results if r.get("sector") == sector]
            if not items:
                continue
            print(f"\n  [{sector}]")
            for r in items:
                name = r.get("name", r["ticker"])
                emoji = r.get("decision_emoji", "🟡")
                decision = r.get("decision", "홀딩")
                score = r.get("combined_score", 0.5)
                r1d = r.get("return_1d")
                pct_str = f"{'+' if r1d>=0 else ''}{r1d:.1f}%" if r1d is not None else "N/A"
                print(f"    {emoji} {name:<16} 점수:{score:.2f}  {pct_str:>7}  → {decision}")
        print(f"\n{'='*60}")
