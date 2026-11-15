"""eval_model.py MODELS_DIR MODEL.onnx NAME [--quiet]: the gold-set measures of judge.py for one encoder file (MiniLM tokenizer,
mean pooling), with the 2.2.0 scoring. Reported for the odd-numbered gold questions (dev: used to choose between
settings), the even-numbered ones (test: the number to quote), and all. NAME labels the cache."""
import sys, pathlib, importlib.util
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
model, name = sys.argv[2], sys.argv[3]; quiet = "--quiet" in sys.argv; sys.argv = sys.argv[:2]
spec = importlib.util.spec_from_file_location("jd", ROOT / "scripts/insight/judge.py"); jd = importlib.util.module_from_spec(spec); spec.loader.exec_module(jd)
enc = jd.Enc(name, model, jd.M / "_clay-design-system_embeddings/package/model/vocab.txt", "mean", vocab=True)
P, N = jd.build(True); E = [[] for _ in jd.A]
F, b = jd.features(enc, jd.gq, P, E)
for sp in ("dev", "test", "all"): jd.gold_report(f"{name}", b, split=sp, quiet=quiet or sp != "all")
