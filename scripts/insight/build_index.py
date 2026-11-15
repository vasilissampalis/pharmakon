"""build_index.py IN.json OUT.json [NEXT.json] [--eval]: Pharmakon Insight's index (site 2.2.0, 14 November 2026; honest
tiers and next questions for site 2.3, 15 November 2026). Called by site/build.js, which writes IN.json: every answer on the
page with its substance, section, pages, the drugs it is about, every wording of its question on the site and its short
answer. Adds the ways people ask each answer (data/verification/insight/variants_reader696.json and the "more" wordings
of nearmiss_*.json, when present; the "near" questions of those files, which an answer does NOT answer, are never indexed
and never reach the page), embeds every wording and short answer with Insight's model (site/insight/model.json names the
file in site/insight/vendor; where the files came from: scripts/insight/MODELS.md) exactly as the page does in the browser
(BERT uncased WordPiece, [CLS] text [SEP], at most 128 tokens, mean over the tokens, unit length), and writes OUT.json: the
vectors (int8; the page scales each row back to unit length), each answer's words for the word-overlap score, the drugs
each answer is about, the names that name a drug in a question, the model's file name, and the weights and tiers of
site/insight/model.json (the page and the checks read them from OUT.json only). NEXT.json gets each answer's next questions
(the nearest answers by the meaning of their questions, never from another drug, never itself): site/build.js puts them in
the page, for "Read next" and "People also ask".

Two looks at every question (2.3; the senior author, 15 November: "it has a high error rate"). The first is 2.2.0's score:
the question, with the drug's own name brought along, against every wording and short answer. Its weakness, measured on
the gold set: the drug's name carries so much of the meaning that any question about kratom scores high against any answer
about kratom. So every wording is embedded a second time with the drug names taken out ("is it addictive"), and so is the
question: that is the topic score. Which drug is meant is then settled by the names themselves, not by the model: an answer
is a best match only when it is about every drug the question names (or the drug of the page the reader is on).

The weights and the tiers (site/insight/model.json; nothing here or in the page holds a threshold):
  weights  q, short, words: the first look, as tuned in tune.py and scored in eval_gold.py: 0.7 x the best wording, 0.3 x
           the short answer, plus 0.2 x word overlap (TF-IDF over each answer's wordings on the site and its short answer);
           topic: candidates are put in order by first look + topic x the topic score; same: an answer about the drugs the
           question names goes this far ahead (in effect: first; on the gold set that puts a fitting answer first under
           Related a little more often than no head start: 72 against 64 of 197 questions).
  tiers    best: a best match needs a first look of this or more ... topic: ... and a topic score of this or more, and to
           be about every drug the question names; sure: or a topic score of this or more with a first look of at least
           `related` (the same question in other words: what "is it addictive", asked on the cannabis page, needs); tie: a
           second best match only when it is this close to the first (first look + weights.topic x topic); related: a
           related answer needs a first look of this or more ... near: ... and a topic score of this or more.
Measured on the gold set with the page's own rule (--eval; 400 forum questions, 79 with a full answer by either reader,
126 that neither reader could answer): scripts/insight/MODELS.md has the table. With all-MiniLM-L6-v2, 2.2.0's score alone
at 0.72 gave a best match that was wrong for about one question in three; the topic score at 0.45 brings that under one in
five, and at 0.60 to one in ten, but then "how can i die from ketamine" (topic 0.49 against the UK deaths answer) is no
longer a best match, which the 2.3 brief asked for: the editor's to settle, with the tiers of each new model.

The tokens are made here by the tokenizers library (BertWordPieceTokenizer, lowercase); the model is run by the page's own
runtime under Node (scripts/insight/embed.js: ONNX Runtime Web from site/insight/vendor), one text at a time, so the
index's numbers are the very numbers the page computes for the same words (bit-identical; the Python onnxruntime on a PC
gives cosine 0.994 to 1 against the page, as its int8 kernels round differently: parity.js). Vectors are cached by text in
site/insight/.cache/, in a file named after the model file's SHA-256 (not committed): a build embeds only new or changed
texts, and a new model embeds everything again.
--eval: also ranks the forum questions of the gold set (two blind readers, data/verification/insight/) with the page's own
rule (class Ranker below, which scripts/insight/parity.js holds the page to), and prints how often a best match is a full
answer, a partial one or wrong, how the related answers do, the same for other thresholds, and how often an answer is
given as best match to a question the near-miss readers wrote as one it does not answer."""
import base64, glob, hashlib, json, math, os, pathlib, re, shutil, subprocess, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / "site/insight/vendor"
CONFIG = json.load(open(ROOT / "site/insight/model.json", encoding="utf-8"))   # the model's file name, the weights, the tiers
MODEL = CONFIG["file"]
MODEL_SHA256 = hashlib.sha256((VENDOR / MODEL).read_bytes()).hexdigest() if (VENDOR / MODEL).exists() else "missing"
CACHE = ROOT / "site/insight/.cache" / ("vectors-" + MODEL_SHA256[:16] + ".npz")   # made by the page's runtime, one text at a time (see embed_all)
VARIANTS = ROOT / "data/verification/insight/variants_reader696.json"
NEARMISS = ROOT / "data/verification/insight"   # nearmiss_*.json: per answer, "more" (wordings it answers) and "near" (questions it does not)
N_NEXT = 10      # next questions kept for each answer (three for each place it lives in, when that is more); the page shows three
# Names that name a drug in a question (for the tiers, the routes and the topic score): each drug's slug, the parts of its
# name and its street names of three letters or more (data/site/substances.json, aliases.json), without the WEAK ones:
# everyday words that are also street names. "pills" in "sleeping pills" must not make a question about ecstasy, nor
# "drink" in "drink water" one about alcohol, nor "analogues" one about fentanyl; they still bring the drug's name along
# for the first look (expand, as 2.2.0 tuned it).
WEAK = set("drink pills crystal ice speed tabs brown lean glue toad robo balloons spice oat microdosing vaping pouches solvents butane analogues".split())
# everyday names beyond aliases.json (the word search has its own list, SR_NAMES in site/src/app.simple.js)
EXTRA = {"benzo": ["benzodiazepines"], "benzodiazepine": ["benzodiazepines"], "xans": ["benzodiazepines"], "ativan": ["benzodiazepines"], "klonopin": ["benzodiazepines"],
         "sleeping pills": ["benzodiazepines"], "sleeping pill": ["benzodiazepines"], "sleeping tablets": ["benzodiazepines"],
         "magic mushrooms": ["psilocybin"], "laughing gas": ["nitrous-oxide"], "nos": ["nitrous-oxide"], "nangs": ["nitrous-oxide"], "whippets": ["nitrous-oxide"],
         "painkillers": ["prescription-opioids"], "oxy": ["prescription-opioids"], "percocet": ["prescription-opioids"], "vicodin": ["prescription-opioids"],
         "fent": ["fentanyl-and-analogues"], "nitazene": ["fentanyl-and-analogues"], "amphetamines": ["amphetamine"], "cathinones": ["synthetic-cathinones"], "2cb": ["2c-x"],
         "beer": ["alcohol"], "beers": ["alcohol"], "wine": ["alcohol"], "liquor": ["alcohol"], "cigarettes": ["nicotine"], "cigarette": ["nicotine"],
         "edible": ["cannabis"], "energy drink": ["caffeine"], "robotussin": ["dxm"]}
