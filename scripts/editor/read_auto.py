#!/usr/bin/env python3
"""read_auto.py: the editor's reading copy of what the machine lane wrote (data/auto/answers).

    python3 -I scripts/editor/read_auto.py [--lane N] [--ids au_w_0043,...] [--since YYYY-MM-DD] [--all]

For each answer: its question, what became of it and why, the gates' own words, each source (how it was read), and every
sentence beside the source's words it rests on, so that the two can be compared line by line. Nothing is changed.
"""
import sys, json, glob, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
arg = sys.argv[1:]
opt = lambda k, d=None: arg[arg.index(k) + 1] if k in arg else d
lane, ids, since = opt("--lane"), [x for x in (opt("--ids") or "").split(",") if x], opt("--since", "")
wrap = lambda t, ind: textwrap.fill(t, 150, initial_indent=ind, subsequent_indent=" " * len(ind))
n = {}
for f in sorted(glob.glob(str(ROOT / "data" / "auto" / "answers" / "au_*.json"))):
    a = json.load(open(f, encoding="utf-8"))
    if ids and a["id"] not in ids: continue
    if lane and str(a.get("lane")) != str(lane): continue
    if since and (a.get("made") or {}).get("on", "") < since: continue
    n[a["status"]] = n.get(a["status"], 0) + 1
    m = a.get("made") or {}
    print("=" * 150)
    print(f"{a['id']}  lane {a.get('lane')}  {a.get('kind', 'answer')}  {a['status'].upper()}  ({a.get('why')})  made {m.get('on')}  {m.get('neurons', '?')} neurons  from {m.get('from')}")
    print(wrap(a["question"], "Q: "))
    for k, v in (a.get("gates") or {}).items(): print(wrap(str(v), f"  gate {k}: "))
    for s in a.get("sources") or []:
        r = s.get("ref") or {}
        who = (r.get("author") or [{}])[0]
        print(wrap(f"[{s.get('tag')}] {s.get('read')}/{s.get('kind')}{'/people' if s.get('people') else ''} near {s.get('near')}: {who.get('literal') or who.get('family')} ({((r.get('issued') or {}).get('date-parts') or [[None]])[0][:1]}) {r.get('title', '')[:110]} | {r.get('DOI') or r.get('URL')}", "  source "))
        if "--all" in arg:
            for x in (s.get("findings") or []) + (s.get("limits") or []): print(wrap(f"{x.get('id')}: {x.get('text')}  <<{x.get('quote')}>>", "      "))
            for x in s.get("rows") or []: print(wrap(f"row: who={x.get('who')} | what={x.get('what')} | show={x.get('show')}  <<{x.get('quote')}>>", "      "))
    for p in a.get("parts") or []:
        print(wrap(p.get("text", ""), f"  {p['part']:>6}: "))
        if p.get("quote"): print(wrap("“" + p["quote"] + "”  (" + str(p.get("quote_ref") or p.get("source")) + ")", "          shown: "))
        if p.get("who_read"): print(wrap(p["who_read"], "          who, as the system's reader gave it: "))
        for r in p.get("rests_on") or []: print(wrap(f"{r.get('label')} {r.get('ref')} ({r.get('where')}): {r.get('quote')}", "          rests on: "))
    # (lane 11) what did not stand: the amounts the second reader refused, the lines that were dropped, the drafts that were written again
    for x in a.get("refused_rows") or []:
        print(wrap(f"{x.get('who')}; {x.get('what')}: “{x.get('quote')}”  ({x.get('source')}, {x.get('where')})", "  REFUSED amount: ")); print(wrap(str(x.get("said")), "          the second reader: "))
        if x.get("full") and x.get("full") != x.get("quote"): print(wrap(x["full"], "          the whole quote: "))
    for x in a.get("dropped") or []:
        print(wrap(x.get("text", ""), f"  DROPPED {x.get('part')} (try {x.get('try')}): ")); print(wrap(str(x.get("said")), f"          {x.get('by')}: "))
        for r in x.get("rests_on") or []: print(wrap(f"{r.get('label')} {r.get('ref')} ({r.get('where')}): {r.get('quote')}", "          rests on: "))
    for x in a.get("tries") or []:
        print(wrap(str(x.get("why")), f"  TRY {x.get('try')} did not stand: "))
        for p in x.get("parts") or []:
            print(wrap(p.get("text", ""), f"      {p.get('part'):>6} {'ok ' if p.get('ok') else 'NOT'}: "))
            if not p.get("ok"): print(wrap(str(p.get("said")), f"             {p.get('by')}: "))
            if "--all" in arg or not p.get("ok"):
                for r in p.get("rests_on") or []: print(wrap(f"{r.get('label')} {r.get('ref')} ({r.get('where')}): {r.get('quote')}", "             rests on: "))
    if "--all" in arg:                                                 # every source the reader was given, with what its gate threw away and why
        for l in a.get("looked") or []:
            print(wrap(f"{l.get('read')}/{l.get('kind')}: {str(l.get('title'))[:90]} | kept {l.get('kept')}, thrown {len(l.get('thrown') or [])}", "  looked at: "))
            for t in l.get("thrown") or []: print(wrap(f"{t.get('why')}  <<{t.get('quote') or ''}>>" + (f"  who={t.get('who')} | what={t.get('what')}" if t.get("who") or t.get("what") else f"  {t.get('text') or ''}"), "      thrown: "))
    if a.get("history"): print(wrap(json.dumps(a["history"][-1], ensure_ascii=False), "  before: "))
    print(wrap(f"complete: {a.get('complete')}; missing: {a.get('missing')}; wanted: {len(a.get('wanted') or [])}; person: {a.get('person')}", "  "))
print("=" * 150); print("in all:", n or "nothing")
