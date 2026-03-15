# learning/tracker.py — Backtest Skeptic + Data Validation Engineer
# 매일 예측을 저장하고, 다음날 실제 결과와 비교해 적중률 추적

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd

PRED_LOG = "output/predictions.jsonl"
ACCURACY_LOG = "output/accuracy_log.json"
os.makedirs("output", exist_ok=True)


# ─────────────────────────────────────────
# 예측 저장
# ─────────────────────────────────────────
def save_predictions(results: List[Dict]) -> None:
    """오늘 예측 결과를 JSONL로 저장"""
    today = datetime.now().strftime("%Y-%m-%d")
    with open(PRED_LOG, "a", encoding="utf-8") as f:
        for r in results:
            record = {
                "date": today,
                "ticker": r["ticker"],
                "name": r.get("name", r["ticker"]),
                "price": r.get("price"),
                "decision": r.get("decision"),
                "combined_score": r.get("combined_score"),
                "technical_score": r.get("technical_score"),
                "sentiment_score": r.get("sentiment_score"),
                "rsi": r.get("rsi"),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ─────────────────────────────────────────
# 결과 검증
# ─────────────────────────────────────────
def evaluate_predictions(days_back: int = 1) -> Dict:
    """
    N일 전 예측 vs 실제 가격 변동 비교
    매수 → 다음날 +수익률이면 적중
    매도 → 다음날 -수익률이면 적중
    홀딩 → 절대값 3% 미만이면 적중
    """
    import yfinance as yf

    if not os.path.exists(PRED_LOG):
        return {"evaluated": 0, "hits": 0, "accuracy": 0.0, "details": []}

    target_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    records = []
    with open(PRED_LOG, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line.strip())
            if r["date"] == target_date:
                records.append(r)

    if not records:
        return {"evaluated": 0, "hits": 0, "accuracy": 0.0, "details": [],
                "target_date": target_date}

    details = []
    hits = 0

    for r in records:
        ticker = r["ticker"]
        entry_price = r.get("price")
        if entry_price is None:
            continue

        try:
            df = yf.download(ticker, period="5d", interval="1d", progress=False, auto_adjust=True)
            if df.empty or len(df) < 2:
                continue
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            # 예측일 다음 거래일 종가
            actual_price = float(df["Close"].iloc[-1])
            actual_return = (actual_price - entry_price) / entry_price * 100
        except Exception:
            continue

        decision = r["decision"]
        if decision == "매수" and actual_return > 0.5:
            hit = True
        elif decision == "매도" and actual_return < -0.5:
            hit = True
        elif decision == "홀딩" and abs(actual_return) < 3.0:
            hit = True
        else:
            hit = False

        if hit:
            hits += 1

        details.append({
            "ticker": ticker,
            "name": r.get("name", ticker),
            "predicted": decision,
            "entry_price": round(entry_price, 2),
            "actual_price": round(actual_price, 2),
            "actual_return": round(actual_return, 2),
            "hit": hit,
            "score": r.get("combined_score"),
        })

    total = len(details)
    accuracy = hits / total if total > 0 else 0.0

    result = {
        "target_date": target_date,
        "evaluated": total,
        "hits": hits,
        "misses": total - hits,
        "accuracy": round(accuracy, 4),
        "details": details,
    }

    _append_accuracy_log(result)
    return result


def _append_accuracy_log(result: Dict) -> None:
    """누적 적중률 로그 저장"""
    log = []
    if os.path.exists(ACCURACY_LOG):
        with open(ACCURACY_LOG, "r", encoding="utf-8") as f:
            try:
                log = json.load(f)
            except Exception:
                log = []
    # 같은 날짜 중복 방지
    log = [x for x in log if x.get("target_date") != result["target_date"]]
    log.append({
        "target_date": result["target_date"],
        "accuracy": result["accuracy"],
        "hits": result["hits"],
        "evaluated": result["evaluated"],
    })
    with open(ACCURACY_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def load_accuracy_history() -> List[Dict]:
    """누적 적중률 이력 로드"""
    if not os.path.exists(ACCURACY_LOG):
        return []
    with open(ACCURACY_LOG, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def overall_accuracy() -> Dict:
    """전체 기간 평균 적중률"""
    history = load_accuracy_history()
    if not history:
        return {"days": 0, "avg_accuracy": 0.0, "total_hits": 0, "total_evaluated": 0}
    total_hits = sum(h["hits"] for h in history)
    total_eval = sum(h["evaluated"] for h in history)
    return {
        "days": len(history),
        "avg_accuracy": round(total_hits / total_eval, 4) if total_eval > 0 else 0.0,
        "total_hits": total_hits,
        "total_evaluated": total_eval,
        "history": history[-10:],  # 최근 10일
    }
