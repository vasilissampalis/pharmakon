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


def sit(model, n_good):
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]
    bad = [i for i in items if not i["good"]]; good = [i for i in items if i["good"]]
    rnd = random.Random(20261115); draw = rnd.sample(good, min(n_good, len(good)))
    res, stopped_by = {}, None
    for it in bad + draw:
        try: out = llm.as_json(llm.chat(model, [{"role": "system", "content": lane.CHECKER_SYS}, {"role": "user", "content": prompt(it)}], 220))
        except llm.Budget as e: stopped_by = "the day's allowance: " + str(e); break
        except llm.Unavailable as e: stopped_by = "the model service: " + str(e)[:200]; break
        v = ((out or {}).get("verdicts") or [{}])[0] if isinstance((out or {}).get("verdicts"), list) and (out or {}).get("verdicts") else {}
        res[it["id"]] = {"through": v.get("supported") is True, "clear": isinstance(v.get("supported"), bool), "problem": str(v.get("problem") or "")[:160]}
    nb = [i for i in bad if i["id"] in res]; ng = [i for i in draw if i["id"] in res]
    bad_through = sum(res[i["id"]]["through"] for i in nb); good_through = sum(res[i["id"]]["through"] for i in ng)
    out = {"_note": "A model as the lane's checker, on a part of the exam (scripts/auto/exam_models.py): every wrong card and a fixed draw of the good ones.", "model": model,
           "wrong_cards_seen": len(nb), "wrong_let_through": bad_through, "wrong_caught": len(nb) - bad_through, "good_cards_seen": len(ng), "good_let_through": good_through, "good_stopped": len(ng) - good_through,
           "no_clear_verdict": sum(not r["clear"] for r in res.values()), "stopped_early": stopped_by, "neurons_today_after": llm.ledger()["neurons"]}
    if nb and ng:
        # what the whole exam would give: its wrong and good cards in their real numbers
        wt = bad_through / len(nb) * len(bad); gt = good_through / len(ng) * len(good)
        share = wt / (wt + gt) if wt + gt else 0.0
        out.update({"on_the_whole_exam": {"wrong_let_through_of_31": round(wt, 1), "good_let_through_of_287": round(gt, 1), "wrong_share_of_what_it_lets_through": round(share, 4), "bar": exam.BAR, "under_the_bar": share <= exam.BAR,
                                          "good_stopped_share": round(1 - good_through / len(ng), 3)},
                    "wrong_let_through_ids": [i["id"] for i in nb if res[i["id"]]["through"]], "what_each_wrong_card_let_through_was": [i.get("what") for i in nb if res[i["id"]]["through"]][:12]})
        print(f"exam: {model}: caught {len(nb) - bad_through} of {len(nb)} wrong cards, stopped {len(ng) - good_through} of {len(ng)} good ones; on the whole exam {100 * share:.1f} in 100 of what it lets through would be wrong (the bar: 2.0)")
    else: print(f"exam: {model}: no result ({stopped_by})")
    json.dump(out, open(EXAM / ("model-" + re.sub(r"[^a-z0-9.-]+", "-", model.lower()).strip("-") + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def selftest():
    it = {"lines": {"short": "In one study, 9 in 100 people had it.", "but": "It was a small study.", "how": ["A survey of 200 adults."]}, "card": {"statement": "Most people have it.", "answer": False, "why": "In one study 9 in 100 had it."}}
    p = prompt(it); assert "It is a myth (it is not true) that: Most people have it. Because: In one study 9 in 100 had it." in p and "PASSAGE: But It was a small study." in p and p.count("PASSAGE:") == 3
    print("exam_models selftest: ok")


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
