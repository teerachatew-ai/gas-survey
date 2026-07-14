# -*- coding: utf-8 -*-
"""
Fill answers onto the PNGD SL-FO-009-19 (MRS Location Survey) form.
Coordinates were measured from an authoritative PDF export of the original
Excel template (Excel COM "Save As PDF"), so the exported PDF matches the
real form pixel-for-pixel, including the Connection Type diagrams.

Scope: only the non-engineer (ส่วนพัฒนาระบบเครือข่าย) fields are filled.
The three engineer sign-off blocks and the Diameter/Max-Flow reference
table are intentionally left blank for the engineer to complete by hand.
"""
import io
import os

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from pdf_filler import FONT, INK, _register_font  # noqa: F401 (font already registered)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_PDF = os.path.join(BASE_DIR, "iso_forms", "slfo009_original.pdf")
PAGE_W, PAGE_H = 975.74, 1380.39


class Overlay009:
    """Same drawing conventions as pdf_filler.Overlay, sized for this
    form's larger ~25pt checkbox squares."""

    def __init__(self, c):
        self.c = c

    def text(self, x, bottom, value, size=13, max_w=None, lift=6):
        value = (value or "").strip()
        if not value:
            return
        if max_w:
            while size > 6 and pdfmetrics.stringWidth(value, FONT, size) > max_w:
                size -= 0.5
        self.c.setFont(FONT, size)
        self.c.setFillColorRGB(*INK)
        self.c.drawString(x, PAGE_H - bottom + lift, value)

    def ctext(self, cx, bottom, value, size=13, max_w=None, lift=6):
        value = (value or "").strip()
        if not value:
            return
        if max_w:
            while size > 6 and pdfmetrics.stringWidth(value, FONT, size) > max_w:
                size -= 0.5
        self.c.setFont(FONT, size)
        self.c.setFillColorRGB(*INK)
        self.c.drawCentredString(cx, PAGE_H - bottom + lift, value)

    def text_2line(self, x1, bottom1, x2, bottom2, value, size=13, max_w1=None, max_w2=None, lift=6):
        """Word-wrap `value` across two blank lines when it doesn't fit on one."""
        value = (value or "").strip()
        if not value:
            return
        if max_w1 and pdfmetrics.stringWidth(value, FONT, size) <= max_w1:
            self.text(x1, bottom1, value, size=size, max_w=max_w1, lift=lift)
            return
        words = value.split(" ")
        line1, rest = "", words[:]
        while rest and max_w1 and pdfmetrics.stringWidth(line1 + (" " if line1 else "") + rest[0], FONT, size) <= max_w1:
            line1 = (line1 + " " + rest.pop(0)).strip() if line1 else rest.pop(0)
        line2 = " ".join(rest)
        self.text(x1, bottom1, line1, size=size, max_w=max_w1, lift=lift)
        self.text(x2, bottom2, line2, size=size, max_w=max_w2, lift=lift)

    def check(self, cx, bottom, on=True, lift=8):
        if not on:
            return
        y = PAGE_H - bottom + lift
        c = self.c
        c.setStrokeColorRGB(*INK)
        c.setLineWidth(2.0)
        c.setLineCap(1)
        c.line(cx - 6.5, y + 2.5, cx - 1.5, y - 4.5)
        c.line(cx - 1.5, y - 4.5, cx + 7.5, y + 9.5)


def _g(data, key):
    v = data.get(key, "")
    return v.strip() if isinstance(v, str) else v


