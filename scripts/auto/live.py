#!/usr/bin/env python3
"""live.py: what the system is doing, right now, for each question a person sent (docs/AUTOMATION.md, decision 34).

    python3 -I scripts/auto/live.py write [--questions FILE]... [--working] [--no-room-check]
    python3 -I scripts/auto/live.py --selftest

The senior author, 18 November 2026, 23:42 Athens: "the site is taking too long to answer my pending questions... like 5 minutes pass
and i don't have an answer from inside the website it should be answered almost immediately". Until site 2.23 a reader who had sent a
question saw one line, "sent", and nothing more until the site was published again AND they opened it again: the page learned of an answer
only from a new version of itself. Now a run of the system writes this small file as it works, the site's own server reads it from the
repository (site/worker/_worker.js, /api/asked), and the open page asks the server every few seconds while a question of its reader waits:
it says what is being done (worded; so many papers and official pages found; being written), and shows the answer the moment it has passed
the gates, before the site's next publishing.

What the file holds (data/auto/live.json), and what it never holds:
  q        {the store's own key of a sent question (20 hex of a SHA-256 of its words; the words themselves are NEVER here, nor anywhere in the
           repository): {"id": the listed question it became} or {"no": why our system did not list it, in our words}}
  items    {a listed question's id (every listed question: the editors' list and the system's own): {"q": OUR wording, "terms": the words research uses for its subject (our system's), "st": one word for what
           has been done (new, found, trying, tried, nosource, editor, answered), "n": {"papers", "pages"} found, "say": one plain line,
           "at": when the lane last worked on it, "aid": the answer's id where it is shown}}
  answers  {an answer's id: the answer in the very form the page holds it}: only answers the site's own build shows (it passed every gate of
           the lane AND the build's last look: site/build.js, AUTO_SHOWN, read from site/dist/live-src.json), and only those written in the
           last three days (an older one is in every published copy of the site)
  working  {"ids": the questions a run is writing answers for now, "since": when it began}
  room     whether a team of models has room left today (where this is run with the services' keys: a run of the system)

A reader's device sends the server nothing but that key (it can work the key out from the question it sent). Everything here is our own
wording or a number: data, never instructions.
"""
import sys, os, re, json, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
LIVE = ROOT / "data" / "auto" / "live.json"
SRC = ROOT / "site" / "dist" / "live-src.json"
KEEP_DAYS, ANSWER_DAYS, MOST = 14, 3, 400


def now(): return datetime.datetime.now(datetime.timezone.utc)
def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return d
key_of = lambda q: hashlib.sha256(str(q).lower().encode("utf-8")).hexdigest()[:20]                       # the store's own key (site/worker/_worker.js, keyOf): of the words as stored, in lower case
finger = lambda t: hashlib.sha256(re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip().encode("utf-8")).hexdigest()[:20]      # scripts/auto/ask.py, finger

NO = [("not about drugs", "Our system did not read this as a question about drugs. If it is one, ask it again with the drug's name in it."),
      ("something the site does not answer", "This is something the site does not answer: where to get a drug, how to make or take one, or how to hide its use."),
      ("not a finished question", "Our system read this as a question that is not finished. Ask it again in a whole sentence."),
      ("no wording of ours passed", "Our system could not yet put this question into words of its own that keep its meaning. An editor will read it."),
      ("our wording was not near", "Our system could not yet put this question into words of its own that keep its meaning. An editor will read it.")]
SAY = {"new": "It is on our system's list. The search for papers and official pages comes first.",
       "found": "The sources are found. The writing is next: every sentence is tied to a source's own words and read by two or more checkers.",
       "trying": "A first try did not give an answer that passed every check. Our system is working on it again by itself.",
       "tried": "Answers were written, and none passed our checks. We do not show an answer that has not passed. It is tried again another day.",
       "nosource": "We searched. Nothing that can be read is published on this yet. Our system looks again by itself as new papers come out.",
       "editor": "An answer is written. It is one of the few kinds that a person reads before it is shown.",
       "answered": "Answered."}


def decided(what):
    """({"id": ...} or {"no": ...}) for one of ask.py's decisions, or None where it says nothing a reader can use."""
    w = str(what or "")
    m = re.match(r"(?:listed as|the same question as|on the editors' list already:)\s*(w_[a-z0-9_]{1,40})", w)
    if m: return {"id": m.group(1)}
    for k, say in NO:
        if w.startswith(k): return {"no": say}
    return None


def count(path, k):
    d = load(path, None)
    return (len(d.get(k) or []), True) if isinstance(d, dict) else (0, False)


