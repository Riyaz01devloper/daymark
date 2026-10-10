import io
import os
import re
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Register Unicode / Hindi fonts if available on Windows
FONT_NAME = "Helvetica"
BOLD_FONT_NAME = "Helvetica-Bold"

FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\Nirmala.ttc", 0),
    (r"C:\Windows\Fonts\mangal.ttf", -1),
    (r"C:\Windows\Fonts\arial.ttf", -1),
]

for font_path, sub_idx in FONT_CANDIDATES:
    if os.path.exists(font_path):
        try:
            if sub_idx >= 0:
                pdfmetrics.registerFont(TTFont("IndicFont", font_path, subfontIndex=sub_idx))
            else:
                pdfmetrics.registerFont(TTFont("IndicFont", font_path))
            FONT_NAME = "IndicFont"
            BOLD_FONT_NAME = "IndicFont"
            break
        except Exception:
            continue


def _clean_markdown_to_reportlab(text: str) -> str:
    """Converts basic markdown bold/italic and escapes XML characters for ReportLab Paragraph."""
    # First escape HTML special characters
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert bold **text** -> <b>text</b>
    safe = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)
    # Convert italic *text* -> <i>\1</i>
    safe = re.sub(r"\*(.+?)\*", r"<i>\1</i>", safe)
    # Convert backticks `code` -> <b>\1</b>
    safe = re.sub(r"`(.+?)`", r"<b>\1</b>", safe)
    # Strip math delimiters $...$ to clean text
    safe = re.sub(r"\$(.+?)\$", r"<b>\1</b>", safe)
    return safe


