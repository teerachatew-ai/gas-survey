# -*- coding: utf-8 -*-
"""
Fill customer answers onto the original PNGD SL-FO-014-09 questionnaire PDF.
Coordinates were measured from the original PDF's text layer (pdfplumber),
so the exported PDF is the original form with answers overlaid in place.
"""
import io
import os

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_PDF = os.path.join(BASE_DIR, "original_form.pdf")

PAGE_W, PAGE_H = 595.32, 841.92
FONT = "ThaiFont"
INK = (0.05, 0.15, 0.55)  # pen-blue answers, clearly distinct from the form


def _register_font():
    # bundled font first so output is identical on Windows and Linux (Render)
    for path in (
        os.path.join(BASE_DIR, "fonts", "Sarabun-Regular.ttf"),
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\LeelawUI.ttf",
        r"C:\Windows\Fonts\leelawad.ttf",
    ):
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(FONT, path))
            return
    raise RuntimeError("No Thai-capable font found")


_register_font()


class Overlay:
    """Draw helpers; y arguments are pdfplumber 'bottom' values (from page top)."""

    def __init__(self, c):
        self.c = c

    def text(self, x, bottom, value, size=8, max_w=None, lift=2.0):
        value = (value or "").strip()
        if not value:
            return
        if max_w:
            while size > 5 and pdfmetrics.stringWidth(value, FONT, size) > max_w:
                size -= 0.5
        self.c.setFont(FONT, size)
        self.c.setFillColorRGB(*INK)
        self.c.drawString(x, PAGE_H - bottom + lift, value)

    def ctext(self, cx, bottom, value, size=8, max_w=None, lift=3.5):
        value = (value or "").strip()
        if not value:
            return
        if max_w:
            while size > 5 and pdfmetrics.stringWidth(value, FONT, size) > max_w:
                size -= 0.5
        self.c.setFont(FONT, size)
        self.c.setFillColorRGB(*INK)
        self.c.drawCentredString(cx, PAGE_H - bottom + lift, value)

    def check(self, cx, bottom, on=True, lift=3.0):
        if not on:
            return
        y = PAGE_H - bottom + lift
        c = self.c
        c.setStrokeColorRGB(*INK)
        c.setLineWidth(1.2)
        c.setLineCap(1)
        c.line(cx - 2.6, y + 1.6, cx - 0.7, y - 0.6)
        c.line(cx - 0.7, y - 0.6, cx + 3.2, y + 5.2)


def _g(data, key):
    v = data.get(key, "")
    return v.strip() if isinstance(v, str) else v


