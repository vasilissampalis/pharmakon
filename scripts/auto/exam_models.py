#!/usr/bin/env python3
"""exam_models.py: a model sits the exam as the lane's checker (docs/AUTOMATION.md; scripts/auto/exam.py).

    python3 -I scripts/auto/exam_models.py requests      (data/auto/requests/exam-*.json: {"models": [...], "good": 62, "exam": "cards" | "lane" | "lines" | "both" | "all"})

The exam's items are our own blind checks: a Myth or fact? card beside the checked lines it was written from, and whether a
blind checker who wrote none of it found that the card says only what the lines say. The model is asked the lane's own
question, in the lane's own words (lane.CHECKER_SYS): do the passages support the sentence? Its yes lets the card through.

Every call costs some of the day's free allowance, so a model sits a part of the exam: every one of the wrong cards (the
ones a checker must catch) and a fixed draw of the good ones (seed 20261115; "good" in the request says how many). From
the two shares the result gives what the whole exam would give: of everything the model would let through, how much is
wrong (exam.py's bar: 1 in 50; the senior author's goal: 1 in 1,000), and how many good cards it would stop.
Writes data/auto/exam/model-<name>.json. The exam is small: it can show that a checker is not good enough, never that it is.

A second exam (16 November 2026), "lane": the sentences the system itself wrote, each beside the words it rests on, with the
editor's verdict (data/auto/exam/lane-sentences.json; scripts/editor/label_auto.py). This is the lane's real task, asked in
the same words. It is sat first, whole (it is small), and written to model-<name>-lane.json.

A third exam, "lines" (scripts/auto/exam_lines.py): plain lines beside the checked claims they were written from, with the
blind checkers' verdicts: every line a checker changed for what it said, and a fixed draw of twice as many good ones.
The claim's fields are the passages. Written to model-<name>-lines.json. ("both": cards and lane; "all": the three.)
"""
import sys, time, re, json, random, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import llm, lane, exam

EXAM = ROOT / "data" / "auto" / "exam"


def prompt(item):
    L = item["lines"]; lines = [L.get("short") or "", ("But " + L["but"]) if L.get("but") else ""] + list(L.get("how") or [])
    ps = "\n".join("   PASSAGE: " + t for t in lines if t)
    c = item["card"]
    sent = c["statement"] if item.get("plain") else ("It is a fact that: " if c["answer"] else "It is a myth (it is not true) that: ") + c["statement"] + (" Because: " + c["why"] if c.get("why") else "")
    return ("For the SENTENCE below, decide whether its PASSAGES support it. Supported means ALL of this: everything the sentence says is stated in its passages; "
            "it is about the same people, animals or setting; every number is the same; it is not stronger or more certain than the passages; it does not say one thing causes another "
            "where the passages only report a link; it does not turn what one study found into a general fact. If any part of the sentence is not in the passages, it is not supported.\n\n"
            f"1. SENTENCE: {sent}\n{ps}\n\n"
            'JSON only, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}]}')


def lane_cards(file=None):
    """The lane's own sentences in the shape of the exam's cards: the sentence as it stands, the words it rests on as its passages."""
    try: items = json.load(open(file or EXAM / "lane-sentences.json", encoding="utf-8"))["items"]
    except (OSError, ValueError): return []
    named = lambda i: [f"({x['source']}; {x['where']}) {x['quote']}" if x.get("source") else x["quote"] for x in i["passages"]] if i.get("passages") else list(i["rests_on"])     # (as in the lane's own question: each passage with its source's name and its place)
    return [{"id": i["id"], "good": i["good"], "what": i.get("what"), "plain": True, "lines": {"short": "", "but": "", "how": named(i)}, "card": {"answer": True, "statement": i["sentence"], "why": ""}} for i in items]


def lines_cards(file=None):
    """The exam of plain lines in the shape of the exam's cards: the line as it stands, the checked claim's fields as its passages."""
    try: d = json.load(open(file or EXAM / "lines.json", encoding="utf-8"))
    except (OSError, ValueError): return []
    return [{"id": i["id"], "good": i["good"], "what": i.get("what"), "plain": True, "lines": {"short": "", "but": "", "how": [f"({label}) {text}" for label, text in d["claims"][i["claim"]]]}, "card": {"answer": True, "statement": i["line"], "why": ""}} for i in d["items"]]


