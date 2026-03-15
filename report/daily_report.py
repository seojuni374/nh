# report/daily_report.py — Daily Report Writer
# PDF 일간 보고서 자동 생성 (reportlab)

import os
from datetime import datetime
from typing import List, Dict
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import UNIVERSE, OUTPUT_DIR, REPORT_DIR

os.makedirs(REPORT_DIR, exist_ok=True)

# ── 폰트 등록 (나눔고딕 또는 시스템 폰트) ─────────────────────
FONT_NAME = "Helvetica"  # 폴백

def _register_korean_font():
    global FONT_NAME
    font_paths = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("KoreanFont", path))
                FONT_NAME = "KoreanFont"
                return
            except Exception:
                continue

_register_korean_font()


# ── 색상 정의 ──────────────────────────────────────────────────
COLOR_BUY    = colors.HexColor("#1a7c3e")
COLOR_SELL   = colors.HexColor("#c0392b")
COLOR_HOLD   = colors.HexColor("#d4a017")
COLOR_HEADER = colors.HexColor("#1a1a2e")
COLOR_SUB    = colors.HexColor("#16213e")
COLOR_LIGHT  = colors.HexColor("#f0f4f8")
COLOR_BORDER = colors.HexColor("#cccccc")


def _decision_color(decision: str):
    return {"매수": COLOR_BUY, "매도": COLOR_SELL, "홀딩": COLOR_HOLD}.get(decision, COLOR_HOLD)


def _get_styles():
    styles = getSampleStyleSheet()
    base = {"fontName": FONT_NAME, "leading": 14}
    return {
        "title": ParagraphStyle("title", fontName=FONT_NAME, fontSize=20, textColor=colors.white,
                                 alignment=TA_CENTER, leading=26, spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle", fontName=FONT_NAME, fontSize=11, textColor=colors.lightgrey,
                                    alignment=TA_CENTER, leading=16),
        "section": ParagraphStyle("section", fontName=FONT_NAME, fontSize=13, textColor=COLOR_HEADER,
                                   leading=18, spaceBefore=12, spaceAfter=6, fontWeight="Bold"),
        "body": ParagraphStyle("body", fontName=FONT_NAME, fontSize=9, textColor=colors.black, leading=13),
        "small": ParagraphStyle("small", fontName=FONT_NAME, fontSize=8, textColor=colors.grey, leading=11),
        "headline": ParagraphStyle("headline", fontName=FONT_NAME, fontSize=8, textColor=colors.HexColor("#333"),
                                    leading=11, leftIndent=8),
        "summary_buy": ParagraphStyle("s_buy", fontName=FONT_NAME, fontSize=10, textColor=COLOR_BUY,
                                       leading=14, alignment=TA_CENTER),
        "summary_sell": ParagraphStyle("s_sell", fontName=FONT_NAME, fontSize=10, textColor=COLOR_SELL,
                                        leading=14, alignment=TA_CENTER),
        "summary_hold": ParagraphStyle("s_hold", fontName=FONT_NAME, fontSize=10, textColor=COLOR_HOLD,
                                        leading=14, alignment=TA_CENTER),
    }


def _fmt_price(price, ticker: str) -> str:
    if price is None:
        return "N/A"
    if ticker.endswith(".KS") or ticker.endswith(".KQ"):
        return f"₩{price:,.0f}"
    return f"${price:,.2f}"


def _fmt_pct(val) -> str:
    if val is None:
        return "N/A"
    sign = "+" if val >= 0 else ""
    return f"{sign}{val:.1f}%"


