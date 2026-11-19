#!/usr/bin/env python3
"""train.py: Insight's own encoder, taught by our examples and by the teachers' wordings (docs/AUTOMATION.md, decision 37, stage two;
19 November 2026).

The senior author, 19 November 2026, 21:44: "we have to teach our ai to work like an llm and do what you do as perfect as possible it
has to work by itself perfectly all the time autonomously". Insight reads every question on the reader's own device with a small open
encoder. This teaches such an encoder the site's questions, as finetune.py did for pharmakon-insight-1 (2.3.0), with three changes:
  - the answers are the site's answers as they are now (site/insight/.cache/index-input.json: node site/build.js first), the machine
    lane's included, not the catalogue of 15 November;
  - the teachers' wordings are added (data/verification/insight/variants_teacher.json, data/auto/insight/teachers.json: the ways a person
    might type each answer's question, slang and typos too, written by the editor and the big free models from OUR wording, never a
    visitor's; --teacher);
  - the base can be another open encoder that reads with the page's own vocabulary and pooling (gte-small: MIT), fetched from Hugging
    Face at a fixed commit, whose files' SHA-256 are kept.
What it learns, as before: a way of asking is pulled towards the other ways of asking the same answer and away from every other
answer's, and from that answer's near-miss questions (questions that sound close and are not answered by it). No forum question and no
gold label is used: the gold set (400 forum questions, two blind readers) stays a fair test, and each model made here is measured on
it as encoders.py measures (the page's first look: 0.7 x the nearest wording + 0.3 x the short answer), beside the model on the site.
Nothing is shipped by this: a model goes to the page only with its own judge, tiers, build and checks (scripts/insight/MODELS.md).

    python3 -I scripts/insight/train.py --base minilm|gte-small --out DIR [--teacher] [--masked SHARE] [--epochs N] [--all]
            [--mix 0.5,1.0] [--from-onnx FILE] [--threads N] [--lr X] [--seed S] [--max-minutes M]
    python3 -I scripts/insight/train.py --selftest

--all trains on every answer (after a held-out run has shown how many passes help); without it, the examples of 15% of the answers
(by a hash of their id, the same rule as finetune.py) are held out and the best pass is kept. --mix writes one model per share of the
trained weights (the rest the base's: 0.5 is how pharmakon-insight-1 was made). --from-onnx reads the base's float weights from an
ONNX file instead of Hugging Face (all-MiniLM-L6-v2 only; the file finetune.py used).
"""
import sys, os, json, math, time, random, hashlib, pathlib, re, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[2]
V = ROOT / "data" / "verification" / "insight"
INPUT = ROOT / "site" / "insight" / ".cache" / "index-input.json"
VENDOR = ROOT / "site" / "insight" / "vendor"
VOCAB = VENDOR / "vocab.txt"
SITE_MODEL = VENDOR / json.load(open(ROOT / "site" / "insight" / "model.json", encoding="utf-8"))["file"]   # the model on the site, whatever its name

# Open encoders that read as the page reads: the page's vocabulary (BERT uncased), mean pooling, 384 numbers. Licences allow any use.
BASES = {
    "minilm": {"repo": "sentence-transformers/all-MiniLM-L6-v2", "licence": "Apache-2.0", "dim": 384},
    "gte-small": {"repo": "thenlper/gte-small", "licence": "MIT", "dim": 384},
}
BATCH, MAXLEN, SCALE, EVAL_LEN = 32, 48, 20.0, 128


def arg(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def log(*a):
    print("train:", *a, flush=True)


def held_out(answer_id):
    """The same 15% of the answers finetune.py holds out: by a hash of the id, so that it does not change between runs."""
    return int(hashlib.sha1(answer_id.encode()).hexdigest(), 16) % 100 < 15


def teacher_wordings():
    """Every teachers' file (data/verification/insight/variants_teacher.json: the editor's round 0; data/auto/insight/teachers.json:
    the free models', written every day by scripts/insight/teachers.py): {answer id: [wordings]}."""
    out = {}
    for f in sorted(V.glob("variants_teacher*.json")) + [ROOT / "data" / "auto" / "insight" / "teachers.json"]:
        if not f.exists(): continue
        try: d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): log(f"{f.name} could not be read: left out"); continue
        for k, ws in (d.get("variants") or {}).items():
            out.setdefault(k, []).extend(w["w"] if isinstance(w, dict) else w for w in ws if (isinstance(w, str) and w.strip()) or (isinstance(w, dict) and w.get("w")))
    return out


