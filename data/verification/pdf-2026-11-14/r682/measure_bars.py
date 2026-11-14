"""Measure bar heights in Hysek 2014 Figures 2 and 3 (300-dpi page render, p. 1648).

Usage: python3 -I measure_bars.py <page_png>
Finds, for each panel, the y axis line, its tick marks, and the top edge of each bar,
then converts the bar tops to axis units by linear interpolation between ticks.
"""
import sys
from PIL import Image

img = Image.open(sys.argv[1]).convert("L")
W, H = img.size
px = img.load()

DARK = 110


def dark(x, y):
    return px[x, y] < DARK


def find_axis_line(x0, x1, y0, y1):
    """Return x of the longest vertical dark run within the window."""
    best = (0, None)
    for x in range(x0, x1):
        run = longest = 0
        for y in range(y0, y1):
            if dark(x, y):
                run += 1
                longest = max(longest, run)
            else:
                run = 0
        if longest > best[0]:
            best = (longest, x)
    return best[1]


def find_ticks(ax, y0, y1):
    """Ticks: rows where pixels just left of the axis line are dark."""
    rows = []
    for y in range(y0, y1):
        if all(dark(ax - d, y) for d in range(3, 12)):
            rows.append(y)
    # group consecutive rows
    groups = []
    for y in rows:
        if groups and y - groups[-1][-1] <= 1:
            groups[-1].append(y)
        else:
            groups.append([y])
    return [sum(g) / len(g) for g in groups]


def bar_top(x, y0, y1):
    """Scan down column x from y0; return first dark row that starts a run of >= 2 dark pixels
    followed by light interior (bar outline)."""
    for y in range(y0, y1):
        if dark(x, y) and dark(x, y + 1):
            return y + 0.5
        if dark(x, y):
            return float(y)
    return None


def bars_in_row(ax, y_probe, x_end):
    """Find bar left/right edges along a row just above the x axis: vertical outlines."""
    edges = []
    x = ax + 5
    while x < x_end:
        if dark(x, y_probe):
            start = x
            while x < x_end and dark(x, y_probe):
                x += 1
            edges.append((start, x - 1))
        x += 1
    return edges


panels = {
    # name: (window for axis search x0,x1,y0,y1 in page px, tick values from top to bottom)
    "Fig2A explicit emotional empathy": (420, 480, 250, 760, [8, 7, 6, 5, 4, 3, 2, 1, 0]),
    "Fig2B implicit emotional empathy": (1060, 1120, 250, 760, [8, 7, 6, 5, 4, 3, 2, 1, 0]),
    "Fig2C cognitive empathy": (1730, 1800, 250, 760, [100, 75, 50, 25, 0]),
    "Fig3A SVO angle": (640, 700, 960, 1500, [50, 40, 30, 20, 10, 0]),
    "Fig3B inequality-aversion index": (1350, 1410, 960, 1500, [0.75, 0.60, 0.45, 0.30, 0.15, 0.00]),
}

for name, (x0, x1, y0, y1, vals) in panels.items():
    ax = find_axis_line(x0, x1, y0, y1)
    ticks = find_ticks(ax, y0, y1)
    if len(ticks) != len(vals):
        print(name, "axis x", ax, "ticks found", [round(t, 1) for t in ticks], "expected", len(vals))
        continue
    top, bottom = ticks[0], ticks[-1]
    vtop, vbot = vals[0], vals[-1]

    def to_val(y):
        return vbot + (bottom - y) * (vtop - vbot) / (bottom - top)

    y_probe = int(bottom) - 6
    edges = bars_in_row(ax, y_probe, ax + 700)
    # pair edges into bars: outline left edge, outline right edge
    bars = []
    i = 0
    while i + 1 < len(edges):
        l, r = edges[i][0], edges[i + 1][1]
        if 25 < r - l < 80:
            bars.append((l, r))
            i += 2
        else:
            i += 1
    out = []
    for (l, r) in bars[:6]:
        xs = l + 4  # just inside the left outline, away from the central error bar
        t = bar_top(xs, int(top) - 5, int(bottom))
        out.append(round(to_val(t), 3) if t is not None else None)
    print(name, "| axis x", ax, "| ticks", [round(t, 1) for t in ticks], "| bars (placebo, MDMA) all, women, men:", out)
