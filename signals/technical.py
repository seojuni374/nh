# signals/technical.py — Alpha Scientist (차트 시그널)

import pandas as pd
from typing import Optional
from config import SIGNAL_PARAMS


def compute_technical_score(df: pd.DataFrame) -> dict:
    """
    최신 기술적 지표로 0~1 점수 계산
    0.0 = 강한 매도, 1.0 = 강한 매수
    """
    if df is None or len(df) < 30:
        return {"score": 0.5, "signals": {}, "detail": "데이터 부족"}

    row = df.iloc[-1]
    signals = {}
    score_components = []

    # ── RSI ─────────────────────────────
    rsi = row.get("RSI")
    if pd.notna(rsi):
        if rsi < SIGNAL_PARAMS.rsi_oversold:
            s = 0.8    # 과매도 → 매수
        elif rsi > SIGNAL_PARAMS.rsi_overbought:
            s = 0.2    # 과매수 → 매도
        else:
            s = 0.5 + (SIGNAL_PARAMS.rsi_oversold - rsi) / (SIGNAL_PARAMS.rsi_oversold * 2) * 0.3
        signals["RSI"] = {"value": round(float(rsi), 1), "score": round(s, 3)}
        score_components.append(s)

    # ── MACD ────────────────────────────
    macd_hist = row.get("MACD_hist")
    macd = row.get("MACD")
    if pd.notna(macd_hist) and pd.notna(macd):
        s = 0.65 if macd_hist > 0 and macd > 0 else \
            0.55 if macd_hist > 0 else \
            0.45 if macd_hist < 0 and macd < 0 else 0.35
        signals["MACD"] = {"hist": round(float(macd_hist), 4), "score": round(s, 3)}
        score_components.append(s)

    # ── 볼린저 밴드 ──────────────────────
    bb_pct = row.get("BB_pct")
    if pd.notna(bb_pct):
        if bb_pct < 0.2:
            s = 0.75   # 하단 근접 → 매수
        elif bb_pct > 0.8:
            s = 0.25   # 상단 근접 → 매도
        else:
            s = 0.5
        signals["BB"] = {"pct": round(float(bb_pct), 3), "score": round(s, 3)}
        score_components.append(s)

    # ── 이동평균 추세 ────────────────────
    ma_trend = row.get("MA_trend")
    if pd.notna(ma_trend):
        s = 0.65 if ma_trend == 1 else 0.35
        signals["MA_trend"] = {"value": "상승" if ma_trend == 1 else "하락", "score": round(s, 3)}
        score_components.append(s)

    # ── 거래량 ──────────────────────────
    vol_ratio = row.get("Volume_ratio")
    if pd.notna(vol_ratio) and vol_ratio > 1.5:
        # 거래량 급증 시 추세 강화
        boost = 0.05 if (ma_trend == 1 if pd.notna(ma_trend) else False) else -0.05
        score_components = [s + boost for s in score_components]

    total_score = sum(score_components) / len(score_components) if score_components else 0.5

    return {
        "score": round(min(max(total_score, 0.0), 1.0), 4),
        "signals": signals,
        "rsi": round(float(rsi), 1) if pd.notna(rsi) else None,
        "return_1d": round(float(row.get("Return_1d", 0)) * 100, 2),
        "return_5d": round(float(row.get("Return_5d", 0)) * 100, 2),
        "pct_from_52w_high": round(float(row.get("Pct_from_52w_high", 0)) * 100, 2),
    }
