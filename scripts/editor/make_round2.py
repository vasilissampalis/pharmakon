"""make_round2.py DIR READER CLAIM1,CLAIM2 [--cards c1,c2]: round-2 tasks for every anchor of the named claims (merged, or
still staged in data/claims/_incoming/) that no second reader has checked yet, plus the named first-pass cards. Writes data/verification/DIR/round2/tasks_reader<N>.json."""
import json, sys, glob, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
d, reader, cids = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
cards = sys.argv[sys.argv.index("--cards") + 1].split(",") if "--cards" in sys.argv else []
where = {}
# the main claim files first (they win), then new claims still staged in _incoming/ (not the patch files): staged claims
# can be checked before they are merged, since merge_claims.py needs their study cards merged first
for f in sorted(glob.glob("data/claims/*.json")) + sorted(x for x in glob.glob("data/claims/_incoming/*.json") if not os.path.basename(x).startswith("patch_")):
    for c in json.load(open(f, encoding="utf-8")): where.setdefault(c["id"], (f, c))
refs = {}
for f in glob.glob("data/references/*.json"):
    for r in json.load(open(f, encoding="utf-8")): refs[r["id"]] = r
pdfp = lambda ref: refs.get(ref, {}).get("verification", {}).get("pdf_path")
A = []
for cid in cids:
    f, c = where[cid]
    for i, e in enumerate(c["evidence"]):
        if e["anchor_status"] in ("ai-checked", "senior-verified"): continue
        A.append({"n": len(A) + 1, "claim_id": cid, "claim_file": f, "anchor_index": i, "reference": e["reference"], "page": e.get("page", ""),
                  "locator": e.get("locator", ""), "source_read": e.get("source_read", ""), "extracted": e["extracted"], "role": e.get("role", ""),
                  "current_status": e["anchor_status"], "located_by": e.get("located_by", ""), "what_changed": "new or reworded anchor", "pdf_path": pdfp(e["reference"])})
C = []
for k in cards:
    fp = glob.glob(f"data/study-cards/_incoming/*/{k}.json")[0]; card = json.load(open(fp, encoding="utf-8"))
    C.append({"card": k, "file": fp, "pdf_path": pdfp(card["reference"])})
out = f"data/verification/{d}/round2/tasks_reader{reader}.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump({"anchors": A, "cards": C}, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(reader, len(A), "anchors", sorted({a["reference"] for a in A}), "| cards", cards, "| missing pdf:", [a["reference"] for a in A if not a["pdf_path"]] + [c["card"] for c in C if not c["pdf_path"]])
