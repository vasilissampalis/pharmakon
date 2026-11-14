import json, re, sys
claims = json.load(open(sys.argv[1], encoding="utf-8"))
refs = []
import glob
for f in glob.glob("data/references/*.json"): refs += json.load(open(f))
ref_ids = {r["id"] for r in refs}
lv = ["very-low", "low", "moderate", "high"]
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"|(?<![A-Za-z])'[^']{12,}?'(?![A-Za-z])")
for c in claims:
    g = c["grade"]; d = g["domains"]
    down = sum(d[k]["levels"] for k in ("risk_of_bias","inconsistency","indirectness","imprecision","publication_bias"))
    up = sum(d.get(k, {"levels":0})["levels"] for k in ("large_effect","dose_response","plausible_confounding"))
    exp = lv[max(0, min(3, (3 if g["starting_level"]=="high" else 1) - down + up))]
    print(c["id"], "grade", g["certainty"], "expected", exp, "OK" if exp==g["certainty"] else "FAIL")
    for e in c["evidence"]:
        if e["reference"] not in ref_ids: print("  unknown ref", e["reference"])
    fields = [c.get(k) or "" for k in ("statement","plain","magnitude","population","exposure","comparator","outcome")] + [g["reasoning"]] + [e["extracted"] for e in c["evidence"]]
    for t in fields:
        tl = t.lower()
        for term in ("addict","abuser","junkie","clean urine","dirty urine","harmless","devastating"):
            if term in tl: print("  WARN term", term)
        if re.search(r"\bcl_[a-z]+_\w+", t): print("  WARN raw id")
        if re.search(r"\b(non-)?users?\b", QUOTED.sub(" ", tl)): print("  WARN users:", re.findall(r".{30}\busers?\b.{20}", tl)[:2])
        if re.search(r"\babuse\b", QUOTED.sub(" ", tl)): print("  NOTE abuse:", re.findall(r".{40}\babuse\b.{20}", tl)[:3])
    if c["verification"]["status"] != "draft": print("  not draft")
    print("  words statement", len(c["statement"].split()), "plain", len(c["plain"].split()), "anchors", len(c["evidence"]))
    print("  ends:", c["statement"][-80:])
