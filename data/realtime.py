# data/realtime.py — Real-Time Feed Engineer
# 실시간 주가 조회 (1분 인터벌, yfinance 기반)

import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Optional, List
import warnings
warnings.filterwarnings("ignore")


def get_realtime_quote(ticker: str) -> Optional[dict]:
    """단일 종목 실시간 시세 (장중 1분봉 최신값)"""
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False, auto_adjust=True)
        if df.empty:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        latest = df.iloc[-1]
        open_price = float(df.iloc[0]["Open"])
        current = float(latest["Close"])
        change_pct = (current - open_price) / open_price * 100
        return {
            "ticker": ticker,
            "current": round(current, 2),
            "open": round(open_price, 2),
            "high": round(float(df["High"].max()), 2),
            "low": round(float(df["Low"].min()), 2),
            "change_pct": round(change_pct, 2),
            "volume": int(df["Volume"].sum()),
            "last_update": str(df.index[-1]),
        }
    except Exception as e:
        print(f"  [Realtime] {ticker} 실시간 조회 실패: {e}")
        return None


def get_realtime_batch(tickers: List[str]) -> dict:
    """다수 종목 실시간 시세 일괄 조회"""
    results = {}
    for ticker in tickers:
        quote = get_realtime_quote(ticker)
        if quote:
            results[ticker] = quote
    return results


def get_intraday_chart(ticker: str, interval: str = "5m") -> Optional[pd.DataFrame]:
    """장중 차트 데이터 (기본 5분봉)"""
    try:
        df = yf.download(ticker, period="1d", interval=interval, progress=False, auto_adjust=True)
        if df.empty:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        return df
    except Exception:
        return None


def format_price(price: float, ticker: str) -> str:
    """한국 종목은 원화, 미국은 달러 포맷"""
    if ticker.endswith(".KS") or ticker.endswith(".KQ"):
        return f"₩{price:,.0f}"
    return f"${price:,.2f}"
