# risk/manager.py — Risk Review Engineer
# 포지션 가드, 손절/익절, 섹터 집중도 체크

from config import RISK_PARAMS, TICKER_TO_SECTOR
from typing import List, Dict


def check_position_risk(ticker: str, score: float, portfolio: Dict[str, float] = None) -> Dict:
    """
    종목 포지션 리스크 평가
    portfolio: {ticker: weight} 현재 포트폴리오 비중
    """
    warnings = []
    portfolio = portfolio or {}

    # 섹터 집중도 체크
    sector = TICKER_TO_SECTOR.get(ticker, "기타")
    sector_weight = sum(
        w for t, w in portfolio.items()
        if TICKER_TO_SECTOR.get(t) == sector
    )
    if sector_weight > RISK_PARAMS.max_sector_pct:
        warnings.append(f"섹터({sector}) 집중도 초과: {sector_weight:.0%} > {RISK_PARAMS.max_sector_pct:.0%}")

    # 단일 종목 비중 체크
    pos_weight = portfolio.get(ticker, 0)
    if pos_weight > RISK_PARAMS.max_position_pct:
        warnings.append(f"단일 종목 비중 초과: {pos_weight:.0%} > {RISK_PARAMS.max_position_pct:.0%}")

    return {
        "ticker": ticker,
        "sector": sector,
        "risk_ok": len(warnings) == 0,
        "warnings": warnings,
    }


def apply_stop_loss(ticker: str, entry_price: float, current_price: float) -> Dict:
    """손절/익절 체크"""
    change = (current_price - entry_price) / entry_price
    action = None
    if change <= RISK_PARAMS.stop_loss_pct:
        action = "손절"
    elif change >= RISK_PARAMS.take_profit_pct:
        action = "익절"
    return {
        "ticker": ticker,
        "change_pct": round(change * 100, 2),
        "action": action,
        "stop_loss": RISK_PARAMS.stop_loss_pct * 100,
        "take_profit": RISK_PARAMS.take_profit_pct * 100,
    }


def screen_results(results: List[Dict]) -> List[Dict]:
    """분석 결과에 리스크 등급 추가"""
    for r in results:
        score = r.get("combined_score", 0.5)
        rsi = r.get("rsi")
        ret_1d = r.get("return_1d", 0) or 0

        risk_flags = []
        if rsi and rsi > 75:
            risk_flags.append("RSI 과매수")
        if rsi and rsi < 25:
            risk_flags.append("RSI 극단 과매도")
        if ret_1d and abs(ret_1d) > 8:
            risk_flags.append(f"일간 급변동 {ret_1d:+.1f}%")

        r["risk_flags"] = risk_flags
        r["risk_level"] = "HIGH" if len(risk_flags) >= 2 else "MED" if risk_flags else "LOW"

    return results
