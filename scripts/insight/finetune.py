"""finetune.py MODELS_DIR --out DIR [--epochs N] [--lr X] [--seed S] [--mine K] [--masked SHARE [--index-script FILE]] [--all]
[--save-each]: Pharmakon Insight 2.3, our own encoder (15 November 2026).

Takes the open encoder all-MiniLM-L6-v2 (Apache-2.0; float weights, byte-identical to the official ONNX file) and teaches
it this site's questions with this site's own examples:
  - a way of asking is pulled towards the other ways of asking the same answer and away from every other answer's;
  - a near-miss question (sounds close, is not answered by that answer; readers 707 and 708) is pushed away from the
    ways of asking that answer.
Nothing else is used: no forum question, no gold label. The examples of 15% of the answers are held out to choose the
epoch.
--masked SHARE: Insight looks at a question twice (scripts/insight/build_index.py): as asked, with the drug's name brought
along, and with the drug names taken out ("is it addictive"), which tells what is asked apart from which drug it is asked
about. With SHARE > 0 that share of the batches is trained the second way: every text with the drug names replaced by
"it" exactly as the page does it, an answer's own near-miss questions (same drug, another question) as its negatives,
and no other answer counted as wrong when it asks the same thing about another drug (answers whose masked wordings are
nearer than 0.8 for the untrained model are left out of each other's comparison). Then the model is written as ONNX and as int8 ONNX with the same inputs and output as the file the site loads
today, so the page code does not change. Evaluate the int8 file on the gold set with judge.py / eval below."""
import sys, json, pathlib, importlib.util, hashlib, math, time, random
import numpy as np, torch, onnx
from onnx import numpy_helper
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
arg = jd.arg; M_DIR = jd.M; A = jd.A
OUT = pathlib.Path(arg("--out")); OUT.mkdir(parents=True, exist_ok=True)
EPOCHS = int(arg("--epochs", "6")); LR = float(arg("--lr", "2e-5")); SEED = int(arg("--seed", "7")); BATCH = 32; MAXLEN = 48; SCALE = 20.0
MASKED = float(arg("--masked", "0"))   # share of batches trained on texts with the drug names taken out, as Insight's second look reads them
MINE = int(arg("--mine", "0"))      # per anchor, this many wordings of the wrong answers that rank highest for it, found afresh each epoch
ALL = "--all" in sys.argv          # train on every answer for exactly --epochs epochs (after the held-out run has chosen the number)
torch.manual_seed(SEED); random.seed(SEED); np.random.seed(SEED); torch.set_num_threads(2)
FP32 = M_DIR / "_maycombhq_embed-model/package/model.onnx"
from transformers import BertConfig, BertModel
from tokenizers import BertWordPieceTokenizer
tok = BertWordPieceTokenizer(str(M_DIR / "_clay-design-system_embeddings/package/model/vocab.txt"), lowercase=True); tok.enable_truncation(MAXLEN); tok.enable_padding()

def load_model():
    m = onnx.load(str(FP32)); init = {i.name: numpy_helper.to_array(i) for i in m.graph.initializer}
    cfg = BertConfig(vocab_size=30522, hidden_size=384, num_hidden_layers=6, num_attention_heads=12, intermediate_size=1536, max_position_embeddings=512,
                     type_vocab_size=2, hidden_act="gelu", layer_norm_eps=1e-12, hidden_dropout_prob=0.1, attention_probs_dropout_prob=0.1)
    model = BertModel(cfg, add_pooling_layer=False)
    sd = {k: torch.tensor(v.copy()) for k, v in init.items() if not k.startswith("onnx::") and k != "embeddings.position_ids"}
    for n in m.graph.node:
        if n.op_type == "MatMul" and n.input[1] in init:
            mod = n.output[0].split("/MatMul")[0].strip("/").replace("/", ".")
            sd[mod + ".weight"] = torch.tensor(init[n.input[1]].T.copy())
    missing, unexpected = model.load_state_dict(sd, strict=False)
    assert not unexpected and all("position_ids" in k or "token_type_ids" in k for k in missing), (missing, unexpected)
    return model