def _page1(o, d):
    # 1. General information — inquiry channel
    inquiry = _g(d, "inquiry_method")
    o.check(178.5, 103.1, inquiry == "inquire")
    o.check(257.0, 103.1, inquiry == "fax")
    o.check(332.0, 103.1, inquiry == "email")
    o.check(420.7, 103.1, inquiry == "other")
    if inquiry == "other":
        o.text(473, 103.1, _g(d, "inquiry_other"), max_w=92)

    o.text(135, 117.1, _g(d, "company_name"), size=9, max_w=425)
    o.text(90, 130.1, _g(d, "address"), size=9, max_w=475)
    o.text(137, 143.1, _g(d, "contact_person"), size=9, max_w=215)
    o.text(413, 143.1, _g(d, "email"), size=9, max_w=150)
    o.text(140, 156.1, _g(d, "nationality"), size=9, max_w=90)
    o.text(332, 156.1, _g(d, "business_type"), size=9, max_w=230)
    o.text(116, 169.1, _g(d, "mobile"), size=9, max_w=112)
    o.text(288, 169.1, _g(d, "tel"), size=9, max_w=115)
    o.text(461, 169.1, _g(d, "fax"), size=9, max_w=102)

    # 2.1 fuel columns
    cb_x = [86.0, 251.0, 417.0]              # main checkbox centres per column
    grade_a = [152.5, 317.0, 483.5]
    grade_c = [178.0, 343.0, 509.0]
    other_x = [142, 307, 473]
    unit_other_x = [141, 306, 472]
    for i in range(3):
        n = i + 1
        ftype = _g(d, f"fuel{n}_type")
        o.check(cb_x[i], 284.7, ftype == "fuel_oil")
        if ftype == "fuel_oil":
            grade = _g(d, f"fuel{n}_grade")
            o.check(grade_a[i], 297.7, grade == "A")
            o.check(grade_c[i], 297.7, grade == "C")
        o.check(cb_x[i], 310.8, ftype == "lpg")
        o.check(cb_x[i], 323.7, ftype == "diesel")
        o.check(cb_x[i], 336.7, ftype == "natural_gas")
        o.check(cb_x[i], 349.8, ftype == "other")
        if ftype == "other":
            o.text(other_x[i], 349.8, _g(d, f"fuel{n}_type_other"), max_w=70)

        unit = _g(d, f"fuel{n}_unit")
        o.check(cb_x[i], 376.3, unit == "liter")
        o.check(cb_x[i], 389.3, unit == "kg")
        o.check(cb_x[i], 402.2, unit == "mmbtu")
        o.check(cb_x[i], 415.3, unit == "other")
        if unit == "other":
            o.text(unit_other_x[i], 415.3, _g(d, f"fuel{n}_unit_other"), size=7, max_w=45)

    # 2.1 monthly table (12 rows)
    borders = [414.8, 432.3, 449.8, 467.2, 484.7, 502.3, 519.8,
               537.3, 554.8, 572.2, 589.8, 607.3, 624.8]
    cons_cx = [121.0, 286.7, 453.2]
    price_cx = [203.5, 369.9, 536.5]
    for r in range(1, 13):
        bottom = borders[r]
        o.ctext(53.2, bottom, _g(d, f"month_label_{r}"), max_w=41)
        for i in range(3):
            n = i + 1
            o.ctext(cons_cx[i], bottom, _g(d, f"fuel{n}_cons_{r}"), max_w=88)
            o.ctext(price_cx[i], bottom, _g(d, f"fuel{n}_price_{r}"), max_w=68)

    # 2.2 future natural-gas demand (7 years)
    year_cx = [171.5, 235.0, 299.0, 362.5, 426.5, 490.0, 552.5]
    cons_cx2 = [160.7, 224.5, 288.0, 351.8, 415.6, 479.6, 542.1]
    for i in range(1, 8):
        o.ctext(year_cx[i - 1], 690.7, _g(d, f"year_{i}"), size=7.5, max_w=28, lift=2.5)
        o.ctext(cons_cx2[i - 1], 722.7, _g(d, f"cons_year_{i}"), max_w=60, lift=6)
        o.ctext(cons_cx2[i - 1], 745.9, _g(d, f"cap_year_{i}"), max_w=60, lift=6)

    o.text(462, 772.8, _g(d, "form_date"), size=9, max_w=100)


def _page2(o, d):
    # 3.1 project and plan
    cur_cx, exp_cx = 353.9, 500.2
    o.ctext(cur_cx, 130.6, _g(d, "product_current"), max_w=140, lift=2.5)
    o.ctext(exp_cx, 130.6, _g(d, "product_expansion"), max_w=136, lift=2.5)
    o.ctext(cur_cx, 144.1, _g(d, "startup_current"), max_w=140, lift=2.5)
    o.ctext(exp_cx, 144.1, _g(d, "startup_expansion"), max_w=136, lift=2.5)
    o.ctext(cur_cx, 157.6, _g(d, "ophour_current"), max_w=140, lift=2.5)
    o.ctext(exp_cx, 157.6, _g(d, "ophour_expansion"), max_w=136, lift=2.5)
    o.ctext(cur_cx, 171.1, _g(d, "opday_current"), max_w=140, lift=2.5)
    o.ctext(exp_cx, 171.1, _g(d, "opday_expansion"), max_w=136, lift=2.5)

    # 3.2 natural-gas requirement
    o.text(180, 203.0, _g(d, "plant_location"), size=8, max_w=90)
    o.text(170, 219.1, _g(d, "land_plot"), size=9, max_w=110)

    purposes = d.get("purpose", [])
    if isinstance(purposes, str):
        purposes = [purposes]
    o.check(230.0, 235.5, "steam" in purposes)
    if "steam" in purposes:
        o.text(455, 235.5, _g(d, "steam_pressure"), size=9, max_w=70)
    o.check(230.0, 251.5, "drying" in purposes)
    o.check(305.0, 251.5, "melting" in purposes)
    o.check(230.0, 266.7, "other" in purposes)
    if "other" in purposes:
        o.text(308, 266.7, _g(d, "purpose_other"), size=9, max_w=185)

    o.text(320, 285.6, _g(d, "ng_supply_date"), size=9, max_w=118)
    o.text(254, 309.6, _g(d, "ng_pressure"), size=9, max_w=88)

    # 3.3 machines
    type_rows = [420.6, 488.5, 556.4, 624.4]
    hour_rows = [443.3, 511.2, 579.0, 646.9]
    char_rows = [465.8, 533.8, 601.7, 669.6]
    for m in range(1, 5):
        i = m - 1
        o.text(133, type_rows[i], _g(d, f"machine{m}_type"), max_w=170)
        o.text(428, type_rows[i], _g(d, f"machine{m}_capacity"), max_w=110)
        o.text(244, hour_rows[i], _g(d, f"machine{m}_ophour"), max_w=60)
        o.text(403, hour_rows[i], _g(d, f"machine{m}_days"), max_w=130)
        o.text(185, char_rows[i], _g(d, f"machine{m}_character"), max_w=118)
        o.text(393, char_rows[i], _g(d, f"machine{m}_qty"), max_w=140)


