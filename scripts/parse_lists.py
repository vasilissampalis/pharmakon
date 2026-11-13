#!/usr/bin/env python3
"""Header-driven parser for search-logs/*_DOI-LIST.md.

Each list is a set of markdown tables whose header names the columns; column
order differs between co-editors, so columns are located by header name, not
position. Returns, per folder, the rows of each tier with: n, paper, venue,
doi, save_as, verif (whatever verification marker the list carries, if any).
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOGS = ROOT / "search-logs"
DOI_RE = re.compile(r"10\.\d{4,9}/\S+")

def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def _header_map(cells):
    m = {}
    for i, c in enumerate(cells):
        k = c.lower().strip()
        if k in ("#", "no", "n"): m["n"] = i
        elif k.startswith("paper") or k.startswith("title") or k.startswith("report"): m["paper"] = i
        elif k.startswith("journal") or k.startswith("venue") or k.startswith("source"): m["venue"] = i
        elif k == "doi" or k.startswith("doi"): m["doi"] = i
        elif k.startswith("save as") or k.startswith("filename") or k.startswith("save"): m["save_as"] = i
        elif k in ("v", "verif.", "verif", "verification", "status"): m["verif"] = i
    return m

def parse(path):
    tier, hdr = None, None
    out = {"A": [], "B": [], "C": [], "reports": []}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("## "):
            low = s.lower()
            if "tier a" in low: tier = "A"
            elif "tier b" in low: tier = "B"
            elif "tier c" in low: tier = "C"
            elif "report" in low: tier = "reports"
            else: tier = None
            hdr = None
            continue
        if s.startswith("### "):  # topic lists put the tiers one level down ('## 1. Alcohol', then '### Tier A'); other subheadings keep the tier
            low = s.lower()
            if "tier a" in low: tier = "A"
            elif "tier b" in low: tier = "B"
            elif "tier c" in low: tier = "C"
            hdr = None
            continue
        if not s.startswith("|"): continue
        cells = _cells(s)
        if set("".join(cells)) <= set("-: "): continue          # separator row
        if hdr is None or (len(cells) != len(hdr_cells if hdr else []) ):
            maybe = _header_map(cells)
            if "doi" in maybe or ("paper" in maybe and "save_as" in maybe):
                hdr, hdr_cells = maybe, cells
                continue
        if hdr is None or tier is None: continue
        get = lambda k: cells[hdr[k]] if k in hdr and hdr[k] < len(cells) else ""
        doi_cell = get("doi")
        m = DOI_RE.search(doi_cell) or (DOI_RE.search(s) if "doi" not in hdr else None)
        row = {"n": get("n"), "paper": get("paper"), "venue": get("venue"),
               "doi": m.group(0).rstrip(".,;)") if m else "", "save_as": get("save_as"), "verif": get("verif")}
        if row["paper"] and (row["doi"] or tier == "reports"):
            out[tier].append(row)
    return out

def all_lists():
    res = {}
    for f in sorted(LOGS.glob("*_DOI-LIST.md")):
        folder = f.name[: -len("_DOI-LIST.md")]
        if folder == "methamphetamine": folder = "Methamphetamine"
        res[folder] = parse(f)
    return res

if __name__ == "__main__":
    import json, sys
    d = all_lists()
    summary = {k: {t: len(v) for t, v in tiers.items()} for k, tiers in d.items()}
    print(json.dumps(summary, indent=1))
    dois = [r["doi"] for tiers in d.values() for t, rows in tiers.items() if t != "reports" for r in rows if r["doi"]]
    print("total rows with DOI:", len(dois), "| distinct:", len(set(dois)))
    if "--dump" in sys.argv:
        (ROOT / "data" / "doi-index.json").write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
        print("wrote data/doi-index.json")
