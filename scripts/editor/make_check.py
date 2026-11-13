"""make_check.py N DIR RATE_IDS LINE_IDS [QUIZ_CLAIMS]: one blind-check task set for checker N.
RATE_IDS, LINE_IDS: comma-separated claim ids (may be empty). Quiz items: those held in data/verification/quiz/pending.json
(only those of QUIZ_CLAIMS when given). Writes data/verification/DIR/tasks_check<N>.json and tasks_check<N>_key.json."""
import json, glob, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
n, d = sys.argv[1], sys.argv[2]
rate_ids = [x for x in sys.argv[3].split(",") if x]; line_ids = [x for x in sys.argv[4].split(",") if x]
quiz_only = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
D = pathlib.Path(f"data/verification/{d}"); D.mkdir(parents=True, exist_ok=True)
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = json.load(open("data/site/simple.json", encoding="utf-8"))
study = lambda c: {k: c.get(k) for k in ("population", "exposure", "comparator", "outcome", "magnitude")}
rate = []
for k in rate_ids:
    c = C[k]; g = c["grade"]
    rate.append({"id": k, "certainty": g["certainty"], "starting_level": g.get("starting_level"), "domains": g.get("domains"), "reasoning": g.get("reasoning"),
                 **study(c), "short": S["claims"][k]["short"], "rate": S["claims"][k].get("rate")})
P = json.load(open("data/verification/quiz/pending.json", encoding="utf-8"))
quiz = []
for kind in ("tf", "quiz"):
    for x in P[kind]:
        if quiz_only and x["claim"] not in quiz_only: continue
        cid = x["claim"]; it = dict(x["item"]); it["v"] = S["claims"][cid]["v"]
        quiz.append({"n": len(quiz) + 1, "page": x["page"], "kind": kind, "item": it, "lines": {f: S["claims"][cid].get(f) for f in ("short", "but", "how", "v")}})
lines = []
for k in line_ids:
    c = C[k]; e = S["claims"][k]
    lines.append({"id": k, "statement": c["statement"], **study(c), "certainty": c["grade"]["certainty"], "reasoning": c["grade"].get("reasoning"),
                  "lines": {f: e.get(f) for f in ("q", "short", "but", "how")}})
json.dump({"rate": rate, "quiz": quiz, "lines": lines}, open(D / f"tasks_check{n}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"quiz_key": [{"n": q["n"], "claim": q["item"]["claim"], "kind": q["kind"], "page": q["page"]} for q in quiz]}, open(D / f"tasks_check{n}_key.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(n, "rate", len(rate), "quiz", len(quiz), "lines", len(lines))
