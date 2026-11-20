#!/usr/bin/env python3
"""reshow_quotes.py: show, under each How-do-we-know line of a published machine-lane answer, the quotation the lane's own rule picks today
(scripts/auto/lane.py, shown_quote), from the items the line already rests on. Nothing else in the record changes: no line, no source, no
gate. A line that shows no quotation is left so (the answers of the lanes before quotations were shown).

    python3 -I scripts/editor/reshow_quotes.py [--write]

Without --write it lists what would change. (20 November 2026: under 'A review examined global toxicological case data on tramadol' stood a
finding's words about how tramadol acts on serotonin, au_w_f0008.)"""
import sys, json, glob, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "auto"))
import lane

n = 0
for f in sorted(glob.glob(str(ROOT / "data" / "auto" / "answers" / "au_*.json"))):
    a = json.load(open(f, encoding="utf-8")); changed = False
    if a.get("status") != "published": continue
    for p in a.get("parts") or []:
        if not p["part"].startswith("how") or not p.get("quote"): continue
        labels = {r["label"]: {"quote": r["quote"], "ref": r["ref"]} for r in p.get("rests_on") or [] if r.get("label") and r.get("quote")}
        new = lane.shown_quote(p, labels)
        if new and new["quote"] != p["quote"]:
            print(f"{a['id']} {p['part']}: {p['text'][:90]}\n   was: {p['quote']}\n   now: {new['quote']}"); n += 1
            p.update(new); changed = True
    if changed and "--write" in sys.argv:
        json.dump(a, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # as the lane writes it
print(f"{n} quotation(s) {'shown anew' if '--write' in sys.argv else 'would change'}")
