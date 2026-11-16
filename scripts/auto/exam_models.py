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
import sys, re, json, random, pathlib
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


def sit(model, n_good, cards=None, chat=None, left=None, file=None):
    """The model's verdict on every wrong card and a fixed draw of the good ones. It goes on where an earlier sitting with
    the same room stopped (its cards are kept in the result), stops when the day's allowance is down to KEEP, and writes
    as it goes, so that a sitting cut short by the allowance or by the machine's time limit is not lost."""
    items = cards or json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]
    bad = [i for i in items if not i["good"]]; good = [i for i in items if i["good"]]
    rnd = random.Random(20261115); draw = rnd.sample(good, min(n_good, len(good)))
    room = lane.room_for(model, 220) if not model.startswith("groq:") else 700          # (a model that reasons first needs room: on 15 November gpt-oss-120b gave no verdict in 220, nor in 700)
    f = file or EXAM / ("model-" + re.sub(r"[^a-z0-9.-]+", "-", model.lower()).strip("-") + ".json")
    try: old = json.load(open(f, encoding="utf-8"))
    except (OSError, ValueError): old = {}
    res = {k: v for k, v in (old.get("cards") or {}).items() if v.get("clear")} if old.get("room") == room else {}
    chat = chat or llm.chat; left = left or llm.left; stopped_by = None

    def result():
        nb = [i for i in bad if i["id"] in res]; ng = [i for i in draw if i["id"] in res]
        bad_through = sum(res[i["id"]]["through"] for i in nb); good_through = sum(res[i["id"]]["through"] for i in ng)
        out = {"_note": "A model as the lane's checker, on a part of the exam (scripts/auto/exam_models.py): every wrong card and a fixed draw of the good ones.", "model": model, "room": room,
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

    todo = [it for it in bad + draw if it["id"] not in res]
    for n, it in enumerate(todo, 1):
        if left() < KEEP: stopped_by = f"the day's allowance: {left():.0f} neurons left, and {KEEP} are kept for the site's own work"; break
        try: out = llm.as_json(chat(model, [{"role": "system", "content": lane.CHECKER_SYS}, {"role": "user", "content": prompt(it)}], room))
        except llm.Budget as e: stopped_by = "the day's allowance: " + str(e); break
        except llm.Unavailable as e: stopped_by = "the model service: " + str(e)[:200]; break
        v = ((out or {}).get("verdicts") or [{}])[0] if isinstance((out or {}).get("verdicts"), list) and (out or {}).get("verdicts") else {}
        res[it["id"]] = {"through": v.get("supported") is True, "clear": isinstance(v.get("supported"), bool), "problem": str(v.get("problem") or "")[:160]}
        if n % 5 == 0: json.dump(result(), open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = result(); json.dump(out, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    w = out.get("on_the_whole_exam")
    print(f"exam: {model}: caught {out['wrong_caught']} of {out['wrong_cards_seen']} wrong cards, stopped {out['good_stopped']} of {out['good_cards_seen']} good ones"
          + (f"; on the whole exam {100 * w['wrong_share_of_what_it_lets_through']:.1f} in 100 of what it lets through would be wrong (the bar: {100 * exam.BAR:.1f})" if w else "")
          + (f"; stopped early ({stopped_by}); {len(todo) - sum(1 for it in todo if it['id'] in res)} cards left for the next sitting" if stopped_by else ""))
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
    assert len(asked) == 4 and asked[0] == 2420 and r["wrong_cards_seen"] == 3 and r["good_cards_seen"] == 1 and "kept for the site" in r["stopped_early"] and len(json.load(open(f))["cards"]) == 4, (len(asked), r)
    r = sit("@cf/openai/gpt-oss-120b", 5, cards=cards, chat=chat, left=lambda: 9000, file=f)
    assert len(asked) == 8 and r["wrong_cards_seen"] == 3 and r["good_cards_seen"] == 5 and r["stopped_early"] is None and "on_the_whole_exam" in r, (len(asked), r)
    print("exam_models selftest: ok (the lane's own question about a card; a sitting that stops at the day's reserve keeps its cards and the next goes on from there)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "requests":
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("exam-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            f.unlink()
            for m in [m for m in (r.get("models") or []) if isinstance(m, str) and re.fullmatch(r"@cf/[A-Za-z0-9._/-]{3,80}", m)][:4]:
                sit(m, int(r.get("good") or 62) if isinstance(r.get("good"), int) else 62)
    else: sys.exit(__doc__)
