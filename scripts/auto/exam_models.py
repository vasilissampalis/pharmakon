#!/usr/bin/env python3
"""exam_models.py: a model sits the exam as the lane's checker (docs/AUTOMATION.md; scripts/auto/exam.py).

    python3 -I scripts/auto/exam_models.py requests      (data/auto/requests/exam-*.json: {"models": [...], "good": 62})

The exam's items are our own blind checks: a Myth or fact? card beside the checked lines it was written from, and whether a
blind checker who wrote none of it found that the card says only what the lines say. The model is asked the lane's own
question, in the lane's own words (lane.CHECKER_SYS): do the passages support the sentence? Its yes lets the card through.

Every call costs some of the day's free allowance, so a model sits a part of the exam: every one of the wrong cards (the
ones a checker must catch) and a fixed draw of the good ones (seed 20261115; "good" in the request says how many). From
the two shares the result gives what the whole exam would give: of everything the model would let through, how much is
wrong (exam.py's bar: 1 in 50; the senior author's goal: 1 in 1,000), and how many good cards it would stop.
Writes data/auto/exam/model-<name>.json. The exam is small: it can show that a checker is not good enough, never that it is.
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
    sent = ("It is a fact that: " if c["answer"] else "It is a myth (it is not true) that: ") + c["statement"] + (" Because: " + c["why"] if c.get("why") else "")
    return ("For the SENTENCE below, decide whether its PASSAGES support it. Supported means ALL of this: everything the sentence says is stated in its passages; "
            "it is about the same people, animals or setting; every number is the same; it is not stronger or more certain than the passages; it does not say one thing causes another "
            "where the passages only report a link; it does not turn what one study found into a general fact. If any part of the sentence is not in the passages, it is not supported.\n\n"
            f"1. SENTENCE: {sent}\n{ps}\n\n"
            'JSON only, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}]}')


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
    room = lane.room_for(model, 700 if pieces else 220) if "gpt-oss" in model or not model.startswith("groq:") else 2000          # (a model that reasons first needs room: on 15 November gpt-oss-120b gave no verdict in 220, nor in 700)
    svc = llm.service_of(model)[0]                                                                             # (a service that counts calls: one card is one call, and five calls are kept)
    groq = model.startswith("groq:"); keep = 5 if svc else max(2000 if groq else KEEP, keep) if isinstance(keep, (int, float)) else 30000 if groq else KEEP      # (Groq counts a day in tokens for each model: 30,000 are left for the lane unless the request says the lane does not run today)
    # how hard a reasoning model at Groq thinks: the request's word, else what llm.chat_groq asks by itself (the larger gpt-oss: medium; the smaller: low; qwen3: none)
    plain_effort = ("low" if model.endswith("gpt-oss-20b") else "medium") if "gpt-oss" in model else "none" if "qwen3" in model else ""
    effort = effort if effort in ("low", "medium", "high") and groq and "gpt-oss" in model else plain_effort
    if groq and effort != plain_effort: llm.EFFORT[model[5:]] = effort
    f = file or EXAM / ("model-" + re.sub(r"[^a-z0-9.-]+", "-", model.lower()).strip("-") + ("-pieces" if pieces else "") + ("-" + effort if effort != plain_effort else "") + ".json")
    try: old = json.load(open(f, encoding="utf-8"))
    except (OSError, ValueError): old = {}
    res = {k: v for k, v in (old.get("cards") or {}).items() if v.get("clear")} if old.get("room") == room and old.get("effort") == effort else {}
    chat = chat or llm.chat; left = left or ((lambda: llm.calls_left(svc)) if svc else (lambda: llm.groq_left(model[5:])) if groq else llm.left); stopped_by = None

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
    todo = [it for it in mixed if it["id"] not in res]
    if isinstance(most, int) and most > 0 and len(todo) > most: todo = todo[:most]; stopped_by = f"the request asked for {most} cards in this sitting"
    for n, it in enumerate(todo, 1):
        if until and time.time() > until: stopped_by = "the time this run has (the job would be stopped before it could keep its results)"; break
        if left() < keep: stopped_by = f"the day's allowance: {left():.0f} {'calls' if svc else 'tokens' if groq else 'neurons'} left, and {keep} are kept for the site's own work"; break
        sent, plain, lines = framed(it)
        try: out = llm.as_json(chat(model, [{"role": "system", "content": lane.PIECES_SYS if pieces else lane.CHECKER_SYS}, {"role": "user", "content": lane.pieces_prompt(sent, lines, denies=not it["card"]["answer"]) if pieces else prompt(it)}], room))
        except llm.Budget as e: stopped_by = "the day's allowance: " + str(e); break
        except llm.Unavailable as e:
            if "too large" in str(e).lower() or "request_too_large" in str(e).lower(): res[it["id"]] = {"through": False, "clear": False, "problem": "the card and its lines are too long for one call"}; continue
            stopped_by = "the model service: " + str(e)[:200]; break
        if pieces:
            v = lane.pieces_verdict(out, plain, lines, denies=not it["card"]["answer"])
            res[it["id"]] = {"through": v["through"], "clear": v["clear"], "problem": ("no words for: " + "; ".join(v["missing"]) if v["missing"] else "words that are not in the lines for: " + "; ".join(v["not_there"]) if v["not_there"] else "pieces leave out: " + ", ".join(v["left_out"]) if not v["through"] and v["left_out"] else "")[:200], "pieces": v["pieces"]}
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
    print("exam_models selftest: ok (the lane's own question about a card; a sitting that stops at the day's reserve keeps its cards and the next goes on from there; "
          "asked piece by piece, the code gives the verdict from the words the reader copied)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "requests":
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("exam-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            f.unlink()
            until = time.time() + 27 * 60                                 # (the job has 40 minutes; a sitting goes on at the next request where it stopped)
            # "how": "pieces", "one verdict", or a list of both (the same cards each way, so that the two can be compared); "most": cards in this sitting; "effort": low, medium or high
            hows = r.get("how") if isinstance(r.get("how"), list) else [r.get("how")]
            for m in [m for m in (r.get("models") or []) if isinstance(m, str) and re.fullmatch(r"(?:@cf/|groq:|mistral:|gemini:|openrouter:)[A-Za-z0-9._/:-]{3,90}", m)][:4]:
                if not llm.has(m): print(f"exam: {m}: no key for its service on this machine: not sat"); continue
                for h in hows[:2]:
                    sit(m, int(r.get("good") or 62) if isinstance(r.get("good"), int) else 62, until=until, how="pieces" if h == "pieces" else None, keep=r.get("keep") if isinstance(r.get("keep"), int) else None,
                        most=r.get("most") if isinstance(r.get("most"), int) else None, effort=r.get("effort") if isinstance(r.get("effort"), str) else None)
    else: sys.exit(__doc__)
