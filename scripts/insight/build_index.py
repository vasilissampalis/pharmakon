"""build_index.py IN.json OUT.json [NEXT.json] [--eval]: Pharmakon Insight's index (site 2.2.0, 14 November 2026; honest
tiers and next questions for site 2.3, 15 November 2026). Called by site/build.js, which writes IN.json: every answer on the
page with its substance, section, pages, the drugs it is about, every wording of its question on the site and its short
answer. Adds the ways people ask each answer (data/verification/insight/variants_reader696.json and the "more" wordings
of nearmiss_*.json, when present; the "near" questions of those files, which an answer does NOT answer, are never indexed
and never reach the page), embeds every wording and short answer with Insight's model (site/insight/model.json names the
file in site/insight/vendor; where the files came from: scripts/insight/MODELS.md) exactly as the page does in the browser
(BERT uncased WordPiece, [CLS] text [SEP], at most 128 tokens, mean over the tokens, unit length), and writes OUT.json: the
vectors (int8; the page scales each row back to unit length), each answer's words for the word-overlap score, the drugs
each answer is about, the names that name a drug in a question, the model's file name, and the weights, the tiers and
the judge of site/insight/model.json (the page and the checks read them from OUT.json only). NEXT.json gets each answer's next questions
(the nearest answers by the meaning of their questions, never from another drug, never itself): site/build.js puts them in
the page, for "Read next" and "People also ask".

Two looks at every question (2.3; the senior author, 15 November: "it has a high error rate"). The first is 2.2.0's score:
the question, with the drug's own name brought along, against every wording and short answer. Its weakness, measured on
the gold set: the drug's name carries so much of the meaning that any question about kratom scores high against any answer
about kratom. So every wording is embedded a second time with the drug names taken out ("is it addictive"), and so is the
question: that is the topic score. Which drug is meant is then settled by the names themselves, not by the model: an answer
is a best match only when it is about every drug the question names (or the drug of the page the reader is on).

The weights, the tiers and the judge (site/insight/model.json; nothing here or in the page holds a number of its own):
  weights  q, short, words: the first look, as tuned in tune.py and scored in eval_gold.py: 0.7 x the best wording, 0.3 x
           the short answer, plus 0.2 x word overlap (TF-IDF over each answer's wordings on the site and its short answer);
           topic: answers are put in order by first look + topic x the topic score; same: an answer about the drugs the
           question names goes this far ahead (in effect: first).
  judge    what makes a best match (the editor, 15 November; scripts/insight/judge2.py trains and measures it). Two
           thresholds on the two looks gave a best match that was wrong for 20 of 77 gold questions. The judge is a small
           logistic regression on six numbers the page has at hand for its first candidate (features, in order: its best
           wording, its second-best wording, its short answer, word overlap, topic, its lead over the next answer about
           the drugs named), each standardized (mu, sd), weighed (w) and summed with b; trained on our own wordings and
           near-miss questions only, never on a gold question. The first candidate is the best match when it is about
           every drug the question names and the judge's number is `best` or more; there is never a second best match.
  tiers    related: a related answer needs a first look of this or more ... near: ... and a topic score of this or more,
           and to be about at least one of the drugs named (or the drug of the page the reader is on).
Measured on the gold set with the page's own rule (--eval; 400 forum questions, 79 with a full answer by either reader,
126 that neither reader could answer): scripts/insight/MODELS.md has the table.

The tokens are made here by the tokenizers library (BertWordPieceTokenizer, lowercase); the model is run by the page's own
runtime under Node (scripts/insight/embed.js: ONNX Runtime Web from site/insight/vendor), one text at a time, so the
index's numbers are the very numbers the page computes for the same words (bit-identical; the Python onnxruntime on a PC
gives cosine 0.994 to 1 against the page, as its int8 kernels round differently: parity.js). Vectors are cached by text in
site/insight/.cache/, in a file named after the model file's SHA-256 (not committed): a build embeds only new or changed
texts, and a new model embeds everything again.
--eval: also ranks the forum questions of the gold set (two blind readers, data/verification/insight/) with the page's own
rule (class Ranker below, which scripts/insight/parity.js holds the page to), and prints how often a best match is a full
answer, a partial one or wrong, how the related answers do, the same for other cuts of the judge's number, and how often
an answer is given as best match to a question the near-miss readers wrote as one it does not answer."""
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
N_NEXT = 10      # next questions kept for each answer about its own drugs (three for each drug, when that is more); the page shows three
N_PAGE = 5       # ... and at least this many on each page the answer is told on (three are shown; the others stand in for answers already opened)
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
    for scripts/insight/parity.js, which requires the page to give the same best match, the same related answers and the
    same judge's number."""
    def __init__(self, D):
        dim = D["dim"]; self.ids = D["ids"]; self.n = len(self.ids); self.rows = np.array(D["rows"])
        self.W, self.M, self.S = unit_rows(D["W"], dim), unit_rows(D["M"], dim), unit_rows(D["S"], dim)
        self.lex = Words(D["docs"]); self.wt = D["weights"]; self.t = D["tiers"]; self.J = D["judge"]
        self.about = [set(D["slugs"][k] for k in xs) for xs in D["about"]]
        self.name_of = {n: [D["slugs"][k] for k in xs] for n, xs in D["names"]}
        self.pat = name_pattern([n for n, _ in D["names"]])
        self.expand = drug_names(); self.canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
        # 2.5: the list of questions not answered yet, as a ranker of its own over the same names, weights and judge
        Wd = D.get("wanted"); self.wanted = None; self.want_cut = (Wd or {}).get("cut", 1.0)
        if Wd: self.wanted = Ranker({"dim": dim, "ids": Wd["ids"], "rows": Wd["rows"], "W": Wd["W"], "M": Wd["M"], "S": Wd["S"], "docs": Wd["docs"], "weights": D["weights"], "tiers": D["tiers"], "judge": D["judge"],
                                     "slugs": D["slugs"], "about": Wd["about"], "names": D["names"]})
    def named(self, q):
        """The drugs a question names, each as the list of drugs its name stands for (a family's name: every drug of it)."""
        out = []
        for m in self.pat.finditer(q):
            g = self.name_of.get(m.group(1).lower())
            if g and g not in out: out.append(g)
        return out
    def mask(self, q): return self.pat.sub("it", q)
    def texts(self, q, drug=None):
        """What is embedded for a question: with the drug's own name brought along, and with the drug names taken out; and
        the drugs it is about (on a drug's page, a question that names none is about that drug)."""
        groups = self.named(q); full = self.expand(q)
        if not groups and drug: groups = [[drug]]; full += " (" + self.canon[drug] + ")"
        return full, self.mask(q), groups
    def look(self, v, mv, q, groups):
        """Everything the page computes for a question, for every answer: bw and bw2, the best and the second-best wording
        of the answer in the first look (-1 where it has no second wording); sh, its short answer; lx, word overlap; plain,
        the first look (the three weighed); topic, its best wording with the drug names taken out; ok, it is about every
        drug the question names; some, about at least one of them; by, plain + weights.topic x topic; key, the page's
        order: by, the answers about the drugs named weights.same ahead. (The reference for these numbers is look() in
        scripts/insight/judge2.py, which trains the judge on them.)"""
        sw, sm = self.W @ v, self.M @ mv
        bw = np.full(self.n, -1.0, np.float32); bw2 = np.full(self.n, -1.0, np.float32); bm = np.full(self.n, -1.0, np.float32)
        np.maximum.at(bw, self.rows, sw); np.maximum.at(bm, self.rows, sm)
        order = np.argsort(-sw, kind="stable")
        rest = sw.copy(); rest[order[np.unique(self.rows[order], return_index=True)[1]]] = -1.0   # without each answer's best wording
        np.maximum.at(bw2, self.rows, rest)
        sh = self.S @ v; lx = self.lex.sims(q)
        plain = self.wt["q"] * bw + self.wt["short"] * sh + self.wt["words"] * lx
        has = lambda i, g: any(s in self.about[i] for s in g)
        ok = np.array([all(has(i, g) for g in groups) for i in range(self.n)])
        some = np.array([not groups or any(has(i, g) for g in groups) for i in range(self.n)])
        by = plain + self.wt["topic"] * bm
        return {"bw": bw, "bw2": bw2, "sh": sh, "lx": lx, "plain": plain, "topic": bm, "ok": ok, "some": some, "by": by, "key": by + self.wt["same"] * ok, "groups": groups}
    def six(self, L, c):
        """The judge's six numbers for answer c (judge.features, in that order): its best wording, its second-best wording
        (0 if it has one wording), its short answer, word overlap, topic, and its lead over the next answer: by[c] less the
        highest by among the other answers about every drug the question names (less 0 if there is no other)."""
        el = L["ok"].copy(); el[c] = False
        lead = float(L["by"][c] - (L["by"][el].max() if el.any() else 0.0))
        return [float(L["bw"][c]), float(max(L["bw2"][c], 0.0)), float(L["sh"][c]), float(L["lx"][c]), float(L["topic"][c]), lead]
    def judge(self, f):
        """The judge's number for six numbers f: how sure it is that the first candidate answers what was asked."""
        J = self.J; z = sum(w * (x - m) / d for w, x, m, d in zip(J["w"], f, J["mu"], J["sd"])) + J["b"]
        return 1.0 / (1.0 + math.exp(-z))
    def tiers(self, plain, topic, groups, feats):
        """The page's rule. c, the first candidate in the page's order, is the best match if it is about every drug the
        question names and the judge's number for it (feats(c): its six numbers) is judge.best or more; there is never a
        second best match. Related: the next answers in that order, up to three, with a first look of tiers.related or
        more and a topic of tiers.near or more, about at least one of the drugs named (c first among them when it is not
        the best match). Returns the best match (a list of none or one), the related answers and the judge's number."""
        t = self.t; has = lambda i, g: any(s in self.about[i] for s in g)
        ok = np.array([all(has(i, g) for g in groups) for i in range(self.n)])
        some = np.array([not groups or any(has(i, g) for g in groups) for i in range(self.n)])
        order = np.argsort(-(plain + self.wt["topic"] * topic + self.wt["same"] * ok), kind="stable")
        c = int(order[0]); p = self.judge(feats(c))
        best = [c] if ok[c] and p >= self.J["best"] else []
        related = [int(i) for i in order if int(i) not in best and plain[i] >= t["related"] and topic[i] >= t["near"] and some[i]][:3]
        return best, related, p
    def rank_vectors(self, q, v, mv, groups):
        L = self.look(v, mv, q, groups); best, related, p = self.tiers(L["plain"], L["topic"], groups, lambda c: self.six(L, c))
        c = int(np.argsort(-L["key"], kind="stable")[0])
        row = lambda i: {"id": self.ids[i], "plain": round(float(L["plain"][i]), 4), "topic": round(float(L["topic"][i]), 4), "off": not bool(L["ok"][i])}
        return {"best": [row(i) for i in best], "related": [row(i) for i in related], "first": {"id": self.ids[c], "p": p, "f": self.six(L, c)},
                "plain": L["plain"], "topic": L["topic"], "ok": L["ok"], "look": L}
    def rank(self, q, drug=None):
        full, masked, groups = self.texts(q, drug)
        v, mv = embed_all([full, masked], quiet=True)
        return self.rank_vectors(q, v, mv, groups)
    def want(self, q, v, mv, groups):
        """The page's second look (insWant): the listed question a typed question is, or None. The list is ranked as the
        answers are, by its own small index; the first candidate is taken when it is about every drug the question names
        and the judge's number for it is the list's cut or more."""
        if self.wanted is None: return None
        r = self.wanted.rank_vectors(q, v, mv, groups); c = r["first"]
        on = bool(r["ok"][self.wanted.ids.index(c["id"])])
        return {"id": c["id"], "p": c["p"]} if on and c["p"] >= self.want_cut else None


