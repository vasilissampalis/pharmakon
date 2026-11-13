#!/usr/bin/env python3
"""Merge a country's national-law reading (data/legal/_incoming/<country>.json, brief W2) into the per-drug law files.

Usage: merge_national_law.py [country-slug ...]   (default: every file in data/legal/_incoming/)

Each incoming file holds {"jurisdiction", "sources", "entries": {drug-page slug: [entry, ...]}, "not_found", "unsettled"}.
For every drug page, the country's existing rows are replaced by the incoming ones (so re-running is safe). When a drug
page has several named items (for example the benzodiazepines), each row's status starts with the item's name, as the
existing national rows do. The row keeps the reading's verification (ai-checked when two readings agreed, draft otherwise).
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INC = ROOT / "data" / "legal" / "_incoming"
names = sys.argv[1:] or sorted(p.stem for p in INC.glob("*.json"))
for name in names:
    d = json.load(open(INC / f"{name}.json", encoding="utf-8"))
    jur = d["jurisdiction"]
    titles = {s.get("url"): s.get("title") for s in d.get("sources", [])}
    n_rows = 0
    for slug, rows in d["entries"].items():
        f = ROOT / "data" / "legal" / f"{slug}.json"
        if not f.exists():
            print(f"SKIP {jur}: no law file for {slug}"); continue
        doc = json.load(open(f, encoding="utf-8")); one = isinstance(doc, dict); docs = [doc] if one else doc
        L = docs[0]
        multi = len(rows) > 1
        new = []
        for e in rows:
            status = e["status"]
            if multi and e.get("item") and not status.startswith(e["item"]):
                status = e["item"].split(" (")[0] + ": " + status
            row = {"jurisdiction": jur, "status": status, "instrument": e.get("instrument") or "Not named in the lists read", "source_url": e.get("source_url") or ""}
            if titles.get(e.get("source_url")): row["source_title"] = titles[e["source_url"]]
            if not row["source_url"]:
                # an item not found names no single source: point to the main list read and name every list searched
                srcs = [x for x in d.get("sources", []) if x.get("url")]
                row["source_url"] = srcs[0]["url"] if srcs else ""
                row["source_title"] = "Lists searched: " + "; ".join(x.get("title", x["url"]) for x in srcs)
            for k in ("source_date", "medical_use", "checked_on", "checked_by", "verification", "note"):
                if e.get(k) is not None: row[k] = e[k]
            new.append(row)
        L["entries"] = [x for x in L["entries"] if x["jurisdiction"] != jur] + new
        n_rows += len(new)
        json.dump(doc if one else docs, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"merged {jur}: {n_rows} rows on {len(d['entries'])} drug pages")
