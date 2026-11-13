"""install_lines.py DIR N [--dry]: install a writer's plain lines (data/verification/DIR/<N>_simple.json) for claims whose
anchors are all checked. Claim entries replace the claim's entry in data/site/simple.json with v = the claim's current
version; true-or-false and quiz items are held in data/verification/quiz/pending.json for the blind check (they go on the
site only after it, through apply_check.py)."""
import json, sys, glob, pathlib, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sj
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
d, n = sys.argv[1], sys.argv[2]; dry = "--dry" in sys.argv
W = json.load(open(f"data/verification/{d}/{n}_simple.json", encoding="utf-8"))
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = sj.load()
PP = pathlib.Path("data/verification/quiz/pending.json")
P = json.load(open(PP, encoding="utf-8")) if PP.exists() else {"_note": "Quiz and true-or-false items written but not yet blind-checked; apply_check.py moves checked items onto the site.", "tf": [], "quiz": []}
ok = set()
for cid, e in (W.get("claims") or {}).items():
    c = C.get(cid)
    if not c: print("!! unknown claim", cid); continue
    waiting = [i for i, a in enumerate(c["evidence"]) if a["anchor_status"] not in ("ai-checked", "senior-verified")]
    if waiting: print("!! held:", cid, "anchors still waiting:", waiting); continue
    e = dict(e); e["v"] = c["version"]
    S["claims"][cid] = e; ok.add(cid); print("installed lines:", cid, "v" + c["version"])
for kind in ("tf", "quiz"):
    for page, items in (W.get(kind) or {}).items():
        for it in items:
            if it["claim"] not in ok: continue
            it = dict(it); it["v"] = C[it["claim"]]["version"]
            key = it.get("statement", it.get("q"))
            P[kind] = [x for x in P[kind] if (x["claim"], x["item"].get("statement", x["item"].get("q"))) != (it["claim"], key)]
            P[kind].append({"claim": it["claim"], "page": page, "item": it}); print("held for blind check:", kind, page, it["claim"])
if not dry:
    sj.save(S); PP.parent.mkdir(parents=True, exist_ok=True)
    with open(PP, "w", encoding="utf-8") as f: json.dump(P, f, ensure_ascii=False, indent=1); f.write("\n")
