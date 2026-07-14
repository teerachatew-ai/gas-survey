# -*- coding: utf-8 -*-
import pypdfium2 as pdfium
from pdf_filler_009 import fill_slfo009

sample = {
    "company_name": "บริษัท ทดสอบอุตสาหกรรม จำกัด",
    "area": "ระยอง",
    "form_date": "14/07/2569",
    "project_no": "PRJ-2026-0042",
    "factory_type": "existing",
    "revision_no": "0",
    "land_plot_address": "88/8 หมู่ 5 นิคมฯ อมตะซิตี้ ต.มาบยางพร อ.ปลวกแดง จ.ระยอง 21140",
    "pipe_within_500m": "yes",
    "pipe_distance_m": "120",
    "attach_hardcopy": True,
    "attach_electronic": True,
    "surveyor_name": "สมชาย ใจดี",
    "surveyor_date": "14/07/2569",
    "gas_heating_zone": "east",
    "estimate_scope": "all",
    "commissioning_date": "01/2027",
    "gas_consumption_mmbtu_yr": "170,000",
    "connection_type": "2",
    "mrs1_pressure": "1.5", "mrs1_max_flow": "1,350",
    "mrs1_year1": "1,200", "mrs1_year2": "1,350", "mrs1_year3": "1,500",
    "mrs1_year4": "1,650", "mrs1_year5": "1,800", "mrs1_year6": "1,950",
    "mrs1_year7": "2,100",
    "purpose": ["slfo010_011_001"],
    "attach_potential_demand": True,
    "mrs_type": "Skid MRS",
    "mrs_in_stock": "available",
    "mrs_no": "MRS-2026-015",
    "outlet_pressure_barg": "1.5",
    "construction_period_days": "45",
    "attach_construction_schedule": True,
    "attach_mrs_location_drawing": True,
    "mrs_renew_available": False,
}

pdf = fill_slfo009(sample, r"D:\Claude Code\gas-survey\test_009_filled.pdf")
doc = pdfium.PdfDocument(r"D:\Claude Code\gas-survey\test_009_filled.pdf")
img = doc[0].render(scale=1.6).to_pil()
crop = img.crop((0, int(img.height * 0.18), int(img.width*0.5), int(img.height * 0.28)))
crop.save(r"D:\Claude Code\gas-survey\test_009_sig.png")
print("done", len(pdf))
