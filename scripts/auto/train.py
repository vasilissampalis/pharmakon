#!/usr/bin/env python3
"""train.py: our own checker learns from the lessons (docs/AUTOMATION.md, decision 23, step two).

    python3 -I scripts/auto/train.py requests      (train-*.json in data/auto/requests, read as data:
                                                    {"from": "lytang/MiniCheck-RoBERTa-Large", "as": "pharmakon-check-1", "top": 4, "epochs": 2, "minutes": 80})
    python3 -I scripts/auto/train.py --selftest    (the part that needs no model: which lessons, what is kept apart, the weights)

Runs ONLY in the workshop job (.github/workflows/own.yml: it may read the repository and holds no key), like everything
that runs things fetched from outside.

What the model learns from (scripts/auto/teach.py):
  supported       the sentences a blind checker passed (the good cards' true parts, beside the lines they were written
                  from), the lane's sentences the editor judged good, and the faithful rewordings a free model wrote of them
  not supported   the made-up wrong sentences, one of each kind our checkers have named, written from those same sentences
What it never sees: any plain line of the third exam (lines.json: the measure), any wrong card, any sentence of the lane
the editor judged not good. Those are the exams, and a model cannot be measured on what it has learned from.

How: the open model named in "from" (the one that did best as it is) is the start. Only its top layers and its last step
are changed ("top"); the rest stays as its makers trained it, which is what a machine without a graphics card can do in an
hour or two, and what keeps the model from forgetting what it knew. One group of sentences in ten (a group is a card's
claim) is kept apart, never trained on, to watch the training: the weights that tell supported from not supported best on
that tenth are the ones kept. It is not a measure: its wrong sentences are made-up ones.

Then the model is made into a file of numbers (workshop.export) and sits the exams as that file (workshop.finish). The
numbers it carries are from the plain lines; own.py adopt compares them with the model in use, by the rule.
"""
import sys, os, re, json, math, time, random, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import teach

OUT = ROOT / "out"


def apart(group):
    """Is this group of sentences kept apart from the training, to watch it? One in ten, by its name, for good."""
    return int(hashlib.sha1(str(group).encode("utf-8")).hexdigest(), 16) % 10 == 0


def examples(src=None, lessons=None):
    """[{"premise", "sentence", "label" (1 supported, 0 not), "group", "kind"}] from the good sentences and the lessons made of them."""
    src = src if src is not None else teach.sources(); lessons = lessons if lessons is not None else teach.made()
    by = {s["id"]: s for s in src}; out = [{"premise": s["passages"], "sentence": s["sentence"], "label": 1, "group": s["group"], "kind": "as written"} for s in src]
    for x in lessons:
        s = by.get(x.get("from"))
        if not s or not x.get("sentence") or x.get("kind") not in teach.KINDS: continue        # a lesson whose sentence is no longer among the good ones is left out
        out.append({"premise": s["passages"], "sentence": x["sentence"], "label": 1 if x["kind"] == "same" else 0, "group": s["group"], "kind": x["kind"]})
    return out


def split(ex):
    return [e for e in ex if not apart(e["group"])], [e for e in ex if apart(e["group"])]


def weights(ex, most=4.0):
    """What a mistake on each label costs, so that the rarer label is not drowned: (for not supported, for supported), the rarer at most `most` times the other."""
    n1 = sum(e["label"] for e in ex); n0 = len(ex) - n1
    if not n0 or not n1: return (1.0, 1.0)
    return (1.0, round(min(most, n0 / n1), 3)) if n0 >= n1 else (round(min(most, n1 / n0), 3), 1.0)


