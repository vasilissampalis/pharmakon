#!/usr/bin/env python3
"""ship.py CANDIDATE.json MODEL.onnx --as NAME [--base minilm|gte-small] [--dry]: a model that candidate.py found better becomes Insight's model
(decision 41; 19 November 2026).

  - the model goes to site/insight/vendor/NAME-q8.onnx, with its NOTICE (what was changed and by whom; its base's licence: Apache-2.0 for
    all-MiniLM-L6-v2, whose text is already beside it; MIT for gte-small, whose text is written beside it);
  - site/insight/model.json names it and takes the judge candidate.py trained for it (CANDIDATE.model.json); the weights, the tiers, the judge's
    cut and the aspects stay as they are. A model of another base than the one on the site spreads its scores otherwise: the tiers are then swept
    for it first (sweep_related.py), and --tiers REL,NEAR gives the result; without it, a new base is refused;
  - the model it replaces leaves vendor/ (all-MiniLM-L6-v2-q8.onnx stays: the way back);
  - prints what changed. Building, every check, the version and publishing are the editor's (or the workflow's) next steps.
"""
import sys, json, re, shutil, pathlib, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / "site" / "insight" / "vendor"
MODEL_JSON = ROOT / "site" / "insight" / "model.json"
KEEP = {"all-MiniLM-L6-v2-q8.onnx"}
BASES = {
    "minilm": {"name": "sentence-transformers/all-MiniLM-L6-v2", "licence": "the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0; LICENSE-Apache-2.0.txt in this folder)",
               "who": "the Sentence-Transformers authors (Nils Reimers, Iryna Gurevych) and the authors of the underlying MiniLM model (Microsoft)", "section": " (Apache-2.0, section 4b)"},
    "gte-small": {"name": "thenlper/gte-small", "licence": "the MIT License (LICENSE-MIT-gte-small.txt in this folder)",
                  "who": "the authors of the GTE models (Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, Meishan Zhang; Alibaba DAMO Academy)", "section": ""},
}
MIT = """MIT License

Copyright (c) 2023 the authors of the GTE models (thenlper/gte-small: Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, Meishan Zhang)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


def arg(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def base_of(file_name):
    return "gte-small" if "gte" in file_name else "minilm"


def notice(name, base, how, sha):
    b = BASES[base]
    return (f"{name}-q8.onnx is Pharmakon's own encoder for Insight ({datetime.date.today().isoformat()}). It is a modified version of {b['name']}, "
            f"which is licensed under {b['licence']}. Copyright of the original: {b['who']}.\n\n"
            f"Changes made by Pharmakon{b['section']}: the original float weights were trained further on Pharmakon's own examples only (the ways people "
            f"ask each answer of the site, written by the site's readers, its editor and free language models from the site's own questions; and near-miss "
            f"questions an answer does not answer): {how}; and written as an int8 ONNX file with the same inputs and output as the original. It uses the "
            f"original vocabulary (vocab.txt, unmodified). Pharmakon's changes are released under the same licence.\n\nsha256({name}-q8.onnx) = {sha}\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (arg("--as"), arg("--base"), arg("--tiers"), arg("--how"))]
    if len(args) < 2 or not arg("--as"): print(__doc__); return
    cand = json.load(open(args[0], encoding="utf-8")); src = pathlib.Path(args[1]); name = arg("--as"); dry = "--dry" in sys.argv
    assert re.fullmatch(r"pharmakon-insight-\d+", name), "--as pharmakon-insight-N"
    if cand.get("verdict") != "better": raise SystemExit(f"ship: the candidate's verdict is '{cand.get('verdict')}': not shipped")
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    if sha != cand["candidate"]["sha256"]: raise SystemExit("ship: this file is not the one candidate.py measured")
    mj_new = json.load(open(pathlib.Path(args[0]).with_suffix(".model.json"), encoding="utf-8"))
    cfg = json.load(open(MODEL_JSON, encoding="utf-8")); old = cfg["file"]
    base = arg("--base", base_of(cand["candidate"]["file"])); assert base in BASES
    if base != base_of(old) and not arg("--tiers"): raise SystemExit(f"ship: {base} is another base than the site's ({old}): sweep the tiers for it first (sweep_related.py) and give --tiers REL,NEAR")
    fn = f"{name}-q8.onnx"
    cfg["file"] = fn; cfg["judge"] = dict(cfg["judge"], **{k: mj_new["judge"][k] for k in ("features", "mu", "sd", "w", "b")})
    if arg("--tiers"):
        rel, near = [float(x) for x in arg("--tiers").split(",")]; cfg["tiers"] = dict(cfg["tiers"], related=rel, near=near)
    how = arg("--how", "the result written as Pharmakon's file (scripts/insight/train.py)")
    print(f"ship: {old} -> {fn} ({base}; SHA-256 {sha[:16]}…); judge for it; tiers {cfg['tiers']}")
    if dry: return
    shutil.copyfile(src, VENDOR / fn)
    (VENDOR / f"NOTICE-{name}.txt").write_text(notice(name, base, how, sha), encoding="utf-8")
    if base == "gte-small" and not (VENDOR / "LICENSE-MIT-gte-small.txt").exists(): (VENDOR / "LICENSE-MIT-gte-small.txt").write_text(MIT, encoding="utf-8")
    json.dump(cfg, open(MODEL_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(MODEL_JSON, "a").write("\n")
    if old != fn and old not in KEEP:
        (VENDOR / old).unlink(missing_ok=True)
        for n in VENDOR.glob("NOTICE-" + old.replace("-q8.onnx", "") + ".txt"): n.unlink()
    print("ship: done; now build, sweep and check (scripts/insight/MODELS.md), set the version, and publish")


if __name__ == "__main__":
    main()
