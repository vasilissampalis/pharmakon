#!/usr/bin/env python3
"""label_rows.py: the editor's verdicts on the ROWS of the answers about amounts that the system wrote, kept as an exam of that
task (data/auto/exam/lane-rows.json; docs/AUTOMATION.md, decisions 11 and 25). The sentences of the other answers are in
lane-sentences.json (scripts/editor/label_auto.py).

    python3 -I scripts/editor/label_rows.py show [--ids au_w_0046,...] [--at COMMIT]    (every row not judged yet)
    python3 -I scripts/editor/label_rows.py add FILE.json [--at COMMIT] [--again]       ({"au_w_0046": {"row1": [1, ""], "row13": [0, "what is wrong"]}})
    python3 -I scripts/editor/label_rows.py rate                                         (for each lane: of the rows it kept, how many are not good)
    (--trial with show or add: the records of trial questions, data/auto/trial/answers: questions that are not on the site's list)
    python3 -I scripts/editor/label_rows.py --selftest

A row is one amount as the site would show it: who it is for, what kind of amount it is, and the source's own words (15 at
most). Good (1): all three are true to the source, the amount is of the kind the question asks for, and the row holds nothing
that is never shown (an amount for each kilogram of body weight, an amount for pregnancy or children, a time between uses, an
amount that harmed, a product's amount, an amount worked out from another). Not good (0): any of that fails; the verdict names
it. A row that is true and only says again what another row says is good, with a note. The editor reads each row against the
record's longer quote and, where that does not settle it, against the source itself.

--at COMMIT: the records as they stood at that commit (the lane writes an answer again and the file then holds the newer one).
A verdict is never changed silently: a second verdict for the same row needs --again, and the first is kept under "before".
"""
import sys, json, hashlib, pathlib, datetime, subprocess, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "data" / "auto" / "answers"
EXAM = ROOT / "data" / "auto" / "exam" / "lane-rows.json"
NOTE = ("The exam of the lane's rows of amounts (decisions 11 and 25; docs/AUTOMATION.md): every row of an answer about amounts that the system wrote and the editor has read, with the editor's verdict. "
        "Good: who it is for, what kind of amount it is and the shown words are true to the source, the amount is of the kind the question asks for, and the row holds nothing that is never shown. "
        "It grows with every batch the editor reads (scripts/editor/label_rows.py), and says of each version of the lane how many of the rows it kept were not good.")
BY = "the AI co-editor (Claude Fable 5.2)"


def key(a, p):
    return f"{a['id']}#L{a.get('lane')}.{p['part']}~{hashlib.sha1('|'.join([p.get('who') or '', p.get('what') or '', p.get('quote') or '']).encode('utf-8')).hexdigest()[:6]}"


def rows(a):
    return [p for p in a.get("parts") or [] if str(p.get("part", "")).startswith("row")] if a.get("kind") == "amounts" else []


def load(exam=None):
    try: return json.load(open(exam or EXAM, encoding="utf-8"))
    except (OSError, ValueError): return {"_note": NOTE, "good": 0, "bad": 0, "items": []}


def answers(at=None, folder=None):
    """{id: record}: from the folder, or as the records stood at a commit."""
    out = {}
    if at:
        names = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "--name-only", at, "data/auto/answers/"], capture_output=True, text=True).stdout.split()
        for n in names:
            if not n.endswith(".json"): continue
            try: a = json.loads(subprocess.run(["git", "-C", str(ROOT), "show", f"{at}:{n}"], capture_output=True, text=True).stdout)
            except ValueError: continue
            if isinstance(a, dict) and a.get("id"): out[a["id"]] = a
        return out
    for f in sorted((folder or ANSWERS).glob("au_*.json")):
        try: a = json.load(open(f, encoding="utf-8"))
        except ValueError: continue
        out[a["id"]] = a
    return out


def waiting(doc, recs, ids=None):
    have = {i["id"] for i in doc["items"]}
    return [(a, p) for aid, a in recs.items() if not ids or aid in ids for p in rows(a) if key(a, p) not in have]


def add(verdicts, doc, recs, today=None, by=BY, again=False):
    """Returns (how many were written, [what was refused and why])."""
    done, refused = 0, []; at = {i["id"]: n for n, i in enumerate(doc["items"])}
    for aid, parts in verdicts.items():
        a = recs.get(aid)
        if not a or a.get("kind") != "amounts": refused.append(f"{aid}: no such answer about amounts"); continue
        here = {p["part"]: p for p in rows(a)}
        for part, v in parts.items():
            if part not in here: refused.append(f"{aid}#{part}: no such row"); continue
            if not (isinstance(v, (list, tuple)) and len(v) == 2 and v[0] in (0, 1, True, False) and isinstance(v[1], str)): refused.append(f"{aid}#{part}: a verdict is [1 or 0, what is wrong (or a note)]"); continue
            good, what = bool(v[0]), v[1].strip()
            if not good and len(what) < 12: refused.append(f"{aid}#{part}: a row that is not good needs what is wrong with it"); continue
            p = here[part]; k = key(a, p)
            item = {"id": k, "lane": a.get("lane") or 1, "question": a["question"], "who": p.get("who"), "what": p.get("what"), "quote": p.get("quote"), "full": ((p.get("rests_on") or [{}])[0]).get("quote") or "",
                    "where": ((p.get("rests_on") or [{}])[0]).get("where") or "", "source": p.get("source"), "read": p.get("read"), "good": good, "said": what, "read_on": today or datetime.date.today().isoformat(), "read_by": by}
            if k in at:
                old = doc["items"][at[k]]
                if (old["good"], old["said"]) == (good, what): continue
                if not again: refused.append(f"{k}: judged already ({'good' if old['good'] else 'not good'}); a second verdict needs --again"); continue
                item["before"] = (old.get("before") or []) + [{x: old[x] for x in ("good", "said", "read_on", "read_by")}]; doc["items"][at[k]] = item
            else: at[k] = len(doc["items"]); doc["items"].append(item)
            done += 1
    doc["_note"] = NOTE; doc["good"] = sum(i["good"] for i in doc["items"]); doc["bad"] = sum(not i["good"] for i in doc["items"])
    return done, refused


