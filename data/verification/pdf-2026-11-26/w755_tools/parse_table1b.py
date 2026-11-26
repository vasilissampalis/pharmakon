"""Parse Brunetti 2021 Table 1 (pp. 5-34): one row per band between rules in the Concentration column.
Usage: python3 -I parse_table1b.py <pdf> <out.json>
"""
import sys, json
from collections import Counter
import pdfplumber

pdf = pdfplumber.open(sys.argv[1])
HEADERS = ['Compound', 'Study', 'Age', 'Observations', 'Concentration', 'Co-Exposure', 'Ref.']

def chunks_of(page):
    words = page.extract_words(x_tolerance=1.5, y_tolerance=2)
    words = sorted(words, key=lambda w: (round(w['top'], 0), w['x0']))
    lines = []
    for w in words:
        for ln in lines:
            if abs(ln['top'] - w['top']) < 1.2:
                ln['words'].append(w); break
        else:
            lines.append({'top': w['top'], 'words': [w]})
    out = []
    for ln in lines:
        ws = sorted(ln['words'], key=lambda w: w['x0'])
        cur = [ws[0]]
        groups = []
        for w in ws[1:]:
            if w['x0'] - cur[-1]['x1'] < 7:
                cur.append(w)
            else:
                groups.append(cur); cur = [w]
        groups.append(cur)
        for c in groups:
            out.append({'text': ' '.join(w['text'] for w in c), 'x0': c[0]['x0'], 'x1': c[-1]['x1'],
                        'top': min(w['top'] for w in c), 'bottom': max(w['bottom'] for w in c)})
    return out

def hrules(page):
    hs = []
    for l in page.lines:
        if abs(l['top'] - l['bottom']) < 1:
            hs.append((l['top'], l['x0'], l['x1']))
    for r in page.rects:
        if r['height'] < 2:
            hs.append((r['top'], r['x0'], r['x1']))
    return hs

rows = []
carry = {'Compound': None, 'Study': None, 'Observations': None, 'Ref.': None}
for pn in range(5, 35):
    page = pdf.pages[pn - 1]
    ch = chunks_of(page)
    head = {}
    for c in ch:
        for h in HEADERS:
            if c['text'].startswith(h) and h not in head and c['top'] < 140:
                head[h] = c
    assert len(head) == 7, (pn, list(head))
    centers = {h: (head[h]['x0'] + head[h]['x1']) / 2 for h in head}
    header_bottom = max(head[h]['bottom'] for h in head) + 1
    hs = hrules(page)
    full = sorted([h for h in hs if h[2] - h[1] > 600], key=lambda h: h[0])
    table_bottom = full[-1][0]
    body = [c for c in ch if header_bottom < c['top'] < table_bottom - 1]
    for c in body:
        cx = (c['x0'] + c['x1']) / 2
        c['col'] = min(centers, key=lambda h: abs(centers[h] - cx))
        c['cy'] = (c['top'] + c['bottom']) / 2
    def bands(col):
        x = centers[col]
        ys = sorted(set(round(h[0], 1) for h in hs if h[1] - 1 <= x <= h[2] + 1 and header_bottom < h[0] < table_bottom - 0.5))
        b = [header_bottom] + ys + [table_bottom]
        return [(b[i], b[i + 1]) for i in range(len(b) - 1) if b[i + 1] - b[i] > 2]
    B = {col: bands(col) for col in centers}
    def band_at(col, y):
        for b in B[col]:
            if b[0] <= y < b[1]:
                return b
        return None
    for (y0, y1) in B['Concentration']:
        conc = sorted([c for c in body if c['col'] == 'Concentration' and y0 <= c['cy'] < y1], key=lambda c: c['top'])
        if not conc:
            continue
        cy = (y0 + y1) / 2
        rec = {'page': pn, 'y0': round(y0, 1), 'y1': round(y1, 1)}
        rec['Concentration'] = [c['text'] for c in conc]
        rec['Co-Exposure'] = [c['text'] for c in sorted([c for c in body if c['col'] == 'Co-Exposure' and y0 <= c['cy'] < y1], key=lambda c: (c['top'], c['x0']))]
        rec['Age'] = ' '.join(c['text'] for c in sorted([c for c in body if c['col'] == 'Age' and y0 <= c['cy'] < y1], key=lambda c: (c['top'], c['x0'])))
        for col in ['Compound', 'Study', 'Observations', 'Ref.']:
            b = band_at(col, cy)
            inb = [c for c in body if c['col'] == col and b and b[0] <= c['cy'] < b[1]]
            if inb:
                txt = ' '.join(c['text'] for c in sorted(inb, key=lambda c: (c['top'], c['x0'])))
                rec[col] = txt
                carry[col] = txt
            else:
                rec[col] = carry[col]
                rec[col + '_inh'] = True
        rows.append(rec)

json.dump(rows, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(len(rows), Counter(r['Study'] for r in rows))
print(Counter((r['Compound'], r['Study']) for r in rows))
