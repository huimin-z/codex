from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "black-hole-model-guide-zh.pdf"

FONT_LIGHT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_MEDIUM_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_UNICODE_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

FONT_BODY = "BH-Heiti-Light"
FONT_BOLD = "BH-Heiti-Medium"
FONT_UNICODE = "BH-Unicode"

INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#5F6B7A")
NAVY = colors.HexColor("#0B1020")
BLUE = colors.HexColor("#2563EB")
CYAN = colors.HexColor("#06B6D4")
ORANGE = colors.HexColor("#F59E0B")
RED = colors.HexColor("#DC2626")
GREEN = colors.HexColor("#059669")
VIOLET = colors.HexColor("#7C3AED")
PAPER = colors.HexColor("#F8FAFC")
LINE = colors.HexColor("#D9E1EA")
PALE_BLUE = colors.HexColor("#EAF2FF")
PALE_ORANGE = colors.HexColor("#FFF4DE")
PALE_GREEN = colors.HexColor("#E8F8F2")
PALE_RED = colors.HexColor("#FDECEC")


def register_fonts() -> None:
    global FONT_BODY, FONT_BOLD, FONT_UNICODE
    local_fonts = [FONT_LIGHT_PATH, FONT_MEDIUM_PATH, FONT_UNICODE_PATH]
    if all(Path(font_path).exists() for font_path in local_fonts):
        pdfmetrics.registerFont(
            TTFont(FONT_BODY, FONT_LIGHT_PATH, subfontIndex=0)
        )
        pdfmetrics.registerFont(
            TTFont(FONT_BOLD, FONT_MEDIUM_PATH, subfontIndex=0)
        )
        pdfmetrics.registerFont(TTFont(FONT_UNICODE, FONT_UNICODE_PATH))
        return

    fallback_font = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(fallback_font))
    FONT_BODY = fallback_font
    FONT_BOLD = fallback_font
    FONT_UNICODE = fallback_font


def build_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleZH",
            parent=sample["Title"],
            fontName=FONT_BOLD,
            fontSize=28,
            leading=38,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=4 * mm,
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "SubtitleZH",
            parent=sample["Normal"],
            fontName=FONT_BODY,
            fontSize=13,
            leading=20,
            textColor=colors.HexColor("#C8D7F0"),
            wordWrap="CJK",
        ),
        "cover_meta": ParagraphStyle(
            "CoverMetaZH",
            parent=sample["Normal"],
            fontName=FONT_BODY,
            fontSize=9.5,
            leading=16,
            textColor=colors.HexColor("#CBD5E1"),
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=sample["Heading1"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=25,
            textColor=NAVY,
            spaceBefore=2 * mm,
            spaceAfter=4 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=sample["Heading2"],
            fontName=FONT_BOLD,
            fontSize=13,
            leading=19,
            textColor=BLUE,
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=sample["Heading3"],
            fontName=FONT_BOLD,
            fontSize=10.5,
            leading=16,
            textColor=INK,
            spaceBefore=3 * mm,
            spaceAfter=1.5 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "BodyZH",
            parent=sample["BodyText"],
            fontName=FONT_BODY,
            fontSize=9.5,
            leading=15.5,
            textColor=INK,
            spaceAfter=2.2 * mm,
            wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "SmallZH",
            parent=sample["BodyText"],
            fontName=FONT_BODY,
            fontSize=8,
            leading=12.5,
            textColor=MUTED,
            spaceAfter=1.5 * mm,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "CaptionZH",
            parent=sample["BodyText"],
            fontName=FONT_BODY,
            fontSize=7.8,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=1.5 * mm,
            spaceAfter=3 * mm,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "BulletZH",
            parent=sample["BodyText"],
            fontName=FONT_BODY,
            fontSize=9.2,
            leading=15,
            leftIndent=5 * mm,
            firstLineIndent=-3.2 * mm,
            bulletIndent=0,
            textColor=INK,
            spaceAfter=1.4 * mm,
            wordWrap="CJK",
        ),
        "equation": ParagraphStyle(
            "EquationZH",
            parent=sample["BodyText"],
            fontName=FONT_UNICODE,
            fontSize=11.2,
            leading=18,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceBefore=2 * mm,
            spaceAfter=2.5 * mm,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=sample["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=10.5,
            leftIndent=3 * mm,
            rightIndent=3 * mm,
            textColor=colors.HexColor("#19304D"),
            backColor=PALE_BLUE,
            borderColor=LINE,
            borderWidth=0.6,
            borderPadding=3 * mm,
            spaceBefore=1.5 * mm,
            spaceAfter=3 * mm,
        ),
        "toc_h": ParagraphStyle(
            "TOCHeading",
            parent=sample["Heading1"],
            fontName=FONT_BOLD,
            fontSize=20,
            leading=28,
            textColor=NAVY,
            spaceAfter=6 * mm,
        ),
        "toc1": ParagraphStyle(
            "TOC1",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=10,
            leading=17,
            leftIndent=0,
            firstLineIndent=0,
            textColor=INK,
        ),
        "toc2": ParagraphStyle(
            "TOC2",
            parent=sample["Normal"],
            fontName=FONT_BODY,
            fontSize=8.5,
            leading=14,
            leftIndent=8 * mm,
            firstLineIndent=0,
            textColor=MUTED,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=8,
            leading=11,
            textColor=colors.white,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "table_body": ParagraphStyle(
            "TableBody",
            parent=sample["Normal"],
            fontName=FONT_BODY,
            fontSize=7.7,
            leading=11.5,
            textColor=INK,
            wordWrap="CJK",
        ),
    }


class GuideDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, styles: dict[str, ParagraphStyle]):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=19 * mm,
            bottomMargin=18 * mm,
            title="实时交互黑洞模型 - 原理、实现与使用指南",
            author="Codex",
            subject="WebGL 实时黑洞模型技术文档",
        )
        self.styles = styles
        self._bookmark_index = 0
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates(
            [
                PageTemplate(
                    id="guide",
                    frames=[frame],
                    onPage=self.draw_page,
                )
            ]
        )

    def beforeDocument(self) -> None:
        self._bookmark_index = 0

    def draw_page(self, canvas, doc) -> None:
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(LINE)
            canvas.setLineWidth(0.5)
            canvas.line(
                self.leftMargin,
                A4[1] - 13 * mm,
                A4[0] - self.rightMargin,
                A4[1] - 13 * mm,
            )
            canvas.setFont(FONT_BODY, 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawString(
                self.leftMargin,
                A4[1] - 10.2 * mm,
                "实时交互黑洞模型 - 原理、实现与使用指南",
            )
            canvas.drawRightString(
                A4[0] - self.rightMargin,
                A4[1] - 10.2 * mm,
                "版本 2.1",
            )
            canvas.setStrokeColor(LINE)
            canvas.line(
                self.leftMargin,
                12 * mm,
                A4[0] - self.rightMargin,
                12 * mm,
            )
            canvas.setFont(FONT_BODY, 7.5)
            canvas.drawString(
                self.leftMargin,
                8.2 * mm,
                "index.html",
            )
            canvas.drawRightString(
                A4[0] - self.rightMargin,
                8.2 * mm,
                f"第 {doc.page} 页",
            )
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if not isinstance(flowable, Paragraph):
            return
        level_map = {"Heading1": 0, "Heading2": 1}
        if flowable.style.name not in level_map:
            return
        level = level_map[flowable.style.name]
        text = flowable.getPlainText()
        self._bookmark_index += 1
        key = f"section-{self._bookmark_index}"
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=False)
        self.notify("TOCEntry", (level, text, self.page, key))


