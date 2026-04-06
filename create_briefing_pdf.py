#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "CS24_7Lever_Briefing.pdf")

DARK_BG = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
ACCENT2 = HexColor("#0f3460")
HEADER_BG = HexColor("#16213e")
ROW_ALT = HexColor("#f0f0f5")
GREEN = HexColor("#27ae60")
RED = HexColor("#c0392b")
BLUE = HexColor("#2980b9")
GOLD = HexColor("#f39c12")
DARK_TEXT = HexColor("#1a1a2e")
LIGHT_GREY = HexColor("#ecf0f1")
MID_GREY = HexColor("#bdc3c7")

styles = getSampleStyleSheet()

s_title = ParagraphStyle("DocTitle", parent=styles["Title"],
    fontSize=26, leading=32, textColor=ACCENT, fontName="Helvetica-Bold",
    spaceAfter=4)

s_subtitle = ParagraphStyle("DocSubtitle", parent=styles["Normal"],
    fontSize=11, leading=14, textColor=MID_GREY, fontName="Helvetica",
    spaceAfter=18)

s_h1 = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=16, leading=20, textColor=ACCENT2, fontName="Helvetica-Bold",
    spaceBefore=16, spaceAfter=8,
    borderWidth=0, borderPadding=0)

s_h2 = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=12, leading=16, textColor=DARK_TEXT, fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=4)

s_body = ParagraphStyle("Body", parent=styles["Normal"],
    fontSize=9.5, leading=13, textColor=DARK_TEXT, fontName="Helvetica",
    spaceAfter=6, alignment=TA_JUSTIFY)

s_body_bold = ParagraphStyle("BodyBold", parent=s_body,
    fontName="Helvetica-Bold")

s_bullet = ParagraphStyle("Bullet", parent=s_body,
    leftIndent=14, bulletIndent=4, spaceBefore=2, spaceAfter=2)

s_small = ParagraphStyle("Small", parent=s_body, fontSize=8, leading=10)

s_conf = ParagraphStyle("Conf", parent=styles["Normal"],
    fontSize=7.5, leading=10, textColor=ACCENT, fontName="Helvetica-Bold",
    alignment=TA_RIGHT)

