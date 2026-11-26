"""fix_pouches_quits_1127.py: cl_nic_pouches_stopping's grade said 'five people had quit across all comparisons'; its own statement
gives seven (1 with pouches, 0 still smoking and 4 with e-cigarettes in the three-arm trial; 2 against 0 in the trial of two pouch
strengths). Found by writer 792 (27 November 2026). The rating does not change (two levels for imprecision either way). The claim
takes a patch version, and its plain lines and myth-or-fact items, which say nothing of the count, take the new version."""
import json, glob, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import sj
CID = "cl_nic_pouches_stopping"
f = next(f for f in glob.glob("data/claims/*.json") if any(c["id"] == CID for c in json.load(open(f, encoding="utf-8"))))
L = json.load(open(f, encoding="utf-8")); c = next(c for c in L if c["id"] == CID)
old_v = c["version"]; a, b, p = (int(x) for x in old_v.split(".")); new_v = f"{a}.{b}.{p + 1}"
g = c["grade"]
o1 = "Imprecision, two levels: five people had quit across all comparisons, and"
n1 = "Imprecision, two levels: seven people had quit across all comparisons (five in the three-arm trial, two in the trial of two strengths), and"
assert g["reasoning"].count(o1) == 1; g["reasoning"] = g["reasoning"].replace(o1, n1)
d = g["domains"]["imprecision"]; o2 = "Five quits in all across the comparisons;"; n2 = "Seven quits in all across the comparisons (five in the three-arm trial, two in the trial of two strengths);"
assert d["note"].count(o2) == 1; d["note"] = d["note"].replace(o2, n2)
c["version"] = new_v
c.setdefault("changelog", []).append({"version": new_v, "date": "2026-11-27", "change": "Editor: the grade's count of people who quit corrected from five to seven (five in the three-arm trial, two in the trial of two pouch strengths), as the statement's own figures give; found by writer 792. The rating does not change."})
json.dump(L, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(f, "a").write("\n")
S = sj.load(); assert S["claims"][CID]["v"] == old_v; S["claims"][CID]["v"] = new_v; n = 0
for kind in ("tf", "quiz"):
    for pg, items in S.get(kind, {}).items():
        for it in items:
            if it.get("claim") == CID and it.get("v") == old_v: it["v"] = new_v; n += 1
sj.save(S)
print(CID, old_v, "->", new_v, "| items re-versioned:", n)
