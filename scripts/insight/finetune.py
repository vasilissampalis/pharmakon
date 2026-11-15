"""finetune.py MODELS_DIR --out DIR [--epochs N] [--lr X] [--seed S]: Pharmakon Insight 2.3, our own encoder (15 November 2026).

Takes the open encoder all-MiniLM-L6-v2 (Apache-2.0; float weights, byte-identical to the official ONNX file) and teaches
it this site's questions with this site's own examples:
  - a way of asking is pulled towards the other ways of asking the same answer and away from every other answer's;
  - a near-miss question (sounds close, is not answered by that answer; readers 707 and 708) is pushed away from the
    ways of asking that answer.
Nothing else is used: no forum question, no gold label. The examples of 15% of the answers are held out to choose the
epoch. Then the model is written as ONNX and as int8 ONNX with the same inputs and output as the file the site loads
today, so the page code does not change. Evaluate the int8 file on the gold set with judge.py / eval below."""
import sys, json, pathlib, importlib.util, hashlib, math, time, random
import numpy as np, torch, onnx
from onnx import numpy_helper
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
arg = jd.arg; M_DIR = jd.M; A = jd.A
OUT = pathlib.Path(arg("--out")); OUT.mkdir(parents=True, exist_ok=True)
EPOCHS = int(arg("--epochs", "6")); LR = float(arg("--lr", "2e-5")); SEED = int(arg("--seed", "7")); BATCH = 32; MAXLEN = 48; SCALE = 20.0
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
tr_ex = [x for x in ex if not val[x[0]]]
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
acc0, auc0 = validate(model); print(f"before: held-out wordings find their answer {100*acc0:.1f}%, wording vs near-miss AUC {auc0:.3f}")

# ---------- training ----------
opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
steps = EPOCHS * math.ceil(len(tr_ex) / BATCH); sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / max(1, int(0.1 * steps)), max(0.0, (steps - s) / max(1, steps - int(0.1 * steps)))))
best = (acc0 + (auc0 if auc0 == auc0 else 0), 0); t0 = time.time(); step = 0
torch.save(model.state_dict(), OUT / "best.pt")
for ep in range(1, EPOCHS + 1):
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
        anchors = [X(w) for _, w in batch]
        positives = [X(random.choice([p for p in P[ai] if p != w] or [w])) for ai, w in batch]
        negs = [X(random.choice(N[ai])) if N[ai] else None for ai, _ in batch]
        neg_txt = [n for n in negs if n is not None]
        ea = encode(model, anchors, grad=True); ep_ = encode(model, positives, grad=True)
        cand = torch.cat([ep_, encode(model, neg_txt, grad=True)]) if neg_txt else ep_
        logits = ea @ cand.T * SCALE; target = torch.arange(len(batch))
        loss = torch.nn.functional.cross_entropy(logits, target) + 0.5 * torch.nn.functional.cross_entropy((ep_ @ ea.T) * SCALE, target)
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); step += 1
        tot += float(loss); nb += 1
    acc, auc = validate(model); score = acc + (auc if auc == auc else 0)
    print(f"epoch {ep}: loss {tot/max(1,nb):.3f} | held out: finds answer {100*acc:.1f}%, AUC {auc:.3f} | {time.time()-t0:.0f}s")
    if score > best[0]: best = (score, ep); torch.save(model.state_dict(), OUT / "best.pt")
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
           "anchors": len(tr_ex), "near_miss_answers": sum(1 for n in N if n), "before": {"acc": acc0, "auc": auc0}}, open(OUT / "train.json", "w"), indent=1)
