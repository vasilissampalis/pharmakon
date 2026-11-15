"""eval_model.py MODELS_DIR MODEL.onnx NAME: the gold-set measures of judge.py for one encoder file (MiniLM tokenizer, mean
pooling), with the 2.2.0 scoring, with and without the near-miss examples in view. NAME labels the cache."""
import sys, pathlib, importlib.util
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
model, name = sys.argv[2], sys.argv[3]; sys.argv = sys.argv[:2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
enc = jd.Enc(name, model, jd.M / "_clay-design-system_embeddings/package/model/vocab.txt", "mean", vocab=True)
P, N = jd.build(True); E = [[] for _ in jd.A]
F, b = jd.features(enc, jd.gq, P, E); jd.gold_report(f"{name}: 2.2.0 scoring", b)
if jd.near:
    F2, b2 = jd.features(enc, jd.gq, P, N)
    jd.gold_report(f"{name}: judged by best wording minus near-miss excess", b2, verdict=F2[..., 0] - np.maximum(F2[..., 5] - F2[..., 0] + 0.02, 0))
    jd.gold_report(f"{name}: ordered and judged with the near-miss penalty", b2 - 0.5 * np.maximum(F2[..., 5] - F2[..., 0] + 0.02, 0))
