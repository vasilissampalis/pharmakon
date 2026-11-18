"""pair.py MODELS_DIR IN.json INDEX.json --out DIR [--epochs N] [--fold F | --all] [--eval-only] [--limit N]: a second look at
the question and the answer TOGETHER (Pharmakon Insight, 18 November 2026).

Why. The senior author, 18 November 2026, 22:15, of a question the page answered with something else: "it think it knows but
it does not. the app should understand that this is a question it does not know (we have to make this function as accurate
as it gets it is not accurate enough)". Measured that evening (scripts/insight/build_index.py --eval): of the 40 gold
questions the page gives a best match, 24 get a full answer, 10 a partial one and 6 a wrong one; 147 of 1,810 near-miss
questions get the very answer they do not ask for; "can you die from nitrous oxide" got the answer about nerve damage with
the judge at 0.93. The judge (scripts/insight/judge2.py) only sees how near the question is to an answer's wordings and how
far ahead that answer is of the next: it cannot see WHAT is asked against WHAT is answered. A model that reads the two
together can.

What. The open cross-encoder ms-marco-MiniLM-L-6-v2 (Apache-2.0; float weights read from its official ONNX file) is taught
with this site's own examples only, the same ones the judge learned from:
  yes: a way people ask (the phrasings writer's, the near-miss readers' hurried wordings) with its own answer;
  no:  a near-miss question (readers 707, 708, 725: "sounds close, is not answered by this answer") with that answer;
       and a way of asking with the other answers that rank highest for it on the page.
The answer is read as the site shows it: its question and its short answer. No gold question is used for training.
Measured: on the examples of answers held out of training (--fold), and on the gold set (400 real forum questions, two
blind readers), as a veto on the page's best match and as a second ordering of the page's first five.
Nothing here changes the site: it writes its numbers and the trained weights to --out."""
import sys, json, pathlib, hashlib, time, random, glob, math
import numpy as np, torch, onnx
from onnx import numpy_helper
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
M_DIR, IN_F, IDX_F = pathlib.Path(ARGS[0]), ARGS[1], ARGS[2]
OUT = pathlib.Path(opt("--out")); OUT.mkdir(parents=True, exist_ok=True)
EPOCHS = int(opt("--epochs", "3")); LR = float(opt("--lr", "2e-5")); SEED = int(opt("--seed", "7")); BATCH = 32; MAXLEN = 96; K = 5
FOLD = None if "--all" in sys.argv else int(opt("--fold", "0")); LIMIT = int(opt("--limit", "0")); THREADS = int(opt("--threads", "2"))
sys.argv = [sys.argv[0]]
import build_index as bi
ROOT = bi.ROOT
torch.manual_seed(SEED); random.seed(SEED); np.random.seed(SEED); torch.set_num_threads(THREADS)
FP32 = M_DIR / "_kontexta-reranker-model/package/models/Xenova/ms-marco-MiniLM-L-6-v2/onnx/model.onnx"
from transformers import BertConfig, BertForSequenceClassification
from tokenizers import BertWordPieceTokenizer
tok = BertWordPieceTokenizer(str(bi.VENDOR / "vocab.txt"), lowercase=True); tok.enable_truncation(MAXLEN, strategy="longest_first"); tok.enable_padding()
log = lambda *a: print(*a, flush=True)

def load_model():
    m = onnx.load(str(FP32)); init = {i.name: numpy_helper.to_array(i) for i in m.graph.initializer}
    cfg = BertConfig(vocab_size=30522, hidden_size=384, num_hidden_layers=6, num_attention_heads=12, intermediate_size=1536, max_position_embeddings=512,
                     type_vocab_size=2, hidden_act="gelu", layer_norm_eps=1e-12, hidden_dropout_prob=0.1, attention_probs_dropout_prob=0.1, num_labels=1)
    model = BertForSequenceClassification(cfg)
    sd = {k: torch.tensor(v.copy()) for k, v in init.items() if not k.startswith("onnx::") and not k.endswith("position_ids")}
    for nd in m.graph.node:   # the dense layers' weights are stored under made-up names; each MatMul's place in the graph says which layer it is
        if nd.op_type == "MatMul" and nd.input[1] in init:
            mod = nd.output[0].split("/MatMul")[0].strip("/").replace("/", ".")
            sd[mod + ".weight"] = torch.tensor(init[nd.input[1]].T.copy())
    missing, unexpected = model.load_state_dict(sd, strict=False)
    assert not unexpected and all("position_ids" in k or "token_type_ids" in k for k in missing), (missing, unexpected)
    return model

