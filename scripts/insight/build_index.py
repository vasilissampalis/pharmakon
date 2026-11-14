"""build_index.py IN.json OUT.json [--eval]: Pharmakon Insight's index (site 2.2.0, 14 November 2026; the senior author: the
site should feel like your own thinking). Called by site/build.js, which writes IN.json: every answer on the page with its
substance, section, pages, every wording of its question on the site and its short answer. Adds the ways people ask each
answer (data/verification/insight/variants_reader696.json, when present), embeds every wording and short answer with
all-MiniLM-L6-v2 (site/insight/vendor, byte-identical to the official files: scripts/insight/MODELS.md) exactly as the page
does in the browser (BERT uncased WordPiece, [CLS] text [SEP], at most 128 tokens, mean over the tokens, unit length), and
writes OUT.json: the vectors (int8; the page scales each row back to unit length), each answer's words for the word-overlap
score, each answer's next questions (the nearest answers by their questions' meaning, the same page first) and which answers
open without a guess (safety: the mixing and drug-checking pages, section 6 Acute risks, or "overdose" in the question).
The tokens are made here by the tokenizers library (BertWordPieceTokenizer, lowercase, as eval_match.py's MiniLM class);
the model is run by the page's own runtime under Node (scripts/insight/embed.js: ONNX Runtime Web from site/insight/vendor),
one text at a time, so the index's numbers are the very numbers the page computes for the same words (bit-identical; the
Python onnxruntime on a PC gives cosine 0.994 to 1 against the page, as its int8 kernels round differently: parity.js).
Vectors are cached by text in site/insight/.cache/ (not committed), so a build embeds only new or changed texts.
--eval: also scores the forum questions of the gold set (two blind readers, data/verification/insight/) the way the page
does (the int8 vectors it reads, the same word overlap and drug names, the same rule for what is shown), and prints the hit
rates and, for each threshold, how many answerable questions get a right answer shown and how many unanswerable ones get a
confident match. The page's threshold (THRESHOLD below) was chosen from that table."""
import ast, base64, glob, hashlib, json, math, os, pathlib, re, shutil, subprocess, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / "site/insight/vendor"
CACHE = ROOT / "site/insight/.cache/vectors-wasm.npz"   # made by the page's runtime, one text at a time (see embed_all)
VARIANTS = ROOT / "data/verification/insight/variants_reader696.json"
# the score the page computes (as tuned in scripts/insight/tune.py and scored in eval_gold.py): 0.7 x the best wording, 0.3 x
# the short answer, plus 0.2 x word overlap (TF-IDF over each answer's wordings on the site and its short answer); a best score
# under THRESHOLD shows "No checked answer fits this closely" instead of answers, and the second and third are shown only
# when they score ALSO or more.
# The editor's measure (scripts/insight/eval_gold.py, MiniLM tuned with the wordings, 14 November 2026): at 0.65 a match is
# shown for 68.6% of answerable questions, with a right answer in the three for 50.4% (73% of those shown), and for 22.2% of
# questions the site cannot answer; at 0.60, 85% and 47%; at 0.70, 41% and 7%. 0.65 kept (the best precision of those), and
# the words on the page say only what that supports: "Closest checked answers", "No checked answer fits this closely".
# This script's --eval (the page's own vectors and rule; answerable: a full answer named by either reader, 79 questions; 126
# that neither reader could answer; top-1 51.9%, top-3 81.0%): at 0.65, 89.9% of answerable questions get a match, 69.6% with
# a right answer, and 31.7% of unanswerable ones get one; at 0.60, 97.5%, 78.5% and 57.1%; at 0.70, 69.6%, 57.0% and 12.7%.
W_Q, W_SHORT, W_WORDS = 0.7, 0.3, 0.2
THRESHOLD, ALSO = 0.65, 0.60
N_NEXT = 6       # the page shows three, leaving out the answers already opened in a row
SAFETY_PAGES = {"interactions", "drug-checking"}


def encoder():
    """eval_match.py's MiniLM class (the Python onnxruntime), loaded without running that script's evaluation: parity.js
    compares it with the page as an independent check of the model; the index itself is made with the page's runtime."""
    src = (ROOT / "scripts/insight/eval_match.py").read_text(encoding="utf-8")
    keep = [n for n in ast.parse(src).body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name in ("MiniLM", "norm")]
    ns = {}
    exec("import numpy as np\nfrom tokenizers import BertWordPieceTokenizer\nimport onnxruntime as ort\n" + ast.unparse(ast.Module(body=keep, type_ignores=[])), ns)
    enc = ns["MiniLM"](VENDOR)
    enc.tok.enable_truncation(128)   # the page truncates at 128 tokens, [CLS] and [SEP] included
    return enc


def tokenizer():
    from tokenizers import BertWordPieceTokenizer
    tok = BertWordPieceTokenizer(str(VENDOR / "vocab.txt"), lowercase=True)
    tok.enable_truncation(128)   # the page truncates at 128 tokens, [CLS] and [SEP] included; no padding
    return tok


