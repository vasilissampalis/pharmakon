#!/usr/bin/env python3
"""workshop.py: where a model of our own is made and sits the exam as the very file the lane will run (decision 23).

    python3 -I scripts/auto/workshop.py requests          (own-*.json in data/auto/requests, read as data:
                                                           {"do": "export", "model": "<an open model on GROUNDED's list>", "as": "pharmakon-check-0"})
    python3 -I scripts/auto/workshop.py sit NAME DIR       (the exam for files already made: DIR/NAME.onnx, DIR/NAME.tokenizer.json)
    python3 -I scripts/auto/workshop.py --selftest

Runs ONLY in the workshop job (.github/workflows/own.yml), which may read the repository and holds no key: this is the
one place where things fetched from outside (an open model, torch, transformers) are run. What leaves it is a folder of
plain files (out/): the model as a file of numbers (ONNX, its weights as 8-bit numbers so that it is small and quick on
one machine), its tokenizer's table, and a candidate's record with the SHA-256 of both and the model's numbers on the
whole exam, sat AS THAT FILE with the same code the lane runs (scripts/auto/own.py). The second job of the workflow, which
runs nothing from outside, puts the files among this repository's release files and the record into
data/auto/own/candidates/. Adopting a candidate is a separate step with its own rule (own.py adopt).

The exam here: every card's true part (a fact's statement and each sentence of its explanation; for a myth only the
explanation, because a myth's statement is false on purpose) against the lines the card was written from. A card is let
through when every such sentence scores at least the threshold. The threshold a candidate carries is the one that lets
the fewest wrong cards through among those that stop no more than one good card in four.
"""
import sys, re, json, time, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import own, nli

EXAM = ROOT / "data" / "auto" / "exam"
OUT = ROOT / "out"
THRESHOLDS = (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95)
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
    ok = [x for x in out if x["good_stopped"] <= 0.25 * len(good)] or out[:1]
    return out, min(ok, key=lambda x: (x["wrong_through"], x["good_stopped"]))


def sit(name, folder, entry, minutes=0):
    """The whole exam for the files in folder, with the lane's own code. Returns (rows, the table, the row it carries)."""
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]; t0 = time.time()
    chk = own.Check(entry=entry, files={"model": folder / (name + ".onnx"), "tokenizer": folder / (name + ".tokenizer.json")})
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
                      dynamic_axes={"input_ids": {0: "n", 1: "t"}, "attention_mask": {0: "n", 1: "t"}, "logits": {0: "n"}}, opset_version=17)
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
    rows, tb, pick, whole, secs = sit(name, OUT, dict(entry, files=files), minutes)
    entry = dict(entry, files=files, threshold=pick["threshold"], exam=dict(pick, whole=whole, seconds_a_sentence=round(secs, 2)), exam_table=tb)
    json.dump(entry, open(OUT / (name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"_note": "The scores of " + name + " for the true part of every card of the exam (scripts/auto/workshop.py).", "items": rows}, open(OUT / (name + ".scores.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"workshop: {name} (from {entry['from']}, {files['model']['bytes'] / 1e6:.0f} MB): at {pick['threshold']}: lets {pick['wrong_through']} of {pick['wrong']} wrong cards through, stops {pick['good_stopped']} of {pick['good']} good ones"
          + ("" if whole else "; NOT the whole exam (time was up)") + f"; {secs:.2f} seconds a sentence")
    return entry


def selftest():
    c = {"statement": "Alcohol is addictive.", "answer": True, "why": "True. Many people become dependent. It was one survey."}
    assert true_part(c) == [("Alcohol is addictive.", "statement"), ("Many people become dependent.", "why"), ("It was one survey.", "why")]
    assert true_part(dict(c, answer=False)) == [("Many people become dependent.", "why"), ("It was one survey.", "why")]          # a myth's statement is false on purpose
    rows = [{"good": True, "scores": [0.9, 0.8]}] * 6 + [{"good": True, "scores": [0.9, 0.35]}] * 2 + [{"good": False, "scores": [0.9, 0.3]}] * 3 + [{"good": False, "scores": [0.95, 0.9]}]
    tb, pick = table(rows)
    at = {x["threshold"]: x for x in tb}
    assert at[0.3]["wrong_through"] == 4 and at[0.4]["wrong_through"] == 1 and at[0.4]["good_stopped"] == 2 and at[0.95]["good_stopped"] == 8
    assert pick["threshold"] == 0.4 and pick["wrong_through"] == 1 and pick["good_stopped"] == 2, pick          # the fewest wrong cards through among thresholds that stop no more than one good card in four
    print("workshop selftest: ok (a card's true part: a myth's statement is left out; the threshold a candidate carries lets the fewest wrong cards through while it stops no more than one good card in four)")


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
    elif len(a) == 3 and a[0] == "sit":
        e = json.load(open(pathlib.Path(a[2]) / (a[1] + ".json"), encoding="utf-8")); print(sit(a[1], pathlib.Path(a[2]), e)[2])
    else: sys.exit(__doc__)
