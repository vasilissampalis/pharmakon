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
        nli = NLI(name); t1 = time.time(); pairs = 0; stopped = False
        for k, it in enumerate(todo):
            if minutes and time.time() - t0 > minutes * 60: stopped = True; break
            L = it["lines"]; premise = " ".join(t for t in [L.get("short") or "", L.get("but") or ""] + list(L.get("how") or []) if t)
            c = it["card"]; why = split(c.get("why") or "")
            pr = nli([(premise, c["statement"])] + [(premise, w) for w in why]); pairs += len(pr)
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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "exam":
        a = sys.argv[2:]; m = float(a[a.index("--minutes") + 1]) if "--minutes" in a else 0
        exam([x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--minutes")] or MODELS, m)
    elif len(sys.argv) > 2 and sys.argv[1] == "rule": rule(sys.argv[2])
    else: sys.exit(__doc__)