def _page3(o, d):
    # 4.1 electricity
    o.check(244.5, 117.5, bool(d.get("elec_bill")))
    o.check(403.5, 117.5, bool(d.get("elec_profile")))
    o.text(100, 140.2, _g(d, "elec_base"), size=9, max_w=125)
    o.text(100, 162.8, _g(d, "elec_peak"), size=9, max_w=125)
    o.text(100, 185.5, _g(d, "elec_offpeak"), size=9, max_w=125)

    sources = d.get("elec_source", [])
    if isinstance(sources, str):
        sources = [sources]
    o.check(59.0, 230.7, "pea" in sources)
    if "pea" in sources:
        o.text(211, 230.7, _g(d, "pea_kv"), size=9, max_w=38)
    o.check(59.0, 253.4, "mea" in sources)
    if "mea" in sources:
        o.text(210, 253.4, _g(d, "mea_kv"), size=9, max_w=38)
    o.check(59.0, 276.0, "spp" in sources)
    o.check(59.0, 298.7, "self" in sources)
    if "self" in sources:
        o.text(185, 298.7, _g(d, "self_mw"), size=9, max_w=60)
        o.text(418, 298.7, _g(d, "self_method"), size=8, max_w=140)
    o.check(59.0, 321.3, "other" in sources)
    if "other" in sources:
        o.text(128, 321.3, _g(d, "elec_source_other"), size=9, max_w=430)

    # 4.2 chiller
    o.check(272.5, 366.6, bool(d.get("chiller_profile")))
    o.text(95, 389.1, _g(d, "chiller_avg"), size=9, max_w=128)
    o.text(108, 411.8, _g(d, "chiller_base"), size=9, max_w=115)
    rows = [434.5, 457.1, 479.8]
    for cnum in range(1, 4):
        b = rows[cnum - 1]
        o.text(102, b, _g(d, f"chiller{cnum}_rt"), size=9, max_w=55)
        o.text(228, b, _g(d, f"chiller{cnum}_type"), size=8, max_w=135)
        o.text(397, b, _g(d, f"chiller{cnum}_cop"), size=9, max_w=120)

    # staff-only box (filled from the back office)
    factory = _g(d, "staff_factory")
    o.check(111.0, 596.0, factory == "existing", lift=2.0)
    o.check(232.0, 596.0, factory == "new", lift=2.0)
    o.text(106, 614.6, _g(d, "staff_received_date"), size=9, max_w=170)
    o.text(370, 614.6, _g(d, "staff_recorded_date"), size=9, max_w=185)
    o.text(92, 631.2, _g(d, "staff_revision"), size=9, max_w=185)
    o.text(353, 631.2, _g(d, "staff_recorder"), size=9, max_w=200)

    o.text(462, 661.7, _g(d, "form_date"), size=9, max_w=100)


def fill_pdf(data, out_path=None):
    """Overlay `data` (dict of answers) onto the original form.
    Returns the PDF bytes; also writes to out_path when given."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    o = Overlay(c)
    _page1(o, data)
    c.showPage()
    o = Overlay(c)
    _page2(o, data)
    c.showPage()
    o = Overlay(c)
    _page3(o, data)
    c.showPage()
    c.save()
    buf.seek(0)

    overlay_reader = PdfReader(buf)
    base_reader = PdfReader(ORIGINAL_PDF)
    writer = PdfWriter()
    for i, page in enumerate(base_reader.pages):
        if i < len(overlay_reader.pages):
            page.merge_page(overlay_reader.pages[i])
        writer.add_page(page)

    out = io.BytesIO()
    writer.write(out)
    pdf_bytes = out.getvalue()
    if out_path:
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
    return pdf_bytes