def embed_ids(ids):
    """Unit vectors for lists of token ids, made by the page's runtime under Node (scripts/insight/embed.js)."""
    d = CACHE.parent; d.mkdir(parents=True, exist_ok=True)
    inp, out = d / "embed-in.json", d / "embed-out.f32"
    inp.write_text(json.dumps({"ids": ids}), encoding="utf-8")
    node = os.environ.get("PK_NODE") or shutil.which("node") or "node"
    r = subprocess.run([node, str(ROOT / "scripts/insight/embed.js"), str(inp), str(out)], capture_output=True, text=True)
    if r.returncode != 0: sys.exit("insight: the page's runtime could not embed the texts: " + r.stderr.strip()[-600:])
    V = np.fromfile(out, dtype="<f4").reshape(len(ids), -1)
    inp.unlink(); out.unlink()
    return V


def embed_all(texts):
    """Unit vectors for texts, from the cache where a text was embedded before. Each text is run alone, as the page runs a
    question (the int8 model sets its scale from all the numbers in a batch: a text run in a padded batch comes out slightly
    different)."""
    key = lambda t: hashlib.sha1(t.encode("utf-8")).hexdigest()
    have = {}
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=False)
        have = dict(zip(z["keys"].tolist(), z["vecs"]))
    need = sorted({t for t in texts if key(t) not in have})
    if need:
        tok = tokenizer()
        for t, v in zip(need, embed_ids([tok.encode(t).ids for t in need])): have[key(t)] = v.astype(np.float32)
        ks = sorted(have); np.savez(CACHE, keys=np.array(ks), vecs=np.vstack([have[k] for k in ks]))
    print(f"insight: {len(texts)} texts embedded ({len(need)} new)", file=sys.stderr)
    return np.vstack([have[key(t)] for t in texts]) if texts else np.zeros((0, 384), np.float32)


def int8(M):
    """Each row as int8 (scaled to its largest value) in base64, and the unit rows the page gets back from it: the page
    reads the int8 values and scales each row to unit length, so no scale needs to be sent."""
    s = np.maximum(np.abs(M).max(1), 1e-12) / 127.0
    q = np.clip(np.round(M / s[:, None]), -127, 127).astype(np.int8)
    back = q.astype(np.float32); back /= np.maximum(np.linalg.norm(back, axis=1, keepdims=True), 1e-9)
    return base64.b64encode(q.tobytes()).decode("ascii"), back


# word overlap as eval_match.py's Lexical: words are runs of a-z and 0-9; a word's weight is log(1 + N / df) over the answers
words = lambda s: re.findall(r"[a-z0-9]+", s.lower())


class Words:
    def __init__(self, docs):
        self.N = len(docs); self.df = {}
        for d in docs:
            for w in set(words(d)): self.df[w] = self.df.get(w, 0) + 1
        self.D = [self.vec(d) for d in docs]
    def vec(self, t):
        v = {}
        for w in words(t):
            if w in self.df: v[w] = v.get(w, 0.0) + math.log(1 + self.N / self.df[w])
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / n for w, x in v.items()}
    def sims(self, t):
        q = self.vec(t)
        return np.array([sum(x * d.get(w, 0.0) for w, x in q.items()) for d in self.D], np.float32)


