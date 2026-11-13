#!/usr/bin/env python3
"""Keep the last fully checked version of every claim (METHODS §12; site publication rule).

The site shows a claim only in a version whose evidence anchors have all been checked by a second reader. While a claim
has anchors a first reader has just added (anchor_status 'ai-located' or 'unchecked'), the build shows the version kept
here instead. Run this before each publish: every claim with no unchecked anchors is copied into
data/claims/_published/<substance>.json, replacing its older copy.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
for f in sorted((ROOT / "data" / "claims").glob("*.json")):
    cur = json.load(open(f, encoding="utf-8"))
    pf = ROOT / "data" / "claims" / "_published" / f.name
    pub = {c["id"]: c for c in (json.load(open(pf, encoding="utf-8")) if pf.exists() else [])}
    kept, updated = [], 0
    for c in cur:
        if any(e.get("anchor_status") in ("ai-located", "unchecked") for e in c["evidence"]):
            if c["id"] in pub: kept.append(c["id"])
            continue
        if pub.get(c["id"]) != c: updated += 1
        pub[c["id"]] = c
    order = [c["id"] for c in cur]
    json.dump([pub[i] for i in order if i in pub], open(pf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{f.name}: {updated} claims updated in the published copy; held at their last checked version: {', '.join(kept) or 'none'}")