def generate_pdf(results: List[Dict], output_path: str = None) -> str:
    """PDF 일간 보고서 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    if output_path is None:
        output_path = os.path.join(REPORT_DIR, f"quant_daily_{today}.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )

    styles = _get_styles()
    story = []

    # ── 헤더 배너 ────────────────────────────────────────────
    header_data = [[
        Paragraph(f"퀀트 트레이딩 일간 보고서", styles["title"]),
    ]]
    header_table = Table(header_data, colWidths=[doc.width])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), COLOR_HEADER),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(header_table)

    now_str = datetime.now().strftime("%Y년 %m월 %d일  %H:%M 기준")
    story.append(Paragraph(now_str, styles["subtitle"]))
    story.append(Spacer(1, 0.4*cm))

    # ── 요약 카드 ────────────────────────────────────────────
    buy_list  = [r for r in results if r.get("decision") == "매수"]
    sell_list = [r for r in results if r.get("decision") == "매도"]
    hold_list = [r for r in results if r.get("decision") == "홀딩"]

    summary_data = [[
        Paragraph(f"🟢 매수\n{len(buy_list)}종목", styles["summary_buy"]),
        Paragraph(f"🔴 매도\n{len(sell_list)}종목", styles["summary_sell"]),
        Paragraph(f"🟡 홀딩\n{len(hold_list)}종목", styles["summary_hold"]),
    ]]
    summary_table = Table(summary_data, colWidths=[doc.width/3]*3)
    summary_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ("BACKGROUND", (0,0), (-1,-1), COLOR_LIGHT),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))

    # ── 섹터별 상세 테이블 ───────────────────────────────────
    story.append(Paragraph("■ 섹터별 종목 분석", styles["section"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.2*cm))

    # 섹터로 그룹핑
    sector_groups: Dict[str, List] = {}
    for r in results:
        sec = r.get("sector", "기타")
        sector_groups.setdefault(sec, []).append(r)

    for sector, items in sector_groups.items():
        story.append(Paragraph(f"[ {sector} ]", styles["section"]))

        # 테이블 헤더
        col_widths = [3.5*cm, 2.2*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.6*cm, 2.0*cm]
        tdata = [[
            Paragraph("종목명", styles["small"]),
            Paragraph("현재가", styles["small"]),
            Paragraph("1일수익률", styles["small"]),
            Paragraph("5일수익률", styles["small"]),
            Paragraph("RSI", styles["small"]),
            Paragraph("감성", styles["small"]),
            Paragraph("시그널", styles["small"]),
        ]]

        for r in items:
            decision = r.get("decision", "홀딩")
            dc = _decision_color(decision)
            emoji = r.get("decision_emoji", "🟡")
            tdata.append([
                Paragraph(f"{r.get('name', r['ticker'])}\n({r['ticker']})", styles["body"]),
                Paragraph(_fmt_price(r.get("price"), r["ticker"]), styles["body"]),
                Paragraph(_fmt_pct(r.get("return_1d")), styles["body"]),
                Paragraph(_fmt_pct(r.get("return_5d")), styles["body"]),
                Paragraph(f"{r.get('rsi', 'N/A')}" if r.get("rsi") else "N/A", styles["body"]),
                Paragraph(r.get("sentiment_label", "-"), styles["body"]),
                Paragraph(f"{emoji} {decision}", ParagraphStyle(
                    "dec", fontName=FONT_NAME, fontSize=9,
                    textColor=dc, leading=13, alignment=TA_CENTER
                )),
            ])

        t = Table(tdata, colWidths=col_widths)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), COLOR_SUB),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, COLOR_LIGHT]),
            ("BOX", (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ("INNERGRID", (0,0), (-1,-1), 0.3, COLOR_BORDER),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(KeepTogether([t, Spacer(1, 0.1*cm)]))
        story.append(Spacer(1, 0.3*cm))

    # ── 매수/매도 하이라이트 ─────────────────────────────────
    if buy_list or sell_list:
        story.append(Paragraph("■ 오늘의 주목 종목", styles["section"]))
        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
        story.append(Spacer(1, 0.2*cm))

        for r in (buy_list + sell_list)[:10]:
            decision = r.get("decision", "홀딩")
            dc = _decision_color(decision)
            emoji = r.get("decision_emoji", "🟡")
            name = r.get("name", r["ticker"])
            score = r.get("combined_score", 0.5)

            highlight_data = [[
                Paragraph(f"{emoji} {name}  ({r['ticker']})", ParagraphStyle(
                    "hl_name", fontName=FONT_NAME, fontSize=10,
                    textColor=dc, leading=14
                )),
                Paragraph(f"종합점수: {score:.2f}", styles["small"]),
                Paragraph(f"현재가: {_fmt_price(r.get('price'), r['ticker'])}", styles["small"]),
            ]]
            ht = Table(highlight_data, colWidths=[6*cm, 3*cm, 3*cm])
            ht.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fafafa")),
                ("BOX", (0,0), (-1,-1), 0.8, dc),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("LEFTPADDING", (0,0), (-1,-1), 8),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ]))
            story.append(ht)

            # 주요 헤드라인
            headlines = r.get("top_headlines", [])
            for hl in headlines[:2]:
                if hl:
                    story.append(Paragraph(f"  • {hl[:90]}", styles["headline"]))
            story.append(Spacer(1, 0.25*cm))

    # ── 리스크 경고 ─────────────────────────────────────────
    risk_items = [r for r in results if r.get("risk_level") in ("HIGH", "MED")]
    if risk_items:
        story.append(Paragraph("■ 리스크 경보", styles["section"]))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.red))
        story.append(Spacer(1, 0.2*cm))
        for r in risk_items:
            flags = ", ".join(r.get("risk_flags", []))
            level_color = colors.red if r.get("risk_level") == "HIGH" else colors.orange
            story.append(Paragraph(
                f"⚠ {r.get('name', r['ticker'])} ({r['ticker']})  |  {flags}",
                ParagraphStyle("risk", fontName=FONT_NAME, fontSize=9, textColor=level_color, leading=13)
            ))
        story.append(Spacer(1, 0.3*cm))

    # ── 푸터 ─────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER))
    story.append(Paragraph(
        "본 보고서는 자동 생성된 퀀트 분석 자료입니다. 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.",
        ParagraphStyle("footer", fontName=FONT_NAME, fontSize=7, textColor=colors.grey,
                       alignment=TA_CENTER, leading=10)
    ))

    doc.build(story)
    return output_path
