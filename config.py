# config.py — Chief Orchestrator 설정 파일
# 섹터, 종목 유니버스, 파라미터 중앙 관리

from dataclasses import dataclass, field
from typing import Dict, List

# ─────────────────────────────────────────
# 섹터별 종목 유니버스
# ─────────────────────────────────────────
UNIVERSE: Dict[str, Dict[str, List[str]]] = {
    "반도체": {
        "KOSPI": ["005930.KS", "000660.KS", "042700.KS"],   # 삼성전자, SK하이닉스, 한미반도체
        "NASDAQ": ["NVDA", "AMD", "INTC", "ASML"],
    },
    "AI": {
        "KOSPI": ["035420.KS", "035720.KS", "377300.KS"],   # 네이버, 카카오, 카카오페이
        "NASDAQ": ["MSFT", "GOOGL", "META", "PLTR"],
    },
    "전력": {
        "KOSPI": ["015760.KS", "010120.KS", "298040.KS"],   # 한국전력, LS일렉트릭, 효성중공업
        "NASDAQ": ["NEE", "AES", "VST", "GEV"],
    },
    "원자력": {
        "KOSPI": ["034020.KS", "229640.KS", "051600.KS"],   # 두산에너빌리티, 한전기술, 한전KPS
        "NASDAQ": ["CEG", "CCJ", "NNE", "SMR"],
    },
    "우주": {
        "KOSPI": ["012450.KS", "144510.KS", "099550.KS"],   # 한화에어로스페이스, AP위성, 쎄트렉아이
        "NASDAQ": ["RKLB", "LUNR", "ASTS", "BA"],
    },
}

# 모든 종목 flat list
ALL_TICKERS: List[str] = [
    ticker
    for sector in UNIVERSE.values()
    for market_tickers in sector.values()
    for ticker in market_tickers
]

# 종목 → 섹터 역매핑
TICKER_TO_SECTOR: Dict[str, str] = {
    ticker: sector
    for sector, markets in UNIVERSE.items()
    for market_tickers in markets.values()
    for ticker in market_tickers
}

# 종목 한글 이름 매핑
TICKER_NAMES: Dict[str, str] = {
    # 반도체
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "042700.KS": "한미반도체",
    "NVDA": "엔비디아",
    "AMD": "AMD",
    "INTC": "인텔",
    "ASML": "ASML",
    # AI
    "035420.KS": "네이버",
    "035720.KS": "카카오",
    "377300.KS": "카카오페이",
    "MSFT": "마이크로소프트",
    "GOOGL": "구글",
    "META": "메타",
    "PLTR": "팔란티어",
    # 전력
    "015760.KS": "한국전력",
    "010120.KS": "LS일렉트릭",
    "298040.KS": "효성중공업",
    "NEE": "넥스트에라에너지",
    "AES": "AES",
    "VST": "비스트라에너지",
    "GEV": "GE버노바",
    # 원자력
    "034020.KS": "두산에너빌리티",
    "229640.KS": "한전기술",
    "051600.KS": "한전KPS",
    "CEG": "콘스텔레이션에너지",
    "CCJ": "카메코",
    "NNE": "나누",
    "SMR": "NuScale",
    # 우주
    "012450.KS": "한화에어로스페이스",
    "144510.KS": "AP위성",
    "099550.KS": "쎄트렉아이",
    "RKLB": "로켓랩",
    "LUNR": "인튜이티브머신스",
    "ASTS": "AST스페이스모바일",
    "BA": "보잉",
}

# ─────────────────────────────────────────
# 시그널 파라미터
# ─────────────────────────────────────────
@dataclass
class SignalParams:
    rsi_period: int = 14
    rsi_oversold: float = 35.0
    rsi_overbought: float = 65.0
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    bb_period: int = 20
    bb_std: float = 2.0
    ma_short: int = 20
    ma_long: int = 60
    weight_technical: float = 0.6
    weight_sentiment: float = 0.4
    buy_threshold: float = 0.55
    sell_threshold: float = 0.40

SIGNAL_PARAMS = SignalParams()

# ─────────────────────────────────────────
# 리스크 파라미터
# ─────────────────────────────────────────
@dataclass
class RiskParams:
    max_position_pct: float = 0.08     # 종목당 최대 8%
    max_sector_pct: float = 0.30       # 섹터당 최대 30%
    stop_loss_pct: float = -0.07       # 손절 -7%
    take_profit_pct: float = 0.15      # 익절 +15%

RISK_PARAMS = RiskParams()

# ─────────────────────────────────────────
# 뉴스 감성 키워드
# ─────────────────────────────────────────
POSITIVE_KEYWORDS = [
    "상승", "급등", "신고가", "호실적", "수주", "계약", "흑자", "성장",
    "bull", "surge", "record", "beat", "upgrade", "buy", "outperform",
    "breakthrough", "win", "profit", "growth", "expansion",
]
NEGATIVE_KEYWORDS = [
    "하락", "급락", "신저가", "적자", "손실", "소송", "리콜", "감산",
    "bear", "drop", "miss", "downgrade", "sell", "underperform",
    "lawsuit", "loss", "decline", "cut", "warning",
]

# ─────────────────────────────────────────
# 출력 경로
# ─────────────────────────────────────────
OUTPUT_DIR = "output"
REPORT_DIR = "output/reports"