def next_lists(A, sim):
    """Each answer's next questions: the answers nearest by the meaning of their questions, never itself. The same drug
    first: the nearest answers about each of its drugs, in turn. After them come the nearest on each page the answer is
    told on (a drug's page, mixing, drug checking, facts about drug use), so that every such page has some to offer under
    "Read next". Nothing else is ever offered: no answer about another drug that shares no page with it (the senior
    author, 15 November: a cannabis answer offered a cocaine question). An answer alone on its drug and its page has no
    next questions."""
    about = [set(a.get("about") or []) for a in A]
    pages = [set(a["pages"]) for a in A]
    out = []
    for i, a in enumerate(A):
        order = [int(j) for j in np.argsort(-sim[i], kind="stable") if j != i]
        first = lambda h: (h != a["substance"], h)
        nx = []
        # 1. the same drug first
        mine = sorted(about[i], key=first)
        lists = [[j for j in order if h in about[j]] for h in mine]
        want = max(N_NEXT, 3 * len(mine)); k = 0
        while len(nx) < want and any(k < len(l) for l in lists):
            for l in lists:
                if k < len(l) and l[k] not in nx and len(nx) < want: nx.append(l[k])
            k += 1
        # 2. then its pages, until each has enough to offer (an answer about no drug has only these)
        homes = sorted(pages[i], key=first)
        need = N_PAGE if nx else N_NEXT
        lists = [[j for j in order if p in pages[j]] for p in homes]
        got = [sum(1 for j in nx if p in pages[j]) for p in homes]; k = 0
        while any(got[x] < need and k < len(l) for x, l in enumerate(lists)):
            for x, l in enumerate(lists):
                if got[x] < need and k < len(l) and l[k] not in nx:
                    nx.append(l[k])
                    for y, p in enumerate(homes): got[y] += p in pages[l[k]]
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
    out = {"_note": "Pharmakon Insight's index (scripts/insight/build_index.py): vectors of every answer's wordings (W), of the same wordings with the drug names taken out (M) and of its short answer (S) (made with the model named here, int8, each row scaled to unit length by the page); its words for the overlap score; the drugs it is about; the names that name a drug in a question; and the weights, the tiers and the judge (from site/insight/model.json).",
           "model": MODEL, "model_sha256": MODEL_SHA256, "dim": int(Wv.shape[1]), "weights": CONFIG["weights"], "tiers": CONFIG["tiers"], "judge": CONFIG["judge"],
           "ids": ids, "rows": rows, "W": wb, "M": mb, "S": sb, "docs": docs, "slugs": slugs, "about": [[at[s] for s in a["about"]] for a in A],
           "names": [[n, [at[s] for s in xs]] for n, xs in names], "variants": len(var), "more": sum(1 for a in A if more.get(a["id"]))}
    # 2.5: the list of questions not answered yet (data/site/wanted.json), as a second, small index of the same kind
    wl = wanted_index(json.load(open(IN, encoding="utf-8")).get("wanted") or [], out, names, pat, at)
    if wl: out["wanted"] = wl
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