# a family's name names every drug of the family (substances.json, cls): an answer about any one of them is about it
FAMILY_WORDS = {"Opioids": ["opioids", "opioid", "opiates", "opiate"], "Stimulants": ["stimulants", "stimulant"], "Depressants": ["depressants", "downers"],
                "Classic psychedelics": ["psychedelics", "psychedelic", "hallucinogens"], "Atypical psychedelics": ["psychedelics", "psychedelic", "hallucinogens"],
                "Dissociatives": ["dissociatives", "dissociative"], "Cannabinoids": ["cannabinoids"], "Inhalants": ["inhalants"]}
SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8"))


class PyEncoder:
    """The same model run by the Python onnxruntime (texts in padded batches, mean over the real tokens, unit length):
    parity.js compares it with the page as an independent check of the model; the index itself is made with the page's
    runtime (embed_ids)."""
    def __init__(self):
        import onnxruntime as ort
        self.tok = tokenizer(); self.tok.enable_padding()
        self.s = ort.InferenceSession(str(VENDOR / MODEL), providers=["CPUExecutionProvider"])
        self.inputs = [i.name for i in self.s.get_inputs()]
    def __call__(self, texts):
        out = []
        for i in range(0, len(texts), 64):
            enc = self.tok.encode_batch(texts[i:i + 64])
            ii = np.array([e.ids for e in enc], dtype=np.int64); am = np.array([e.attention_mask for e in enc], dtype=np.int64)
            feed = {"input_ids": ii, "attention_mask": am}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.zeros_like(ii)
            h = self.s.run(None, feed)[0]; m = am[..., None].astype(np.float32)
            v = (h * m).sum(1) / np.maximum(m.sum(1), 1e-9)
            out.append(v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9))
        return np.vstack(out)


