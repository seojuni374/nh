# data/news.py — Data Pipeline Builder (뉴스 담당)
# yfinance 내장 뉴스 수집 + 감성 키워드 스코어링

import yfinance as yf
from typing import List, Dict, Optional
from datetime import datetime
import re


def fetch_news(ticker: str, max_items: int = 10) -> List[Dict]:
    """종목 뉴스 수집 (yfinance)"""
    try:
        tk = yf.Ticker(ticker)
        news = tk.news
        if not news:
            return []
        results = []
        for item in news[:max_items]:
            content = item.get("content", {})
            title = (
                content.get("title", "")
                if isinstance(content, dict)
                else str(content)
            )
            pub_date = item.get("providerPublishTime") or item.get("pubDate", "")
            if isinstance(pub_date, (int, float)):
                pub_date = datetime.fromtimestamp(pub_date).strftime("%Y-%m-%d %H:%M")
            results.append({
                "ticker": ticker,
                "title": title,
                "date": str(pub_date),
                "url": item.get("link", ""),
            })
        return results
    except Exception as e:
        print(f"  [News] {ticker} 뉴스 수집 실패: {e}")
        return []


def score_sentiment(text: str, positive_kw: List[str], negative_kw: List[str]) -> float:
    """
    키워드 기반 감성 점수 [-1.0 ~ +1.0]
    룩어헤드 바이어스 주의: 이 함수는 이미 공개된 뉴스에만 적용
    """
    text_lower = text.lower()
    pos = sum(1 for kw in positive_kw if kw.lower() in text_lower)
    neg = sum(1 for kw in negative_kw if kw.lower() in text_lower)
    total = pos + neg
    if total == 0:
        return 0.0
    return round((pos - neg) / total, 4)


def get_news_sentiment(ticker: str) -> Dict:
    """종목 뉴스 수집 + 감성 점수 계산"""
    from config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS

    articles = fetch_news(ticker)
    if not articles:
        return {"ticker": ticker, "score": 0.0, "articles": [], "summary": "뉴스 없음",
                "headline_count": 0, "positive_count": 0, "negative_count": 0}

    scores = [
        score_sentiment(a["title"], POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS)
        for a in articles
    ]
    avg_score = round(sum(scores) / len(scores), 4) if scores else 0.0

    return {
        "ticker": ticker,
        "score": avg_score,
        "articles": articles[:5],
        "headline_count": len(articles),
        "positive_count": sum(1 for s in scores if s > 0),
        "negative_count": sum(1 for s in scores if s < 0),
        "summary": _sentiment_label(avg_score),
    }


def _sentiment_label(score: float) -> str:
    if score > 0.3:
        return "긍정적"
    elif score > 0.0:
        return "약긍정"
    elif score == 0.0:
        return "중립"
    elif score > -0.3:
        return "약부정"
    else:
        return "부정적"