class CoverBlackHole(Flowable):
    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self) -> None:
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        c.setFillColor(colors.HexColor("#070A12"))
        c.roundRect(0, 0, w, h, 5 * mm, fill=1, stroke=0)

        star_data = [
            (0.08, 0.78, 1.1),
            (0.16, 0.42, 0.7),
            (0.22, 0.84, 0.8),
            (0.31, 0.25, 0.9),
            (0.39, 0.68, 0.6),
            (0.62, 0.82, 0.8),
            (0.71, 0.33, 0.7),
            (0.79, 0.71, 1.0),
            (0.88, 0.52, 0.6),
            (0.93, 0.85, 0.9),
        ]
        c.setFillColor(colors.HexColor("#D9E8FF"))
        for x, y, r in star_data:
            c.circle(w * x, h * y, r, fill=1, stroke=0)

        cx, cy = w * 0.56, h * 0.50
        disk_w, disk_h = w * 0.56, h * 0.33
        for i, col in enumerate(
            [
                colors.HexColor("#263B8A"),
                colors.HexColor("#3A57C4"),
                colors.HexColor("#E38A2E"),
                colors.HexColor("#FFC56E"),
            ]
        ):
            inset = i * 2.2 * mm
            c.setStrokeColor(col)
            c.setLineWidth(3.5 - i * 0.5)
            c.ellipse(
                cx - disk_w / 2 + inset,
                cy - disk_h / 2 + inset * 0.35,
                cx + disk_w / 2 - inset,
                cy + disk_h / 2 - inset * 0.35,
                fill=0,
                stroke=1,
            )

        c.setFillColor(colors.HexColor("#020307"))
        c.circle(cx, cy, h * 0.22, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#F8B84E"))
        c.setLineWidth(2.2)
        c.circle(cx, cy, h * 0.255, fill=0, stroke=1)
        c.setStrokeColor(colors.HexColor("#70D5FF"))
        c.setLineWidth(0.8)
        c.circle(cx + h * 0.012, cy, h * 0.272, fill=0, stroke=1)

        c.setFont(FONT_BOLD, 9)
        c.setFillColor(colors.white)
        c.drawString(8 * mm, 8 * mm, "光线弯曲")
        c.setFillColor(colors.HexColor("#93C5FD"))
        c.drawString(36 * mm, 8 * mm, "光子临界区")
        c.setFillColor(colors.HexColor("#FDBA74"))
        c.drawString(76 * mm, 8 * mm, "频移与束射")
        c.restoreState()


class PipelineDiagram(Flowable):
    def __init__(self, width: float, height: float = 45 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self) -> None:
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        nodes = [
            ("交互输入", BLUE),
            ("JS 状态", VIOLET),
            ("Uniforms", CYAN),
            ("每像素光线", ORANGE),
            ("颜色合成", GREEN),
        ]
        box_w = w * 0.16
        gap = (w - box_w * len(nodes)) / (len(nodes) - 1)
        y = h * 0.55
        for index, (label, color) in enumerate(nodes):
            x = index * (box_w + gap)
            c.setFillColor(colors.Color(color.red, color.green, color.blue, alpha=0.12))
            c.setStrokeColor(color)
            c.setLineWidth(1.1)
            c.roundRect(x, y, box_w, 11 * mm, 2 * mm, fill=1, stroke=1)
            c.setFillColor(INK)
            c.setFont(FONT_BOLD, 8)
            c.drawCentredString(x + box_w / 2, y + 4.2 * mm, label)
            if index < len(nodes) - 1:
                ax = x + box_w + 1.2 * mm
                bx = x + box_w + gap - 1.2 * mm
                c.setStrokeColor(MUTED)
                c.line(ax, y + 5.5 * mm, bx, y + 5.5 * mm)
                c.line(bx - 2 * mm, y + 7 * mm, bx, y + 5.5 * mm)
                c.line(bx - 2 * mm, y + 4 * mm, bx, y + 5.5 * mm)

        branch_y = h * 0.12
        branch_labels = [
            ("捕获 → 阴影", NAVY),
            ("命中盘面 → 辐射", ORANGE),
            ("逃逸 → 星空", BLUE),
        ]
        branch_w = w * 0.26
        branch_gap = (w - branch_w * 3) / 2
        for index, (label, color) in enumerate(branch_labels):
            x = index * (branch_w + branch_gap)
            c.setFillColor(colors.Color(color.red, color.green, color.blue, alpha=0.10))
            c.setStrokeColor(color)
            c.roundRect(x, branch_y, branch_w, 9 * mm, 1.5 * mm, fill=1, stroke=1)
            c.setFillColor(INK)
            c.setFont(FONT_BODY, 7.5)
            c.drawCentredString(x + branch_w / 2, branch_y + 3.3 * mm, label)
        c.restoreState()


class DopplerDiagram(Flowable):
    def __init__(self, width: float, height: float = 52 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self) -> None:
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        cx, cy = w * 0.50, h * 0.50
        c.setStrokeColor(LINE)
        c.setLineWidth(8)
        c.ellipse(cx - w * 0.34, cy - h * 0.19, cx + w * 0.34, cy + h * 0.19)
        c.setStrokeColor(colors.HexColor("#4F8CFF"))
        c.setLineWidth(7)
        c.arc(cx - w * 0.34, cy - h * 0.19, cx + w * 0.34, cy + h * 0.19, 95, 170)
        c.setStrokeColor(colors.HexColor("#F6A23C"))
        c.setLineWidth(7)
        c.arc(cx - w * 0.34, cy - h * 0.19, cx + w * 0.34, cy + h * 0.19, 275, 170)
        c.setFillColor(NAVY)
        c.circle(cx, cy, h * 0.20, fill=1, stroke=0)
        c.setStrokeColor(ORANGE)
        c.setLineWidth(1.3)
        c.circle(cx, cy, h * 0.23, fill=0, stroke=1)

        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(BLUE)
        c.drawString(w * 0.03, h * 0.77, "朝向观察者")
        c.setFillColor(INK)
        c.setFont(FONT_BODY, 7.5)
        c.drawString(w * 0.03, h * 0.64, "蓝移 / 增亮")
        c.setFillColor(ORANGE)
        c.setFont(FONT_BOLD, 8.5)
        c.drawRightString(w * 0.97, h * 0.77, "远离观察者")
        c.setFillColor(INK)
        c.setFont(FONT_BODY, 7.5)
        c.drawRightString(w * 0.97, h * 0.64, "红移 / 变暗")

        c.setStrokeColor(BLUE)
        c.setLineWidth(1.2)
        c.line(w * 0.28, h * 0.78, w * 0.40, h * 0.67)
        c.setStrokeColor(ORANGE)
        c.line(w * 0.72, h * 0.78, w * 0.60, h * 0.67)
        c.restoreState()


class IscoChart(Flowable):
    def __init__(self, width: float, height: float = 68 * mm):
        super().__init__()
        self.width = width
        self.height = height

    @staticmethod
    def isco(spin: float) -> float:
        z1 = 1 + (1 - spin * spin) ** (1 / 3) * (
            (1 + spin) ** (1 / 3) + (1 - spin) ** (1 / 3)
        )
        z2 = math.sqrt(3 * spin * spin + z1 * z1)
        return 3 + z2 - math.sqrt((3 - z1) * (3 + z1 + 2 * z2))

    def draw(self) -> None:
        c = self.canv
        w, h = self.width, self.height
        left, right = 16 * mm, 7 * mm
        bottom, top = 12 * mm, 6 * mm
        plot_w = w - left - right
        plot_h = h - bottom - top
        c.saveState()
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        for y_value in [1, 2, 3, 4, 5, 6]:
            y = bottom + (y_value - 1) / 5 * plot_h
            c.line(left, y, left + plot_w, y)
            c.setFillColor(MUTED)
            c.setFont(FONT_BODY, 7)
            c.drawRightString(left - 2 * mm, y - 1.8, str(y_value))

        c.setStrokeColor(INK)
        c.line(left, bottom, left, bottom + plot_h)
        c.line(left, bottom, left + plot_w, bottom)
        c.setFont(FONT_BODY, 7)
        c.setFillColor(MUTED)
        for spin in [0, 0.25, 0.5, 0.75, 0.98]:
            x = left + spin / 0.98 * plot_w
            c.drawCentredString(x, bottom - 4 * mm, f"{spin:.2f}")

        points = []
        for index in range(100):
            spin = 0.98 * index / 99
            value = self.isco(spin)
            x = left + spin / 0.98 * plot_w
            y = bottom + (value - 1) / 5 * plot_h
            points.append((x, y))
        c.setStrokeColor(BLUE)
        c.setLineWidth(2)
        path = c.beginPath()
        path.moveTo(*points[0])
        for point in points[1:]:
            path.lineTo(*point)
        c.drawPath(path, stroke=1, fill=0)

        default_spin = 0.72
        default_isco = self.isco(default_spin)
        dx = left + default_spin / 0.98 * plot_w
        dy = bottom + (default_isco - 1) / 5 * plot_h
        c.setFillColor(ORANGE)
        c.circle(dx, dy, 2.2, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 7.5)
        c.drawString(dx + 2 * mm, dy + 1 * mm, f"默认值 {default_isco:.2f} r_g")

        c.setFont(FONT_BOLD, 7.5)
        c.setFillColor(INK)
        c.drawCentredString(left + plot_w / 2, 1.5 * mm, "无量纲自旋 a*")
        c.saveState()
        c.translate(3 * mm, bottom + plot_h / 2)
        c.rotate(90)
        c.drawCentredString(0, 0, "顺行 ISCO / r_g")
        c.restoreState()
        c.restoreState()


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullet(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph("• " + text, styles["bullet"])


def table(
    rows: list[list[str]],
    widths: list[float],
    styles: dict[str, ParagraphStyle],
    header: bool = True,
) -> Table:
    rendered = []
    for row_index, row in enumerate(rows):
        style = styles["table_header"] if header and row_index == 0 else styles["table_body"]
        rendered.append([Paragraph(str(cell), style) for cell in row])
    result = Table(rendered, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.2 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8 * mm),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
            ]
        )
    else:
        commands.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, PAPER]))
    result.setStyle(TableStyle(commands))
    return result