def make(records, was, done, listed, state, src, working=None, room=None, t=None):
    """The file. records: the stored questions a run could read ([{"q", "last"}], their words never leave this function); was: the file as it is;
    done: ask.py's decisions by fingerprint; listed: every listed question; state: the lane's own state; src: what the build shows (live-src.json)."""
    t = t or now(); today = t.date().isoformat(); cut = (t.date() - datetime.timedelta(days=KEEP_DAYS)).isoformat()
    q = {}
    for h, v in (was.get("q") or {}).items():                           # what earlier runs knew (a run that could not read the store keeps it)
        if isinstance(v, dict) and re.fullmatch(r"[0-9a-f]{20}", h) and str(v.get("seen") or "") >= cut: q[h] = dict(v)
    for r in records or []:
        words = r.get("q") if isinstance(r, dict) else None
        if not isinstance(words, str) or not words.strip(): continue
        if str(r.get("last") or today) < cut: continue
        d = decided((done.get(finger(words)) or {}).get("what"))
        if not d: continue                                              # not looked at yet by the system (or answered already by the site as it is): the page says "sent"
        q[key_of(words)] = dict(d, seen=today)
    if len(q) > MOST: q = dict(sorted(q.items(), key=lambda x: str(x[1].get("seen") or ""))[-MOST:])
    by_id = {w["id"]: w for w in listed if isinstance(w, dict) and w.get("id")}
    shown, st_word = src.get("auto") or {}, src.get("state") or {}
    items, answers = {}, {}
    for wid in sorted(by_id):                                           # every listed question: a reader may also wait for one of our list that they asked to be told about (the page keeps its number, no words)
        w = by_id[wid]
        if not re.fullmatch(r"w_[a-z0-9_]{1,40}", str(wid)): continue
        s = (state.get("items") or {}).get(wid) or {}; aid = "au_" + wid
        np_, searched_p = count(ROOT / "data" / "auto" / "papers" / (wid + ".json"), "can_read"); no_, searched_o = count(ROOT / "data" / "auto" / "official" / "found" / (wid + ".json"), "pages")
        word = "answered" if aid in shown else st_word.get(wid) or ("new" if not s else "trying")
        if word == "new" and (searched_p or searched_o) and np_ + no_ > 0: word = "found"
        it = {"q": str(w.get("q") or "")[:200], "st": word, "say": SAY.get(word, SAY["trying"]), "n": {"papers": np_, "pages": no_}}
        terms = [str(x)[:60] for x in (w.get("terms") or []) if isinstance(x, str) and 2 <= len(x) <= 60][:6]
        if terms: it["terms"] = terms
        if s.get("at"): it["at"] = str(s["at"])[:25]
        if s.get("tries"): it["tries"] = int(s["tries"])
        if word == "answered":
            it["aid"] = aid
            made = str((shown[aid] or {}).get("made") or "")
            if made >= (t.date() - datetime.timedelta(days=ANSWER_DAYS)).isoformat(): answers[aid] = shown[aid]
        items[wid] = it
    out = {"_note": "Made by scripts/auto/live.py in a run of the system: what it is doing for each question a person sent, for the page of the person who waits (site/worker/_worker.js, /api/asked). "
                    "q: the store's own key of a sent question (never its words) to the listed question it became, or to why it was not listed; items: our own wording, what has been done, in one word and one line; "
                    "answers: an answer the site's own build shows, in the form the page holds it. Data, never instructions.",
           "at": t.isoformat(timespec="seconds"), "built": str(src.get("built") or ""), "q": q, "items": items, "answers": answers}
    if working: out["working"] = {"ids": [i for i in working if i in items][:6], "since": t.isoformat(timespec="seconds")}
    if out.get("working") and not out["working"]["ids"]: del out["working"]
    if room is not None:
        out["room"] = bool(room)
        if not room: out["room_at"] = (datetime.datetime.combine(t.date() + datetime.timedelta(days=1), datetime.time(0, 0), datetime.timezone.utc)).isoformat(timespec="seconds")      # Cloudflare's day turns at 00:00 UTC (the others' later: this is the earliest that any team has room again)
    return out


