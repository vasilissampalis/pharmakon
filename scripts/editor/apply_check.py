"""apply_check.py N DIR [--dry]: apply blind check N (data/verification/DIR/check_out<N>.json) to data/site/simple.json.
rate: fix puts in the checker's text, reject removes the line. quiz: ok and fix go on the site (fix with the checker's
item); reject or weak stays off; every checked item leaves data/verification/quiz/pending.json. lines: fix replaces each
named field."""
import json, sys, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sj
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
n, d = sys.argv[1], sys.argv[2]; dry = "--dry" in sys.argv
D = pathlib.Path(f"data/verification/{d}")
o = json.load(open(D / f"check_out{n}.json", encoding="utf-8")); t = json.load(open(D / f"tasks_check{n}.json", encoding="utf-8"))
S = sj.load(); cnt = {"rate": {}, "quiz": {}, "lines": {}}
for r in o.get("rate", []):
    v = r["verdict"]; cnt["rate"][v] = cnt["rate"].get(v, 0) + 1
    if v == "fix": S["claims"][r["id"]]["rate"] = r["text"]
    elif v == "reject": S["claims"][r["id"]].pop("rate", None); print("rate line removed:", r["id"], "|", r.get("reason", ""))
Q = {q["n"]: q for q in t["quiz"]}
PP = pathlib.Path("data/verification/quiz/pending.json"); P = json.load(open(PP, encoding="utf-8"))
for r in o.get("quiz", []):
    q = Q[r["n"]]; v = r["verdict"] + ("+weak" if r.get("weak") else ""); cnt["quiz"][v] = cnt["quiz"].get(v, 0) + 1
    key = (q["item"]["claim"], q["item"].get("statement", q["item"].get("q")))
    P[q["kind"]] = [y for y in P[q["kind"]] if (y["claim"], y["item"].get("statement", y["item"].get("q"))) != key]
    if r["verdict"] == "reject" or r.get("weak"): print("quiz left off:", r["n"], key[0], "|", r.get("reason", "")); continue
    item = dict(r["item"]) if r["verdict"] == "fix" and r.get("item") else dict(q["item"])
    item["claim"] = q["item"]["claim"]; item["v"] = q["item"]["v"]
    S[q["kind"]].setdefault(q["page"], []).append(item)
for r in o.get("lines", []):
    v = r["verdict"]; cnt["lines"][v] = cnt["lines"].get(v, 0) + 1
    if v == "fix":
        for f, val in (r.get("fields") or {}).items(): S["claims"][r["id"]][f] = val
print(cnt); print("pending left:", len(P["tf"]), "tf,", len(P["quiz"]), "quiz")
if not dry:
    sj.save(S)
    with open(PP, "w", encoding="utf-8") as f: json.dump(P, f, ensure_ascii=False, indent=1); f.write("\n")
