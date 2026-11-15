"""compare.py MODELS_DIR NAME=FILE.onnx NAME=FILE.onnx [...] [--mean A+B ...]: paired comparison of encoder files on the gold set.

The first NAME=FILE is the reference; every other one (and every --mean of two names: the two scores averaged) is compared
with it question by question: how many gold questions only the one or only the other gets right, the difference in
points, and a 95% interval from 4,000 resamples of the questions. A difference whose interval includes 0 is not shown
to be a difference. All files take the MiniLM vocabulary and mean pooling; scoring is 2.2.0's (0.7 best wording + 0.3
short answer + 0.2 word overlap), with the hurried wordings of the near-miss round in the index. NAME labels the cache."""
import sys, pathlib, importlib.util
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
pairs = [a.split("=", 1) for a in sys.argv[2:] if "=" in a and not a.startswith("--")]
means = [sys.argv[i + 1].split("+") for i, a in enumerate(sys.argv) if a == "--mean"]
sys.argv = sys.argv[:2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
vocab = jd.M / "_clay-design-system_embeddings/package/model/vocab.txt"
P, N = jd.build(True); E = [[] for _ in jd.A]; score = {}
for name, f in pairs:
    _, score[name] = jd.features(jd.Enc(name, f, vocab, "mean", vocab=True), jd.gq, P, E)
for a, b in means: score[f"{a}+{b}"] = (score[a] + score[b]) / 2
def hits(s, k, sets):
    s = np.where(jd.oldmask[None, :], s, -9.0); top = np.argsort(-s, 1)[:, :k]
    return {n: any(jd.ids[j] in sets[n] for j in top[i]) for i, n in enumerate(jd.ns) if sets[n]}
ref = pairs[0][0]; rng = np.random.default_rng(1)
for label, sets in (("strict", jd.strict), ("lenient", jd.lenient)):
    for k in (1, 3):
        a = hits(score[ref], k, sets); keys = list(a)
        print(f"{label} top-{k}: {ref} {100*np.mean([a[n] for n in keys]):.1f}% of {len(keys)}")
        for name in score:
            if name == ref: continue
            x = hits(score[name], k, sets); d = np.array([x[n] - a[n] for n in keys], float)
            bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(4000)]
            print(f"    {name:<22} {100*np.mean([x[n] for n in keys]):5.1f}% | only it +{int(sum(x[n] and not a[n] for n in keys))}, only {ref} -{int(sum(a[n] and not x[n] for n in keys))} | {100*d.mean():+5.1f} points (95% interval {100*np.percentile(bs,2.5):+.1f} to {100*np.percentile(bs,97.5):+.1f})")