def callout(
    label: str,
    text: str,
    styles: dict[str, ParagraphStyle],
    kind: str = "info",
) -> Table:
    palette = {
        "info": (BLUE, PALE_BLUE),
        "approx": (ORANGE, PALE_ORANGE),
        "ok": (GREEN, PALE_GREEN),
        "warn": (RED, PALE_RED),
    }
    accent, background = palette[kind]
    label_style = ParagraphStyle(
        f"CalloutLabel-{kind}",
        parent=styles["small"],
        fontName=FONT_BOLD,
        textColor=accent,
        fontSize=8,
        leading=11,
        spaceAfter=1 * mm,
    )
    body_style = ParagraphStyle(
        f"CalloutBody-{kind}",
        parent=styles["body"],
        fontSize=8.7,
        leading=14,
        spaceAfter=0,
    )
    content = [
        Paragraph(label, label_style),
        Paragraph(text, body_style),
    ]
    box = Table([[content]], colWidths=[174 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.8, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    return box


def add_section(story: list, title: str, styles: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph(title, styles["h1"]))


def add_subsection(story: list, title: str, styles: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph(title, styles["h2"]))


def build_story(styles: dict[str, ParagraphStyle]) -> list:
    story: list = []

    story.append(Spacer(1, 3 * mm))
    cover_box = Table(
        [
            [
                [
                    Paragraph("实时交互黑洞模型", styles["title"]),
                    Paragraph("原理、实现与使用指南", styles["title"]),
                    Spacer(1, 2 * mm),
                    Paragraph(
                        "基于 WebGL 的 Schwarzschild 光学度规与 Kerr 参数混合实时模型",
                        styles["subtitle"],
                    ),
                    Spacer(1, 8 * mm),
                    Paragraph(
                        "程序：index.html<br/>"
                        "文档版本：2.1<br/>"
                        "生成日期：2026 年 7 月 16 日<br/>"
                        "适用场景：教学、演示、交互探索",
                        styles["cover_meta"],
                    ),
                ]
            ]
        ],
        colWidths=[174 * mm],
        rowHeights=[82 * mm],
    )
    cover_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 10 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 10 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8 * mm),
            ]
        )
    )
    story.append(cover_box)
    story.append(Spacer(1, 6 * mm))
    story.append(CoverBlackHole(174 * mm, 74 * mm))
    story.append(Spacer(1, 6 * mm))
    story.append(
        callout(
            "重要定位",
            "界面中的事件视界、ISCO 和轨道周期采用解析 Kerr 公式；画面中的光线弯曲采用 Schwarzschild 各向同性光学度规，"
            "自旋帧拖曳、盘内缘坐标映射和辐射颜色属于实时近似。该程序不能替代严格 Kerr 零测地线与广义相对论辐射传输代码。",
            styles,
            "approx",
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("目录", styles["toc_h"]))
    toc = TableOfContents()
    toc.levelStyles = [styles["toc1"], styles["toc2"]]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(Spacer(1, 8 * mm))
    story.append(
        callout(
            "阅读建议",
            "第一次使用可先读第 2、3、10 节；需要理解物理近似时阅读第 4 至第 8 节；"
            "进行二次开发或验证时重点阅读第 9、11、12 节。",
            styles,
            "info",
        )
    )
    story.append(PageBreak())

    add_section(story, "1. 摘要与模型定位", styles)
    story.append(
        paragraph(
            "本程序在浏览器 GPU 上为每个像素反向发射一条观察光线。光线进入黑洞附近后，"
            "利用各向同性坐标下的 Schwarzschild 光学折射率近似计算弯曲，并采用二阶中点积分更新位置和方向。"
            "一条光线最终可能被捕获、与薄吸积盘相交，或带着偏折后的方向离开透镜区并查询程序化星空。",
            styles["body"],
        )
    )
    story.append(
        paragraph(
            "辐射部分加入顺行 Kerr ISCO、薄盘零力矩温度轮廓、特殊相对论多普勒因子、"
            "Schwarzschild 引力红移、频率三次方束射、程序噪声条带与近似帧拖曳。"
            "模型目标是在普通桌面 GPU 上保持实时交互，同时保留主要现象的方向、趋势和数量级。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "解析物理量",
            "事件视界半径、顺行 ISCO 半径和 ISCO 坐标周期由 JavaScript 解析公式直接计算，"
            "适合教学计算与数量级检查。",
            styles,
            "info",
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "实时视觉近似",
            "阴影边界、帧拖曳、光子环宽度、盘内缘坐标映射和伪彩色辐射为实时近似，"
            "适合解释现象与参数趋势，不适合天文观测拟合或参数反演。",
            styles,
            "approx",
        )
    )
    add_subsection(story, "1.1 优化版的主要变化", styles)
    story.append(
        table(
            [
                ["模块", "旧实现", "优化版"],
                ["多普勒效应", "线性近似 (1 + βμ)³", "δ = [γ(1 - βμ)]⁻¹，并与引力红移合成为总频移 g"],
                ["强度变换", "独立亮度系数", "使用 g³ 的比强度式束射近似"],
                ["光线积分", "一阶方向更新", "各向同性光学度规 + RK2 中点积分"],
                ["盘温度", "内缘最高的经验热度", "零力矩薄盘形状，内缘通量为零并在外侧达峰"],
                ["实时性能", "固定像素比例", "透镜球裁剪、动态分辨率、96/64/48 步编译降级"],
                ["稳定性", "无恢复与卸载处理", "mediump 安全哈希、时间取模、上下文恢复、观察器清理"],
            ],
            [28 * mm, 56 * mm, 90 * mm],
            styles,
        )
    )
    story.append(PageBreak())

    add_section(story, "2. 三分钟快速上手", styles)
    quick_steps = [
        "打开本对话中的实时模型，等待左上角显示实时 FPS 与质量信息。",
        "调节“质量”，观察事件视界、ISCO 和内盘周期的物理读数。质量增大时 km 与 ms 数值近似成比例增加。",
        "调节“自旋”，比较事件视界、ISCO 与盘内缘变化。自旋越高，顺行 ISCO 越靠近黑洞。",
        "调节“吸积率”，观察盘面亮度、伪色温与临界光线辉光同步变化。该值是归一化视觉控制量。",
        "调节“观测倾角”。5° 接近俯视，85° 接近侧视；高倾角最容易看到多普勒明暗不对称。",
        "在画布上水平拖动改变方位角；垂直拖动可补充调整倾角。使用滚轮或触控板缩放。",
        "单击“暂停运动”冻结盘面时间演化。暂停时继续调节参数仍会立即重绘。",
    ]
    for index, item in enumerate(quick_steps, 1):
        story.append(bullet(f"{index}. {item}", styles))

    add_subsection(story, "2.1 推荐实验", styles)
    story.append(
        table(
            [
                ["实验", "参数", "应观察的现象"],
                ["非旋转基准", "M=8 M☉, a*=0, i=60°", "ISCO 为 6 r_g；画面无自旋拖曳偏置"],
                ["高自旋对照", "M=8 M☉, a*=0.98, i=60°", "ISCO 与周期显著减小，盘内缘视觉上向内移动"],
                ["多普勒不对称", "a*=0.9, 吸积率=80%, i=80°", "接近侧显著增亮，远离侧变暗"],
                ["近轴观察", "i=5°", "盘面接近圆形，左右速度投影和亮度差减弱"],
                ["透镜背景", "吸积率=0%", "盘面消失，背景星空偏折与临界辉光更清楚"],
            ],
            [31 * mm, 58 * mm, 85 * mm],
            styles,
        )
    )
    add_subsection(story, "2.2 如何解读左上角状态", styles)
    story.append(
        paragraph(
            "状态格式示例为“实时 · 48 FPS · 82% · 96步”。其中 FPS 是约 700 ms 窗口的即时估计；"
            "百分比是相对于当前设备像素比上限的内部渲染比例；步数是着色器每条光线的最大积分次数。"
            "若设备无法编译 96 步版本，程序会自动尝试 64 步和 48 步。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    add_section(story, "3. 参数、输出与内部状态", styles)
    story.append(
        table(
            [
                ["参数", "范围 / 默认值", "物理或程序含义", "主要视觉影响", "限制"],
                ["质量 M", "2-20 M☉ / 8", "黑洞质量；用于物理长度、周期与动画时间尺度", "改变内部视觉尺度和轨道动画速率", "没有距离参数，画面大小不是实际角直径"],
                ["自旋 a*", "0-0.98 / 0.72", "顺行无量纲 Kerr 自旋", "改变解析视界、ISCO、帧拖曳项和内盘视觉位置", "不支持负自旋或逆行盘"],
                ["吸积率", "0-100% / 65%", "归一化发光强度", "按近似 Ṁ^(1/4) 改变色温，并调节盘面与临界辉光", "不是 Eddington 比或真实质量流率"],
                ["倾角 i", "5°-85° / 64°", "观察方向与自旋轴夹角", "控制盘的投影扁率与速度视线分量", "为避免极点坐标退化而不取端点"],
                ["方位角 ψ", "拖动 / -0.45 rad", "绕自旋轴的观察方向", "移动亮侧和透镜结构的方向", "无独立滑块"],
                ["缩放 z", "0.72-1.75 / 1", "改变焦距比例", "放大或缩小画面", "不代表相机物理距离"],
            ],
            [23 * mm, 30 * mm, 45 * mm, 45 * mm, 31 * mm],
            styles,
        )
    )
    add_subsection(story, "3.1 界面输出", styles)
    story.append(
        paragraph(
            "画面下方显示“事件视界 km · ISCO km · 内盘周期 ms”。这些数值由解析公式计算，"
            "不是从图像像素反推。默认参数 M=8 M☉、a*=0.72 时，典型结果约为事件视界 20.0 km、"
            "ISCO 39.0 km、内盘周期 1.7 ms。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "不要直接量像素",
            "渲染使用内部无量纲场景尺度，并对质量、焦距和盘半径做视觉映射。"
            "因此不能用画面中的像素直径换算事件视界或 ISCO 的 km 数值。",
            styles,
            "warn",
        )
    )
    story.append(PageBreak())

    add_section(story, "4. 黑洞的基本物理尺度", styles)
    add_subsection(story, "4.1 引力半径与引力时间", styles)
    story.append(paragraph("定义引力半径与引力时间：", styles["body"]))
    story.append(
        Paragraph(
            "r<sub>g</sub> = GM/c<super>2</super> = 1.4766 (M/M☉) km",
            styles["equation"],
        )
    )
    story.append(
        Paragraph(
            "t<sub>g</sub> = GM/c<super>3</super> = 4.9255 (M/M☉) μs",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "黑洞附近的大多数长度都与质量 M 成正比，轨道时间也与 M 成正比。"
            "这正是质量滑块同时影响 km 读数与动画时间尺度的原因。",
            styles["body"],
        )
    )

    add_subsection(story, "4.2 Kerr 外事件视界", styles)
    story.append(
        Paragraph(
            "r<sub>+</sub> = r<sub>g</sub> [1 + √(1 - a*<super>2</super>)]",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "当 a*=0 时，r+=2r_g；自旋增大时，以 r_g 为单位的外视界半径减小。"
            "界面读数使用此式。着色器光线部分使用 Schwarzschild 各向同性坐标中的捕获半径，"
            "因此高自旋时解析读数与黑色捕获区不是同一套几何。",
            styles["body"],
        )
    )

    add_subsection(story, "4.3 顺行最内稳定圆轨道 ISCO", styles)
    story.append(
        Paragraph(
            "Z<sub>1</sub> = 1 + (1-a*<super>2</super>)<super>1/3</super>"
            "[(1+a*)<super>1/3</super> + (1-a*)<super>1/3</super>]",
            styles["equation"],
        )
    )
    story.append(
        Paragraph(
            "Z<sub>2</sub> = √(3a*<super>2</super> + Z<sub>1</sub><super>2</super>)",
            styles["equation"],
        )
    )
    story.append(
        Paragraph(
            "r<sub>ISCO</sub>/r<sub>g</sub> = 3 + Z<sub>2</sub> - "
            "√[(3-Z<sub>1</sub>)(3+Z<sub>1</sub>+2Z<sub>2</sub>)]",
            styles["equation"],
        )
    )
    story.append(IscoChart(174 * mm))
    story.append(
        paragraph(
            "图 1. 顺行 Kerr ISCO 随自旋单调减小。橙点对应默认 a*=0.72。",
            styles["caption"],
        )
    )
    story.append(PageBreak())

    add_section(story, "5. 相机、光线与引力透镜", styles)
    add_subsection(story, "5.1 相机模型", styles)
    story.append(
        Paragraph(
            "C = 8.6 [sin(i)cos(ψ), cos(i), sin(i)sin(ψ)]",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "每个片元将像素坐标归一化为屏幕平面坐标，再由相机前、右、上三个正交方向构造初始光线。"
            "缩放通过焦距因子 0.92/z 改变视场，不移动物理相机。",
            styles["body"],
        )
    )

    add_subsection(story, "5.2 透镜球裁剪", styles)
    story.append(
        paragraph(
            "程序先计算初始光线是否与包围黑洞和吸积盘的透镜球相交。"
            "未相交的像素直接查询程序化星空，避免执行 48-96 次光线积分。"
            "这一裁剪对宽屏画面尤其有效，因为四角大量像素不会靠近黑洞。",
            styles["body"],
        )
    )

    add_subsection(story, "5.3 Schwarzschild 各向同性光学度规", styles)
    story.append(
        Paragraph(
            "n(ρ) = [1 + M/(2ρ)]<super>3</super> / [1 - M/(2ρ)]",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "在静态 Schwarzschild 时空的各向同性坐标中，可以把空间光路写成具有位置相关折射率 n(ρ) 的光学问题。"
            "程序计算 ∇ln n，并只保留垂直于当前方向的分量，使光线转向但保持方向向量归一化。",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "d d̂/ds = ∇ln n - d̂(d̂ · ∇ln n) + f<sub>drag</sub>",
            styles["equation"],
        )
    )
    story.append(
        callout(
            "混合模型",
            "n(ρ) 对 Schwarzschild 情形有明确光学几何来源。f_drag 是与自旋成正比的横向启发式修正，"
            "不是完整 Kerr 测地线项。因此文档称其为“Schwarzschild 光学度规 + Kerr 参数信息”的混合模型。",
            styles,
            "approx",
        )
    )
    story.append(PageBreak())

    add_section(story, "6. 数值积分、阴影与光子临界区", styles)
    add_subsection(story, "6.1 RK2 中点积分", styles)
    story.append(
        paragraph(
            "每步先在当前位置计算曲率 k1，再估计半步方向与半步位置，随后在中点计算 k2 并更新整步方向。"
            "相对于一阶欧拉更新，中点法能在相近开销下减少强弯曲区的方向误差。",
            styles["body"],
        )
    )
    story.append(
        Preformatted(
            "k1      = curvature(position, ray)\n"
            "midRay  = normalize(ray + 0.5*h*k1)\n"
            "midPos  = position + 0.5*h*ray\n"
            "k2      = curvature(midPos, midRay)\n"
            "nextRay = normalize(ray + h*k2)\n"
            "nextPos = position + h*midRay",
            styles["code"],
        )
    )
    story.append(
        paragraph(
            "步长随半径自适应：黑洞附近较小，远处较大。最大步数在着色器编译时固定为 96；"
            "若驱动指令预算不足，则降级到 64 或 48。",
            styles["body"],
        )
    )

    add_subsection(story, "6.2 三种终止结果", styles)
    story.append(PipelineDiagram(174 * mm))
    story.append(
        paragraph(
            "图 2. 从交互输入到像素颜色的实时渲染管线。",
            styles["caption"],
        )
    )
    for text_item in [
        "捕获：各向同性半径小于 1.025 M/2，输出主题自适应的近黑色阴影。",
        "命中盘面：相邻两步跨越 y=0，并且交点位于盘内缘与外缘之间。",
        "逃逸：光线离开透镜球且方向朝外，用最终方向查询星空。",
        "临界：达到最大步数仍未逃逸，视为未解析的临界光线并增强窄环。",
    ]:
        story.append(bullet(text_item, styles))

    add_subsection(story, "6.3 光子临界辉光", styles)
    story.append(
        paragraph(
            "模型不是把光子环当作实体发光表面，而是累计光线在 Schwarzschild 光子球附近的驻留量。"
            "驻留越久，说明该光线越接近临界轨道。"
            "为避免有限步数使环完全消失，还叠加一个受限高斯项。该辉光代表未解析高阶像区域，而非真实局部辐射。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    add_section(story, "7. 吸积盘温度与辐射模型", styles)
    add_subsection(story, "7.1 几何假设", styles)
    story.append(
        paragraph(
            "吸积盘被视为位于 y=0 的无限薄、不透明表面。程序只取观察光线的第一次有效盘面交点，"
            "因此不会累计穿过多层盘面，也不能完整显示次级和更高阶盘像。",
            styles["body"],
        )
    )
    story.append(
        paragraph(
            "内缘由 JavaScript 传入的解析 Kerr ISCO 乘以 0.72 后映射到着色器各向同性场景坐标；"
            "该系数维持合理画面构图，但不是 Boyer-Lindquist 到 Kerr 各向同性坐标的严格变换。"
            "外缘固定为 8 个内部 r_g。",
            styles["body"],
        )
    )

    add_subsection(story, "7.2 零力矩薄盘温度形状", styles)
    story.append(
        Paragraph(
            "T(r) ∝ (r<sub>in</sub>/r)<super>3/4</super>"
            "[1 - √(r<sub>in</sub>/r)]<super>1/4</super>",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "该形状来自经典零力矩薄盘通量 F(r)∝r⁻³[1-√(r_in/r)] 的四次方根。"
            "它使盘面温度在内缘为零，并在约 1.36r_in 附近达到峰值，比旧版“内缘最热”的经验函数更合理。",
            styles["body"],
        )
    )

    add_subsection(story, "7.3 条带、噪声与动画", styles)
    story.append(
        paragraph(
            "盘面细节由价值噪声、非轴对称螺旋相位与团块结构叠加。统一轨道相位驱动细丝沿方位旋转，"
            "速度大致遵循 Ω∝[r^(3/2)+a*]⁻¹，并额外乘以 8M☉/M，使更大质量的黑洞在真实秒尺度下动画更慢。"
            "发射强度使用有界色调映射，避免高吸积率或浅色主题把运动细节压成同一饱和值。"
            "这些结构不是磁流体动力学模拟，只用于显示差分旋转感。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "颜色不是人眼真实颜色",
            "盘面颜色来自宿主主题的两组可视化颜色，并由总频移因子改变冷热混合和亮度。"
            "恒星质量黑洞的真实薄盘峰值通常位于高能波段；本模型使用伪彩色帮助观察结构。",
            styles,
            "warn",
        )
    )
    story.append(PageBreak())

    add_section(story, "8. 相对论多普勒效应与引力红移", styles)
    story.append(DopplerDiagram(174 * mm))
    story.append(
        paragraph(
            "图 3. 高倾角下，盘面接近侧蓝移增亮，远离侧红移变暗。实际亮侧方向还随方位角和旋转方向改变。",
            styles["caption"],
        )
    )
    add_subsection(story, "8.1 特殊相对论多普勒因子", styles)
    story.append(
        Paragraph(
            "δ = 1 / [γ(1 - βμ)]，γ = 1 / √(1 - β<super>2</super>)",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "β=v/c，μ 是盘面切向速度与“从盘面指向观察者”的光线方向之间的夹角余弦。"
            "μ>0 时物质朝向观察者运动，δ 增大；μ<0 时远离，δ 减小。"
            "优化版已包含洛伦兹因子 γ 和正确分母，不再使用旧版 (1+βμ)³ 的线性近似。",
            styles["body"],
        )
    )
    story.append(
        paragraph(
            "局部轨道速度使用 Schwarzschild 静止观察者近似 β≈[R/M-2]⁻¹/²，"
            "再进行上限约束和轻微自旋修正。由于光线几何不是完整 Kerr，β 仍是混合模型中的近似量。",
            styles["body"],
        )
    )

    add_subsection(story, "8.2 引力红移与总频移", styles)
    story.append(
        Paragraph(
            "g<sub>grav</sub> ≈ √(1 - 2M/R)，g = δ · g<sub>grav</sub>",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "程序先把多普勒频移和引力红移合成为总频移 g，再用 g 同时调节伪色温和亮度。"
            "为防止强场近似产生负根或数值爆炸，R、分母、β 与 g 都设置了安全下限和上限。",
            styles["body"],
        )
    )

    add_subsection(story, "8.3 为什么强度取 g³", styles)
    story.append(
        Paragraph(
            "I<sub>ν,obs</sub>(ν<sub>obs</sub>) = g<super>3</super>"
            " I<sub>ν,em</sub>(ν<sub>obs</sub>/g)",
            styles["equation"],
        )
    )
    story.append(
        paragraph(
            "在真空中 Iν/ν³ 沿光线保持不变，因此固定观测频率附近的比强度具有 g³ 因子。"
            "若对全部频率积分，玻尔兹曼总强度通常出现 g⁴ 标度。"
            "本模型使用 g³，是“频带比强度式”的实时近似；它没有积分真实黑体谱或仪器通带。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "当前精度边界",
            "多普勒因子的特殊相对论形式是完整的，但 β、μ 和引力红移来自混合几何近似。"
            "科研级实现应使用 Kerr 光子的守恒量 ξ=Lz/E，并采用 g=[uᵗ(1-Ωξ)]⁻¹。",
            styles,
            "approx",
        )
    )
    story.append(PageBreak())

    add_section(story, "9. WebGL 实现与性能优化", styles)
    add_subsection(story, "9.1 单个全屏三角形", styles)
    story.append(
        paragraph(
            "CPU 只上传一个覆盖裁剪空间的超大三角形。顶点着色器几乎不做计算；"
            "所有相机、光线、盘面与辐射计算都在片元着色器中按像素执行。"
            "渲染关闭 alpha、深度、模板和 MSAA，以减少显存和带宽。",
            styles["body"],
        )
    )
    add_subsection(story, "9.2 主要性能措施", styles)
    performance_items = [
        "透镜球裁剪：不会接近黑洞的像素直接采样星空。",
        "自适应 RK2 步长：远处步长大，强场区步长小。",
        "编译降级：依次尝试 96、64、48 个最大积分步。",
        "动态分辨率：连续两个窗口低于 29 FPS 时降低内部比例，最低为 68%。",
        "质量恢复：连续四个窗口高于 52 FPS 时逐步提高内部比例。",
        "DPR 上限 1.35：避免高 DPI 屏幕把片元数量放大到设备像素比平方。",
        "离屏与后台暂停：IntersectionObserver 和 visibilitychange 阻止不可见时持续占用 GPU。",
        "减少动态效果：系统启用 reduced motion 时默认暂停。",
        "数值安全：mediump 安全哈希、临界环距离限幅、时间 4096 秒取模、方位角归一到 [-π,π]。",
    ]
    for item in performance_items:
        story.append(bullet(item, styles))

    add_subsection(story, "9.3 动态分辨率为何延迟到下一帧", styles)
    story.append(
        paragraph(
            "改变 canvas.width 或 canvas.height 会立即清空绘图缓冲。"
            "因此优化版只在 FPS 统计时记录 pendingQualityScale，并在下一帧绘制之前改变尺寸，"
            "随后立即绘制新帧，避免质量切换时闪现空白。",
            styles["body"],
        )
    )
    add_subsection(story, "9.4 WebGL 上下文恢复与清理", styles)
    story.append(
        paragraph(
            "发生 webglcontextlost 时程序停止 RAF，并进入独立 contextLost 状态；"
            "恢复后重新编译着色器、创建缓冲、重新查询 uniforms 和设置 viewport。"
            "组件从宿主中移除时，程序取消 RAF、断开观察器、移除文档监听并释放 GPU 对象。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    add_section(story, "10. 使用场景与结果解读", styles)
    add_subsection(story, "10.1 质量扫描", styles)
    story.append(
        paragraph(
            "固定 a*=0.72，比较 M=2、8、20 M☉。解析事件视界、ISCO 的 km 数值和轨道周期应与质量近似成正比。"
            "画面内部尺度也会变化，但因没有输入距离，不能解释为真实角直径。",
            styles["body"],
        )
    )
    add_subsection(story, "10.2 自旋扫描", styles)
    story.append(
        table(
            [
                ["a*", "事件视界 / km", "ISCO / km", "ISCO 周期 / ms", "预期趋势"],
                ["0.00", "23.6", "70.9", "3.6", "非旋转基准；ISCO=6r_g"],
                ["0.72", "20.0", "39.0", "1.7", "默认状态；盘内缘和周期明显缩小"],
                ["0.98", "14.2", "19.1", "0.8", "高自旋；解析 ISCO 接近视界"],
            ],
            [18 * mm, 30 * mm, 28 * mm, 30 * mm, 68 * mm],
            styles,
        )
    )
    story.append(
        paragraph(
            "表中取 M=8 M☉，数值按界面公式四舍五入。高自旋时渲染仍采用 Schwarzschild 光学度规，"
            "因此画面阴影的自旋形变仅来自启发式帧拖曳，不能和严格 Kerr 临界曲线逐像素比较。",
            styles["small"],
        )
    )
    add_subsection(story, "10.3 多普勒不对称", styles)
    story.append(
        paragraph(
            "固定高自旋和高吸积率，把倾角从 5° 增至 80°。"
            "近俯视时盘速度主要垂直于视线，μ 接近零，亮度差较弱；"
            "近侧视时 |μ| 增大，接近侧的 δ 与 g³ 显著提升。拖动方位角会让亮侧绕中心移动。",
            styles["body"],
        )
    )
    add_subsection(story, "10.4 透镜与临界光线", styles)
    story.append(
        paragraph(
            "将吸积率降为 0% 可移除盘面交点与辐射，保留星空偏折和临界辉光。"
            "这有助于区分“盘本身发光”与“背景光被弯曲”两种来源。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    add_section(story, "11. 代码结构与维护入口", styles)
    story.append(
        table(
            [
                ["模块", "职责", "维护提示"],
                ["HTML 与控件", "画布、四个滑块、状态、暂停按钮、辅助说明", "保持原生 input 和 button，避免破坏键盘与读屏行为"],
                ["state", "质量、自旋、吸积率、倾角、方位角、缩放、时间和暂停状态", "新增参数时同时更新输出、uniform 与文档"],
                ["vertexSource", "绘制全屏三角形", "通常无需改动"],
                ["fragmentSourceTemplate", "星空、光学曲率、RK2、盘面求交、频移和颜色", "复杂度最高；修改后必须真实 GPU 编译测试"],
                ["initializeWithFallback", "尝试 96/64/48 步着色器", "新增质量档时保持循环上限为编译期常量"],
                ["calculateIsco", "顺行 Kerr ISCO", "输入范围固定为 0-0.98"],
                ["updateReadout", "把 r_g、视界、ISCO、周期转换为 km 与 ms", "解析读数与画面近似必须在文档中区分"],
                ["draw / scheduleFrame", "上传 uniforms、绘制、统计 FPS、合并重绘", "避免在 drawArrays 后直接 resize"],
                ["观察器与事件", "响应尺寸、主题、可见性、指针、滚轮和上下文", "任何新增全局监听都要加入 cleanup"],
            ],
            [36 * mm, 66 * mm, 72 * mm],
            styles,
        )
    )
    add_subsection(story, "11.1 关键着色器片段", styles)
    story.append(
        Preformatted(
            "float gamma = inversesqrt(max(1.0 - beta*beta, 0.05));\n"
            "float delta = 1.0 / max(gamma*(1.0 - beta*mu), 0.08);\n"
            "float gGrav = sqrt(max(0.025, 1.0 - 2.0/max(RoverM, 2.01)));\n"
            "float g = clamp(delta*gGrav, 0.18, 2.5);\n"
            "float beaming = clamp(pow(g, 3.0), 0.02, 9.0);",
            styles["code"],
        )
    )
    story.append(
        paragraph(
            "该片段说明优化版如何把多普勒与引力红移统一为总频移 g。"
            "任何后续升级到 Kerr ZAMO 或守恒量形式时，应保持“先求 g，再处理频谱和强度”的结构。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    add_section(story, "12. 验证计划", styles)
    add_subsection(story, "12.1 解析公式测试", styles)
    analytic_tests = [
        "calculateIsco(0) 必须等于 6r_g。",
        "a* 从 0 增至 0.98 时，顺行 ISCO 应单调减小。",
        "固定自旋时，事件视界 km、ISCO km 和周期 ms 应与质量成正比。",
        "M=8 M☉、a*=0.72 应显示约 20.0 km、39.0 km、1.7 ms。",
        "所有合法参数组合不得产生 NaN 或 Infinity。",
    ]
    for item in analytic_tests:
        story.append(bullet(item, styles))

    add_subsection(story, "12.2 交互测试", styles)
    interaction_tests = [
        "四个滑块输入时立即更新输出与画面。",
        "垂直拖动把倾角限制在 5°-85°，方位角持续归一到 [-π,π]。",
        "缩放限制在 0.72-1.75；到达边界后滚轮应恢复页面滚动。",
        "暂停后时间纹理冻结，但参数调整仍能重绘。",
        "离屏或后台停止动画，返回后 FPS 窗口重新计数。",
        "系统 reduced motion 开启时默认暂停。",
        "WebGL context 恢复后重新出现画面。",
    ]
    for item in interaction_tests:
        story.append(bullet(item, styles))

    add_subsection(story, "12.3 视觉回归状态", styles)
    story.append(
        table(
            [
                ["基准状态", "检查重点"],
                ["默认参数", "环连续、盘面无 NaN 色块、状态读数正确"],
                ["a*=0", "帧拖曳偏置消失或显著减弱"],
                ["a*=0.98", "内盘视觉位置稳定，频移不爆亮"],
                ["i=5°", "盘接近圆形，左右亮度差较弱"],
                ["i=85°", "盘极扁但不丢失，多普勒亮侧方向一致"],
                ["吸积率=0%", "无盘面辐射，星空透镜仍可见"],
                ["最大/最小质量", "动画相位稳定，画面不越界"],
            ],
            [48 * mm, 126 * mm],
            styles,
        )
    )
    story.append(
        callout(
            "当前验证状态",
            "代码已完成 JavaScript 语法、唯一 ID、HTML fragment 合同和静态数值审查。"
            "不同 GPU 的 WebGL 编译与视觉回归仍应在目标浏览器上执行；图像比较建议使用感知阈值而非逐像素完全相等。",
            styles,
            "ok",
        )
    )
    story.append(PageBreak())

    add_section(story, "13. 模型局限性", styles)
    limitations = [
        "没有积分完整 Kerr 度规的零测地线；自旋阴影形变和帧拖曳是启发式修正。",
        "捕获半径使用 Schwarzschild 各向同性坐标，不随自旋按 Kerr 视界变化。",
        "盘内缘使用解析 Kerr ISCO 的视觉坐标映射，而非严格 Kerr 坐标变换。",
        "吸积盘无限薄、无厚度、无自遮挡，只处理首次交点。",
        "没有累积次级和高阶盘像的完整辐射贡献。",
        "不求解 Novikov-Thorne 完整相对论通量、GRMHD、磁场、喷流或辐射散射。",
        "吸积率是归一化亮度参数，不是物理质量流率。",
        "颜色是主题伪彩色，不是黑体谱，也没有模拟观测波段和仪器响应。",
        "多普勒公式包含完整 SR 因子，但局部轨道速度和引力红移仍来自混合近似。",
        "光子环由驻留量和有限宽度补偿生成，不是严格 Kerr 临界曲线。",
        "没有距离、望远镜波束、曝光、噪声或星际散射模型。",
        "只支持 0≤a*≤0.98 的顺行配置，不支持逆行盘。",
    ]
    for item in limitations:
        story.append(bullet(item, styles))
    story.append(
        callout(
            "正确使用结论",
            "该程序适合回答“现象为什么出现”和“参数改变时趋势如何变化”；"
            "不适合从图像反演质量、自旋、吸积率，也不适合生成科研论文中的定量模拟数据。",
            styles,
            "warn",
        )
    )

    add_subsection(story, "13.1 后续升级路线", styles)
    roadmap = [
        "用 Kerr Hamilton 或 Mino 参数严格积分零测地线，得到真实 Kerr 阴影与临界曲线。",
        "使用光子守恒量 ξ=Lz/E 计算 g=[uᵗ(1-Ωξ)]⁻¹。",
        "加入 Novikov-Thorne 通量和黑体/康普顿化频谱查找表。",
        "累积多个盘面交点，显示次级与高阶盘像。",
        "加入距离、视场角和望远镜点扩散函数，实现角尺度标定。",
        "使用 WebGL2 或 WebGPU 的并行能力与浮点纹理缓存。",
        "建立真实 GPU 截图基线和跨浏览器性能基准。",
    ]
    for item in roadmap:
        story.append(bullet(item, styles))
    story.append(PageBreak())

    add_section(story, "14. 故障排查", styles)
    story.append(
        table(
            [
                ["现象", "可能原因", "处理方法"],
                ["显示 WebGL 不可用", "GPU 被禁用、远程环境受限或浏览器不支持", "更新浏览器，启用硬件加速，检查 WebGL 支持"],
                ["渲染初始化失败", "96/64/48 步均编译失败或精度不支持", "尝试其他现代浏览器，查看着色器编译日志"],
                ["FPS 长期很低", "画布过大、GPU 负载高", "缩小窗口，关闭其他 GPU 页面，等待动态分辨率降档"],
                ["动画默认暂停", "系统启用了减少动态效果", "单击“启动运动”"],
                ["滚轮改变了黑洞大小", "指针位于画布内，滚轮用于缩放", "将指针移出画布后滚动页面"],
                ["显卡切换后短暂停止", "WebGL context 丢失并重建", "等待状态恢复；若失败则重新打开模型"],
                ["仍显示旧版静态效果", "浏览器缓存了先前的 index.html", "强制刷新页面或重新打开本地文件"],
            ],
            [40 * mm, 57 * mm, 77 * mm],
            styles,
        )
    )
    add_subsection(story, "14.1 性能记录表", styles)
    story.append(
        table(
            [
                ["设备", "浏览器", "画布像素", "质量/步数", "平均 FPS", "备注"],
                ["待测", "待测", "待测", "待测", "待测", "建议预热 3 秒后记录 10 秒"],
                ["待测", "待测", "待测", "待测", "待测", "高 DPI 与普通 DPI 各测试一次"],
            ],
            [30 * mm, 32 * mm, 31 * mm, 31 * mm, 25 * mm, 25 * mm],
            styles,
        )
    )
    story.append(PageBreak())

    add_section(story, "15. 术语表", styles)
    story.append(
        table(
            [
                ["术语", "说明"],
                ["事件视界", "光和信息无法向外逃逸的边界。"],
                ["黑洞阴影", "由被捕获光线和强引力透镜共同形成的暗区，不等同于事件视界本身。"],
                ["ISCO", "最内稳定圆轨道；薄盘内缘通常与其相关。"],
                ["光子球 / 临界曲线", "接近不稳定光子轨道的光线在观察屏幕上形成的临界结构。"],
                ["帧拖曳", "旋转时空对附近惯性系的拖动效应。"],
                ["多普勒增亮", "朝向观察者运动的辐射因频移和相对论束射而增强。"],
                ["引力红移", "光从强引力区传播到远处时频率降低。"],
                ["光线追踪", "从观察者反向追踪每个像素对应的光路。"],
                ["片元着色器", "在 GPU 上为每个候选像素计算颜色的程序。"],
                ["Uniform", "由 JavaScript 向一次 GPU 绘制传入的全局参数。"],
                ["DPR", "设备像素比；高 DPR 会按平方增加片元数量。"],
            ],
            [40 * mm, 134 * mm],
            styles,
        )
    )
    story.append(PageBreak())

    add_section(story, "16. 参考文献与进一步阅读", styles)
    references = [
        "1. Kerr, R. P. “Gravitational Field of a Spinning Mass as an Example of Algebraically Special Metrics.” "
        "Physical Review Letters 11, 237-238 (1963). DOI: 10.1103/PhysRevLett.11.237.",
        "2. Bardeen, J. M., Press, W. H., and Teukolsky, S. A. “Rotating Black Holes: Locally Nonrotating Frames, "
        "Energy Extraction, and Scalar Synchrotron Radiation.” The Astrophysical Journal 178, 347-369 (1972). "
        "DOI: 10.1086/151796.",
        "3. Page, D. N., and Thorne, K. S. “Disk-Accretion onto a Black Hole. Time-Averaged Structure of Accretion Disk.” "
        "The Astrophysical Journal 191, 499-506 (1974).",
        "4. Cunningham, C. T. “The Effects of Redshifts and Focusing on the Spectrum of an Accretion Disk around a Kerr "
        "Black Hole.” The Astrophysical Journal 202, 788-802 (1975).",
        "5. Luminet, J.-P. “Image of a Spherical Black Hole with Thin Accretion Disk.” Astronomy and Astrophysics 75, "
        "228-235 (1979).",
    ]
    for ref in references:
        story.append(Paragraph(ref, styles["body"]))
    story.append(Spacer(1, 4 * mm))
    story.append(
        paragraph(
            "在线入口（访问日期 2026-07-16）：",
            styles["h3"],
        )
    )
    online = [
        "Kerr 1963: https://doi.org/10.1103/PhysRevLett.11.237",
        "Bardeen, Press, Teukolsky 1972: https://adsabs.harvard.edu/pdf/1972ApJ...178..347B",
        "Cunningham 1975: https://adsabs.harvard.edu/pdf/1975ApJ...202..788C",
        "Luminet 1979 ADS: https://ui.adsabs.harvard.edu/abs/1979A%26A....75..228L/abstract",
    ]
    for item in online:
        story.append(bullet(item, styles))
    story.append(
        callout(
            "文档完成度",
            "本文档描述的是 index.html 2.1 优化版。"
            "若代码中的积分公式、频移模型、质量档或交互范围发生变化，应同步更新第 5 至第 12 节。",
            styles,
            "ok",
        )
    )
    return story


def main() -> None:
    register_fonts()
    styles = build_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = GuideDocTemplate(str(OUTPUT), styles)
    story = build_story(styles)
    doc.multiBuild(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()
