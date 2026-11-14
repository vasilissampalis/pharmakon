"""make_demand.py [--dry]: how much people ask about each answer's question, from every source on file (CLAUDE.md, "Demand
first"), written to data/site/demand.json (the site reads each answer's score) and data/verification/demand-themes.md
(the themes ranked, with what the site already answers: the list of what to write next).

Sources, by family:
- Reddit: data/verification/questions-2026-11-13/reddit-themes.json (posts with a question, per theme, from the senior
  author's pastes of 13 November) and any later per-question files whose `site` is "Reddit".
- Forums: data/verification/questions-*/forums.json (per question: site, theme, covered_by), from 14 November on.
Each question is weighted by how much it was read or answered, against what is typical where it was posted (so one big
community does not decide the order): Reddit posts by votes plus comments over their community's median, as in the Reddit
coding (its theme scores, `reddit-themes.md`); forum questions by views over their site's median where the site shows views
(Bluelight), capped at 10, otherwise 1. A theme's share in a family is its share of that family's weight; the two families count equally (a
theme's demand is the mean of its two shares), so neither drowns the other.
Themes are matched by their exact names. The four themes the site will not answer (amounts and redosing, strongest drug,
form or route and preparation, getting drugs and legal trouble, hiding use) are ranked but give no score.
Scores: the answerable themes in order of demand get 100 down to about 2; an answer takes the best score of the themes it
covers (covered_by in either source)."""
import json, glob, ast, os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
dry = "--dry" in sys.argv
lit = lambda v: ast.literal_eval(v) if isinstance(v, str) else v
R = json.load(open("data/verification/questions-2026-11-13/reddit-themes.json", encoding="utf-8"))["themes"]
fam = {"reddit": {}, "forums": {}}; covers = {}; examples = {}; no = set(); can = {}
def cover(theme, ids):
    for i in ids or []:
        cid = i["id"] if isinstance(i, dict) else i
        if cid: covers.setdefault(theme, set()).add(cid)
import re, statistics
md = open("data/verification/questions-2026-11-13/reddit-themes.md", encoding="utf-8").read()
rscore = {}
for row in md.splitlines():
    c = [x.strip() for x in row.strip().strip("|").split("|")]
    if len(c) >= 6 and c[0].isdigit():
        try: rscore[c[1]] = float(c[5].replace(",", ""))
        except ValueError: pass
for th in R:
    name = th["theme"]; fam["reddit"][name] = fam["reddit"].get(name, 0) + rscore.get(name, float(th.get("posts") or 0))
    cover(name, lit(th.get("covered_by"))); can[name] = th.get("can_we_answer")
    if th.get("can_we_answer") == "no": no.add(name)
    examples.setdefault(name, []).extend([e for e in (lit(th.get("examples")) or [])][:2])
qs = [q for f in sorted(glob.glob("data/verification/questions-*/forums.json")) + sorted(glob.glob("data/verification/questions-*/reddit-*.questions.json"))
      for q in json.load(open(f, encoding="utf-8"))["questions"]]
med = {}
for site in {q.get("site") for q in qs}:
    v = [q["views"] for q in qs if q.get("site") == site and isinstance(q.get("views"), (int, float)) and q["views"] > 0]
    if v: med[site] = statistics.median(v)
for q in qs:
        k = "reddit" if q.get("site") == "Reddit" else "forums"
        # views over the site's median, capped at 10 times a typical question, so a few megathreads (some have tens of times the
        # typical views, and their parts count separately) cannot decide the order alone
        w = q["engagement"] if isinstance(q.get("engagement"), (int, float)) else (min(10.0, q["views"] / med[q["site"]]) if q.get("site") in med and isinstance(q.get("views"), (int, float)) and q["views"] > 0 else 1)
        name = q["theme"]; fam[k][name] = fam[k].get(name, 0) + w
        cover(name, q.get("covered_by"))
        if len(examples.setdefault(name, [])) < 3 and q.get("question"): examples[name].append(q["question"] + " (" + q.get("site", "") + ")")
tot = {k: sum(v.values()) or 1 for k, v in fam.items()}
themes = sorted(set(fam["reddit"]) | set(fam["forums"]))
share = {t: (fam["reddit"].get(t, 0) / tot["reddit"] + fam["forums"].get(t, 0) / tot["forums"]) / 2 for t in themes}
ranked = sorted(themes, key=lambda t: -share[t])
answerable = [t for t in ranked if t not in no]
n = len(answerable)
tscore = {t: round(100 - i * 98 / max(1, n - 1)) for i, t in enumerate(answerable)}
claims = {}
for t in answerable:
    for cid in covers.get(t, ()):
        cur = claims.get(cid)
        if not cur or tscore[t] > cur["score"]: claims[cid] = {"score": tscore[t], "themes": []}
for t in answerable:
    for cid in covers.get(t, ()): claims[cid]["themes"].append(ranked.index(t) + 1)
out = {"_note": "How much people ask about each answer's question (scripts/editor/make_demand.py): themes from the Reddit pages the "
       "senior author pasted (13 November 2026) and from forums outside Reddit (Bluelight, Drugs-Forum, Drugs.com Answers, Ask Erowid, "
       "Shroomery, DMT-Nexus, DanceSafe; 14 November), each family counting equally; score 100 for the most-asked answerable theme down "
       "to about 2; an answer takes the best score of the themes it covers; themes we will not answer give no score. The ranked themes, "
       "and what the site does not answer yet: data/verification/demand-themes.md.", "claims": dict(sorted(claims.items()))}
lines = ["# What people ask, ranked (all sources)", "",
         f"Made by `scripts/editor/make_demand.py`. Reddit and forum columns are weights (votes, comments or views against what is typical where posted; 1 = a typical question). "
         "Demand = the mean of a theme's share of Reddit questions and its share of forum questions. \"no\" = a theme the site will not "
         "answer (it gives no score). Answers = published answers that cover the theme (fully or partly).", "",
         "| Rank | Theme | Reddit | Forums | Demand | Answers | Examples |", "|---|---|---|---|---|---|---|"]
for i, t in enumerate(ranked, 1):
    ex = "; ".join(str(e) for e in examples.get(t, [])[:2]).replace("|", "/")
    lines.append(f"| {i} | {t}{' (no)' if t in no else ''} | {fam['reddit'].get(t, 0):.1f} | {fam['forums'].get(t, 0):.1f} | {share[t]*100:.1f}% | {len(covers.get(t, ()))} | {ex[:160]} |")
lines += ["", "## Most asked, and the site has no answer yet", ""]
lines += [f"- {t} ({share[t]*100:.1f}%)" for t in answerable if not covers.get(t)][:25]
print(f"{len(ranked)} themes ({len(no)} not answered by policy); {len(claims)} answers scored; top 10:")
for t in ranked[:10]: print(f"  {share[t]*100:5.1f}%  {'no ' if t in no else ''}{t[:95]}  [answers: {len(covers.get(t, ()))}]")
if not dry:
    with open("data/site/demand.json", "w", encoding="utf-8") as f: json.dump(out, f, ensure_ascii=False, indent=1); f.write("\n")
    with open("data/verification/demand-themes.md", "w", encoding="utf-8") as f: f.write("\n".join(lines) + "\n")
