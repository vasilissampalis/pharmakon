#!/usr/bin/env python3
"""label_auto.py: the editor's verdicts on the sentences the system wrote, kept as an exam of the lane's own task
(data/auto/exam/lane-sentences.json; docs/AUTOMATION.md, decision 23).

    python3 -I scripts/editor/label_auto.py show [--ids au_w_0044,...]     (every sentence not judged yet, beside the words it rests on)
    python3 -I scripts/editor/label_auto.py add FILE.json                    (the verdicts: {"au_w_0001": {"short": [0, "what it says that its source does not"], "how1": [1, ""]}})
    python3 -I scripts/editor/label_auto.py rate                             (for each lane: of the sentences it kept, how many are not good; of the ones it did not keep, how many were good)
    python3 -I scripts/editor/label_auto.py --selftest

The standard is the blind checkers' own. Good (1): the sentence says only what the words it rests on say. Not good (0): it
says something they do not carry, however small (a word of how often or how sure, a cause where the source reports, a
hedge left out, a thing from elsewhere); the verdict then names it. Leaving something out is not wrong. The words a
sentence rests on are the quotes its record keeps.

What is judged: the sentences the models wrote. Not the lines the code writes (fixed), and not the rows of an answer about
amounts (who received an amount is in the passage around the quote, not in the quote: those are read against the source
itself). A sentence is kept with the words it rested on when it was judged: if the system rewrites the answer later, the
new sentence is a new item and the old one stays. A verdict is never changed silently: a second verdict for the same
sentence is refused unless --again is given, and then the first is kept under "before".
"""
import sys, json, hashlib, pathlib, datetime, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "data" / "auto" / "answers"
EXAM = ROOT / "data" / "auto" / "exam" / "lane-sentences.json"
NOTE = ("The exam of the lane's own sentences (decision 23; docs/AUTOMATION.md): every sentence the system wrote that the editor has read against the words it rests on, with the editor's verdict by the blind checkers' standard "
        "(good: the sentence says only what those words say; not good: it says something they do not carry, however small: a word of how often or how sure, a cause where the source reports, a hedge left out, a thing from elsewhere). "
        "Leaving something out is not counted as wrong. A checker of our own sits this exam beside the quiz cards' exam (data/auto/exam/cards.json), because this is the lane's real task. "
        "It grows with every batch the editor reads (scripts/editor/label_auto.py). The words a sentence rests on are the quotes the record keeps (the lane itself also sees the passage around them); 'passages' gives each quote with its source's name and its place, "
        "as the lane's own second reader sees them: a sentence may say 'Health Canada says' or 'a 2024 review' only because its source is named there.")
BY = "the AI co-editor (Claude Fable 5.2)"


def key(aid, part, text):
    return f"{aid}#{part}~{hashlib.sha1(text.encode('utf-8')).hexdigest()[:6]}"


def source_name(a, ref):
    """A source's name as the lane's second reader sees it beside a passage (lane.py: paper_name): a body and its page, or a paper's title and year."""
    s = next((s for s in a.get("sources") or [] if (s.get("ref") or {}).get("id") == ref), None)
    if not s: return ""
    return f"{s.get('name')}: {s.get('title')}" if s.get("read") == "page" or s.get("name") else f"{s.get('title')} ({s.get('year')})"


def all_parts(a):
    """Every sentence a model wrote for an answer, the ones the lane kept and (lane 11) the ones it did not: [(name, the part, kept?, what the lane said of it)].
    The kept ones are the answer's own parts. The others are the sentences of each draft that was written again ("t1.short": the
    short answer of try 1) and the lines that were dropped ("x2.how3": line 3, dropped at try 2). The same sentence over the same
    words is listed once: where a draft's sentence went on into the answer it is the answer's part."""
    out, seen = [], set()
    def add(name, p, kept, said):
        quotes = tuple(r["quote"] for r in p.get("rests_on") or [] if r.get("quote"))
        if p.get("fixed") or not p.get("text") or not quotes or (p["text"], quotes) in seen: return
        seen.add((p["text"], quotes)); out.append((name, p, kept, said))
    for p in a.get("parts") or []: add(p["part"], p, True, "kept")
    for t in a.get("tries") or []:
        for p in t.get("parts") or []: add(f"t{t.get('try')}.{p.get('part')}", p, False, ("accepted, in a draft that was written again" if p.get("ok") else f"refused by {p.get('by')}: {p.get('said')}"))
    for p in a.get("dropped") or []: add(f"x{p.get('try')}.{p.get('part')}", p, False, f"dropped by {p.get('by')}: {p.get('said')}")
    return out