def batch_of(pairs):
    e = tok.encode_batch([(a, b) for a, b in pairs])
    return (torch.tensor([x.ids for x in e]), torch.tensor([x.attention_mask for x in e]), torch.tensor([x.type_ids for x in e]))
def score(model, pairs, bs=64):
    model.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(pairs), bs):
            ii, am, tt = batch_of(pairs[i:i + bs]); out.append(model(input_ids=ii, attention_mask=am, token_type_ids=tt).logits.squeeze(-1))
    return torch.cat(out).numpy() if out else np.zeros(0)
def auc(s, lab):
    lab = np.asarray(lab, bool); pos, neg = s[lab], s[~lab]
    r = np.argsort(np.argsort(np.r_[pos, neg])) + 1
    return (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / max(1, len(pos) * len(neg))

# ---------- the examples ----------
A = json.load(open(IN_F, encoding="utf-8"))["answers"]; D = json.load(open(IDX_F, encoding="utf-8"))
R = bi.Ranker(D); n = R.n; idx = {a: i for i, a in enumerate(R.ids)}
var, more, near = bi.people_wordings()
text_of = [(a["wordings"][0] + " " + a["short"]).strip() for a in A]   # the answer as the site shows it: its question and its short answer
site = [set(a["wordings"]) for a in A]
people = [(i, w) for i, a in enumerate(A) for w in dict.fromkeys([w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()] + more.get(a["id"], [])) if w not in site[i]]
nm = [(q, idx[a]) for a, qs in sorted(near.items()) if a in idx for q in qs]
fold_of = lambda i: int(hashlib.sha1(R.ids[i].encode()).hexdigest(), 16) % K
def looks(questions):
    tx = [R.texts(q) for q in questions]; V = bi.embed_all([t[0] for t in tx] + [t[1] for t in tx], quiet=True)
    return [R.look(V[i], V[len(tx) + i], questions[i], tx[i][2]) for i in range(len(tx))]
log(f"pair: {len(people)} ways of asking, {len(nm)} near-miss questions, {n} answers")
LP = looks([w for _, w in people])
ex = []   # (question, answer index, label, kind, the answer whose fold it belongs to)
for (i, w), L in zip(people, LP):
    ex.append((w, i, 1.0, "wording", i))
    for j in [int(j) for j in np.argsort(-L["key"], kind="stable") if int(j) != i][:3]: ex.append((w, j, 0.0, "other answer", i))
for q, i in nm: ex.append((q, i, 0.0, "near-miss", i))
if LIMIT: random.shuffle(ex); ex = ex[:LIMIT]
train = [e for e in ex if FOLD is None or fold_of(e[4]) != FOLD]; held = [e for e in ex if FOLD is not None and fold_of(e[4]) == FOLD]
log(f"pair: {len(ex)} pairs ({sum(e[2] for e in ex):.0f} yes); training on {len(train)}, held out {len(held)} (fold {FOLD} of {K}, by answer)")

# ---------- the gold set ----------
G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
lab = {}
for Rd in readers:
    for x in Rd: lab.setdefault(x["n"], []).append(x)
tests = []
for g in G:
    ls = lab.get(g["n"], [])
    if len(ls) < len(readers): continue
    full = {a for x in ls for a in x.get("answers", []) if a in idx}; part = {a for x in ls for a in x.get("partly", []) if a in idx} - full
    tests.append((g["n"], g["question"], full, part, all(x.get("none") for x in ls)))
LG = looks([t[1] for t in tests])
TOP = 5
gold_rows = []
for (nq, q, full, part, un), L in zip(tests, LG):
    order = [int(j) for j in np.argsort(-L["key"], kind="stable")[:TOP]]
    best, related, p = R.tiers(L["plain"], L["topic"], L["groups"], lambda c: R.six(L, c))
    gold_rows.append({"n": nq, "q": q, "full": full, "part": part, "un": un, "order": order, "ok": [bool(L["ok"][j]) for j in order], "rule": bool(best), "p": p})

def report(model, label):
    sig = lambda x: 1.0 / (1.0 + np.exp(-x))
    if held:
        s = score(model, [(e[0], text_of[e[1]]) for e in held]); kind = np.array([e[3] for e in held]); y = np.array([e[2] for e in held])
        wn = (kind == "wording") | (kind == "near-miss")
        log(f"{label}: answers held out of training: a way of asking against a near-miss question, area under the curve {auc(s[wn], y[wn]):.3f} (the judge's six numbers: 0.877); against the other answers too {auc(s, y):.3f}")
        for t in (0.5, 0.7, 0.8, 0.9, 0.95):
            pr = sig(s) >= t; log(f"    at {t:.2f}: ways of asking kept {pr[kind == 'wording'].mean() * 100:.1f}%; near-miss questions let through {pr[kind == 'near-miss'].mean() * 100:.1f}%; other answers let through {pr[kind == 'other answer'].mean() * 100:.1f}%")
    S = score(model, [(r["q"], text_of[j]) for r in gold_rows for j in r["order"]]).reshape(len(gold_rows), TOP); P = sig(S)
    nfull = sum(bool(r["full"]) for r in gold_rows); nun = sum(r["un"] for r in gold_rows)
    def line(name, pick):
        b = f = p = un = 0
        for r, pr in zip(gold_rows, P):
            j = pick(r, pr)
            if j is None: continue
            a = R.ids[r["order"][j]]; b += 1; f += a in r["full"]; p += a in r["part"]; un += r["un"]
        log(f"    {name:<58} best match for {b:3d} of {len(gold_rows)}: full {f:3d}, partial {p:3d}, wrong {b - f - p:3d}; unanswerable given one {un} of {nun}; full answers found {f} of {nfull}")
    log(f"{label}: the gold set ({len(gold_rows)} forum questions; {nfull} with a full answer, {nun} unanswerable)")
    line("the page now (the judge alone)", lambda r, pr: 0 if r["rule"] else None)
    for t in (0.5, 0.7, 0.8, 0.9, 0.95):
        line(f"veto: the page's best match, if this look says {t:.2f} or more", lambda r, pr, t=t: 0 if r["rule"] and pr[0] >= t else None)
    for t in (0.5, 0.7, 0.8, 0.9, 0.95):
        line(f"second order: the best of the first {TOP} by this look, from {t:.2f}", lambda r, pr, t=t: (lambda j: j if r["ok"][j] and pr[j] >= t else None)(int(np.argmax(np.where(r["ok"], pr, -1.0)))))
    return S

model = load_model()
if (OUT / "pair.pt").exists() and "--eval-only" in sys.argv: model.load_state_dict(torch.load(OUT / "pair.pt")); report(model, "kept weights"); sys.exit(0)
report(model, "before any teaching (the open model as it is)")
optim = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
steps = EPOCHS * math.ceil(len(train) / BATCH); warm = int(0.1 * steps)
sched = torch.optim.lr_scheduler.LambdaLR(optim, lambda s: (s + 1) / warm if s < warm else max(0.0, (steps - s) / max(1, steps - warm)))
lossf = torch.nn.BCEWithLogitsLoss(); t0 = time.time(); step = 0
for ep in range(EPOCHS):
    model.train(); random.shuffle(train); tot = 0.0
    for b in range(0, len(train), BATCH):
        chunk = train[b:b + BATCH]; ii, am, tt = batch_of([(e[0], text_of[e[1]]) for e in chunk]); y = torch.tensor([e[2] for e in chunk])
        loss = lossf(model(input_ids=ii, attention_mask=am, token_type_ids=tt).logits.squeeze(-1), y)
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optim.step(); sched.step(); optim.zero_grad(); tot += float(loss); step += 1
        if step % 50 == 0: log(f"  epoch {ep + 1}, step {step} of {steps}: loss {tot / (b // BATCH + 1):.4f}; {time.time() - t0:.0f} s")
    torch.save(model.state_dict(), OUT / "pair.pt")
    S = report(model, f"after epoch {ep + 1}")
np.save(OUT / "gold-scores.npy", S)
json.dump({"model": "ms-marco-MiniLM-L-6-v2, taught with our own examples (scripts/insight/pair.py)", "epochs": EPOCHS, "lr": LR, "seed": SEED, "fold": FOLD, "pairs": len(train), "held": len(held), "maxlen": MAXLEN}, open(OUT / "pair.json", "w"), indent=1)
log("pair: done in", round(time.time() - t0), "s")
