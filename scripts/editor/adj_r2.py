"""adj_r2.py DIR READER [--dry]: adjudicate a round-2 reader's checks of first-pass study cards.

Reads data/verification/DIR/round2/tasks_reader<N>.json (cards: {card, file}) and out_reader<N>.json (card_checks).
- key finding or reporting issue `corrected`: the reader's text replaces the card's (a finding may start "finding:" or
  "note:"; an issue may be "issue: ... | consequence: ..."); the old text goes into verification.disagreements.
- `wrong-location`: "page: X; locator: Y" from the correction updates the item's page and locator.
- `not-found`: logged as a disagreement held for the editor and printed; the item is not changed.
- `missed`: logged as a disagreement "recorded for the card's next revision".
- Risk-of-bias and interpretation-gap verdicts are printed for the editor, who decides them separately.
Marks each card ai-checked (checked_by "AI reader <N> (round-2 check); adjudicated by the AI co-editor").
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
d, n = sys.argv[1], sys.argv[2]; dry = "--dry" in sys.argv
D = ROOT / "data" / "verification" / d / "round2"
tasks = json.load(open(D / f"tasks_reader{n}.json", encoding="utf-8"))
out = json.load(open(D / f"out_reader{n}.json", encoding="utf-8"))
date = out.get("date", "")
who = f"AI reader {n} (round-2 check)"
files = {c["card"]: ROOT / c["file"] for c in tasks.get("cards", [])}

def loc_parse(text):
    m = re.search(r"page:\s*(.*?)\s*;\s*locator:\s*(.*?)(?:\.\s+(The .*))?$", text or "", re.S)
    return (m.group(1), m.group(2)) if m else (None, None)

for cid, cc in (out.get("card_checks") or {}).items():
    fp = files.get(cid)
    if not fp or not fp.exists():
        print("!! no incoming file for", cid); continue
    card = json.load(open(fp, encoding="utf-8")); ver = card.setdefault("verification", {})
    dis = ver.setdefault("disagreements", [])
    held = []
    def log(field, old, new, res): dis.append({"field": field, "first_pass": old, "reviewer": new, "resolution": res})
    for kind, textkey in (("key_findings", "finding"), ("reporting_issues", "issue")):
        items = card.get(kind, [])
        for r in cc.get(kind, []):
            i, v, corr = r.get("index"), r.get("verdict"), (r.get("correction") or "").strip()
            if v == "confirmed" or i is None: continue
            if not (0 <= i < len(items)):
                held.append(f"{kind}[{i}] {v}: index out of range"); continue
            it = items[i]
            if v == "corrected" and corr:
                if kind == "key_findings":
                    m = re.match(r"^(finding|note):\s*", corr, re.I)
                    key = (m.group(1).lower() if m else "finding"); text = corr[m.end():] if m else corr
                    old = it.get(key, ""); it[key] = text
                    log(f"{kind}[{i}].{key}", old, text, f"Second reader's correction adopted by the AI co-editor ({who})")
                else:
                    if "|" in corr and re.search(r"consequence:", corr, re.I):
                        a, b = corr.split("|", 1)
                        new_issue = re.sub(r"^\s*issue:\s*", "", a, flags=re.I).strip(); new_cons = re.sub(r"^\s*consequence:\s*", "", b, flags=re.I).strip()
                        log(f"{kind}[{i}]", it.get("issue", "") + " | " + it.get("consequence", ""), corr, f"Second reader's correction adopted by the AI co-editor ({who})")
                        it["issue"], it["consequence"] = new_issue, new_cons
                    elif re.match(r"^\s*consequence:", corr, re.I):
                        new_cons = re.sub(r"^\s*consequence:\s*", "", corr, flags=re.I).strip()
                        log(f"{kind}[{i}].consequence", it.get("consequence", ""), new_cons, f"Second reader's correction adopted by the AI co-editor ({who})")
                        it["consequence"] = new_cons
                    else:
                        new_issue = re.sub(r"^\s*issue:\s*", "", corr, flags=re.I).strip()
                        log(f"{kind}[{i}].issue", it.get("issue", ""), new_issue, f"Second reader's correction adopted by the AI co-editor ({who})")
                        it["issue"] = new_issue
            elif v == "wrong-location":
                pg, lc = loc_parse(corr)
                if pg is None:
                    held.append(f"{kind}[{i}] wrong-location, unparsed: {corr[:200]}"); continue
                log(f"{kind}[{i}].page/locator", f"{it.get('page', '')}; {it.get('locator', '')}", f"{pg}; {lc}", f"Second reader's location adopted by the AI co-editor ({who})")
                it["page"] = pg
                if lc: it["locator"] = lc
            elif v == "not-found":
                log(f"{kind}[{i}]", it.get(textkey, ""), corr or "not found at the stated place", f"Not found by {who}: held for the editor")
                held.append(f"{kind}[{i}] NOT FOUND: {corr[:300]}")
    for m in cc.get("missed", []):
        txt = m if isinstance(m, str) else json.dumps(m, ensure_ascii=False)
        log("missed", "", txt, "Recorded for the card's next revision; not yet in the card.")
    ver["status"] = "ai-checked"
    ver["checked_by"] = f"{who}; adjudicated by the AI co-editor"
    if date: ver["checked_on"] = date
    rob, gap = cc.get("risk_of_bias", {}), cc.get("interpretation_gap", {})
    print(f"== {cid}: rob {rob.get('verdict')} | {(rob.get('note') or '')[:300]}")
    print(f"   gap {gap.get('verdict')} | {(gap.get('note') or '')[:300]}")
    for h in held: print("   HELD", h)
    if not dry:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(card, f, ensure_ascii=False, indent=1); f.write("\n")