WANT_CUT = 0.75   # the judge's number from which a typed question IS a listed one (see wanted_index)


def wanted_index(items, out, names, pat, at):
    """The list of questions the site does not answer yet (site 2.5; the senior author, 15 November 2026: "make the site
    understand on its own what the users want added in the website in-app and not via email"). When no answer is a best
    match, the page takes a second look, at this list, with the same ranking and the same judge: a typed question that is
    one of the listed questions gets "Not answered yet. It is on our list", and the site counts one more person asking
    it, by the item's number alone (the words never leave the device).

    Each item is indexed as an answer is: its question and its other ways of asking as the wordings, its question again
    as the short line. An item the site answers by now (its own question gets a best match among the answers) is left
    out, so the list empties itself as answers are written. How well this finds a listed question was measured on
    answered questions standing in for listed ones (42 at random, five times; hurried rewordings held out): with the
    question alone 10 in 100 found their item; with six ways of asking and the judge at 0.75, 82 in 100, none a wrong
    item, and 4 in 100 questions that were not on the list were taken for a listed one (at the answers' own cut, 0.60:
    87 and 6). So every item carries six ways, and the cut for the list is 0.75 (WANT_CUT)."""
    if not items: return None
    R = Ranker(out); keep, gone = [], []
    for w in items:
        k = R.rank(w["q"])
        (gone if k["best"] else keep).append((w, k["best"][0]["id"] if k["best"] else None))
    if gone: print("insight: " + str(len(gone)) + " listed questions are answered by now and left off the list: " + ", ".join(w["id"] + " by " + c for w, c in gone), file=sys.stderr)
    items = [w for w, _ in keep]
    if not items: return None
    rows, W_txt = [], []
    for i, w in enumerate(items):
        for t in list(dict.fromkeys([w["q"]] + [x for x in w.get("ways") or [] if isinstance(x, str) and x.strip()])): rows.append(i); W_txt.append(t)
    shorts = [w["q"] for w in items]; M_txt = [pat.sub("it", t) for t in W_txt]
    V = embed_all(W_txt + shorts + M_txt)
    Wv, Sv, Mv = V[:len(W_txt)], V[len(W_txt):len(W_txt) + len(shorts)], V[len(W_txt) + len(shorts):]
    wb, _ = int8(Wv); sb, _ = int8(Sv); mb, _ = int8(Mv)
    name_of = {n: xs for n, xs in names}
    about = []
    for w in items:   # the drugs an item is about: the ones its question names (a family's name: every drug of it)
        ab = set()
        for m in pat.finditer(w["q"]): ab |= set(name_of.get(m.group(1).lower(), []))
        about.append(sorted(at[s] for s in ab if s in at))
    print(f"insight: {len(items)} questions on the list of those not answered yet, {len(W_txt)} wordings", file=sys.stderr)
    return {"ids": [w["id"] for w in items], "q": shorts, "rows": rows, "W": wb, "M": mb, "S": sb, "docs": [" ".join(dict.fromkeys([w["q"]] + (w.get("ways") or []))) for w in items], "about": about, "cut": WANT_CUT}


