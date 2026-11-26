"""Applies the validator's claim rules (scripts/validate.py) to one staged claim file."""
import json, re, glob, sys, pathlib

ROOT = pathlib.Path(sys.argv[1])
claims = json.load(open(sys.argv[2], encoding="utf-8"))
refs = []
for f in glob.glob(str(ROOT / "data/references/*.json")):
    refs += json.load(open(f, encoding="utf-8"))
ref_ids = {r["id"] for r in refs}
cards = {}
for f in glob.glob(str(ROOT / "data/study-cards/*.json")):
    for c in json.load(open(f, encoding="utf-8")):
        cards[c["id"]] = c
for f in glob.glob(str(ROOT / "data/study-cards/_incoming/*/*.json")):
    c = json.load(open(f, encoding="utf-8"))
    cards[c["id"]] = c
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"|(?<![A-Za-z])'[^']{12,}?'(?![A-Za-z])")
problems = 0
for c in claims:
    for e in c["evidence"]:
        if e["reference"] not in ref_ids:
            print("unknown reference", e["reference"]); problems += 1
        if e["study_card"] not in cards:
            print("unknown card", e["study_card"]); problems += 1
        elif cards[e["study_card"]]["reference"] != e["reference"]:
            print("card/reference mismatch", e["study_card"], e["reference"]); problems += 1
        q = e.get("quote")
        if q and len(q.split()) > 15:
            print("quote too long"); problems += 1
    nq = sum(1 for e in c["evidence"] if e.get("quote"))
    print("quotes:", nq)
    g = c["grade"]; d = g["domains"]
    lv = ["very-low", "low", "moderate", "high"]
    down = sum(d[k]["levels"] for k in ("risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"))
    up = sum(d.get(k, {"levels": 0})["levels"] for k in ("large_effect", "dose_response", "plausible_confounding"))
    expect = lv[max(0, min(3, (3 if g["starting_level"] == "high" else 1) - down + up))]
    print("GRADE:", g["starting_level"], "-", down, "+", up, "=>", expect, "| stated", g["certainty"])
    if expect != g["certainty"]:
        problems += 1
    fields = [(f, c.get(f) or "") for f in ("statement", "plain", "magnitude", "population", "exposure", "comparator", "outcome")]
    fields += [("grade.reasoning", g.get("reasoning") or "")] + [(f"evidence[{i}].extracted", e.get("extracted") or "") for i, e in enumerate(c["evidence"])]
    for fld, raw in fields:
        txt = raw.lower()
        for term in ("addict", "abuser", "junkie", "clean urine", "dirty urine", "harmless", "devastating"):
            if term in txt:
                print("WARN term", term, "in", fld); problems += 1
        if re.search(r"\bcl_[a-z]+_\w+", raw):
            print("WARN raw claim id in", fld); problems += 1
        if re.search(r"\b(non-)?users?\b", QUOTED.sub(" ", txt)):
            print("WARN users in", fld); problems += 1
    # quotation marks in the statement: count double-quoted spans (labels in single quotes are labels)
    print("double-quoted spans in statement:", re.findall(r"\"[^\"]*\"", c["statement"]))
    print("statement words:", len(c["statement"].split()), "| plain words:", len(c["plain"].split()))
    sup = [e for e in c["evidence"] if e["role"] == "supports"]
    print("supporting anchors:", len(sup), "designs:", sorted({cards[e['study_card']].get('design') for e in sup}))
print("problems:", problems)
