#!/usr/bin/env python3
"""nli.py: a checker that costs nothing: does a passage ENTAIL a sentence? (docs/AUTOMATION.md)

    python3 -I scripts/auto/nli.py exam [MODEL ...]     (on GitHub's machine: writes data/auto/exam/nli-<model>.json)

The lane's checker must say whether a paper's passage supports a sentence. That is the task "natural language inference"
models are trained for: given a premise and a hypothesis, the model gives three numbers, entailment (the premise says it),
neutral (the premise does not say it) and contradiction. Such a model is small enough to run on GitHub's own machine, so
it costs none of the day's free allowance and can sit the WHOLE exam, every time.

This file runs open NLI models (DeBERTa-v3, trained on MNLI, FEVER, ANLI and others; MIT licence; fetched from Hugging
Face on GitHub's machine and kept there) and writes, for every card of the exam, the numbers for the card's statement and
for each sentence of its "why" against the answer's checked lines. Which rule on those numbers catches the wrong cards is
then worked out from that file (scripts/auto/nli.py rule), where anyone can repeat it.
"""
import sys, re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAM = ROOT / "data" / "auto" / "exam"
MODELS = ["MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli", "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"]
# (16 November 2026) The senior author: "if we can make our own ai we should that's what i was trying to do from the beginning, our own
# autonomous self expanding ai". A checker of our own begins here: small open models made for exactly our question ("does this
# passage support this sentence?"), run on GitHub's own machine with no key and no service. Each sits the whole exam; the best
# one is then trained further on our own checked record (scripts/auto/train_check.py, to come), and only a model that scores
# better on the exam than the one in use replaces it.
#   seq:   MiniCheck (Tang, Laban & Durrett, 2024; MIT): a classifier; the passage and the sentence joined by the tokenizer's end sign; the second of two numbers is "supported"
#   t5:    MiniCheck on Flan-T5: "predict: " before the same pair; the first step's numbers for two signs (3: no, 209: yes)
#   spans: LettuceDetect (KR Labs, 2025; MIT; the package "lettucedetect"): marks the WORDS of a sentence its passage does not carry
GROUNDED = {"lytang/MiniCheck-RoBERTa-Large": ("seq", 512), "lytang/MiniCheck-DeBERTa-v3-Large": ("seq", 1024), "lytang/MiniCheck-Flan-T5-Large": ("t5", 1024),
            "KRLabsOrg/lettucedect-large-modernbert-en-v1": ("spans", 4096), "KRLabsOrg/lettucedect-base-modernbert-en-v1": ("spans", 4096)}