def encoder(): return PyEncoder()


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


def embed_all(texts, quiet=False):
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
    if not quiet: print(f"insight: {len(texts)} texts embedded ({len(need)} new)", file=sys.stderr)
    return np.vstack([have[key(t)] for t in texts]) if texts else np.zeros((0, 384), np.float32)


def int8(M):
    """Each row as int8 (scaled to its largest value) in base64, and the unit rows the page gets back from it: the page
    reads the int8 values and scales each row to unit length, so no scale needs to be sent."""
    s = np.maximum(np.abs(M).max(1), 1e-12) / 127.0
    q = np.clip(np.round(M / s[:, None]), -127, 127).astype(np.int8)
    back = q.astype(np.float32); back /= np.maximum(np.linalg.norm(back, axis=1, keepdims=True), 1e-9)
    return base64.b64encode(q.tobytes()).decode("ascii"), back


def unit_rows(b64, dim):
    """The rows as the page reads them: int8 from base64, each scaled to unit length."""
    q = np.frombuffer(base64.b64decode(b64), dtype=np.int8).astype(np.float32).reshape(-1, dim)
    return q / np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-9)


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


def drug_name_sets():
    """Each drug's names, as tune.py's: its slug, the parts of its name and its street names of three letters or more."""
    out = {}
    for s in SUB:
        ns = {s["slug"].replace("-", " ")}
        for part in re.split(r"[()/,;]| and ", s["name"]):
            p = part.strip().lower()
            if len(p) >= 3: ns.add(p)
        for a in AL.get(s["slug"], []):
            if len(a) >= 3: ns.add(a.lower())
        out[s["slug"]] = ns
    return out


# drug names for the first look (as tune.py's expand): a street or brand name in a question brings the drug's own name along
def drug_names():
    pats, canon = {}, {}
    for slug, ns in drug_name_sets().items():
        pats[slug] = re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(ns, key=len, reverse=True)) + r")\b")
    for s in SUB: canon[s["slug"]] = s["name"].split(" (")[0]
    def expand(t):
        tl = t.lower(); d = sorted(slug for slug, p in pats.items() if p.search(tl))
        extra = [canon[x] for x in d if canon[x].lower() not in tl]
        return t + (" (" + ", ".join(extra) + ")" if extra else "")
    return expand


def names_table():
    """[name, [drugs]] for every name that names a drug in a question, the longest first (so "crystal meth" is read before
    "meth"): the drugs' own names without the WEAK ones, the EXTRA everyday names, and the families' names."""
    t = {}
    for slug, ns in drug_name_sets().items():
        for n in ns:
            if n not in WEAK: t.setdefault(n, set()).add(slug)
    for n, slugs in EXTRA.items(): t.setdefault(n, set()).update(slugs)
    for fam, ws in FAMILY_WORDS.items():
        members = {s["slug"] for s in SUB if s["cls"] == fam}
        for w in ws: t.setdefault(w, set()).update(members)
    return [[n, sorted(t[n])] for n in sorted(t, key=lambda n: (-len(n), n))]


