# -*- coding: utf-8 -*-
"""Dump word coordinates from the original PDF so we can anchor overlay fields."""
import json
import pdfplumber

OUT = []
with pdfplumber.open(r"D:\Claude Code\gas-survey\original_form.pdf") as pdf:
    for pno, page in enumerate(pdf.pages):
        info = {
            "page": pno + 1,
            "width": page.width,
            "height": page.height,
            "words": [],
        }
        for w in page.extract_words(use_text_flow=False, keep_blank_chars=False):
            info["words"].append({
                "text": w["text"],
                "x0": round(w["x0"], 1),
                "x1": round(w["x1"], 1),
                "top": round(w["top"], 1),
                "bottom": round(w["bottom"], 1),
            })
        OUT.append(info)

with open(r"D:\Claude Code\gas-survey\coords.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)

for p in OUT:
    print(f"--- page {p['page']} size {p['width']}x{p['height']} words={len(p['words'])}")
