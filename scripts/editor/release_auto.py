#!/usr/bin/env python3
"""The editor lets answers written by the system out after reading them (data/auto/lane/policy.json, hold_new: while it is
true, the lane holds what it writes as "waiting"). Only an answer the lane itself had passed and held for this reading
can be let out here: one that waits for a person for another reason (dying, overdose, mixing, pregnancy, children,
suicide, a disagreement with a checked claim) is not this tool's to release.

  python3 -I scripts/editor/release_auto.py au_w_0001 au_w_0002      (let these out)
  python3 -I scripts/editor/release_auto.py --list                    (what is held)
"""
import json, sys, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "data" / "auto" / "answers"
recs = {f.stem: json.load(open(f, encoding="utf-8")) for f in sorted(OUT.glob("au_*.json"))}
held = {k: r for k, r in recs.items() if r.get("status") == "waiting" and r.get("held")}
if "--list" in sys.argv or len(sys.argv) < 2:
    for k, r in held.items(): print(k, "| lane", r.get("lane"), "|", r.get("question"))
    sys.exit(0)
for k in [a for a in sys.argv[1:] if not a.startswith("--")]:
    r = held.get(k)
    if not r: print(k, ": not held for the editor's reading (nothing done)"); continue
    r["status"] = "published"; r["why"] = "passed every gate; read by the editor and let out on " + datetime.date.today().isoformat(); r["released"] = {"by": "the editor, after reading every sentence against its sources", "on": datetime.date.today().isoformat(), "was": r.pop("held")}
    json.dump(r, open(OUT / (k + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(k, ": let out")