def auc(scores, labels):
    """How often a supported sentence scores above one that is not (1 is always, 0.5 is chance)."""
    pos = [s for s, l in zip(scores, labels) if l]; neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg: return 0.5
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def train(base, name, top=4, epochs=2, minutes=80, batch=8, lr=2e-5, max_len=512, seed=1, ex=None, out=None, every=60):
    """Trains the top of an open classifier on the lessons; leaves the trained model in a folder; returns (the folder, what happened)."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    torch.manual_seed(seed); rnd = random.Random(seed); torch.set_num_threads(max(1, os.cpu_count() or 1))
    tok = AutoTokenizer.from_pretrained(base); m = AutoModelForSequenceClassification.from_pretrained(base)
    eos = tok.eos_token or tok.sep_token or "</s>"
    ex = ex if ex is not None else examples()
    text = lambda e: e["premise"] + eos + e["sentence"]
    fits = [e for e in ex if len(tok(text(e), truncation=False)["input_ids"]) <= max_len]            # a pair too long for the model would lose the end of its sentence: left out, and counted
    tr, watch = split(fits)
    if len(tr) < 16 or not watch or len({e["label"] for e in tr}) < 2: raise SystemExit(f"train: too few lessons to learn from ({len(tr)} to train on, {len(watch)} kept apart)")
    for p in m.parameters(): p.requires_grad = False
    layers = list(m.base_model.encoder.layer)
    for l in layers[-top:] if top else []:
        for p in l.parameters(): p.requires_grad = True
    for n_, p in m.named_parameters():
        if n_.split(".")[0] in ("classifier", "pooler"): p.requires_grad = True
    params = [p for p in m.parameters() if p.requires_grad]; names = {n_ for n_, p in m.named_parameters() if p.requires_grad}
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    lossf = torch.nn.CrossEntropyLoss(weight=torch.tensor(weights(tr), dtype=torch.float))
    enc = lambda items: tok([text(e) for e in items], padding=True, truncation=True, max_length=max_len, return_tensors="pt")

    def look():
        m.eval(); sc = []
        with torch.no_grad():
            for b in range(0, len(watch), 16): sc += torch.softmax(m(**enc(watch[b:b + 16])).logits, dim=-1)[:, 1].tolist()
        m.train(); return auc(sc, [e["label"] for e in watch])

    total = max(1, epochs * math.ceil(len(tr) / batch)); t0 = time.time(); step = 0; seen = []
    start = look(); best = (start, None); m.train(); stopped = ""
    for ep in range(epochs):
        rnd.shuffle(tr)
        for b in range(0, len(tr), batch):
            if time.time() - t0 > minutes * 60: stopped = "the time for training was up"; break
            for g in opt.param_groups: g["lr"] = lr * max(0.05, 1 - step / total)                 # the steps get smaller as the training goes on
            x = enc(tr[b:b + batch]); y = torch.tensor([e["label"] for e in tr[b:b + batch]])
            loss = lossf(m(**x).logits, y); loss.backward(); torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step(); opt.zero_grad(); step += 1
            if step % every == 0 or step == total:
                a = look(); seen.append((step, round(a, 4), round(float(loss), 4)))
                print(f"train: step {step} of {total}: on the tenth kept apart a supported sentence scores above a made-up wrong one {100 * a:.1f} times in 100 ({(time.time() - t0) / 60:.0f} minutes)", flush=True)
                if a > best[0]: best = (a, {k: v.detach().clone() for k, v in m.state_dict().items() if k in names})
        if stopped: break
    if best[1] is not None: m.load_state_dict(best[1], strict=False)
    m.eval(); folder = pathlib.Path(out or (OUT / "_trained")); folder.mkdir(parents=True, exist_ok=True)
    m.save_pretrained(str(folder)); tok.save_pretrained(str(folder))
    kinds = {}
    for e in tr: kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    what = {"from": base, "top_layers_changed": top, "epochs": epochs, "steps": step, "of_steps": total, "stopped": stopped, "lessons_trained_on": len(tr), "by_kind": kinds, "kept_apart_to_watch": len(watch),
            "left_out_too_long": len(ex) - len(fits), "weights": list(weights(tr)), "watch_before": round(start, 4), "watch_best": round(best[0], 4), "watch": seen[-12:], "minutes": round((time.time() - t0) / 60, 1),
            "kept": "the weights that did best on the tenth kept apart" if best[1] is not None else "the open model as it was: no step of the training did better on the tenth kept apart"}
    print(f"train: {name}: {step} steps on {len(tr)} lessons; on the tenth kept apart: {100 * start:.1f} in 100 before, {100 * best[0]:.1f} at best; {what['kept']}")
    return folder, what


def make(req):
    """One request: train, make into a file, sit the exams. Returns the candidate's record, or None."""
    import nli, workshop
    base, name = req.get("from"), req.get("as")
    if base not in nli.GROUNDED or nli.GROUNDED[base][0] != "seq" or not isinstance(name, str) or not re.fullmatch(r"pharmakon-[a-z]+-[0-9a-z.-]{1,20}", name):
        print("train: a request that names no classifier of the list, or no name of the form pharmakon-<job>-<number>: left alone"); return None
    num = lambda k, d, lo, hi: min(hi, max(lo, req[k])) if isinstance(req.get(k), (int, float)) and not isinstance(req.get(k), bool) else d
    folder, what = train(base, name, top=int(num("top", 4, 0, 12)), epochs=int(num("epochs", 2, 1, 6)), minutes=float(num("minutes", 80, 1, 200)), lr=float(num("lr", 2e-5, 1e-6, 1e-4)))
    nli.GROUNDED[str(folder)] = ("seq", nli.GROUNDED[base][1])
    entry = workshop.export(str(folder), name, quant=req.get("quant") is not False)
    entry.update({"from": base, "licence": "the open model's own (" + workshop.LICENCES.get(base, "see its page") + "); the training and the lessons are ours (NOTICE.md)",
                  "how": "the open model, with its top layers trained on our own lessons (scripts/auto/teach.py, train.py)", "trained": what})
    import shutil; shutil.rmtree(folder, ignore_errors=True)                # the trained model in its makers' form is large and is not kept: the file of numbers is the model
    return workshop.finish(entry, name, minutes=float(num("exam_minutes", 25, 1, 60)), lines_minutes=float(num("lines_minutes", 40, 0, 90)))


