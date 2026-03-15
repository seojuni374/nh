# data/pipeline.py — Data Pipeline Builder
# OHLCV 수집, 정제, 기술적 피처 계산, 캐싱

import os
import warnings
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional

warnings.filterwarnings("ignore")

CACHE_DIR = "output/cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def fetch_ohlcv(ticker: str, period: str = "6mo", interval: str = "1d") -> Optional[pd.DataFrame]:
    """종목 OHLCV 데이터 수집 (yfinance)"""
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if df.empty:
            return None
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df.index = pd.to_datetime(df.index)
        df = df[["Open", "Close", "High", "Low", "Volume"]].dropna()
        return df
    except Exception as e:
        print(f"  [Pipeline] {ticker} 수집 실패: {e}")
        return None


def fetch_all(tickers: list, period: str = "6mo") -> dict:
    """전체 종목 OHLCV 일괄 수집"""
    data = {}
    for ticker in tickers:
        df = fetch_ohlcv(ticker, period=period)
        if df is not None and len(df) >= 30:
            data[ticker] = df
    return data


def add_technical_features(df: pd.DataFrame, params=None) -> pd.DataFrame:
    """기술적 지표 계산 (pandas 순수 구현 — 외부 의존 없음)"""
    if params is None:
        from config import SIGNAL_PARAMS
        params = SIGNAL_PARAMS

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(params.rsi_period).mean()
    loss = (-delta.clip(upper=0)).rolling(params.rsi_period).mean()
    rs = gain / loss.replace(0, float("nan"))
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema_fast = close.ewm(span=params.macd_fast, adjust=False).mean()
    ema_slow = close.ewm(span=params.macd_slow, adjust=False).mean()
    df["MACD"] = ema_fast - ema_slow
    df["MACD_signal"] = df["MACD"].ewm(span=params.macd_signal, adjust=False).mean()
    df["MACD_hist"] = df["MACD"] - df["MACD_signal"]

    # Bollinger Bands
    sma = close.rolling(params.bb_period).mean()
    std = close.rolling(params.bb_period).std()
    df["BB_upper"] = sma + params.bb_std * std
    df["BB_lower"] = sma - params.bb_std * std
    df["BB_pct"] = (close - df["BB_lower"]) / (df["BB_upper"] - df["BB_lower"])

    # 이동평균
    df["MA20"] = close.rolling(params.ma_short).mean()
    df["MA60"] = close.rolling(params.ma_long).mean()
    df["MA_trend"] = (df["MA20"] > df["MA60"]).astype(float)

    # 거래량 이상치
    df["Volume_MA20"] = volume.rolling(20).mean()
    df["Volume_ratio"] = volume / df["Volume_MA20"].replace(0, float("nan"))

    # 전일 대비 수익률
    df["Return_1d"] = close.pct_change(1)
    df["Return_5d"] = close.pct_change(5)
    df["Return_20d"] = close.pct_change(20)

    # 52주 고저
    df["High_52w"] = high.rolling(252, min_periods=60).max()
    df["Low_52w"] = low.rolling(252, min_periods=60).min()
    df["Pct_from_52w_high"] = (close - df["High_52w"]) / df["High_52w"]

    return df


def get_latest_price(ticker: str) -> Optional[dict]:
    """단일 종목 최신 가격 정보"""
    try:
        tk = yf.Ticker(ticker)
        info = tk.fast_info
        hist = tk.history(period="2d", interval="1d")
        if hist.empty:
            return None
        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else latest
        change_pct = (latest["Close"] - prev["Close"]) / prev["Close"] * 100
        return {
            "ticker": ticker,
            "price": round(float(latest["Close"]), 2),
            "change_pct": round(float(change_pct), 2),
            "volume": int(latest["Volume"]),
            "high": round(float(latest["High"]), 2),
            "low": round(float(latest["Low"]), 2),
            "timestamp": str(hist.index[-1].date()),
        }
    except Exception as e:
        print(f"  [Pipeline] {ticker} 최신가 실패: {e}")
        return None
