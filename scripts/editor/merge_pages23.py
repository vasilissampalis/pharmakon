"""merge_pages23.py [for-you] [descriptions] [kits] [interest] [--dry]: install what the 2.3 content rounds produced, only
as the second readers confirmed it (data/verification/pages-2026-11-15, data/verification/quiz/interest-2026-11-15).

for-you       reader 701's "For you" lines, as second reader 702 judged them -> data/site/stay-safer.json signs.<family>.self
descriptions  reader 703's lines on what each drug is, as second reader 704 judged them -> data/site/descriptions.json
kits          finder 705's seller pages per drug, those verifier 706 confirmed -> data/site/kit-links.json
interest      raters 699 and 700 -> data/site/tf-interest.json (mean of the two; the cut decides what the decks show)
A line is installed only with verdict ok, or fix (the second reader's corrected line), and only with its confirmed
anchors (corrected quotes and headings taken over); a line left with no confirmed anchor is not installed."""
import json, sys, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]; P = ROOT / "data/verification/pages-2026-11-15"
J = lambda p: json.load(open(p, encoding="utf-8")); dry = "--dry" in sys.argv; what = [a for a in sys.argv[1:] if not a.startswith("--")]
def save(p, d):
    if not dry: p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
def take(lines, checks, who):
    """lines: [{line, anchors}], checks: [{index, line_verdict, line, anchors: [{index, verdict, quote, where}]}]"""
    out, dropped = [], []
    by = {c["index"]: c for c in checks or []}
    for i, ln in enumerate(lines):
        c = by.get(i)
        if not c or c.get("line_verdict") not in ("ok", "fix"): dropped.append((ln["line"], (c or {}).get("line_verdict", "not checked"))); continue
        av = {a["index"]: a for a in c.get("anchors") or []}; anchors = []
        for j, a in enumerate(ln["anchors"]):
            v = av.get(j)
            if not v or v.get("verdict") not in ("confirmed", "corrected"): continue
            a = dict(a)
            if v["verdict"] == "corrected":
                if v.get("quote"): a["quote"] = v["quote"]
                if v.get("where"): a["where"] = v["where"]
            a.update({"check": "confirmed", "checked_by": who, "checked_on": "2026-11-15"}); anchors.append(a)
        if not anchors: dropped.append((ln["line"], "no confirmed anchor")); continue
        line = c["line"].strip() if c["line_verdict"] == "fix" and (c.get("line") or "").strip() else ln["line"]
        item = {"line": line, "anchors": anchors, "line_check": {"by": who, "on": "2026-11-15", "ok": True}}
        if line != ln["line"]: item["edited"] = "line changed to match its sources after the second reading"
        out.append(item)
    return out, dropped
if "for-you" in what:
    a = J(P / "for_you_701.json")["families"]; c = J(P / "for_you_check_702.json")["families"]
    S = J(ROOT / "data/site/stay-safer.json"); n = 0
    for fam, v in a.items():
        lines, dropped = take(v.get("self") or [], c.get(fam), "AI reader 702 (second reader)")
        if fam in S["signs"] and lines: S["signs"][fam]["self"] = lines; n += len(lines)
        print(f"for you / {fam}: {len(lines)} installed" + (f"; not installed: {dropped}" if dropped else ""))
    save(ROOT / "data/site/stay-safer.json", S); print("for-you lines installed:", n)
if "descriptions" in what:
    a = J(P / "descriptions_703.json")["drugs"]; c, who_of = {}, {}
    for f in sorted(P.glob("descriptions_check_*.json")):      # second readers 704, 715 and 716, ten drugs each
        x = J(f)
        for slug, checks in x["drugs"].items(): c[slug] = checks; who_of[slug] = x["reader"]
    out = {"_note": "What each drug is, in two to four plain lines, for the top of its page (senior author, 15 November 2026: 'a description for each drug that makes you understand what it is and its sources are validated'). Identity lines only (no risks, amounts or how-to), in our own words from official pages; written by AI reader 703, every anchor and line checked at its source by a second reader (AI readers 704, 715 and 716, ten drugs each); data/verification/pages-2026-11-15.", "read_on": "2026-11-15", "drugs": {}}
    for slug, v in a.items():
        lines, dropped = take(v.get("lines") or [], c.get(slug), who_of.get(slug, "second reader"))
        if lines: out["drugs"][slug] = {"lines": lines}
        print(f"description / {slug}: {len(lines)} lines" + (f"; not installed: {dropped}" if dropped else ""))
    save(ROOT / "data/site/descriptions.json", out); print("drugs with a description:", len(out["drugs"]))
