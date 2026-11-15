"""adapt.py MODELS_DIR [--enc minilm|bge] [--steps N] [--save FILE]: Pharmakon Insight 2.3, a small model of our own on top
of the open encoder (15 November 2026).

The encoder turns a question into 384 numbers. It was trained on a billion general sentence pairs; it does not know that
on this site "does ketamine help depression" and "what side effects does ketamine treatment have" are different
questions. We teach it with our own examples, without touching the encoder: one 384 x 384 matrix M applied to the
question's numbers (q' = normalize(q M)), trained so that
  - a way of asking lands nearest the other ways of asking the same answer (all the site's wordings are the candidates);
  - a near-miss question (sounds close, is not answered by that answer) lands under a threshold for that answer, and a
    true wording above it, so that one cut-off can mean "this answers what was asked".
M starts as the identity and is held near it. Trained on the examples of 85% of the answers; the other 15% choose when
to stop. The gold set (400 real forum questions) is only looked at to report. Plain numpy, a minute on two cores."""
import sys, json, pathlib, importlib.util, hashlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
arg = jd.arg; M_DIR = jd.M; A = jd.A; norm = jd.norm
which = arg("--enc", "minilm"); STEPS = int(arg("--steps", "300"))
if which == "minilm": enc = jd.Enc("minilm", M_DIR / "_clay-design-system_embeddings/package/model/all-MiniLM-L6-v2-q8.onnx", M_DIR / "_clay-design-system_embeddings/package/model/vocab.txt", "mean", vocab=True)
else:
    bd = M_DIR / "_impro-plugin-semantic-mute-model/package"; enc = jd.Enc("bge-n", bd / "bge-small-en-v1.5-q8.onnx", bd / "bge-small-en-v1.5-tokenizer.json", "cls")
P, N = jd.build(True)
assert jd.near, "near-miss files needed"
# documents: every wording of every answer; queries: the wordings that are not the site's own questions, and the near-misses
Dtxt = [w for ws in P for w in ws]; Down = np.array([i for i, ws in enumerate(P) for _ in ws])
val = np.array([int(hashlib.sha1(a["id"].encode()).hexdigest(), 16) % 100 < 15 for a in A])
q_txt, q_ans, q_y, q_self = [], [], [], []
pos_of = {(int(Down[j]), w): j for j, w in enumerate(Dtxt)}
for ai, a in enumerate(A):
    for w in P[ai]:
        if w not in a["questions"]: q_txt.append(w); q_ans.append(ai); q_y.append(1); q_self.append(pos_of[(ai, w)])
    for w in N[ai]: q_txt.append(w); q_ans.append(ai); q_y.append(0); q_self.append(-1)
q_ans, q_y, q_self = np.array(q_ans), np.array(q_y), np.array(q_self)
Q = enc([jd.expand(t) for t in q_txt]); D = enc(Dtxt); n_q, n_d = len(q_txt), len(Dtxt)
is_val = val[q_ans]; tr = ~is_val
same = (q_ans[:, None] == Down[None, :])                       # documents of the query's own answer
selfmask = np.zeros((n_q, n_d), bool); selfmask[np.arange(n_q)[q_self >= 0], q_self[q_self >= 0]] = True
print(f"encoder {which}: {n_q} example questions ({int(q_y.sum())} wordings, {int((1 - q_y).sum())} near-misses; {int(is_val.sum())} held out), {n_d} wordings as candidates")
TAU, T, THETA, MARG, LAM, MU, LR = 0.05, 0.05, 0.62, 0.06, 1.0, 0.02, 2e-3
def forward(M):
    U = Q @ M; nu = np.linalg.norm(U, axis=1, keepdims=True); S = (U / nu) @ D.T
    return U, nu, S
def measures(S, rows):
    Sx = np.where(selfmask, -9, S); best_own = np.where(same & ~selfmask, S, -9).max(1)
    top = Down[np.argmax(Sx, 1)]
    pos = rows & (q_y == 1); neg = rows & (q_y == 0)
    acc = float((top[pos] == q_ans[pos]).mean()); auc = jd.auc_of(np.r_[best_own[pos], best_own[neg]], np.r_[np.ones(pos.sum(), bool), np.zeros(neg.sum(), bool)])
    return acc, auc