def fill_slfo009(data, out_path=None):
    """`data` is the iso_documents.data dict (see app.py ISO009_FIELDS)."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    o = Overlay009(c)

    # ---------------- header ----------------
    o.text(133, 88.0, _g(data, "company_name"), max_w=372)
    o.text(587, 88.0, _g(data, "area"), max_w=142)
    o.text(812, 88.0, _g(data, "form_date"), max_w=117)
    o.text(158, 117.7, _g(data, "project_no"), max_w=197)
    factory = _g(data, "factory_type")
    o.check(493.0, 118.2, factory == "existing")
    o.check(617.9, 118.2, factory == "new")
    o.text(857, 117.3, _g(data, "revision_no"), max_w=72)

    # ---------------- Part 1 ----------------
    o.text_2line(183, 181.2, 58, 211.1, _g(data, "land_plot_address"),
                max_w1=267, max_w2=392)
    pipe = _g(data, "pipe_within_500m")
    o.check(518.0, 182.2, pipe == "yes")
    o.check(742.9, 182.2, pipe == "no")
    o.text(758, 211.1, _g(data, "pipe_distance_m"), max_w=147)
    o.check(238.6, 240.2, bool(data.get("attach_hardcopy")))
    o.check(343.1, 240.2, bool(data.get("attach_electronic")))
    o.ctext(367.55, 310.5, _g(data, "surveyor_name"), size=12, max_w=170, lift=4)
    o.ctext(367.55, 356.7, _g(data, "surveyor_date"), max_w=170)

    # ---------------- Part 2 ----------------
    heating = _g(data, "gas_heating_zone")
    o.check(518.0, 391.7, heating == "west")
    o.check(518.0, 421.2, heating == "east")
    scope = _g(data, "estimate_scope")
    o.check(63.65, 421.2, scope == "main_pipe")
    o.check(238.6, 421.2, scope == "all")
    o.text(358, 455.1, _g(data, "commissioning_date"), max_w=222)
    o.text(682, 455.1, _g(data, "gas_consumption_mmbtu_yr"), max_w=172)

    conn_type = _g(data, "connection_type")
    type_x = {"1": 63.65, "2": 138.6, "3": 265.85, "4": 393.0, "5": 543.0, "6": 742.9}
    if conn_type in type_x:
        o.check(type_x[conn_type], 503.9, True)

    # NG flow rate table — MRS rows 1-3, Pressure / Max flow / Year 1-15
    row_bottoms = [780.4, 805.0, 829.6]
    year_cx = [200.1, 252.35, 304.6, 354.6, 404.55, 454.5, 504.5, 554.5,
               604.45, 654.4, 704.4, 754.4, 804.4, 854.35, 904.3]
    for r in range(1, 4):
        b = row_bottoms[r - 1]
        o.ctext(100.15, b, _g(data, f"mrs{r}_pressure"), size=11, max_w=44)
        o.ctext(150.1, b, _g(data, f"mrs{r}_max_flow"), size=11, max_w=44)
        for y in range(1, 16):
            o.ctext(year_cx[y - 1], b, _g(data, f"mrs{r}_year{y}"), size=10, max_w=44)

    purpose = data.get("purpose", [])
    if isinstance(purpose, str):
        purpose = [purpose]
    o.check(63.65, 863.1, "slfo008" in purpose)
    o.check(293.1, 863.1, "slfo010_011_001" in purpose)
    o.check(767.85, 863.1, bool(data.get("attach_potential_demand")))

    # ---------------- MRS & Construction Information ----------------
    o.text(128, 1080.1, _g(data, "mrs_type"), max_w=202)
    stock = _g(data, "mrs_in_stock")
    o.check(443.0, 1080.5, stock == "available")
    o.check(543.0, 1080.5, stock == "not_available")
    o.text(707, 1080.1, _g(data, "mrs_no"), max_w=198)
    o.text(178, 1104.5, _g(data, "outlet_pressure_barg"), max_w=127)
    o.text(178, 1129.2, _g(data, "construction_period_days"), max_w=127)
    o.check(138.6, 1154.3, bool(data.get("attach_construction_schedule")))
    o.check(318.1, 1154.3, bool(data.get("attach_mrs_location_drawing")))
    o.check(138.6, 1203.5, bool(data.get("mrs_renew_available")))

    c.showPage()
    c.save()
    buf.seek(0)

    overlay_reader = PdfReader(buf)
    base_reader = PdfReader(ORIGINAL_PDF)
    writer = PdfWriter()
    page = base_reader.pages[0]
    page.merge_page(overlay_reader.pages[0])
    writer.add_page(page)

    out = io.BytesIO()
    writer.write(out)
    pdf_bytes = out.getvalue()
    if out_path:
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
    return pdf_bytes
