# signals/combiner.py — Alpha Scientist (시그널 통합)

from config import SIGNAL_PARAMS, TICKER_NAMES, TICKER_TO_SECTOR
from signals.technical import compute_technical_score
from signals.sentiment import compute_sentiment_score
from data.pipeline import add_technical_features, fetch_ohlcv


def DECISION(score: float) -> str:
    if score >= SIGNAL_PARAMS.buy_threshold:
        return "매수"
    elif score <= SIGNAL_PARAMS.sell_threshold:
        return "매도"
    return "홀딩"


def DECISION_EN(score: float) -> str:
    d = DECISION(score)
    return {"매수": "BUY", "매도": "SELL", "홀딩": "HOLD"}[d]


def DECISION_EMOJI(score: float) -> str:
    d = DECISION(score)
    return {"매수": "🟢", "매도": "🔴", "홀딩": "🟡"}[d]


def analyze_ticker(ticker: str, df=None) -> dict:
    """
    단일 종목 종합 분석
    df: 이미 피처가 계산된 DataFrame (없으면 새로 수집)
    """
    # 데이터 수집 및 피처 계산
    if df is None:
        raw = fetch_ohlcv(ticker)
        if raw is None:
            return _empty_result(ticker, "데이터 수집 실패")
        df = add_technical_features(raw)

    tech = compute_technical_score(df)
    sent = compute_sentiment_score(ticker)

    w_t = SIGNAL_PARAMS.weight_technical
    w_s = SIGNAL_PARAMS.weight_sentiment
    combined = w_t * tech["score"] + w_s * sent["score"]

    latest = df.iloc[-1]

    return {
        "ticker": ticker,
        "name": TICKER_NAMES.get(ticker, ticker),
        "sector": TICKER_TO_SECTOR.get(ticker, "기타"),
        "price": round(float(latest["Close"]), 2),
        "decision": DECISION(combined),
        "decision_emoji": DECISION_EMOJI(combined),
        "combined_score": round(combined, 4),
        "technical_score": tech["score"],
        "sentiment_score": sent["score"],
        "rsi": tech.get("rsi"),
        "return_1d": tech.get("return_1d"),
        "return_5d": tech.get("return_5d"),
        "pct_from_52w_high": tech.get("pct_from_52w_high"),
        "sentiment_label": sent["label"],
        "top_headlines": sent["top_headlines"],
        "tech_signals": tech["signals"],
    }


def analyze_all(tickers: list, data_dict: dict = None) -> list:
    """전체 종목 일괄 분석"""
    results = []
    for ticker in tickers:
        df = data_dict.get(ticker) if data_dict else None
        result = analyze_ticker(ticker, df)
        results.append(result)
    results.sort(key=lambda x: x["combined_score"], reverse=True)
    return results


def _empty_result(ticker: str, reason: str) -> dict:
    return {
        "ticker": ticker,
        "name": TICKER_NAMES.get(ticker, ticker),
        "sector": TICKER_TO_SECTOR.get(ticker, "기타"),
        "price": None,
        "decision": "홀딩",
        "decision_emoji": "🟡",
        "combined_score": 0.5,
        "technical_score": 0.5,
        "sentiment_score": 0.5,
        "rsi": None,
        "return_1d": None,
        "return_5d": None,
        "pct_from_52w_high": None,
        "sentiment_label": "데이터 없음",
        "top_headlines": [],
        "tech_signals": {},
        "error": reason,
    }