def judged_parts(a):
    """The sentences of an answer that are judged here: [(part, text, [the quotes it rests on], [each quote with its source's name and its place])]."""
    if a.get("kind") == "amounts": return []
    return [(name, p["text"], [r["quote"] for r in p.get("rests_on") or [] if r.get("quote")],
             [{"source": source_name(a, r.get("ref")), "where": r.get("where") or "", "quote": r["quote"]} for r in p.get("rests_on") or [] if r.get("quote")]) for name, p, _, _ in all_parts(a)]


def lane_said(a):
    """{part's name: (did the lane keep it, what the lane said of it)}"""
    return {name: (kept, said) for name, _, kept, said in all_parts(a)} if a.get("kind") != "amounts" else {}


def load(exam=None):
    try: return json.load(open(exam or EXAM, encoding="utf-8"))
    except (OSError, ValueError): return {"_note": NOTE, "good": 0, "bad": 0, "items": []}


def answers(folder=None):
    out = {}
    for f in sorted((folder or ANSWERS).glob("au_*.json")):
        try: a = json.load(open(f, encoding="utf-8"))
        except ValueError: continue
        out[a["id"]] = a
    return out


def waiting(doc, recs, ids=None):
    have = {i["id"] for i in doc["items"]}
    return [(a, part, text, quotes) for aid, a in recs.items() if not ids or aid in ids for part, text, quotes, _ in judged_parts(a) if key(aid, part, text) not in have]


def add(verdicts, doc, recs, today=None, by=BY, again=False):
    """Returns (how many were written, [what was refused and why])."""
    done, refused = 0, []; at = {i["id"]: n for n, i in enumerate(doc["items"])}
    for aid, parts in verdicts.items():
        a = recs.get(aid)
        if not a: refused.append(f"{aid}: no such answer"); continue
        here = {part: (text, quotes, passages) for part, text, quotes, passages in judged_parts(a)}; said = lane_said(a)
        for part, v in parts.items():
            if part not in here: refused.append(f"{aid}#{part}: not a sentence that is judged here (a line the code writes, a row of amounts, or no such part)"); continue
            if not (isinstance(v, (list, tuple)) and len(v) == 2 and v[0] in (0, 1, True, False) and isinstance(v[1], str)): refused.append(f"{aid}#{part}: a verdict is [1 or 0, what is wrong]"); continue
            good, what = bool(v[0]), v[1].strip()
            if not good and len(what) < 12: refused.append(f"{aid}#{part}: a sentence that is not good needs what it says that its source does not"); continue
            text, quotes, passages = here[part]; k = key(aid, part, text)
            item = {"id": k, "lane": a.get("lane") or 1, "question": a["question"], "sentence": text, "rests_on": quotes, "passages": passages, "good": good, "what": what,
                    "read_on": today or datetime.date.today().isoformat(), "read_by": by}
            if not said[part][0]: item["kept"] = False; item["lane_said"] = said[part][1][:300]         # (lane 11) a sentence the lane itself did not keep: judged all the same (was it rightly refused?)
            if k in at:
                old = doc["items"][at[k]]
                if (old["good"], old["what"]) == (good, what): continue
                if not again: refused.append(f"{k}: judged already ({'good' if old['good'] else 'not good'}); a second verdict needs --again"); continue
                item["before"] = (old.get("before") or []) + [{x: old[x] for x in ("good", "what", "read_on", "read_by")}]; doc["items"][at[k]] = item
            else: at[k] = len(doc["items"]); doc["items"].append(item)
            done += 1
    doc["_note"] = NOTE; doc["good"] = sum(i["good"] for i in doc["items"]); doc["bad"] = sum(not i["good"] for i in doc["items"])
    return done, refused


def by_lane(doc):
    out = {}
    for i in doc["items"]: g = out.setdefault(i["lane"], [0, 0]); g[0 if i["good"] else 1] += 1
    return "; ".join(f"lane {l}: {g} good, {b} not good" for l, (g, b) in sorted(out.items()))