def name_pattern(names):
    """One pattern for all the names, in the order given; the page builds the same one (insPrepare in app.insight.js)."""
    return re.compile(r"(?<!\w)(" + "|".join(re.escape(n) for n in names) + r")(?!\w)", re.I)


class Ranker:
    """The page's ranking (insRank in site/src/app.insight.js) in Python, from the index the page reads: for --eval, and
    for scripts/insight/parity.js, which requires the page to give the same tiers and scores."""
    def __init__(self, D):
        dim = D["dim"]; self.ids = D["ids"]; self.n = len(self.ids); self.rows = np.array(D["rows"])
        self.W, self.M, self.S = unit_rows(D["W"], dim), unit_rows(D["M"], dim), unit_rows(D["S"], dim)
        self.lex = Words(D["docs"]); self.wt = D["weights"]; self.t = D["tiers"]
        self.about = [set(D["slugs"][k] for k in xs) for xs in D["about"]]
        self.name_of = {n: [D["slugs"][k] for k in xs] for n, xs in D["names"]}
        self.pat = name_pattern([n for n, _ in D["names"]])
        self.expand = drug_names(); self.canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
    def named(self, q):
        """The drugs a question names, each as the list of drugs its name stands for (a family's name: every drug of it)."""
        out = []
        for m in self.pat.finditer(q):
            g = self.name_of[m.group(1).lower()]
            if g not in out: out.append(g)
        return out
    def mask(self, q): return self.pat.sub("it", q)
    def texts(self, q, drug=None):
        """What is embedded for a question: with the drug's own name brought along, and with the drug names taken out; and
        the drugs it is about (on a drug's page, a question that names none is about that drug)."""
        groups = self.named(q); full = self.expand(q)
        if not groups and drug: groups = [[drug]]; full += " (" + self.canon[drug] + ")"
        return full, self.mask(q), groups
    def score(self, v, mv, q):
        """The two looks for every answer: first look (plain) and topic."""
        sw, sm = self.W @ v, self.M @ mv
        bw = np.full(self.n, -1.0, np.float32); bm = np.full(self.n, -1.0, np.float32)
        np.maximum.at(bw, self.rows, sw); np.maximum.at(bm, self.rows, sm)
        return self.wt["q"] * bw + self.wt["short"] * (self.S @ v) + self.wt["words"] * self.lex.sims(q), bm
    def tiers(self, plain, topic, groups):
        t = self.t; ok = np.array([all(any(s in self.about[i] for s in g) for g in groups) for i in range(self.n)])
        order_by = plain + self.wt["topic"] * topic
        key = order_by + self.wt["same"] * ok
        cand = [int(i) for i in np.argsort(-key, kind="stable") if plain[i] >= t["related"]]
        fits = [i for i in cand if ok[i] and ((plain[i] >= t["best"] and topic[i] >= t["topic"]) or topic[i] >= t["sure"])]
        best = fits[:1] + [i for i in fits[1:2] if order_by[i] >= order_by[fits[0]] - t["tie"]]
        related = [i for i in cand if i not in best and topic[i] >= t["near"]][:3]
        return best, related, ok
    def rank_vectors(self, q, v, mv, groups):
        plain, topic = self.score(v, mv, q); best, related, ok = self.tiers(plain, topic, groups)
        row = lambda i: {"id": self.ids[i], "plain": round(float(plain[i]), 4), "topic": round(float(topic[i]), 4), "off": not bool(ok[i])}
        return {"best": [row(i) for i in best], "related": [row(i) for i in related], "plain": plain, "topic": topic, "ok": ok}
    def rank(self, q, drug=None):
        full, masked, groups = self.texts(q, drug)
        v, mv = embed_all([full, masked], quiet=True)
        return self.rank_vectors(q, v, mv, groups)


