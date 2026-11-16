#!/usr/bin/env python3
"""workshop.py: where a model of our own is made and sits the exam as the very file the lane will run (decision 23).

    python3 -I scripts/auto/workshop.py requests          (own-*.json in data/auto/requests, read as data:
                                                           {"do": "export", "model": "<an open model on GROUNDED's list>", "as": "pharmakon-check-0"})
    python3 -I scripts/auto/workshop.py sit NAME DIR       (the exam for files already made: DIR/NAME.onnx, DIR/NAME.tokenizer.json)
    python3 -I scripts/auto/workshop.py pick NAME          (a candidate's numbers counted again from the scores it left, by today's rule; no model is run)
    python3 -I scripts/auto/workshop.py more NAME lines    (a candidate on file sits a further exam on this machine, as the very file its record names)
    python3 -I scripts/auto/workshop.py --selftest

Runs ONLY in the workshop job (.github/workflows/own.yml), which may read the repository and holds no key: this is the
one place where things fetched from outside (an open model, torch, transformers) are run. What leaves it is a folder of
plain files (out/): the model as a file of numbers (ONNX, its weights as 8-bit numbers so that it is small and quick on
one machine), its tokenizer's table, and a candidate's record with the SHA-256 of both and the model's numbers on the
whole exam, sat AS THAT FILE with the same code the lane runs (scripts/auto/own.py). The second job of the workflow, which
runs nothing from outside, puts the files among this repository's release files and the record into
data/auto/own/candidates/. Adopting a candidate is a separate step with its own rule (own.py adopt).

Two exams. The cards: every card's true part (a fact's statement and each sentence of its explanation; for a myth only the
explanation, because a myth's statement is false on purpose) against the lines the card was written from. A card is let
through when every such sentence scores at least the threshold. The threshold a candidate carries is the one that lets
the fewest wrong cards through among those that stop no more than one good card in twelve (BUDGET). Why so few: our own
checker is one judge of several, and every judge must accept a sentence, so what each one wrongly stops adds up. The first
open models showed where such a judge earns its place (16 November 2026): MiniCheck on RoBERTa at 0.05 caught 3 of the 22
faulty sentences and stopped 4 of 742 good ones (when it speaks there, it is nearly always right); at 0.5 it caught 5 and
stopped 78. (Until that day the rule here allowed one good card in four; it chose 0.5.)
Beside the cards the same scores are counted sentence by sentence (data/auto/exam/cards-where.json says which sentence of
each wrong card carries the fault): the lane's unit is the sentence.
The lane's own sentences (data/auto/exam/lane-sentences.json): every sentence the system wrote that the editor has judged,
against the words it rests on. This is the lane's real task; it is small still and grows with every batch the editor reads,
so a candidate's numbers on it are written down beside the cards' and count in the rule once the exam is large enough
(own.py). The two exams can ask for different thresholds: both tables are kept.
"""
import sys, re, json, time, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import own, nli

EXAM = ROOT / "data" / "auto" / "exam"
OUT = ROOT / "out"
THRESHOLDS = (0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95)
BUDGET = 1 / 12        # the share of good cards one judge of a panel may stop
LICENCES = {"lytang/MiniCheck-RoBERTa-Large": "MIT", "lytang/MiniCheck-DeBERTa-v3-Large": "MIT", "lytang/MiniCheck-Flan-T5-Large": "MIT",
            "KRLabsOrg/lettucedect-large-modernbert-en-v1": "MIT", "KRLabsOrg/lettucedect-base-modernbert-en-v1": "MIT"}


def true_part(card):
    """The sentences of a card that it states as true: [(text, what it is)]."""
    why = nli.split(re.sub(r"^(?:true|false|myth|fact)[.!:]?\s+", "", card.get("why") or "", flags=re.I))
    return ([(card["statement"], "statement")] if card["answer"] else []) + [(w, "why") for w in why]


def table(rows):
    """rows: [{"good", "scores": [...]}] -> for each threshold what it lets through; and the one a candidate carries."""
    good = [r for r in rows if r["good"]]; bad = [r for r in rows if not r["good"]]; out = []
    for t in THRESHOLDS:
        gt = sum(all(s >= t for s in r["scores"]) for r in good); bt = sum(all(s >= t for s in r["scores"]) for r in bad)
        out.append({"threshold": t, "wrong": len(bad), "good": len(good), "wrong_through": bt, "good_stopped": len(good) - gt})
    ok = [x for x in out if x["good_stopped"] <= BUDGET * len(good)] or out[:1]
    return out, min(ok, key=lambda x: (x["wrong_through"], x["good_stopped"]))