if "kits" in what:
    a = J(P / "kit_links_705.json")["sellers"]; c = {(x["seller"], x["slug"]): x for x in J(P / "kit_links_check_706.json")["checks"]}
    out = {"_note": "Each seller's own page for each drug's test kit (senior author, 15 November 2026: 'the links should be individualized for each drug page'). Found by AI reader 705, each page opened and confirmed by AI reader 706; data/verification/pages-2026-11-15. A link, not an endorsement: we have not tested their kits.", "read_on": "2026-11-15", "sellers": {}}
    n = 0
    # the editor's decisions after the verifier's notes (kit_links_editor.json): entries not to show, with the reason; plain
    # labels that say what is sold (the seller's own label stays as label_seen); a seller's page language
    E = J(P / "kit_links_editor.json") if (P / "kit_links_editor.json").exists() else {}
    dropped = {(x["seller"], x["slug"]) for x in E.get("drop", [])}; relabel = {(x["seller"], x["slug"]): x["label"] for x in E.get("label", [])}
    out["_note"] += " The editor's decisions (entries left out, with reasons, and plain labels): kit_links_editor.json in the same folder."
    for seller, v in a.items():
        drugs = {}
        for s, d in (v.get("drugs") or {}).items():
            if c.get((seller, s), {}).get("verdict") != "confirmed" or (seller, s) in dropped: continue
            e = {"url": d["url"], "label": relabel.get((seller, s), d["label"]), "read_on": d.get("read_on", "2026-11-15"), "check": "confirmed", "checked_by": "AI reader 706"}
            if e["label"] != d["label"]: e["label_seen"] = d["label"]
            drugs[s] = e
        if drugs: out["sellers"][seller] = {"name": seller, "home": v.get("home"), **(E.get("seller", {}).get(seller) or {}), "drugs": drugs}; n += len(drugs)
        print(f"kit links / {seller}: {len(drugs)} of {len(v.get('drugs') or {})} shown" + (f" ({sum(1 for s in (v.get('drugs') or {}) if (seller, s) in dropped)} left out by the editor)" if any((seller, s) in dropped for s in (v.get('drugs') or {})) else ""))
    save(ROOT / "data/site/kit-links.json", out); print("kit links installed:", n)
if "interest" in what:
    R = ROOT / "data/verification/quiz/interest-2026-11-15"; ra, rb = J(R / "ratings_699.json")["ratings"], J(R / "ratings_700.json")["ratings"]
    acc = {}
    for r in ra + rb: acc.setdefault(r["key"], []).append(r)
    items = {k: {"interest": round(sum(x["interest"] for x in v) / len(v), 2), "clear": round(sum(x["clear"] for x in v) / len(v), 2), "test_feel": sum(bool(x.get("test_feel")) for x in v), "n": len(v)} for k, v in acc.items()}
    cut = {"interest": 4.0, "clear": 4.0}
    keep = sum(1 for v in items.values() if v["interest"] >= cut["interest"] and v["clear"] >= cut["clear"])
    out = {"_note": "How much a common person would care about each Myth or fact? card, and how clear it is on first read (1 to 5; mean of AI raters 699 and 700, each blind to the other; data/verification/quiz/interest-2026-11-15). Senior author, 15 November 2026: 'less than half of them are interesting for most users. they feel a lot like an academic test'. Decks show the cards at or above the cut, most interesting first. key = first 12 hex of SHA-1 of the statement.", "cut": cut, "items": items}
    save(ROOT / "data/site/tf-interest.json", out); print(f"cards rated: {len(items)}; kept at the cut: {keep}")
