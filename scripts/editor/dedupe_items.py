"""dedupe_items.py [--dry]: remove true-or-false and quiz items in data/site/simple.json that a newer copy of the same item
(same kind, page, claim and statement or question) supersedes. Items with no newer copy are kept, whatever their v."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sj
dry = "--dry" in sys.argv
S = sj.load()
vt = lambda v: tuple(int(x) for x in (v or "0").split("."))
gone = 0
for kind in ("tf", "quiz"):
    for page, items in S[kind].items():
        best = {}
        for it in items:
            k = (it["claim"], it.get("statement", it.get("q")))
            best[k] = max(best.get(k, (0,)), vt(it.get("v")))
        keep = []
        for it in items:
            k = (it["claim"], it.get("statement", it.get("q")))
            if vt(it.get("v")) < best[k]:
                gone += 1; print("superseded:", kind, page, it["claim"], "v" + str(it.get("v")), "|", k[1][:80])
            else:
                keep.append(it)
        S[kind][page] = keep
print(gone, "removed" + (" (dry run)" if dry else ""))
if not dry and gone: sj.save(S)