def slug(model): return re.sub(r"[^a-z0-9.-]+", "-", model.lower()).strip("-")


KEEP = 700            # neurons of the day's allowance the exam leaves for the site's own work (a visitor's question must still be listed)


def framed(item):
    """A card as one sentence (as in prompt()), the plain words its pieces must cover, and its lines."""
    L = item["lines"]; lines = [t for t in [L.get("short") or "", ("But " + L["but"]) if L.get("but") else ""] + list(L.get("how") or []) if t]
    c = item["card"]
    sent = ("It is a fact that: " if c["answer"] else "It is a myth (it is not true) that: ") + c["statement"] + (" Because: " + c["why"] if c.get("why") else "")
    return sent, c["statement"] + " " + re.sub(r"^(?:true|false|myth|fact)[.!:]?\s+", "", c.get("why") or "", flags=re.I), lines


def sit(model, n_good, cards=None, chat=None, left=None, file=None, until=None, how=None, keep=None, most=None, effort=None):
    """The model's verdict on every wrong card and a fixed draw of the good ones. It goes on where an earlier sitting with
    the same room stopped (its cards are kept in the result), stops when the day's allowance is down to KEEP, and writes
    as it goes, so that a sitting cut short by the allowance or by the machine's time limit is not lost."""
    items = cards or json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]
    bad = [i for i in items if not i["good"]]; good = [i for i in items if i["good"]]
    rnd = random.Random(20261115); draw = rnd.sample(good, min(n_good, len(good)))
    pieces = how == "pieces"                                                                               # (16 November: the reader copies the passage's words for every piece of the card, and the code gives the verdict: lane.pieces_verdict)
    bare = how == "plain"                                                                                  # (16 November: one verdict, on the card's true part as it stands. The frame "It is a fact that:" made strict readers refuse good cards for the frame's own sureness)
    marks = how == "marks"                                                                                 # (16 November: five small questions, one for each kind of fault our checkers find, and the code gives the verdict: lane.marks_verdict)
    room = lane.room_for(model, 700 if pieces else 420 if marks else 220) if "gpt-oss" in model or not model.startswith("groq:") else 2000          # (a model that reasons first needs room: on 15 November gpt-oss-120b gave no verdict in 220, nor in 700)
    svc = llm.service_of(model)[0]                                                                             # (a service that counts calls: one card is one call, and five calls are kept)
    groq = model.startswith("groq:"); keep = 5 if svc else max(2000 if groq else KEEP, keep) if isinstance(keep, (int, float)) else 30000 if groq else KEEP      # (Groq counts a day in tokens for each model: 30,000 are left for the lane unless the request says the lane does not run today)
    # how hard a reasoning model at Groq thinks: the request's word, else what llm.chat_groq asks by itself (the larger gpt-oss: medium; the smaller: low; qwen3: none)
    plain_effort = ("low" if model.endswith("gpt-oss-20b") else "medium") if "gpt-oss" in model else "none" if "qwen3" in model else ""
    effort = effort if effort in ("low", "medium", "high") and groq and "gpt-oss" in model else plain_effort
    if groq and effort != plain_effort: llm.EFFORT[model[5:]] = effort
    f = file or EXAM / ("model-" + re.sub(r"[^a-z0-9.-]+", "-", model.lower()).strip("-") + ("-pieces" if pieces else "-marks" if marks else "-plain" if bare else "") + ("-" + effort if effort != plain_effort else "") + ".json")
    if marks and file and "-marks" not in file.name: f = file.with_name(file.name.replace(".json", "-marks.json"))          # (a second way of asking never writes into the first way's file)
    try: old = json.load(open(f, encoding="utf-8"))
    except (OSError, ValueError): old = {}
    res = {k: v for k, v in (old.get("cards") or {}).items() if v.get("clear")} if old.get("room") == room and old.get("effort") == effort else {}
    chat = chat or llm.chat; left = left or ((lambda: llm.calls_left(model)) if svc else (lambda: llm.groq_left(model[5:])) if groq else llm.left); stopped_by = None

    def result():
        nb = [i for i in bad if i["id"] in res]; ng = [i for i in draw if i["id"] in res]
        bad_through = sum(res[i["id"]]["through"] for i in nb); good_through = sum(res[i["id"]]["through"] for i in ng)
        out = {"_note": "A model as the lane's checker, on a part of the exam (scripts/auto/exam_models.py): every wrong card and a fixed draw of the good ones." + (" Asked piece by piece: it copied the lines' own words for every piece of the card and the code gave the verdict (lane.pieces_verdict)." if pieces else ""), "model": model, "how": how or "one verdict", "effort": effort, "room": room,
               "wrong_cards_seen": len(nb), "wrong_let_through": bad_through, "wrong_caught": len(nb) - bad_through, "good_cards_seen": len(ng), "good_let_through": good_through, "good_stopped": len(ng) - good_through,
               "no_clear_verdict": sum(not r["clear"] for r in res.values()), "stopped_early": stopped_by, "neurons_today_after": llm.ledger()["neurons"] if chat is llm.chat else None,
               "wrong_let_through_ids": [i["id"] for i in nb if res[i["id"]]["through"]], "what_each_wrong_card_let_through_was": [i.get("what") for i in nb if res[i["id"]]["through"]][:12]}
        if nb and ng:
            # what the whole exam would give: its wrong and good cards in their real numbers
            wt = bad_through / len(nb) * len(bad); gt = good_through / len(ng) * len(good)
            share = wt / (wt + gt) if wt + gt else 0.0
            out["on_the_whole_exam"] = {"wrong_let_through_of_%d" % len(bad): round(wt, 1), "good_let_through_of_%d" % len(good): round(gt, 1), "wrong_share_of_what_it_lets_through": round(share, 4), "bar": exam.BAR, "under_the_bar": share <= exam.BAR,
                                        "good_stopped_share": round(1 - good_through / len(ng), 3)}
        out["cards"] = res
        return out

    mixed = [x for pair in zip(bad, draw) for x in pair] + bad[len(draw):] + draw[len(bad):]             # a wrong card, a good one, in turn: a sitting cut short still says something about both
    failed, last_failed = 0, -9
    todo = [it for it in mixed if it["id"] not in res]
    if isinstance(most, int) and most > 0 and len(todo) > most: todo = todo[:most]; stopped_by = f"the request asked for {most} cards in this sitting"
    for n, it in enumerate(todo, 1):
        if until and time.time() > until: stopped_by = "the time this run has (the job would be stopped before it could keep its results)"; break
        if left() < keep: stopped_by = f"the day's allowance: {left():.0f} {'calls' if svc else 'tokens' if groq else 'neurons'} left, and {keep} are kept for the site's own work"; break
        sent, plain, lines = framed(it)
        if marks and not it.get("plain"): sent = plain                                                      # (a card's true part, as a checker of sentences reads it: no frame of "It is a fact that")
        try: out = llm.as_json(chat(model, [{"role": "system", "content": lane.PIECES_SYS if pieces else lane.MARKS_SYS if marks else lane.CHECKER_SYS},
                                            {"role": "user", "content": lane.pieces_prompt(sent, lines, denies=not it["card"]["answer"]) if pieces else lane.marks_prompt(it["card"]["statement"] if it.get("plain") else sent, lines) if marks
                                             else prompt(dict(it, plain=True, card=dict(it["card"], statement=plain))) if bare and not it.get("plain") else prompt(it)}], room))
        except llm.Budget as e: stopped_by = "the day's allowance: " + str(e); break
        except llm.Unavailable as e:
            if "too large" in str(e).lower() or "request_too_large" in str(e).lower(): res[it["id"]] = {"through": False, "clear": False, "problem": "the card and its lines are too long for one call"}; continue
            failed = failed + 1 if n == last_failed + 1 else 1; last_failed = n
            if failed < 3 and re.search(r"answered 50\d|high demand|could not be reached|timed out|gave no answer", str(e), re.I):        # a service that is busy for a moment: this card waits for the next sitting, the exam goes on
                if chat is llm.chat: time.sleep(30)
                continue
            stopped_by = "the model service: " + str(e)[:200]; break
        if pieces:
            v = lane.pieces_verdict(out, plain, lines, denies=not it["card"]["answer"])
            res[it["id"]] = {"through": v["through"], "clear": v["clear"], "problem": ("no words for: " + "; ".join(v["missing"]) if v["missing"] else "words that are not in the lines for: " + "; ".join(v["not_there"]) if v["not_there"] else "pieces leave out: " + ", ".join(v["left_out"]) if not v["through"] and v["left_out"] else "")[:200], "pieces": v["pieces"]}
            if n % 5 == 0: json.dump(result(), open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            continue
        if marks:
            v = lane.marks_verdict(out, lines); res[it["id"]] = {"through": v["through"], "clear": v["clear"], "problem": v["problem"][:200]}
            if n % 5 == 0: json.dump(result(), open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            continue
        v = ((out or {}).get("verdicts") or [{}])[0] if isinstance((out or {}).get("verdicts"), list) and (out or {}).get("verdicts") else {}
        res[it["id"]] = {"through": v.get("supported") is True, "clear": isinstance(v.get("supported"), bool), "problem": str(v.get("problem") or "")[:160]}
        if n % 5 == 0: json.dump(result(), open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = result(); json.dump(out, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    llm.EFFORT.pop(model[5:], None)
    w = out.get("on_the_whole_exam")
    print(f"exam: {model}{' (piece by piece)' if pieces else ''}{' (effort: ' + effort + ')' if effort else ''}: caught {out['wrong_caught']} of {out['wrong_cards_seen']} wrong cards, stopped {out['good_stopped']} of {out['good_cards_seen']} good ones, no clear word on {out['no_clear_verdict']}"
          + (f"; on the whole exam {100 * w['wrong_share_of_what_it_lets_through']:.1f} in 100 of what it lets through would be wrong (the bar: {100 * exam.BAR:.1f})" if w else "")
          + (f"; stopped early ({stopped_by}); {sum(1 for it in mixed if it['id'] not in res)} cards left for the next sitting" if stopped_by else ""))
    return out


def selftest():
    it = {"lines": {"short": "In one study, 9 in 100 people had it.", "but": "It was a small study.", "how": ["A survey of 200 adults."]}, "card": {"statement": "Most people have it.", "answer": False, "why": "In one study 9 in 100 had it."}}
    p = prompt(it); assert "It is a myth (it is not true) that: Most people have it. Because: In one study 9 in 100 had it." in p and "PASSAGE: But It was a small study." in p and p.count("PASSAGE:") == 3
    # a sitting stops at the day's reserve, keeps what it has, and the next one goes on where it stopped
    import tempfile
    cards = [{"id": f"c{i}", "good": i >= 3, "what": "x", "lines": it["lines"], "card": it["card"]} for i in range(8)]
    f = pathlib.Path(tempfile.mkdtemp()) / "m.json"; asked = []
    def chat(model, messages, room): asked.append(room); return json.dumps({"verdicts": [{"n": 1, "supported": len(asked) % 2 == 0, "problem": ""}]})
    room = iter([9000, 9000, 9000, 9000, 100, 100, 100, 100, 100, 100])
    r = sit("@cf/openai/gpt-oss-120b", 5, cards=cards, chat=chat, left=lambda: next(room), file=f)
    assert len(asked) == 4 and asked[0] == 2420 and r["wrong_cards_seen"] == 2 and r["good_cards_seen"] == 2 and "kept for the site" in r["stopped_early"] and len(json.load(open(f))["cards"]) == 4, (len(asked), r)
    r = sit("@cf/openai/gpt-oss-120b", 5, cards=cards, chat=chat, left=lambda: 9000, file=f)
    assert len(asked) == 8 and r["wrong_cards_seen"] == 3 and r["good_cards_seen"] == 5 and r["stopped_early"] is None and "on_the_whole_exam" in r, (len(asked), r)
    # piece by piece: the code gives the verdict from the words the reader copied
    f2 = pathlib.Path(tempfile.mkdtemp()) / "p.json"; seen = []
    def chat2(model, messages, room):
        seen.append((messages[0]["content"], messages[1]["content"], room))
        wrong = len(seen) % 2 == 1                                           # (wrong and good cards come in turn, a wrong one first)
        return json.dumps({"pieces": [{"says": "Most people have it", "passage_words": "NONE" if wrong else "9 in 100 people had it", "denied": True}, {"says": "In one study 9 in 100 had it", "passage_words": "In one study, 9 in 100 people had it."}]})
    r = sit("groq:openai/gpt-oss-120b", 3, cards=cards[:6], chat=chat2, left=lambda: 90000, file=f2, how="pieces", keep=3000)
    assert seen[0][0] == lane.PIECES_SYS and "Take the SENTENCE below apart" in seen[0][1] and '"denied": false' in seen[0][1] and seen[0][2] == 2900, seen[0]
    assert r["how"] == "pieces" and r["wrong_caught"] == 3 and r["good_stopped"] == 0 and r["no_clear_verdict"] == 0 and r["cards"]["c0"]["problem"].startswith("no words for: Most people"), r
    assert r["effort"] == "medium" and not llm.EFFORT
    f3 = pathlib.Path(tempfile.mkdtemp()) / "h.json"; efforts = []
    def chat3(model, messages, room): efforts.append(dict(llm.EFFORT)); return json.dumps({"verdicts": [{"n": 1, "supported": True, "problem": ""}]})
    r = sit("groq:openai/gpt-oss-120b", 3, cards=cards[:6], chat=chat3, left=lambda: 90000, file=f3, keep=3000, most=4, effort="high")
    assert len(efforts) == 4 and efforts[0] == {"openai/gpt-oss-120b": "high"} and r["effort"] == "high" and "asked for 4 cards" in r["stopped_early"] and r["wrong_cards_seen"] == 2 and r["good_cards_seen"] == 2 and not llm.EFFORT, r
    # the lane's own sentences sit the same question: the sentence as it stands (no "It is a fact that"), the words it rests on as its passages
    lf = pathlib.Path(tempfile.mkdtemp()) / "lane.json"
    json.dump({"items": [{"id": "au_x#short~1", "good": False, "what": "'often'", "sentence": "It often is so.", "rests_on": ["It can be so.", "Some said so."]}, {"id": "au_x#how1~2", "good": True, "what": "", "sentence": "Some said so.", "rests_on": ["Some said so."]}]}, open(lf, "w"))
    lc = lane_cards(lf); pr = prompt(lc[0])
    json.dump({"items": [{"id": "n", "good": True, "sentence": "Health Canada says it can be so.", "rests_on": ["It can be so."], "passages": [{"source": "Health Canada: Ketamine", "where": "Risks", "quote": "It can be so."}]}]}, open(lf.parent / "named.json", "w"))
    assert "   PASSAGE: (Health Canada: Ketamine; Risks) It can be so." in prompt(lane_cards(lf.parent / "named.json")[0])                       # a passage carries its source's name, as in the lane
    assert "1. SENTENCE: It often is so.\n   PASSAGE: It can be so.\n   PASSAGE: Some said so." in pr and "It is a fact" not in pr and slug("gemini:gemma-4-31b-it") == "gemini-gemma-4-31b-it"
    asked = []
    def chat4(model, messages, room): asked.append(messages[1]["content"]); return json.dumps({"verdicts": [{"n": 1, "supported": "SENTENCE: It often" not in messages[1]["content"], "problem": ""}]})
    r = sit("gemini:gemma-4-31b-it", 10 ** 6, cards=lc, chat=chat4, left=lambda: 1000, file=lf.parent / "out.json")
    assert r["wrong_caught"] == 1 and r["good_stopped"] == 0 and r["wrong_cards_seen"] == 1 and r["good_cards_seen"] == 1 and len(asked) == 2, r
    xf = pathlib.Path(tempfile.mkdtemp()) / "lines.json"
    json.dump({"claims": {"c1": [["THE CLAIM", "People said desire often rose."], ["WHO WAS STUDIED", "20 men"]]}, "items": [{"id": "c1#short~was", "claim": "c1", "good": False, "line": "Desire often goes up.", "what": "a recollection said as a fact"}, {"id": "c1#short", "claim": "c1", "good": True, "line": "People say desire often goes up."}]}, open(xf, "w"))
    xc = lines_cards(xf); pr = prompt(xc[0])
    assert "1. SENTENCE: Desire often goes up.\n   PASSAGE: (THE CLAIM) People said desire often rose.\n   PASSAGE: (WHO WAS STUDIED) 20 men" in pr and xc[1]["good"] and xc[0]["what"], pr[-300:]
    # one verdict on a card's true part as it stands: no frame, and a file of its own
    pf = pathlib.Path(tempfile.mkdtemp()) / "p.json"; seen6 = []
    def chat6(model, messages, room): seen6.append(messages[1]["content"]); return json.dumps({"verdicts": [{"n": 1, "supported": True, "problem": ""}]})
    r = sit("gemini:gemini-3.5-flash-lite", 3, cards=cards[:6], chat=chat6, left=lambda: 1000, file=pf, how="plain")
    assert "It is a fact that" not in seen6[0] and "It is a myth" not in "".join(seen6) and "1. SENTENCE: " in seen6[0] and r["how"] == "plain", seen6[0][-300:]
    # asked for marks: five small questions, the code gives the verdict, and the result goes to a file of its own
    mf = pathlib.Path(tempfile.mkdtemp()) / "model-x-lane.json"; got = []
    def chat5(model, messages, room):
        got.append((messages[0]["content"], messages[1]["content"], room)); often = "SENTENCE: It often" in messages[1]["content"]
        return json.dumps({"measure": [{"word": "often", "passage_words": "NONE"}] if often else [], "report_as_fact": False, "wider": False, "cause_added": False, "extra": False, "which": ""})
    r = sit("gemini:gemma-4-31b-it", 10 ** 6, cards=lc, chat=chat5, left=lambda: 1000, file=mf, how="marks")
    assert got[0][0] == lane.MARKS_SYS and "Answer five questions" in got[0][1] and r["how"] == "marks" and r["wrong_caught"] == 1 and r["good_stopped"] == 0 and (mf.parent / "model-x-lane-marks.json").exists() and not mf.exists(), r
    assert "no passage says it" in r["cards"]["au_x#short~1"]["problem"]
    print("exam_models selftest: ok (the lane's own question about a card; a sitting that stops at the day's reserve keeps its cards and the next goes on from there; "
          "asked piece by piece, the code gives the verdict from the words the reader copied)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "requests":
        until = time.time() + 27 * 60                                     # (the job has 40 minutes for ALL its requests; a sitting goes on at the next request where it stopped)
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("exam-*.json")):
            if time.time() > until - 60: print(f"exam: {f.name}: no time left in this run: it stays for the next"); continue
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            f.unlink()
            # "how": "pieces", "one verdict", or a list of both (the same cards each way, so that the two can be compared); "most": cards in this sitting; "effort": low, medium or high
            hows = r.get("how") if isinstance(r.get("how"), list) else [r.get("how")]
            for m in [m for m in (r.get("models") or []) if isinstance(m, str) and re.fullmatch(r"(?:@cf/|groq:|mistral:|gemini:|openrouter:)[A-Za-z0-9._/:-]{3,90}", m)][:4]:
                if not llm.has(m): print(f"exam: {m}: no key for its service on this machine (or it is not a free model): not sat"); continue
                which = r.get("exam") if r.get("exam") in ("cards", "lane", "lines", "both", "all") else "cards"
                opts = dict(until=until, keep=r.get("keep") if isinstance(r.get("keep"), int) else None, most=r.get("most") if isinstance(r.get("most"), int) else None, effort=r.get("effort") if isinstance(r.get("effort"), str) else None,
                            how="marks" if "marks" in hows else None)         # (the lane's sentences and the plain lines are sat one way in a request: with "marks" in "how", that way)
                if which in ("lane", "both", "all") and lane_cards():    # the lane's own sentences first, all of them: the real task, and small
                    sit(m, 10 ** 6, cards=lane_cards(), file=EXAM / ("model-" + slug(m) + "-lane.json"), **opts)
                if which in ("lines", "all") and lines_cards():          # plain lines beside their checked claims: every wrong one, and twice as many good ones
                    lc = lines_cards(); sit(m, 2 * sum(not i["good"] for i in lc), cards=lc, file=EXAM / ("model-" + slug(m) + "-lines.json"), **opts)
                if which in ("lane", "lines"): continue
                for h in hows[:2]:
                    sit(m, int(r.get("good") or 62) if isinstance(r.get("good"), int) else 62, until=until, how=h if h in ("pieces", "marks", "plain") else None, keep=r.get("keep") if isinstance(r.get("keep"), int) else None,
                        most=r.get("most") if isinstance(r.get("most"), int) else None, effort=r.get("effort") if isinstance(r.get("effort"), str) else None)
    else: sys.exit(__doc__)