def encode(model, texts, grad=False, bs=64):
    outs = []
    for i in range(0, len(texts), bs):
        e = tok.encode_batch(texts[i:i + bs])
        ii = torch.tensor([x.ids for x in e]); am = torch.tensor([x.attention_mask for x in e])
        with torch.set_grad_enabled(grad):
            h = model(input_ids=ii, attention_mask=am, token_type_ids=torch.zeros_like(ii)).last_hidden_state
            m = am.unsqueeze(-1).float(); v = (h * m).sum(1) / m.sum(1).clamp(min=1e-9)
            outs.append(torch.nn.functional.normalize(v, dim=-1))
    return torch.cat(outs)

model = load_model()
# the PyTorch copy must give the same numbers as the ONNX file it was read from
import onnxruntime as ort
s = ort.InferenceSession(str(FP32), providers=["CPUExecutionProvider"]); probe = ["does molly mess up your memory", "How many deaths does alcohol cause worldwide?", "xanax"]
e = tok.encode_batch(probe); ii = np.array([x.ids for x in e], np.int64); am = np.array([x.attention_mask for x in e], np.int64)
h = s.run(None, {"input_ids": ii, "attention_mask": am, "token_type_ids": np.zeros_like(ii)})[0]; mm = am[..., None].astype(np.float32); ref = jd.norm((h * mm).sum(1) / mm.sum(1))
model.eval(); got = encode(model, probe).numpy(); print("PyTorch copy against the ONNX file, cosine:", np.round((ref * got).sum(1), 6))
assert ((ref * got).sum(1) > 0.9999).all()

# ---------- examples ----------
P, N = jd.build(True)
val = np.array([int(hashlib.sha1(a["id"].encode()).hexdigest(), 16) % 100 < 15 for a in A])
X = lambda t: jd.expand(t)
ex = []   # (answer row, wording that is not a site question)
for ai, a in enumerate(A):
    for w in P[ai]:
        if w not in a["questions"]: ex.append((ai, w))
tr_ex = [x for x in ex if ALL or not val[x[0]]]
print(f"{len(ex)} wordings as anchors ({len(tr_ex)} for training); near-miss questions for {sum(1 for n in N if n)} answers ({sum(len(n) for n in N)}); held-out answers {int(val.sum())}")
Dtxt = [w for ws in P for w in ws]; Down = np.array([i for i, ws in enumerate(P) for _ in ws]); pos_of = {(int(Down[j]), w): j for j, w in enumerate(Dtxt)}
def validate(model):
    model.eval(); D = encode(model, [X(t) for t in Dtxt]).numpy()
    q = [(ai, w, 1) for ai, w in ex if val[ai]] + [(ai, w, 0) for ai in range(len(A)) if val[ai] for w in N[ai]]
    Q = encode(model, [X(w) for _, w, _ in q]).numpy(); S = Q @ D.T
    hit, own_pos, own_neg = [], [], []
    for r, (ai, w, y) in enumerate(q):
        row = S[r].copy()
        if y: row[pos_of[(ai, w)]] = -9
        own = row[Down == ai].max()
        if y: hit.append(Down[row.argmax()] == ai); own_pos.append(own)
        else: own_neg.append(own)
    auc = jd.auc_of(np.r_[own_pos, own_neg], np.r_[np.ones(len(own_pos), bool), np.zeros(len(own_neg), bool)]) if own_neg else float("nan")
    return float(np.mean(hit)), auc
# the second look: drug names taken out, with the page's own pattern
bi_file = pathlib.Path(arg("--index-script", str(ROOT / "scripts/insight/build_index.py")))
mask = None
try:
    spec2 = importlib.util.spec_from_file_location("bi", bi_file); bi = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(bi)
    _pat = bi.name_pattern([n for n, _ in bi.names_table()]); mask = lambda t: _pat.sub("it", t)
except Exception as e_:
    assert not MASKED, f"--masked needs the index script with name_pattern and names_table ({bi_file}): {e_}"