def rate(doc):
    """What the lane as a whole did with the sentences its models wrote, by the editor's verdicts: for each lane, of the sentences
    it KEPT how many are not good (what a reader would have been shown wrong, before the editor's reading), and of the ones it
    did NOT keep how many were good (what it lost). Sentences it did not keep are on file from lane 11 on."""
    out = {}
    for i in doc["items"]:
        g = out.setdefault(i["lane"], {"kept": 0, "kept_bad": 0, "not_kept": 0, "not_kept_good": 0})
        if i.get("kept", True): g["kept"] += 1; g["kept_bad"] += not i["good"]
        else: g["not_kept"] += 1; g["not_kept_good"] += bool(i["good"])
    return out


def selftest():
    recs = {"au_t_1": {"id": "au_t_1", "lane": 9, "question": "Is it so?", "parts": [
                {"part": "short", "text": "It often is so.", "rests_on": [{"quote": "It can be so."}]},
                {"part": "but", "text": "The evidence is thin.", "fixed": True, "rests_on": []},
                {"part": "how1", "text": "One study found it.", "rests_on": [{"quote": "We found it."}, {"quote": ""}]},
                {"part": "how2", "text": "It rests on nothing.", "rests_on": []}]},
            "au_t_2": {"id": "au_t_2", "kind": "amounts", "question": "How much?", "parts": [{"part": "row1", "text": "12 people; a dose.", "rests_on": [{"quote": "a dose of 10 mg"}]}]}}
    doc = {"items": []}
    recs["au_t_1"]["sources"] = [{"ref": {"id": "r1"}, "read": "page", "name": "Health Canada", "title": "Ketamine"}, {"ref": {"id": "r2"}, "title": "A review", "year": 2024}]
    recs["au_t_1"]["parts"][0]["rests_on"][0].update(ref="r1", where="Risks"); recs["au_t_1"]["parts"][2]["rests_on"][0].update(ref="r2", where="Abstract")
    assert judged_parts(recs["au_t_1"])[0][3] == [{"source": "Health Canada: Ketamine", "where": "Risks", "quote": "It can be so."}] and judged_parts(recs["au_t_1"])[1][3][0]["source"] == "A review (2024)"
    assert [(p, t) for _, p, t, _ in waiting(doc, recs)] == [("short", "It often is so."), ("how1", "One study found it.")]            # not the code's line, not a sentence that rests on nothing, not a row of amounts
    n, bad = add({"au_t_1": {"short": [0, "'often': the source says 'can be'"], "how1": [1, ""], "but": [1, ""], "how2": [1, ""]}, "au_t_2": {"row1": [1, ""]}, "au_t_9": {"short": [1, ""]}}, doc, recs, today="2026-11-16")
    assert n == 2 and len(bad) == 4 and doc["good"] == 1 and doc["bad"] == 1 and doc["items"][1]["rests_on"] == ["We found it."], (n, bad)
    assert add({"au_t_1": {"short": [0, "too short"]}}, doc, recs)[1] and not waiting(doc, recs)                                          # a "not good" names what is wrong; nothing waits now
    assert add({"au_t_1": {"short": [0, "'often': the source says 'can be'"]}}, doc, recs) == (0, [])                                     # the same verdict again changes nothing
    n, bad = add({"au_t_1": {"short": [1, ""]}}, doc, recs); assert n == 0 and "--again" in bad[0] and not doc["items"][0]["good"]          # never changed silently
    n, bad = add({"au_t_1": {"short": [1, ""]}}, doc, recs, today="2026-11-17", again=True)
    assert n == 1 and doc["items"][0]["good"] and doc["items"][0]["before"][0]["what"].startswith("'often'") and doc["good"] == 2
    recs["au_t_1"]["parts"][0]["text"] = "It can be so."                                                                                 # the system rewrote its answer: a new item, the old one stays
    assert [p for _, p, _, _ in waiting(doc, recs)] == ["short"] and add({"au_t_1": {"short": [1, ""]}}, doc, recs)[0] == 1 and len(doc["items"]) == 3
    assert by_lane(doc) == "lane 9: 3 good, 0 not good"
    # (lane 11) the sentences the lane did not keep are judged too: those of a draft that was written again, and the lines that were dropped
    q = lambda t: [{"quote": t, "ref": "r1", "where": "Risks"}]
    recs["au_t_3"] = {"id": "au_t_3", "lane": 11, "question": "Is it so?", "sources": recs["au_t_1"]["sources"],
                      "parts": [{"part": "short", "text": "It can be so.", "rests_on": q("It can be so.")}, {"part": "how1", "text": "One page says it can be so.", "rests_on": q("It can be so.")}],
                      "tries": [{"try": 1, "why": "the short answer or the But was not accepted: written again", "parts": [
                          {"part": "short", "text": "It always is so.", "rests_on": q("It can be so."), "ok": False, "by": "the second reader", "said": "always is not in the passage"},
                          {"part": "how1", "text": "One page says it can be so.", "rests_on": q("It can be so."), "ok": True}]}],
                      "dropped": [{"try": 2, "part": "how2", "text": "It is so for everyone.", "rests_on": q("It can be so."), "by": "our own checker", "said": "our own checker does not find it (0.02)"}]}
    assert [p for _, p, _, _ in waiting(doc, recs, {"au_t_3"})] == ["short", "how1", "t1.short", "x2.how2"]                                 # the line of try 1 that went on into the answer is listed once, as the answer's
    n, bad = add({"au_t_3": {"short": [1, ""], "how1": [1, ""], "t1.short": [0, "'always': the source says 'can be'"], "x2.how2": [0, "'for everyone' is not in the source"]}}, doc, recs, today="2026-11-17")
    kept_no = [i for i in doc["items"] if i.get("kept") is False]
    assert n == 4 and not bad and [i["lane_said"] for i in kept_no] == ["refused by the second reader: always is not in the passage", "dropped by our own checker: our own checker does not find it (0.02)"], (n, bad, kept_no)
    assert rate(doc)[11] == {"kept": 2, "kept_bad": 0, "not_kept": 2, "not_kept_good": 0} and rate(doc)[9] == {"kept": 3, "kept_bad": 0, "not_kept": 0, "not_kept_good": 0}, rate(doc)
    print("label_auto selftest: ok (only the sentences the models wrote are judged, the ones the lane kept and the ones it did not; a 'not good' names what is wrong; a verdict is never changed silently; a rewritten sentence is a new item)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a and a[0] == "show":
        ids = set((a[a.index("--ids") + 1]).split(",")) if "--ids" in a else None; doc = load(); w = waiting(doc, answers(), ids); last = None
        wrap = lambda t, ind: textwrap.fill(t, 150, initial_indent=ind, subsequent_indent=" " * len(ind))
        for rec, part, text, quotes in w:
            if rec["id"] != last: last = rec["id"]; said = lane_said(rec); print("=" * 150); print(f"{rec['id']}  lane {rec.get('lane') or 1}  {rec.get('status')}  ({rec.get('why')})"); print(wrap(rec["question"], "Q: "))
            print(wrap(text, f"  {part:>8}: "))
            if not said[part][0]: print(wrap(said[part][1], "            the lane: "))
            for q in quotes: print(wrap(q, "            rests on: "))
        print("=" * 150); print(f"{len(w)} sentences wait for a verdict; judged so far: {doc['good']} good, {doc['bad']} not good ({by_lane(doc) or 'none'})")
    elif len(a) >= 2 and a[0] == "add":
        doc = load(); n, bad = add(json.load(open(a[1], encoding="utf-8")), doc, answers(), again="--again" in a)
        if n: json.dump(doc, open(EXAM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for b in bad: print("refused:", b)
        print(f"{n} verdicts written; the exam now: {doc['good']} good, {doc['bad']} not good ({by_lane(doc)})")
        sys.exit(1 if bad else 0)
    elif a and a[0] == "rate":
        for l, g in sorted(rate(load()).items()):
            print(f"lane {l}: of {g['kept']} sentences it kept, {g['kept_bad']} are not good" + (f"; of {g['not_kept']} it did not keep, {g['not_kept_good']} were good" if g["not_kept"] else "; the ones it did not keep are not on file (kept from lane 11 on)"))
    else: sys.exit(__doc__)
