"""make_voice_tasks.py DIR FIRST_WRITER N_WRITERS MIN_SCORE: tasks for the plain-voice pass (docs/WRITING-RULES.md, Rule 0c;
senior author, 13 November 2026: "too academic, nobody reads it"; "people like talking to humans not textbooks").

Takes every answer with a demand score of MIN_SCORE or more (data/site/demand.json) that is on the site with plain lines,
leaves out section 7 (senior-gated wording), ranks them by score and deals them out in turn, so each writer gets a mix.
Writes data/verification/DIR/tasks_voice<k>.json for writers k = FIRST_WRITER .. FIRST_WRITER + N_WRITERS - 1, and
data/verification/DIR/before.json with the lines as they are now (kept for comparison and for going back).

Each task carries what the writer may use: the claim's own text fields (statement, who was studied, comparison, outcome,
how big, the rating reasoning, the editors' reading of a debate), the current plain lines and question headings, the
sources' short names for the How-we-know source lists, and how people ask the question (Reddit theme examples)."""
import json, glob, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
d, first, nw, minsc = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
D = pathlib.Path(f"data/verification/{d}"); D.mkdir(parents=True, exist_ok=True)
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
R = {}
for f in glob.glob("data/references/*.json"):
    for r in json.load(open(f, encoding="utf-8")): R[r["id"]] = r
def short(rid):
    r = R.get(rid)
    if not r: return rid
    a = r.get("author") or []
    fam = lambda x: x.get("family") or x.get("literal") or "?"
    who = fam(a[0]) if len(a) == 1 else fam(a[0]) + " & " + fam(a[1]) if len(a) == 2 else (fam(a[0]) + " et al." if a else (r.get("publisher") or "?"))
    y = ((r.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    return f"{who}, {y}"
S = json.load(open("data/site/simple.json", encoding="utf-8"))["claims"]
Q = json.load(open("data/site/questions.json", encoding="utf-8"))
qs = {}
for slug, groups in Q.items():
    if slug == "_note": continue
    for g in groups:
        for cid, q in g["items"]: qs.setdefault(cid, []).append({"page": slug, "topic": g.get("topic"), "q": q})
DM = json.load(open("data/site/demand.json", encoding="utf-8"))["claims"]
TH = json.load(open("data/verification/questions-2026-11-13/reddit-themes.json", encoding="utf-8"))["themes"]
score = {k: (v["score"] if isinstance(v, dict) else v) for k, v in DM.items()}
ids = [k for k, v in sorted(score.items(), key=lambda kv: (-kv[1], kv[0])) if v >= minsc and k in S and k in C and C[k].get("section") != 7]
before, tasks = {}, {k: [] for k in range(first, first + nw)}
for i, k in enumerate(ids):
    c = C[k]; e = S[k]; before[k] = e
    themes = []
    for t in (DM[k].get("themes") if isinstance(DM[k], dict) else []) or []:
        if 1 <= t <= len(TH): th = TH[t - 1]; themes.append({"theme": th["theme"], "examples": th.get("examples", [])[:4]})
    refs = sorted({a["reference"] for a in c["evidence"]})
    tasks[first + i % nw].append({
        "id": k, "section": c.get("section"), "substance": c.get("substance"), "status": c.get("status"), "certainty": c["grade"]["certainty"],
        "demand": score[k], "how_people_ask": themes,
        "questions_now": qs.get(k, []) + ([{"page": "(general pages)", "q": e["q"]}] if e.get("q") else []),
        "lines_now": {f: e[f] for f in ("short", "but", "how", "how_src", "rate", "freq") if f in e},
        "sources": [{"ref": r, "name": short(r)} for r in refs],
        "claim": {"statement": c["statement"], "population": c.get("population"), "exposure": c.get("exposure"), "comparator": c.get("comparator"),
                  "outcome": c.get("outcome"), "magnitude": c.get("magnitude"), "rating_reasoning": c["grade"].get("reasoning"),
                  "editors_reading": (c.get("debate") or {}).get("editors_reading"), "version": c["version"]}})
for k, t in tasks.items():
    with open(D / f"tasks_voice{k}.json", "w", encoding="utf-8") as f: json.dump({"writer": k, "answers": t}, f, ensure_ascii=False, indent=1); f.write("\n")
with open(D / "before.json", "w", encoding="utf-8") as f:
    json.dump({"_note": "Plain lines before the plain-voice pass (Rule 0c), for comparison and for going back.", "claims": before}, f, ensure_ascii=False, indent=1); f.write("\n")
print(len(ids), "answers;", ", ".join(f"writer {k}: {len(t)}" for k, t in tasks.items()))
