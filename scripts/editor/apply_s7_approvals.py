"""apply_s7_approvals.py DECISIONS.json [--write]: the senior author's decisions on section 7 answers, from his to-do page, into
data/verification/senior-gate.json (27 November 2026).

DECISIONS.json is the page's database collection s7 as read with the artifact database tool: either a list of documents
({"id": ..., "data": {...}} or the fields themselves with "id"), or {id: {...}}. Each document: decision ("approved" or
"change"), note, v (the claim version the lines on the page were written for), lv (the day those lines were written),
at (when he saved it).

An approval is recorded only where it is his, for exactly what he saw: decision "approved", v equal to the claim's version
now, and lv equal to the day of the lines on his page (data/verification/s7-simple-2026-11-27: "2026-11-27"; the lines of
the answers he approved before carry none). Anything else is reported and never written: a decision for other lines or an
older version (it stays as his record on the page), and every "change" with its note, for the editor. "Never record an
approval he did not give" (CLAUDE.md). Without --write it only shows what it would do."""
import glob, json, sys

LV = "2026-11-27"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args: sys.exit(__doc__)
raw = json.load(open(args[0], encoding="utf-8"))
docs = {}
for d in (raw.items() if isinstance(raw, dict) else ((x.get("id"), x) for x in raw)):
    k, v = d
    v = v.get("data", v) if isinstance(v, dict) else {}
    if k: docs[str(k).split("/")[-1]] = v
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
G = json.load(open("data/verification/senior-gate.json", encoding="utf-8"))
write, out, report = "--write" in sys.argv, [], []
for cid, d in sorted(docs.items()):
    c = C.get(cid)
    if not c or c.get("section") != 7: report.append(f"{cid}: not a section 7 answer: left alone"); continue
    dec, v, lv, at, note = str(d.get("decision") or ""), str(d.get("v") or ""), str(d.get("lv") or ""), str(d.get("at") or ""), str(d.get("note") or "").strip()
    if dec == "change": report.append(f"{cid} {v} (lines of {lv or 'before'}): CHANGE ASKED: {note}"); continue
    if dec != "approved": report.append(f"{cid}: decision '{dec}': left alone"); continue
    if v != c["version"]: report.append(f"{cid}: approved {v}, the claim is now {c['version']}: not recorded (he approved other lines)"); continue
    g = G.get(cid)
    if isinstance(g, dict) and g.get("version") == v and str(g.get("decision", "")).startswith("approved"): report.append(f"{cid} {v}: already approved in the gate"); continue
    if lv != LV: report.append(f"{cid}: approved {v} for lines of {lv or 'an earlier day'}, the page shows the lines of {LV}: not recorded"); continue
    rec = {"version": v, "decision": "approved", "date": at[:10] or None, "note": f"His approval as recorded on his to-do page at {at} (the plain lines of {LV}, checked blind twice)." + (f" His note: {note}" if note else "")}
    out.append((cid, rec)); report.append(f"{cid} {v}: APPROVED, recorded" if write else f"{cid} {v}: APPROVED, would be recorded")
if write and out:
    for cid, rec in out: G[cid] = rec
    json.dump(G, open("data/verification/senior-gate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in report: print(r)
print(f"{len(out)} approvals {'recorded' if write else 'to record (run again with --write)'}; {sum('CHANGE ASKED' in r for r in report)} changes asked")
