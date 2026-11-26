"""split_round2.py DIR FIRST N --claims GLOB --patches GLOB --cards-by READERS [--dry]: round-2 tasks for a whole round, split by source.

(26 November 2026, round pdf-2026-11-26.) make_round2.py writes one reader's tasks from the claims and cards the editor names; this
one takes every anchor of a round that no second reader has checked yet (the new claims matched by --claims, still staged in
data/claims/_incoming/, and the new anchors of the revision patches matched by --patches, at the index each will take when its
patch is applied) and every first-pass card written by the first readers named in --cards-by (a range such as 731-745), groups
them by SOURCE, so that a reader opens each PDF once and checks its anchors before its card, and shares the sources among N
readers numbered from FIRST, the heaviest first (an anchor weighs 1, a card 5). Writes data/verification/DIR/round2/
tasks_reader<N>.json in make_round2.py's form ({"anchors": [...], "cards": [...]}), so that adj_r2.py and apply_r2.sh read them.
"""
import glob, json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
d, first, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); dry = "--dry" in sys.argv
arg = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else ""
lo, hi = (int(x) for x in arg("--cards-by").split("-"))
refs = {}
for f in glob.glob("data/references/*.json"):
    for r in json.load(open(f, encoding="utf-8")): refs[r["id"]] = r
pdfp = lambda ref: refs.get(ref, {}).get("verification", {}).get("pdf_path")
where = {}
for f in sorted(glob.glob("data/claims/*.json")) + sorted(x for x in glob.glob("data/claims/_incoming/*.json") if not os.path.basename(x).startswith("patch_")):
    for c in json.load(open(f, encoding="utf-8")): where.setdefault(c["id"], (f, c))
A = []
for f in sorted(glob.glob(arg("--claims"))):
    for c in json.load(open(f, encoding="utf-8")):
        for i, e in enumerate(c["evidence"]):
            if e["anchor_status"] in ("ai-checked", "senior-verified"): continue
            A.append({"claim_id": c["id"], "claim_file": f, "anchor_index": i, "reference": e["reference"], "page": e.get("page", ""), "locator": e.get("locator", ""),
                      "source_read": e.get("source_read", ""), "extracted": e["extracted"], "role": e.get("role", ""), "current_status": e["anchor_status"],
                      "located_by": e.get("located_by", ""), "what_changed": "new anchor", "pdf_path": pdfp(e["reference"])})
for pf in sorted(glob.glob(arg("--patches"))):
    for p in json.load(open(pf, encoding="utf-8")):
        f, c = where[p["claim"]]; base = len(c["evidence"])
        assert not p.get("evidence_set"), "a patch changes existing anchors: check them separately"
        for k, e in enumerate(p.get("evidence_add", [])):
            A.append({"claim_id": p["claim"], "claim_file": f, "anchor_index": base + k, "reference": e["reference"], "page": e.get("page", ""), "locator": e.get("locator", ""),
                      "source_read": e.get("source_read", ""), "extracted": e["extracted"], "role": e.get("role", ""), "current_status": e.get("anchor_status", "ai-located"),
                      "located_by": e.get("located_by", ""), "what_changed": "new anchor in revision patch " + os.path.basename(pf), "pdf_path": pdfp(e["reference"])})
C = []
for fp in sorted(glob.glob("data/study-cards/_incoming/*/sc_*.json")):
    c = json.load(open(fp, encoding="utf-8")); v = c.get("verification") or {}
    m = re.search(r"agent (\d+)", str(v.get("extracted_by") or v.get("first_pass_by") or ""))
    if v.get("status") == "first-pass" and m and lo <= int(m.group(1)) <= hi:
        C.append({"card": c["id"], "file": fp, "reference": c.get("reference"), "pdf_path": pdfp(c.get("reference"))})
by = {}
for a in A: by.setdefault(a["reference"], {"anchors": [], "cards": []})["anchors"].append(a)
for c in C: by.setdefault(c["reference"], {"anchors": [], "cards": []})["cards"].append(c)
weight = lambda g: len(g["anchors"]) + 5 * len(g["cards"])
bins = [{"anchors": [], "cards": [], "w": 0} for _ in range(n)]
for ref, g in sorted(by.items(), key=lambda kv: -weight(kv[1])):
    b = min(bins, key=lambda x: x["w"]); b["anchors"] += g["anchors"]; b["cards"] += g["cards"]; b["w"] += weight(g)
out = ROOT / "data" / "verification" / d / "round2"; out.mkdir(parents=True, exist_ok=True)
for k, b in enumerate(bins):
    for i, a in enumerate(b["anchors"]): a["n"] = i + 1
    t = {"anchors": [{"n": a["n"], **{x: a[x] for x in a if x != "n"}} for a in b["anchors"]], "cards": [{x: c[x] for x in ("card", "file", "pdf_path")} for c in b["cards"]]}
    nm = out / f"tasks_reader{first + k}.json"
    print(nm.name, "anchors", len(t["anchors"]), "cards", len(t["cards"]), "sources", len({a["reference"] for a in b["anchors"]} | {c["reference"] for c in b["cards"]}),
          "no PDF:", sorted({a["reference"] for a in b["anchors"] if not a["pdf_path"]}))
    if not dry: json.dump(t, open(nm, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("anchors", len(A), "cards", len(C), "sources", len(by))
