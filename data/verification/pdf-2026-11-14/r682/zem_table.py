"""Recount Zemishlany 2001 Table I from the pdftotext -layout output. Usage: python3 -I zem_table.py <txt>"""
import sys, re, math
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
rows = {"M": [], "F": []}
cur = None
for ln in lines:
    s = ln.strip()
    if s.startswith("Males"): cur = "M"; continue
    if s.startswith("Females"): cur = "F"; continue
    if s.startswith("Numbers represent"): cur = None
    if cur:
        toks = s.replace("–", "-").split()
        if len(toks) == 8 and toks[0].isdigit():
            rows[cur].append(toks)
def val(t): return None if t == "A" else int(t)
def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z*z/n; c = p + z*z/(2*n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return round(100*(c-h)/d, 1), round(100*(c+h)/d, 1)
names = ["no", "age", "edu", "desire", "erection_lubrication", "orgasm_intensity", "orgasm_delayed", "satisfaction"]
for sex in "MF":
    R = rows[sex]; n = len(R)
    print(sex, "n =", n, "ages", min(int(r[1]) for r in R), "-", max(int(r[1]) for r in R))
    for j in range(3, 8):
        vals = [r[j] for r in R]
        v = [val(x) for x in vals]
        pos = sum(1 for x in v if x is not None and x > 0)
        pos23 = sum(1 for x in v if x is not None and x >= 2)
        neg = sum(1 for x in v if x is not None and x < 0)
        neg23 = sum(1 for x in v if x is not None and x <= -2)
        zero = sum(1 for x in v if x == 0)
        A = sum(1 for x in vals if x == "A")
        print(f"  {names[j]:22s} up {pos:2d} (2-3: {pos23:2d})  down {neg:2d} (2-3: {neg23})  zero {zero:2d}  A {A}  | Wilson up {wilson(pos,n)} down {wilson(neg,n) if neg else ''}")
    # satisfaction among men with weaker erections / anorgasmia
    weak = [r for r in R if val(r[4]) is not None and val(r[4]) < 0]
    print("  satisfaction of those with erection/lubrication down:", [r[7] for r in weak])
    print("  satisfaction of anorgasmic:", [r[7] for r in R if r[6] == "A"])
allr = rows["M"] + rows["F"]
print("All 35: desire up", sum(1 for r in allr if int(r[3]) > 0), "desire 2-3", sum(1 for r in allr if int(r[3]) >= 2),
      "satisfaction 2-3", sum(1 for r in allr if int(r[7]) >= 2), "Wilson", wilson(sum(1 for r in allr if int(r[7]) >= 2), 35),
      "| desire 2-3 Wilson", wilson(34, 35))
print("Men erection up/down Wilson:", wilson(8, 20), "; orgasm delayed men", wilson(16, 20), "women", wilson(6, 15))
