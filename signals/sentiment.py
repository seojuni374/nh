# signals/sentiment.py — Alpha Scientist (뉴스 감성 시그널)

from data.news import get_news_sentiment


def compute_sentiment_score(ticker: str) -> dict:
    """
    뉴스 감성 점수를 0~1 시그널로 변환
    -1.0 ~ +1.0 감성 → 0.0 ~ 1.0 시그널
    """
    result = get_news_sentiment(ticker)
    raw_score = result["score"]   # -1.0 ~ +1.0

    # 선형 변환: -1 → 0.1, 0 → 0.5, +1 → 0.9
    signal = 0.5 + raw_score * 0.4

    return {
        "score": round(min(max(signal, 0.0), 1.0), 4),
        "raw_sentiment": raw_score,
        "label": result["summary"],
        "headline_count": result["headline_count"],
        "positive": result["positive_count"],
        "negative": result["negative_count"],
        "top_headlines": [a["title"] for a in result["articles"][:3]],
    }