def next_lists(A, sim):
    """Each answer's next questions: the answers nearest by the meaning of their questions, never itself, and only answers
    that live where it lives: about one of its drugs, or on its page (mixing, drug checking, facts about drug use). An
    answer that lives in several places takes the nearest of each in turn, so that every page it is on has some to offer.
    Nothing from another drug is ever offered (the senior author, 15 November: a cannabis answer offered a cocaine
    question); an answer alone on its drug has no next questions."""
    drugs = {s["slug"] for s in SUB}
    at = [set(a.get("about") or []) | set(a["pages"]) for a in A]         # where an answer lives: its drugs and its pages
    out = []
    for i, a in enumerate(A):
        order = [int(j) for j in np.argsort(-sim[i], kind="stable") if j != i]
        homes = sorted(at[i], key=lambda h: (h != a["substance"], h not in drugs, h))
        lists = [[j for j in order if h in at[j]] for h in homes]
        want = max(N_NEXT, 3 * len(homes)); nx = []; k = 0
        while len(nx) < want and any(k < len(l) for l in lists):
            for l in lists:
                if k < len(l) and l[k] not in nx and len(nx) < want: nx.append(l[k])
            k += 1
        out.append(nx)
    return out


def people_wordings():
    """The ways people ask each answer: the six wordings of phrasings writer 696 (variants) and the three hurried wordings
    of the near-miss readers ("more" in nearmiss_*.json, when those files are there; they are still growing, so a file that
    cannot be read is left out, with a line saying so). The same readers' "near" questions are questions an answer does
    NOT answer: they come back apart, for --eval alone; they are never indexed and never reach the page."""
    var = dict(json.load(open(VARIANTS, encoding="utf-8")).get("variants", {})) if VARIANTS.exists() else {}
    more, near = {}, {}
    for f in sorted(NEARMISS.glob("nearmiss_*.json")):
        try: items = json.load(open(f, encoding="utf-8")).get("items", {})
        except ValueError:
            print(f"insight: {f.name} could not be read (still being written?): left out of this build", file=sys.stderr); continue
        for k, v in items.items():
            more.setdefault(k, []).extend(w for w in (v.get("more") or []) if isinstance(w, str) and w.strip())
            near.setdefault(k, []).extend(w for w in (v.get("near") or []) if isinstance(w, str) and w.strip())
    return var, more, near


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    IN, OUT = pathlib.Path(args[0]), pathlib.Path(args[1])
    A = json.load(open(IN, encoding="utf-8"))["answers"]
    var, more, near = people_wordings()
    ids = [a["id"] for a in A]
    drugs = [s["slug"] for s in SUB]
    for a in A: a["about"] = sorted(set(a.get("about") or [p for p in a["pages"] if p in drugs]))
    rows, W_txt = [], []
    for i, a in enumerate(A):
        ws = list(dict.fromkeys([w for w in a["wordings"] if w] + [w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()] + more.get(a["id"], [])))
        for w in ws: rows.append(i); W_txt.append(w)
    shorts = [a["short"] for a in A]
    docs = [" ".join(a["wordings"]) + " " + a["short"] for a in A]   # word overlap: the site's own wordings and the short answer
    names = names_table(); pat = name_pattern([n for n, _ in names])
    M_txt = [pat.sub("it", w) for w in W_txt]                          # every wording again, with the drug names taken out
    V = embed_all(W_txt + shorts + M_txt)
    Wv, Sv, Mv = V[:len(W_txt)], V[len(W_txt):len(W_txt) + len(shorts)], V[len(W_txt) + len(shorts):]
    # next questions: the answers nearest by the meaning of their questions as the site words them
    site_rows = [k for k, (r, w) in enumerate(zip(rows, W_txt)) if w in A[r]["wordings"]]
    Q = np.zeros((len(A), Wv.shape[1]), np.float32)
    for k in site_rows: Q[rows[k]] += Wv[k]
    Q /= np.maximum(np.linalg.norm(Q, axis=1, keepdims=True), 1e-9)
    nxt = next_lists(A, Q @ Q.T)
    wb, _ = int8(Wv); sb, _ = int8(Sv); mb, _ = int8(Mv)
    slugs = sorted({s for a in A for s in a["about"]} | {s for _, xs in names for s in xs})
    at = {s: k for k, s in enumerate(slugs)}
    out = {"_note": "Pharmakon Insight's index (scripts/insight/build_index.py): vectors of every answer's wordings (W), of the same wordings with the drug names taken out (M) and of its short answer (S) (made with the model named here, int8, each row scaled to unit length by the page); its words for the overlap score; the drugs it is about; the names that name a drug in a question; and the weights and the tiers (from site/insight/model.json).",
           "model": MODEL, "model_sha256": MODEL_SHA256, "dim": int(Wv.shape[1]), "weights": CONFIG["weights"], "tiers": CONFIG["tiers"],
           "ids": ids, "rows": rows, "W": wb, "M": mb, "S": sb, "docs": docs, "slugs": slugs, "about": [[at[s] for s in a["about"]] for a in A],
           "names": [[n, [at[s] for s in xs]] for n, xs in names], "variants": len(var), "more": sum(1 for a in A if more.get(a["id"]))}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    if len(args) > 2:
        pathlib.Path(args[2]).write_text(json.dumps({"ids": ids, "next": nxt}, separators=(",", ":")), encoding="utf-8")
    changed = sum(1 for w, m in zip(W_txt, M_txt) if w != m)
    idset = set(ids); bare = [a["id"] for a in A if not var.get(a["id"]) and not more.get(a["id"])]
    print(f"insight: model {MODEL} (SHA-256 {MODEL_SHA256[:12]}…); {len(ids)} answers, {len(W_txt)} wordings ({sum(len(v) for k, v in var.items() if k in idset)} from the phrasings writer, "
          f"{sum(len(v) for k, v in more.items() if k in idset)} hurried ones from the near-miss readers; {changed} name a drug), {len(names)} names, {OUT.stat().st_size // 1024} KB", file=sys.stderr)
    if bare: print(f"insight: {len(bare)} answers have only the site's own questions to be found by (no wordings written for them yet): {', '.join(bare[:30])}{' …' if len(bare) > 30 else ''}", file=sys.stderr)
    print(f"insight: next questions for {sum(1 for x in nxt if x)} answers ({sum(len(x) for x in nxt)} in all)", file=sys.stderr)
    if "--eval" in sys.argv: evaluate(out, near)


