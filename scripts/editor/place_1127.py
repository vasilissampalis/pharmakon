"""place_1127.py [--dry]: put the answer on what a drug screen can miss (writer 765, round pdf-2026-11-26, checked 27 November 2026)
on its home page (data/site/questions.json, in people's words from its plain lines). Its other pages show it through its plain
lines' `pages` (fentanyl, benzodiazepines, prescription opioids)."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
dry = "--dry" in sys.argv
QF = ROOT / "data/site/questions.json"
Q = json.load(open(QF, encoding="utf-8"))
S = json.load(open(ROOT / "data/site/simple.json", encoding="utf-8"))["claims"]
PLACE = [("general", "Drug tests", "cl_gen_drug_test_misses")]
done = []
for page, group, cid in PLACE:
    if cid not in S or not S[cid].get("q"): print("  no plain lines yet, not placed:", cid); continue
    groups = Q.setdefault(page, [])
    if any(it[0] == cid for g in groups for it in g["items"]): continue
    g = next((g for g in groups if g.get("topic") == group), None)
    if not g: g = {"topic": group, "items": []}; groups.append(g)
    g["items"].append([cid, S[cid]["q"]]); done.append(f"{page} / {group}: {cid}")
print("\n".join(done) or "nothing to place")
if not dry: QF.write_text(json.dumps(Q, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
