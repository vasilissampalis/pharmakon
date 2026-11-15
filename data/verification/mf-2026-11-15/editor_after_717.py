"""editor_after_717.py: the editor's decisions after blind check 717 (15 November 2026). The checker passed five facts twice,
once as a new card (writer 712) and once as a clearer wording of an older card, and asked the editors to keep one of each.
Kept: the clearer or better-hedged one. Left off (n in tasks_check717.json): 9, 36, 17, 38, 31. Card 42 says "serotonin
changes on scans", words the checker did not find in the plain lines it was given: they are the answer's own question on
the site ("After stopping ecstasy, do serotonin changes on scans return to normal?"), so the card stays. Then the checker's
interest and clarity scores for the cards that stay go to data/site/tf-interest.json (n = 1)."""
import json, sys, pathlib, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts/editor"))
import sj
D = ROOT / "data/verification/mf-2026-11-15"
o = json.load(open(D / "check_out717.json", encoding="utf-8")); t = json.load(open(D / "tasks_check717.json", encoding="utf-8"))
Q = {q["n"]: q for q in t["quiz"]}; R = {r["n"]: r for r in o["quiz"]}
final = lambda n: (R[n].get("item") if R[n]["verdict"] == "fix" and R[n].get("item") else Q[n]["item"])["statement"]
LEAVE = {9: "same fact as card 35, which is clearer", 36: "same fact as card 16, which is plainer", 17: "same fact as card 28, which says 'in published cases'",
         38: "same fact as card 26, which is plainer", 31: "same answer as card 11, which is the stronger card"}
S = sj.load(); gone = 0
for n, why in LEAVE.items():
    st = final(n); claim = Q[n]["item"]["claim"]
    for pg, items in S["tf"].items():
        keep = [x for x in items if not (x.get("claim") == claim and x.get("statement") == st)]
        gone += len(items) - len(keep); S["tf"][pg] = keep
sj.save(S)
TI = ROOT / "data/site/tf-interest.json"; T = json.loads(TI.read_text(encoding="utf-8")); add = 0
for n, r in R.items():
    if r["verdict"] not in ("ok", "fix") or n in LEAVE: continue
    T["items"][hashlib.sha1(final(n).encode("utf-8")).hexdigest()[:12]] = {"interest": float(r["interest"]), "clear": float(r["clear"]), "test_feel": 0, "n": 1, "by": "AI reader 717 (blind check)"}; add += 1
TI.write_text(json.dumps(T, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
cut = T["cut"]; shown = sum(1 for items in S["tf"].values() for x in items if (lambda v: v and v["interest"] >= cut["interest"] and v["clear"] >= cut["clear"])(T["items"].get(hashlib.sha1(x["statement"].encode("utf-8")).hexdigest()[:12])))
print("cards left off as repeats:", gone, "| scores added:", add, "| cards on file:", sum(len(v) for v in S["tf"].values()), "| shown at the cut:", shown)
