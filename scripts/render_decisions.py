#!/usr/bin/env python3
"""Write docs/SENIOR-DECISIONS.md from data/site/decisions.json (the same list is shown in the site's Review tab).

Usage: render_decisions.py [DECISIONS_FROM_DB.json]
With a JSON export of the site's 'decisions' collection ({id: {choice, note, date}}), each item also shows the senior
author's recorded choice.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
data = json.load(open(ROOT / "data" / "site" / "decisions.json", encoding="utf-8"))
made = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
out = ["# Decisions for the senior author", "",
       f"Updated {data['updated']}. Generated from `data/site/decisions.json` by `scripts/render_decisions.py`; the same list is at the",
       "top of the site's Review tab, where your choices are saved. Each item gives the options and the editor's recommendation;",
       "nothing changes until you decide.", ""]
group = None
for n, it in enumerate(data["items"], 1):
    if it["group"] != group:
        group = it["group"]; out += [f"## {group}", ""]
    line = f"{n}. **{it['title']}**"
    if it.get("detail"): line += f" {it['detail']}"
    if it.get("claims"): line += " (" + ", ".join(f"`{c}`" for c in it["claims"]) + ")"
    out.append(line)
    if it.get("options"):
        out.append("   " + " ".join(f"☐ {o}" for o in it["options"]) + f". *Recommendation: {it['options'][it['recommend']]}.*")
    else:
        out.append("   ______")
    m = made.get(it["id"])
    if m:
        ch = it["options"][m["choice"]] if isinstance(m.get("choice"), int) and it.get("options") else m.get("choice", "")
        out.append(f"   **Decided {m.get('date', '')}:** {ch}" + (f" — {m['note']}" if m.get("note") else ""))
    out.append("")
(ROOT / "docs" / "SENIOR-DECISIONS.md").write_text("\n".join(out), encoding="utf-8")
print(f"wrote docs/SENIOR-DECISIONS.md ({len(data['items'])} items, {len(made)} decided)")