split = lambda t: [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'])", t or "") if len(s.strip()) > 3]


class NLI:
    def __init__(self, name):
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        self.torch = torch; self.tok = AutoTokenizer.from_pretrained(name); self.m = AutoModelForSequenceClassification.from_pretrained(name); self.m.eval()
        self.labels = [self.m.config.id2label[i].lower() for i in range(self.m.config.num_labels)]
    def __call__(self, pairs):
        """[(premise, hypothesis)] -> [{"entailment", "neutral", "contradiction"}]"""
        out = []
        for i in range(0, len(pairs), 8):
            b = pairs[i:i + 8]
            x = self.tok([p for p, _ in b], [h for _, h in b], truncation="only_first", max_length=512, padding=True, return_tensors="pt")
            with self.torch.no_grad(): pr = self.torch.softmax(self.m(**x).logits, -1).tolist()
            out += [{l: round(v, 4) for l, v in zip(self.labels, row)} for row in pr]
        return out


class Grounded:
    """A model made to say whether a passage supports a sentence. Called like NLI: [(passage, sentence)] -> [{"entailment":
    how sure it is that the passage supports the sentence, "neutral": the rest, "contradiction": 0}], so that the same rule
    reads both kinds of file. A model that marks words also gives them ("spans")."""
    def __init__(self, name):
        import torch
        self.torch, self.name = torch, name; self.kind, self.most = GROUNDED[name]
        if self.kind == "spans":
            from lettucedetect.models.inference import HallucinationDetector
            self.det = HallucinationDetector(method="transformer", model_path=name); return
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
        self.tok = AutoTokenizer.from_pretrained(name)
        self.m = (AutoModelForSeq2SeqLM if self.kind == "t5" else AutoModelForSequenceClassification).from_pretrained(name); self.m.eval()
    def __call__(self, pairs):
        out = []
        if self.kind == "spans":
            for premise, sentence in pairs:
                try: sp = self.det.predict(context=[premise], question=None, answer=sentence, output_format="spans")
                except TypeError: sp = self.det.predict(context=[premise], question="", answer=sentence, output_format="spans")
                sp = [{"text": str(x.get("text") or "").strip()[:80], "p": round(float(x.get("confidence") or 0), 4)} for x in sp or []]
                worst = max([x["p"] for x in sp] or [0.0])
                out.append({"entailment": round(1 - worst, 4), "neutral": round(worst, 4), "contradiction": 0.0, "spans": sp[:6]})
            return out
        eos = self.tok.eos_token or self.tok.sep_token or ""
        for i in range(0, len(pairs), 4):
            b = pairs[i:i + 4]; texts = [("predict: " if self.kind == "t5" else "") + p + eos + h for p, h in b]
            x = self.tok(texts, truncation=True, max_length=self.most, padding=True, return_tensors="pt")
            with self.torch.no_grad():
                if self.kind == "t5":
                    start = self.torch.zeros((len(b), 1), dtype=self.torch.long)
                    pr = self.torch.softmax(self.m(**x, decoder_input_ids=start).logits[:, 0, [3, 209]], -1)[:, 1].tolist()
                else: pr = self.torch.softmax(self.m(**x).logits, -1)[:, 1].tolist()
            out += [{"entailment": round(v, 4), "neutral": round(1 - v, 4), "contradiction": 0.0} for v in pr]
        return out


def exam(names, minutes=0):
    """Every card of the exam through each model. The numbers are written as it goes and a run takes up where the last one
    stopped (the first try, on 15 November 2026, ran out of its 45 minutes with the large model and kept nothing)."""
    import time
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]; t0 = time.time()
    for name in names:
        out = EXAM / ("nli-" + re.sub(r"[^a-z0-9.-]+", "-", name.lower()).strip("-") + ".json")
        try: rows = json.load(open(out, encoding="utf-8"))["items"]
        except (OSError, ValueError, KeyError): rows = []
        have = {r["id"] for r in rows}; todo = [it for it in items if it["id"] not in have]
        if not todo: print(f"nli: {name}: all {len(rows)} cards were done before"); continue
        def keep(done):
            json.dump({"_note": "An NLI model's numbers for every card of the exam (scripts/auto/nli.py): the card's statement, and each sentence of its why, against the answer's checked lines.",
                       "model": name, "complete": done, "items": rows}, open(out, "w", encoding="utf-8"), ensure_ascii=False)
        try: nli = Grounded(name) if name in GROUNDED else NLI(name)
        except Exception as e: print(f"nli: {name}: could not be loaded ({type(e).__name__}: {str(e)[:200]})"); continue
        t1 = time.time(); pairs = 0; stopped = False
        for k, it in enumerate(todo):
            if minutes and time.time() - t0 > minutes * 60: stopped = True; break
            L = it["lines"]; premise = " ".join(t for t in [L.get("short") or "", L.get("but") or ""] + list(L.get("how") or []) if t)
            c = it["card"]; why = split(c.get("why") or "")
            try: pr = nli([(premise, c["statement"])] + [(premise, w) for w in why]); pairs += len(pr)
            except Exception as e: print(f"nli: {name}: stopped at card {it['id']} ({type(e).__name__}: {str(e)[:200]})"); stopped = True; break
            rows.append({"id": it["id"], "good": it["good"], "answer": c["answer"], "statement": pr[0], "why": pr[1:]})
            if k % 25 == 24: keep(False)
        keep(not stopped)
        print(f"nli: {name}: {len(rows)} of {len(items)} cards" + ("; the time for this run was up, the next run goes on" if stopped else "") + (f"; {(time.time() - t1) / max(pairs, 1):.2f} seconds a pair" if pairs else ""))
        if stopped: break