def rate(doc):
    """{lane: [rows read, rows not good]}"""
    out = {}
    for i in doc["items"]: g = out.setdefault(i["lane"], [0, 0]); g[0] += 1; g[1] += not i["good"]
    return out


def selftest():
    recs = {"au_t_1": {"id": "au_t_1", "lane": 12, "kind": "amounts", "question": "How much?", "parts": [
                {"part": "short", "text": "Amounts ...", "fixed": True},
                {"part": "row1", "who": "Adults", "what": "a daily amount", "quote": "up to 400 mg a day", "source": "s1", "read": "page", "rests_on": [{"quote": "up to 400 mg a day for adults", "where": "FAQ"}]},
                {"part": "row2", "who": "Adults", "what": "a daily amount", "quote": "6 mg kg(-1) body weight", "source": "s2", "read": "summary", "rests_on": [{"quote": "6 mg kg(-1) body weight day(-1)", "where": "Summary"}]}]},
            "au_t_2": {"id": "au_t_2", "lane": 12, "kind": "answer", "question": "Is it so?", "parts": [{"part": "row1", "who": "x", "what": "y", "quote": "z"}]}}
    doc = {"items": []}
    assert [(a["id"], p["part"]) for a, p in waiting(doc, recs)] == [("au_t_1", "row1"), ("au_t_1", "row2")]                               # only the rows of answers about amounts
    n, bad = add({"au_t_1": {"row1": [1, ""], "row2": [0, "an amount for each kilogram of body weight"], "row9": [1, ""], "short": [1, ""]}, "au_t_2": {"row1": [1, ""]}}, doc, recs, today="2026-11-17")
    assert n == 2 and len(bad) == 3 and doc["good"] == 1 and doc["bad"] == 1 and doc["items"][1]["full"].startswith("6 mg kg(-1)") and doc["items"][0]["id"].startswith("au_t_1#L12.row1~"), (n, bad)
    assert add({"au_t_1": {"row2": [0, "too short"]}}, doc, recs)[1] and not waiting(doc, recs) and add({"au_t_1": {"row1": [1, ""]}}, doc, recs) == (0, [])
    n, bad = add({"au_t_1": {"row1": [0, "the amount is for another group"]}}, doc, recs); assert n == 0 and "--again" in bad[0]              # never changed silently
    n, bad = add({"au_t_1": {"row1": [0, "the amount is for another group"]}}, doc, recs, again=True); assert n == 1 and doc["items"][0]["before"][0]["good"] is True and doc["bad"] == 2
    recs["au_t_1"]["lane"] = 13; recs["au_t_1"]["parts"][1]["who"] = "Healthy adults"                                                      # the lane wrote the answer again: its rows are new items
    assert len(waiting(doc, recs)) == 2 and add({"au_t_1": {"row1": [1, "says again what another row says"]}}, doc, recs)[0] == 1 and rate(doc) == {12: [2, 2], 13: [1, 0]}, rate(doc)
    print("label_rows selftest: ok (only the rows of answers about amounts are judged; a 'not good' names what is wrong; a verdict is never changed silently; a row the lane wrote again is a new item)")


if __name__ == "__main__":
    a = sys.argv[1:]; at = a[a.index("--at") + 1] if "--at" in a else None
    if "--trial" in a: ANSWERS = ROOT / "data" / "auto" / "trial" / "answers"
    if "--selftest" in a: selftest()
    elif a and a[0] == "show":
        ids = set((a[a.index("--ids") + 1]).split(",")) if "--ids" in a else None; doc = load(); w = waiting(doc, answers(at, ANSWERS), ids); last = None
        wrap = lambda t, ind: textwrap.fill(t, 150, initial_indent=ind, subsequent_indent=" " * len(ind))
        for rec, p in w:
            if rec["id"] != last: last = rec["id"]; print("=" * 150); print(f"{rec['id']}  lane {rec.get('lane')}  {rec.get('status')}"); print(wrap(rec["question"], "Q: "))
            print(wrap(f"{p.get('who')}; {p.get('what')}: “{p.get('quote')}”  ({p.get('source')}, {p.get('read')})", f"  {p['part']:>6}: "))
            for r in p.get("rests_on") or []: print(wrap(f"({r.get('where')}) {r.get('quote')}", "          rests on: "))
        print("=" * 150); print(f"{len(w)} rows wait for a verdict; judged so far: {doc['good']} good, {doc['bad']} not good")
    elif len(a) >= 2 and a[0] == "add":
        doc = load(); n, bad = add(json.load(open(a[1], encoding="utf-8")), doc, answers(at, ANSWERS), again="--again" in a)
        if n: json.dump(doc, open(EXAM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for b in bad: print("refused:", b)
        print(f"{n} verdicts written; the exam of rows now: {doc['good']} good, {doc['bad']} not good")
        sys.exit(1 if bad else 0)
    elif a and a[0] == "rate":
        for l, (n, b) in sorted(rate(load()).items()): print(f"lane {l}: of {n} rows of amounts it kept, {b} are not good")
    else: sys.exit(__doc__)
