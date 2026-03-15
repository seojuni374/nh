# learning/discussion.py — Chief Orchestrator 주관 팀 토의
# 매일 예측 결과를 검토하고, 팀원들이 토의해 가중치·임계값을 자동 조정

import json
import os
from datetime import datetime
from typing import Dict, List

PARAMS_FILE = "output/learned_params.json"


# ─────────────────────────────────────────
# 학습된 파라미터 로드/저장
# ─────────────────────────────────────────
def load_params() -> Dict:
    """저장된 학습 파라미터 로드 (없으면 기본값)"""
    defaults = {
        "weight_technical": 0.60,
        "weight_sentiment": 0.40,
        "buy_threshold": 0.55,
        "sell_threshold": 0.40,
        "rsi_oversold": 35.0,
        "rsi_overbought": 65.0,
        "version": 0,
        "last_updated": None,
        "adjustment_history": [],
    }
    if not os.path.exists(PARAMS_FILE):
        return defaults
    with open(PARAMS_FILE, "r", encoding="utf-8") as f:
        try:
            saved = json.load(f)
            defaults.update(saved)
            return defaults
        except Exception:
            return defaults


def save_params(params: Dict) -> None:
    with open(PARAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(params, f, ensure_ascii=False, indent=2)


def apply_params_to_config(params: Dict) -> None:
    """학습된 파라미터를 SignalParams에 반영"""
    from config import SIGNAL_PARAMS
    SIGNAL_PARAMS.weight_technical = params["weight_technical"]
    SIGNAL_PARAMS.weight_sentiment = params["weight_sentiment"]
    SIGNAL_PARAMS.buy_threshold    = params["buy_threshold"]
    SIGNAL_PARAMS.sell_threshold   = params["sell_threshold"]
    SIGNAL_PARAMS.rsi_oversold     = params["rsi_oversold"]
    SIGNAL_PARAMS.rsi_overbought   = params["rsi_overbought"]


# ─────────────────────────────────────────
# 팀 토의 시뮬레이션
# ─────────────────────────────────────────
def run_team_discussion(eval_result: Dict, params: Dict) -> Dict:
    """
    Chief Orchestrator 주관 팀 토의:
    오답 패턴을 분석하고 파라미터 조정 방향을 결정

    Returns: 조정된 params + 토의 로그
    """
    details     = eval_result.get("details", [])
    accuracy    = eval_result.get("accuracy", 0.5)
    target_date = eval_result.get("target_date", "?")
    discussion  = []

    discussion.append(f"{'='*60}")
    discussion.append(f"🎼 Chief Orchestrator — 팀 토의 개시")
    discussion.append(f"   검토 날짜: {target_date}  |  적중률: {accuracy:.1%}  ({eval_result.get('hits',0)}/{eval_result.get('evaluated',0)})")
    discussion.append(f"{'='*60}")

    if not details:
        discussion.append("  [데이터 부족 — 토의 생략]")
        return {"params": params, "discussion": "\n".join(discussion), "adjusted": False}

    # ── 오답 분류 ────────────────────────────────────────────
    missed_buys  = [d for d in details if d["predicted"] == "매수" and not d["hit"]]  # 매수 틀림
    missed_sells = [d for d in details if d["predicted"] == "매도" and not d["hit"]]  # 매도 틀림
    missed_holds = [d for d in details if d["predicted"] == "홀딩" and not d["hit"]]  # 홀딩 틀림 (급변)
    correct      = [d for d in details if d["hit"]]

    # ── 팀원 발언 ─────────────────────────────────────────────
    discussion.append("")
    discussion.append("① Backtest Skeptic:")
    if len(missed_buys) > len(missed_sells):
        discussion.append(f"   매수 오신호가 {len(missed_buys)}건으로 많습니다. buy_threshold를 올려야 합니다.")
        action = "raise_buy"
    elif len(missed_sells) > len(missed_buys):
        discussion.append(f"   매도 오신호가 {len(missed_sells)}건입니다. sell_threshold를 낮춰야 합니다.")
        action = "raise_sell"
    else:
        discussion.append(f"   매수/매도 오답 균형적. 임계값 유지, 가중치 조정 검토.")
        action = "balance"

    # 감성 vs 기술 오답 분석
    avg_tech_miss = _avg(d.get("score", 0.5) for d in (missed_buys + missed_sells))
    avg_sent_corr = _avg(d.get("score", 0.5) for d in correct)

    discussion.append("")
    discussion.append("② Alpha Scientist:")
    if missed_buys and avg_tech_miss > 0.5:
        discussion.append(f"   오답 종목의 기술 점수 평균이 {avg_tech_miss:.2f}로 높음.")
        discussion.append(f"   뉴스 감성이 실제 방향과 달랐을 가능성 → 기술 가중치 소폭 상향.")
        tech_adj = +0.02
    elif missed_sells:
        discussion.append(f"   매도 오신호 분석: 감성 과신 가능성 → 감성 가중치 소폭 하향.")
        tech_adj = +0.03
    else:
        discussion.append(f"   오답 패턴 불명확. 가중치 미조정.")
        tech_adj = 0.0

    discussion.append("")
    discussion.append("③ Regime Strategist:")
    avg_return_miss = _avg(abs(d.get("actual_return", 0)) for d in (missed_buys + missed_sells))
    if avg_return_miss > 3.0:
        discussion.append(f"   오답의 평균 변동폭 {avg_return_miss:.1f}% — 시장 급변 구간.")
        discussion.append(f"   RSI 임계값을 조정해 과민 반응 완화.")
        rsi_adj = +1.0
    else:
        discussion.append(f"   시장 급변 아님. RSI 임계값 유지.")
        rsi_adj = 0.0

    discussion.append("")
    discussion.append("④ Execution & Risk Officer:")
    discussion.append(f"   오늘 적중률 {accuracy:.1%}. 목표 60% 기준 {'상회' if accuracy >= 0.6 else '미달'}.")
    if accuracy < 0.4:
        discussion.append(f"   심각한 저조 → 전반적 임계값 완화 (홀딩 범위 확대).")
        threshold_adj = -0.02
    elif accuracy > 0.75:
        discussion.append(f"   고적중률 유지 중 → 파라미터 소폭 보수화.")
        threshold_adj = +0.01
    else:
        threshold_adj = 0.0

    # ── 파라미터 조정 적용 ────────────────────────────────────
    new_params = dict(params)
    adjusted = False

    # 기술/감성 가중치
    if abs(tech_adj) > 0:
        new_tech = min(max(params["weight_technical"] + tech_adj, 0.4), 0.8)
        new_sent = 1.0 - new_tech
        new_params["weight_technical"] = round(new_tech, 3)
        new_params["weight_sentiment"] = round(new_sent, 3)
        adjusted = True

    # 매수 임계값
    if action == "raise_buy":
        new_params["buy_threshold"] = round(min(params["buy_threshold"] + 0.02, 0.72), 3)
        adjusted = True
    elif threshold_adj != 0:
        new_params["buy_threshold"]  = round(min(max(params["buy_threshold"]  + threshold_adj, 0.50), 0.72), 3)
        new_params["sell_threshold"] = round(min(max(params["sell_threshold"] - threshold_adj, 0.28), 0.48), 3)
        adjusted = True

    # RSI 임계값
    if rsi_adj != 0:
        new_params["rsi_oversold"]   = round(min(max(params["rsi_oversold"]   + rsi_adj, 25), 45), 1)
        new_params["rsi_overbought"] = round(min(max(params["rsi_overbought"] - rsi_adj, 55), 75), 1)
        adjusted = True

    discussion.append("")
    discussion.append("🎼 Chief Orchestrator — 결론:")
    if adjusted:
        discussion.append(f"   기술 가중치: {params['weight_technical']:.2f} → {new_params['weight_technical']:.2f}")
        discussion.append(f"   감성 가중치: {params['weight_sentiment']:.2f} → {new_params['weight_sentiment']:.2f}")
        discussion.append(f"   매수 임계값: {params['buy_threshold']:.2f} → {new_params['buy_threshold']:.2f}")
        discussion.append(f"   RSI 과매도:  {params['rsi_oversold']:.1f} → {new_params['rsi_oversold']:.1f}")
        discussion.append(f"   ✅ 파라미터 업데이트 적용.")
    else:
        discussion.append("   변경 없음 — 현 파라미터 유지.")

    # 히스토리 기록
    new_params["version"] = params.get("version", 0) + (1 if adjusted else 0)
    new_params["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    history = params.get("adjustment_history", [])
    history.append({
        "date": target_date,
        "accuracy": accuracy,
        "adjusted": adjusted,
        "buy_threshold": new_params["buy_threshold"],
        "weight_technical": new_params["weight_technical"],
    })
    new_params["adjustment_history"] = history[-30:]  # 최근 30일 보관

    discussion.append(f"{'='*60}")

    return {
        "params": new_params,
        "discussion": "\n".join(discussion),
        "adjusted": adjusted,
    }


def _avg(iterable) -> float:
    lst = list(iterable)
    return sum(lst) / len(lst) if lst else 0.0


# ─────────────────────────────────────────
# 적중률 트렌드 요약
# ─────────────────────────────────────────
def accuracy_trend_summary() -> str:
    from learning.tracker import load_accuracy_history
    history = load_accuracy_history()
    if not history:
        return "  아직 누적 데이터 없음 (내일부터 집계 시작)"

    lines = ["  날짜            적중률   적중/평가"]
    for h in history[-7:]:
        bar = "█" * int(h["accuracy"] * 10) + "░" * (10 - int(h["accuracy"] * 10))
        lines.append(f"  {h['target_date']}  {h['accuracy']:.1%}  [{bar}]  {h['hits']}/{h['evaluated']}")

    if len(history) >= 2:
        recent = history[-1]["accuracy"]
        prev   = history[-2]["accuracy"]
        trend  = "▲ 개선" if recent > prev else ("▼ 하락" if recent < prev else "━ 유지")
        lines.append(f"\n  최근 추세: {trend}  ({prev:.1%} → {recent:.1%})")

    params = load_params()
    lines.append(f"  파라미터 버전: v{params.get('version', 0)}  (마지막 업데이트: {params.get('last_updated', '-')})")
    return "\n".join(lines)