# drug names (as tune.py's expand): a street or brand name in a question brings the drug's own name along
def drug_names():
    AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8")); SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
    pats, canon = {}, {}
    for s in SUB:
        slug = s["slug"]; ns = {slug.replace("-", " ")}
        for part in re.split(r"[()/,;]| and ", s["name"]):
            p = part.strip().lower()
            if len(p) >= 3: ns.add(p)
        for a in AL.get(slug, []):
            if len(a) >= 3: ns.add(a.lower())
        pats[slug] = re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(ns, key=len, reverse=True)) + r")\b")
        canon[slug] = s["name"].split(" (")[0]
    def expand(t):
        tl = t.lower(); d = sorted(slug for slug, p in pats.items() if p.search(tl))
        extra = [canon[x] for x in d if canon[x].lower() not in tl]
        return t + (" (" + ", ".join(extra) + ")" if extra else "")
    return expand


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    IN, OUT = pathlib.Path(args[0]), pathlib.Path(args[1])
    A = json.load(open(IN, encoding="utf-8"))["answers"]
    var = json.load(open(VARIANTS, encoding="utf-8")).get("variants", {}) if VARIANTS.exists() else {}
    ids = [a["id"] for a in A]
    rows, W_txt = [], []
    for i, a in enumerate(A):
        ws = list(dict.fromkeys([w for w in a["wordings"] if w] + [w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()]))
        for w in ws: rows.append(i); W_txt.append(w)
    shorts = [a["short"] for a in A]
    docs = [" ".join(a["wordings"]) + " " + a["short"] for a in A]   # word overlap: the site's own wordings and the short answer
    V = embed_all(W_txt + shorts)
    Wv, Sv = V[:len(W_txt)], V[len(W_txt):]
    # next questions: the answers nearest by the meaning of their questions as the site words them, the same page first
    site_rows = [k for k, (r, w) in enumerate(zip(rows, W_txt)) if w in A[r]["wordings"]]
    Q = np.zeros((len(A), Wv.shape[1]), np.float32)
    for k in site_rows: Q[rows[k]] += Wv[k]
    Q /= np.maximum(np.linalg.norm(Q, axis=1, keepdims=True), 1e-9)
    sim = Q @ Q.T
    nxt = []
    for i, a in enumerate(A):
        order = [j for j in np.argsort(-sim[i]) if j != i]
        same = [j for j in order if set(A[j]["pages"]) & set(a["pages"])]
        nxt.append([ids[j] for j in (same + [j for j in order if j not in same])[:N_NEXT]])
    safety = [i for i, a in enumerate(A) if a["substance"] in SAFETY_PAGES or set(a["pages"]) & SAFETY_PAGES or a["section"] == 6
              or any(re.search(r"overdos", w, re.I) for w in a["wordings"])]
    wb, Wq = int8(Wv); sb, Sq = int8(Sv)
    out = {"_note": "Pharmakon Insight's index (scripts/insight/build_index.py): vectors of every answer's wordings and short answer (all-MiniLM-L6-v2, int8, each row scaled to unit length by the page), its words for the overlap score, its next questions, and the answers that open without a guess.",
           "model": "all-MiniLM-L6-v2-q8", "dim": int(Wv.shape[1]), "threshold": THRESHOLD, "also": ALSO, "weights": {"q": W_Q, "short": W_SHORT, "words": W_WORDS},
           "ids": ids, "rows": rows, "W": wb, "S": sb, "docs": docs, "next": nxt, "safety": safety, "variants": len(var)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"insight: {len(ids)} answers, {len(W_txt)} wordings ({sum(len(v) for v in var.values()) if var else 0} from the readers' variants), {OUT.stat().st_size // 1024} KB", file=sys.stderr)
    print(f"insight: {len(safety)} answers open without a guess (safety)", file=sys.stderr)
    if "--eval" in sys.argv: evaluate(A, ids, rows, Wq, Sq, docs)


def evaluate(A, ids, rows, Wv, Sv, docs):
    """The page's score on the gold set's forum questions (answerable: either reader names an answer that fully answers it;
    unanswerable: both readers say none does), with the vectors the page reads and its rule for what is shown."""
    G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
    readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
    lab = {}
    for R in readers:
        for x in R: lab.setdefault(x["n"], []).append(x)
    idset = set(ids); expand = drug_names(); lex = Words(docs)
    tests = []
    for g in G:
        ls = lab.get(g["n"], [])
        if len(ls) < len(readers): continue
        good = {a for x in ls for a in x.get("answers", []) if a in idset}
        none = all(x.get("none") for x in ls)
        if good or none: tests.append((g["question"], good))
    texts = [expand(t) for t, _ in tests]
    T = embed_all(texts)
    simw = T @ Wv.T
    best = np.full((len(tests), len(ids)), -1.0, np.float32)
    for col, r in enumerate(rows): best[:, r] = np.maximum(best[:, r], simw[:, col])
    L = np.vstack([lex.sims(t) for t, _ in tests])
    S = W_Q * best + W_SHORT * (T @ Sv.T) + W_WORDS * L
    ans_i = [i for i, (_, g) in enumerate(tests) if g]; un_i = [i for i, (_, g) in enumerate(tests) if not g]
    top = np.argsort(-S, 1)[:, :3]; tops = np.take_along_axis(S, top, 1)
    h1 = sum(ids[top[i, 0]] in tests[i][1] for i in ans_i) / max(1, len(ans_i)); h3 = sum(any(ids[j] in tests[i][1] for j in top[i]) for i in ans_i) / max(1, len(ans_i))
    print(f"gold questions: {len(ans_i)} answerable, {len(un_i)} not; top-1 {h1 * 100:.1f}%, top-3 {h3 * 100:.1f}%")
    for th in np.round(np.arange(0.50, 0.80, 0.025), 3):
        shown = lambda i: [j for k, j in enumerate(top[i]) if tops[i, 0] >= th and (k == 0 or tops[i, k] >= th - (THRESHOLD - ALSO))]
        keep = [i for i in ans_i if shown(i)]; right = sum(any(ids[j] in tests[i][1] for j in shown(i)) for i in ans_i)
        conf = sum(1 for i in un_i if shown(i))
        mark = "  <- the page" if abs(th - THRESHOLD) < 1e-9 else ""
        print(f"  threshold {th:.3f}: answerable shown {len(keep) / len(ans_i) * 100:5.1f}%, with a right answer {right / len(ans_i) * 100:5.1f}%; unanswerable given a match {conf / max(1, len(un_i)) * 100:5.1f}%{mark}")


if __name__ == "__main__":
    main()