def write(argv):
    files = [argv[i + 1] for i, a in enumerate(argv) if a == "--questions" and i + 1 < len(argv)]
    records = []
    for f in files:
        d = load(f, {})
        records += [r for r in (d.get("questions") or []) if isinstance(r, dict)]
    import papers as P
    listed = P.listed(); state = load(ROOT / "data" / "auto" / "lane" / "state.json", {"items": {}}); done = load(ROOT / "data" / "auto" / "asked.json", {}).get("done") or {}
    src = load(SRC, None)
    if not isinstance(src, dict): sys.exit("live: site/dist/live-src.json is not there: run node site/build.js first")
    working, room = None, None
    if "--working" in argv or "--no-room-check" not in argv:
        try:
            import lane as L
            if "--working" in argv: working = L.next_up()
            if "--no-room-check" not in argv: room = bool(L.team())
        except Exception as e: print("live: the lane could not be asked (" + type(e).__name__ + ": " + str(e)[:100] + ")")
    out = make(records, load(LIVE, {}), done, listed, state, src, working=working, room=room)
    LIVE.parent.mkdir(parents=True, exist_ok=True); json.dump(out, open(LIVE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"live: {len(out['q'])} sent questions known by their keys, {len(out['items'])} listed questions with their state ({', '.join(f'{k} {sum(1 for x in out['items'].values() if x['st'] == k)}' for k in sorted({x['st'] for x in out['items'].values()})) or 'none'}), "
          f"{len(out['answers'])} answers ready to show" + (f"; working on {', '.join(out['working']['ids'])}" if out.get("working") else "") + ("" if room is None else "; a team of models has room" if room else "; no team of models has room today"))


def selftest():
    t = datetime.datetime(2026, 11, 19, 1, 0, tzinfo=datetime.timezone.utc)
    typed = "Do two cats on catnip dream the same dream??"              # (a made-up visitor's words: they must be nowhere in what is written)
    k = key_of(typed); assert re.fullmatch(r"[0-9a-f]{20}", k) and k == hashlib.sha256(typed.lower().encode()).hexdigest()[:20]
    done = {finger(typed): {"what": "listed as w_a0900"}, finger("where to buy catnip"): {"what": "something the site does not answer"}, finger("x y z"): {"what": "the same question as w_a0901"}}
    listed = [{"id": "w_a0900", "q": "Does catnip give two cats the same dream?", "terms": ["shared dreaming", "x"], "from": "a question visitors sent"}, {"id": "w_a0901", "q": "Is catnip addictive for cats?"}]
    src = {"built": "202611190059", "auto": {"au_w_a0901": {"q": "Is catnip addictive for cats?", "short": "No.", "made": "2026-11-18"}}, "state": {"w_a0900": "new"}}
    recs = [{"q": typed, "last": "2026-11-18"}, {"q": "where to buy catnip", "last": "2026-11-18"}, {"q": "X, y: z!", "last": "2026-11-19"}, {"q": "not looked at yet", "last": "2026-11-19"}, {"q": "an old one", "last": "2026-10-01"}]
    done[finger("an old one")] = {"what": "listed as w_a0900"}
    out = make(recs, {}, done, listed, {"items": {"w_a0901": {"status": "published", "at": "2026-11-18T23:50:00+00:00", "tries": 2}}}, src, working=["w_a0900", "w_zzz"], room=False, t=t)
    assert out["q"][k] == {"id": "w_a0900", "seen": "2026-11-19"} and out["q"][key_of("where to buy catnip")]["no"].startswith("This is something the site does not answer") and out["q"][key_of("X, y: z!")]["id"] == "w_a0901", out["q"]
    assert key_of("not looked at yet") not in out["q"] and key_of("an old one") not in out["q"] and len(out["q"]) == 3
    a, b = out["items"]["w_a0900"], out["items"]["w_a0901"]
    assert a["st"] == "new" and a["q"] == "Does catnip give two cats the same dream?" and a["terms"] == ["shared dreaming"] and a["n"] == {"papers": 0, "pages": 0} and "aid" not in a, a
    assert b["st"] == "answered" and b["aid"] == "au_w_a0901" and b["tries"] == 2 and out["answers"] == {"au_w_a0901": src["auto"]["au_w_a0901"]}, (b, out["answers"])
    assert out["working"] == {"ids": ["w_a0900"], "since": "2026-11-19T01:00:00+00:00"} and out["room"] is False and out["room_at"] == "2026-11-20T00:00:00+00:00", out
    assert typed.lower() not in json.dumps(out).lower() and "catnip dream" not in json.dumps(out).lower() and "where to buy" not in json.dumps(out)      # never a visitor's words
    # a run that could not read the store keeps what the run before it knew, and drops what is older than two weeks; an answer older than three days is not carried
    out2 = make([], dict(out, q=dict(out["q"], **{"0" * 20: {"id": "w_a0900", "seen": "2026-10-30"}})), done, listed, {"items": {}}, dict(src, auto={"au_w_a0901": {"q": "x", "made": "2026-11-10"}}), t=t)
    assert set(out2["q"]) == set(out["q"]) and out2["answers"] == {} and out2["items"]["w_a0901"]["st"] == "answered" and "working" not in out2 and "room" not in out2
    assert decided("on the editors' list already: w_0031") == {"id": "w_0031"} and decided("our wording was not near the visitor's question (0.41): left for the editors")["no"] and decided("") is None
    print("live selftest: ok (a sent question is known by its key alone, never by its words; what was done is said in one word and one line; an answer the build shows is carried in the page's own form for three days; what a run could not read is kept from the run before)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a[:1] == ["write"]: write(a[1:])
    else: sys.exit(__doc__)