def sentence_table(rows, where=None):
    """The same scores, sentence by sentence: for each threshold, how many of the faulty sentences score under it (caught) and
    how many of the good ones (stopped). where: data/auto/exam/cards-where.json's "cards"."""
    if where is None:
        try: where = json.load(open(EXAM / "cards-where.json", encoding="utf-8"))["cards"]
        except (OSError, ValueError): return []
    bad, good = [], []
    for r in rows:
        at = set((where.get(r["id"]) or {}).get("at") or [])
        for k, s in enumerate(r["scores"]): (bad if k in at else good).append(s)
    return [{"threshold": t, "faulty": len(bad), "good": len(good), "faulty_caught": sum(s < t for s in bad), "good_stopped": sum(s < t for s in good)} for t in THRESHOLDS] if bad and good else []


def pick(name, folder=None):
    """Count a candidate's numbers again from the scores it left (no model is run): the tables, the threshold by today's rule,
    its numbers on the lane's own sentences at that threshold. Writes the candidate's record; returns it."""
    folder = folder or own.OWN / "candidates"
    e = json.load(open(folder / (name + ".json"), encoding="utf-8")); sc = json.load(open(folder / (name + ".scores.json"), encoding="utf-8"))
    tb, best = table(sc["items"]); ltb = table(sc["lane"])[0] if sc.get("lane") else []
    e.update(threshold=best["threshold"], exam=dict(best, whole=(e.get("exam") or {}).get("whole", True), seconds_a_sentence=(e.get("exam") or {}).get("seconds_a_sentence")), exam_table=tb, exam_sentences=sentence_table(sc["items"]),
             threshold_rule=f"the fewest wrong cards let through among the thresholds that stop no more than 1 good card in {round(1 / BUDGET)}")
    if ltb: e.update(exam_lane=at_threshold(ltb, best["threshold"]), exam_lane_table=ltb)
    if sc.get("lines"):
        xtb = table(sc["lines"])[0]; e.update(exam_lines=at_threshold(xtb, best["threshold"]), exam_lines_table=xtb)
    json.dump(e, open(folder / (name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return e


def more(name, what, minutes=0, folder=None):
    """A candidate that is on file sits a further exam on THIS machine, as the file whose SHA-256 its record names (fetched from
    the repository's release files by own.fetch, which refuses any other file). what: "lines" or "lane". The scores are added
    to the candidate's scores and its record is counted again."""
    folder = folder or own.OWN / "candidates"
    e = json.load(open(folder / (name + ".json"), encoding="utf-8")); sf = folder / (name + ".scores.json"); sc = json.load(open(sf, encoding="utf-8"))
    chk = own.Check(entry=e)
    if what == "lines": sc["lines"] = sit_lines(chk, minutes=minutes)[0]
    elif what == "lane": sc["lane"] = sit_lane(chk)[0]
    else: sys.exit("workshop: a further exam is 'lines' or 'lane'")
    json.dump(sc, open(sf, "w", encoding="utf-8"), ensure_ascii=False)
    return pick(name, folder)


def sit_lane(chk, exam=None):
    """The exam of the lane's own sentences: (rows, the table). A row is one sentence, so its "scores" hold one number."""
    try: items = json.load(open(exam or EXAM / "lane-sentences.json", encoding="utf-8"))["items"]
    except (OSError, ValueError): return [], []
    premise = lambda i: " ".join((x["source"] + ". " if x.get("source") else "") + x["quote"] for x in i["passages"]) if i.get("passages") else " ".join(i["rests_on"])     # (the source's name stands with its words, as in the lane: lane.own_word)
    scores = chk.score([(premise(i), i["sentence"]) for i in items]) if items else []
    rows = [{"id": i["id"], "good": i["good"], "scores": [s]} for i, s in zip(items, scores)]
    return rows, (table(rows)[0] if rows else [])


def sit_lines(chk, n_good=168, minutes=0, exam=None, seed=20261116):
    """The exam of plain lines (scripts/auto/exam_lines.py): every line a blind checker changed for what it said and a fixed
    draw of the good ones, each against the checked claim it was written from (a long text: the best part counts, as in the
    lane). Returns (rows, the table)."""
    import random
    try: d = json.load(open(exam or EXAM / "lines.json", encoding="utf-8"))
    except (OSError, ValueError): return [], []
    bad = [i for i in d["items"] if not i["good"]]; good = [i for i in d["items"] if i["good"]]
    draw = random.Random(seed).sample(good, min(n_good, len(good)))
    mixed = [x for pair in zip(bad, draw) for x in pair] + bad[len(draw):] + draw[len(bad):]; rows = []; t0 = time.time()
    for i in mixed:                                                   # a wrong line, a good one, in turn: a sitting cut short still says something about both
        if minutes and time.time() - t0 > minutes * 60: break
        rows.append({"id": i["id"], "good": i["good"], "scores": chk.score([(" ".join(x for _, x in d["claims"][i["claim"]]), i["line"])])})
    return rows, (table(rows)[0] if any(r["good"] for r in rows) and any(not r["good"] for r in rows) else [])


def at_threshold(tb, threshold):
    """A table's row for one threshold (the numbers a candidate has on the lane's sentences at the threshold it carries)."""
    return next((dict(x) for x in tb if x["threshold"] == threshold), None)


def sit(name, folder, entry, minutes=0, chk=None):
    """The whole exam for the files in folder, with the lane's own code. Returns (rows, the table, the row it carries)."""
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]; t0 = time.time()
    chk = chk or own.Check(entry=entry, files={"model": folder / (name + ".onnx"), "tokenizer": folder / (name + ".tokenizer.json")})
    rows = []
    for it in items:
        if minutes and time.time() - t0 > minutes * 60: break
        L = it["lines"]; premise = " ".join(t for t in [L.get("short") or "", L.get("but") or ""] + list(L.get("how") or []) if t)
        tp = true_part(it["card"])
        rows.append({"id": it["id"], "good": it["good"], "scores": chk.score([(premise, t) for t, _ in tp]) if tp else []})
    tb, pick = table(rows)
    return rows, tb, pick, len(rows) == len(items), (time.time() - t0) / max(1, sum(len(r["scores"]) for r in rows))


def export(model, name, quant=True):
    """An open classifier of GROUNDED's list as a file of numbers. Returns the candidate's entry (without its exam)."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    kind, most = nli.GROUNDED[model]
    if kind != "seq": sys.exit("workshop: only a classifier (kind seq) can be made into a file here yet: " + model)
    OUT.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(model); m = AutoModelForSequenceClassification.from_pretrained(model); m.eval()
    eos = tok.eos_token or tok.sep_token or "</s>"
    x = tok("A passage of a source." + eos + "A sentence written from it.", return_tensors="pt")
    raw = OUT / (name + ".fp32.onnx")
    torch.onnx.export(m, (x["input_ids"], x["attention_mask"]), str(raw), input_names=["input_ids", "attention_mask"], output_names=["logits"],
                      dynamic_axes={"input_ids": {0: "n", 1: "t"}, "attention_mask": {0: "n", 1: "t"}, "logits": {0: "n"}}, opset_version=17, dynamo=False)      # (the plain exporter: the newer one needs a package more and is not needed for a classifier)
    final = OUT / (name + ".onnx")
    if quant:
        from onnxruntime.quantization import quantize_dynamic, QuantType
        quantize_dynamic(str(raw), str(final), weight_type=QuantType.QInt8); raw.unlink()
        for extra in OUT.glob(name + ".fp32.onnx*"): extra.unlink()
    else: raw.rename(final)
    tok.save_pretrained(str(OUT / "_tok")); (OUT / "_tok" / "tokenizer.json").rename(OUT / (name + ".tokenizer.json"))
    for f in (OUT / "_tok").iterdir(): f.unlink()
    (OUT / "_tok").rmdir()
    return {"name": name, "job": "check", "from": model, "licence": LICENCES.get(model, "see the model's page"), "kind": "seq", "max_len": min(most, 512), "join": eos, "weights": "8-bit" if quant else "32-bit",
            "made": datetime.date.today().isoformat(), "how": "made from the open model as it is (no training of ours yet): scripts/auto/workshop.py export"}


def finish(entry, name, minutes=0):
    files = {}
    for kind, fn in (("model", name + ".onnx"), ("tokenizer", name + ".tokenizer.json")):
        p = OUT / fn; files[kind] = {"url": own.RELEASES + "own-models/" + fn, "sha256": own.sha256(p), "bytes": p.stat().st_size}
    chk = own.Check(entry=dict(entry, files=files), files={"model": OUT / (name + ".onnx"), "tokenizer": OUT / (name + ".tokenizer.json")})
    rows, tb, pick, whole, secs = sit(name, OUT, dict(entry, files=files), minutes, chk)
    lrows, ltb = sit_lane(chk); lane_at = at_threshold(ltb, pick["threshold"])
    entry = dict(entry, files=files, threshold=pick["threshold"], exam=dict(pick, whole=whole, seconds_a_sentence=round(secs, 2)), exam_table=tb, exam_sentences=sentence_table(rows),
                 threshold_rule=f"the fewest wrong cards let through among the thresholds that stop no more than 1 good card in {round(1 / BUDGET)}")
    if lane_at: entry.update(exam_lane=lane_at, exam_lane_table=ltb)
    json.dump(entry, open(OUT / (name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"_note": "The scores of " + name + " for the true part of every card of the exam, and for every sentence of the lane's own that the editor has judged (scripts/auto/workshop.py).", "items": rows, "lane": lrows},
              open(OUT / (name + ".scores.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"workshop: {name} (from {entry['from']}, {files['model']['bytes'] / 1e6:.0f} MB): at {pick['threshold']}: lets {pick['wrong_through']} of {pick['wrong']} wrong cards through, stops {pick['good_stopped']} of {pick['good']} good ones"
          + ("" if whole else "; NOT the whole exam (time was up)") + f"; {secs:.2f} seconds a sentence"
          + (f"; of the lane's own sentences it lets {lane_at['wrong_through']} of {lane_at['wrong']} that are not good through and stops {lane_at['good_stopped']} of {lane_at['good']} good ones" if lane_at else ""))
    return entry


def selftest():
    c = {"statement": "Alcohol is addictive.", "answer": True, "why": "True. Many people become dependent. It was one survey."}
    assert true_part(c) == [("Alcohol is addictive.", "statement"), ("Many people become dependent.", "why"), ("It was one survey.", "why")]
    assert true_part(dict(c, answer=False)) == [("Many people become dependent.", "why"), ("It was one survey.", "why")]          # a myth's statement is false on purpose
    rows = [{"id": f"g{n}", "good": True, "scores": [0.9, 0.8]} for n in range(22)] + [{"id": "g22", "good": True, "scores": [0.9, 0.35]}, {"id": "g23", "good": True, "scores": [0.9, 0.15]}] \
         + [{"id": "w0", "good": False, "scores": [0.9, 0.03]}, {"id": "w1", "good": False, "scores": [0.9, 0.3]}, {"id": "w2", "good": False, "scores": [0.95, 0.9]}]
    tb, best = table(rows)
    at = {x["threshold"]: x for x in tb}
    assert at[0.02]["wrong_through"] == 3 and at[0.05]["wrong_through"] == 2 and at[0.2]["good_stopped"] == 1 and at[0.4]["wrong_through"] == 1 and at[0.4]["good_stopped"] == 2 and at[0.95]["good_stopped"] == 24
    assert best["threshold"] == 0.4 and best["wrong_through"] == 1 and best["good_stopped"] == 2, best          # 2 of 24 good cards is one in twelve: the fewest wrong cards through within that
    rows.append({"id": "g24", "good": True, "scores": [0.38]}); assert table(rows)[1]["threshold"] == 0.05      # with 3 of 25 stopped at 0.4 it is over the budget: the best threshold within it
    st = sentence_table(rows, {"w0": {"at": [1]}, "w1": {"at": [1]}, "w2": {"at": []}})
    s = {x["threshold"]: x for x in st}
    assert s[0.05] == {"threshold": 0.05, "faulty": 2, "good": 53, "faulty_caught": 1, "good_stopped": 0} and s[0.4]["faulty_caught"] == 2 and s[0.4]["good_stopped"] == 3, s[0.05]
    # the lane's own sentences: one score a sentence, against the words it rests on, and the numbers at the threshold the candidate carries
    import tempfile
    class Chk:
        def score(self, pairs): self.seen = pairs; return [0.9 if "can be" in s else 0.2 for _, s in pairs]
    f = pathlib.Path(tempfile.mkdtemp()) / "lane.json"
    json.dump({"items": [{"id": "a", "good": True, "sentence": "It can be so.", "rests_on": ["It can", "be so."]}, {"id": "b", "good": False, "sentence": "It often is so.", "rests_on": ["It can be so."]},
                         {"id": "c", "good": False, "sentence": "It can be so, experts say.", "rests_on": ["It can be so."]}]}, open(f, "w"))
    c = Chk(); lrows, ltb = sit_lane(c, f)
    assert c.seen[0] == ("It can be so.", "It can be so.") and [r["scores"] for r in lrows] == [[0.9], [0.2], [0.9]]
    assert at_threshold(ltb, 0.4) == {"threshold": 0.4, "wrong": 2, "good": 1, "wrong_through": 1, "good_stopped": 0} and at_threshold(ltb, 0.95)["good_stopped"] == 1 and at_threshold(ltb, 0.33) is None
    assert sit_lane(c, f.parent / "none.json") == ([], [])
    xf = f.parent / "lines.json"
    json.dump({"claims": {"c1": [["THE CLAIM", "It can be so."], ["WHO", "20 men"]]}, "items": [{"id": "x~was", "claim": "c1", "good": False, "line": "It often is so."}, {"id": "x", "claim": "c1", "good": True, "line": "It can be so."}, {"id": "y", "claim": "c1", "good": True, "line": "It can be so for men."}]}, open(xf, "w"))
    c2 = Chk(); xrows, xtb = sit_lines(c2, n_good=1, exam=xf)
    assert len(xrows) == 2 and not xrows[0]["good"] and xrows[0]["scores"] == [0.2] and c2.seen[0][0] == "It can be so. 20 men" and at_threshold(xtb, 0.5)["wrong_through"] == 0 and at_threshold(xtb, 0.5)["good_stopped"] == 0
    print("workshop selftest: ok (a card's true part: a myth's statement is left out; the threshold a candidate carries lets the fewest wrong cards through while it stops no more than one good card in twelve; the same scores are counted sentence by sentence; "
          "the lane's own sentences are sat against the words they rest on, and counted at that threshold)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a and a[0] == "requests":
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("own-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            model, name = r.get("model"), r.get("as")
            if r.get("do") != "export" or model not in nli.GROUNDED or not isinstance(name, str) or not re.fullmatch(r"pharmakon-[a-z]+-[0-9a-z.-]{1,20}", name):
                print("workshop: a request that names no model of the list, or no name of the form pharmakon-<job>-<number>: left alone:", f.name); continue
            try: finish(export(model, name, quant=r.get("quant") is not False), name, minutes=float(r.get("minutes") or 30))
            except SystemExit: raise
            except Exception as e: print(f"workshop: {name} from {model}: not made ({type(e).__name__}: {str(e)[:300]})")
    elif len(a) >= 2 and a[0] in ("pick", "more") and re.fullmatch(r"pharmakon-[a-z]+-[0-9a-z.-]{1,20}", a[1]):
        e = pick(a[1]) if a[0] == "pick" else more(a[1], a[2] if len(a) > 2 else "lines", minutes=float(a[a.index("--minutes") + 1]) if "--minutes" in a else 0); x = e["exam"]; s = next((r for r in e.get("exam_sentences") or [] if r["threshold"] == e["threshold"]), None); l = e.get("exam_lane")
        print(f"workshop: {a[1]}: at {e['threshold']} ({e['threshold_rule']}): lets {x['wrong_through']} of {x['wrong']} wrong cards through, stops {x['good_stopped']} of {x['good']} good ones"
              + (f"; sentence by sentence: catches {s['faulty_caught']} of {s['faulty']} faulty ones, stops {s['good_stopped']} of {s['good']} good ones" if s else "")
              + (f"; of the lane's own sentences: lets {l['wrong_through']} of {l['wrong']} that are not good through, stops {l['good_stopped']} of {l['good']} good ones" if l else "")
              + (f"; of the plain lines: lets {e['exam_lines']['wrong_through']} of {e['exam_lines']['wrong']} wrong ones through, stops {e['exam_lines']['good_stopped']} of {e['exam_lines']['good']} good ones" if e.get("exam_lines") else ""))
    elif len(a) == 3 and a[0] == "sit":
        e = json.load(open(pathlib.Path(a[2]) / (a[1] + ".json"), encoding="utf-8")); print(sit(a[1], pathlib.Path(a[2]), e)[2])
    else: sys.exit(__doc__)
