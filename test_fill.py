# -*- coding: utf-8 -*-
import pypdfium2 as pdfium
from pdf_filler import fill_pdf

sample = {
    "inquiry_method": "email", "inquiry_other": "",
    "company_name": "บริษัท ทดสอบอุตสาหกรรม จำกัด (Test Industry Co., Ltd.)",
    "address": "88/8 หมู่ 5 นิคมอุตสาหกรรมอมตะซิตี้ ต.มาบยางพร อ.ปลวกแดง จ.ระยอง 21140",
    "contact_person": "คุณสมชาย ใจดี (ผู้จัดการโรงงาน)",
    "email": "somchai@test-industry.co.th",
    "nationality": "ไทย/ญี่ปุ่น", "business_type": "ผลิตชิ้นส่วนยานยนต์",
    "mobile": "081-234-5678", "tel": "038-123-456", "fax": "038-123-457",
    "fuel1_type": "fuel_oil", "fuel1_grade": "C", "fuel1_unit": "liter",
    "fuel2_type": "lpg", "fuel2_unit": "kg",
    "fuel3_type": "other", "fuel3_type_other": "ถ่านหิน", "fuel3_unit": "other", "fuel3_unit_other": "ตัน",
    "form_date": "6 กรกฎาคม 2569",
    "product_current": "ชิ้นส่วนยานยนต์", "product_expansion": "แบตเตอรี่ EV",
    "startup_current": "01/01/2015", "startup_expansion": "06/2027",
    "ophour_current": "20 ชม./วัน", "ophour_expansion": "24 ชม./วัน",
    "opday_current": "300 วัน/ปี", "opday_expansion": "330 วัน/ปี",
    "plant_location": "อมตะซิตี้ ระยอง", "land_plot": "G-12/3",
    "purpose": ["steam", "drying", "other"], "steam_pressure": "10",
    "purpose_other": "ให้ความร้อนเตาอบสี",
    "ng_supply_date": "01/01/27", "ng_pressure": "1.5 Bar (g)",
    "machine1_type": "Water Steam Boiler", "machine1_capacity": "10 ton/hr",
    "machine1_ophour": "20", "machine1_days": "300", "machine1_character": "Steady", "machine1_qty": "2",
    "machine2_type": "Air Heater", "machine2_capacity": "400,000 Btu/hr",
    "machine2_ophour": "8", "machine2_days": "250", "machine2_character": "On-OFF", "machine2_qty": "1",
    "elec_bill": True, "elec_profile": True,
    "elec_base": "12", "elec_peak": "15", "elec_offpeak": "8",
    "elec_source": ["pea", "self"], "pea_kv": "115", "self_mw": "2.5", "self_method": "Solar Rooftop",
    "chiller_profile": True, "chiller_avg": "450", "chiller_base": "300",
    "chiller1_rt": "250", "chiller1_type": "Water-cooled screw", "chiller1_cop": "5.2",
    "chiller2_rt": "250", "chiller2_type": "Air-cooled", "chiller2_cop": "3.1",
    "staff_factory": "existing", "staff_received_date": "06/07/2026",
    "staff_recorded_date": "06/07/2026", "staff_revision": "0", "staff_recorder": "ธีรเชษฐ์",
    "pdpa_accept": True, "pdpa_name": "สมชาย ใจดี", "pdpa_title": "ผู้จัดการโรงงาน",
}
for r in range(1, 13):
    sample[f"month_label_{r}"] = f"{r:02d}/2025"
    sample[f"fuel1_cons_{r}"] = f"{40000 + r * 250:,}"
    sample[f"fuel1_price_{r}"] = "18.50"
    sample[f"fuel2_cons_{r}"] = f"{9000 + r * 100:,}"
    sample[f"fuel2_price_{r}"] = "26.00"
    sample[f"fuel3_cons_{r}"] = f"{120 + r}"
    sample[f"fuel3_price_{r}"] = "3,200"
for i in range(1, 8):
    sample[f"year_{i}"] = str(2026 + i)
    sample[f"cons_year_{i}"] = f"{150000 + i * 20000:,}"
    sample[f"cap_year_{i}"] = f"{1200 + i * 150:,}"

pdf = fill_pdf(sample, r"D:\Claude Code\gas-survey\test_filled.pdf")
doc = pdfium.PdfDocument(r"D:\Claude Code\gas-survey\test_filled.pdf")
print("pages:", len(doc))
for i, page in enumerate(doc):
    img = page.render(scale=2.2).to_pil()
    img.save(rf"D:\Claude Code\gas-survey\test_p{i+1}.png")
print("done", len(pdf))