def examples(use_teacher):
    """The answers, the ways of asking each (P), its near-miss questions (N), and which wordings are which (for the held-out test,
    which reads only the readers' wordings, never the teachers', so that every model is tested on the same questions)."""
    A = [a for a in json.load(open(INPUT, encoding="utf-8"))["answers"] if a.get("wordings") and a.get("short")]
    var = json.load(open(V / "variants_reader696.json", encoding="utf-8")).get("variants") or {}
    more, near = {}, {}
    for f in sorted(V.glob("nearmiss_*.json")):
        for k, v in (json.load(open(f, encoding="utf-8")).get("items") or {}).items():
            more.setdefault(k, []).extend(w for w in (v.get("more") or []) if isinstance(w, str) and w.strip())
            near.setdefault(k, []).extend(w for w in (v.get("near") or []) if isinstance(w, str) and w.strip())
    tea = teacher_wordings() if use_teacher else {}
    if use_teacher:   # the near-miss questions the free models wrote (scripts/insight/teachers.py; a model of another family said each asks something else)
        try: tn = json.load(open(ROOT / "data" / "auto" / "insight" / "teachers.json", encoding="utf-8")).get("near") or {}
        except (OSError, ValueError): tn = {}
        for k, ws in tn.items(): near.setdefault(k, []).extend(w["w"] for w in ws if isinstance(w, dict) and w.get("w"))
    P, N, R, T = [], [], [], []
    for a in A:
        readers = list(dict.fromkeys([w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()] + more.get(a["id"], [])))
        site = list(dict.fromkeys(a["wordings"]))
        t = [w for w in dict.fromkeys(tea.get(a["id"], [])) if w not in site and w not in readers]
        P.append(list(dict.fromkeys(site + readers + t))); R.append([w for w in readers if w not in site]); T.append(t)
        N.append(list(dict.fromkeys(near.get(a["id"], []))))
    return A, P, N, R, T


def gold():
    G = json.load(open(V / "gold-sample.json", encoding="utf-8"))["questions"]
    L = [{x["n"]: x for x in json.load(open(V / f"gold_reader{r}.json", encoding="utf-8"))["labels"]} for r in ("693", "694")]
    ans = lambda x: set(x.get("answers") or []); part = lambda x: set(x.get("answers") or []) | set(x.get("partly") or [])
    yes = lambda x: bool(part(x)) and not x.get("none")
    rows = []
    for q in G:
        n = q["n"]
        if n not in L[0] or n not in L[1]: continue
        a, b = L[0][n], L[1][n]
        rows.append({"n": n, "q": q["question"], "strict": ans(a) | ans(b), "lenient": part(a) | part(b), "none": not yes(a) and not yes(b)})
    return rows