def generate_chapter_pdf(
    grade: int,
    subject: str,
    chapter: str,
    notes_content: str,
    takeaways: list[str] | None = None,
    language: str = "en",
) -> bytes:
    """Generates a clean, professionally formatted NCERT chapter revision notes PDF."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36,
    )

    is_hi = language in ("hi", "hindi")
    font_main = FONT_NAME
    font_bold = BOLD_FONT_NAME

    # Color Palette: Deep Academic Forest Green & Warm Sand
    c_primary = colors.HexColor("#244b36")
    c_accent = colors.HexColor("#3f7053")
    c_dark = colors.HexColor("#1b2b20")
    c_light_bg = colors.HexColor("#f4f8f3")
    c_border = colors.HexColor("#cbe0ce")
    c_takeaway_bg = colors.HexColor("#eaf3e9")

    styles = getSampleStyleSheet()

    header_title_style = ParagraphStyle(
        "HeaderTitle",
        fontName=font_bold,
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=0,
    )
    header_meta_style = ParagraphStyle(
        "HeaderMeta",
        fontName=font_main,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#536e5b"),
    )
    h2_style = ParagraphStyle(
        "Heading2Custom",
        fontName=font_bold,
        fontSize=13,
        leading=17,
        textColor=c_accent,
        spaceBefore=12,
        spaceAfter=4,
    )
    h3_style = ParagraphStyle(
        "Heading3Custom",
        fontName=font_bold,
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "BodyCustom",
        fontName=font_main,
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "BulletCustom",
        fontName=font_main,
        fontSize=9,
        leading=13.5,
        textColor=c_dark,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )
    takeaway_title_style = ParagraphStyle(
        "TakeawayTitle",
        fontName=font_bold,
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceAfter=4,
    )
    takeaway_item_style = ParagraphStyle(
        "TakeawayItem",
        fontName=font_main,
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2,
    )

    story: list[Any] = []

    # 1. Header Banner
    title_text = f"कक्षा {grade} {subject} — {chapter}" if is_hi else f"Class {grade} {subject} — {chapter}"
    sub_title = (
        "आधिकारिक NCERT एवं CBSE बोर्ड पुनरावृत्ति नोट्स • Daymark Study Hub"
        if is_hi
        else "Official NCERT & CBSE Revision Notes • Daymark Study Hub"
    )

    story.append(Paragraph(title_text, header_title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(sub_title, header_meta_style))
    story.append(Spacer(1, 4))

    # Meta Info Row Table
    cur_date = datetime.now().strftime("%d %b %Y")
    meta_row = [
        [
            Paragraph(f"<b>{'कक्षा/Class:'}</b> {grade}", header_meta_style),
            Paragraph(f"<b>{'विषय/Subject:'}</b> {subject}", header_meta_style),
            Paragraph(f"<b>{'तारीख/Date:'}</b> {cur_date}", header_meta_style),
            Paragraph(f"<b>{'सिलेबस/Syllabus:'}</b> CBSE / NCERT", header_meta_style),
        ]
    ]
    meta_table = Table(meta_row, colWidths=["20%", "30%", "25%", "25%"])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), c_light_bg),
                ("BOX", (0, 0), (-1, -1), 0.5, c_border),
                ("PADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=8))

    # 2. Key Takeaways Callout Box (if present)
    if takeaways:
        takeaway_flowables: list[Any] = [
            Paragraph(
                "🎯 महत्वपूर्ण परीक्षा बिंदु (Key Exam Takeaways):"
                if is_hi
                else "🎯 High-Yield Board Exam Takeaways:",
                takeaway_title_style,
            )
        ]
        for t in takeaways:
            clean_t = _clean_markdown_to_reportlab(t)
            takeaway_flowables.append(
                Paragraph(f"&bull; {clean_t}", takeaway_item_style)
            )

        takeaway_box = Table([[takeaway_flowables]], colWidths=["100%"])
        takeaway_box.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), c_takeaway_bg),
                    ("BOX", (0, 0), (-1, -1), 1, c_accent),
                    ("PADDING", (0, 0), (-1, -1), 8),
                    ("ROUNDEDCORNERS", [4, 4, 4, 4]),
                ]
            )
        )
        story.append(takeaway_box)
        story.append(Spacer(1, 10))

    # 3. Main Body Content (Parsing Markdown lines)
    lines = notes_content.splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue

        if line.startswith("####"):
            heading = _clean_markdown_to_reportlab(line.lstrip("#").strip())
            story.append(Paragraph(heading, h3_style))
        elif line.startswith("###"):
            heading = _clean_markdown_to_reportlab(line.lstrip("#").strip())
            story.append(Paragraph(heading, h2_style))
        elif line.startswith("##"):
            heading = _clean_markdown_to_reportlab(line.lstrip("#").strip())
            story.append(Paragraph(heading, h2_style))
        elif line.startswith("#"):
            heading = _clean_markdown_to_reportlab(line.lstrip("#").strip())
            story.append(Paragraph(heading, header_title_style))
        elif line.startswith(("- ", "* ", "• ")):
            bullet_text = _clean_markdown_to_reportlab(line[2:].strip())
            story.append(Paragraph(f"&bull; {bullet_text}", bullet_style))
        elif re.match(r"^\d+\.\s+", line):
            num_match = re.match(r"^(\d+\.)\s+(.+)$", line)
            if num_match:
                prefix = num_match.group(1)
                text = _clean_markdown_to_reportlab(num_match.group(2))
                story.append(Paragraph(f"<b>{prefix}</b> {text}", bullet_style))
            else:
                story.append(Paragraph(_clean_markdown_to_reportlab(line), body_style))
        else:
            story.append(Paragraph(_clean_markdown_to_reportlab(line), body_style))

    # 4. Footer Line
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_border, spaceAfter=6))
    footer_text = (
        "सुरक्षित और आधिकारिक NCERT पाठ्यपुस्तक सामग्री • Daymark अध्ययन केंद्र • ऑल राइट्स रिसर्व्ड"
        if is_hi
        else "Official NCERT & CBSE Curriculum Verified • Daymark Study Hub • www.cbse.gov.in / ncert.nic.in"
    )
    story.append(Paragraph(footer_text, header_meta_style))

    doc.build(story)
    return buf.getvalue()


def generate_printable_html(
    grade: int,
    subject: str,
    chapter: str,
    notes_content: str,
    takeaways: list[str] | None = None,
    language: str = "en",
) -> str:
    """Generates a standalone, beautiful HTML printable document with @media print styles."""
    is_hi = language in ("hi", "hindi")
    cur_date = datetime.now().strftime("%d %b %Y")

    title_text = f"कक्षा {grade} {subject} — {chapter}" if is_hi else f"Class {grade} {subject} — {chapter}"
    takeaways_header = "🎯 महत्वपूर्ण परीक्षा बिंदु (Key Exam Takeaways)" if is_hi else "🎯 High-Yield Board Exam Takeaways"

    # Format markdown lines to HTML
    html_body_lines: list[str] = []
    for raw in notes_content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("####"):
            html_body_lines.append(f"<h4>{line.lstrip('#').strip()}</h4>")
        elif line.startswith("###"):
            html_body_lines.append(f"<h3>{line.lstrip('#').strip()}</h3>")
        elif line.startswith("##"):
            html_body_lines.append(f"<h2>{line.lstrip('#').strip()}</h2>")
        elif line.startswith(("- ", "* ", "• ")):
            clean_b = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line[2:].strip())
            html_body_lines.append(f"<li>{clean_b}</li>")
        elif re.match(r"^\d+\.\s+", line):
            clean_n = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html_body_lines.append(f"<p class='num-step'>{clean_n}</p>")
        else:
            clean_p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html_body_lines.append(f"<p>{clean_p}</p>")

    formatted_body = "\n".join(html_body_lines)

    takeaway_html = ""
    if takeaways:
        items = "".join(f"<li>{t}</li>" for t in takeaways)
        takeaway_html = f"""
        <div class="takeaways-box">
            <h3>{takeaways_header}</h3>
            <ul>{items}</ul>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="{ 'hi' if is_hi else 'en' }">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - NCERT Notes</title>
    <style>
        @page {{
            size: A4;
            margin: 1.5cm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Nirmala UI", Arial, sans-serif;
            color: #1a281e;
            background: #ffffff;
            line-height: 1.6;
            margin: 0;
            padding: 24px;
        }}
        .print-container {{
            max-width: 820px;
            margin: 0 auto;
        }}
        .print-header {{
            border-bottom: 2px solid #234c35;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .print-brand {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #496b53;
            font-weight: 700;
        }}
        h1 {{
            font-size: 1.7rem;
            color: #1e3f2c;
            margin: 6px 0 8px;
            line-height: 1.25;
        }}
        .meta-strip {{
            display: flex;
            gap: 16px;
            background: #f2f7f1;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.82rem;
            color: #3b5444;
            margin-bottom: 14px;
            border: 1px solid #d4e2d3;
        }}
        .takeaways-box {{
            background: #eaf3e9;
            border-left: 4px solid #2d5a3f;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 18px;
        }}
        .takeaways-box h3 {{
            margin: 0 0 8px;
            font-size: 1.05rem;
            color: #1f422e;
        }}
        .takeaways-box ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .takeaways-box li {{
            margin-bottom: 4px;
            font-size: 0.9rem;
        }}
        h2, h3, h4 {{
            color: #244d36;
            margin-top: 18px;
            margin-bottom: 6px;
        }}
        h2 {{ font-size: 1.25rem; border-bottom: 1px dashed #d5e4d4; padding-bottom: 4px; }}
        h3 {{ font-size: 1.1rem; }}
        h4 {{ font-size: 0.98rem; }}
        p {{ margin: 6px 0; font-size: 0.92rem; }}
        li {{ font-size: 0.92rem; margin-bottom: 4px; }}
        ul {{ padding-left: 22px; margin: 6px 0 12px; }}
        .num-step {{
            background: #f7faf6;
            padding: 4px 8px;
            border-left: 2px solid #588567;
            margin: 4px 0;
        }}
        .print-footer {{
            margin-top: 28px;
            padding-top: 10px;
            border-top: 1px solid #d8e5d7;
            font-size: 0.78rem;
            color: #687e6f;
            display: flex;
            justify-content: space-between;
        }}
        .no-print-bar {{
            background: #254835;
            color: #ffffff;
            padding: 12px 18px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .print-btn {{
            background: #4bb374;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 0.88rem;
            font-weight: 700;
            cursor: pointer;
        }}
        @media print {{
            .no-print-bar {{ display: none !important; }}
            body {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="print-container">
        <div class="no-print-bar">
            <span>📄 <strong>Daymark NCERT Notes</strong> — Ready for PDF Download / Print</span>
            <button class="print-btn" onclick="window.print()">🖨️ Save as PDF / Print</button>
        </div>

        <div class="print-header">
            <span class="print-brand">CBSE & NCERT Verified Revision Hub</span>
            <h1>{title_text}</h1>
            <div class="meta-strip">
                <span><strong>Class:</strong> {grade}</span>
                <span><strong>Subject:</strong> {subject}</span>
                <span><strong>Date:</strong> {cur_date}</span>
                <span><strong>Curriculum:</strong> Official NCERT 2024–26</span>
            </div>
        </div>

        {takeaway_html}

        <div class="notes-body">
            {formatted_body}
        </div>

        <div class="print-footer">
            <span>Daymark Study Hub • Verified CBSE & NCERT Syllabus</span>
            <span>www.cbse.gov.in / ncert.nic.in</span>
        </div>
    </div>
</body>
</html>
"""
