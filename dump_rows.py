# -*- coding: utf-8 -*-
"""Print words grouped into visual lines: 'y | text@x0..x1' for placement design."""
import json, sys

with open(r"D:\Claude Code\gas-survey\coords.json", encoding="utf-8") as f:
    pages = json.load(f)

page_no = int(sys.argv[1])
ymin = float(sys.argv[2]) if len(sys.argv) > 2 else 0
ymax = float(sys.argv[3]) if len(sys.argv) > 3 else 9999

p = pages[page_no - 1]
lines = {}
for w in p["words"]:
    if not (ymin <= w["top"] <= ymax):
        continue
    key = round(w["top"] / 4) * 4
    lines.setdefault(key, []).append(w)

for key in sorted(lines):
    ws = sorted(lines[key], key=lambda w: w["x0"])
    parts = [f"{w['text']}@{w['x0']:.0f}-{w['x1']:.0f}" for w in ws]
    print(f"y={ws[0]['top']:.1f}-{ws[0]['bottom']:.1f} | " + "  ".join(parts))