def rule(path):
    """Which rule on the numbers lets the fewest wrong cards through? Prints a table (run here, on the file GitHub wrote)."""
    d = json.load(open(path, encoding="utf-8")); rows = d["items"]; good = [r for r in rows if r["good"]]; bad = [r for r in rows if not r["good"]]
    print(d["model"], "|", len(good), "good cards,", len(bad), "wrong ones")
    def passes(r, t, ts):
        s = r["statement"]
        ok_s = s["entailment"] >= ts if r["answer"] else s["entailment"] < 0.5        # a "fact" must be said by the lines; a "myth" must not be
        return ok_s and all(w["entailment"] >= t for w in r["why"])
    for ts in (0.0, 0.5, 0.8):
        for t in (0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.98):
            bt = sum(passes(r, t, ts) for r in bad); gt = sum(passes(r, t, ts) for r in good); share = bt / (bt + gt) if bt + gt else 0
            print(f"  every why-sentence entailed >= {t:.2f}, a fact's statement >= {ts:.1f}: lets through {gt} of {len(good)} good and {bt} of {len(bad)} wrong: {100 * share:.1f} wrong in 100 let through; stops {100 * (1 - gt / len(good)):.0f} in 100 good ones")


def best(path):
    """One line for a finished file: the rule (a threshold for every sentence of the true part) that lets the fewest wrong cards through
    while it stops no more than 4 good cards in 10; and what the plain threshold of one half does."""
    d = json.load(open(path, encoding="utf-8")); rows = d["items"]; good = [r for r in rows if r["good"]]; bad = [r for r in rows if not r["good"]]
    if not good or not bad: return f"{d['model']}: {len(rows)} cards, not enough of both kinds to say"
    def passes(r, t):
        s = r["statement"]
        return (s["entailment"] >= t if r["answer"] else True) and all(w["entailment"] >= t for w in r["why"])     # a myth's statement is false on purpose: only its explanation is held against the lines
    rowsof = []
    for t in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
        bt = sum(passes(r, t) for r in bad); gt = sum(passes(r, t) for r in good)
        rowsof.append((t, len(bad) - bt, len(good) - gt, bt / (bt + gt) if bt + gt else 0.0))
    half = next(x for x in rowsof if x[0] == 0.5); ok = [x for x in rowsof if x[2] <= 0.4 * len(good)] or rowsof[:1]; b = min(ok, key=lambda x: (x[3], x[2]))
    say = lambda x: f"at {x[0]:.2f}: catches {x[1]} of {len(bad)} wrong cards, stops {x[2]} of {len(good)} good ones, {100 * x[3]:.1f} wrong in 100 let through"
    return f"{d['model']} ({len(rows)} cards{'' if d.get('complete') else ', not all yet'}): {say(half)}; its best rule, {say(b)}"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "exam":
        a = sys.argv[2:]; m = float(a[a.index("--minutes") + 1]) if "--minutes" in a else 0
        names = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--minutes")]
        if "--requests" in a:                                              # nli-*.json: {"models": ["lytang/MiniCheck-RoBERTa-Large", ...]}: read as data, never run
            names = []
            for f in sorted((ROOT / "data" / "auto" / "requests").glob("nli-*.json")):
                try: r = json.load(open(f, encoding="utf-8"))
                except ValueError: r = {}
                names += [x for x in (r.get("models") or []) if isinstance(x, str) and (x in GROUNDED or x in MODELS)]
        names = list(dict.fromkeys(names)) or MODELS
        exam(names, m)
        for name in names:
            p = EXAM / ("nli-" + re.sub(r"[^a-z0-9.-]+", "-", name.lower()).strip("-") + ".json")
            if p.exists(): print("exam:", best(p))
    elif len(sys.argv) > 2 and sys.argv[1] == "rule": rule(sys.argv[2])
    else: sys.exit(__doc__)