def selftest():
    src = [{"id": "cards:c1#0", "group": "cards:cl_a", "passages": "It can be so. Men said so.", "sentence": "It can be so."}, {"id": "cards:c2#0", "group": "cards:cl_b", "passages": "P2", "sentence": "S2"}]
    lessons = [{"from": "cards:c1#0", "kind": "measure", "sentence": "It often is so."}, {"from": "cards:c1#0", "kind": "same", "sentence": "So it can be."}, {"from": "cards:gone#0", "kind": "cause", "sentence": "x"},
               {"from": "cards:c2#0", "kind": "not a kind", "sentence": "y"}, {"from": "cards:c2#0", "kind": "wider", "sentence": ""}]
    ex = examples(src, lessons)
    assert [(e["sentence"], e["label"], e["kind"]) for e in ex] == [("It can be so.", 1, "as written"), ("S2", 1, "as written"), ("It often is so.", 0, "measure"), ("So it can be.", 1, "same")]      # a made-up wrong sentence is "not supported"; a faithful rewording stays supported; a lesson without its sentence or of no known kind is left out
    assert ex[2]["premise"] == "It can be so. Men said so." and ex[2]["group"] == "cards:cl_a"
    groups = [f"cards:cl_{n}" for n in range(400)]; kept = [g for g in groups if apart(g)]
    assert 20 <= len(kept) <= 60 and apart(kept[0]) and [apart(g) for g in groups] == [apart(g) for g in groups]                                 # about one group in ten, and always the same ones
    tr, watch = split([dict(e, group=g) for g in groups for e in ex[:1]]); assert len(watch) == len(kept) and not {e["group"] for e in tr} & set(kept)   # a group is never on both sides
    assert weights([{"label": 0}] * 6 + [{"label": 1}] * 2) == (1.0, 3.0) and weights([{"label": 0}] * 60 + [{"label": 1}] * 2) == (1.0, 4.0) and weights([{"label": 1}] * 4 + [{"label": 0}] * 2) == (2.0, 1.0) and weights([{"label": 1}]) == (1.0, 1.0)
    assert auc([0.9, 0.8, 0.2, 0.1], [1, 1, 0, 0]) == 1.0 and auc([0.1, 0.9], [1, 0]) == 0.0 and auc([0.5, 0.5], [1, 0]) == 0.5 and auc([0.3], [1]) == 0.5
    print("train selftest: ok (a made-up wrong sentence is a lesson in 'not supported', a faithful rewording stays supported; one group in ten is kept apart, always the same, and never on both sides; the rarer label weighs more, four times at most)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a and a[0] == "requests":
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("train-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            try: make(r if isinstance(r, dict) else {})
            except SystemExit as e: print(str(e))
            except Exception as e: print(f"train: {f.name}: not made ({type(e).__name__}: {str(e)[:300]})")
    else: sys.exit(__doc__)