def auc(pos, neg):
    if not pos or not neg: return None
    allv = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg]); r = 0.0; i = 0
    while i < len(allv):
        j = i
        while j < len(allv) and allv[j][0] == allv[i][0]: j += 1
        r += (i + j + 1) / 2.0 * sum(1 for k in range(i, j) if allv[k][1] == 1); i = j
    return (r - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


class OnnxEncoder:
    """An encoder file as the page runs it: the page's vocabulary, at most 128 tokens, mean pooling, unit length."""
    def __init__(self, path, threads=None):
        import onnxruntime as ort
        from tokenizers import BertWordPieceTokenizer
        so = ort.SessionOptions(); so.intra_op_num_threads = threads or os.cpu_count() or 2
        self.s = ort.InferenceSession(str(path), so, providers=["CPUExecutionProvider"]); self.inputs = {i.name for i in self.s.get_inputs()}
        self.tok = BertWordPieceTokenizer(str(VOCAB), lowercase=True); self.tok.enable_truncation(EVAL_LEN)

    def __call__(self, texts):
        import numpy as np
        out = []
        for t in texts:
            e = self.tok.encode(t); ids = np.array([e.ids], dtype=np.int64); mask = np.ones_like(ids)
            feeds = {"input_ids": ids, "attention_mask": mask}
            if "token_type_ids" in self.inputs: feeds["token_type_ids"] = np.zeros_like(ids)
            v = self.s.run(None, feeds)[0][0].mean(axis=0); out.append(v / max(float(np.linalg.norm(v)), 1e-9))
        return np.stack(out).astype("float32")


def gold_eval(enc, A, index_wordings, G):
    """The page's first look on the gold set, as encoders.py measures it: per answer the nearest of its wordings (0.7) and its short
    answer (0.3). Strict: an answer that either blind reader judged to answer the question as asked; lenient: also in part."""
    import numpy as np
    t0 = time.time(); rows, W = [], []
    for i, ws in enumerate(index_wordings):
        for w in ws: rows.append(i); W.append(w)
    Wv = enc(W); Sv = enc([a["short"] for a in A]); Qv = enc([g["q"] for g in G])
    rows = np.array(rows); best_w = np.full((len(G), len(A)), -1.0, dtype=np.float32); sims = Qv @ Wv.T
    for i in range(len(A)):
        k = np.where(rows == i)[0]
        if len(k): best_w[:, i] = sims[:, k].max(axis=1)
    score = 0.7 * best_w + 0.3 * (Qv @ Sv.T); ids = [a["id"] for a in A]
    s1 = s3 = l1 = l3 = ns = nl = 0; top = []; per = {}
    for qi, g in enumerate(G):
        order = np.argsort(-score[qi])[:3]; got = [ids[k] for k in order]; top.append(float(score[qi][order[0]]))
        per[g["n"]] = [got[0], round(top[-1], 4)]
        if g["strict"]: ns += 1; s1 += got[0] in g["strict"]; s3 += bool(set(got) & g["strict"])
        if g["lenient"]: nl += 1; l1 += got[0] in g["lenient"]; l3 += bool(set(got) & g["lenient"])
    can = [top[i] for i, g in enumerate(G) if g["lenient"] and not g["none"]]; cannot = [top[i] for i, g in enumerate(G) if g["none"]]
    return {"strict_top1": round(s1 / max(ns, 1), 3), "strict_top3": round(s3 / max(ns, 1), 3), "lenient_top1": round(l1 / max(nl, 1), 3),
            "lenient_top3": round(l3 / max(nl, 1), 3), "n_strict": ns, "n_lenient": nl, "answerable_vs_not_auc": round(auc(can, cannot) or 0, 3),
            "seconds": round(time.time() - t0, 1)}, per


def selftest():
    assert held_out("cl_meth_pk_halflife") in (True, False)
    assert round(auc([0.9, 0.8], [0.1, 0.85]), 3) == 0.75, auc([0.9, 0.8], [0.1, 0.85])
    share = sum(held_out(f"x{i}") for i in range(2000)) / 2000; assert 0.11 < share < 0.19, share
    if INPUT.exists():
        A, P, N, R, T = examples(True)
        assert len(A) == len(P) == len(N) == len(R) == len(T)
        for a, p, r, t in zip(A, P, R, T):
            assert all(w in p for w in a["wordings"]) and all(w in p for w in r) and all(w in p for w in t)
            assert not set(t) & set(r) and not set(t) & set(a["wordings"])
        G = gold(); gq = {re.sub(r"[^a-z0-9 ]", "", g["q"].lower()).strip() for g in G}
        leak = [w for t in T for w in t if re.sub(r"[^a-z0-9 ]", "", w.lower()).strip() in gq]
        assert not leak, f"a teacher's wording is a gold question: {leak[:3]}"
    print("train selftest: ok")


def main():
    if "--selftest" in sys.argv: return selftest()
    import numpy as np, torch
    base = arg("--base", "minilm"); assert base in BASES, f"--base must be one of {list(BASES)}"
    OUT = pathlib.Path(arg("--out", "insight-train")); OUT.mkdir(parents=True, exist_ok=True)
    EPOCHS = int(arg("--epochs", "6")); LR = float(arg("--lr", "2e-5")); SEED = int(arg("--seed", "7"))
    MASKED = float(arg("--masked", "0")); ALL = "--all" in sys.argv; TEACH = "--teacher" in sys.argv
    MIX = [float(x) for x in arg("--mix", "0.5,1.0").split(",") if x.strip()]
    STOP = time.time() + 60 * float(arg("--max-minutes", "330"))
    torch.manual_seed(SEED); random.seed(SEED); np.random.seed(SEED); torch.set_num_threads(int(arg("--threads", str(os.cpu_count() or 2))))
    from tokenizers import BertWordPieceTokenizer
    tok = BertWordPieceTokenizer(str(VOCAB), lowercase=True); tok.enable_truncation(MAXLEN); tok.enable_padding()
    record = {"base": base, "licence": BASES[base]["licence"], "teacher": TEACH, "masked": MASKED, "epochs": EPOCHS, "lr": LR, "seed": SEED, "batch": BATCH,
              "max_tokens": MAXLEN, "all_answers": ALL, "mix": MIX, "began": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # ---------- the base ----------
    if arg("--from-onnx"):
        assert base == "minilm", "--from-onnx reads all-MiniLM-L6-v2's float file only"
        import onnx
        from onnx import numpy_helper
        from transformers import BertConfig, BertModel
        f = pathlib.Path(arg("--from-onnx")); m = onnx.load(str(f)); init = {i.name: numpy_helper.to_array(i) for i in m.graph.initializer}
        cfg = BertConfig(vocab_size=30522, hidden_size=384, num_hidden_layers=6, num_attention_heads=12, intermediate_size=1536, max_position_embeddings=512,
                         type_vocab_size=2, hidden_act="gelu", layer_norm_eps=1e-12, hidden_dropout_prob=0.1, attention_probs_dropout_prob=0.1)
        model = BertModel(cfg, add_pooling_layer=False)
        sd = {k: torch.tensor(v.copy()) for k, v in init.items() if not k.startswith("onnx::") and k != "embeddings.position_ids"}
        for n in m.graph.node:
            if n.op_type == "MatMul" and n.input[1] in init:
                sd[n.output[0].split("/MatMul")[0].strip("/").replace("/", ".") + ".weight"] = torch.tensor(init[n.input[1]].T.copy())
        missing, unexpected = model.load_state_dict(sd, strict=False)
        assert not unexpected and all("position_ids" in k or "token_type_ids" in k for k in missing), (missing, unexpected)
        record["source"] = {"file": f.name, "sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "bytes": f.stat().st_size}
    else:
        from huggingface_hub import HfApi, hf_hub_download
        from transformers import AutoModel
        repo = BASES[base]["repo"]; info = HfApi().model_info(repo); files = {s.rfilename for s in info.siblings or []}
        vocab = hf_hub_download(repo, "vocab.txt", revision=info.sha)
        assert pathlib.Path(vocab).read_text(encoding="utf-8").split("\n") == VOCAB.read_text(encoding="utf-8").split("\n"), f"{repo} does not read with the page's vocabulary"
        weights = "model.safetensors" if "model.safetensors" in files else "pytorch_model.bin"
        wf = hf_hub_download(repo, weights, revision=info.sha)
        kw = {"revision": info.sha, "attn_implementation": "eager"}   # plain attention: it is written to ONNX as the page's file is
        model = AutoModel.from_pretrained(repo, add_pooling_layer=False, **kw) if "bert" in str((info.config or {}).get("model_type", "bert")) else AutoModel.from_pretrained(repo, **kw)
        record["source"] = {"repo": repo, "commit": info.sha, "weights": weights, "sha256": hashlib.sha256(open(wf, "rb").read()).hexdigest(), "bytes": os.path.getsize(wf),
                            "licence_on_the_hub": getattr(getattr(info, "card_data", None), "license", None)}
        for f in ("LICENSE", "LICENSE.txt", "README.md"):   # the base's own licence and card, kept beside the model for its NOTICE
            if f in files:
                try: OUT.joinpath("base-" + f.replace(".md", ".txt").replace("LICENSE.txt", "LICENSE")).write_bytes(open(hf_hub_download(repo, f, revision=info.sha), "rb").read()[:200000])
                except Exception as e_: log(f"{f} of the base could not be kept: {e_}")
    log("base", json.dumps(record["source"]))

    def encode(texts, grad=False, bs=64):
        outs = []
        for i in range(0, len(texts), bs):
            e = tok.encode_batch(texts[i:i + bs])
            ii = torch.tensor([x.ids for x in e]); am = torch.tensor([x.attention_mask for x in e])
            with torch.set_grad_enabled(grad):
                h = model(input_ids=ii, attention_mask=am, token_type_ids=torch.zeros_like(ii)).last_hidden_state
                m_ = am.unsqueeze(-1).float(); v = (h * m_).sum(1) / m_.sum(1).clamp(min=1e-9)
                outs.append(torch.nn.functional.normalize(v, dim=-1))
        return torch.cat(outs)

    # ---------- the examples ----------
    A, P, N, R, T = examples(TEACH)
    val = np.array([held_out(a["id"]) for a in A])
    site_q = [set(a["wordings"]) for a in A]
    ex = [(ai, w) for ai in range(len(A)) for w in P[ai] if w not in site_q[ai]]
    tr_ex = [x for x in ex if ALL or not val[x[0]]]
    record.update({"answers": len(A), "held_out_answers": int(val.sum()), "anchors": len(tr_ex), "readers_wordings": sum(len(r) for r in R),
                   "teachers_wordings": sum(len(t) for t in T), "near_miss": sum(len(n) for n in N)})
    log(f"{len(A)} answers; {len(tr_ex)} wordings as anchors ({record['teachers_wordings']} of them the teachers'); {record['near_miss']} near-miss questions; held out {int(val.sum())}")
    # the held-out test: the readers' wordings of the held-out answers, against every answer's site and readers' wordings
    Dtxt = [w for ai in range(len(A)) for w in list(dict.fromkeys(list(site_q[ai]) + R[ai]))]
    Down = np.array([ai for ai in range(len(A)) for _ in list(dict.fromkeys(list(site_q[ai]) + R[ai]))])
    pos_of = {(int(Down[j]), w): j for j, w in enumerate(Dtxt)}

    def validate():
        model.eval(); D = encode(Dtxt).numpy()
        q = [(ai, w, 1) for ai in range(len(A)) if val[ai] for w in R[ai]] + [(ai, w, 0) for ai in range(len(A)) if val[ai] for w in N[ai]]
        if not q: return float("nan"), float("nan")
        Q = encode([w for _, w, _ in q]).numpy(); S = Q @ D.T; hit, own_pos, own_neg = [], [], []
        for r, (ai, w, y) in enumerate(q):
            row = S[r].copy()
            if y and (ai, w) in pos_of: row[pos_of[(ai, w)]] = -9
            own = row[Down == ai].max()
            if y: hit.append(Down[row.argmax()] == ai); own_pos.append(float(own))
            else: own_neg.append(float(own))
        return float(np.mean(hit)), (auc(own_pos, own_neg) or float("nan"))

    mask = None
    if MASKED:
        spec = importlib.util.spec_from_file_location("bi", ROOT / "scripts/insight/build_index.py"); bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)
        _pat = bi.name_pattern([n for n, _ in bi.names_table()]); mask = lambda t: _pat.sub("it", t)
    acc0, auc0 = validate(); record["before"] = {"held_out_finds_answer": round(acc0, 4), "held_out_auc": round(auc0, 4)}
    log(f"before: held-out wordings find their answer {100 * acc0:.1f}%, wording vs near-miss AUC {auc0:.3f}")
    SAME = None
    if MASKED:
        Dall = [w for ws in P for w in ws]; Oall = np.array([i for i, ws in enumerate(P) for _ in ws])
        Wm = encode([mask(t) for t in Dall]).numpy(); SAME = np.zeros((len(A), len(A)), bool)
        for ai in range(len(A)):
            rows = np.flatnonzero(Oall == ai)
            if not len(rows): continue
            s = (Wm[rows] @ Wm.T).max(0); best = np.full(len(A), -1.0); np.maximum.at(best, Oall, s); SAME[ai] = best >= 0.8
        np.fill_diagonal(SAME, False); SAME |= SAME.T

    # ---------- training ----------
    orig = {k: v.detach().clone() for k, v in model.state_dict().items()}
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    steps = EPOCHS * math.ceil(len(tr_ex) / BATCH)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / max(1, int(0.1 * steps)), max(0.0, (steps - s) / max(1, steps - int(0.1 * steps)))))
    fin = lambda x: x if x == x else 0.0
    best = (acc0 + fin(auc0), 0); torch.save(model.state_dict(), OUT / "best.pt"); t0 = time.time(); curve = []
    for ep in range(1, EPOCHS + 1):
        if time.time() > STOP: log("out of time: no more passes"); break
        model.train(); random.shuffle(tr_ex); tot = 0.0; nb = 0; pool = list(tr_ex)
        while pool:
            batch, seen, rest = [], set(), []
            for x in pool:   # one anchor per answer in a batch, so that no other row's positive is secretly right
                if x[0] not in seen and len(batch) < BATCH: batch.append(x); seen.add(x[0])
                else: rest.append(x)
            pool = rest
            if len(batch) < 4: break
            masked = MASKED > 0 and random.random() < MASKED
            T_ = mask if masked else (lambda t: t)
            anchors = [T_(w) for _, w in batch]
            positives = [T_(random.choice([p for p in P[ai] if p != w] or [w])) for ai, w in batch]
            negs = [T_(random.choice(N[ai])) if N[ai] else None for ai, _ in batch]; neg_txt = [n for n in negs if n is not None]
            ea = encode(anchors, grad=True); ep_ = encode(positives, grad=True)
            cand = torch.cat([ep_, encode(neg_txt, grad=True)]) if neg_txt else ep_
            target = torch.arange(len(batch)); logits = ea @ cand.T * SCALE; back = (ep_ @ ea.T) * SCALE
            if masked:   # its own positive, its own near-miss question, and the positives of answers that do not ask the same of another drug
                rows_ai = np.array([ai for ai, _ in batch]); neg_row = [r for r, n in enumerate(negs) if n is not None]
                allow = np.zeros((len(batch), len(batch) + len(neg_txt)), bool)
                allow[:, :len(batch)] = ~SAME[np.ix_(rows_ai, rows_ai)]; allow[np.arange(len(batch)), np.arange(len(batch))] = True
                for c, r in enumerate(neg_row): allow[r, len(batch) + c] = True
                am_ = torch.tensor(allow); logits = logits.masked_fill(~am_, -1e4); back = back.masked_fill(~am_[:, :len(batch)].T, -1e4)
            loss = torch.nn.functional.cross_entropy(logits, target) + 0.5 * torch.nn.functional.cross_entropy(back, target)
            opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step()
            tot += float(loss.detach()); nb += 1
        acc, au = validate(); curve.append({"pass": ep, "loss": round(tot / max(1, nb), 4), "held_out_finds_answer": round(acc, 4), "held_out_auc": round(au, 4), "seconds": round(time.time() - t0)})
        log(f"pass {ep}: loss {tot / max(1, nb):.3f} | held out{' (now trained on)' if ALL else ''}: finds its answer {100 * acc:.1f}%, AUC {au:.3f} | {time.time() - t0:.0f}s")
        if ALL or acc + fin(au) > best[0]: best = (acc + fin(au), ep); torch.save(model.state_dict(), OUT / "best.pt")
    record["passes"] = curve; record["kept_pass"] = best[1]
    trained = torch.load(OUT / "best.pt")

    # ---------- models: one per share of the trained weights; ONNX as the page loads it (same inputs and output), and int8 ----------
    from onnxruntime.quantization import quantize_dynamic, QuantType

    class Wrap(torch.nn.Module):
        def __init__(self, m): super().__init__(); self.m = m
        def forward(self, input_ids, attention_mask, token_type_ids):
            return self.m(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids).last_hidden_state

    G = gold(); idx_std = [list(dict.fromkeys(list(a["wordings"]) + [w for w in R[i] if w])) for i, a in enumerate(A)]
    T_all = teacher_wordings()   # (for the second measure, whether or not this model learned from them: would they help in the index?)
    idx_tea = [list(dict.fromkeys(idx_std[i] + [w for w in T_all.get(a["id"], []) if w not in idx_std[i]])) for i, a in enumerate(A)]
    record["gold"] = {}; per_q = {}
    if SITE_MODEL.exists():
        enc = OnnxEncoder(SITE_MODEL); r1, p1 = gold_eval(enc, A, idx_std, G); r2, _ = gold_eval(enc, A, idx_tea, G)
        record["gold"]["pharmakon-insight-1 (on the site)"] = {"index": r1, "index_with_teachers_wordings": r2, "sha256": hashlib.sha256(SITE_MODEL.read_bytes()).hexdigest()}
        per_q["pharmakon-insight-1"] = p1; log("site model:", json.dumps(r1))
    for alpha in MIX:
        sd = {k: (1 - alpha) * orig[k] + alpha * trained[k] if orig[k].is_floating_point() else trained[k] for k in orig}
        model.load_state_dict(sd); model.eval()
        name = f"{base}{'-teach' if TEACH else ''}{'-masked' if MASKED else ''}-mix{int(round(alpha * 100))}"
        fp = OUT / f"{name}-fp32.onnx"; q8 = OUT / f"{name}-q8.onnx"
        e = tok.encode_batch(["a short example", "another, slightly longer example question"]); ii = torch.tensor([x.ids for x in e]); am = torch.tensor([x.attention_mask for x in e])
        torch.onnx.export(Wrap(model).eval(), (ii, am, torch.zeros_like(ii)), str(fp), input_names=["input_ids", "attention_mask", "token_type_ids"], output_names=["last_hidden_state"],
                          dynamic_axes={k: {0: "batch", 1: "sequence"} for k in ("input_ids", "attention_mask", "token_type_ids", "last_hidden_state")},
                          opset_version=14, do_constant_folding=True, dynamo=False)
        model.eval()   # the export gives the wrapper back the mode it had, and the wrapper hands it down: without this, dropout would be on below
        quantize_dynamic(str(fp), str(q8), weight_type=QuantType.QUInt8)
        probe = ["does molly mess up your memory", "How many deaths does alcohol cause worldwide?", "xanax", "is weed a gateway drug"]
        ref = encode(probe).numpy(); got = OnnxEncoder(q8)(probe); cos = (ref * got).sum(1)
        assert float(cos.min()) > 0.95, f"the int8 file does not compute what the trained model computes: {cos}"
        enc = OnnxEncoder(q8); r1, p1 = gold_eval(enc, A, idx_std, G); r2, _ = gold_eval(enc, A, idx_tea, G); per_q[name] = p1
        record["gold"][name] = {"index": r1, "index_with_teachers_wordings": r2, "share_trained": alpha, "int8_vs_trained_cosine_min": round(float(cos.min()), 4),
                                "file": q8.name, "bytes": q8.stat().st_size, "sha256": hashlib.sha256(q8.read_bytes()).hexdigest()}
        log(name, json.dumps(r1), "| with the teachers' wordings in the index:", json.dumps(r2))
        fp.unlink()
    record["ended"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    json.dump(record, open(OUT / "train.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(per_q, open(OUT / "gold-first.json", "w", encoding="utf-8"), ensure_ascii=False)
    log("done:", OUT / "train.json")


if __name__ == "__main__":
    main()
