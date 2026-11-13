#!/usr/bin/env python3
"""Read bar heights from a page rendered at 300 dpi (AI reader 652, round pdf-2026-11-13r; Wood et al., 2006, Figure 1).

usage: python3 -I 652_read_bars.py PAGE.png NAME X_TICK Y_TOP Y_BOTTOM VMAX NTICKS X_FROM X_TO HALF_STROKE_PX

- Ticks: dark runs in column X_TICK between Y_TOP and Y_BOTTOM; the darkness-weighted centre of each run is the tick
  position; value = a + b*row is fitted through the ticks (top tick = VMAX, bottom tick = 0).
- Bars: dark runs along the row 6 px above the zero tick, between X_FROM and X_TO.
- For each bar, in the central half of its width, the outer top edge is the top of the continuous dark run rising from
  the zero line (a partly covered edge row counts as a fraction). The value is given at the outer edge and inside the
  outline, i.e. with the edge moved down by half the outline's stroke width (HALF_STROKE_PX).

Commands used for Wood et al. (2006), Figure 1 (p. 692 = PDF page 4; bars outlined with a 0.96-point stroke, so half the
stroke is 0.48 pt = 2.0 px at 300 dpi):
  pdftoppm -r 300 -f 4 -l 4 -png Wood_2006_CanadianHeroinSupplyShortage.pdf w06-300-p
  python3 -I 652_read_bars.py w06-300-p-4.png A 417 320 810 450 10 430 1600 2.0    # deaths, British Columbia
  python3 -I 652_read_bars.py w06-300-p-4.png B 417 980 1460 900 10 430 1600 2.0   # naloxone, Downtown Eastside
  python3 -I 652_read_bars.py w06-300-p-4.png C 417 1630 2125 250 6 430 1600 2.0   # heroin seized, kg
Results inside the outlines: A 399.0, 271.8, 218.0, 220.9, 169.0, 185.7; B 732.0, 840.3, 655.3, 464.3, 387.5, 350.1;
C 233.6, 141.5, 176.5, 93.5, 45.6, 59.6. Cross-check: the bar rectangles drawn in the PDF (pdfplumber page.rects) give
A 399.5, 271.7, 217.8, 220.7, 169.0, 185.9; B 733.3, 841.0, 654.7, 464.9, 388.0, 350.4; C 233.8, 141.8, 177.0, 93.9,
45.9, 59.9. The PDF itself is never modified or copied into the project.
"""
import sys
from PIL import Image

a_ = sys.argv
im = Image.open(a_[1]).convert('L'); px = im.load()
name = a_[2]; xt = int(a_[3]); yt = int(a_[4]); yb = int(a_[5]); vmax = float(a_[6]); nt = int(a_[7])
x0 = int(a_[8]); x1 = int(a_[9]); hs = float(a_[10])
rows = [y for y in range(yt, yb) if px[xt, y] < 200]
g = []
for y in rows:
    if g and y - g[-1][-1] <= 1: g[-1].append(y)
    else: g.append([y])
cent = []
for grp in g:
    ys = list(range(grp[0] - 1, grp[-1] + 2))
    w = [255 - px[xt, y] for y in ys]
    cent.append(sum(y * wi for y, wi in zip(ys, w)) / sum(w))
assert len(cent) == nt, (name, len(cent), cent)
vals = [vmax - i * vmax / (nt - 1) for i in range(nt)]
n = len(cent); mx = sum(cent) / n; my = sum(vals) / n
b = sum((c - mx) * (v - my) for c, v in zip(cent, vals)) / sum((c - mx) ** 2 for c in cent); a = my - b * mx
res = max(abs(v - (a + b * c)) for c, v in zip(cent, vals))
print('%s: ticks %s; %.3f units per px; max tick residual %.2f' % (name, [round(c, 1) for c in cent], -b, res))
yz = int(round(cent[-1])) - 6
runs = []; s = None
for x in range(x0, x1):
    d = px[x, yz] < 128
    if d and s is None: s = x
    if not d and s is not None: runs.append((s, x - 1)); s = None
runs = [r for r in runs if r[1] - r[0] > 20]
for (s, e) in runs:
    cols = range(s + (e - s) // 4, e - (e - s) // 4 + 1)
    tops = []
    for x in cols:
        y = yz
        while px[x, y - 1] < 128: y -= 1
        cov = (255 - px[x, y - 1]) / (255 - 32)
        tops.append(y - max(0.0, min(cov, 1.0)))
    t = sum(tops) / len(tops)
    print('  bar x %d-%d: outer top %.2f px -> %.1f; inside outline (+%.1f px) -> %.1f' % (s, e, t, a + b * t, hs, a + b * (t + hs)))