def validate_masked(model):
    """Held-out answers, drug names taken out: is a wording nearer to the other wordings of its answer than that answer's
    near-miss questions are? (area under the curve)"""
    if mask is None: return float("nan")
    model.eval(); pos, neg = [], []
    for ai in range(len(A)):
        if not val[ai] or len(P[ai]) < 2: continue
        W = encode(model, [mask(w) for w in P[ai]]).numpy(); S = W @ W.T; np.fill_diagonal(S, -9)
        pos += [float(S[k].max()) for k, w in enumerate(P[ai]) if w not in A[ai]["questions"]]
        if N[ai]: neg += [float(x) for x in (encode(model, [mask(w) for w in N[ai]]).numpy() @ W.T).max(1)]
    return jd.auc_of(np.r_[pos, neg], np.r_[np.ones(len(pos), bool), np.zeros(len(neg), bool)]) if pos and neg else float("nan")
acc0, auc0 = validate(model); aucm0 = validate_masked(model)
print(f"before: held-out wordings find their answer {100*acc0:.1f}%, wording vs near-miss AUC {auc0:.3f}; with the drug names taken out {aucm0:.3f}")
SAME = None
if MASKED:   # answers that ask the same thing about another drug, as the untrained model sees their masked wordings
    Wm = encode(model, [mask(t) for t in Dtxt]).numpy(); SAME = np.zeros((len(A), len(A)), bool)
    for ai in range(len(A)):
        rows = np.flatnonzero(Down == ai)
        if not len(rows): continue
        s = (Wm[rows] @ Wm.T).max(0); best = np.full(len(A), -1.0); np.maximum.at(best, Down, s); SAME[ai] = best >= 0.8
    np.fill_diagonal(SAME, False); SAME |= SAME.T
    print(f"masked batches: share {MASKED}; pairs of answers that ask the same thing about another drug (left out of each other's comparison): {int(SAME.sum() // 2)}")

# ---------- training ----------
opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
steps = EPOCHS * math.ceil(len(tr_ex) / BATCH); sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / max(1, int(0.1 * steps)), max(0.0, (steps - s) / max(1, steps - int(0.1 * steps)))))
fin = lambda x: x if x == x else 0.0
best = (acc0 + fin(auc0) + (fin(aucm0) if MASKED else 0), 0); t0 = time.time(); step = 0
torch.save(model.state_dict(), OUT / "best.pt")
for ep in range(1, EPOCHS + 1):
    hard = {}
    if MINE:   # the wordings of other answers that the model, as it is now, puts nearest to each anchor
        model.eval(); Dv = encode(model, [X(t) for t in Dtxt]).numpy(); Av = encode(model, [X(w) for _, w in tr_ex]).numpy()
        S_ = Av @ Dv.T
        for r, (ai, w) in enumerate(tr_ex):
            S_[r, Down == ai] = -9; hard[(ai, w)] = [Dtxt[j] for j in np.argsort(-S_[r])[:max(MINE * 3, 6)]]
    model.train(); random.shuffle(tr_ex); tot = 0.0; nb = 0
    # batches with one anchor per answer, so that no other row's positive is secretly right
    pool = list(tr_ex)
    while pool:
        batch, seen, rest = [], set(), []
        for x in pool:
            if x[0] not in seen and len(batch) < BATCH: batch.append(x); seen.add(x[0])
            else: rest.append(x)
        pool = rest
        if len(batch) < 4: break
        masked = MASKED > 0 and random.random() < MASKED
        T_ = mask if masked else X
        anchors = [T_(w) for _, w in batch]
        positives = [T_(random.choice([p for p in P[ai] if p != w] or [w])) for ai, w in batch]
        negs = [T_(random.choice(N[ai])) if N[ai] else None for ai, _ in batch]
        neg_txt = [n for n in negs if n is not None]
        if masked:
            # each row is compared with its own positive, its own near-miss question, and the positives of the answers
            # in the batch that do not ask the same thing about another drug
            rows_ai = np.array([ai for ai, _ in batch]); neg_row = [r for r, n in enumerate(negs) if n is not None]
            allow = np.zeros((len(batch), len(batch) + len(neg_txt)), bool)
            allow[:, :len(batch)] = ~SAME[np.ix_(rows_ai, rows_ai)]; allow[np.arange(len(batch)), np.arange(len(batch))] = True
            for c, r in enumerate(neg_row): allow[r, len(batch) + c] = True
            ea = encode(model, anchors, grad=True); ep_ = encode(model, positives, grad=True)
            cand = torch.cat([ep_, encode(model, neg_txt, grad=True)]) if neg_txt else ep_
            am_ = torch.tensor(allow); target = torch.arange(len(batch))
            logits = (ea @ cand.T * SCALE).masked_fill(~am_, -1e4)
            back = ((ep_ @ ea.T) * SCALE).masked_fill(~am_[:, :len(batch)].T, -1e4)
            loss = torch.nn.functional.cross_entropy(logits, target) + 0.5 * torch.nn.functional.cross_entropy(back, target)
            opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); step += 1
            tot += float(loss.detach()); nb += 1
            continue
        if MINE:
            own = {ai for ai, _ in batch}
            for ai, w in batch:
                picks = [h for h in hard.get((ai, w), []) if pos_of.get((ai, h)) is None]   # never a wording of the anchor's own answer
                neg_txt += [X(h) for h in random.sample(picks, min(MINE, len(picks)))]
        ea = encode(model, anchors, grad=True); ep_ = encode(model, positives, grad=True)
        cand = torch.cat([ep_, encode(model, neg_txt, grad=True)]) if neg_txt else ep_
        logits = ea @ cand.T * SCALE; target = torch.arange(len(batch))
        loss = torch.nn.functional.cross_entropy(logits, target) + 0.5 * torch.nn.functional.cross_entropy((ep_ @ ea.T) * SCALE, target)
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); step += 1
        tot += float(loss.detach()); nb += 1
    acc, auc = validate(model); aucm = validate_masked(model); score = acc + fin(auc) + (fin(aucm) if MASKED else 0)
    print(f"epoch {ep}: loss {tot/max(1,nb):.3f} | held out{' (now trained on)' if ALL else ''}: finds answer {100*acc:.1f}%, AUC {auc:.3f}, names out {aucm:.3f} | {time.time()-t0:.0f}s", flush=True)
    if ALL or score > best[0]: best = (score, ep); torch.save(model.state_dict(), OUT / "best.pt")
    if "--save-each" in sys.argv: torch.save(model.state_dict(), OUT / f"ep{ep}.pt")