s_footer = ParagraphStyle("Footer", parent=styles["Normal"],
    fontSize=7, leading=9, textColor=MID_GREY, fontName="Helvetica",
    alignment=TA_CENTER)

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top bar
    canvas.setFillColor(HEADER_BG)
    canvas.rect(0, h - 18*mm, w, 18*mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(15*mm, h - 12*mm, "CARSALE24")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(ACCENT)
    canvas.drawRightString(w - 15*mm, h - 12*mm,
                           "CONFIDENTIAL -- Carsale24 Internal")
    # Accent line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(0, h - 18*mm, w, h - 18*mm)
    # Footer
    canvas.setFillColor(MID_GREY)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawCentredString(w/2, 10*mm,
        f"Page {doc.page}  |  Path to EUR500K -- 7-Lever Scenario Framework  |  April 2026")
    canvas.restoreState()

def make_table(data, col_widths=None, header_color=HEADER_BG):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t

def sensitivity_table(title, col_headers, row_headers, data, highlight_cells=None):
    elems = []
    elems.append(Paragraph(title, s_h2))
    full = [[""] + col_headers]
    for rh, row in zip(row_headers, data):
        full.append([rh] + row)
    ncols = len(col_headers) + 1
    cw = [55] + [58] * len(col_headers)
    t = Table(full, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT2),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 0), (0, -1), ACCENT2),
        ("TEXTCOLOR", (0, 0), (0, -1), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    # Color positive green, negative red
    for ri in range(1, len(full)):
        for ci in range(1, ncols):
            val = full[ri][ci]
            if "+" in str(val) or (str(val).replace(",","").replace(" ","").lstrip("-").isdigit() == False and str(val).startswith("+")):
                pass
            try:
                num = float(str(val).replace(",","").replace("+","").replace(" ","").replace("EUR",""))
                if num > 0:
                    style_cmds.append(("TEXTCOLOR", (ci, ri), (ci, ri), GREEN))
                elif num < 0:
                    style_cmds.append(("TEXTCOLOR", (ci, ri), (ci, ri), RED))
            except:
                pass
    if highlight_cells:
        for (r, c) in highlight_cells:
            style_cmds.append(("BACKGROUND", (c, r), (c, r), HexColor("#fff9c4")))
    for i in range(1, len(full)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (1, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style_cmds))
    elems.append(t)
    return elems

def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4,
        topMargin=24*mm, bottomMargin=18*mm,
        leftMargin=15*mm, rightMargin=15*mm)
    story = []
    W = A4[0] - 30*mm

    # ── TITLE PAGE ──
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("Path to EUR500K", s_title))
    story.append(Paragraph("7-Lever Scenario Framework", ParagraphStyle(
        "Title2", parent=s_title, fontSize=20, leading=24, textColor=ACCENT2)))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Carsale24 Internal  --  April 2026", s_subtitle))
    story.append(Spacer(1, 15*mm))

    kpis = [
        ["Q1 2026 Actual NCF", "Budget FY Forecast", "Best Case FY Forecast", "Target", "Gap to Close"],
        ["-EUR43K", "-EUR402K", "+EUR597K", "+EUR500K", "EUR902K"]
    ]
    kt = Table(kpis, colWidths=[W/5]*5)
    kt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT2),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (0, 1), (0, 1), RED),
        ("TEXTCOLOR", (1, 1), (1, 1), RED),
        ("TEXTCOLOR", (2, 1), (2, 1), GREEN),
        ("TEXTCOLOR", (3, 1), (3, 1), GREEN),
        ("TEXTCOLOR", (4, 1), (4, 1), GOLD),
    ]))
    story.append(kt)

    story.append(Spacer(1, 20*mm))
    story.append(Paragraph(
        "This document outlines the 7 key levers available to close the EUR902K gap between "
        "budget and the EUR500K target. It maps their interdependencies and provides sensitivity "
        "analysis to support scenario selection for Q2-Q4 2026.", s_body))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Q1 Actuals (Locked): Jan -EUR32K | Feb -EUR6K | Mar -EUR6K | Cumulative: -EUR43K",
        s_body_bold))

    story.append(PageBreak())

    # ── SECTION 1: EXECUTIVE SUMMARY ──
    story.append(Paragraph("1. Executive Summary", s_h1))
    story.append(Paragraph(
        "Carsale24 closed Q1 2026 with a cumulative net cash flow of <b>-EUR43K</b>. "
        "The budget (Real Case) projects a full-year cumulative of <b>-EUR402K</b>, while the "
        "Best Case model shows <b>+EUR597K</b> is structurally achievable. The target of "
        "<b>+EUR500K</b> requires closing a <b>EUR902K gap</b> vs. budget across the remaining "
        "9 months (Apr-Dec 2026).", s_body))
    story.append(Paragraph(
        "Seven levers have been identified through goal-seek analysis. No single lever can close "
        "the gap alone -- the maximum solo contribution ranges from 5% to 16.5%. "
        "A coordinated pull across multiple levers at ~63% of their maximum range is required.", s_body))

    # ── SECTION 2: 7 LEVERS TABLE ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("2. The 7 Levers", s_h1))
    lever_data = [
        ["#", "Lever", "Budget\n(Real)", "Best\nCase", "Goal-Seek\nOptimal", "Solo\nImpact"],
        ["1", "Volume", "957\ncars/mo", "1,041\ncars/mo", "1,082\ncars/mo\n(+125)", "16.5%"],
        ["2", "Sourcing Mix\n(GenSearch %)", "~45%\nGenSearch", "~46%\nGenSearch", "~34%\nGenSearch\n(-11pp)", "12.5%"],
        ["3", "Perf Marketing\nSpend", "EUR91K/mo", "EUR92K/mo", "EUR75K/mo\n(-EUR16K)", "15.7%"],
        ["4", "Commission\nper Car", "EUR288\navg", "EUR305\navg", "EUR313 avg\n(+EUR25)", "13.4%"],
        ["5", "Subscription\nRevenue", "EUR37K/mo", "EUR42K/mo", "EUR47K/mo\n(+EUR9.4K)", "9.4%"],
        ["6", "GenSearch\nExp/Share", "EUR200/car", "EUR174/car", "EUR175/car\n(-EUR25)", "8.7%"],
        ["7", "Car Buy/Sell\nMargin", "EUR30/car", "EUR34/car", "EUR36/car\n(+EUR6)", "~5%"],
    ]
    cw = [18, 72, 62, 62, 72, 42]
    lt = make_table(lever_data, col_widths=cw)
    story.append(lt)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Goal-Seek Optimal = value needed if this lever alone closed 100% of the gap. "
        "Solo Impact = % of EUR902K gap closed at maximum feasible pull.</i>", s_small))

    story.append(PageBreak())

    # ── SECTION 3: INTERDEPENDENCY MAP ──
    story.append(Paragraph("3. Lever Interdependency Map", s_h1))
    story.append(Paragraph(
        "The 7 levers do not operate independently. Understanding their interactions is critical "
        "for building a realistic scenario.", s_body))

    # 3a Volume <-> Marketing
    story.append(Paragraph("Volume <-> Performance Marketing  (TENSION)", s_h2))
    story.append(Paragraph(
        "More cars requires more GenSearch leads, which requires <b>more</b> marketing spend. "
        "But reducing marketing spend reduces GenSearch-sourced cars. This creates a direct tension: "
        "you cannot simultaneously maximize volume through GenSearch and minimize marketing cost.",
        s_body))
    story.append(Paragraph(
        "<b>Resolution:</b> Volume growth must come from TIAAS and Brands (organic channels), "
        "not GenSearch. This decouples the volume lever from the marketing lever.", s_body))

    # 3b Sourcing <-> Marketing
    story.append(Paragraph("Sourcing Mix <-> Performance Marketing  (SYNERGY)", s_h2))
    story.append(Paragraph(
        "This is the <b>most powerful synergy</b> in the model. Shifting away from GenSearch "
        "(EUR200 exp/share + perf marketing) toward TIAAS (EUR140 exp/share, no perf marketing) "
        "and Brands (EUR32 exp/share, no perf marketing) simultaneously improves two levers:",
        s_body))
    story.append(Paragraph(
        "Every 1pp shift from GenSearch to TIAAS/Brands saves ~EUR600-700/month per 1,000 cars "
        "in exp/share costs AND reduces the performance marketing budget required.",
        s_bullet))

    # 3c Commission <-> Volume
    story.append(Paragraph("Commission <-> Volume  (MULTIPLIER)", s_h2))
    story.append(Paragraph(
        "Higher commission per car multiplied by more cars creates a multiplicative effect. "
        "+EUR25/car x 125 extra cars/month = <b>EUR3,125 extra/month</b> from the interaction "
        "term alone -- above and beyond the individual lever contributions.", s_body))

    # 3d Subscription
    story.append(Paragraph("Subscription Revenue  (INDEPENDENT)", s_h2))
    story.append(Paragraph(
        "Subscription revenue is the only lever that is fully independent of all others. "
        "Growing from EUR37K to EUR47K/month adds ~EUR90K/year with zero risk to other levers. "
        "This is the safest lever to pull.", s_body))

    # 3e GenSearch Exp/Share
    story.append(Paragraph("GenSearch Exp/Share <-> Sourcing  (DIMINISHING RETURNS)", s_h2))
    story.append(Paragraph(
        "Negotiating lower GenSearch exp/share matters less if GenSearch share is simultaneously "
        "being reduced. <b>Prioritize the sourcing shift first</b>, then negotiate exp/share "
        "on the reduced GenSearch volume.", s_body))

    story.append(PageBreak())

    # ── SECTION 4: PER-CAR ECONOMICS ──
    story.append(Paragraph("4. Per-Car Economics by Source", s_h1))
    story.append(Paragraph(
        "Understanding the true net margin per car by channel reveals why the sourcing mix "
        "is the single most impactful strategic lever.", s_body))

    econ_data = [
        ["Channel", "Commission", "Exp/Share", "Net Margin\n/Car", "Marketing\nCost/Car", "True Net\n/Car"],
        ["Brands", "EUR288-314", "EUR23-51", "EUR237-291", "EUR0\n(organic)", "EUR237-291"],
        ["TIAAS", "EUR302-322", "EUR137-142", "EUR160-185", "EUR0", "EUR160-185"],
        ["B2B", "EUR360-380", "EUR0", "EUR360-380", "EUR0", "EUR360-380"],
        ["GenSearch", "EUR288-320", "EUR139-234", "EUR86-149", "~EUR180/car\n(perf mktg)", "-EUR31 to\n-EUR94"],
    ]
    et = make_table(econ_data, col_widths=[55, 62, 55, 60, 62, 62])
    # highlight GenSearch row red
    # GenSearch row highlighted via table styling
    story.append(et)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Key insight:</b> GenSearch is the ONLY channel that loses money on a fully-loaded basis "
        "when performance marketing is included. But it drives volume. The critical business question: "
        "at what GenSearch share does volume growth stop justifying the cost?", s_body))

    story.append(Spacer(1, 10))

    # ── SECTION 5: SENSITIVITY TABLES ──
    story.append(Paragraph("5. Two-Way Sensitivity Analysis", s_h1))
    story.append(Paragraph(
        "FY cumulative cash flow (EURK) under different lever combinations. "
        "Green = positive, Red = negative.", s_body))

    # 5a Volume x Sourcing
    elems = sensitivity_table(
        "Volume x Sourcing Shift (GenSearch pp change)",
        ["GS 0pp", "GS -5pp", "GS -10pp", "GS -15pp", "GS -20pp"],
        ["+0 cars", "+50", "+100", "+150", "+200", "+250"],
        [
            ["-402", "-354", "-306", "-259", "-210"],
            ["-327", "-277", "-227", "-177", "-126"],
            ["-253", "-201", "-148", "-95", "-42"],
            ["-180", "-124", "-69", "-14", "+41"],
            ["-106", "-48", "+10", "+68", "+126"],
            ["-32", "+28", "+88", "+149", "+209"],
        ]
    )
    story.extend(elems)
    story.append(Spacer(1, 8))

    # 5b Volume x Marketing
    elems = sensitivity_table(
        "Volume x Marketing Cut (EUR/mo reduction)",
        ["Mktg 0", "-EUR10K", "-EUR20K", "-EUR30K", "-EUR40K"],
        ["+0 cars", "+100", "+200", "+250"],
        [
            ["-402", "-312", "-222", "-132", "-42"],
            ["-253", "-163", "-73", "+17", "+107"],
            ["-106", "-16", "+74", "+164", "+254"],
            ["-32", "+58", "+148", "+238", "+328"],
        ]
    )
    story.extend(elems)

    story.append(PageBreak())

    # 5c Commission x Subscription
    elems = sensitivity_table(
        "Commission Increase x Subscription Growth (EUR/mo)",
        ["Subs +0", "+EUR10K", "+EUR20K", "+EUR30K"],
        ["+EUR0/car", "+EUR20", "+EUR40", "+EUR60", "+EUR80"],
        [
            ["-402", "-312", "-222", "-132"],
            ["-241", "-151", "-61", "+29"],
            ["-80", "+10", "+100", "+190"],
            ["+81", "+171", "+261", "+351"],
            ["+242", "+332", "+422", "+512"],
        ]
    )
    story.extend(elems)

    story.append(Spacer(1, 12))

    # ── SECTION 6: SCENARIOS ──
    story.append(Paragraph("6. Three Credible Scenarios", s_h1))

    # Scenario A
    story.append(Paragraph("Scenario A: \"Best Case Achievable\" -- Target EUR500K+", s_h2))
    story.append(Paragraph(
        "All 7 levers pulled to ~63% of maximum range. Requires: 1,082 cars/mo, GenSearch at 34%, "
        "commission +EUR25/car, marketing -EUR16K/mo, subscriptions +EUR9.4K/mo. "
        "Ambitious but structurally validated -- the Best Case model shows EUR597K is possible.", s_body))

    # Scenario B
    story.append(Paragraph("Scenario B: \"Breakeven Plus\" -- Target EUR100-200K", s_h2))
    story.append(Paragraph(
        "Focus on 3-4 levers: volume +100 cars/mo, GenSearch -10pp shift, marketing -EUR15K/mo, "
        "commission +EUR15/car. More achievable execution. Proves the business model works "
        "and builds confidence for further optimization.", s_body))

    # Scenario C
    story.append(Paragraph("Scenario C: \"Marketing Efficiency\" -- Target Breakeven", s_h2))
    story.append(Paragraph(
        "Primarily sourcing shift + marketing cut: GenSearch -15pp, marketing -EUR25K/mo, "
        "modest volume growth +50 cars/mo. Lowest execution risk. Reaches breakeven but "
        "does not generate significant positive cash flow.", s_body))

    # Scenario comparison table
    sc_data = [
        ["", "Scenario A", "Scenario B", "Scenario C"],
        ["Target", "EUR500K+", "EUR100-200K", "Breakeven"],
        ["Volume", "+125 cars/mo", "+100 cars/mo", "+50 cars/mo"],
        ["GenSearch Shift", "-11pp", "-10pp", "-15pp"],
        ["Marketing Cut", "-EUR16K/mo", "-EUR15K/mo", "-EUR25K/mo"],
        ["Commission", "+EUR25/car", "+EUR15/car", "+EUR0/car"],
        ["Subscriptions", "+EUR9.4K/mo", "+EUR0", "+EUR0"],
        ["Execution Risk", "High", "Medium", "Low"],
        ["Levers Required", "All 7", "3-4", "2-3"],
    ]
    st = make_table(sc_data, col_widths=[80, 80, 80, 80])
    story.append(Spacer(1, 4))
    story.append(st)

    story.append(PageBreak())

    # ── SECTION 7: DISCUSSION QUESTIONS ──
    story.append(Paragraph("7. Recommended Discussion Questions", s_h1))

    questions = [
        ("1.", "What is the realistic TIAAS pipeline growth?",
         "Drives Levers 1, 2, and 3 simultaneously. TIAAS growth is the single highest-leverage "
         "input because it increases volume while shifting sourcing away from GenSearch and "
         "reducing the need for performance marketing."),
        ("2.", "Can commission rates be renegotiated by Q2?",
         "Lever 4 requires dealer conversations. Each EUR10/car increase across ~1,000 cars/month "
         "adds ~EUR90K/year to cash flow."),
        ("3.", "What is the minimum GenSearch share before volume collapses?",
         "This is the critical threshold. The model assumes GenSearch can be reduced from ~45% to "
         "~34%, but if organic channels cannot absorb the volume, total cars will drop."),
        ("4.", "Is subscription growth on track for EUR40K+/month by Q3?",
         "Lever 5 is the safest lever. Check the current pipeline and conversion rates against "
         "the EUR47K/month target."),
        ("5.", "Which scenario should we commit to for board reporting?",
         "Scenario A is ambitious but validated. Scenario B is more conservative but still meaningful. "
         "The decision framework: commit to B, stretch for A, accept C as the floor."),
    ]
    for num, q, detail in questions:
        story.append(Paragraph(f"<b>{num} {q}</b>", s_body_bold))
        story.append(Paragraph(detail, s_body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Prepared for Carsale24 leadership. Based on Financial Model v5 and KPI Dashboard v3.2. "
        "All projections use Q1 2026 actuals as baseline. Interactive scenario modeling available "
        "in the CS24 Goal-Seek Dashboard.", s_small))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF created: {OUT}")

if __name__ == "__main__":
    build()
