# -*- coding: utf-8 -*-
"""End-to-end test: submit survey -> admin login -> list -> export PDF."""
import urllib.request
import urllib.parse
import http.cookiejar

BASE = "http://127.0.0.1:5000"
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def post(path, fields):
    data = urllib.parse.urlencode(fields, doseq=True).encode()
    req = urllib.request.Request(BASE + path, data=data)
    return opener.open(req)


def get(path):
    return opener.open(BASE + path)


fields = {
    "inquiry_method": "email",
    "company_name": "บริษัท สยามเซรามิก จำกัด",
    "address": "99 หมู่ 3 นิคมฯ บางปู สมุทรปราการ 10280",
    "contact_person": "คุณวิภา สุขใจ",
    "email": "wipa@siamceramic.co.th",
    "nationality": "ไทย",
    "business_type": "เซรามิก",
    "mobile": "089-999-8888",
    "tel": "02-323-4455",
    "fax": "02-323-4456",
    "fuel1_type": "lpg", "fuel1_unit": "kg",
    "month_label_1": "Jan-25", "fuel1_cons_1": "12,000", "fuel1_price_1": "25.5",
    "month_label_2": "Feb-25", "fuel1_cons_2": "11,500", "fuel1_price_2": "25.5",
    "year_1": "2027", "cons_year_1": "80,000", "cap_year_1": "600",
    "product_current": "กระเบื้องเซรามิก",
    "startup_current": "2010",
    "ophour_current": "24", "opday_current": "330",
    "plant_location": "นิคมฯ บางปู", "land_plot": "B-07",
    "purpose": ["melting", "drying"],
    "ng_supply_date": "01/06/27", "ng_pressure": "1 Bar (g)",
    "machine1_type": "Kiln", "machine1_capacity": "5 MW",
    "machine1_ophour": "24", "machine1_days": "330",
    "machine1_character": "Steady", "machine1_qty": "3",
    "elec_bill": "1",
    "elec_base": "8", "elec_peak": "10", "elec_offpeak": "6",
    "elec_source": ["mea"], "mea_kv": "24",
    "chiller_avg": "120", "chiller_base": "80",
    "chiller1_rt": "150", "chiller1_type": "Air-cooled", "chiller1_cop": "3.2",
}

r = post("/survey", fields)
print("submit ->", r.status, r.url)

r = post("/admin/login", {"username": "admin", "password": "pngd@2026"})
print("login ->", r.status, r.url)

r = get("/admin")
body = r.read().decode()
print("admin list contains company:", "สยามเซรามิก" in body)

# find newest id from the list page
import re
ids = [int(m) for m in re.findall(r"/admin/(\d+)", body)]
sid = max(ids)
print("newest submission id:", sid)

r = get(f"/admin/{sid}/pdf?download=1")
pdf = r.read()
print("pdf bytes:", len(pdf), "content-type:", r.headers.get("Content-Type"))
with open(r"D:\Claude Code\gas-survey\e2e_export.pdf", "wb") as f:
    f.write(pdf)

# staff fields then re-export
r = post(f"/admin/{sid}/staff", {"staff_factory": "new", "staff_received_date": "06/07/2026",
                                 "staff_recorded_date": "06/07/2026", "staff_revision": "1",
                                 "staff_recorder": "FE03"})
print("staff save ->", r.status)
r = get(f"/admin/{sid}/pdf")
with open(r"D:\Claude Code\gas-survey\e2e_export2.pdf", "wb") as f:
    f.write(r.read())

import pypdfium2 as pdfium
doc = pdfium.PdfDocument(r"D:\Claude Code\gas-survey\e2e_export2.pdf")
for i in (0, 2):
    doc[i].render(scale=2.2).to_pil().save(rf"D:\Claude Code\gas-survey\e2e_p{i+1}.png")
print("OK")
