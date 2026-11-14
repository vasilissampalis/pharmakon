"""make_mf_tasks.py DIR FIRST_WRITER N_WRITERS MIN_DEMAND: tasks for the myth-or-fact pass (14 November 2026; the senior
author: users should find it interesting "as if a super educated joe rogan answered their reddit questions", and "we should
not discard everything if people in forums would find it useful").

Two kinds of task, dealt out in turn so each writer gets a mix:
- "convert": every Quick question on file that the site would ask (its answer published, written for the answer's current
  version). The writer keeps it as one myth-or-fact statement if a person on a drug forum would find it useful or
  surprising, or drops it with a reason.
- "new": every answer with a demand score of MIN_DEMAND or more that has no myth-or-fact statement and no Quick question:
  one statement, if the answer holds a fact worth repeating.
Each task carries the answer's plain lines (the only source an item may use), its question headings, the statements it
already has, and its demand score. Writes data/verification/DIR/tasks_mf<k>.json."""
import json, glob, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
d, first, nw, mind = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
D = pathlib.Path(f"data/verification/{d}"); D.mkdir(parents=True, exist_ok=True)
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = json.load(open("data/site/simple.json", encoding="utf-8"))
Q = json.load(open("data/site/questions.json", encoding="utf-8"))
DM = json.load(open("data/site/demand.json", encoding="utf-8"))["claims"]
score = lambda k: (DM[k]["score"] if isinstance(DM.get(k), dict) else DM.get(k)) or 0
heads, pages = {}, {}
for slug, gs in Q.items():
    if slug == "_note": continue
    for g in gs:
        for cid, q in g["items"]: heads.setdefault(cid, []).append(q); pages.setdefault(cid, []).append(slug)
live = lambda x: x.get("claim") in C and x.get("claim") in S["claims"] and x.get("v") == C[x["claim"]]["version"]
tf_of = {}
for slug, items in (S.get("tf") or {}).items():
    for x in items:
        if live(x): tf_of.setdefault(x["claim"], []).append(x["statement"])
lines = lambda k: {f: S["claims"][k][f] for f in ("short", "but", "how") if f in S["claims"][k]}
tasks, mc_claims = [], set()
for slug, items in (S.get("quiz") or {}).items():
    for x in items:
        if not live(x): continue
        k = x["claim"]; mc_claims.add(k)
        tasks.append({"kind": "convert", "claim": k, "page": slug, "demand": score(k), "questions": sorted(set(heads.get(k, [])))[:3],
                      "lines": lines(k), "has_statements": tf_of.get(k, []),
                      "quick_question": {f: x[f] for f in ("q", "options", "answer", "why") if f in x}})
for k in sorted(S["claims"], key=lambda k: (-score(k), k)):
    if k not in C or score(k) < mind or k in tf_of or k in mc_claims or C[k].get("section") == 7: continue
    if S["claims"][k].get("v") != C[k]["version"]: continue
    tasks.append({"kind": "new", "claim": k, "page": (pages.get(k) or [C[k]["substance"]])[0], "demand": score(k),
                  "questions": sorted(set(heads.get(k, [])))[:3], "lines": lines(k), "has_statements": []})
tasks.sort(key=lambda t: (-t["demand"], t["claim"]))
out = {k: [] for k in range(first, first + nw)}
for i, t in enumerate(tasks): out[first + i % nw].append(t)
for k, t in out.items():
    with open(D / f"tasks_mf{k}.json", "w", encoding="utf-8") as f: json.dump({"writer": k, "tasks": t}, f, ensure_ascii=False, indent=1); f.write("\n")
print(len(tasks), "tasks:", sum(t["kind"] == "convert" for t in tasks), "convert,", sum(t["kind"] == "new" for t in tasks), "new;", ", ".join(f"writer {k}: {len(t)}" for k, t in out.items()))