def step_grad(M):
    U, nu, S = forward(M)
    E = np.zeros_like(S)
    # (1) which answer: softmax over all candidates but itself, any wording of the same answer is right
    rows = np.flatnonzero(tr & (q_y == 1))
    Z = np.where(selfmask[rows], -1e9, S[rows] / TAU); Z -= Z.max(1, keepdims=True); Pm = np.exp(Z); Pm /= Pm.sum(1, keepdims=True)
    posm = same[rows] & ~selfmask[rows]; pp = (Pm * posm).sum(1, keepdims=True) + 1e-12
    E[rows] += (Pm - Pm * posm / pp) / TAU / len(rows)
    loss = float(-np.log(pp).mean())
    # (2) above or under the line: the best wording of the query's own answer
    own = np.where(same & ~selfmask, S, -9); j = own.argmax(1); m = own[np.arange(n_q), j]
    rows2 = np.flatnonzero(tr & (m > -8))
    y = q_y[rows2]; x = np.where(y == 1, -(m[rows2] - THETA - MARG), (m[rows2] - THETA)) / T
    sig = 1 / (1 + np.exp(-x)); g = np.where(y == 1, -sig, sig) / T * LAM / len(rows2)
    E[rows2, j[rows2]] += g; loss += float(LAM * np.logaddexp(0, x).mean())
    GU = (E @ D) / nu - ((E * S).sum(1, keepdims=True)) * U / (nu ** 2)
    G = Q.T @ GU + 2 * MU * (M - np.eye(M.shape[0], dtype=M.dtype))
    return loss, G, S
M = np.eye(Q.shape[1], dtype=np.float64); m1 = np.zeros_like(M); m2 = np.zeros_like(M); best = (None, -1, None)
_, _, S0 = forward(M); print("before: held-out wordings find their answer %.1f%%, wording vs near-miss AUC %.3f | train %.1f%% / %.3f" % (100 * measures(S0, is_val)[0], measures(S0, is_val)[1], 100 * measures(S0, tr)[0], measures(S0, tr)[1]))
for it in range(1, STEPS + 1):
    loss, G, S = step_grad(M)
    m1 = 0.9 * m1 + 0.1 * G; m2 = 0.999 * m2 + 0.001 * G * G
    M -= LR * (m1 / (1 - 0.9 ** it)) / (np.sqrt(m2 / (1 - 0.999 ** it)) + 1e-8)
    if it % 25 == 0 or it == STEPS:
        _, _, S = forward(M); va, vu = measures(S, is_val); ta, tu = measures(S, tr); score = va + vu
        print(f"step {it:4d} loss {loss:.3f} | held out: finds answer {100*va:.1f}%, AUC {vu:.3f} | train {100*ta:.1f}% / {tu:.3f} | |M-I| {np.linalg.norm(M - np.eye(len(M))):.2f}")
        if score > best[1]: best = (M.copy(), score, it)
M = best[0]; print("kept the matrix of step", best[2])
# ---------- the gold set, once ----------
class Adapted:
    def __init__(self, enc, M): self.enc, self.M = enc, M
    def __call__(self, texts, query=False):
        X = self.enc(texts, query=query)
        return norm(X @ self.M).astype(np.float32) if query else X
E_ = [[] for _ in A]
F0, b0 = jd.features(enc, jd.gq, P, E_); jd.gold_report(f"{which}: before (with hurried wordings)", b0)
F1, b1 = jd.features(Adapted(enc, M), jd.gq, P, E_); jd.gold_report(f"{which}: with our matrix", b1)
F2, b2 = jd.features(Adapted(enc, M), jd.gq, P, N); jd.gold_report(f"{which}: with our matrix, judged by best wording minus near-miss excess", b2, verdict=F2[..., 0] - np.maximum(F2[..., 5] - F2[..., 0] + 0.02, 0))
jd.gold_report(f"{which}: with our matrix, judged by the best wording alone", b2, verdict=F2[..., 0])
out = arg("--save")
if out:
    np.save(out, M.astype(np.float32)); print("saved", out)