def evaluate(D, near=None):
    """The page's rule on the gold set's forum questions (full answer: either reader names an answer that fully answers
    it; partial: a reader names it as answering part; unanswerable: both readers say none does), printed as
    scripts/insight/judge2.py prints it: the best matches at the judge's cut of model.json and at other cuts, on the
    odd-numbered questions (dev: where a cut is chosen), the even-numbered ones (test: where it is reported) and all; the
    related answers at each cut; and the near-miss readers' questions (each written as a question one answer does NOT
    answer: is that answer given as its best match?)."""
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
        tests.append((g["n"], g["question"], full, part, all(x.get("none") for x in ls)))
    def looks(questions):
        tx = [R.texts(q) for q in questions]; V = embed_all([t[0] for t in tx] + [t[1] for t in tx])
        return [R.look(V[i], V[len(tx) + i], questions[i], tx[i][2]) for i in range(len(tx))]
    LG = looks([t[1] for t in tests])
    n_full = sum(bool(t[2]) for t in tests); n_un = sum(t[4] for t in tests)
    order = [np.argsort(-L["by"], kind="stable") for L in LG]
    h1 = sum(R.ids[o[0]] in tests[i][2] for i, o in enumerate(order) if tests[i][2]) / n_full
    h3 = sum(any(R.ids[j] in tests[i][2] for j in o[:3]) for i, o in enumerate(order) if tests[i][2]) / n_full
    print(f"model {D['model']}; gold questions: {len(tests)}; {n_full} with a full answer, {n_un} unanswerable; candidates in order of first look + weights.topic x topic: a full answer first {h1 * 100:.1f}%, in the first three {h3 * 100:.1f}%")
    print("judge weights (on standardized numbers):", {f: round(float(w), 2) for f, w in zip(R.J["features"], R.J["w"])}, "bias", round(float(R.J["b"]), 2), "; a best match from", R.J["best"])
    keep = R.J; cuts = sorted({0.5, 0.6, 0.7, 0.8, float(keep["best"])})
    # the near-miss questions: (question, the answer it must not get), for answers on the page
    nm = [(q, a) for a, qs in sorted((near or {}).items()) if a in idset for q in qs]
    LN = looks([q for q, _ in nm]) if nm else []
    def ranked(L): return R.tiers(L["plain"], L["topic"], L["groups"], lambda c: R.six(L, c))
    for split, use in (("dev (odd-numbered)", lambda n: n % 2 == 1), ("test (even-numbered)", lambda n: n % 2 == 0), ("all", lambda n: True)):
        rs = [(t, L) for t, L in zip(tests, LG) if use(t[0])]
        nun = sum(t[4] for t, _ in rs); nf = sum(bool(t[2]) for t, _ in rs)
        print(f"gold, {split}: {len(rs)} questions")
        for th in cuts:
            R.J = dict(keep, best=th); b = f = p = un = 0; rel = {"rows": 0, "good": 0, "q": 0, "un": 0}; miss = 0
            for (nq, q, full, part, u), L in rs:
                best, related, _ = ranked(L)
                if best: a = R.ids[best[0]]; b += 1; f += a in full; p += a in part; un += u
                elif full and any(R.ids[j] in full for j in related): miss += 1
                if related:
                    rel["q"] += 1; rel["rows"] += len(related); rel["un"] += u; rel["good"] += sum(R.ids[j] in full or R.ids[j] in part for j in related)
            w = b - f - p; label = f"judge >= {th:g} (and about the drugs named)" + (" <- model.json" if th == float(keep["best"]) else "")
            print(f"  {label:<46} best match for {b:3d} of {len(rs)}: full {f:3d} ({100 * f / max(1, b):3.0f}%), partial {p:3d} ({100 * p / max(1, b):3.0f}%), wrong {w:3d} ({100 * w / max(1, b):3.0f}%); "
                  f"unanswerable given one {un} of {nun}; questions with a full answer that get it as best match {f} of {nf}; "
                  f"related: {rel['rows']} rows for {rel['q']} questions, {100 * rel['good'] / max(1, rel['rows']):.0f}% full or partial, {rel['un']} of {nun} unanswerable questions get some; "
                  f"no best match but a full answer under Related {miss}")
    if nm:
        for th in cuts:
            R.J = dict(keep, best=th); hit = sum(any(R.ids[j] == a for j in ranked(L)[0]) for (q, a), L in zip(nm, LN))
            print(f"near-miss questions given the answer they do not get as best match, judge >= {th:g}: {hit} of {len(nm)} ({100 * hit / len(nm):.1f}%)")
    R.J = keep


if __name__ == "__main__":
    main()