print("kept epoch", best[1])
model.load_state_dict(torch.load(OUT / "best.pt")); model.eval()

# ---------- write ONNX (same inputs and output as the file the site loads) and its int8 version ----------
class Wrap(torch.nn.Module):
    def __init__(self, m): super().__init__(); self.m = m
    def forward(self, input_ids, attention_mask, token_type_ids): return self.m(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids).last_hidden_state
e = tok.encode_batch(["a short example", "another, slightly longer example question"]); ii = torch.tensor([x.ids for x in e]); am = torch.tensor([x.attention_mask for x in e])
fp = OUT / "insight-fp32.onnx"
torch.onnx.export(Wrap(model), (ii, am, torch.zeros_like(ii)), str(fp), input_names=["input_ids", "attention_mask", "token_type_ids"], output_names=["last_hidden_state"],
                  dynamic_axes={k: {0: "batch", 1: "sequence"} for k in ("input_ids", "attention_mask", "token_type_ids", "last_hidden_state")}, opset_version=14, do_constant_folding=True, dynamo=False)
from onnxruntime.quantization import quantize_dynamic, QuantType
q8 = OUT / "insight-q8.onnx"; quantize_dynamic(str(fp), str(q8), weight_type=QuantType.QUInt8)
for f in (fp, q8): print(f.name, f.stat().st_size, "bytes, SHA-256", hashlib.sha256(f.read_bytes()).hexdigest())
json.dump({"base": "all-MiniLM-L6-v2 (fp32 ONNX, npm @maycombhq/embed-model 2.0.0-beta.1)", "epochs_kept": best[1], "epochs": EPOCHS, "lr": LR, "seed": SEED, "batch": BATCH,
           "mine": MINE, "masked": MASKED, "all_answers": ALL, "anchors": len(tr_ex), "near_miss_answers": sum(1 for n in N if n), "before": {"acc": acc0, "auc": auc0}}, open(OUT / "train.json", "w"), indent=1)
