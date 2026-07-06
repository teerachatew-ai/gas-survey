# -*- coding: utf-8 -*-
"""Dump table grid lines (horizontal/vertical) per page to locate table cells."""
import pdfplumber

with pdfplumber.open(r"D:\Claude Code\gas-survey\original_form.pdf") as pdf:
    for pno, page in enumerate(pdf.pages):
        print(f"=== PAGE {pno+1} (w={page.width} h={page.height}) ===")
        hlines = set()
        vlines = set()
        for l in page.lines + page.rects:
            x0, x1 = round(l["x0"], 1), round(l["x1"], 1)
            t, b = round(l["top"], 1), round(l["bottom"], 1)
            if abs(t - b) < 2 and (x1 - x0) > 20:
                hlines.add((t, x0, x1))
            elif abs(x1 - x0) < 2 and (b - t) > 8:
                vlines.add((x0, t, b))
            elif (x1 - x0) > 20 and (b - t) > 8:
                # rect: emit its 4 edges
                hlines.add((t, x0, x1)); hlines.add((b, x0, x1))
                vlines.add((x0, t, b)); vlines.add((x1, t, b))
        print("H-lines (top, x0..x1):")
        for h in sorted(hlines):
            print(f"  y={h[0]}  x {h[1]}..{h[2]}")
        print("V-lines (x, top..bottom):")
        for v in sorted(vlines):
            print(f"  x={v[0]}  y {v[1]}..{v[2]}")