def evaluate(D, near=None):
    """The page's tiers on the gold set's forum questions (full answer: either reader names an answer that fully answers
    it; partial: a reader names it as answering part; unanswerable: both readers say none does), then on the near-miss
    readers' questions (each written as a question one answer does NOT answer: is that answer given as best match?)."""
    G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
    readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
    lab = {}
    for R in readers:
        for x in R: lab.setdefault(x["n"], []).append(x)
    R = Ranker(D); idset = set(R.ids); tests = []
    for g in G:
        ls = lab.get(g["n"], [])
        if len(ls) < len(readers): continue
        full = {a for x in ls for a in x.get("answers", []) if a in idset}
        part = {a for x in ls for a in x.get("partly", []) if a in idset} - full
        tests.append((g["question"], full, part, all(x.get("none") for x in ls)))
    tx = [R.texts(q) for q, _, _, _ in tests]
    V = embed_all([t[0] for t in tx] + [t[1] for t in tx])
    scored = [R.score(V[i], V[len(tests) + i], tests[i][0]) for i in range(len(tests))]
    n_full = sum(bool(f) for _, f, _, _ in tests); n_un = sum(u for _, _, _, u in tests)
    order = [np.argsort(-(p + R.wt["topic"] * t), kind="stable") for p, t in scored]
    h1 = sum(R.ids[o[0]] in tests[i][1] for i, o in enumerate(order) if tests[i][1]) / n_full
    h3 = sum(any(R.ids[j] in tests[i][1] for j in o[:3]) for i, o in enumerate(order) if tests[i][1]) / n_full
    print(f"model {D['model']}; gold questions: {len(tests)}; {n_full} with a full answer, {n_un} unanswerable; candidates in the page's order: a full answer first {h1 * 100:.1f}%, in the first three {h3 * 100:.1f}%")
    keep = dict(R.t)
    # the near-miss questions: (question, the answer it must not get), for answers on the page
    nm = [(q, a) for a, qs in sorted((near or {}).items()) if a in idset for q in qs]
    if nm:
        ntx = [R.texts(q) for q, _ in nm]
        NV = embed_all([t[0] for t in ntx] + [t[1] for t in ntx])
        nscored = [R.score(NV[i], NV[len(nm) + i], nm[i][0]) for i in range(len(nm))]
    def table(label):
        b = {"n": 0, "full": 0, "part": 0, "un": 0}; s = {"n": 0, "good": 0}; rel = {"rows": 0, "good": 0, "q": 0, "un": 0}; miss = 0
        for i, (q, full, part, un) in enumerate(tests):
            best, related, _ = R.tiers(scored[i][0], scored[i][1], tx[i][2])
            if best:
                a = R.ids[best[0]]; b["n"] += 1; b["full"] += a in full; b["part"] += a in part; b["un"] += un
                if len(best) > 1: s["n"] += 1; s["good"] += R.ids[best[1]] in full or R.ids[best[1]] in part
            elif full and any(R.ids[j] in full for j in related): miss += 1
            if related:
                rel["q"] += 1; rel["rows"] += len(related); rel["un"] += un
                rel["good"] += sum(R.ids[j] in full or R.ids[j] in part for j in related)
        wrong = b["n"] - b["full"] - b["part"]
        line = (f"  {label}: best match for {b['n']} questions: a full answer {b['full']} ({b['full'] / max(1, b['n']) * 100:.0f}%), a partial one {b['part']} ({b['part'] / max(1, b['n']) * 100:.0f}%), "
                f"wrong {wrong} ({wrong / max(1, b['n']) * 100:.0f}%); unanswerable questions given one {b['un']} of {n_un}; a second best {s['n']} ({s['good']} full or partial); "
                f"related: {rel['rows']} rows for {rel['q']} questions, {rel['good'] / max(1, rel['rows']) * 100:.0f}% full or partial, {rel['un']} of {n_un} unanswerable questions get some; "
                f"no best match but a full answer under Related {miss}")
        if nm:
            hit = 0
            for i, (q, a) in enumerate(nm):
                best, _, _ = R.tiers(nscored[i][0], nscored[i][1], ntx[i][2])
                hit += any(R.ids[j] == a for j in best)
            line += f"; near-miss questions given the answer they do not get as best match {hit} of {len(nm)} ({hit / len(nm) * 100:.1f}%)"
        print(line)
    table("the page's tiers " + json.dumps(keep))
    r2 = lambda x: round(x, 2)
    for topic in (0.0, r2(keep["topic"] - 0.05), r2(keep["topic"] + 0.05), r2(keep["topic"] + 0.10), r2(keep["topic"] + 0.15), r2(keep["topic"] + 0.20)):
        R.t = dict(keep, topic=topic, sure=2.0 if topic == 0.0 else keep["sure"]); table(f"topic {topic:.2f}" + (" (the first look alone, with the drug rule)" if topic == 0.0 else ""))
    for best in (r2(keep["best"] - 0.04), r2(keep["best"] - 0.02), r2(keep["best"] + 0.02), r2(keep["best"] + 0.04)):
        R.t = dict(keep, best=best); table(f"best {best:.2f}")
    for nearv in (0.0, r2(keep["near"] - 0.05), r2(keep["near"] + 0.05)):
        R.t = dict(keep, near=nearv); table(f"near {nearv:.2f}")
    R.t = keep


if __name__ == "__main__":
    main()
