#!/usr/bin/env python3
"""Write blind second-reader task files (METHODS §5.5; docs/VERIFICATION-BRIEF.md).

For each source, the task lists only what reader 2 may see before its blind extraction: the reference (DOI, PMCID, PDF
path, title, year), where the first reader read it, and the claims that cite it with their statement, magnitude, the
number of anchors from this source and their roles. Never the anchors themselves.

Usage: make_blind_tasks.py ROUND [--refs id1,id2,...] [--include-incoming]
  ROUND               folder under data/verification/ (e.g. round2)
  --refs              only these reference ids (default: every source cited by a claim that has an ai-located anchor)
  --include-incoming  also read staged claims in data/claims/_incoming/*.json and references in data/references/_incoming
Cards with no claim yet get a task with an empty claim list: reader 2 then checks the card only.
"""
import json, sys, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
rnd = sys.argv[1]
refs_only = None
for i, a in enumerate(sys.argv):
    if a == "--refs":
        refs_only = set(sys.argv[i + 1].split(","))
incoming = "--include-incoming" in sys.argv

claims = []
for f in sorted(glob.glob(str(ROOT / "data/claims/*.json"))):
    claims += json.load(open(f, encoding="utf-8"))
if incoming:
    for f in sorted(glob.glob(str(ROOT / "data/claims/_incoming/*.json"))):
        claims += json.load(open(f, encoding="utf-8"))
refs = {}
for f in glob.glob(str(ROOT / "data/references/*.json")):
    for r in json.load(open(f, encoding="utf-8")):
        refs[r["id"]] = r
stubs = {}
if incoming:
    for f in glob.glob(str(ROOT / "data/references/_incoming/*.txt")):
        for line in open(f, encoding="utf-8"):
            p = line.strip().split(">")
            if len(p) >= 2 and not line.startswith("#"):
                stubs[p[0]] = {"DOI": p[1], "where": p[2] if len(p) > 2 else ""}
cards = {}
for f in glob.glob(str(ROOT / "data/study-cards/*.json")):
    for c in json.load(open(f, encoding="utf-8")):
        cards[c["reference"]] = c
if incoming:
    for f in glob.glob(str(ROOT / "data/study-cards/_incoming/*/*.json")):
        c = json.load(open(f, encoding="utf-8")); cards[c["reference"]] = c

by_ref = {}
for c in claims:
    if not isinstance(c, dict) or "evidence" not in c:
        continue  # a staged patch or note, not a claim
    for e in c["evidence"]:
        if e["anchor_status"] != "ai-located" and refs_only is None:
            continue
        by_ref.setdefault(e["reference"], {}).setdefault(c["id"], {"claim": c, "n": 0, "roles": set()})
        by_ref[e["reference"]][c["id"]]["n"] += 1
        by_ref[e["reference"]][c["id"]]["roles"].add(e["role"])
targets = refs_only if refs_only is not None else set(by_ref)
out = ROOT / "data" / "verification" / rnd / "tasks"
out.mkdir(parents=True, exist_ok=True)
n = 0
for rid in sorted(targets):
    r = refs.get(rid); s = stubs.get(rid, {}); card = cards.get(rid, {})
    where = (card.get("verification") or {}).get("source_read", "")
    task = {
        "reference": rid,
        "DOI": (r or {}).get("DOI") or s.get("DOI"),
        "PMCID": (r or {}).get("PMCID") or (s.get("where") if s.get("where", "").startswith("PMC") else None),
        "pdf_path": ((r or {}).get("verification") or {}).get("pdf_path"),
        "first_reader_source": where.split(" (")[0] if where else s.get("where", ""),
        "title": (r or {}).get("title"),
        "year": ((r or {}).get("issued") or {}).get("date-parts", [[None]])[0][0],
        "study_card": "sc_" + rid.replace("-", "_"),
        "claims": [{"claim_id": cid, "statement": v["claim"]["statement"], "magnitude": v["claim"].get("magnitude", ""),
                    "n_anchors_from_this_source": v["n"], "roles": sorted(v["roles"])}
                   for cid, v in sorted(by_ref.get(rid, {}).items())],
    }
    (out / f"{rid}.json").write_text(json.dumps(task, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    n += 1
print(f"wrote {n} task files to {out.relative_to(ROOT)}")
