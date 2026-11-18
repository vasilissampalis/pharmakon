/* ---------- Insight (site 2.2.0, 14 November 2026; the senior author: the site should feel like your own thinking. Site 2.3,
   15 November: "as smart as possible", "it has a high error rate", "it should be everywhere"). The search box understands a
   question asked in a reader's own words, on the reader's own phone: nothing typed leaves it. It never writes text: it only
   finds answers the editors have checked.
   How: a small model turns the question into numbers with ONNX Runtime Web (MIT), both published with the site. Since 2.3
   the model is Pharmakon's own: the open model all-MiniLM-L6-v2 (Apache-2.0) trained further on this site's own examples
   only (the ways people ask each checked answer), as insight/NOTICE-pharmakon-insight-1.txt states (the model's file is
   named in site/insight/model.json; how it was made and measured: scripts/insight/MODELS.md), and those numbers
   are compared with every wording of every question on the site and its short answer, made into numbers with the same model
   when the site is built (data/insight.json, scripts/insight/build_index.py). The files (about 40 MB, kept by the browser's
   cache for the next visit) are fetched only when someone puts the cursor in the search box or types in it, never with the
   page; on a connection that asks to save data, or a 2G one, only when the reader taps the quiet line that offers it. Word
   search stays as it was and answers at once.
   2.3, what changed:
   - One function ranks: insRank(question, { drug }) gives { routes, best, related }. Every question gets two looks (insScore):
     the first with the drug's own name brought along (2.2.0's score), the second with the drug names taken out (the topic).
     "best" (none or one) is the first answer when it is about every drug the question names and a small judge, fed six
     numbers of that answer, says it answers what was asked (insTiers); "related" (up to 3) are near answers. Every number
     comes from data/insight.json (weights, tiers, judge): none is written here.
   - On a drug's page a question that names no drug is about that drug; the box there reads "Ask about cannabis".
   - Routes: a question that is really a request for something else (two drugs: the mixing tool; a dose: the Doses block;
     an emergency in progress: "If it gets too much"; testing a sample: the test kits; "what is X": the drug's page) gets
     that as its first row. Getting drugs, hiding use, beating a drug test: no route and no answer.
   - While typing: the route, then "Best match" with the short answer in full, then "Related"; with no best match, one calm
     line, "We haven't checked exactly this yet.", and the way to ask us. A related answer is never shown as the answer.
     (2.9) A question that is not finished ("can i die from", "is it addictive" off a drug's page) gets no verdict and no
     way to send it: "Which drug do you mean?" or "Go on.", with what was found under "You may mean". A question that is
     not about drugs by its words is told so ("This does not look like a question about drugs"), or, where one unknown
     word stands among words that could be asked of any drug, "We do not know <word> as a drug"; both keep a way to send.
   - Enter opens the sheet for the question as asked: the person's own words as the heading, each best answer in full under
     it; "full evidence", "the studies", "in detail" open "How do we know?"; "short", "tl;dr", "eli5" keep to the short
     answer and its But. No guess first, anywhere. No emergency line, except when the question is an emergency.
   - An answer linked from outside its own page opens in this sheet, over the page (Myth or fact's "Read the answer", the
     start page, a shared answer's other questions), and Back returns to exactly where the reader was.
   - Next questions ("People also ask" here, "Read next" on the pages) are the nearest answers by meaning, never from another
     drug, without the ones already opened in this visit (const INS_NEXT, put at the head of the page by site/build.js). ---------- */
const INS = { state: "idle", tries: 0, cache: new Map(), seq: 0, timer: 0, times: [], queue: Promise.resolve(), run: null, view: null, back: null, from: null, go: null, want: null, list: null, scope: null, wantT: 0 };
const INS_WAIT = 150;       // ms of no typing before a question is looked up (each keystroke still gets the word search at once)
const INS_WORDS = 3;        // a question of three words or more; a drug's name alone is for the word search
const INS_END = 4;          // the calm end comes after four answers in a row
const INS_BASE = () => new URL("insight/", document.baseURI).href;
// a connection that asks to save data, or a very slow one: nothing is fetched until the reader asks for it
const insSaver = () => { const c = navigator.connection; return !!(c && (c.saveData || /^(slow-)?2g$/.test(c.effectiveType || ""))); };
const insMB = () => (typeof INS_MB === "number" ? INS_MB : 40);   // what the reader's browser fetches once (site/build.js adds up the files)
const insGetText = () => "Understand questions in your own words (downloads about " + insMB() + " MB once)";

/* Loading, on first use. One thread (no cross-origin isolation is needed); the WebGPU build is never fetched. The page is
   told the model's file name by the build (const INS_MODEL), so its download starts at once; the index names the model that
   made it too, and if the two ever differ (an old page with a new index) the page goes by the index. */
function insScript(src) {
  return new Promise((ok, fail) => { const s = document.createElement("script"); s.src = src; s.async = true; s.onload = () => ok(); s.onerror = () => fail(new Error("script " + src)); document.head.appendChild(s); });
}
function insightLoad() {
  if (INS.state !== "idle") return INS.loading || Promise.resolve(INS.state === "ready");
  if (typeof WebAssembly !== "object" || typeof BigInt64Array === "undefined" || typeof fetch !== "function" || typeof INS_MODEL !== "string") { INS.state = "off"; return Promise.resolve(false); }
  INS.state = "loading"; INS.tries++; INS.t0 = Date.now();
  const base = INS_BASE(), get = (u, how) => fetch(u).then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r[how](); });
  const runtime = insScript(base + "ort.wasm.min.js").then(() => {
    const ort = window.ort; ort.env.wasm.numThreads = 1; ort.env.wasm.proxy = false; ort.env.wasm.wasmPaths = base; ort.env.logLevel = "error"; return ort; });
  const told = get(base + INS_MODEL, "arrayBuffer"); told.catch(() => {});
  INS.loading = Promise.all([get("data/insight.json", "json"), get(base + "vocab.txt", "text"), runtime])
    .then(([data, vocab, ort]) => (data.model === INS_MODEL ? told : get(base + data.model, "arrayBuffer"))
      .then(b => ort.InferenceSession.create(new Uint8Array(b), { executionProviders: ["wasm"], graphOptimizationLevel: "all" }))
      .then(s => { insPrepare(data, vocab); INS.session = s; return insEmbed("warm up"); }))
    .then(() => { INS.state = "ready"; try { localStorage.setItem(INS_HAD, "1"); } catch (e) { /* no storage: fetched on first use, as before */ } insightReady(); return true; })
    // offline or an old browser: the word search goes on alone; one more try, and then the page says so (it never fails without a word)
    .catch(() => { INS.state = INS.tries < 2 ? "idle" : "off"; INS.loading = null; insightFailed(); return false; });
  return INS.loading;
}
/* (2.16.1; the senior author, 17 November 2026, with a picture of unrelated rows under his question: "did you make insight more stupid?";
   then, when the real result came: "for a few seconds it didn't and i thought it was stupid".) Those rows were the plain word search, shown
   while Insight was getting ready (on every opening of the page it has to be started again, which takes a few seconds). Two changes.
   One: a device that has fetched Insight before starts it when the page opens, so it is ready before the first question (nothing is
   downloaded for it: the files are in the browser's cache; a first visit still fetches them on first use, and a connection that saves
   data only when asked). Two: while it is getting ready, a whole question gets one calm line and no rows found by a word in common
   (insightAfterSearch); when it cannot start, the page says so and offers to try again. */
const INS_HAD = "pk-ins-had", INS_SLOW = 8000;
function insWarm() {
  let had = false; try { had = localStorage.getItem(INS_HAD) === "1"; } catch (e) { had = false; }
  if (had && INS.state === "idle" && !insSaver()) insightLoad();
}
function insightFailed() {
  const s = document.getElementById("search"), box = document.getElementById("search-results");
  if (s && box && !box.hidden && s.value.trim()) runSearch(s.value);
}
// the index: int8 vectors, each row scaled back to unit length; the words of each answer for the overlap; the drug names
function insRows(b64, dim) {
  const bin = atob(b64), n = bin.length / dim, M = new Float32Array(bin.length);
  for (let r = 0; r < n; r++) {
    let s = 0; const o = r * dim;
    for (let j = 0; j < dim; j++) { const b = bin.charCodeAt(o + j), x = b > 127 ? b - 256 : b; M[o + j] = x; s += x * x; }
    const k = 1 / Math.max(Math.sqrt(s), 1e-9); for (let j = 0; j < dim; j++) M[o + j] *= k;
  }
  return M;
}
const insTok = s => String(s).toLowerCase().match(/[a-z0-9]+/g) || [];
/* (2.15, 17 November 2026) Old phones. Safari before 16.4 (every iPhone that stopped at iOS 15, and those not updated since early 2023)
   cannot read a look-behind in a pattern. Written as a literal, one such pattern stopped the whole page there: nothing was shown at all.
   Now no pattern of the page is written with one. Where a word's left edge is needed, insNb gives the look-behind where the browser
   reads it, and the plain word edge (\b) where it does not: on such a phone a name that begins with a letter outside a to z is not
   found by its edge, and everything else reads the same. The build refuses a look-behind anywhere else in the page's script. */
const INS_LB = (() => { try { new RegExp("(?<!a)b"); return true; } catch (e) { return false; } })();
function insNb(cls) { return INS_LB ? "(?<![" + cls + "])" : "\\b"; }

const insRx = n => n.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&");
// word overlap (TF-IDF as scripts/insight/eval_match.py's Lexical): a word's weight is log(1 + N / documents with it);
// post: word -> [answer, weight in its unit-length vector]
function insWords(docs) {
  const N = docs.length, df = new Map(), post = new Map();
  docs.forEach(t => new Set(insTok(t)).forEach(w => df.set(w, (df.get(w) || 0) + 1)));
  const idf = new Map([...df].map(([w, n]) => [w, Math.log(1 + N / n)]));
  docs.forEach((t, i) => { const v = new Map(); insTok(t).forEach(w => v.set(w, (v.get(w) || 0) + idf.get(w)));
    const n = Math.sqrt([...v.values()].reduce((a, x) => a + x * x, 0)) || 1; v.forEach((x, w) => { if (!post.has(w)) post.set(w, []); post.get(w).push([i, x / n]); }); });
  return { idf, post };
}
function insPrepare(d, vocabText) {
  INS.dim = d.dim; INS.ids = d.ids; INS.rows = d.rows; INS.wt = d.weights; INS.t = d.tiers; INS.judge = d.judge;
  INS.W = insRows(d.W, d.dim); INS.M = insRows(d.M, d.dim); INS.S = insRows(d.S, d.dim);
  INS.idx = new Map(d.ids.map((id, i) => [id, i]));
  INS.about = d.about.map(xs => new Set(xs.map(k => d.slugs[k])));   // the drugs each answer is about
  // the names that name a drug in a question (build_index.py's names_table: the longest first), and the drugs each stands for
  INS.nameOf = new Map(d.names.map(([n, xs]) => [n, xs.map(k => d.slugs[k])]));
  INS.nameRe = new RegExp(insNb("\\p{L}\\p{N}_") + "(" + d.names.map(([n]) => insRx(n)).join("|") + ")(?![\\p{L}\\p{N}_])", "giu");
  Object.assign(INS, insWords(d.docs));
  // 2.5: what makes a question a question about drugs (site/insight/scope.json, through the index: the same patterns, between
  // the same word boundaries, as the build's Ranker.in_scope), and the list of questions not answered yet
  // (data/site/wanted.json): a second, small index of the same kind as the answers', with the judge's cut for it
  const wb = insNb("A-Za-z0-9_") + "(?:", we = ")(?![A-Za-z0-9_])", L = d.wanted;
  INS.scope = d.scope ? { re: new RegExp(wb + d.scope.src + we, "i"), not: new RegExp(wb + d.scope.not + we, "gi") } : null;
  INS.unfin = d.scope && d.scope.unfinished ? insUnfinRule(d.scope.unfinished, d.names.map(x => x[0])) : null;   // 2.9: is a question finished?
  INS.spell = d.scope && d.scope.spell && INS.unfin ? insSpellRule(d.scope.spell, d.scope.unfinished.names || []) : null;   // 2.9.1: a drug's name with a letter wrong
  // 2.13: the places of the site, found by the meaning of a question (site/insight/places.json through the index: insWhere)
  { const PL = d.places; INS.places = PL && PL.ids && PL.ids.length ? { ids: PL.ids, rows: PL.rows, meta: PL.meta, cut: PL.cut, near: PL.near, W: insRows(PL.W, d.dim) } : null; }
  INS.list = L && L.ids.length ? Object.assign({ ids: L.ids, q: L.q, rows: L.rows, cut: L.cut, near: L.near || [0, 0], W: insRows(L.W, d.dim), M: insRows(L.M, d.dim), S: insRows(L.S, d.dim),
    about: L.about.map(xs => new Set(xs.map(k => d.slugs[k]))) }, insWords(L.docs)) : null;
  // vocab.txt: one token a line, its line number its id (as the tokenizers library reads it)
  const lines = vocabText.split("\n"); if (lines.length && lines[lines.length - 1] === "") lines.pop();
  INS.vocab = new Map(); lines.forEach((t, i) => INS.vocab.set(t.trimEnd(), i));
  INS.unk = INS.vocab.get("[UNK]"); INS.cls = INS.vocab.get("[CLS]"); INS.sep = INS.vocab.get("[SEP]");
  INS.special = new Map(["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"].filter(t => INS.vocab.has(t)).map(t => [t, INS.vocab.get(t)]));
  // drug names for the first look (tune.py's expand): each drug's slug, the parts of its name and its street names of three
  // letters or more; and every one of those names with its drug, for "what is speed"
  INS.any = new Map();
  INS.drugs = SUBSTANCES.map(s => {
    const ns = new Set([s.slug.replace(/-/g, " ")]);
    s.name.split(/[()\/,;]| and /).forEach(p => { p = p.trim().toLowerCase(); if (p.length >= 3) ns.add(p); });
    (ALIASES[s.slug] || []).forEach(a => { if (a.length >= 3) ns.add(a.toLowerCase()); });
    ns.forEach(n => { if (!INS.any.has(n)) INS.any.set(n, s.slug); });
    const alt = [...ns].sort((a, b) => b.length - a.length).map(insRx).join("|");
    return { slug: s.slug, canon: s.name.split(" (")[0], re: new RegExp(insNb("\\p{L}\\p{N}_") + "(?:" + alt + ")(?![\\p{L}\\p{N}_])", "u") };
  }).sort((a, b) => (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0));
  INS.canon = new Map(INS.drugs.map(x => [x.slug, x.canon]));
}
function insExpand(t) {
  const tl = t.toLowerCase(), extra = INS.drugs.filter(x => x.re.test(tl) && !tl.includes(x.canon.toLowerCase())).map(x => x.canon);
  return t + (extra.length ? " (" + extra.join(", ") + ")" : "");
}

/* The tokenizer: BERT uncased WordPiece, as the tokenizers library's BertWordPieceTokenizer (lowercase) does it, so the page
   and the build make the same numbers (scripts/insight/parity.js checks it). */
const INS_SPECIAL = /(\[PAD\]|\[UNK\]|\[CLS\]|\[SEP\]|\[MASK\])/;
const insCJK = c => (c >= 0x4E00 && c <= 0x9FFF) || (c >= 0x3400 && c <= 0x4DBF) || (c >= 0x20000 && c <= 0x2A6DF) || (c >= 0x2A700 && c <= 0x2B73F) ||
  (c >= 0x2B740 && c <= 0x2B81F) || (c >= 0x2B920 && c <= 0x2CEAF) || (c >= 0xF900 && c <= 0xFAFF) || (c >= 0x2F800 && c <= 0x2FA1F);
const insPunc = ch => { const c = ch.codePointAt(0); return (c >= 33 && c <= 47) || (c >= 58 && c <= 64) || (c >= 91 && c <= 96) || (c >= 123 && c <= 126) || /\p{P}/u.test(ch); };
function insNormalize(t) {
  let out = "";
  for (const ch of t) {                                   // clean the text: drop NUL, U+FFFD and control characters; any space is a space
    const c = ch.codePointAt(0);
    if (c === 0 || c === 0xFFFD) continue;
    if (ch === "\t" || ch === "\n" || ch === "\r") { out += " "; continue; }
    if (/\p{C}/u.test(ch)) continue;
    if (/\s/u.test(ch)) { out += " "; continue; }
    out += insCJK(c) ? " " + ch + " " : ch;                // Chinese characters stand alone
  }
  out = out.normalize("NFD").replace(/\p{Mn}/gu, "");     // accents off
  let low = ""; for (const ch of out) low += ch.toLowerCase();   // one character at a time, as the library does
  return low;
}
function insPieces(word, out) {
  const cs = Array.from(word);
  if (cs.length > 100) { out.push(INS.unk); return; }
  const ids = []; let start = 0;
  while (start < cs.length) {
    let end = cs.length, id;
    while (start < end) { id = INS.vocab.get((start > 0 ? "##" : "") + cs.slice(start, end).join("")); if (id !== undefined) break; end--; }
    if (id === undefined) { out.push(INS.unk); return; }
    ids.push(id); start = end;
  }
  out.push(...ids);
}
function insEncode(text) {
  const ids = [];
  String(text).split(INS_SPECIAL).forEach(part => {
    if (!part) return;
    if (INS.special.has(part)) { ids.push(INS.special.get(part)); return; }
    let w = "";
    const flush = () => { if (w) insPieces(w, ids); w = ""; };
    for (const ch of insNormalize(part)) { if (/\s/u.test(ch)) flush(); else if (insPunc(ch)) { flush(); insPieces(ch, ids); } else w += ch; }
    flush();
  });
  return [INS.cls].concat(ids.slice(0, 126), [INS.sep]);   // at most 128 tokens with [CLS] and [SEP]
}
// one text in, a unit vector out: the model's last layer, averaged over the tokens (as sentence-transformers does)
function insEmbed(text) {
  return insRun(async () => {
    const ids = insEncode(text), n = ids.length, ort = window.ort, s = INS.session;
    const feeds = { input_ids: new ort.Tensor("int64", BigInt64Array.from(ids, x => BigInt(x)), [1, n]), attention_mask: new ort.Tensor("int64", new BigInt64Array(n).fill(1n), [1, n]) };
    if (s.inputNames.includes("token_type_ids")) feeds.token_type_ids = new ort.Tensor("int64", new BigInt64Array(n), [1, n]);
    const out = await s.run(feeds), h = out[s.outputNames[0]].data, d = h.length / n, v = new Float32Array(d);
    for (let i = 0; i < n; i++) for (let j = 0; j < d; j++) v[j] += h[i * d + j];
    let q = 0; for (let j = 0; j < d; j++) { v[j] /= n; q += v[j] * v[j]; }
    const k = 1 / Math.max(Math.sqrt(q), 1e-9); for (let j = 0; j < d; j++) v[j] *= k;
    return v;
  });
}
// one run at a time on the session
function insRun(fn) { const p = INS.queue.then(fn, fn); INS.queue = p.catch(() => {}); return p; }

/* ---------- Reading the question (2.3) ---------- */
const insClean = raw => String(raw == null ? "" : raw).trim().replace(/\s+/g, " ");
const insWordsIn = q => (q.match(/[\p{L}\p{N}]+/gu) || []).length;
// the drugs a question names, each as the list of drugs its name stands for (a family's name stands for every drug of it)
function insNamed(t) {
  const out = [], seen = new Set();
  for (const m of String(t).matchAll(INS.nameRe)) { const g = INS.nameOf.get(m[1].toLowerCase()); if (!g) continue; const k = g.join("|"); if (!seen.has(k)) { seen.add(k); out.push(g); } }
  return out;
}
const insMask = t => String(t).replace(INS.nameRe, "it");
// what is embedded for a question: with the drug's own name brought along, and with the drug names taken out; and the drugs
// it is about (on a drug's page, a question that names none is about that drug)
function insTexts(q, drug) {
  let groups = insNamed(q), full = insExpand(q);
  if (!groups.length && drug && INS.canon.has(drug)) { groups = [[drug]]; full += " (" + INS.canon.get(drug) + ")"; }
  return { full, masked: insMask(q), groups };
}
/* Depth words: understood, and taken out before matching. A request for the evidence ("give me the full evidence about …",
   "… the studies", "… in detail", "scientific", "explain …") opens every answer with "How do we know?" open; a request for
   the short of it ("tl;dr", "eli5", "short answer", "in a sentence", "simply") keeps to the short answer and its But. They
   count only where a request stands (the start or the end of the question), so "why was my trip so short" stays a question. */
const INS_DEPTH = [
  [/^(?:(?:please|pls|can you|could you|i want|i need|i'?d like)\s+)*(?:(?:give|show|tell|get|find|send)\s+(?:me\s+|us\s+)?|what(?:'s|\s+is|\s+are)\s+|is there\s+|are there\s+)?(?:(?:a|an|the|all|any|some|of|full|whole|complete|entire|actual|real|hard|scientific|detailed|more)\s+)*(?:evidence|studies|research|sources|science|proof|references|citations)\s+(?:about|on|for|of|behind|that|whether|regarding)\s+/i, "full"],
  [/^(?:(?:please|pls|can you|could you)\s+)*explain\s+(?:(?:to\s+)?me\s+)?(?:simply|briefly|in simple (?:terms|words)|like i'?m (?:five|5|a child))\s+/i, "short"],
  [/^(?:(?:please|pls|can you|could you)\s+)*explain\s+(?:(?:to\s+)?me\s+)?(?:in (?:full |more )?(?:detail|depth)\s+)?/i, "full"],
  [/^(?:tl;?dr|eli5|in short|in brief|briefly|quick(?:ly)?|(?:short|simple|quick) (?:answer|version)|in (?:a|one) sentence|simply(?: put)?)\s*[:,;-]?\s+/i, "short"],
  [/^(?:short|simple|quick)\s*[:,;-]\s*/i, "short"],
  [/[\s,;:(–-]+(?:in (?:full |more |great )?(?:detail|depth)|with (?:the |all the |full )?(?:sources|evidence|studies|references|citations)|(?:(?:the|all the|full|all) )?(?:evidence|studies|sources|references|citations)|scientific(?:ally)?|detailed|explained?)(?:\s+(?:please|pls|plz|thanks|thx))?\s*[)?.!]*$/i, "full"],
  [/[\s,;:(–-]+(?:tl;?dr|eli5|in short|in brief|briefly|(?:short|simple|quick) (?:answer|version)|in simple (?:terms|words)|in plain (?:english|words)|in (?:a|one) sentence|simply|keep it (?:short|simple))(?:\s+(?:please|pls|plz|thanks|thx))?\s*[)?.!]*$/i, "short"],
  [/[,;:(?!–-]\s*(?:short|simple|quick)\s*[)?.!]*$/i, "short"],
  [/\bscientific(?:ally)?\s+(?=\S)/i, "full"]
];
function insDepth(q) {
  let core = q, full = false, short = false;
  for (let n = 0; n < 4; n++) {
    const was = core;
    for (const [re, kind] of INS_DEPTH) { const m = core.match(re); if (!m || !m[0].trim()) continue;
      const rest = (core.slice(0, m.index) + " " + core.slice(m.index + m[0].length)).replace(/\s+/g, " ").trim();
      if (!insWordsIn(rest)) continue;                       // a question made only of such words is left as it is
      core = rest; if (kind === "full") full = true; else short = true; }
    if (core === was) break;
  }
  return { core, depth: full ? "full" : short ? "short" : "" };
}

/* Where a route leads. The pages are being rebuilt (branch pages23) and the addresses of their sections may change: every
   link Insight makes to a part of a page is made here and nowhere else, so the editor adjusts this one table at the merge.
   href: today's hash route. el: the block to bring into view once the page has drawn (left out where the route itself does
   it). On today's pages the Doses block (#sf-dose) and the test kits block (#sf-test) sit inside "Staying safer", which has
   no route of its own that lands on them: the drug's page opens, then the block is brought into view. */
const INS_PLACE = {
  help: slug => ({ href: "#s-" + slug + "/part-d-help" }),              // "If it gets too much" (#d-help)
  doses: slug => ({ href: "#s-" + slug + "/part-d-doses" }),            // the Doses section (#d-doses; 2.3 pages: every part is a section with its own address)
  test: slug => ({ href: "#s-" + slug + "/part-d-kits" }),              // the Test kits section (#d-kits)
  page: slug => ({ href: "#s-" + slug }),                               // the drug's page
  mix: () => ({ href: "#interactions", el: "mix2" }),                   // the mixing tool (insMixPick chooses both drugs)
  numbers: () => ({ href: "#emergency" }),                              // emergency numbers by country
  checking: () => ({ href: "#checking" }),                              // drug checking and test kits, no drug named
  drugs: () => ({ href: "#substances" })                                // every drug (a dose question that names none)
};
/* Routes: what kind of request is this? A small table in order; each entry has its test here, and scripts/ux/insight_check.js
   asks each one a question that must take it and one that must not. A route is a first row, in the list and in the sheet;
   the answers that match still show under it. */
const INS_RE = {
  // an emergency in progress: someone not breathing, not waking, fitting, overdosing now, too high, a trip gone bad
  help: new RegExp([
    "\\b(?:not|isn'?t|stopped|can'?t|cant|cannot|barely|struggling to)\\s+breath(?:e|ing)\\b",
    "\\b(?:won'?t|wont|can'?t|cant|cannot|not|isn'?t)\\s+wak(?:e|ing)(?:\\s+up)?\\b", "\\bunresponsive\\b", "\\bunconscious\\b", "\\bpassed out\\b",
    "\\b(?:is|are|'s|he'?s|she'?s|i'?m|am|friend|someone|they'?re)\\s+(?:\\w+\\s+)?having\\s+a\\s+(?:seizure|fit)\\b", "\\bseizing\\b",
    "\\b(?:is|am|are|i'?m|he'?s|she'?s|they'?re|might be|may be|could be)\\s+(?:\\w+\\s+)?overdosing\\b", "\\boverdosing\\s+(?:right\\s+)?now\\b", "\\bod'?ing\\b",
    "\\btoo high\\b", "\\bgreen(?:ing|ed)?\\s+out\\b", "\\bwhitey\\b", "\\bbad trip\\b.{0,24}\\bhelp\\b", "\\bhelp\\b.{0,24}\\bbad trip\\b", "\\bfreaking out\\b", "\\bturning blue\\b", "\\bblue lips\\b",
    "\\bi think (?:i'?m|i am|he'?s|she'?s|they'?re) (?:dying|overdosing)\\b"].join("|"), "i"),
  // "what do i do" is an emergency only beside a sign that something is happening now
  whatdo: /\bwhat (?:do|should|can|shall) (?:i|we) do\b/i,
  acute: /\b(?:just|right now|now|tonight|took|taken|ate|eaten|swallowed|drank|too much|too many|unwell|sick|shaking|sweating|overheat\w*|burning up|heart|chest|breath\w*|pass(?:ed|ing)? out|faint\w*|collaps\w*|seiz\w*|fitting|panic\w*|freak\w*|scared|terrified|bad trip|too high|overdos\w*|unconscious|unresponsive|blue|vomit\w*|throwing up|emergency|ambulance|help me)\b/i,
  // someone writing about ending their own life: the numbers, at once
  self: /\b(?:i|i'?m|im|i am|i feel|feeling|me)\b[^?.!]{0,30}\bsuicid\w*|\bsuicid\w*\b[^?.!]{0,20}\b(?:myself|me|i)\b|\bkill(?:ing)? myself\b|\bwant(?:ing)? to die\b|\bend(?:ing)? my life\b|\bdon'?t want to (?:live|be alive|be here)\b/i,
  // a dose question: how much to take, which dose, an amount. Not a question about what a dose does ("what does one dose of
  // meth do", "after high doses of DXM"): those are answers the site has.
  dose: new RegExp([
    "\\bhow\\s+much\\b[^?.!]{0,40}\\b(?:should|can|could|do|does|did|would|to|must)\\b[^?.!]{0,20}\\b(?:take|use|dose|smoke|snort|drink|eat|swallow|need|redose|start with|try)\\b",
    "\\bhow\\s+(?:much|many)\\b[^?.!]{0,50}\\b(?:too much|too many|is safe|safe to take|is enough|to overdose|to od|lethal|fatal)\\b",
    "\\bhow many\\s+(?:mg|milligrams?|micrograms?|ug|mcg|grams?|pills?|tabs?|tablets?|lines?|hits?|drops?|puffs?|capsules?|caps|bumps?|beers?|drinks?|joints?|shots?|units?)\\b",
    "\\b(?:what(?:'s|s|\\s+is|\\s+are|\\s+would be|\\s+should be)|which)\\s+(?:(?:a|an|the|my|your)\\s+)?(?:(?!of\\b|after\\b|effects?\\b|happens\\b)[\\w-]+\\s+){0,3}(?:dose|doses|dosage|dosages|amount)\\b",
    "\\bwhat\\s+(?:dose|dosage)\\b", "\\bwhat\\s+amount\\s+(?:of|should|is|to)\\b",
    "\\b(?:right|good|safe|safest|starting|recommended|correct|proper|max|maximum|minimum|lethal|fatal|deadly|threshold|beginner|beginners|first[- ]time|best|ideal|average|typical)\\s+(?:[\\w-]+\\s+)?(?:dose|doses|dosage|dosages|amount)\\b",
    "\\b(?:dose|doses|amount)\\b[^?.!]{0,30}\\btoo (?:much|high)\\b", "\\b(?:dosage|dosages|dosing|redose|redosing|re-dose)\\b",
    "\\b(?:dose|doses)\\s+(?:for|guide|chart|calculator|range|by weight|per kg)\\b",
    "\\b\\d+(?:[.,]\\d+)?\\s?(?:mg|milligrams?|ug|µg|mcg|micrograms?|ml)\\b",
    "\\b\\d+(?:[.,]\\d+)?\\s?(?:g|grams?|pills?|tabs?|tablets?|lines?|hits?|drops?|bumps?)\\b[^?.!]{0,40}\\b(?:too much|enough|safe|ok|okay|a lot|dangerous|overdose|fine|kill)\\b"].join("|"), "i"),
  // testing a sample: a request to test or to get a kit, not a question about how well tests work (those have answers)
  test: new RegExp([
    "\\bhow\\s+(?:do|can|could|should|would)\\s+(?:i|you|u|we|one)\\s+(?:test|check)\\b", "\\bhow\\s+to\\s+(?:test|check|use\\s+(?:a\\s+)?(?:test|reagent|fentanyl))\\b",
    "\\bis\\s+(?:my|this|the)\\s+(?:[\\w-]+\\s+){1,3}(?:real|pure|cut|laced|fake|legit|bunk|spiked|contaminated)\\b",
    "\\b(?:test|check)\\s+(?:my|your|the|this|a)\\s+(?:[\\w-]+\\s+)?(?:drugs?|pills?|powder|stuff|sample|tabs?|bag|gear|batch)\\b", "\\bwhat(?:'s| is)\\s+(?:really\\s+|actually\\s+)?in(?:side)?\\s+my\\b",
    "\\b(?:get|buy|order|find|need)\\s+(?:(?:a|an|some|the|my|free|cheap|good)\\s+){0,2}(?:[\\w-]+\\s+)?(?:test(?:ing)?\\s+kits?|test\\s+strips?|reagents?|fentanyl\\s+strips?)\\b",
    "\\b(?:which|best)\\s+(?:[\\w-]+\\s+)?(?:test(?:ing)?\\s+kits?|reagents?|test\\s+strips?)\\b",
    "\\bwhere\\b[^?.!]{0,30}\\b(?:test(?:ing)?\\s+kits?|test\\s+strips?|reagents?|fentanyl\\s+strips?|drug\\s+checking|tested|test\\s+(?:my|it|them))\\b",
    "\\bwhat\\s+(?:kind\\s+of\\s+|type\\s+of\\s+|sort\\s+of\\s+)?(?:test(?:ing)?\\s+kits?|test\\s+strips?|reagents?)\\s+(?:do|should|can|to|for|is|are|works?)\\b",
    "^(?:[\\w-]+\\s+){0,2}(?:test(?:ing)?\\s+kits?|reagents?|test\\s+strips?|drug\\s+checking)\\s*\\??$"].join("|"), "i"),
  /* (2.9.2; the senior author asked "are drugs legal in greece" and was told "We haven't checked exactly this yet", while the
     site has the answer on its page of treaties by country: "pharmakon insight has to incorporate all information from the
     website from all sections".) law: a question of what the law says: "is … legal", "the laws on", "go to jail for".
     "legal highs" are a kind of drug, and a question that begins with why, when, who or should asks for something else
     (lawNot). lawc: with a country named, one of these words is enough ("is it allowed in japan"). lawPlain: the question
     asks what is legal and nothing more ("are drugs legal in greece"): the route is its answer; any other keeps the line
     for a question we have not checked and the way to send it ("can you go to jail for weed": the route is shown, loose).
     nums: a question for an emergency number. checkc: drug checking, with a country named. */
  law: new RegExp(["\\b(?:is|are|isn'?t|aren'?t|was|were)\\b[^?.!]{0,50}\\b(?:legal(?! highs?\\b)|illegal|lawful|unlawful|banned|prohibited|outlawed|decriminali[sz]ed|criminali[sz]ed|controlled|allowed by law)\\b",
    "\\b(?:legal status|legality|drug laws?|the law|laws? (?:on|about|for|in|around|regarding)|penalt(?:y|ies)|(?:go|goes|going|went|sent|get) to (?:jail|prison)|(?:jail|prison) time|arrested for|get arrested|caught with|possession)\\b"].join("|"), "i"),
  lawNot: /^(?:why|when|who|should|shouldn'?t|how come|since when)\b/i,
  // (2.10.2) a greeting, and a question about the site itself: each has a line of its own, and nothing to send
  greet: /^(?:hi|hello|hey|yo|hiya|good (?:morning|evening|afternoon)|thanks|thank you|thx|ok|okay|test|testing)(?: (?:there|you|test|testing|pharmakon))*[.!? ]*$/i,
  about: /^(?:(?:who|what|how|where|why) (?:are|is|made|created|built|were) (?:you|this|this site|this website|pharmakon|insight|pharmakon insight)|what can you do|what do you do|how do you work|how does (?:this|it|insight|this site) work|are you (?:real|human|a human|a person|a robot|an ai|ai|a bot|a chatbot|chatgpt|there)|what(?:'s| is) your name|who am i talking to)[.!? ]*$/i,
  lawc: /\b(?:legal(?! highs?\b)|illegal|laws?|allowed|permitted|ok|okay|strict|tolerated|decriminali[sz]ed|banned)\b/i,
  lawPlain: /\b(?:legal|illegal|lawful|unlawful|banned|prohibited|outlawed|decriminali[sz]ed|criminali[sz]ed|controlled substance|controlled|allowed|permitted|legal status|legality|laws?|the law)(?:\s+(?:in|at|on|for|here|there|where|anywhere|everywhere|now|yet|today|still)\b[^?.!]*)?\s*[?.!]*$/i,
  nums: /\b(?:emergency|ambulance|poisons? (?:control|cent(?:er|re)|line|information)|helpline|hotline|crisis line)\b[^?.!]{0,40}\b(?:numbers?|lines?|phone|call)\b|\b(?:what|which) number\b|\bwho (?:do|should|can) (?:i|we|you) call\b|\bnumber (?:to|do i|should i) call\b/i,
  checkc: /\b(?:drug[- ]check\w*|pill[- ]test\w*|test(?:ing|ed)? (?:my |your |the |some )?(?:drugs?|pills?|stuff)|(?:drugs?|pills?) tested)\b/i,
  // two drugs: mixed (a mixing word), not compared, and not one as a treatment for the other, found in the other or counted
  // in deaths with it (those are questions with answers of their own, not a request for the mixing tool)
  mixing: /\b(?:mix|mixing|mixed|combin\w*|together|same time|at once|on top of|with|while (?:on|taking|drinking|using))\b/i,
  loose: /\b(?:and|plus|on|after|before|during)\b|[+&]/i,
  versus: /\b(?:vs\.?|versus|or|than|compared?|comparison|difference|differences|different|differ|better|worse|stronger|weaker|safer|same as|which)\b/i,
  notmix: /\b(?:therapy|treat\w*|trial|help(?:s|ed)?\s+(?:people\s+)?(?:with|stop|quit)|withdrawal|detox|addiction|use disorder|dependence|problems?|quit(?:ting)?|stop(?:ping)?|coming off|come off|replac\w*|substitut\w*|instead of|compar\w*|found in|laced|cut with|contain\w*|deaths?|died|strips?|false positive|shows? up)\b/i,
  // "what is ketamine", "tell me about speed": the rest must be a drug's name
  what: /^(?:(?:what(?:'s|\s+is|\s+are|s)|tell me about|about|info(?:rmation)? (?:on|about)|everything about|all about)\s+)?(?:(?:a|an|the)\s+)?(.+?)\s*\??$/i,
  // getting drugs, hiding use, beating a drug test: no route and no answer
  shops: /\b(?:dealer|dealers|plug|vendor|vendors|darknet|dark ?web|deep ?web|silk ?road)\b/i,
  buy: /\b(?:buy|buying|bought|purchase|purchasing|order|ordering|score|scoring)\s+(?:(?:some|any|more|good|real|pure|cheap|the|a|an|my|legit|quality)\s+){0,3}$/i,
  get: /\b(?:get|getting|find|finding|obtain|obtaining|source|sourcing|cop)\s+(?:(?:some|any|more|good|real|pure|cheap|the|a|an|my|legit|quality)\s+){0,3}$/i,
  ask: /\b(?:where|how|can i|could i|want to|trying to|need to)\b/i,
  // making a drug ("how to make …", "cook …", "how is … made"), not "does heat make molly overheating worse"
  make: /\b(?:how\s+(?:to|do\s+(?:i|you|u|we|they|people)|can\s+(?:i|you|u|we)|would\s+(?:i|you))\s+make|cook|cooking|synthesi[sz]e|synthesi[sz]ing|grow|growing|extract|extracting|brew|brewing|manufacture|manufacturing)\s+(?:(?:some|my|your|own|pure|the|a|good|homemade)\s+){0,3}$/i,
  made: /^\s+(?:(?:is|are|be|being|gets?|was|were)\s+)?(?:made|cooked|synthesi[sz]ed|grown|extracted|produced|manufactured)\b(?!\s+(?:of|from|me|my|him|her|us|them|you|it)\b)/i,
  how: /\bhow\b/i, recipe: /\b(?:recipe|synthesis)\b/i,
  fine: /\b(?:test(?:ing)?\s+kits?|strips?|reagents?|naloxone|narcan|help|treatment|therapy|prescri\w*|doctor|clinic|rehab|support|needle exchange|drug checking)\b/i,
  hide: /\bhow\s+(?:to|do\s+i|can\s+i)\s+(?:hide|conceal|sneak|smuggle|cover up|mask)\b|\b(?:hide|hiding|conceal(?:ing)?)\s+(?:it|that|this|my|being|the\s+(?:smell|fact|signs|use|high))\b|\b(?:hide|hiding|conceal(?:ing)?)\b[^?.!]{0,40}\bfrom\s+(?:my|the|your|his|her|their|a|parents|mom|mum|dad|wife|husband|boss|cops|police|teachers?|doctors?)\b|\b(?:sneak|sneaking|smuggle|smuggling)\b|\bwithout\b.{0,40}\b(?:knowing|finding out|noticing)\b|\b(?:not|avoid|without)\s+(?:get(?:ting)?\s+)?caught\b|\b(?:mask|cover(?:\s+up)?|get rid of)\s+the\s+smell\b|\b(?:look|seem|act|appear)\s+sober\b/i,
  beat: /\b(?:pass|passing|beat|beating|cheat|cheating|fool|trick|get around|get past)\b.{0,30}\b(?:tests?|screens?|screening)\b|\b(?:fake|synthetic|someone else'?s|borrowed)\s+(?:pee|piss|urine)\b|\b(?:flush|get|clear|clean)\b.{0,25}\bout of (?:my|your|the|his|her) (?:system|body|urine|blood|hair|pee)\b|\bdetox (?:drinks?|kits?|pills?|shampoo|products?)\b|\b(?:clean|negative)\s+(?:in time\s+)?for\s+(?:a|my|the)\s+(?:drug\s+)?(?:test|screen)/i
};
function insBlocked(q) {
  if (INS_RE.hide.test(q) || INS_RE.beat.test(q)) return true;
  if (INS_RE.fine.test(q)) return false;                       // getting a test kit, naloxone, help or treatment is not getting drugs
  if (INS_RE.shops.test(q)) return true;
  let named = false;
  for (const m of q.matchAll(INS.nameRe)) {                    // a verb of getting or making, with a drug as what is got or made
    const before = q.slice(0, m.index), after = q.slice(m.index + m[0].length); named = true;
    if (INS_RE.buy.test(before) || (INS_RE.get.test(before) && INS_RE.ask.test(q)) || INS_RE.make.test(before) || (INS_RE.how.test(q) && INS_RE.made.test(after))) return true;
  }
  return named && INS_RE.recipe.test(q);
}
/* (2.11; the senior author, 17 November 2026: "the user can navigate the site perfectly through pharmakon insight … this search
   engine should be the best ever possible it has to be so good that it feels like you dream it".) Every place on the site can
   be asked for. INS_PLACES: a place, the words people use for it (p), and, for some, words that only point towards it (h).
   A question that IS a request for the place ("show me all drugs", "where is the quiz", "how do you check facts", "do you
   track me") gets the place as its answer (insRoutes). A question with no checked answer that points towards a place ("how
   many people use cocaine") gets the place as a way on, under the line that says we have not checked it (insRank). The parts
   of a drug's page work the same way (INS_PARTS), and a word of the glossary asked for by its meaning gets its meaning. */
const INS_NAV_PRE = "^(?:(?:please |pls |can you |could you |i want to |i'd like to |let me )?(?:go to|open|show(?: me)?|take me to|bring me to|where(?:'s| is| are| can i (?:find|see|read))|find|see|read|view|give me|can i see|do you have|is there|i want|what(?:'s| is| are))\\s+)?(?:(?:the|your|a|an|all|all the|some|any|this|that)\\s+)*(?:";
const INS_NAV_POST = ")(?:\\s+(?:page|section|tool|part|list|here|please|pls|(?:on|of|for) (?:this|the) (?:site|website)))*\\s*[?.!]*$";
const INS_PLACES = [
  { href: "#substances", icon: "molecule", k: "All drugs", t: "Every drug on this site, by family",
    p: "all drugs|all the drugs|every drug|list of (?:all )?(?:the )?drugs|drugs? list|drug index|drugs a-z|(?:which|what) drugs (?:do you (?:have|cover)|are (?:here|covered|on (?:this|the) (?:site|website)))" },
  { href: "#interactions", icon: "mix", k: "Mixing", t: "Is it safe to mix? Choose two drugs and see what is known",
    p: "mixing|mixing drugs|mixing (?:tool|checker)|drug (?:combinations?|interactions?)|(?:combination|interaction)s? (?:tool|checker|chart|table)|combo chart|is it safe to mix(?: drugs)?|what (?:can|can't|cannot|shouldn't) (?:i|you|be) mix(?:ed)?", h: "mix|mixing|mixed|combine|combining|combination" },
  { href: "#numbers", icon: "pulse", k: "Statistics", t: "Official figures: how many people use each drug, deaths, treatment",
    p: "statistics|stats|official figures|figures|drug statistics", h: "how many people|how common|prevalence|statistics|per year|percentage of people|percent of people" },
  { href: "#facts", icon: "bulb", k: "Big questions", t: "Big questions about drugs, not about one drug", p: "big questions(?: about drugs)?|general questions|questions about drugs in general" },
  { href: "#quiz", icon: "bulb", k: "Myth or fact?", t: "Guess first, then see what studies found: every card, by drug", p: "quiz|myth or fact|myths(?: and facts)?|test my knowledge|trivia|game" },
  { href: "#glossary", icon: "book", k: "Words explained", t: "What the words on this site mean", p: "glossary|dictionary|words explained|terms explained|list of terms" },
  { href: "#methods", icon: "search", k: "How we check facts", t: "How every answer is checked, and what the bars mean",
    p: "how (?:do|did) you (?:check|verify|know|grade|rate)(?: (?:the |your )?(?:facts?|answers?|evidence|this|that|things))?|how we check facts|methods?|methodology|what (?:do|does) the (?:bars?|dots?|certainty bars?) mean|how (?:is|are) (?:the |your )?(?:evidence|answers|facts|certainty) (?:checked|graded|rated|verified)|can i trust (?:this|you|this site|pharmakon)|is (?:this|this site|pharmakon) (?:reliable|trustworthy|legit|accurate|biased)|where (?:do|does) (?:your|the|this) (?:information|info|facts|answers|data) come from|sources" },
  { href: "#howto", icon: "book", k: "How to read this site", t: "What each part of a page is for", p: "how (?:do i|to) (?:use|read|navigate) (?:this|the) (?:site|website|page)|how does this (?:site|website) work|how to read this site|site guide|user guide" },
  { href: "#about", icon: "people", k: "About us", t: "Who writes Pharmakon, and who pays for it",
    p: "about|about (?:us|you|this site|pharmakon)|who (?:made|makes|wrote|writes|runs|owns|funds|pays for|is behind) (?:this|this site|this website|pharmakon|the site)|who are the (?:authors|editors)|contact|contact (?:us|you)|funding|conflicts? of interest|authors|editors" },
  { href: "#about/part-a-privacy", icon: "people", k: "Privacy", t: "What this site keeps, what it sends and what it counts",
    p: "privacy|privacy policy|cookies|my data|do you (?:track|record|log|store|keep|save)(?: me| my (?:data|questions|searches))?|what do you (?:keep|store|know|save)(?: about me)?|is (?:this|it) (?:anonymous|private)|are my (?:questions|searches) (?:private|anonymous|saved|stored)" },
  { href: "#wanted", icon: "message", k: "On our list", t: "Questions the site does not answer yet, and how many people wait for each",
    p: "on (?:our|your) list|not answered yet|unanswered questions|questions? (?:without|with no) (?:an )?answers?|what (?:are )?people (?:waiting|asking) for" },
  { href: "#auto", icon: "book", k: "Written by our system", t: "Answers our system wrote by itself, not yet checked by a person",
    p: "written by (?:your|the|our) system|machine[- ]written(?: answers)?|ai[- ]written(?: answers)?|system(?:'s)? answers|answers (?:by|from) (?:the |your |an )?(?:ai|machine|system)" },
  { href: "#home", el: "home-asked", icon: "message", k: "Your questions", t: "The questions you asked us, kept on this device", p: "my questions|your questions|questions i (?:asked|sent)|what (?:did|have) i (?:ask|asked|sent)" },
  { href: "#about", fb: "issue", icon: "message", k: "Report a mistake", t: "Tell us what is wrong: opens the form",
    p: "report (?:a |an )?(?:mistake|error|problem|bug)|i found (?:a |an )?(?:mistake|error|problem|bug)|something is wrong|this is wrong|feedback|send feedback|suggestion|suggest something|share an idea" }
].map(x => Object.assign(x, { nav: new RegExp(INS_NAV_PRE + x.p + INS_NAV_POST, "i"), hint: x.h ? new RegExp("\\b(?:" + x.h + ")\\b", "i") : null }));
// the parts of a drug's page: [the words that ask for it, the part, its name]. A question that is nothing but such words and
// the drug's name ("cocaine risks", "what does lsd look like", "is ketamine legal") gets the part as a way straight to it,
// above whatever else is found; any other question that holds such a word gets it only when no checked answer was found.
const INS_PARTS = [
  ["looks? like|looks?|pictures?|photos?|images?|appearance|recogni[sz]e|forms?", "d-looks", "What does it look like?"],
  ["myth or fact|quiz|myths?|facts?", "d-quiz", "Myth or fact?"],
  ["risks?|risky|dangers?|dangerous|go wrong|side effects?|harms?|harmful|bad|safe|unsafe", "d-risk", "What can go wrong?"],
  ["feels? like|feels?|feeling|effects?|high", "d-feel", "What does it feel like?"],
  ["comedowns?|hangovers?|day after|next day|after ?effects?|stopping|withdrawals?|quitting|coming off", "d-after", "The day after, and after stopping"],
  ["medicines?|medical|medically|medicinal|therapy|treatment|prescribed|therapeutic", "d-med", "As a medicine, and treatment"],
  ["mix|mixing|mixed|combinations?|combining|other drugs|interactions?", "d-mix", "Is it safe to mix?"],
  ["law|laws|legal|illegal|legality|legal status", "d-law", "Is it legal where you are?"]
].map(([w, id, name]) => ({ id, name, any: new RegExp("\\b(?:" + w + ")\\b", "i"), only: new RegExp("^(?:\\s*(?:" + w + "))+\\s*$", "i") }));
const INS_PART_FILL = /\b(?:what|whats|what's|does|do|is|are|the|of|a|an|it|its|how|can|could|with|on|for|about|me|tell|show|to|please|i|you|will|would|there|any|some|and|get|have|has|use|uses|used|using|go|page|section|part|open|see|read)\b/gi;
// does this drug's page have this part? (a part exists only where there is something to show in it)
function insPartHas(slug, id) {
  const zone = z => drugQuestions(slug).some(([, , t]) => topicZone(t) === z);
  return id === "d-looks" ? (FORMS[slug] || []).some(x => x.name) : id === "d-quiz" ? mfCount(mfPagePool(slug)) >= 3 : id === "d-risk" ? zone("risk") : id === "d-feel" ? zone("feel") : id === "d-after" ? zone("after")
    : id === "d-med" ? zone("med") : id === "d-mix" ? mixQuestions(slug).length > 0 : id === "d-law" ? LEGAL.some(d => d.substance === slug)
    : id === "d-kits" ? !NO_TEST.includes(slug) : id === "d-doses" ? !!dosesBody(slug) : false;
}
/* (2.13, 17 November 2026) A place of the site by the MEANING of a question. The senior author asked "how can i use test kits at
   home" and was told "We haven't checked exactly this yet", although the site has a part on test kits to use at home: "i should
   be answered and be given links etc and i think we already have info about that on the website. man we have to incorporate
   every instance of human language it is still stupid". A place was found only by patterns of words (INS_PLACES, INS_RE): a
   wording nobody had foreseen found nothing. Now every place has the ways people ask for what it holds (site/insight/places.json),
   the build turns them into the model's numbers, and here the question (its drug names read as "it") is compared with every way:
   the place of the nearest one is taken when it is near enough. An entry that is not a place ("does it show up on a drug test" is
   not drug checking) leads nowhere when its way is the nearest. With one drug named, the same part of that drug's page.
   Returns the route and how near it is (s), or null. Measured: scripts/insight/build_index.py --places. */
const INS_PART_T = { "d-kits": s => "Test kits for " + pageWord(s) + ": what home tests can and can’t tell you", "d-doses": () => "We don’t list doses. These harm reduction groups do",
  "d-law": s => "Is " + pageWord(s) + " legal where you are?", "d-looks": s => "What " + pageWord(s) + " looks like: every form", "d-mix": s => "Is it safe to mix " + pageWord(s) + " with other drugs?" };
function insWhere(mv, groups) {
  const X = INS.places; if (!X || !mv) return null;
  const dim = INS.dim, n = X.ids.length, best = new Float32Array(n).fill(-1);
  for (let k = 0, o = 0; k < X.rows.length; k++, o += dim) { let s = 0; for (let j = 0; j < dim; j++) s += mv[j] * X.W[o + j]; if (s > best[X.rows[k]]) best[X.rows[k]] = s; }
  let i = 0; for (let j = 1; j < n; j++) if (best[j] > best[i]) i = j;
  const m = X.meta[i], s = best[i]; if (m.none || s < X.near) return null;
  const one = groups.length === 1 && groups[0].length === 1 && subBySlug[groups[0][0]] ? groups[0][0] : null;
  if (m.part && one && INS_PART_T[m.part] && insPartHas(one, m.part)) return { kind: "part", icon: SEC_ICON[m.part] || m.icon, k: drugName(one), t: INS_PART_T[m.part](one), href: "#s-" + one + "/part-" + m.part, where: X.ids[i], s: +s.toFixed(4) };
  return { kind: "go", icon: m.icon, k: m.k, t: m.t, href: m.href, where: X.ids[i], s: +s.toFixed(4) };
}
// the word of the glossary a question asks the meaning of ("what does tolerance mean", "define half-life", "bioavailability meaning"), or null
function insTerm(q) {
  const flat = s => norm(s).replace(/[^a-z0-9' ]+/g, " ").replace(/\s+/g, " ").trim();
  if (!insTerm.t) { insTerm.t = [];
    GLOSSARY.forEach((g, i) => String(g.term).replace(/\(([^)]*)\)/g, ",$1").split(/,|\/|:|\band\b|\bversus\b/).forEach(n => { const k = flat(n); if (k.length >= 3 && k.split(" ").length <= 4) insTerm.t.push([k, i]); })); }
  const t = flat(q), m = t.match(/^(?:what(?:'s| is| are| does| do)|define|definition of|meaning of|explain|what is meant by)\s+(?:an? |the )?(.+?)(?:\s+(?:mean|means|stand for|stands for))?$/) || t.match(/^(.+?)\s+(?:meaning|definition|means|defined)$/);
  if (!m || INS.any.get(m[1])) return null;
  const x = m[1].replace(/s$/, ""), hit = insTerm.t.find(([k]) => k === m[1] || k === x || k.replace(/s$/, "") === x);
  return hit ? { i: hit[1], g: GLOSSARY[hit[1]] } : null;
}
// a place the question asks for by name (plain: the place is the answer), and, in insRank, a place it points towards
function insPlace(q, about, pointing) {
  if (about && insWordsIn(q) <= 8) {
    // what is left of the question without the drug's name and the small words: nothing but a part's words, or not
    const rest = insMask(q).toLowerCase().replace(/[^a-z' ]+/g, " ").replace(INS_PART_FILL, " ").replace(/\s+/g, " ").trim();
    const part = INS_PARTS.find(x => insPartHas(about, x.id) && (pointing ? x.any.test(q) : rest && x.only.test(rest)));
    // (the part with the pictures is the answer to "what does it look like". Any other part asked for by name is a way straight to
    // it: what else is found still shows, and the line "we haven't checked exactly this" is left out, the part being what we have)
    if (part) return Object.assign({ kind: "part", icon: SEC_ICON[part.id] || "molecule", k: drugName(about), t: part.name.replace(/\bit\b/, pageWord(about)), href: "#s-" + about + "/part-" + part.id },
      pointing ? { loose: true, way: true } : part.id !== "d-looks" ? { loose: true, named: true } : {}); }
  if (about && !pointing) return null;
  const pl = INS_PLACES.find(x => pointing ? x.hint && x.hint.test(q) : x.nav.test(q));
  return pl ? Object.assign({ kind: "go", icon: pl.icon, k: pl.k, t: pl.t, href: pl.href }, pl.el ? { el: pl.el } : {}, pl.fb ? { fb: pl.fb } : {}, pointing ? { loose: true, way: true } : {}) : null;
}
const insCap = t => t.charAt(0).toUpperCase() + t.slice(1);
/* (2.9.2) The country a question names: the UN's names, the names the site shows, their other names and a few everyday
   ones, read with the drugs' names taken out ("china white" is not China). "here", "where i am", "my country": the country
   the reader chose, if any. Returns the UN's name, or "". */
const INS_CTRY_MORE = { "United States of America": ["usa", "u.s.a.", "u.s.", "america", "the states", "the us"], "United Kingdom of Great Britain and Northern Ireland": ["uk", "u.k.", "britain", "great britain", "england", "scotland", "wales", "northern ireland"],
  "Netherlands (Kingdom of the)": ["holland"], "United Arab Emirates": ["uae", "dubai"], "Republic of Korea": ["korea"] };
function insCountry(q) {
  const flat = s => norm(s).replace(/[^a-z0-9' ]+/g, " ").replace(/\s+/g, " ").trim();
  if (!insCountry.t) { insCountry.t = [];
    WORLD_LAW.countries.forEach(c => { if (c.name === "European Union") return;
      [c.name, ctryName(c.name), shortCtry(c.name)].concat(CTRY_ALT[c.name] || [], INS_CTRY_MORE[c.name] || []).forEach(n => { const k = flat(n); if (k.length >= 2) insCountry.t.push([k, c.name]); }); });
    insCountry.t.sort((a, b) => b[0].length - a[0].length); }
  const t = " " + flat(insMask(q)).replace(/\bcold turkey\b/g, " ") + " ", hit = insCountry.t.find(([n]) => t.includes(" " + n + " "));
  if (hit) return hit[1];
  return PREF_COUNTRY && /\b(?:here|where i (?:am|live)|(?:in )?my country)\b/.test(t) ? PREF_COUNTRY : "";
}
// what the treaties page says of a country, in a line
function insLawLine(un) {
  const c = WORLD_LAW.countries.find(x => x.name === un), n = c ? ["c1961", "c1971", "c1988"].filter(k => c[k] && c[k].status === "party").length : 0, nm = insCap(inCtry(un));
  return (n === 3 ? nm + " has joined all three UN drug treaties" : n ? nm + " has joined " + n + " of the three UN drug treaties" : nm + " has not joined the UN drug treaties") + ". Its own law on each drug is on that drug’s page";
}
/* (2.14, 17 November 2026) A question that asks for a count ("how many people die from heroin", "how many people use cocaine",
   "how common is ketamine") is answered from the official figures the site holds (the statistics page: every figure checked at
   its source). The senior author asked the first, was told "We haven't checked exactly this yet" with nine rows about other
   things, opened the statistics page it pointed to and found "all statistics were irrelevant": "this is such a simple question".
   The site had the figure (heroin was involved in an estimated 1,600 deaths in the EU in 2024); nothing led to it.
   insCountKind: what kind of count a question asks for (the statistics page's own kinds: death, use, disorder, treat, harm), or "".
   insFigures: the figures of that kind for the drug named, the ones about that very drug before the ones about its family
   ("opioids"), the reader's own place first, the newest first; with no drug named, the figures about all drugs. */
const INS_COUNT = [
  ["death", /\b(?:how many|how much|number of|numbers? (?:on|of|for)|count of|statistics (?:on|of|for)|figures (?:on|of|for))\b[^?]*\b(?:die|dies|died|dying|deaths?|killed|kills|fatal|fatalities|overdoses?|od)\b|\b(?:deaths?|death toll|death rate|mortality|fatalities|overdose deaths?)\b[^?]*\b(?:per year|a year|each year|every year|yearly|annually|statistics|stats|numbers?|figures?|rate|toll|how many)\b|\bhow many (?:people )?(?:does|do|did|has|have) [^?]{1,40}\b(?:kill|killed)\b|\b(?:death|mortality) (?:statistics|stats|numbers|figures|rate|toll)\b/i],
  ["treat", /\bhow many\b[^?]*\b(?:in treatment|treated|in rehab|enter(?:ing)? treatment|get(?:ting)? treatment|seek(?:ing)? (?:help|treatment))\b/i],
  ["disorder", /\bhow (?:many|common)\b[^?]*\b(?:addicted|dependent|hooked|addicts|use disorder|dependence|addiction)\b/i],
  ["harm", /\bhow many\b[^?]*\b(?:hospital|hospitalised|hospitalized|emergency room|emergency department|a&e|\ber\b)/i],
  ["use", /\bhow (?:many|common|widespread|popular|prevalent)\b[^?]*\b(?:use|uses|used|using|users?|take|takes|taking|took|tried|try|smoke|smokes|smoking|drink|drinks|drinking|inject|injects|do|does|on)\b|\bhow (?:common|widespread|popular|prevalent) (?:is|are)\b|\bwhat (?:percentage|percent|share|proportion|fraction) of\b|\b(?:prevalence|usage statistics|use statistics|how many users)\b|\bhow many (?:people|adults|teens|teenagers|students|young people|americans|europeans|greeks)\b[^?]*\b(?:it|them)\b/i]
];
const INS_COUNT_NOT = /\bhow (?:many|much)\s+(?:mg|mcg|ug|milligrams?|micrograms?|grams?|g|ml|pills?|tablets?|tabs?|capsules?|lines?|drinks?|hits?|puffs?|doses?|drops?|times|hours?|days?|weeks?)\b|\bhow (?:much|long)\b(?![^?]*\b(?:people|deaths?)\b)/i;   // an amount or a time, not a count of people
// a few words that ask for a count without saying "how many" ("heroin deaths", "cocaine statistics", "deaths from alcohol"): only where a
// drug is named, or drugs or overdoses in general, and the words are not a question of another kind ("what is ego death")
const INS_COUNT_SHORT = [["death", /^\s*(?:[\w'-]+\s+){1,3}(?:deaths?|death toll|death rate|mortality|fatalities|overdose deaths?)(?:\s+(?:in|for|across|around)\s+(?:the\s+)?[a-z][a-z'. -]{1,38})?\s*\??$|^\s*(?:deaths?|overdose deaths?|mortality|fatalities)\s+(?:from|by|of|due to|caused by)\s+\S/i],
  ["use", /^\s*(?:[\w'-]+\s+){1,3}(?:statistics|stats|prevalence|usage|use statistics)(?:\s+(?:in|for|across|around)\s+(?:the\s+)?[a-z][a-z'. -]{1,38})?\s*\??$/i]];
function insCountKind(q) {
  const t = String(q); for (const [kind, re] of INS_COUNT) if (re.test(t)) return kind;
  if (!INS.nameRe || /^\s*(?:what|why|who|when|where|which|is|are|was|were|does|do|did|can|could|should|will|would|how|my|i)\b/i.test(t)) return "";
  if (!(insNamed(insSpell(t).text).length === 1 || /\b(?:drugs?|overdoses?)\b/i.test(t))) return "";
  for (const [kind, re] of INS_COUNT_SHORT) if (re.test(t)) return kind;
  return "";
}
/* (2.16.1; the senior author, 17 November 2026, 23:38, asked "how many heroin deaths in america" and was shown, as the answer, the figure for
   the European Union: "the ai should understand what i mean!") A counting question that names a place is about that place. insFigPlace reads
   the place (the world, Europe, a country by any of its names, "here" for the reader's own country); insFigures then marks the figures that
   are from it (here). With none from it, the question is NOT answered: the page says that it has no figure for that place yet, and what it
   has from elsewhere stands below as that, never as the answer (insRank: figMiss). */
function insFigPlace(q) {
  const t = " " + norm(insMask(q)).replace(/[^a-z0-9' ]+/g, " ").replace(/\s+/g, " ").trim() + " ";
  if (/ (?:worldwide|world wide|globally|global|in the world|around the world|all over the world|across the world|on earth|internationally) /.test(t)) return { file: "global", name: "the world" };
  if (/ (?:europe|european|europeans|the eu|eu|european union) /.test(t)) return { file: "europe", name: "Europe" };
  // ("us" alone is also a pronoun: it is the country where it stands after "in", before "citizens", or first or last in a few words that ask for a count: "us heroin deaths")
  const un = / (?:americans?|in (?:the )?us|us (?:citizens|adults|population)) |^ us [a-z]| [a-z]+ us $/.test(t) && !/ (?:of|for|to|with|about|tell|give|show|help|let) us $/.test(t) ? "United States of America" : / greeks? /.test(t) ? "Greece" : insCountry(q);
  if (!un) return null;
  if (un === "United States of America") return { file: "us", name: "the United States" };
  if (un === "Greece") return { file: "greece", name: "Greece" };
  return { country: shortCtry(un), name: inCtry(un) };
}
function insFigures(kind, groups, wantEver, place) {
  if (typeof EPI_ALL === "undefined" || !EPI_ALL.length) return [];
  const inPlace = r => !place ? false : place.country ? new RegExp("(?:^|[^A-Za-z])" + place.country.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?:$|[^A-Za-z])").test(String(r.geography)) : r.file === place.file;
  const one = groups.length === 1 && groups[0].length === 1 ? groups[0][0] : null, any = !groups.length;
  const rows = [];
  EPI_ALL.forEach(r => { if (r.status !== "verified" || figKind(r) !== kind) return;
    if (kind === "death" && r.measure !== "deaths") return;                         // a count of deaths, not years of life lost
    let fit = 0;
    if (any) fit = /^any (?:drug|illicit drug)$/.test(r.substance) ? 2 : 0;
    // the figure's own drug, read as a whole name (its note in brackets left out): 2 that very drug; 1 the family it belongs to ("opioids"
    // for heroin), shown under the family's own name. A figure about another drug of the family, or about a group nobody names so, is not taken.
    else if (one) { const g = INS.nameOf.get(String(r.substance).toLowerCase().replace(/\s*\([^)]*\)/g, "").trim()); fit = !g ? 0 : g.length === 1 && g[0] === one ? 2 : g.length > 1 && g.includes(one) ? 1 : 0; }
    if (fit) rows.push({ r, fit, here: inPlace(r) }); });
  const yr = r => parseInt(String(r.data_year).match(/\d{4}/) || "0", 10), count = r => (/^(?:persons|deaths|million|thousand)/.test(String(r.unit)) ? 0 : 1);
  const ever = wantEver ? r => (r.measure === "lifetime-prevalence" ? 0 : 1) : r => (r.measure === "past-year-prevalence" ? 0 : 1);
  const sample = r => (/web survey|non-representative|not a random sample/i.test(String(r.population) + " " + String(r.geography)) ? 1 : 0);   // a survey of whoever answered comes after a count of everyone
  const wide = r => (/^(?:European Union|EU\b|Europe\b|global|United States|Greece)|\b(?:Member States|countries)\b/.test(String(r.geography)) ? 0 : 1);   // a region's figure before one small country's
  rows.sort((a, b) => (b.here ? 1 : 0) - (a.here ? 1 : 0) || b.fit - a.fit || figRank(a.r.file) - figRank(b.r.file) || (kind === "use" ? ever(a.r) - ever(b.r) : 0) || sample(a.r) - sample(b.r) || wide(a.r) - wide(b.r) || count(a.r) - count(b.r) || yr(b.r) - yr(a.r));
  // the lowest and the highest of a range of national estimates are one figure, said in one line
  rows.forEach(x => { const m = String(x.r.label || x.r.def || "").match(/^(lowest|highest) (.+)$/i); if (!m) return;
    const other = rows.find(y => y !== x && y.r.file === x.r.file && new RegExp("^(?:lowest|highest) " + m[2].replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$", "i").test(String(y.r.label || y.r.def || "")));
    if (other && !other.pair && !x.pair) { const lo = /^lowest/i.test(m[1]) ? x : other, hi = lo === x ? other : x; lo.pair = hi.r; hi.skip = true; } });
  const kept = rows.filter(x => !x.skip);
  // one figure from a place: the best of each, the reader's own place first (a named country's own figure is a place of its own)
  const seen = new Set(), at = x => x.r.file + (x.here && place && place.country ? "|" + place.country : ""); return kept.filter(x => !seen.has(at(x)) && seen.add(at(x)));
}
// a figure in one line: the number in everyday words, what it counts, and where and when; its source
function insFigLine(r, hi) {
  const f = figParts(r), v = figVal(r); let unit = v.u; if (unit === "people" && r.measure === "deaths") unit = "deaths";
  if (hi) { v.v = v.v + " to " + figVal(hi).v; f.what = "Lowest and highest " + f.what.replace(/^lowest /i, ""); f.place = f.place + " (lowest), " + figParts(hi).place + " (highest)"; }
  const cont = /^[a-z]/.test(f.what); if ((unit === "people" || unit === "deaths") && (cont || /death|people|persons/i.test(f.what))) unit = "";
  const what = cont || /^[A-Z]{2}|^[A-Z][a-z]*[A-Z0-9]/.test(f.what) ? f.what : f.what.charAt(0).toLowerCase() + f.what.slice(1);
  return { t: v.v + (unit ? " " + unit : "") + (cont ? " " : ": ") + what + (f.period ? " (" + f.period + ")" : ""), m: f.place + " · " + figYear(r) + " · " + figSrc(r) };
}
const INS_FIG_KIND = { death: "Deaths", use: "How many people use it", disorder: "Use disorder", treat: "Treatment", harm: "Hospital emergencies" };
/* (2.12) A page our system started, for a question that names what it is about ("can i get high with kanna", "what is mitragyna
   javanica"): the page is a place to look. It does not answer the question, so the row does not count as an answer. Asked
   what it looks like, a page with pictures is the answer. The names are the page's own, the filing's, the ones the system
   learned and the species' (AUTO_NAMES, from the build), read with the phrases taken out in which a drug's name is not a drug. */
const INS_LOOKS = /\b(?:looks? like|pictures?|photos?|images?|appearance)\b/i;
function insStartedFlat(s) { return norm(s).replace(/[^a-z0-9' ]+/g, " ").replace(/\s+/g, " ").trim(); }
function insStartedNames() {
  if (!insStartedNames.t) insStartedNames.t = typeof AUTO_NAMES === "object" && AUTO_NAMES && typeof AUTO_PAGES === "object" && AUTO_PAGES
    ? Object.keys(AUTO_NAMES).map(n => [insStartedFlat(n), AUTO_NAMES[n]]).filter(x => x[0].length >= 3 && AUTO_PAGES[x[1]]).sort((a, b) => b[0].length - a[0].length) : [];
  return insStartedNames.t;
}
function insStarted(q) {
  const t = " " + insStartedFlat(INS.scope ? String(q).replace(INS.scope.not, " ") : q) + " ";
  const hit = insStartedNames().find(([n]) => t.includes(" " + n + " ") || t.includes(" " + n + "s ") || (n.length >= 5 && n.endsWith("s") && t.includes(" " + n.slice(0, -1) + " ")));
  if (!hit) return null;
  const k = hit[1], name = AUTO_PAGES[k], sh = autoShell(k), pics = autoPics(k), n = autoFor("new:" + k).length, kind = sh && sh.science.length ? sh.science[0].kind : "";
  const base = { kind: "page", icon: kind === "fungus" ? "mushroom" : kind === "plant" ? "leaf" : "book", k: "A page our system started", href: "#auto/p-" + k, started: k };
  if (pics.length && INS_LOOKS.test(q)) return Object.assign(base, { href: base.href + (pics.length > 1 || n || (sh && sh.asked.length) ? "/part-p-looks" : ""),
    t: insCap(autoLow(k)) + ": " + pics.length + (pics.length === 1 ? " picture" : " pictures") + " our system found, not yet checked by a person" });
  const has = [pics.length ? "pictures" : "", n ? n + (n === 1 ? " answer" : " answers") + " by our system" : "", sh && sh.asked.length ? "what people ask" : ""].filter(Boolean);
  return Object.assign(base, { t: name + (has.length ? ": " + andList(has) : ""), loose: true });
}
function insRoutes(q, groups, drug) {
  const out = [], one = groups.filter(g => g.length === 1).map(g => g[0]).filter((s, i, a) => a.indexOf(s) === i && subBySlug[s]);
  const about = one[0] || (drug && subBySlug[drug] ? drug : null);   // the drug a route is for: the one named, else the page's
  const add = (kind, place, k, t, extra) => out.push(Object.assign({ kind, k, t }, place, extra || {}));
  if (INS_RE.self.test(q)) add("help", INS_PLACE.numbers(), "Get help now", "Emergency numbers where you are");
  else if (INS_RE.help.test(q) || (INS_RE.whatdo.test(q) && INS_RE.acute.test(q))) {
    const s = [about].concat(one).find(x => x && helpSigns(x));
    if (s) add("help", INS_PLACE.help(s), drugName(s), "If it gets too much: what helps"); else add("help", INS_PLACE.numbers(), "Get help", "Emergency numbers");
  }
  if (one.length === 2 && !INS_RE.notmix.test(q) && (INS_RE.mixing.test(q) || (INS_RE.loose.test(q) && !INS_RE.versus.test(q))))
    add("mix", INS_PLACE.mix(), "Mixing", insCap(pageWord(one[0])) + " + " + pageWord(one[1]) + ": what’s known about mixing them", { mix: one[0] + "," + one[1] });
  if (INS_RE.dose.test(q)) {
    if (about) add("dose", INS_PLACE.doses(about), drugName(about), "We don’t list doses. These harm reduction groups do");
    else add("dose", INS_PLACE.drugs(), "Doses", "We don’t list doses. Each drug’s page links to harm reduction groups that do");
  }
  const term = insTerm(q), place = term ? null : insPlace(q, about, false);   // (2.11) a place asked for by name is not a request to test a drug ("how do you check facts")
  if (INS_RE.test.test(q) && !(place && place.kind === "go")) {
    if (about && !NO_TEST.includes(about)) add("test", INS_PLACE.test(about), drugName(about), "Test kits for " + pageWord(about));
    else add("test", INS_PLACE.checking(), "Drug checking", "Drug checking and test kits");
  }
  // (2.9.2) the site's other sections, by country: the law, the emergency numbers, drug checking
  const c = insCountry(q);
  if (!INS_RE.lawNot.test(q) && (INS_RE.law.test(q) || (c && INS_RE.lawc.test(q)))) { const loose = INS_RE.lawPlain.test(q) ? null : { loose: true };
    if (about) add("law", { href: "#s-" + about + "/part-d-law" }, "The law · " + drugName(about) + (c ? " · " + shortCtry(c) : ""),
      c ? (legalReady(about) ? lawPlain(about, c) : "What the law of " + inCtry(c) + " says about " + pageWord(about)) : "Is " + pageWord(about) + " legal where you are?", Object.assign(c ? { country: c, slug: about } : {}, loose));
    else if (c) add("law", { href: "#law/c-" + encodeURIComponent(ctryName(c)) }, "The law · " + shortCtry(c), insLawLine(c), loose);
    else add("law", { href: "#law" }, "The law", "Drug treaties, country by country", loose);
  }
  if (INS_RE.nums.test(q) && !out.some(r => r.kind === "help")) { const em = c ? emFor(c) : null;
    add("numbers", { href: em ? "#emergency/c-" + encodeURIComponent(em.country) : "#emergency" }, "Emergency numbers" + (c ? " · " + shortCtry(c) : ""), em ? "In " + inCtry(c) + ", call " + em.numbers[0].n : "Emergency numbers, country by country"); }
  if (c && INS_RE.checkc.test(q)) { const dc = DRUGCHECK.services.filter(s => sameCountry(s.country, c)), i = out.findIndex(r => r.kind === "test");
    const r = Object.assign({ kind: "test", k: "Drug checking · " + shortCtry(c), t: dc.length ? dc.length + " drug checking service" + (dc.length === 1 ? "" : "s") + " in " + inCtry(c) : "Drug checking in " + inCtry(c) + ": what we found" }, { href: "#checking/c-" + encodeURIComponent(dc.length ? dc[0].country : shortCtry(c)) });
    if (i >= 0 && !about) out[i] = r; else out.push(r); }
  // (2.11) a place on the site asked for by name, a part of a drug's page, or the meaning of a word of the glossary
  if (!out.length) {
    if (term) add("term", { href: "#g-" + term.i }, "Words explained", term.g.term + ": " + String(term.g.short || term.g.def).replace(/\.$/, ""), { icon: "book" });
    else if (place) out.push(place); }
  const w = (q.match(INS_RE.what) || [])[1], slug = w && INS.any.get(w.toLowerCase().replace(/[.!?]+$/, "").trim());
  if (slug && subBySlug[slug] && !out.length) add("page", INS_PLACE.page(slug), "Drug · " + subBySlug[slug].cls, subBySlug[slug].name, { whole: true });
  return out;
}

/* ---------- The match (2.3) ---------- */
/* The score. One small function with one clear input: the question's numbers (v: with the drug's own name brought along;
   mv: with the drug names taken out; q: its words) against every answer's rows. Out, for every answer: the first look
   (2.2.0's score: the best wording, the short answer, the words in common) and the topic score (the best wording with the
   drug names taken out). A second scoring step, a trained judge, goes here and nowhere else. */
function insScore(v, mv, q, X) {
  X = X || INS;   // the answers' index, or the list's (2.5)
  const dim = INS.dim, nA = X.ids.length, W = X.W, M = X.M, S = X.S, wt = INS.wt, rows = X.rows;
  const bw = new Float32Array(nA).fill(-1), bw2 = new Float32Array(nA).fill(-1), topic = new Float32Array(nA).fill(-1), sh = new Float32Array(nA), lex = new Float32Array(nA), plain = new Float32Array(nA), qv = new Map();
  for (let k = 0, o = 0; k < rows.length; k++, o += dim) {
    let s = 0, t = 0; for (let j = 0; j < dim; j++) { s += v[j] * W[o + j]; t += mv[j] * M[o + j]; }
    const a = rows[k]; if (s > bw[a]) { bw2[a] = bw[a]; bw[a] = s; } else if (s > bw2[a]) bw2[a] = s;
    if (t > topic[a]) topic[a] = t;
  }
  insTok(q).forEach(w => { if (X.idf.has(w)) qv.set(w, (qv.get(w) || 0) + X.idf.get(w)); });
  const qn = Math.sqrt([...qv.values()].reduce((a, x) => a + x * x, 0)) || 1;
  qv.forEach((x, w) => X.post.get(w).forEach(([i, y]) => { lex[i] += (x / qn) * y; }));
  for (let i = 0, o = 0; i < nA; i++, o += dim) { let s = 0; for (let j = 0; j < dim; j++) s += v[j] * S[o + j]; sh[i] = s; plain[i] = wt.q * bw[i] + wt.short * s + wt.words * lex[i]; }
  return { plain, topic, bw, bw2, sh, lex };
}
/* What is a best match, and what is related (the numbers: data/insight.json, set in site/insight/model.json; build_index.py
   explains each and measures them on the gold set; scripts/insight/parity.js holds this to the build's own copy of the rule).
   The answers in order of first look + weights.topic x topic, those about the drugs the question names weights.same ahead.
   best: the first of them, when it is about every drug named and the judge says so: a small logistic regression
   (scripts/insight/judge2.py, trained on our own wordings and near-miss questions) on six numbers of that answer: its best
   wording, its second-best wording, its short answer, word overlap, topic, and its lead over the next answer about the drugs
   named. Its number must be judge.best or more. There is never a second best match. related: the next ones, up to three,
   with a first look of tiers.related or more and a topic of tiers.near or more, about at least one of the drugs named. */
function insJudge(f) {
  const J = INS.judge; let z = J.b; for (let i = 0; i < J.w.length; i++) z += J.w[i] * (f[i] - J.mu[i]) / J.sd[i];
  return 1 / (1 + Math.exp(-z));
}
function insTiers(sc, groups, X) {
  X = X || INS;
  const T = INS.t, wt = INS.wt, all = [];
  for (let i = 0; i < X.ids.length; i++) {
    const has = g => g.some(s => X.about[i].has(s)), on = groups.every(has), by = sc.plain[i] + wt.topic * sc.topic[i];
    all.push({ i, on, some: !groups.length || groups.some(has), by, key: by + (on ? wt.same : 0), plain: sc.plain[i], topic: sc.topic[i] });
  }
  all.sort((a, b) => b.key - a.key || a.i - b.i);
  const c = all[0]; let next = null; for (const x of all) if (x !== c && x.on && (next === null || x.by > next)) next = x.by;
  c.f = [sc.bw[c.i], Math.max(sc.bw2[c.i], 0), sc.sh[c.i], sc.lex[c.i], c.topic, c.by - (next === null ? 0 : next)]; c.p = insJudge(c.f);
  const best = c.on && c.p >= INS.judge.best ? [c] : [];
  return { first: c, best, related: all.filter(x => !best.includes(x) && x.plain >= T.related && x.topic >= T.near && x.some).slice(0, 3) };
}
/* 2.5 (15 November 2026; the senior author: "make the site understand on its own what the users want added in the website
   in-app and not via email"). When no answer is a best match, a second look, at the list of questions not answered yet
   (data/site/wanted.json): the same ranking and the same judge over the list's own small index. The typed question is
   taken for a listed one when the list's first candidate is about every drug named, the judge's number for it is the
   list's cut or more, and its best wording is near enough in both looks, with the drug's name and with the drug names
   taken out (the list's "near"; scripts/insight/build_index.py, wanted_index, measures all three and says why the judge
   alone is not enough on a small list). Then the page says "Not answered yet. A question like yours is on our list" (a
   neighbouring question can be taken too, so it does not say "yours"), and one more person asking is counted by the
   item's number alone (wantCount, below): the words stay here. */
function insWant(v, mv, q, groups) {
  const X = INS.list; if (!X) return null;
  const c = insTiers(insScore(v, mv, q, X), groups, X).first;
  return c.on && c.p >= X.cut && c.f[0] >= X.near[0] && c.f[4] >= X.near[1] ? { id: X.ids[c.i], q: X.q[c.i], p: +c.p.toFixed(5) } : null;
}
/* 2.5 (the senior author, of "can i die from mosquito bites" being offered "Ask us to check it": "pharmakon insight should
   understand trolling ... this is a drug website there should be no mistakes"). Is this a question about drugs? By its
   words alone, no model: with the phrases that are not drug talk taken out (stomach acid, diet coke), it names a drug the
   site covers, or holds a drug word, the name of a drug the site does not cover, or a research chemical's name by its
   shape (site/insight/scope.json). It decides only which line a question without an answer gets. */
function insScope(q) {
  if (!INS.scope) return true;
  const t = String(q).replace(INS.scope.not, " ");
  return insNamed(t).length > 0 || INS.scope.re.test(t);
}
/* 2.9 (the senior author typed "can i die from " and was told "We have no answer to this. Pharmakon answers questions about
   drugs": "it should understand and correctly diagnose every instance and meaning of human language"). Is the question
   finished? By its words alone, with each drug's name read as "it"; site/insight/scope.json ("unfinished") explains the
   rule and holds its lists, and the build reads them the same way (Ranker.unfinished in build_index.py, which measures the
   rule on real questions: --words). "" when it is finished; else why it is not: "ends" (its last word cannot end a
   question: "can i die from"), "bare" (a drug is named, or it is asked on a drug's page, and only function words are said
   of it: "is cocaine"), "which" (no drug is named and every word could be asked of any drug: "is it addictive"), "typing"
   (its last word is the beginning of a word: "can i die from coc"). A question that is not finished gets no verdict and no
   way to send it: the page asks which drug is meant, or to go on, and shows the nearest answers. */
function insUnfinRule(U, names) {
  const R = {}, sets = ["ends", "aux", "func", "topic", "nouns", "gap", "join", "who", "whoadj", "help", "do", "det", "be", "open", "verbs", "wants", "pp", "abbr"];
  sets.forEach(k => { R[k] = new Set(U[k] || []); });
  ["strand", "whole", "named"].forEach(k => { R[k] = (U[k] || []).map(p => new RegExp(p)); });
  // the words that could be asked of any drug ("verbs", "open", "wants", "pp" only say how a word is read); the short forms people type are words too
  R.short = new Map(Object.entries(U.short || {}));
  R.known = new Set(); ["ends", "aux", "func", "topic", "nouns", "gap", "join", "who", "whoadj", "help", "det", "be", "abbr"].forEach(k => R[k].forEach(x => R.known.add(x))); R.short.forEach((v, k) => R.known.add(k));
  // every beginning of a word: of a word of the lists (two letters or more), of a word of a drug's name (three or more);
  // a word without its plural s is a word, not a beginning
  const begin = (words, start) => { const out = new Set(); words.forEach(w => { for (let i = start; i < w.length; i++) out.add(w.slice(0, i)); }); words.forEach(w => { if (w.endsWith("s")) out.delete(w.slice(0, -1)); }); return out; };
  const ofNames = new Set(); names.concat(U.names || []).forEach(n => (n.toLowerCase().match(/[a-z0-9]+/g) || []).forEach(x => { if (x.length >= 4) ofNames.add(x); }));
  R.begin = begin(R.known, 2); R.beginName = begin(ofNames, 3);
  return R;
}
/* 2.9.2 (the senior author typed "do gay people" and was told "This does not look like a question about drugs": "we have to
   include our site responding perfectly to every circumstance this is what smartness is about"). Two more ways a question is
   not finished, both in scope.json's note: "open", nothing but function words and words for people ("do gay people", "why do
   women"); "verb", a helper verb and no main verb after it ("does smoking weed", "how long does the high", "can dogs").
   insUnfTokens: the words as the rule reads them: small letters, the short forms people type read as their words ("u",
   "ppl", "gonna"), each drug's name read as "it" (nm: the name it stands for), and a name inside a phrase that is not drug
   talk ("weed my garden") left as a word. */
function insUnfTokens(q) {
  const U = INS.unfin, t = String(q).toLowerCase().replace(/\u2019/g, "'"), blank = INS.scope ? t.replace(INS.scope.not, m => " ".repeat(m.length)) : t;
  const surf = [], w = [], nm = []; let out = "", at = 0, m, k = 0; INS.nameRe.lastIndex = 0;
  while ((m = INS.nameRe.exec(blank))) { out += t.slice(at, m.index) + " 0n0 "; surf.push(t.slice(m.index, m.index + m[0].length)); at = m.index + m[0].length; }
  out += t.slice(at);
  (out.match(/[a-z0-9']+/g) || []).forEach(y => { y = y.replace(/^'+|'+$/g, ""); if (!y) return;
    if (y === "0n0" && k < surf.length) { w.push("it"); nm.push(surf[k++]); return; }
    (U.short.has(y) ? U.short.get(y).split(" ") : [y]).forEach(z => { w.push(z); nm.push(null); }); });
  return { w, nm };
}
// the -ing and -ed forms a verb with this base form would have; may a word be the base form of a verb, by the model's word list alone
function insVerbForms(x) {
  const f = [x + "ing", x + "ed"], n = x.length;
  if (x.endsWith("e")) f.push(x.slice(0, -1) + "ing", x + "d");
  if (x.endsWith("ie")) f.push(x.slice(0, -2) + "ying");
  if (n > 2 && x.endsWith("y") && !"aeiou".includes(x[n - 2])) f.push(x.slice(0, -1) + "ied");
  if (n >= 2 && !"aeiouwxy".includes(x[n - 1]) && "aeiou".includes(x[n - 2])) f.push(x + x[n - 1] + "ing", x + x[n - 1] + "ed");
  if (x.endsWith("c")) f.push(x + "king", x + "ked");
  return f;
}
function insVerbish(x) {
  const V = INS.vocab;
  if (V.has(x)) return insVerbForms(x).some(f => V.has(f));
  if (x.endsWith("ing") || x.endsWith("ed")) return false;
  if (x.endsWith("s") && !x.endsWith("ss") && (V.has(x.slice(0, -1)) || (x.endsWith("es") && V.has(x.slice(0, -2))) || (x.endsWith("ies") && V.has(x.slice(0, -3) + "y")))) return false;
  return true;
}
const INS_SUBJ = new Set(["i", "you", "we", "they", "he", "she", "it"]);   // after one of these stands the verb
function insVerbless(w, nm) {
  const U = INS.unfin; if (w.length > 6) return false;
  const thing = x => !!INS.scope && INS.scope.re.test(x);                                 // a drug word
  const base = j => { const x = w[j], prev = j ? w[j - 1] : "";                           // may word j be the main verb where it stands?
    if (U.det.has(prev)) return false;                                                    // "the high", "a test": a thing
    if (nm[j] !== null) return j > 0 && !U.help.has(prev) && !prev.endsWith("ing") && /^[a-z]+$/.test(nm[j]) && insVerbish(nm[j]);   // a drug's name: only where its own word can be a verb ("can i speed up")
    if (U.verbs.has(x) || U.be.has(x)) return true;
    if (U.aux.has(x) || U.gap.has(x) || U.who.has(x) || U.whoadj.has(x)) return false;
    if (j && (nm[j - 1] !== null || INS_SUBJ.has(prev))) return true;                     // right after a pronoun or a drug's name: the verb's place
    if (thing(x)) return false;
    return insVerbish(x); };
  for (let i = 0; i < w.length; i++) { const x = w[i], prev = i ? w[i - 1] : "";
    if (nm[i] === null && U.help.has(x) && !U.det.has(prev) && prev !== "to") {
      if (U.do.has(x) && w.slice(0, i).some(y => !U.open.has(y))) return false;           // "people do drugs": do can be the main verb
      for (let j = i + 1; j < w.length; j++) if (base(j)) return false;
      return true; }
    // before the helper: question words, function words, people, drugs' names and drug words, a word in -ing ("smoking weed can"); nothing else
    if (nm[i] === null && (U.be.has(x) || x === "to" || !(U.open.has(x) || U.aux.has(x) || U.ends.has(x) || U.gap.has(x) || U.who.has(x) || U.whoadj.has(x) || x.endsWith("ing") || thing(x)))) return false; }
  return false;
}
function insUnfinished(q, onPage) {
  const U = INS.unfin; if (!U) return "";
  const { w, nm } = insUnfTokens(q), names = nm.filter(n => n !== null).length; if (!w.length) return "";
  const s = w.join(" "), any = ps => ps.some(p => p.test(s)), all = (xs, S) => xs.every(x => S.has(x)), last = w[w.length - 1];
  if (any(U.whole)) return "";
  if (U.ends.has(last) && !any(U.strand)) return "ends";
  if (names >= 2 && w.every(x => x === "it" || U.join.has(x))) return "";               // two drugs and a word that joins them
  // nothing but function words and words for people: a subject, and nothing said of it, unless a form of "be" stands before
  // a last word that describes people ("are people gay") or before "for kids" and the like ("is weed for kids")
  const people = w.every(x => U.aux.has(x) || U.who.has(x) || U.whoadj.has(x)), be = w.findIndex(x => U.be.has(x)), gap = w.some(x => U.gap.has(x));
  const said = be >= 0 && U.whoadj.has(last) && be < w.length - 1, saidOf = be >= 0 && w.slice(be + 2, -1).some(x => U.pp.has(x));
  if (names || onPage) {
    if (people && !said && !saidOf) return names && any(U.named) ? "" : "bare";          // "what is ketamine" is finished
    if (!people && insVerbless(w, nm)) return "verb";
  } else if (all(w, U.known)) {
    if (people) return said || (saidOf && !gap) ? "" : "open";
    if (insVerbless(w, nm)) return "verb";                                                // "how long does withdrawal"
    // a word for people that is not an everyday one, and no "it": the question is about people, and finished ("how do i get a girlfriend")
    if (!gap && w.some(x => (U.who.has(x) || U.whoadj.has(x)) && !U.func.has(x) && !U.aux.has(x) && !U.topic.has(x))) return "";
    return !gap && (w.some(x => U.nouns.has(x)) || (w[0] === "why" && w.some(x => U.topic.has(x)))) ? "" : "which";
  } else if (insVerbless(w, nm)) return "verb";                                           // "does the government", "can dogs"
  // the last word is still being typed: not a word, and the beginning of a drug's name, or (in a question that otherwise
  // reads as one about drugs) of a word this rule knows
  if (w.length >= 2 && !U.known.has(last) && !INS.vocab.has(last)) {
    if (U.beginName.has(last)) return "typing";
    if (U.begin.has(last) && (names || onPage || all(w.slice(0, -1), U.known) || insScope(w.slice(0, -1).join(" ")))) return "typing";
  }
  return "";
}
/* 2.9: a word of the question that the model does not know (three letters or more; not in its vocabulary with or without
   an ending; not a word of the lists above), when everything else in the question could be asked of any drug: it may be
   the name of a drug we do not know ("is tusi dangerous"). build_index.py's unknown_words reads the same way. */
const INS_UNK_ENDS = [["s", ""], ["es", ""], ["ies", "y"], ["ed", ""], ["ed", "e"], ["d", ""], ["ing", ""], ["ing", "e"], ["ly", ""], ["er", ""], ["est", ""]];
function insUnknown(q) {
  if (!INS.unfin || !INS.vocab) return [];
  const t = String(q).toLowerCase().replace(/n['\u2019]t\b/g, " not").replace(/['\u2019](?:s|re|ve|ll|d|m)\b/g, " "), out = [];
  new Set(t.match(/[a-z]{3,}/g) || []).forEach(w => {
    if (INS.unfin.known.has(w)) return;
    const forms = [w].concat(INS_UNK_ENDS.filter(([end]) => w.length > end.length + 2 && w.endsWith(end)).map(([end, put]) => w.slice(0, -end.length) + put));
    if (!forms.some(f => INS.vocab.has(f))) out.push(w);
  });
  return out;
}
// (the unknown word or words, three at most, of a question whose other words could be asked of any drug: what the page
// then says of them. 2.9.2, the senior author of "what is mytragina javanica" being told "This does not look like a question
// about drugs": a name of two words that we do not know is a name we do not know)
function insStranger(q) {
  const unk = insUnknown(q); if (!unk.length || unk.length > 3) return "";
  const toks = (String(q).toLowerCase().replace(/\u2019/g, "'").match(/[a-z0-9']+/g) || []).map(x => x.replace(/^'+|'+$/g, "")).filter(Boolean), set = new Set(unk);
  const rest = toks.filter(x => !set.has(x));
  return rest.length && rest.every(x => INS.unfin.known.has(x)) ? toks.filter((x, i) => set.has(x) && toks.indexOf(x) === i).join(" ") : "";
}
// does a question that is not finished and names no drug call for a drug's name ("is it addictive", "can i die from"), or only for its end ("do gay people")?
function insUnfCue(q) {
  const U = INS.unfin, T = insUnfTokens(q), w = T.w, last = w[w.length - 1];
  if (T.nm.some(n => n !== null)) return false;   // (2.12) a drug is named, though the site has no page on it ("is kanna addictive for"): "which drug do you mean?" would be wrong
  return w.some(x => U.gap.has(x) || U.topic.has(x)) || (U.wants.has(last) && w.some(x => U.func.has(x) && !U.who.has(x)));
}
/* 2.9.1: a drug's name with a letter wrong is read as that name before the question is read ("can i die from cocane",
   "is ketamin addictive", "herion"), and the page says what it read. site/insight/scope.json ("spell") explains the rule
   and holds its tables; build_index.py reads the same way (Ranker.correct) and parity.js holds the two to each other. */
function insNear(a, b) {   // one letter apart: a letter put in, left out or changed, or two neighbours swapped
  const la = a.length, lb = b.length; if (a === b || Math.abs(la - lb) > 1) return false;
  let i = 0; while (i < la && i < lb && a[i] === b[i]) i++;
  if (la === lb) return a.slice(i + 1) === b.slice(i + 1) || (i + 1 < la && a[i] === b[i + 1] && a[i + 1] === b[i] && a.slice(i + 2) === b.slice(i + 2));
  return la < lb ? a.slice(i) === b.slice(i + 1) : a.slice(i + 1) === b.slice(i);
}
function insSpellRule(Sp, other) {
  const group = new Map(); INS.nameOf.forEach((g, n) => group.set(n, g.join("|"))); other.forEach(n => { if (!group.has(n)) group.set(n, "other:" + n); });
  const targets = [...group.keys()].filter(n => n.length >= 6 && /^[a-z]+$/.test(n)).sort((a, b) => b.length - a.length || (a < b ? -1 : a > b ? 1 : 0));
  // (2.9.3) what people typed for a name the system learned by looking it up ("mytragina javanica"): read as that name first
  const phr = new Map(Object.entries(Sp.phr || {})), keys = [...phr.keys()].sort((a, b) => b.length - a.length || (a < b ? -1 : a > b ? 1 : 0));
  const phrRe = keys.length ? new RegExp(insNb("A-Za-z0-9'\u2019-") + "(?:" + keys.map(k => k.split(" ").map(insRx).join("\\s+")).join("|") + ")(?![A-Za-z0-9'\u2019-])", "gi") : null;
  return { map: new Map(Object.entries(Sp.map || {})), keep: new Set(Sp.keep || []), group, targets, phr, phrRe };
}
function insSpellWord(w) {
  const R = INS.spell; if (R.map.has(w)) return R.map.get(w);
  if (w.length < 5 || R.group.has(w) || R.keep.has(w) || INS.unfin.known.has(w)) return null;
  const forms = [w].concat(INS_UNK_ENDS.filter(([end]) => w.length > end.length + 2 && w.endsWith(end)).map(([end, put]) => w.slice(0, -end.length) + put));
  if (forms.some(f => INS.vocab.has(f))) return null;                                    // a word
  for (const end of ["s", "es"]) if (w.length > end.length + 2 && w.endsWith(end) && R.group.has(w.slice(0, -end.length))) return w.slice(0, -end.length);   // a name with a plural or possessive s
  if (forms.slice(1).some(f => R.group.has(f)) || (INS.scope && INS.scope.re.test(w))) return null;   // a name with another ending, or drug talk
  const hits = R.targets.filter(n => Math.abs(n.length - w.length) <= 1 && insNear(w, n));
  return hits.length && new Set(hits.map(n => R.group.get(n))).size === 1 ? hits[0] : null;
}
function insSpell(q) {
  const read = []; if (!INS.spell) return { text: q, read };
  if (INS.spell.phrRe) q = String(q).replace(INS.spell.phrRe, m => { const name = INS.spell.phr.get(m.toLowerCase().replace(/\s+/g, " ")); read.push([m, name]); return name; });
  // (a word with nothing of a word before it: the character before is taken with it and put back, so no look-behind is needed)
  const text = String(q).replace(/(^|[^A-Za-z0-9'\u2019-])([A-Za-z]+)(?![A-Za-z0-9'\u2019-])/g, (m, pre, word) => { const n = insSpellWord(word.toLowerCase()); if (!n) return m; read.push([word, n]); return pre + n; });
  return { text, read };
}
const insReadHtml = (res, cls) => res.read && res.read.length ? '<p class="' + cls + '">We read ' + res.read.map(([a, b]) => "\u201c" + esc(a) + "\u201d as <b>" + esc(b) + "</b>").join(" and ") + ".</p>" : "";
// the page an answer is shown as being on: a drug the question names (or the page's own) when the answer is asked there
function insPageOf(id, groups, drug) {
  if (isAuto(id)) return AUTO[id].page;   // (2.6) an answer written by the system lives on its drug's page, or among the big questions
  const want = groups.flat().concat(drug ? [drug] : []).find(s => (QUESTIONS[s] || []).some(g => g.items.some(([x]) => x === id)));
  return answerPageKey(id, want) || claimById[id].substance;
}
/* insRank(question, ctx): everything Insight understands of one question. ctx.drug: the drug whose page the reader is on.
   Out: q (as typed), core (without depth words: what was matched), depth ("", "full" or "short"), routes, best (0 to 2) and
   related (up to 3), each { id, page, plain, topic, off } (off: not about every drug asked about), and what the list and
   the sheet say when there is no best match: note ("none": we haven't checked exactly this yet, with the way to ask us;
   "want": a question like it is on our list (want: { id, q, p }); "other": not a question about drugs by its words, no promise to check it;
   "blocked": the first line without the way to ask; "": nothing, the route says it). insRead is the part that needs no model: the depth
   words, the drugs named, the routes. */
function insRead(query, ctx) {
  const q = insClean(query), sp = insSpell(q), drug = ctx && ctx.drug && subBySlug[ctx.drug] ? ctx.drug : null, d = insDepth(sp.text), named = insNamed(d.core);   // (2.9.1) a misspelt name is read as the name
  const res = { q, core: d.core, depth: d.depth, drug: named.length ? null : drug, groups: named.length ? named : drug ? [[drug]] : [], routes: [], best: [], related: [], note: "", emergency: false, read: sp.read };
  // (2.5: with the phrases in which a drug's name is not a drug taken out first: "how do i cook mushrooms in butter" is not a request to make a drug)
  if (insBlocked(INS.scope ? d.core.replace(INS.scope.not, " ") : d.core)) { res.note = "blocked"; return res; }
  res.routes = insRoutes(d.core, named, drug); res.emergency = res.routes.some(r => r.kind === "help");
  return res;
}
// (2.9.2) a question that is not written in the Latin alphabet (three letters or more, three in ten of its letters)
function insForeign(q) { const L = String(q).match(/\p{L}/gu) || [], o = L.filter(ch => !/\p{Script=Latin}/u.test(ch)).length; return o >= 3 && o / L.length >= 0.3; }
async function insRank(query, ctx) {
  const t0 = performance.now(), res = insRead(query, ctx);
  if (res.note === "blocked") { res.ms = performance.now() - t0; return res; }
  // Pharmakon reads English for now: the page says so, keeps the emergency route and the rows the word search found (it knows
  // the drugs' Greek names), and gives no verdict
  if (insForeign(res.q) && !res.emergency) { res.note = "language"; res.greek = /\p{Script=Greek}/u.test(res.q); res.routes = res.routes.filter(r => r.kind === "help"); res.ms = performance.now() - t0; return res; }
  // (2.14) a question that asks for a count: the official figures are fetched (once) and the ones that answer it are routes of their own
  const ck = insCountKind(res.core);
  if (ck && !res.emergency && res.groups.length <= 1 && !res.routes.some(r => r.kind === "dose") && !INS_COUNT_NOT.test(res.core)) {
    if (!FIGURES_DONE) { try { await Promise.race([loadFigures(), new Promise(ok => setTimeout(ok, 2500))]); } catch (e) { /* the statistics page is still pointed to */ } }
    const place = insFigPlace(res.core), all = insFigures(ck, res.groups, /\b(?:tried|ever|lifetime|in their li(?:fe|ves))\b/i.test(res.core), place), one = res.groups.length === 1 && res.groups[0].length === 1 ? res.groups[0][0] : null;
    // (2.16.1) a place was named: its own figures are the answer; with none, the figures from elsewhere are only a place to look, and the question stays open
    const from = place ? all.filter(x => x.here) : all, miss = !!place && !from.length, figs = miss ? all : from;
    if (miss) res.figMiss = place.name;
    figs.slice(0, 2).forEach(({ r, fit, pair }) => { const l = insFigLine(r, pair);
      res.routes.push(Object.assign({ kind: "figure", icon: "pulse", k: "Statistics · " + (one ? (fit === 2 ? drugName(one) : insCap(String(r.substance))) : "All drugs") + " · " + INS_FIG_KIND[ck], t: l.t, m: l.m,
        href: "#numbers/part-n-" + r.file + "/f-" + ck + "-" + numSlug(one ? r.substance : ""), fig: r.file + "|" + (one ? r.substance : "") + "|" + ck }, miss ? { loose: true, way: true } : {})); });
  }
  const st = insStarted(res.core);                             // (2.12) a page our system started that the question names
  if (st && !st.loose) res.routes.push(st);                    // asked what it looks like: its pictures are the answer
  const whole = res.routes.some(r => r.whole);                 // the question is a drug's name and nothing more: its page is the answer
  // (2.9.2) the law of a named country on a named drug: the drug's law rows are fetched (once), so that the row says what the law says
  const lr = res.routes.find(r => r.kind === "law" && r.country && r.slug);
  if (lr && !legalReady(lr.slug)) { try { await Promise.race([loadFull(lr.slug), new Promise(ok => setTimeout(ok, 2500))]); } catch (e) { /* the row keeps its plain words */ } }
  if (lr && legalReady(lr.slug)) lr.t = lawPlain(lr.slug, lr.country);
  // a route is the answer to what was asked, except the mixing tool and a route that only points the way (loose)
  const answered = res.routes.some(r => r.kind !== "mix" && !r.loose), named = !res.drug && res.groups.length > 0, unf = insUnfinished(res.core, !!res.drug);
  if (!(whole && insWordsIn(res.core) < INS_WORDS)) {
    const drug = ctx && ctx.drug, tx = insTexts(res.core, drug), v = await insEmbed(tx.full), mv = tx.masked === tx.full ? v : await insEmbed(tx.masked);
    const sc = insScore(v, mv, res.core), tiers = insTiers(sc, tx.groups);
    Object.defineProperty(res, "sc", { value: { bw: sc.bw, topic: sc.topic }, enumerable: false });   // (2.13) how near every answer is in meaning: for the word search's rows (insInject)
    const row = c => ({ id: INS.ids[c.i], page: insPageOf(INS.ids[c.i], tx.groups, drug), plain: +c.plain.toFixed(4), topic: +c.topic.toFixed(4), off: !c.on });
    res.best = tiers.best.map(row); res.related = res.emergency ? [] : tiers.related.map(row);   // an emergency gets its route and the answers that fit, nothing nearby
    res.judge = { id: INS.ids[tiers.first.i], p: tiers.first.p, f: tiers.first.f };              // (for the checks: the first candidate and the judge's number for it)
    // (2.15.2; the senior author, 17 November 2026, of his sent "is cocaethylene more dangerous than cocaine or alcohol alone?", hours on his
    // list: "will these be answered? ... this is disappointing". The site had the checked answer on cocaine with alcohol, which names
    // cocaethylene; the judge's number for it was under its cut, so it stood under "Related" and the page offered to send the question.)
    // Two drugs are named and the site has checked answers about mixing exactly those two: they are what we have checked on the question,
    // whatever the judge's number. The nearest in meaning first, two at most.
    // It must be an answer about those two with each other: its own question names both, by two different names ("Cocaine with alcohol"; an
    // answer on "opioids with benzodiazepines" is not an answer on fentanyl with heroin). And the question must be about the two together:
    // the mixing tool's own reading of it (its route), or a word of the question that the model's word list does not hold and that the
    // answer's own plain text uses ("cocaethylene"). "cocaine vs alcohol, which is more addictive" is neither.
    if (!res.best.length && !res.emergency && !unf && tx.groups.length === 2) {
      const [g1, g2] = tx.groups, text = id => { const s = (SIMPLE.claims || {})[id] || {}; return (insQ(id) + " " + (s.short || "") + " " + (s.but || "") + " " + (s.how || []).join(" ")).toLowerCase(); };
      const namesIn = t => { const out = []; INS.nameRe.lastIndex = 0; let m; while ((m = INS.nameRe.exec(t))) out.push(INS.nameOf.get(m[1].toLowerCase()) || []); INS.nameRe.lastIndex = 0; return out; };
      const both = id => { const ns = namesIn(String(insQ(id) || "").toLowerCase()); return ns.some((a, i) => a.some(s => g1.includes(s)) && ns.some((b, j) => j !== i && b.some(s => g2.includes(s)))); };
      const rare = (res.core.toLowerCase().match(/[a-z]{8,}/g) || []).filter(w => !INS.vocab.has(w) && !INS.nameOf.has(w));
      const mixing = res.routes.some(r => r.kind === "mix");
      const pair = INS.ids.map((id, i) => i).filter(i => { const id = INS.ids[i], m = MIXFOR[id] || []; if (!(g1.some(s => m.includes(s)) && g2.some(s => m.includes(s))) || !both(id)) return false; return mixing || rare.some(w => text(id).includes(w)); })
        .sort((a, b) => (sc.topic[b] || 0) - (sc.topic[a] || 0)).slice(0, 2);
      if (pair.length) { res.judged = { best: [], related: res.related.map(x => x.id) };   // (what the judge alone gave, for the check that the page and the build rank alike)
        res.best = pair.map(i => ({ id: INS.ids[i], page: insPageOf(INS.ids[i], tx.groups, drug), plain: +(sc.bw[i] || 0).toFixed(4), topic: +(sc.topic[i] || 0).toFixed(4), off: false, pair: true }));
        const got = new Set(res.best.map(x => x.id)); res.related = res.related.filter(x => !got.has(x.id)); res.pair = true; }
    }
    // 2.9: a question that is not finished and names no drug has no "best match": the answers found are ways to go on
    if (unf && !named && !answered && res.best.length) { res.related = res.best.concat(res.related).slice(0, 3); res.best = []; res.demoted = true; }
    if (!res.best.length && !answered && !unf) res.want = insWant(v, mv, res.core, tx.groups);   // 2.5: is it on our list?
    // (2.13) nothing answers it yet: a place of the site that holds what is asked, found by meaning
    if (!res.best.length && !answered && !unf && !res.want && !res.routes.some(r => r.named)) res.where = insWhere(mv, tx.groups);
  }
  // with no best match, say so, unless a route already is the answer to what was asked (help, a dose, a test, the drug's page).
  // 2.9: "unfinished", the question is not finished yet (unf says why); 2.5: "want", a question like it is on our list;
  // "other", by its words it is not a question about drugs (on a drug's page a question that names no drug is about that
  // drug), with the one word we do not know, if that is what stands in the way (stranger); "none", a drug question we have
  // not checked yet
  if (!res.best.length && !answered) {
    // (2.11) with no checked answer: a place on the site that the question points towards, as a way on ("how many people use cocaine": Statistics)
    if (!unf && !res.routes.length && !res.where) { const drug1 = res.groups.length === 1 && res.groups[0].length === 1 ? res.groups[0][0] : null, way = insPlace(res.core, drug1, true); if (way) res.routes.push(way); }
    res.note = unf ? "unfinished" : res.want ? "want" : res.drug || insScope(res.core) ? "none" : "other";
    // (2.13) the place found by meaning. A question about drugs: the place is the answer when it is very near (the index's 'cut'), else
    // a place to look under the line for a question we have not checked. A question that is not about drugs by its words is a question
    // about the site ("is my search private", "who checks this"): its place is the answer, in place of "not a question about drugs".
    if (res.where && !res.routes.some(r => r.href === res.where.href) && !(res.note === "other" && (INS_RE.greet.test(res.core) || INS_RE.about.test(res.core)))) {
      const sure = !res.figMiss && (res.note === "other" || res.where.s >= INS.places.cut);   // (2.16.1: a count asked for a place we have no figure for is not answered by the statistics page)
      res.routes.push(sure ? res.where : Object.assign(res.where, { loose: true, way: true })); if (sure) res.note = ""; }
    if (unf) { res.unf = unf; if (!res.groups.length) res.cue = insUnfCue(res.core); }
    else if (res.note === "none" && res.routes.some(r => r.named)) res.note = "";   // (2.11) a part of a drug's page asked for by name: the part is what we have
    else if (res.note === "other" && INS_RE.greet.test(res.core)) res.note = "hello";
    else if (res.note === "other" && INS_RE.about.test(res.core)) res.note = "about";
    else if (res.note === "other") res.stranger = insStranger(res.core);
  }
  // (2.12) the page our system started for what the question names: first when nothing else was found, else among the places to look.
  // A question that names it is a question about a drug, whatever its other words.
  if (st && st.loose) { if (res.note === "other") { res.note = "none"; delete res.stranger; }
    // the very question that page lists (the same words): not answered yet, and on our list
    if (res.note === "none") { const sh = autoShell(st.started), flat = insStartedFlat(res.core), hit = sh && sh.asked.find(a => !(a.answer && isAuto(a.answer)) && insStartedFlat(a.q) === flat);
      if (hit) { res.note = "want"; res.want = { id: hit.id, q: hit.q, started: st.started }; } }
    res.routes.push(Object.assign(st, res.best.length || res.routes.length ? { way: true } : {})); }
  res.ms = performance.now() - t0; INS.times.push(res.ms);
  return res;
}
// the same, kept for the questions of this visit (in memory only: nothing typed is stored)
const insKey = (q, ctx) => insClean(q).toLowerCase() + "|" + ((ctx && ctx.drug) || "");
function insAnswer(q, ctx) {
  const key = insKey(q, ctx), have = INS.cache.get(key); if (have) return Promise.resolve(have);
  return insRank(q, ctx).then(res => { INS.cache.set(key, res); if (INS.cache.size > 60) INS.cache.delete(INS.cache.keys().next().value); return res; });
}
// the page the reader is on: a drug's page (or its research page) makes a question about that drug
function insCtx() {
  const v = document.querySelector(".view.active"), id = v ? v.id : "";
  const drug = id === "view-drug" ? renderedDrug : id === "view-monograph" ? currentSlug : null;
  return { drug: drug && subBySlug[drug] ? drug : null };
}
// the box says so: "Ask about cannabis" on the cannabis page, its own words everywhere else
function insPlaceholder() {
  const s = document.getElementById("search"); if (!s) return;
  if (insPlaceholder.own == null) insPlaceholder.own = s.getAttribute("placeholder") || "";
  const home = !!document.querySelector("#view-home.active");
  // (2.15) the same Insight on every page, and named: "Ask Insight about cannabis" on a drug's page, "Ask Insight about drugs" elsewhere
  const d = insCtx().drug, want = d ? "Ask Insight about " + pageWord(d) : home ? insPlaceholder.own : "Ask Insight about drugs";
  if (s.getAttribute("placeholder") !== want) s.setAttribute("placeholder", want);
}

/* ---------- In the search results ---------- */
const insQ = (id, page) => isAuto(id) ? AUTO[id].q : (page && sharedQuestion(page, id)) || anyQuestion(id) || ((SIMPLE.claims || {})[id] || {}).q || claimText(claimById[id]);
const insNoteText = () => "Runs on your " + (window.matchMedia && window.matchMedia("(pointer: coarse)").matches ? "phone" : "computer") +
  (autoSendOn() ? ". A question we have no answer to is sent to our system by itself, so that it gets answered: no name, no address."
    : FIND_ON && autoOn() ? ". With no answer of ours, only the drug’s name and a few key words go out, to look up research." + (ASK_ON ? " Your question is sent only if you send it." : "")
    : ASK_ON ? ". What you type stays on it, unless you ask us to check a question." : ". Nothing you type leaves it.");
const INS_ICON = { help: "heart", mix: "mix", dose: "book", test: "flask", page: "molecule", law: "scale", numbers: "phone" };
// the emergency number where the reader is, or the way to the numbers: shown with an emergency route, and nowhere else
function insSosHtml(cls) {
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  return '<p class="' + cls + '">' + icon("phone") + "<span>" + (em ? "Emergency number in " + esc(inCtry(PREF_COUNTRY)) + ': <a href="tel:' + esc(telOf(em.numbers[0])) + '">' + esc(em.numbers[0].n) + "</a> · " : "") +
    '<a href="#emergency">' + (em ? "Other numbers" : "Emergency numbers by country") + "</a></span></p>";
}
function insRouteHtml(r, cls) {
  return '<a class="' + cls + " r-" + r.kind + '" href="' + esc(r.href) + '" data-ins-route="' + r.kind + '"' + (r.el ? ' data-el="' + esc(r.el) + '"' : "") + (r.mix ? ' data-mix="' + esc(r.mix) + '"' : "") + (r.country ? ' data-country="' + esc(r.country) + '"' : "") + (r.fb ? ' data-fb-open="' + esc(r.fb) + '"' : "") + (r.fig ? ' data-fig="' + esc(r.fig) + '"' : "") + ">" +
    '<span class="ri">' + icon(r.icon || INS_ICON[r.kind] || "arrow") + '</span><span class="k">' + esc(r.k) + '</span><span class="t">' + esc(r.t) + (r.m ? '<span class="rm">' + esc(r.m) + "</span>" : "") + '</span><span class="go">' + icon("arrow") + "</span></a>";
}
// "Ask us to check it": one tap (2.4, below: Your questions); where the page can send it, a quiet line says what is sent
const insAskBtn = (q, cls, label, after) => '<button type="button" class="' + cls + '" data-ask="' + esc(q) + '">' + (label || "Ask us to check it") + "</button>" + (after || "") + (ASK_ON ? '<span class="ask-note">Sends only this question. No name, no address.</span>' : "");
/* 2.5: the line under a question with no best match, in the list (sheet false) and in the sheet. "none": a drug question we
   have not checked: the way to ask us. "want": a question like it is on our list; the reader can ask to be told, on this
   device, when it is answered, or send their own words if the listed question is not the same. "other": by its words not
   a question about drugs: a line that is true whatever it was about, no promise to check it, and a quiet way to send it all
   the same (for the drug question whose words did not give it away). "blocked": what we do not answer. */
function insNoneHtml(res, sheet) {
  if (!res.note) return "";
  if (res.note === "want") {
    const w = res.want, note = wantOn() ? '<span class="want-n">We count how many people ask this. Your words are not sent.</span>' : "", at = ' data-want="' + esc(w.id) + '"' + (note ? " data-count" : "");
    // (2.17) already on the reader's own list (put there by a tap, or by the page itself: insAutoSend): the card says so in place of the button
    const keep = askedList().some(x => x.w === w.id) ? '<p class="ask-said" role="status">It is on your list: we will tell you on this device when it is answered.</p>'
      : '<button type="button" class="' + (sheet ? "qz2-nb ins-askus" : "linklike") + '" data-want-keep="' + esc(w.id) + '">Tell me when it is answered</button>';
    const other = '<button type="button" class="linklike want-other" data-ask="' + esc(res.q) + '">Not the same? Send yours to us</button>';
    const list = w.started ? "#auto/p-" + w.started : "#wanted";   // (2.12) a question listed on a page our system started: that page is where it stands
    return sheet ? '<div class="ins-none ins-want"' + at + '><p class="ins-none-t">Not answered yet. A question like yours is on our list.</p><p class="want-q">' + esc(w.q) + "</p>" + keep + other + note + '<a class="want-all" href="' + esc(list) + '">' + (w.started ? "See its page " : "See the whole list ") + icon("arrow") + "</a></div>"
      : '<div class="sr-fit-none sr-want"' + at + '><p class="want-t"><b>Not answered yet.</b> A question like yours is <a href="' + esc(list) + '">on our list</a>:</p><p class="want-q">' + esc(w.q) + '</p><p class="want-a">' + keep + other + "</p>" + note + "</div>";
  }
  // (2.10.2) a greeting, and a question about the site itself
  if (res.note === "hello" || res.note === "about") { const t = insHelloText(res.note);
    return sheet ? '<div class="ins-none ins-hello"><p class="ins-none-t">' + esc(t[0]) + '</p><p class="ins-none-s">' + esc(t[1]) + (res.note === "about" ? ' <a href="#about">About us</a>' : "") + "</p></div>"
      : '<p class="sr-fit-none sr-hello"><b>' + esc(t[0]) + "</b> " + esc(t[1]) + (res.note === "about" ? ' <a href="#about">About us</a>' : "") + "</p>"; }
  if (res.note === "language") { const el = res.greek ? " Προς το παρόν διαβάζουμε ερωτήσεις μόνο στα αγγλικά." : "";
    return sheet ? '<div class="ins-none ins-lang"><p class="ins-none-t">Pharmakon reads questions in English for now.</p><p class="ins-none-s">Please ask in English.' + el + "</p></div>" : '<p class="sr-fit-none sr-lang"><b>Pharmakon reads questions in English for now.</b> Please ask in English.' + el + "</p>"; }
  // (2.9.2; the senior author opened a question he had sent and was offered to send it again) a question already sent says so
  if ((res.note === "none" || res.note === "other") && askedSentHas(res.q)) { const who = res.stranger ? "We do not know \u201c" + esc(res.stranger) + "\u201d as a drug yet. " : "", rest = who + "No answer yet. It turns green under “Your questions” on the start page when there is one.";
    return sheet ? '<div class="ins-none ins-sent"><p class="ins-none-t">You sent us this question.</p><p class="ins-none-s">' + rest + "</p></div>" : '<p class="sr-fit-none sr-sent"><b>You sent us this question.</b> ' + rest + "</p>"; }
  // 2.9: not finished yet: no verdict, no way to send it; which drug is meant, or go on
  if (res.note === "unfinished") { const t = insUnfinText(res);
    return sheet ? '<div class="ins-none ins-unfin"><p class="ins-none-t">' + esc(t[0]) + '</p><p class="ins-none-s">' + esc(t[1]) + "</p></div>" : '<p class="sr-fit-none sr-unfin"><b>' + esc(t[0]) + "</b> " + esc(t[1]) + "</p>"; }
  // 2.9: not about drugs by its words. The line says what the page read (the senior author, of "We have no answer to this":
  // "it has to have 1/1000 error rate"): with one word it does not know among words that could be asked of any drug, that
  // the word is not known as a drug; else that this does not look like a question about drugs. Both keep the way to send:
  // the rule reads words, and a drug question in everyday words must not be lost.
  if (res.note === "other" && res.stranger) { const w = "\u201c" + esc(res.stranger) + "\u201d";
    return sheet ? '<div class="ins-none ins-other ins-stranger"><p class="ins-none-t">We do not know ' + w + ' as a drug.</p><p class="ins-none-s">If it is one, send us your question and we will look into it.</p>' + insAskBtn(res.q, "linklike", "Send it to us") + "</div>"
      : '<p class="sr-fit-none sr-other sr-stranger"><b>We do not know ' + w + " as a drug.</b> If it is one, " + insAskBtn(res.q, "linklike", "send us your question", " and we will look into it.") + "</p>"; }
  if (res.note === "other") return sheet ? '<div class="ins-none ins-other"><p class="ins-none-t">This does not look like a question about drugs.</p><p class="ins-none-s">Pharmakon answers questions about drugs. If yours is about one, name the drug, or send it to us.</p>' + insAskBtn(res.q, "linklike", "Send it to us") + "</div>"
    : '<p class="sr-fit-none sr-other"><b>This does not look like a question about drugs.</b> Pharmakon answers questions about drugs. If yours is about one, name the drug, or ' + insAskBtn(res.q, "linklike", "send it to us", ".") + "</p>";
  // (2.17) where the page sends such a question by itself (insAutoSend) there is no button to press: the place where the notice will stand
  const line = insNoneLine(res), auto = res.note === "none" && autoSendOn() && !askedGone(res.q);
  return sheet ? '<div class="ins-none"><p class="ins-none-t">' + esc(line) + "</p>" + (res.note !== "none" ? "" : auto ? '<span class="ask-auto"></span>' : insAskBtn(res.q, "qz2-nb ins-askus")) + "</div>"
    : '<p class="sr-fit-none"><b>' + esc(line) + "</b>" + (res.note !== "none" ? "" : auto ? ' <span class="ask-auto"></span>' : " " + insAskBtn(res.q, "linklike")) + "</p>";
}
// the line for a drug question we have no answer to: with a count asked for a place we hold no figure for, it says exactly that
function insNoneLine(res) { return res.figMiss ? "We have no checked figure on this for " + res.figMiss + " yet." : "We haven’t checked exactly this yet."; }
// 2.9: what a question that is not finished is told: [the line, what to do]. With no drug named: which drug is meant;
// with one (or on its page): go on about it
const insHelloText = kind => kind === "hello" ? ["Hello.", "Ask a question about a drug and Insight will look: for example, “is ketamine addictive?”"]
  : ["This is Pharmakon Insight.", "It reads your question on your own device and finds the answer on this site. No person and no chatbot replies to you. Ask about a drug: for example, “is ketamine addictive?”"];
function insUnfinText(res) {
  if (!res.groups.length) return res.cue === false ? ["Go on.", "Finish your question and we will look."] : ["Which drug do you mean?", "Finish your question with its name and we will look."];
  const one = res.groups.length === 1 && res.groups[0].length === 1 ? res.groups[0][0] : null;
  return ["Go on.", "Finish your question" + (one ? " about " + pageWord(one) : "") + " and we will look."];
}
function insRowHtml(x, best) {
  if (isAuto(x.id)) return autoRowHtml(x, best);
  const c = claimById[x.id], sp = SIMPLE.claims[x.id], w = mfWhere(x.page);
  return '<a class="sr-ans sr-fit-a' + (best ? " sr-best" : "") + '" href="' + esc(answerAddr(x.id, x.page)) + '" data-insight="' + esc(x.id) + '" data-page="' + esc(x.page) + '"><span class="k">' + esc(w.name) + '</span><span class="t">' + esc(insQ(x.id, x.page)) +
    '</span><span class="a">' + (best ? cueNum(esc(sp.short)) : esc(glanceClause(sp.short))) + '</span><span class="m">' + meterHtml(c.grade.certainty, true) + "</span></a>";
}
function insFitHtml(res) {
  // (2.11) a place the question only points towards stands last, under its own small heading: the answers found come first
  const routes = res.routes.filter(r => !r.way).map(r => insRouteHtml(r, "sr-route")).join("") + (res.emergency ? insSosHtml("sr-sos") : "");
  const ways = res.routes.filter(r => r.way).map(r => insRouteHtml(r, "sr-route sr-way")).join("");
  const best = res.best.length ? '<p class="sr-fit-h">Best match</p>' + res.best.map(x => insRowHtml(x, true)).join("") : "";
  const none = insNoneHtml(res, false);
  const related = res.related.length ? '<p class="sr-fit-h">' + (res.note === "unfinished" ? "You may mean" : "Related") + "</p>" + res.related.map(x => insRowHtml(x, false)).join("") : "";
  // (2.16.1) a count asked for a place we hold no figure for: the figures from other places stand right under the line that says so
  const far = ways ? '<p class="sr-fit-h">' + (res.figMiss ? "Figures we do have" : "A place to look") + "</p>" + ways : "";
  return '<div class="sr-fit" data-q="' + esc(res.q) + '">' + insReadHtml(res, "sr-read") + routes + best + none + (res.figMiss ? far + related : related + far) + '<button type="button" class="sr-fit-h sr-words" hidden aria-expanded="false">More results</button></div>';
}
// what a screen reader hears when the answers arrive: the route, the tier, the question matched
function insSay(res) {
  const parts = (res.read && res.read.length ? ["We read " + res.read.map(([a, b]) => a + " as " + b).join(" and ")] : []).concat(res.routes.map(r => r.t));
  if (res.best.length) parts.push("Best match: " + res.best.map(x => insQ(x.id, x.page)).join("; "));
  else if (res.note === "want") parts.push("Not answered yet. A question like yours is on our list: " + res.want.q);
  else if (res.note === "unfinished") parts.push(insUnfinText(res).join(" ").replace(/\.$/, ""));
  else if (res.note === "language") parts.push("Pharmakon reads questions in English for now. Please ask in English");
  else if (res.note === "hello" || res.note === "about") parts.push(insHelloText(res.note).join(" "));
  else if ((res.note === "none" || res.note === "other") && askedSentHas(res.q)) parts.push("You sent us this question. No answer yet");
  else if (res.note === "other") parts.push(res.stranger ? "We do not know \u201c" + res.stranger + "\u201d as a drug. If it is one, you can send us your question" : "This does not look like a question about drugs. Pharmakon answers questions about drugs");
  else if (res.note) parts.push(insNoneLine(res).replace(/\.$/, ""));
  if (res.related.length) parts.push(res.related.length + " related answer" + (res.related.length === 1 ? "" : "s"));
  return parts.join(". ");
}
function insInject(box, res) {
  box.querySelectorAll(".sr-fit").forEach(e => e.remove());
  // what Insight shows is not repeated by the word search below it, which no longer calls any of its rows the best answer
  res.best.concat(res.related).forEach(x => box.querySelectorAll('a.sr-ans[data-cid="' + x.id + '"]').forEach(a => a.remove()));
  res.routes.forEach(r => box.querySelectorAll(':scope > a[href="' + r.href + '"]').forEach(a => a.remove()));
  // (2.12) the question names a drug of a page our system started and no drug the site has checked answers on: the answers the
  // word search found are about other drugs (a stray word in common), and the page's own row is the route above
  if (res.routes.some(r => r.started) && !res.groups.length) box.querySelectorAll(":scope > a.sr-ans, :scope > a[href^='#auto/p-']").forEach(a => a.remove());
  // (2.13; the senior author asked "How many people die from methamphetamine" and found the rows under "More results" "completely
  // irrelevant ... this creates visual clutter") The word search finds an answer by a word in common ("people", "meth", "test"). Under
  // Insight's own block such a row stays only when the answer is also near the question in meaning (the nearest of its wordings
  // with the drug names taken out, INS_MORE or more); the others are taken out.
  if (res.sc) box.querySelectorAll(":scope > a.sr-ans[data-cid]").forEach(a => { const i = INS.idx.get(a.dataset.cid); if (i == null || res.sc.topic[i] < INS_MORE) a.remove(); });
  box.querySelectorAll(":scope > a.sr-ans.best").forEach(a => { a.classList.remove("best"); const k = a.querySelector(".k"); if (k) k.textContent = k.textContent.replace(/^Best answer/, "Answer"); });
  const none = box.querySelector(":scope > .none"), ask = box.querySelector(":scope > .sr-ask");
  if (none) none.remove();                                     // Insight has its own line for a question with no checked answer
  if (ask && (res.note || !box.querySelector(":scope > a"))) ask.remove();   // one way to ask us, not two (and none for what we do not answer)
  if (res.note === "blocked") box.querySelectorAll(":scope > a").forEach(a => { if (!/^#s-[a-z0-9-]+$/.test(a.getAttribute("href") || "")) a.remove(); });
  if (res.note === "other" || res.note === "hello" || res.note === "about") box.querySelectorAll(":scope > a").forEach(a => a.remove());   // 2.5: not about drugs by its words: one calm line, no rows found by a stray word
  const note = box.querySelector(":scope > .sr-note");
  if (note) note.insertAdjacentHTML("afterend", insFitHtml(res)); else box.insertAdjacentHTML("afterbegin", insFitHtml(res));
  // the word search's own rows follow under a quiet label, so that none reads as part of the best match or the related answers
  // (2.13; the senior author, of a question that got nine rows: "it should be much easier to find what I want this is so confusing I read so many
  // things I don't want to read") What Insight found stands alone. The word search's own rows wait behind one quiet button, "More results (5)",
  // and open on a tap; with nothing from Insight they are the results and stand open.
  const words = box.querySelector(".sr-fit .sr-words"), more = [...box.querySelectorAll(":scope > a")], shown = !!(res.routes.length || res.best.length || res.related.length || res.note);
  if (words) { words.hidden = !more.length || !shown;
    if (!words.hidden) { more.forEach(a => { a.hidden = true; }); words.textContent = "More results (" + more.length + ")"; words.setAttribute("aria-expanded", "false");
      words.onclick = e => { e.preventDefault(); e.stopPropagation(); const open = words.getAttribute("aria-expanded") !== "true"; more.forEach(a => { a.hidden = !open; }); words.setAttribute("aria-expanded", String(open)); words.textContent = (open ? "Fewer results" : "More results (" + more.length + ")"); }; } }
  const live = document.getElementById("search-count"); if (live) live.textContent = insSay(res);
  insAuto(box.querySelector(".sr-fit"), res, false);   // (2.16.1) with no answer of ours: what is published on it, looked up by itself
  // 2.5: a listed question that stays on the screen is counted once (wantCount), only where its card says so
  clearTimeout(INS.wantT);
  if (res.note === "want") INS.wantT = setTimeout(() => { const b = document.getElementById("search-results"), s = document.getElementById("search");
    if (b && !b.hidden && s && insClean(s.value) === res.q && b.querySelector('.sr-want[data-count][data-want="' + res.want.id + '"]')) wantCount(res.want.id); }, WANT_WAIT);
}
// How near in meaning an answer the word search found must be to stay under "More results": the nearest of its wordings with the drug names taken out
// (the same look that makes an answer "related"). Looked at on 17 November 2026: for "how many people die from methamphetamine" every row the word
// search added was 0.37 or less (none was about dying); for "how can i use test kits at home" the answers about test strips were 0.37 to 0.48 and the
// rows found by the word "test" alone 0.29 or less; for "does weed help you sleep" the answer about sleep was 0.55 and the others 0.35 or less.
const INS_MORE = 0.4;
/* (2.9.2) An entry of one or two words is for the word search. When it is not a finished question ("can i", "do gay", "is
   cocaine"), the page says so in place of "No match … Ask us": a beginning is not sent. A drug's name alone keeps its rows. */
function insShort(box, q) {
  if (!INS.unfin || !q) return;
  const text = insSpell(q).text, groups = insNamed(text), drug = groups.length ? null : insCtx().drug, unf = insUnfinished(text, !!drug);
  // a greeting of one or two words ("hello", "thank you"): its own line, in place of "No match"
  if (!groups.length && !drug && INS_RE.greet.test(q) && !box.querySelector(":scope > a")) { box.querySelectorAll(":scope > .sr-ask, :scope > .none").forEach(e => e.remove());
    box.insertAdjacentHTML("afterbegin", '<div class="sr-fit" data-q="' + esc(q) + '">' + insNoneHtml({ q, note: "hello" }, false) + "</div>"); const l = document.getElementById("search-count"); if (l) l.textContent = insHelloText("hello").join(" "); return; }
  if (!unf) return;
  box.querySelectorAll(":scope > .sr-ask, :scope > .none").forEach(e => e.remove());
  if (groups.length && insUnfTokens(text).w.every(x => x === "it")) return;            // the name and nothing more: its rows are the answer
  { const flat = insStartedFlat(text); if (insStartedNames().some(([n]) => n === flat || n + "s" === flat || n === flat + "s")) return; }   // (2.12) the same for a page our system started
  const res = { q, note: "unfinished", unf, groups: groups.length ? groups : drug ? [[drug]] : [] }; if (!res.groups.length) res.cue = insUnfCue(text);
  const html = '<div class="sr-fit" data-q="' + esc(q) + '">' + insNoneHtml(res, false) + "</div>", note = box.querySelector(":scope > .sr-note");
  if (note) note.insertAdjacentHTML("afterend", html); else box.insertAdjacentHTML("afterbegin", html);
  const live = document.getElementById("search-count"); if (live) live.textContent = insUnfinText(res).join(" ");
}
// called by runSearch after the word search has drawn its results
function insightAfterSearch(raw) {
  const box = document.getElementById("search-results"); if (!box || box.hidden) return;
  if (INS.state !== "ready") {
    const q0 = insClean(raw), whole = !!q0 && (insWordsIn(q0) >= INS_WORDS || !!insCountKind(q0));
    // saving data: one quiet line under the results offers it; once tapped, it says it is coming
    if (INS.state === "idle" && insSaver()) { box.insertAdjacentHTML("beforeend", '<p class="sr-get"><button type="button" class="linklike" data-ins-get>' + esc(insGetText()) + "</button></p>"); return; }
    if (INS.state === "idle" && q0) insightLoad();   // (the box's own listener starts it too; here it has begun before the rows are judged)
    // (2.16.1) it could not start (offline, or a browser that cannot run it): said, with a way to try again; the rows are the word search's own
    if (INS.state === "off") { if (whole) box.insertAdjacentHTML("afterbegin", '<p class="sr-get sr-wait sr-off" role="status">Insight could not start on this device, so these are matches by words alone. ' + (typeof WebAssembly === "object" ? '<button type="button" class="linklike" data-ins-again>Try again</button>' : "") + "</p>"); return; }
    if (INS.state !== "loading") return;
    if (whole) {
      // (2.16.1) a whole question, and Insight is still getting ready: one calm line. The rows the word search found by a word in common are not an
      // answer to it and are not shown as one: they wait (a drug's own page stays). On a slow first download they come back after a few seconds,
      // under a line that says what they are.
      const waited = Date.now() - (INS.t0 || Date.now()), slow = waited >= INS_SLOW, rows = [...box.querySelectorAll(":scope > a")].filter(a => !/^#(?:s-[a-z0-9-]+|emergency)$/.test(a.getAttribute("href") || ""));
      box.querySelectorAll(":scope > .sr-ask, :scope > .none").forEach(e => e.remove());
      if (!slow) rows.forEach(a => { a.hidden = true; });
      box.insertAdjacentHTML("afterbegin", '<p class="sr-get sr-wait" role="status">' + (INS.byHand ? "Downloading, once: about " + insMB() + " MB…" : slow ? "Still getting ready: the first time, Insight downloads about " + insMB() + " MB." + (rows.length ? " Until then, matches by words alone:" : "") : "One moment: Insight is getting ready to read your question…") + "</p>");
      clearTimeout(INS.slowT);
      if (!slow) INS.slowT = setTimeout(() => { const s = document.getElementById("search"); if (INS.state === "loading" && s && !box.hidden && insClean(s.value) === q0) runSearch(s.value); }, INS_SLOW - waited + 60);
      return;
    }
    if (INS.byHand) box.insertAdjacentHTML("beforeend", '<p class="sr-get" role="status">Downloading, once: about ' + insMB() + " MB…</p>");
    return;
  }
  if (!box.querySelector(":scope > .sr-note")) box.insertAdjacentHTML("afterbegin", '<p class="sr-note">' + icon("mobile") + "<span>" + esc(insNoteText()) + "</span></p>");
  const q = insClean(raw); clearTimeout(INS.timer);
  if (insWordsIn(q) < INS_WORDS && !insCountKind(q)) { INS.seq++; insShort(box, q); return; }   // (2.14: "heroin deaths" asks for a count, in two words)
  const ctx = insCtx(), have = INS.cache.get(insKey(q, ctx));
  if (have) { INS.seq++; insInject(box, have); return; }
  const seq = ++INS.seq;
  INS.timer = setTimeout(() => insAnswer(q, ctx).then(res => {
    const s = document.getElementById("search"), b = document.getElementById("search-results");
    if (seq !== INS.seq || !s || insClean(s.value) !== q || !b || b.hidden) return;   // the reader has typed on
    insInject(b, res);
  }).catch(() => {}), INS_WAIT);
}
// once ready, the results already open take their answers; a question sent with Enter meanwhile opens now
function insightReady() {
  askedCheck();   // (2.4) the reader's kept questions, asked again once per new version
  const s = document.getElementById("search"), box = document.getElementById("search-results");
  if (s && INS.want && insClean(s.value) === INS.want && !EV.open) { INS.want = null; insAsk(s.value); return; }
  INS.want = null;
  if (s && box && !box.hidden && (document.activeElement === s || s.value.trim())) runSearch(s.value);
}
(function () {
  const s = document.getElementById("search"); if (!s) return;
  const auto = () => { if (!insSaver()) insightLoad(); };
  s.addEventListener("focus", auto); s.addEventListener("input", auto);
  s.addEventListener("focus", insPlaceholder);
  document.getElementById("search-results").addEventListener("click", e => {
    if (!e.target.closest || !e.target.closest("[data-ins-get]")) return;
    INS.byHand = true; insightLoad(); setTimeout(() => { s.focus(); runSearch(s.value); }, 0);   // after this click has run its course
  });
  document.getElementById("search-results").addEventListener("click", e => {   // (2.16.1) "Try again", where Insight could not start
    if (!e.target.closest || !e.target.closest("[data-ins-again]")) return;
    e.preventDefault(); INS.tries = 0; INS.state = "idle"; insightLoad(); setTimeout(() => { s.focus(); runSearch(s.value); }, 0);
  });
  if (window.requestIdleCallback) requestIdleCallback(insWarm, { timeout: 2500 }); else setTimeout(insWarm, 1200);
  window.addEventListener("hashchange", () => { insPlaceholder(); insArrive(); });
  insPlaceholder();
})();
/* Enter (or the search key on a phone) opens the answer to the question as asked. Before the page's own handler, which
   opens the first result: that stays for a word or two (a drug's name goes to its page) and when Insight is not there. */
document.addEventListener("keydown", e => {
  if (e.key !== "Enter" || e.isComposing || !e.target || e.target.id !== "search") return;
  const q = insClean(e.target.value); if (insWordsIn(q) < INS_WORDS && !insCountKind(q)) return;
  if (INS.state === "ready") { e.preventDefault(); e.stopPropagation(); insAsk(q); return; }
  if (INS.state === "loading") { e.preventDefault(); e.stopPropagation(); INS.want = q; runSearch(e.target.value); }   // it opens once ready (insightReady)
}, true);

/* ---------- Next questions (2.3): the nearest answers by meaning, never from another drug (const INS_NEXT, from the build).
   These few functions are also called while the pages draw, before the rest of this file has run: they read nothing of it. */
function insNextOf(id) {
  if (typeof INS_NEXT === "undefined" || !INS_NEXT || !INS_NEXT.ids) return null;
  if (!insNextOf.at) insNextOf.at = new Map(INS_NEXT.ids.map((x, i) => [x, i]));
  const i = insNextOf.at.get(id); return i == null ? [] : (INS_NEXT.next[i] || []).map(j => INS_NEXT.ids[j]);
}
// the answers opened in this visit (in memory only), so that none is offered again
function insOpenedNow() { return insOpenedNow.s || (insOpenedNow.s = new Set()); }
// the answers that have a card on a page: a drug's page (its own and its mixing answers), mixing, drug checking, the facts page
function insOnPage(page) {
  const m = insOnPage.m || (insOnPage.m = new Map()); if (m.has(page)) return m.get(page);
  const ids = page === "interactions" ? (QUESTIONS.interactions || []).flatMap(g => g.items.map(x => x[0])) : drugQuestions(page).map(x => x[0]).concat(subBySlug[page] ? mixQuestions(page).map(x => x[0]) : []);
  const s = new Set(ids.filter(id => claimById[id])); m.set(page, s); return s;
}
/* "Read next" at the end of an open answer on a page (app.simple.js readNextHtml hands over to this): up to three of its next
   questions that are on this page, without the ones opened in this visit. If the index was not built, the next questions of
   the topic, as before 2.3. The block is drawn again when its answer opens, so it is right at the moment it is read. */
function insReadNext(id, nexts, page, pre) {
  const P = pre || "ask-", nx = insNextOf(id), here = insOnPage(page), seen = insOpenedNow();
  const ids = nx ? nx.filter(x => here.has(x) && !seen.has(x) && (SIMPLE.claims || {})[x]).slice(0, 3) : (nexts || []).map(x => x[0]);
  if (!ids.length) return "";
  const href = x => (subBySlug[page] ? "#s-" + page + "/q-" + x : answerAddr(x, page));
  return '<div class="rn" data-rn="' + esc(id) + '" data-rn-page="' + esc(page) + '" data-rn-pre="' + esc(P) + '"><p class="rn-k">Read next</p><ul class="rn-l">' +
    ids.map(x => '<li><a href="' + esc(href(x)) + '" data-open="' + esc(P + x) + '" data-rn-id="' + esc(x) + '"><span>' + esc((page && sharedQuestion(page, x)) || anyQuestion(x) || "") + "</span>" + icon("arrow") + "</a></li>").join("") + "</ul></div>";
}
document.addEventListener("toggle", e => {
  const d = e.target; if (!d.matches || !d.matches("details.ask[open]") || !d.dataset.cid) return;
  insOpenedNow().add(d.dataset.cid);
  const rn = d.querySelector(":scope > .ask-a > .rn[data-rn]"); if (!rn) return;
  const html = insReadNext(rn.dataset.rn, null, rn.dataset.rnPage, rn.dataset.rnPre);
  if (html) rn.outerHTML = html; else rn.remove();
}, true);

/* ---------- One answer at a time, or the answer to a question as asked, over the page (the sheet the evidence opens in, with
   its Back button, Escape and the phone's own Back) ---------- */
function insPeopleAsk(ids, shown, groups) {
  const had = new Set(shown.concat([...insOpenedNow()])), out = [];
  // (a question that named a drug keeps to that drug: the next questions of a related answer may live on other drugs' pages too)
  const fits = x => !groups || !groups.length || !INS.about || !INS.idx.has(x) || groups.some(g => g.some(s => INS.about[INS.idx.get(x)].has(s)));
  for (let k = 0; out.length < 3 && k < 60; k++) for (const id of ids) { const x = (insNextOf(id) || [])[k]; if (x && !had.has(x) && claimById[x] && (SIMPLE.claims || {})[x] && fits(x) && out.length < 3) { had.add(x); out.push(x); } }
  if (!out.length) return "";
  return '<div class="rn ins-next"><p class="rn-k">People also ask</p><ul class="rn-l">' + out.map(x => '<li><a href="' + esc(answerAddr(x)) + '" data-insight-next="' + esc(x) + '"><span>' + esc(insQ(x)) + "</span>" + icon("arrow") + "</a></li>").join("") + "</ul></div>";
}
function insEndHtml() {
  const n = INS.run.n;
  return '<div class="ins-end"><p class="ins-end-t">You’ve read ' + n + " answers</p><p class=\"ins-end-s\">Ask something else, or keep going with questions like these.</p>" +
    '<div class="ins-end-b"><button type="button" class="qz2-nb" data-ins-ask>Ask something else</button><button type="button" class="linklike" data-ins-more>Keep reading</button></div></div>';
}
// one checked answer in the sheet, as everywhere on the site: the short answer, its But, the picture of its numbers, an
// early draft's reason, How do we know?, the bars and the evidence. depth "full": How do we know? open and the evidence as
// a button; "short": the short answer and its But, the bars and the way to the evidence, nothing else.
function insBodyHtml(id, depth) {
  if (isAuto(id)) return autoBodyHtml(id);
  const c = claimById[id], sp = SIMPLE.claims[id];
  if (depth === "short") return '<p class="ask-short">' + cueNum(esc(sp.short)) + "</p>" + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") +
    '<div class="ask-foot">' + meterHtml(c.grade.certainty, true) + '<span class="ask-acts"><a class="ask-ev" href="#' + esc(id) + '">The evidence ' + icon("arrow") + "</a></span></div>";
  const body = answerBody(id, c, sp, false);
  return depth === "full" ? body.replace('<details class="ask-how">', '<details class="ask-how" open>') : body;
}
const insPageLink = (id, page) => { if (isAuto(id)) { const p = AUTO[id].page, k = typeof p === "string" && p.slice(0, 4) === "new:" ? p.slice(4) : "";      // (2.8) an answer on a page the system started links to that page
    return k && typeof AUTO_PAGES === "object" && AUTO_PAGES && AUTO_PAGES[k] ? '<p class="ins-page"><a class="qz2-ev" href="#auto/p-' + esc(k) + '">' + esc(AUTO_PAGES[k]) + ": the page our system started " + icon("arrow") + "</a></p>"
      : '<p class="ins-page"><a class="qz2-ev" href="#auto">Everything written by our system ' + icon("arrow") + "</a></p>"; }
  const addr = answerAddr(id, page), w = mfWhere(page), pl = sharedPlace(page || "", id);
  return '<p class="ins-page">' + (/^#cl_/.test(addr) ? '<a class="qz2-ev" href="' + esc(pl.href) + '">' + esc(pl.more) + " " + icon("arrow") + "</a>" : '<a class="qz2-ev" href="' + esc(addr) + '">See it on the ' + esc(w.name) + " page " + icon("arrow") + "</a>") + "</p>"; };
const insBar = eye => '<div class="ev-bar"><button type="button" class="ev-back">' + icon("arrow") + '<span>Back</span></button><span class="ev-eye ins-eye">' + eye + "</span></div>";
function insTailHtml(ids, shown, groups) { return INS.run.n - INS.run.more >= INS_END ? insEndHtml() : insPeopleAsk(ids, shown, groups); }
// v: { kind: "one", id, page, depth, sos } (one answer, its own question as the heading) or { kind: "asked", res } (the
// person's own question as the heading, then each best answer in full, each under a quiet label naming the checked question)
function insHtml(v) {
  if (v.kind === "one") {
    const w = mfWhere(v.page);
    return insBar(icon(w.f.icon) + "<span>" + esc(w.name) + "</span>") + '<div class="ins' + (v.depth ? " ins-" + v.depth : "") + '"><h2 id="ev-title" tabindex="-1">' + esc(insQ(v.id, v.page)) + "</h2>" + (v.sos ? insSosHtml("dh-help ins-sos") : "") +
      '<div class="ins-ans">' + insBodyHtml(v.id, v.depth) + "</div>" + insPageLink(v.id, v.page) + insTailHtml([v.id], [v.id]) + "</div>";
  }
  const res = v.res, away = r => !!(res.figMiss && r.way), routes = res.routes.filter(r => !away(r)).map(r => insRouteHtml(r, "ins-route")).join("") + (res.emergency ? insSosHtml("dh-help ins-sos") : "");
  const ways = res.routes.filter(away).map(r => insRouteHtml(r, "ins-route")).join("");
  const best = res.best.map((x, n) => { const w = mfWhere(x.page);
    return '<section class="ins-one" aria-labelledby="ins-l' + n + '"><p class="ins-l" id="ins-l' + n + '"><span class="ins-l-k">' + icon(w.f.icon) + "<span>" + (isAuto(x.id) ? "Written by our system" : "Checked answer") + " · " + esc(w.name) + '</span></span><span class="ins-l-q">' + esc(insQ(x.id, x.page)) + "</span></p>" +
      '<div class="ins-ans">' + insBodyHtml(x.id, res.depth) + "</div>" + insPageLink(x.id, x.page) + "</section>"; }).join("");
  const none = insNoneHtml(res, true);
  const related = !res.best.length && res.related.length ? '<div class="rn ins-rel"><p class="rn-k">' + (res.note === "unfinished" ? "You may mean" : "Related") + '</p><ul class="rn-l">' + res.related.map(x => { const w = mfWhere(x.page);
    return '<li><a href="' + esc(answerAddr(x.id, x.page)) + '" data-insight-next="' + esc(x.id) + '" data-page="' + esc(x.page) + '"><span><span class="ins-rel-k">' + esc(w.name) + "</span>" + esc(insQ(x.id, x.page)) + "</span>" + icon("arrow") + "</a></li>"; }).join("") + "</ul></div>" : "";
  const from = (res.best.length ? res.best : res.related).map(x => x.id), shown = res.best.concat(res.related).map(x => x.id);
  return insBar("<span>Your question</span>") + '<div class="ins ins-asked' + (res.depth ? " ins-" + res.depth : "") + '"><h2 id="ev-title" class="ins-yours" tabindex="-1">' + esc(insCap(res.q.length > 240 ? res.q.slice(0, 237) + "…" : res.q)) + "</h2>" +
    insReadHtml(res, "ins-read") + routes + best + none + (ways ? '<p class="rn-k ins-ways-h">Figures we do have</p>' + ways : "") + related + insTailHtml(from, shown, res.groups) + "</div>";
}
function insDraw(v, opener) {
  const sh = document.getElementById("evsheet"), panel = sh && sh.querySelector(".panel"); if (!panel) return false;
  if (!EV.open) { EV.opener = opener === undefined ? document.activeElement : opener; try { history.pushState({ pkEvidence: "insight", pk: NAV_CUR }, ""); EV.pushed = true; } catch (e) { EV.pushed = false; } }
  // (an evidence still on its way for this sheet is not drawn over the answer: openEvidence draws only for its own EV.id)
  EV.id = "ins:" + (v.kind === "one" ? v.id : "asked"); EV.open = true; sh.classList.add("open"); document.documentElement.classList.add("sheet-open"); hidePop(); closeSearch();
  INS.view = v; INS.back = null;
  panel.innerHTML = insHtml(v); panel.scrollTop = 0;
  if (v.kind === "asked") insAuto(panel, v.res, true);   // (2.16.1) with no answer of ours: what is published on it, looked up by itself
  (v.kind === "one" ? [v.id] : v.res.best.map(x => x.id)).forEach(id => { markSeen(id); insOpenedNow().add(id); });
  const f = panel.querySelector("#ev-title"); if (f) f.focus({ preventScroll: true });
  const wc = panel.querySelector(".ins-want[data-count]"); if (wc) wantCount(wc.dataset.want);   // 2.5: Enter on a listed question counts it at once
  return true;
}
// a new run of answers starts when the sheet opens; each answer or question read in it counts one towards the calm end
function insCount(fresh) { if (fresh || !INS.run || !EV.open) INS.run = { n: 0, more: 0 }; INS.run.n++; }
// one answer (opt: page, depth, sos, opener, fresh, from)
function openInsight(id, opener, fresh, opt) {
  if (!isAuto(id) && (!claimById[id] || !(SIMPLE.claims || {})[id])) return false;
  opt = opt || {}; insCount(fresh);
  if (!EV.open) INS.from = opt.from || null;
  return insDraw({ kind: "one", id, page: isAuto(id) ? AUTO[id].page : opt.page || answerPageKey(id) || claimById[id].substance, depth: opt.depth || "", sos: !!opt.sos }, opener);
}
// what the search box and its results were when the sheet opened over them: Back puts them back as they were
function insFromSearch(id) { const s = document.getElementById("search"); return { value: s ? s.value : "", hash: location.hash, id: id || null }; }
// the answer to a question as asked (Enter). A question that is only a request for something else (a dose, a test, a drug's
// page, help now) and has no checked answer of its own goes straight to that place, as its row in the list would.
function insAsk(q) {
  const from = insFromSearch(null);
  return insAnswer(q, insCtx()).then(res => {
    // Enter goes straight to a place only when the place is the answer, or was asked for by name; a place the question only points
    // towards, or that leaves the question open, is shown in the sheet with what else was found and the way to ask us (2.11)
    if (!res.best.length && res.routes.length === 1 && res.routes[0].kind !== "mix" && (!res.routes[0].loose || res.routes[0].named)) { insFollow(res.routes[0]); return res; }
    insCount(true); if (!EV.open) INS.from = from; insDraw({ kind: "asked", res }, null); return res;
  });
}
function insFollow(r) {
  const s = document.getElementById("search"); if (s) { s.value = ""; s.blur(); } closeSearch();
  if (r.fb) { openFeedback(r.fb, location.hash, ""); return; }                       // (2.11) "report a mistake": the form
  INS.go = { at: Date.now(), el: r.el || null, mix: r.mix ? r.mix.split(",") : null, country: r.country || null, fig: r.fig || null };   // (the country a law question named goes with it; the figures a counting question asked for)
  if (location.hash === r.href) { route(); insArrive(); } else location.hash = r.href;
}
/* Back to where the reader was. The sheet closes in app.simple.js (its Back button, a tap outside, Escape, the phone's Back);
   seen from here, when it has closed over a search, the question is still in the box and its results are open again, with
   the cursor on the row that was opened (on a phone, no keyboard jumps up). A page reached from the sheet is left alone. */
function insClosed() {
  const f = INS.from; INS.from = null; INS.view = null; INS.back = null; if (!f) return;
  setTimeout(() => {   // once the click or key that closed the sheet has run its course (the page closes the results on a click outside them)
    const s = document.getElementById("search"), box = document.getElementById("search-results");
    if (!s || !box || EV.open || location.hash !== f.hash || s.value !== f.value) return;
    const touch = !!(window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
    if (!insClean(f.value)) { if (!touch) s.focus({ preventScroll: true }); return; }   // opened from the questions to try, under an empty box
    runSearch(s.value);
    const row = (f.id && box.querySelector('a[data-insight="' + f.id + '"], a[data-cid="' + f.id + '"]')) || (touch ? box.querySelector("a") : null);
    if (row) row.focus({ preventScroll: true }); else s.focus({ preventScroll: true });
  }, 0);
}
(function () {
  const sh = document.getElementById("evsheet"); if (!sh || typeof MutationObserver === "undefined") return;
  new MutationObserver(() => { if (!sh.classList.contains("open") && (INS.view || INS.from)) insClosed(); }).observe(sh, { attributes: true, attributeFilter: ["class"] });
})();

/* Following a route. The link itself goes to the page (its address is the route's); once the page has drawn, the block the
   route is for is brought into view, and the mixing tool gets both drugs chosen. */
function insArrive() {
  const g = INS.go; INS.go = null; if (!g || Date.now() - g.at > 4000) return;
  if (g.mix) insMixPick(g.mix[0], g.mix[1]);
  if (g.country) insLawFor(g.country);
  // (2.14) the figures a counting question asked for: the statistics page shows that place, that drug's figures, at that kind
  if (g.fig && !/\/f-/.test(location.hash)) { const [file, sub, kind] = g.fig.split("|"); let n = 0;   // (2.15.3: the address itself carries the drug and the kind now)
    const show = () => { const sec = document.getElementById("n-" + file), sel = document.getElementById("num-sub-" + file);
      if (!sec || !sec.querySelector(".sec-b") || !sec.querySelector(".sec-b").children.length) { if (n++ < 40) setTimeout(show, 100); return; }
      if (sel && sub && sel.value !== sub && [...sel.options].some(o => o.value === sub)) { sel.value = sub; sel.dispatchEvent(new Event("change", { bubbles: true })); }
      const name = (FIG_KINDS.find(x => x[0] === kind) || [])[1], h = name && [...sec.querySelectorAll("h3.tp")].find(x => x.textContent.indexOf(name) === 0);
      if (h) { scrollToEl(h); h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } };
    setTimeout(show, 80); }
  if (g.el) setTimeout(() => { const el = document.getElementById(g.el); if (!el || !el.closest(".view.active")) return; scrollToEl(el);
    const h = el.querySelector("h2, h3") || el; h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }, 60);
}
// (2.9.2) the law part of a drug's page for the country a question named ("is weed legal in greece"), without changing the
// country the reader chose for themselves; the reader's own country comes back with the page's next drawing
function insLawFor(un) {
  setTimeout(() => { const slug = renderedDrug, box = document.querySelector("#drug2 #d-law .sec-b"); if (!slug || !box || !WORLD_LAW.countries.some(x => x.name === un)) return;
    const draw = () => { if (renderedDrug !== slug) return;
      box.innerHTML = '<div class="cq set"><p class="cq-where">' + icon("pin") + "<span>" + esc(shortCtry(un)) + '</span></p><span class="cq-asked">The country you asked about</span></div><p class="say">' + esc(lawPlain(slug, un)) +
        '</p><details class="lawmore" open><summary>What the law says, with its sources</summary><div class="lawmore-b">' + countryOut(slug, un) + '<p class="small"><a href="#law">Treaties, country by country</a></p></div></details>'; };
    if (legalReady(slug)) draw(); else whenReady(() => loadFull(slug), box, "The law", draw); }, 120);
}
/* The mixing tool with both drugs chosen. The tool (app.simple.js renderMix2) takes one drug; here the second chip is pressed
   too and the list keeps to the answers about both. With no checked answer about the pair, it says so and shows what is
   known about mixing the first. Choosing a chip afterwards is the tool's own again. */
function insMixPick(a, b) {
  const all = (QUESTIONS.interactions || []).flatMap(g => g.items.map(x => x[0])).filter(id => claimById[id]), has = s => all.some(id => (MIXFOR[id] || []).includes(s));
  if (!has(a) && has(b)) [a, b] = [b, a];
  mixPick = has(a) ? a : ""; renderMix2();
  const box = document.getElementById("mix2"), line = box && box.querySelector(".mix-n"); if (!box || !line) return;
  const both = new Set(all.filter(id => (MIXFOR[id] || []).includes(a) && (MIXFOR[id] || []).includes(b))), pair = pageWord(a) + " with " + pageWord(b);
  const chip = box.querySelector('button.mixchip[data-mix="' + b + '"]'); if (chip && both.size) chip.setAttribute("aria-pressed", "true");
  if (!both.size) { line.textContent = "No checked answer yet about mixing " + pair + ". " + line.textContent.replace(/^(\d+ questions?)( about .*)?$/, mixPick ? "$1$2:" : "Every answer on mixing:"); return; }
  const more = box.querySelector(".asks-more"); if (more) { more.hidden = false; const mb = box.querySelector("button.morebtn"); if (mb) mb.remove(); }
  box.querySelectorAll("details.ask[data-cid]").forEach(d => { d.hidden = !both.has(d.dataset.cid); });
  line.textContent = both.size + " question" + (both.size === 1 ? "" : "s") + " about mixing " + pair;
  const first = box.querySelector("details.ask[data-cid]:not([hidden])"); if (first && both.size === 1) first.open = true;
}
/* Clicks, before the page's own handlers (capture). */
const insPlain = e => !(e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey);   // a new tab, or a link opened another way, goes its own way
// the answer an address opens, and whether the reader is on the page it opens on (there, questions open in place as before)
function insLinked(a) {
  const h = a.getAttribute("href") || "", v = (document.querySelector(".view.active") || {}).id || "";
  let m = h.match(/^#s-([a-z0-9-]+)\/q-(cl_[a-z0-9_]+)$/); if (m) return { id: m[2], page: m[1], here: v === "view-drug" && renderedDrug === m[1] };
  m = h.match(/^#facts\/q-(cl_[a-z0-9_]+)$/); if (m) return { id: m[1], page: GEN, here: v === "view-facts" };
  m = h.match(/^#checking\/q-(cl_[a-z0-9_]+)$/); if (m) return { id: m[1], page: DC, here: v === "view-checking" };
  return null;
}
document.addEventListener("click", e => {
  if (!e.target.closest || !insPlain(e)) return;
  const a = e.target.closest("a[href]"); if (!a) return;
  const inSheet = !!a.closest("#evsheet"), inSearch = !!a.closest("#search-results");
  // a route: the link goes to the page; what is left to do there is noted for when the page has drawn (insArrive)
  if (a.dataset.insRoute) {
    if (a.dataset.fbOpen) { e.preventDefault(); e.stopPropagation(); if (inSearch) { const s = document.getElementById("search"); if (s) s.value = ""; closeSearch(); } openFeedback(a.dataset.fbOpen, location.hash, ""); return; }   // (2.11) "report a mistake": the form
    INS.go = { at: Date.now(), el: a.dataset.el || null, mix: a.dataset.mix ? a.dataset.mix.split(",") : null, country: a.dataset.country || null, fig: a.dataset.fig || null };
    if (location.hash === a.getAttribute("href")) { e.preventDefault(); if (inSearch) { const s = document.getElementById("search"); if (s) s.value = ""; closeSearch(); } route(); insArrive(); }
    return;
  }
  // in the sheet: a next question opens here; the evidence opened from an answer comes back to it with Back
  if (inSheet) {
    const ins = document.querySelector("#evsheet .panel .ins");
    if (ins && a.dataset.insightNext) { e.preventDefault(); e.stopPropagation(); openInsight(a.dataset.insightNext, null, false, { page: a.dataset.page, sos: !!(INS.view && INS.view.kind === "asked" && INS.view.res.emergency),
      depth: INS.view && INS.view.kind === "asked" && a.closest(".ins-rel") ? INS.view.res.depth : "" }); return; }   // (asked for the full evidence, or the short of it: a related answer opens that way)
    if (ins && /^#cl_/.test(a.getAttribute("href") || "")) INS.back = INS.view;
    return;
  }
  // in the results: an answer opens over the page, the question staying in the box for the way back
  if (inSearch) {
    const id = a.dataset.insight || a.dataset.cid || (insLinked(a) || {}).id; if (!id) return;
    const res = a.dataset.insight ? INS.cache.get(insKey(document.getElementById("search").value, insCtx())) : null;
    if (openInsight(id, null, true, { page: a.dataset.page || (insLinked(a) || {}).page, depth: res ? res.depth : "", sos: !!(res && res.emergency), from: insFromSearch(id) })) { e.preventDefault(); e.stopPropagation(); }
    return;
  }
  // Myth or fact's "Read the answer" (always), a "Read next" whose answer is not on the page in view, and any link to an
  // answer from outside its own page: the answer opens over the page, and Back returns to the same card, scrolled as it was
  const rn = a.dataset.rnId && !((document.getElementById(a.dataset.open) || { closest: () => null }).closest(".view.active"));
  const l = a.dataset.sheet ? { id: a.dataset.sheet, page: (insLinked(a) || {}).page, here: false } : rn ? { id: a.dataset.rnId, here: false } : insLinked(a);
  if (!l || l.here) return;
  if (openInsight(l.id, a, true, { page: l.page })) { e.preventDefault(); e.stopPropagation(); }
}, true);
document.addEventListener("click", e => {
  if (!e.target.closest || !EV.open) return;
  // Back from the evidence that an answer here opened returns to the answer
  if (INS.back && !document.querySelector("#evsheet .panel .ins") && e.target.closest("#evsheet .ev-back")) {
    e.preventDefault(); e.stopPropagation();
    const v = INS.back; INS.back = null; insDraw(v); return;
  }
  const t = e.target.closest("#evsheet [data-ins-ask], #evsheet [data-ins-more]"); if (!t || !INS.view) return;
  if (t.hasAttribute("data-ins-ask")) { INS.from = null; closeEvidence(); const s = document.getElementById("search"); if (s) { s.value = ""; setTimeout(() => s.focus(), 0); } return; }
  INS.run.more = INS.run.n;
  const v = INS.view, ids = v.kind === "one" ? [v.id] : (v.res.best.length ? v.res.best : v.res.related).map(x => x.id), box = t.closest(".ins-end");
  if (box) box.outerHTML = insPeopleAsk(ids, v.kind === "one" ? [v.id] : v.res.best.concat(v.res.related).map(x => x.id), v.kind === "one" ? null : v.res.groups);
  const f = document.querySelector("#evsheet .ins-next a"); if (f) f.focus();
}, true);
/* ---------- Your questions (site 2.4, 15 November 2026). The senior author: "Ask us to check it" opened an email form, "a very
   slow and non flexible way"; and, of a site where requests are answered by other people: it shows "requests solved" at the
   top of the page, "the same should happen for the questions the user raised ... the site should be able to remember 2 or
   more questions".
   - One tap. The question is put on a short list kept on this device (localStorage, at most 20), and, where the site has
     its small store switched on (GET api/ask answers ok: site/worker/_worker.js on Cloudflare Pages), it is sent there:
     the question's words, the drug page it was asked on and the site version. No name, no address, no cookie; nothing else
     that was typed is ever sent. Where the store is not switched on, the email form opens with the question, as before.
   - The start page shows the list under the search box: "We are checking" for each question still open, and, in green,
     "Answered" as soon as a later version of the site has a best match for it (Insight asks itself the kept questions once
     per new version, on this device). Reading an answered question, or the cross beside any, takes it off the list.
   Reading the list back is how a person without an account, an address or a cookie hears that their question was answered. ---------- */
const ASK_KEY = "pk-asked", ASK_API = "api/ask";
// (2.6) the site publishes itself, with new answers, without a new version number: a kept question is asked again once per
// BUILD (the build's own stamp), and while a question waits an open page looks every few minutes whether a newer site exists
// (a small fixed file, data/build.json: nothing about the reader is sent) and then offers to load it
const ASK_BUILD = typeof SITE_BUILD === "string" ? SITE_BUILD : SITE_VERSION, ASK_LOOK = 5 * 60 * 1000;
let ASK_NEWER = false;
// what the page says once a question is sent. The promise of an answer within the hour is made only by a site whose half-hourly
// run is on and has been seen to keep it (AUTO_LOOP, from data/auto/lane/policy.json at build time); until then: the plain truth
const ASK_SENT = (typeof AUTO_LOOP !== "undefined" && AUTO_LOOP)
  ? "Sent. Our system starts on it within half an hour. If it finds research it can read, the answer is usually here within the hour: your question then turns green under “Your questions” on the start page."
  : "Sent. Our own answer usually takes a day or two; some wait for a person. It turns green under “Your questions” on the start page.";
function askedLook() {   // one look: is the site on the server newer than this page?
  if (ASK_NEWER) return Promise.resolve(true);
  return fetch("data/build.json", { cache: "no-store" }).then(r => (r.ok ? r.json() : null)).then(j => { if (j && typeof j.build === "string" && j.build !== ASK_BUILD) { ASK_NEWER = true; if (askedWatch.t) clearInterval(askedWatch.t); askedBox(); } return ASK_NEWER; }).catch(() => false);
}
function askedWatch() {
  if (askedWatch.on || ASK_NEWER || !askedList().some(it => it.st === "wait")) return; askedWatch.on = true;
  askedWatch.t = setInterval(() => { if (!document.hidden && askedList().some(it => it.st === "wait")) askedLook(); }, ASK_LOOK);
  // and when the reader comes back to the tab after a while
  document.addEventListener("visibilitychange", () => { if (!document.hidden && Date.now() - (askedWatch.at || 0) > ASK_LOOK && askedList().some(it => it.st === "wait")) { askedWatch.at = Date.now(); askedLook(); } });
}
// (2.16.1) FIND_ON: the site's server can look up published research (POST api/find). Learned by the same one question to the server
let FIND_ON = (() => { try { return sessionStorage.getItem("pk-find-on") === "1"; } catch (e) { return false; } })();
// (2.17) AUTO_SRV: the server takes a question the page sends by itself (POST api/ask with a: 1), and keeps it apart
let AUTO_SRV = (() => { try { return sessionStorage.getItem("pk-auto-on") === "1"; } catch (e) { return false; } })();
// (2.18) QUICK_ON: the server can write an answer within seconds (POST api/answer: a language model is bound to it)
let QUICK_ON = (() => { try { return sessionStorage.getItem("pk-quick-on") === "1"; } catch (e) { return false; } })();
let ASK_ON = (() => { try { const x = sessionStorage.getItem("pk-ask-on"); if (sessionStorage.getItem("pk-find-on") == null || sessionStorage.getItem("pk-auto-on") == null) return null; return x === "1" ? true : x === "0" ? false : null; } catch (e) { return null; } })();
// The reader's own switch for what the page does by itself (looking research up; sending a question we have no answer to): on, unless switched
// off on this device (About us, Privacy; or "Don't send mine" on the notice). These stand here, above the first drawing of the reader's list.
const AUTO_OFF = "pk-auto";
function autoOn() { try { return localStorage.getItem(AUTO_OFF) !== "0"; } catch (e) { return true; } }
function autoSendOn() { return ASK_ON === true && AUTO_SRV && autoOn(); }
// (2.18) The server is asked once on every opening of the page, not once per tab: what it can do changes with a publishing (a model bound to it), and a
// tab left open must not go on believing yesterday's answer. Until its reply is in, the page starts from what the tab learned before.
function askProbe() {
  if (askProbe.p) return askProbe.p;
  return (askProbe.p = fetch(ASK_API, { headers: { accept: "application/json" } }).then(r => r.ok ? r.json() : null).then(j => { FIND_ON = !!(j && j.find === true); AUTO_SRV = !!(j && j.auto === true); QUICK_ON = !!(j && j.quick === true); return !!(j && j.ok === true); }, () => { FIND_ON = false; AUTO_SRV = false; QUICK_ON = false; return false; })
    .then(on => { const was = ASK_ON; ASK_ON = on; try { sessionStorage.setItem("pk-ask-on", on ? "1" : "0"); sessionStorage.setItem("pk-find-on", FIND_ON ? "1" : "0"); sessionStorage.setItem("pk-auto-on", AUTO_SRV ? "1" : "0"); sessionStorage.setItem("pk-quick-on", QUICK_ON ? "1" : "0"); } catch (e) { /* this page only */ }
      if (was !== on && typeof askedBox === "function") askedBox(); return on; }));
}
function askedList() { try { const x = JSON.parse(localStorage.getItem(ASK_KEY) || "[]"); return Array.isArray(x) ? x.filter(it => it && typeof it.q === "string" && it.k) : []; } catch (e) { return []; } }
function askedSave(list) { try { localStorage.setItem(ASK_KEY, JSON.stringify(list.slice(-20))); } catch (e) { /* this visit only */ } }
function askedAdd(q, drug) {
  const text = insClean(q).slice(0, 200), k = text.toLowerCase(); if (k.length < 3) return null;
  const list = askedList(); let it = list.find(x => x.k === k);
  if (!it) { it = { k, q: text, d: drug || "", t: Date.now(), cv: ASK_BUILD, st: "wait", sent: 0 }; list.push(it); askedSave(list); }
  return it;
}
const askedSentHas = q => { const k = insClean(q).slice(0, 200).toLowerCase(); return askedList().some(it => it.k === k && it.sent); };
function askedSet(k, patch) { const list = askedList(), it = list.find(x => x.k === k); if (!it) return; Object.assign(it, patch); askedSave(list); }
function askedDrop(k) { askedSave(askedList().filter(x => x.k !== k)); }
// (2.17) a question the reader took off the list is not put back by the page in this visit (kept until the tab closes: its key only)
function askedGoneSet() { try { const a = JSON.parse(sessionStorage.getItem("pk-asked-x") || "[]"); return new Set(Array.isArray(a) ? a : []); } catch (e) { return askedGoneSet.mem || (askedGoneSet.mem = new Set()); } }
function askedGoneAdd(k) { const s = askedGoneSet(); s.add(String(k)); try { sessionStorage.setItem("pk-asked-x", JSON.stringify([...s].slice(-40))); } catch (e) { askedGoneSet.mem = s; } }
const askedGone = q => askedGoneSet().has(insClean(q).slice(0, 200).toLowerCase());
// a question sent by the page a moment ago that was only the beginning of this one ("does kanna help" before "does kanna help with anxiety") leaves the list
function askedTidy(k) { const now = Date.now(), list = askedList(), keep = list.filter(x => x.k === k || !(x.auto && !x.w && now - (x.t || 0) < 180000 && k.length > x.k.length && k.indexOf(x.k) === 0)); if (keep.length !== list.length) askedSave(keep); }
function askedBox() {
  const box = document.getElementById("home-asked"); if (!box) return;
  { const all = askedList(), keep = all.filter(it => !it.u && !it.gone); if (keep.length !== all.length) askedSave(keep); }   // (2.15.2) rows kept by an older page as "Not a whole question" leave the list
  const list = askedList().filter(it => it.st !== "ans" || it.h || claimById[it.id] || isAuto(it.id));
  if (!list.length) { box.hidden = true; box.innerHTML = ""; return; }
  const x = it => '<button type="button" class="aq-x" data-asked-x="' + esc(it.k) + '" aria-label="Take this question off the list">' + icon("x") + "</button>";
  const byNew = (a, b) => (b.t || 0) - (a.t || 0);   // (2.9.2, the senior author) the newest first, the oldest last
  // (2.9; the senior author, 17 November, of his two sent questions: "i cannot click on them to see the answer") a question
  // that waits can be opened too: it is asked again in the box above, which shows what the site has on it so far
  // (2.15.2) how long ago, and for a question on our list what our system has done with it so far (AUTO_STATE, from the lane's own record)
  const ago = it => { const h = (Date.now() - (it.t || Date.now())) / 3600000; return h < 1 ? "less than an hour ago" : h < 36 ? Math.round(h) + (Math.round(h) === 1 ? " hour ago" : " hours ago") : Math.round(h / 24) + " days ago"; };
  const state = it => { const s = it.w && typeof AUTO_STATE !== "undefined" ? AUTO_STATE[it.w] : ""; return s === "person" ? "Written. A person has to check it first" : s === "nosource" ? "Searched. Nothing we can read is published on it yet" : s === "tried" ? "Tried. No answer passed our checks yet" : s === "new" ? "In line. Not tried yet" : ""; };
  const look = (it, k) => '<li class="aq wait' + (it.w ? " onlist" : "") + '"><button type="button" class="aq-a aq-look" data-asked-look="' + esc(it.k) + '"><span class="aq-k">' + icon("clock") + (state(it) || k) + (it.sent ? '<span class="aq-ago"> · ' + (it.kept ? "asked " : "sent ") + ago(it) + "</span>" : "") + '</span><span class="aq-q">' + esc(it.q) +
    '</span><span class="aq-go">See what we have so far ' + icon("arrow") + "</span></button>" + x(it) + "</li>";
  const row = it => it.st === "ans"
    ? '<li class="aq ans"><a class="aq-a" href="' + esc(it.h ? it.h : isAuto(it.id) ? "#auto/q-" + it.id : answerAddr(it.id, it.p)) + '"' + (it.h ? "" : ' data-sheet="' + esc(it.id) + '"') + ' data-asked-open="' + esc(it.k) + '"><span class="aq-k">' + icon("check") + 'Answered</span><span class="aq-q">' + esc(it.q) + '</span><span class="aq-go">Read the answer ' + icon("arrow") + "</span></a>" + x(it) + "</li>"
    : it.w ? look(it, "On our list")
    : it.sent ? look(it, "Sent. We are checking")
    : '<li class="aq unsent"><span class="aq-a"><span class="aq-k">Not sent</span><span class="aq-q">' + esc(it.q) + '</span><button type="button" class="aq-send" data-asked-send="' + esc(it.k) + '">Send it to us</button></span>' + x(it) + "</li>";
  // (the senior author, 15 November, seeing his own unsent question listed: "does the site know what the user asked ... even if he
  // didn't send the email? ... the user should be informed": the list says where it is kept, and each row whether it was sent)
  const newer = ASK_NEWER ? '<p class="aq-new" role="status">The site has new answers. <button type="button" class="aq-reload" data-asked-reload>Load them</button> to see whether yours is among them.</p>' : "";
  box.innerHTML = '<h2 class="aq-h">Your questions</h2><p class="aq-note">' + (autoSendOn() ? "This list is kept on this device only. A question we had no answer to is sent to our system by itself (About us, Privacy switches that off). It works on them by itself, the ones people sent first: most take a day or two, and some then wait for a person. A question turns green here when it is answered."
    : "This list is kept on this device only. We see a question only if you send it. Our system works on sent questions by itself, the ones people sent first: most take a day or two, and some then wait for a person. A question turns green here when it is answered.") + "</p>" + newer + '<ul class="aq-l">' + list.filter(it => it.st === "ans").sort(byNew).concat(list.filter(it => it.st !== "ans").sort(byNew)).map(row).join("") + "</ul>";
  box.hidden = false;
  askedCheckSoon(); askedWatch();
}
// a kept question is asked again once per new version of the site: a best match now means it has been answered
async function askedCheck() {
  if (INS.state !== "ready") return;
  const list = askedList(); let changed = false;
  for (const it of list) {
    if (it.st !== "wait" || it.cv === ASK_BUILD) continue;
    try { const res = await insRank(it.q, { drug: it.d && subBySlug[it.d] ? it.d : null });
      // (2.10.1) answered by a checked answer, or by a place on the site that is the answer ("are drugs legal in greece": Greece on the page of treaties)
      const rt = res.note ? null : res.routes.find(r => r.kind !== "mix" && !r.loose);
      if (res.best.length) { it.st = "ans"; it.id = res.best[0].id; it.p = res.best[0].page; }
      else if (rt) { it.st = "ans"; it.h = rt.href; }
      else if (res.want && !it.w && it.sent) it.w = res.want.id;   // (2.9) sent, not answered yet, and now on our list: its row says so
      else if (!it.w && it.sent) { const pg = res.routes.find(r => r.started), sh = pg && typeof autoShell === "function" ? autoShell(pg.started) : null;   // (2.15.2) about a drug whose page the system started: the question listed on that page is the one it waits for
        if (sh && sh.asked && sh.asked.length) it.w = sh.asked[0].id; }
      // (2.15.2; the senior author, of "do gay people" on his list as "Not a whole question": "why are non drug questions included... bad
      // design") a beginning, or a question that is not about drugs, is not a question the site can work on: it leaves the list. One with
      // a word we do not know stays (it may be the name of a drug the system has yet to learn).
      if (res.note === "unfinished" || (res.note === "other" && !res.stranger)) it.gone = 1;
      delete it.u; it.cv = ASK_BUILD; changed = true; } catch (e) { /* asked again on the next visit */ }
  }
  if (changed) { askedSave(list.filter(it => !it.gone)); askedBox(); }
}
function askedCheckSoon() {
  if (askedCheckSoon.done || !askedList().some(it => it.st === "wait" && it.cv !== ASK_BUILD)) return;
  askedCheckSoon.done = true;
  const go = () => { if (INS.state === "ready") askedCheck(); else if (!insSaver()) insightLoad().then(ok => { if (ok) askedCheck(); }); };
  if (window.requestIdleCallback) requestIdleCallback(go, { timeout: 4000 }); else setTimeout(go, 1500);
}
document.addEventListener("click", async e => {
  if (!e.target.closest) return;
  if (e.target.closest("button[data-asked-reload]")) { location.reload(); return; }
  const xb = e.target.closest("button[data-asked-x]"); if (xb) { askedGoneAdd(xb.dataset.askedX); askedDrop(xb.dataset.askedX); askedBox(); const h = document.querySelector("#home-asked .aq-h") || document.getElementById("search"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } return; }
  const op = e.target.closest("a[data-asked-open]"); if (op) { askedDrop(op.dataset.askedOpen); return; }   // read: it leaves the list (the sheet opens by its data-sheet)
  // (2.10) a thing to try under the capsule: put in the box and asked
  const tr = e.target.closest("button[data-try]");
  if (tr) { e.preventDefault(); const s = document.getElementById("search"); if (!s) return; s.value = tr.dataset.try;
    setTimeout(() => { s.focus({ preventScroll: true }); runSearch(s.value); }, 0); return; }
  // (2.9) a question that waits: asked again in the box, which shows what the site has on it so far
  const lk = e.target.closest("button[data-asked-look]");
  if (lk) { e.preventDefault(); const it = askedList().find(x => x.k === lk.dataset.askedLook), s = document.getElementById("search"); if (!it || !s) return;
    s.value = it.q; if (s.scrollIntoView) s.scrollIntoView({ block: "center" });
    setTimeout(() => { s.focus({ preventScroll: true }); runSearch(it.q); }, 0); return; }   // after this click has run its course (the page closes the results on a click outside them)
  // a question in the list that was not sent: one tap sends it where the site can send; elsewhere the email form opens with it
  const sb = e.target.closest("button[data-asked-send]");
  if (sb) { e.preventDefault(); const it = askedList().find(x => x.k === sb.dataset.askedSend); if (!it) return; sb.disabled = true;
    if (await askProbe()) { let ok = false;
      try { const r = await fetch(ASK_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ q: it.q, d: it.d, v: SITE_VERSION }) }); ok = r.ok; } catch (err) { ok = false; }
      if (ok) { askedSet(it.k, { sent: 1 }); askedBox(); return; } }
    sb.disabled = false; openFeedback("feedback", location.hash, it.q); return; }
  // 2.5: a question on our list: "Tell me when it is answered" keeps the LISTED question (never the words typed) in the
  // reader's own list; it turns green when a later version of the site answers it
  const wk = e.target.closest("button[data-want-keep]");
  if (wk) { e.preventDefault(); e.stopPropagation(); const id = wk.dataset.wantKeep, q = wantQ(id) || autoAskedQ(id); if (!q) return;   // (2.12: a question listed on a page our system started is kept the same way)
    const it = askedAdd(q, ""); if (it) askedSet(it.k, { w: id, sent: 1, kept: 1 });   // (kept: a question of our list the reader asked to be told about; no words of theirs were sent)
    if (wk.closest("#view-wanted, [data-count]")) wantCount(id);   // counted where the page says so (the list's own page; a card that carries the line)
    const said = document.createElement("p"); said.className = "ask-said"; said.setAttribute("role", "status"); said.textContent = "We will tell you on this device. It is under “Your questions” on the start page."; wk.replaceWith(said);
    askedBox(); return; }
  const b = e.target.closest("button[data-ask]"); if (!b || b.disabled) return;
  e.preventDefault(); e.stopPropagation();
  const q = b.dataset.ask, it = askedAdd(q, insCtx().drug || ""); if (!it) return;
  const note = b.parentElement && b.parentElement.querySelector(".ask-note");
  const say = t => { const p = document.createElement("p"); p.className = "ask-said"; p.setAttribute("role", "status"); p.textContent = t; if (note) note.remove(); b.replaceWith(p); };
  b.disabled = true;
  const on = await askProbe();
  if (it.sent) { say("Already sent. It is under “Your questions” on the start page."); return; }
  if (on) {
    let ok = false;
    try { const r = await fetch(ASK_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ q: it.q, d: it.d, v: SITE_VERSION }) }); ok = r.ok; } catch (err) { ok = false; }
    if (ok) { askedSet(it.k, { sent: 1 }); say(ASK_SENT); askedBox(); return; }   // (the published research stands under it already: insAuto)
  }
  // the page cannot send it (the store is not switched on, or the connection failed): kept on this device, and the email form opens with it
  say("Not sent yet. It is kept on this device only, under “Your questions”. To send it to us, press Send by email in the form.");
  askedBox(); if (EV.open) closeEvidence(); openFeedback("feedback", location.hash, q);
}, true);
// The start page is drawn before this part of the script has run (the list's own names do not exist yet at that moment),
// so the list of kept questions is drawn here, once: without this line it was missing after every reload.
if (typeof document !== "undefined") askedBox();
/* Published research, at once (site 2.16; the senior author, 17 November 2026: "a big problem is that answers take too long to get responses and
   people are used to get responses instantly"; "it feels stupid and slow our ai should be able to find answers almost instantly").
   An answer of ours takes a day or two: papers have to be found, read and checked. But what research has been published on a question can be
   looked up in seconds. The page asks this site's own server for the papers on its drug and its key words in Europe PMC, the open index of
   medical research, and shows them: title, kind of paper, year, journal, whether it is free to read, and its link (2.16.0: when a reader sent
   the question; since 2.16.1 by itself, whenever we have no answer of ours: insAuto, below). Said plainly with them: we have not read these
   yet, and a title is not a finding. What leaves the device for this: the drug's names and up to five plain key words, never the sentence.
   Not looked up: a question about dying, overdose, amounts, pregnancy, children or an emergency, and a question that names no drug. */
const FIND_API = "api/find";
const FIND_STOP = new Set(("what when where which while with would could should does doing done have having from that this these those there their them they your yours about into than then also just very much many more most some such only over under after before because being been were will shall might must cant dont long take takes taking took taken using used uses make makes made feel feels feeling felt people person someone anyone thing things really actually good bad safe okay fine true real ever still even like know want need tell does help helps helped work works worked " +
  // (2.18.2) words that stand in nearly every paper's summary, or say nothing a search can use
  "cause causes caused causing study studies studying studied time times term same different between kind kinds type types happen happens happened give gives given get gets getting mean means compared versus " +
  // (2.19, after the first trial with the real index of papers) words for what a drug does to something, which say nothing about WHAT: every key word must now stand in a paper
  "improve improves improved improving lower lowers lowered raise raises raised increase increases increased decrease decreases decreased reduce reduces reduced change changes changed changing affect affects affected " +
  "damage damages damaged damaging loss lose loses losing lost hurt hurts harm harms problem problems issue issues worse").split(" "));
// an everyday word and the word papers use for it: the search asks for both
const FIND_SAY = { high: "psychoactive", addictive: "addiction", addicted: "addiction", addicting: "addiction", dangerous: "adverse", harmful: "adverse", legal: "legal", illegal: "legal", anxious: "anxiety", depressed: "depression", sleepy: "sleep", effects: "effects", effect: "effects",
  hungry: "appetite", hunger: "appetite", munchies: "appetite", nosebleed: "epistaxis", nosebleeds: "epistaxis", concentrate: "attention", concentration: "attention", focus: "attention", focused: "attention", smarter: "cognitive", smart: "cognitive", tired: "fatigue", paranoid: "paranoia",
  horny: "sexual", sex: "sexual", teeth: "dental", tooth: "dental", kidneys: "renal", kidney: "renal", lungs: "pulmonary", lung: "pulmonary", heart: "cardiac", liver: "hepatic", forget: "memory", forgetful: "memory", remember: "memory", shaky: "tremor", shakes: "tremor", sweat: "sweating", sweaty: "sweating", puke: "vomiting", vomit: "vomiting", throwing: "vomiting", comedown: "comedown", hangover: "hangover",
  eye: "eye", eyes: "eye", ear: "ear", ears: "ear", gut: "gut", fat: "fat", ocd: "ocd", ibs: "ibs", hiv: "hiv", eat: "appetite", eating: "appetite" };   // (2.19: short words that are the very thing asked about)
const FIND_HELD = /\b(pregnan\w*|breast-?feed\w*|child|children|kids?|bab(y|ies)|infants?|teen\w*|minors?|suicid\w*|kill\w*|die[sd]?|dying|deaths?|dead|deadly|overdos\w*|lethal|fatal\w*|dos(e|es|age|ing)|mg|milligrams?|grams?|micrograms?)\b/i;
/* What is looked up for a result: the names of its drug and up to five key words; null when nothing is to be looked up.
   (2.18.2, after looking at what twenty real questions gave) The names: the name as the reader wrote it, when it is a name of its own and not an
   everyday word ("xanax", on the page about benzodiazepines; "weed", "acid", "speed", "ice" are everyday words and would find every paper that
   holds them); then the page's names, each on its own ("GHB / GBL" is two names); a started page's names; a word we do not know as a drug; and, for
   a question about drugs that names none we know, the first word that is no everyday word, nor one made from one ("addictive", "migraines").
   The key words: from the question with the drugs' names taken out by whatever name was used (insMask: "magic" of "magic mushrooms" is no key
   word), without the words that stand in every summary; an everyday word goes with the word papers use for it ("hungry": appetite). */
function insFindTerms(res) {
  if (!res || res.emergency || FIND_HELD.test(res.q || "") || (res.routes || []).some(r => r.kind === "help" || r.kind === "dose" || r.kind === "mix")) return null;
  const names = [], add = s => { s = String(s || "").toLowerCase().replace(/[^a-z0-9 ,.'+()-]/g, " ").replace(/\s+/g, " ").trim(); if (s.length >= 3 && !names.includes(s)) names.push(s); };
  const text = String(res.core || res.q || "").toLowerCase();
  if ((res.groups || []).length && INS.nameRe) { INS.nameRe.lastIndex = 0; let m; while ((m = INS.nameRe.exec(text))) { const a = String(m[1] || "").toLowerCase(); if (a.length >= 4 && !/\s/.test(a) && !INS.vocab.has(a)) add(a); if (m.index === INS.nameRe.lastIndex) INS.nameRe.lastIndex++; } INS.nameRe.lastIndex = 0; }
  // (2.19) a page that stands for several things ("Cannabis (THC, CBD)"): the ones the reader named, where they named any ("does cbd help with sleep" is
  // about CBD); all of them where they named none ("weed")
  for (const g of res.groups || []) for (const slug of g.slice(0, 2)) { const s = subBySlug[slug]; if (!s) continue;
    const parts = String(s.name || "").split(/[(),/]| and | or /).map(x => x.toLowerCase().replace(/[^a-z0-9 ,.'+()-]/g, " ").replace(/\s+/g, " ").trim()).filter(x => x.length >= 3);
    const typed = parts.filter(x => (" " + text.replace(/[^a-z0-9+-]+/g, " ") + " ").includes(" " + x + " "));
    (typed.length ? typed : parts).forEach(add); }
  const pg = (res.routes || []).find(r => r.started), sh = pg && typeof autoShell === "function" ? autoShell(pg.started) : null;
  if (sh) { add(sh.name); (sh.science || []).forEach(x => add(x.name)); }
  if (!names.length && res.stranger) add(res.stranger);
  // a question about drugs that names none we know ("is tianeptine addictive"): the first word that is no everyday word is most likely the drug's name
  if (!names.length && res.note !== "other") { const known = w => INS.vocab.has(w) || FIND_STOP.has(w) || !!FIND_SAY[w],
      plain = w => known(w) || ["ies", "es", "s", "ed", "d", "ing", "ly", "ive", "al", "er", "est", "y", "ness", "ful"].some(suf => w.length > suf.length + 2 && w.endsWith(suf) && (known(w.slice(0, -suf.length)) || known(w.slice(0, -suf.length) + "e") || (suf === "ies" && known(w.slice(0, -3) + "y")) || (suf === "ive" && known(w.slice(0, -3) + "ion"))));
    const cand = (text.match(/[a-z]{5,}/g) || []).filter(w => !plain(w)); if (cand.length) add(cand[0]); }
  if (!names.length) return null;
  const inName = new Set(names.join(" ").split(/[^a-z0-9]+/)), words = [], masked = (typeof insMask === "function" ? String(insMask(text)) : text).toLowerCase();
  for (const w0 of masked.match(/[a-z]{3,}/g) || []) { const say = FIND_SAY[w0];
    if ((w0.length < 4 && !say) || FIND_STOP.has(w0) || inName.has(w0) || INS.nameOf.has(w0)) continue;
    const e = say && say !== w0 ? say + "|" + w0 : w0;   // (2.19) the word papers use and the everyday word are one thing asked for, in two ways: one entry
    if (!words.includes(e) && !words.includes(say || w0) && words.length < 5) words.push(e); }
  return { names: names.slice(0, 6), words };
}
function insFoundHtml(d) {
  if (!d || !d.ok || d.held) return "";
  if (!d.papers || !d.papers.length) return '<p class="ins-found-n">We looked in Europe PMC, an open index of medical research, just now: nothing was found on these words.</p>';
  return '<p class="ins-found-h">Published research on this, found just now</p><ul class="ins-found-l">' + d.papers.map(p => { const href = p.doi ? "https://doi.org/" + p.doi : "https://europepmc.org/article/MED/" + p.pmid;
    return '<li><a href="' + esc(href) + '" target="_blank" rel="noopener">' + esc(p.t) + '</a><span class="m">' + esc([p.kind, p.y, p.j, p.oa ? "free to read" : ""].filter(Boolean).join(" \u00B7 ")) + "</span></li>"; }).join("") +
    '</ul><p class="ins-found-n">From Europe PMC, an open index of medical research. We have not read these yet, and a title is not a finding.</p>';
}
/* (2.16.1, 17 November 2026, 23:19 and 23:20 Athens. The senior author, of the list that came only after he had pressed "Send": "it should
   automatically search the user should not even have to click it"; and, typing a question he had already sent: "now when i type it again the
   sites do not show".) By itself, every time. Whenever Insight has no answer of ours to a whole question about a drug (not answered, on our
   list, or a word we do not know as a drug), in the results and in the sheet, sent or not, the page looks the published research up and puts
   it under the line that says so. In the results it waits a moment (FIND_WAIT) so that nothing is asked while the reader is still typing; in
   the sheet (Enter) at once. What it found is kept for this visit (FIND_MEM): the same question is not asked twice.
   The reader can switch this off (About us, Privacy: AUTO_OFF); then one quiet button looks it up on a tap. */
const FIND_WAIT = 700, FIND_MEM = new Map();
function insFindGet(terms) {
  const key = JSON.stringify(terms); let m = FIND_MEM.get(key); if (m) return m.p;
  m = { d: undefined };
  m.p = fetch(FIND_API, { method: "POST", headers: { "content-type": "application/json" }, body: key }).then(r => (r.ok ? r.json() : null)).catch(() => null).then(d => { m.d = d; if (!d) FIND_MEM.delete(key); return d; });
  FIND_MEM.set(key, m); if (FIND_MEM.size > 40) FIND_MEM.delete(FIND_MEM.keys().next().value);
  return m.p;
}
// what is looked up for a result: nothing when we have an answer of ours, or when the question is not one a drug's research can answer
function insFindWanted(res) {
  if (!res || (res.best && res.best.length) || !(res.note === "none" || res.note === "want" || (res.note === "other" && res.stranger))) return null;
  return insFindTerms(res);
}
function insAuto(root, res, now) {
  clearTimeout(INS.findT); clearTimeout(INS.sendT);
  const after = root && res ? root.querySelector(".sr-fit-none, .ins-none") : null; if (!after) return;
  clearTimeout(INS.quickT);
  askProbe().then(() => { if (!after.isConnected) return; const found = insAutoFind(after, res, now); insAutoSend(after, res, now, found); insAutoQuick(after, res, now); });
}
/* (site 2.18, 18 November 2026. The senior author, 17 November: "people are used to get responses instantly. We have to make an ai which is able to do that
   for questions it does not know"; "we have to make instant as good as getting answers from a very good claude api. whatever it takes".)
   What the papers say, within seconds. Where the site's server has a language model bound to it (QUICK_ON), a question that is sent by itself also gets,
   at once, what up to three of the papers found say on it IN THE PAPERS' OWN WORDS (at most 15 from each summary, with the paper's kind, year, journal and
   link): the model chooses the sentence, the server's code cuts the words out and decides what may be shown (site/worker/_worker.js, iaCheck). Since 2.19
   the model's own plain sentence is not shown: tried with the real model, about one in three said more than its paper; it is shown only once an exam
   allows it (the server then sends it as "t", and it stands above the paper's words). The block stands right under the line that says we have no answer
   of ours, above the list of papers, under its own label: chosen by our system from the papers' summaries, the papers themselves not read, no person has
   checked the choice. It is never called an answer of ours and nothing of it is kept on the page. Asked for a moment after the papers (QUICK_WAIT; at once
   on Enter), once per question per visit.
   Not asked for: a question about dying, overdose, amounts, pregnancy, children (insFindTerms gives nothing for these); anything, when the reader has
   switched the page's own doing off (then one quiet button asks for it). */
const QUICK_API = "api/answer", QUICK_WAIT = 1200, QUICK_MEM = new Map();
function insQuickGet(body) {
  const key = JSON.stringify(body); let m = QUICK_MEM.get(key); if (m) return m.p;
  m = { d: undefined };
  m.p = fetch(QUICK_API, { method: "POST", headers: { "content-type": "application/json" }, body: key }).then(r => (r.ok ? r.json() : null)).catch(() => null).then(d => { m.d = d; if (!d) QUICK_MEM.delete(key); return d; });
  QUICK_MEM.set(key, m); if (QUICK_MEM.size > 40) QUICK_MEM.delete(QUICK_MEM.keys().next().value);
  return m.p;
}
function insQuickHtml(d) {
  const L = d && d.ok && d.answer && Array.isArray(d.answer.lines) ? d.answer.lines.filter(l => l && typeof l.quote === "string" && l.quote && (l.doi || l.pmid)).slice(0, 3) : []; if (!L.length) return "";
  let when = "just now"; if (d.again && d.answer.at) { const t = new Date(d.answer.at); if (!isNaN(t)) when = "on " + t.getUTCDate() + " " + ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][t.getUTCMonth()]; }
  // (2.19) What is shown is the paper's own words; a plain sentence of the system's stands above them only where the server sends one (it sends none
  // until an exam of such sentences allows it: site/worker/_worker.js, IA.plain). "In animals or cells" is the server's own reading of the sentence
  // and its summary; where a summary covers animals and people and the sentence does not say which, the line says so.
  const wrote = L.some(l => typeof l.t === "string" && l.t);
  return '<p class="ins-quick-h">' + (wrote ? "In short, from the papers’ own summaries" : "What the papers say, in their own words") + '</p><ul class="ins-quick-l">' + L.map(l => { const href = l.doi ? "https://doi.org/" + l.doi : "https://europepmc.org/article/MED/" + l.pmid;
    const paper = '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + esc([l.kind, l.y, l.j].filter(Boolean).join(" \u00B7 ")) + "</a>" + (l.animal ? '<span class="qk-an"> \u00B7 in animals or cells, not in people</span>' : l.mixed ? '<span class="qk-an"> \u00B7 its summary covers work in animals or cells too</span>' : "");
    return typeof l.t === "string" && l.t ? '<li><p class="qk-t">' + esc(l.t) + '</p><p class="qk-m">' + paper + '<span class="qk-q">The paper’s own words: \u201C' + esc(l.quote) + "\u201D</span></p></li>"
      : '<li><p class="qk-w">\u201C' + esc(l.quote) + '\u201D</p><p class="qk-m">' + paper + "</p></li>"; }).join("") +
    '</ul><p class="ins-quick-n">' + (wrote ? "Written " + esc(when) + " by our system from the summaries of these papers. It has not read the papers themselves, and no person has checked it."
      : "Chosen " + esc(when) + " by our system from the summaries of these papers: the words are the papers’ own. It has not read the papers themselves, and no person has checked its choice.") + " Our own answer follows when it is ready.</p>";
}
function insAutoQuick(after, res, now) {
  if (!QUICK_ON || ASK_ON !== true || res.note !== "none" || (res.best && res.best.length)) return;
  const terms = insFindTerms(res); if (!terms) return;
  const body = { q: res.q, names: terms.names, words: terms.words };
  const box = document.createElement("div"); box.className = "ins-quick"; box.setAttribute("aria-live", "polite");
  box.addEventListener("click", e => e.stopPropagation());
  const put = () => { if (!box.isConnected && after.isConnected) after.insertAdjacentElement("afterend", box); };   // (right under the line: above the papers)
  const draw = d => { const html = insQuickHtml(d); if (!html) { box.remove(); return; } put(); box.innerHTML = html; };
  const have = QUICK_MEM.get(JSON.stringify(body));
  if (have && have.d) { draw(have.d); return; }
  const go = () => { if (!after.isConnected) return; put(); box.innerHTML = '<p class="ins-quick-n ins-quick-w">Looking through the papers’ summaries for what they say on it\u2026</p>'; insQuickGet(body).then(d => { if (after.isConnected) draw(d); else box.remove(); }); };
  if (!autoOn()) { put(); box.innerHTML = '<p class="ins-quick-n"><button type="button" class="linklike" data-quick-now>Show what the papers’ summaries say on it</button></p>'; box.querySelector("button").addEventListener("click", e => { e.preventDefault(); go(); }); return; }
  if (askedGone(res.q)) return;
  if (now) go(); else INS.quickT = setTimeout(() => { const s = document.getElementById("search"), b = document.getElementById("search-results"); if (s && b && !b.hidden && insClean(s.value) === res.q) go(); }, QUICK_WAIT);
}
// the published research under the line; resolves with what was found (null when nothing is looked up)
function insAutoFind(after, res, now) {
  const terms = FIND_ON ? insFindWanted(res) : null; if (!terms) return Promise.resolve(null);
  const box = document.createElement("div"); box.className = "ins-found"; box.setAttribute("aria-live", "polite");
  box.addEventListener("click", e => e.stopPropagation());   // a paper opens in its own tab: the question and its results stay as they are
  const put = () => { if (box.isConnected || !after.isConnected) return; const q = after.nextElementSibling; (q && q.classList.contains("ins-quick") ? q : after).insertAdjacentElement("afterend", box); };   // (under the answer within seconds, when that is there)
  const draw = d => { const html = insFoundHtml(d); if (!html) { box.remove(); return; } put(); box.innerHTML = html; };
  const have = FIND_MEM.get(JSON.stringify(terms));
  if (have && have.d) { draw(have.d); return Promise.resolve(have.d); }
  const go = () => { if (!after.isConnected) return Promise.resolve(null); put(); box.innerHTML = '<p class="ins-found-n">Looking for published research on it\u2026</p>'; return insFindGet(terms).then(d => { if (after.isConnected) draw(d); return d; }); };
  if (!autoOn()) { put(); box.innerHTML = '<p class="ins-found-n"><button type="button" class="linklike" data-find-now>Look up published research on this</button></p>'; box.querySelector("button").addEventListener("click", e => { e.preventDefault(); go(); }); return Promise.resolve(null); }
  if (now) return go();
  return new Promise(ok => { INS.findT = setTimeout(() => ok(go()), FIND_WAIT); });
}
/* (site 2.17, 18 November 2026. The senior author, 17 November, 23:38, of a question the site could not answer: "the ai should understand what i mean!
   it should send the question immediately in every instance and the user should be notified".) The question, sent by itself. When Insight has no
   answer of ours to a whole question about a drug, the page sends it to our system so that it gets answered, without a button, and says so in the
   same place: "Sent to our system, so that it gets answered. It turns green under 'Your questions' on the start page when it is." The question is
   put on the reader's own list like one they sent themselves.
   - When: in the results once the question has stood unchanged for AUTO_WAIT (so that a sentence still being typed is not sent piece by piece);
     on Enter (the sheet) at once. A beginning sent a moment before the whole question leaves the reader's list (askedTidy).
   - What: exactly what "Ask us to check it" sends (the question's words, the drug page, the site's version), marked as sent by the page (a: 1).
     The server keeps such a question apart and its words are never written into the public repository (site/worker/_worker.js; docs/AUTOMATION.md,
     decision 31). No name, no address, no cookie.
   - Not sent by itself: a beginning, a question that is not about drugs, what the site does not answer; a question the reader took off their list
     in this visit; anything, once the reader has switched it off (the notice's own "Don't send mine", or About us, Privacy).
   - A word we do not know as a drug ("We do not know 'x' as a drug"): sent by itself only when research is published under that name (the lookup
     above found papers): then it is most likely a drug we have yet to learn, not a slip of the keyboard.
   - A question like one on our list: nothing of the reader's is sent (the device counts the listed question by its number, as before); the LISTED
     question is put on the reader's list by itself, so that they are told when it is answered. */
const AUTO_WAIT = 2500, AUTO_SENT = "Sent to our system, so that it gets answered. It turns green under “Your questions” on the start page when it is.";
const insAutoSaidHtml = t => '<span class="ask-said ask-auto-said" role="status">' + esc(t) + ' <button type="button" class="linklike" data-auto-stop>Don’t send mine</button></span>';
function insAutoSaid(after, text) {
  let slot = after.querySelector(".ask-auto");
  if (!slot) {   // the card was drawn with the way to send by hand (before the server had answered, or for a word we did not know): that gives way to the notice
    const b = after.querySelector("button[data-ask]"), n = after.querySelector(".ask-note"); if (!b) return;
    if (after.matches(".sr-stranger, .ins-stranger")) { [...after.childNodes].forEach(x => { if (!(x.nodeType === 1 && x.matches("b, .ins-none-t"))) x.remove(); }); slot = document.createElement("span"); after.appendChild(document.createTextNode(" ")); after.appendChild(slot); }
    else { slot = document.createElement("span"); b.replaceWith(slot); if (n) n.remove(); }
  }
  slot.outerHTML = insAutoSaidHtml(text);
}
function insAutoSend(after, res, now, found) {
  if (!autoOn()) return;
  const sheet = after.matches(".ins-none");
  const still = q => { if (!after.isConnected) return false; if (now) return true; const s = document.getElementById("search"), b = document.getElementById("search-results"); return !!(s && b && !b.hidden && insClean(s.value) === q); };
  // a question like one on our list: the listed question goes on the reader's own list by itself (nothing of theirs is sent)
  if (res.note === "want" && res.want) {
    const id = res.want.id, wq = wantQ(id) || autoAskedQ(id); if (!wq || askedGone(wq) || askedList().some(x => x.w === id)) return;
    const keep = () => { if (!still(res.q)) return; const it = askedAdd(wq, ""); if (!it) return; askedSet(it.k, { w: id, sent: 1, kept: 1, auto: 1 }); askedBox();
      const b = after.querySelector("button[data-want-keep]"); if (b) { const said = document.createElement("p"); said.className = "ask-said"; said.setAttribute("role", "status"); said.textContent = "It is on your list: we will tell you on this device when it is answered."; b.replaceWith(said); } };
    if (now) keep(); else INS.sendT = setTimeout(keep, AUTO_WAIT);
    return;
  }
  const stranger = res.note === "other" && !!res.stranger, q = res.q;
  if (!autoSendOn() || !(res.note === "none" || stranger) || askedSentHas(q) || askedGone(q)) return;
  const drug = insCtx().drug || "";
  const send = async () => {
    if (!still(q) || insAutoSend.busy === q || askedSentHas(q)) return;
    insAutoSend.busy = q;
    try {
      if (stranger) { const d = await found; if (!d || !d.papers || !d.papers.length || !still(q)) return; }
      const k = insClean(q).slice(0, 200).toLowerCase(), had = askedList().some(x => x.k === k), it = askedAdd(q, drug); if (!it) return;
      let ok = false;
      try { const r = await fetch(ASK_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ q: it.q, d: it.d, v: SITE_VERSION, a: 1 }) }); ok = r.ok; } catch (e) { ok = false; }
      if (!ok) {   // not taken (the day's room for such questions is used, or the connection failed): nothing is claimed; the way to send by hand stands
        if (!had) askedDrop(it.k);
        const slot = after.querySelector(".ask-auto"); if (slot) slot.outerHTML = insAskBtn(q, sheet ? "qz2-nb ins-askus" : "linklike");
        return; }
      askedSet(it.k, { sent: 1, auto: 1 }); askedTidy(it.k); askedBox();
      if (after.isConnected) insAutoSaid(after, AUTO_SENT);
    } finally { insAutoSend.busy = null; }
  };
  if (now) send(); else INS.sendT = setTimeout(send, AUTO_WAIT);
}
if (typeof document !== "undefined") document.addEventListener("click", e => {   // "Don't send mine": off on this device, said in the same place
  const b = e.target.closest && e.target.closest("button[data-auto-stop]"); if (!b) return;
  e.preventDefault(); e.stopPropagation();
  try { localStorage.setItem(AUTO_OFF, "0"); } catch (err) { /* this page only */ }
  const p = b.closest(".ask-auto-said"); if (p) p.textContent = "Off on this device: from now on nothing is sent or looked up by itself (About us, Privacy turns it on again). This one question was sent.";
  askedBox();
}, true);
/* (2.15.3; the senior author, 17 November 2026: "I may want to read the history of questions I made somewhere although it has to be discreet".)
   The questions a reader asked, the last thirty, kept on this device only and shown folded under "Your questions" on the start page. A tap asks
   one again. Kept when a question is asked with Enter, when one of its results is opened, and when it is sent. Nothing of it leaves the device.
   It is OFF until the reader turns it on, with one quiet line on the start page: the site's promise stands that nothing typed is kept unless the
   reader chooses so, and a phone is often shared (a list of questions about drugs is not for everyone who picks it up). Turning it off clears it. */
const HIST_KEY = "pk-hist", HIST_ON = "pk-hist-on", HIST_MAX = 30;
function histOn() { try { return localStorage.getItem(HIST_ON) === "1"; } catch (e) { return false; } }
function histList() { try { const a = JSON.parse(localStorage.getItem(HIST_KEY) || "[]"); return Array.isArray(a) ? a.filter(x => x && typeof x.q === "string").slice(0, HIST_MAX) : []; } catch (e) { return []; } }
function histAdd(q) {
  if (!histOn()) return;
  q = insClean(q); if (insWordsIn(q) < 2 || q.length > 160) return;
  try { const k = q.toLowerCase(), a = histList().filter(x => x.q.toLowerCase() !== k); a.unshift({ q, t: Date.now() }); localStorage.setItem(HIST_KEY, JSON.stringify(a.slice(0, HIST_MAX))); } catch (e) { /* no storage: no history */ }
  histBox();
}
function histBox() {
  const box = document.getElementById("home-hist"); if (!box) return; box.hidden = false;
  if (!histOn()) { box.innerHTML = '<p class="hist-off"><button type="button" class="linklike" data-hist-on>Keep my past searches on this device</button></p>'; return; }
  const a = histList(), was = box.querySelector("details"), open = was && was.open;
  box.innerHTML = '<details class="hist"' + (open ? " open" : "") + '><summary>Your past searches (' + a.length + ')</summary><p class="hist-n">Kept on this device only. ' + (a.length ? "" : "Nothing yet: a question is kept when you ask it. ") + '</p><ul>' +
    a.map(x => '<li><button type="button" class="hist-q" data-hist="' + esc(x.q) + '">' + esc(x.q) + "</button></li>").join("") + '</ul><p class="hist-c"><button type="button" class="linklike" data-hist-clear>Stop keeping them and clear this list</button></p></details>';
}
if (typeof document !== "undefined") {
  histBox();
  document.addEventListener("click", e => { if (!e.target.closest) return;
    const hq = e.target.closest("button[data-hist]"); if (hq) { const s = document.getElementById("search"); if (!s) return; s.value = hq.dataset.hist; window.scrollTo(0, 0); setTimeout(() => { s.focus({ preventScroll: true }); runSearch(s.value); }, 0); return; }
    if (e.target.closest("button[data-hist-clear]")) { try { localStorage.removeItem(HIST_KEY); localStorage.removeItem(HIST_ON); } catch (err) { /* nothing kept */ } histBox(); return; }
    if (e.target.closest("button[data-hist-on]")) { try { localStorage.setItem(HIST_ON, "1"); } catch (err) { /* no storage: it stays off */ } histBox(); const d = document.querySelector("#home-hist details"); if (d) d.open = true; return; }
    if (e.target.closest("#search-results a, #search-results button[data-ask]")) { const s = document.getElementById("search"); if (s && s.value) histAdd(s.value); }
  }, true);
  document.addEventListener("keydown", e => { if (e.key === "Enter" && !e.isComposing && e.target && e.target.id === "search" && e.target.value) histAdd(e.target.value); }, true);
}
if (typeof window !== "undefined") { if (window.requestIdleCallback) requestIdleCallback(() => askProbe(), { timeout: 3000 }); else setTimeout(askProbe, 1200); }

/* ---------- Written by our system (site 2.6, 15 November 2026). The senior author: machine-written answers "should be published
   and automatically deployed with a very discreet disclaimer and we should just be able to access everything that was
   automatically written and deployed to check whenever we want"; "if the automatic answer is not complete it should have a
   small discreet disclaimer"; in "the language and format we write the rest of the website".
   AUTO (from the build: data/auto/answers, the published ones) holds each such answer: its question, short answer, But, How
   do we know? and its sources as reference records. It is shown in the site's own form with two differences that are
   always there: a quiet line, "Written by our system from N papers. Not yet checked by a person." (and "Not complete yet"
   where papers could not be read), and no evidence bars, because nobody has rated it. The search box finds it as it finds
   every answer; its drug's page lists it in a section of its own; the page "Written by our system" lists every one.
   (These functions are also called while the pages draw, before the rest of this file has run: they read nothing of it.) ---------- */
function isAuto(id) { return typeof AUTO === "object" && AUTO !== null && typeof id === "string" && Object.prototype.hasOwnProperty.call(AUTO, id); }
function autoFor(page) { return typeof AUTO === "object" && AUTO ? Object.keys(AUTO).filter(id => AUTO[id].page === page).sort((a, b) => (AUTO[b].made || "").localeCompare(AUTO[a].made || "") || a.localeCompare(b)) : []; }
// what it read (2.7): papers in full, the summaries of papers behind a paywall, the pages of official bodies
function autoFrom(a) {
  const f = a.from || { papers: a.refs.length, summaries: 0, official: 0 }, bits = [];
  if (f.papers) bits.push(f.papers + (f.papers === 1 ? " paper" : " papers"));
  if (f.summaries) bits.push(f.summaries === 1 ? "the summary of 1 paper" : "the summaries of " + f.summaries + " papers");
  if (f.official) bits.push(f.official + (f.official === 1 ? " official page" : " official pages"));
  return bits.length > 1 ? bits.slice(0, -1).join(", ") + " and " + bits[bits.length - 1] : bits[0] || "0 papers";
}
function autoLabel(a) {
  return '<p class="auto-l">Written by our system from ' + autoFrom(a) + ". Not yet checked by a person." + (a.complete ? "" : ' <span class="auto-inc">Not complete yet.</span>') + "</p>";
}
function autoBodyHtml(id) {
  const a = AUTO[id];
  const tail = autoLabel(a) + '<details class="auto-src"><summary>Sources (' + a.refs.length + ')</summary><ol class="auto-refs">' + a.refs.map(r => "<li>" + apaReference(r) + "</li>").join("") + "</ol></details>" +
    '<p class="auto-acts"><button type="button" class="linklike" data-auto-report="' + esc(id) + '">Report a mistake in this answer</button></p>';
  // an answer about amounts (2.7; the senior author's decisions of 15 November 2026): the lines the code wrote, then each amount in
  // its source's own words (15 at most), with who received it, under what care, and whose words they are
  if (a.kind === "amounts") return (a.first ? '<p class="auto-first" role="note">' + esc(a.first) + "</p>" : "") + '<p class="ask-short">' + esc(a.short) + '</p><p class="ask-but">' + esc(a.but) + "</p>" +
    '<ul class="auto-rows">' + a.rows.map(r => { const ref = a.refs.find(x => x.id === r.ref);
      return '<li class="ar"><span class="ar-who">' + esc(r.who) + "; " + esc(r.what) + '.</span> <q class="ar-q">' + esc(r.quote) + '</q> <span class="ar-src">' + (ref ? esc(inTextLabel(ref, a.refs)) : "") + (r.read === "summary" ? ", read in summary only" : "") + "</span></li>"; }).join("") + "</ul>" + tail;
  return '<p class="ask-short">' + esc(a.short) + '</p><p class="ask-but"><b>But</b> ' + esc(a.but.replace(/^but[,:]?\s+/i, "")) + "</p>" +
    '<details class="ask-how"><summary>How do we know?</summary><ul class="ask-howl">' + a.how.map((t, i) => { const hq = a.howq && a.howq[i], ref = hq && a.refs.find(x => x.id === hq.ref);
      // (2.7.1) the source's own words under the line, 15 at most: what the system wrote can be compared with what the source says
      return "<li>" + esc(t) + (hq && ref ? '<span class="how-q"><q>' + esc(hq.q) + '</q> <span class="how-src">' + esc(inTextLabel(ref, a.refs)) + "</span></span>" : "") + "</li>"; }).join("") + "</ul></details>" + tail;
}
function autoRowHtml(x, best) {
  const a = AUTO[x.id], w = mfWhere(a.page);
  return '<a class="sr-ans sr-fit-a sr-auto' + (best ? " sr-best" : "") + '" href="#auto/q-' + esc(x.id) + '" data-insight="' + esc(x.id) + '" data-page="' + esc(a.page) + '"><span class="k">' + esc(w.name) + '</span><span class="t">' + esc(a.q) +
    '</span><span class="a">' + esc(best ? a.short : glanceClause(a.short)) + '</span><span class="m auto-m">Written by our system · not yet checked by a person</span></a>';
}
// a list of such answers as links that open each over the page (a drug's page, and the page that lists them all)
function autoListHtml(ids, withPage) {
  const day = d => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || ""); return m ? +m[3] + " " + ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][+m[2] - 1] + " " + m[1] : ""; };
  return '<ul class="wl auto-list">' + ids.map(id => { const a = AUTO[id], w = withPage ? mfWhere(a.page) : null;
    return '<li class="wl-i auto-i"><a class="auto-a" href="#auto/q-' + esc(id) + '" data-sheet="' + esc(id) + '"><span class="wl-q">' + esc(a.q) + '</span><span class="auto-meta">' + (w ? esc(w.name) + " · " : "") + esc(autoFrom(a)) +
      (day(a.made) ? " · " + day(a.made) : "") + (a.complete ? "" : " · not complete yet") + "</span></a></li>"; }).join("") + "</ul>";
}
// (2.8) the pages the system started: drugs people ask about that had no page. Each has an address of its own (#auto/p-kava), is
// listed with the drugs, and says at its top that the system started it and that nobody has checked it yet.
function autoStarted() { return typeof AUTO_PAGES === "object" && AUTO_PAGES ? Object.keys(AUTO_PAGES).filter(k => autoFor("new:" + k).length || autoShell(k)).sort((a, b) => AUTO_PAGES[a].localeCompare(AUTO_PAGES[b])) : []; }
function autoStartedListHtml() {
  const ks = autoStarted(); if (!ks.length) return "";
  const meta = k => { const n = autoFor("new:" + k).length, p = autoPics(k).length, sh = autoShell(k), q = sh ? sh.asked.length : 0;
    return [n ? n + (n === 1 ? " answer" : " answers") : "No answer yet", p ? p + (p === 1 ? " picture" : " pictures") : "", q ? q + (q === 1 ? " question asked" : " questions asked") : ""].filter(Boolean).join(" · "); };
  return '<h2 class="auto-h">Pages our system started</h2><p class="auto-sec">Drugs and medicines people ask about that had no page here. Our system started these by itself. A person has not checked them yet.</p><ul class="wl auto-pages">' +
    ks.map(k => { const ph = autoPics(k)[0]; return '<li class="wl-i"><a class="auto-a' + (ph ? " hasth" : "") + '" href="#auto/p-' + esc(k) + '">' + (ph ? '<span class="auto-th">' + autoPicImg(ph, "t", "", true) + "</span>" : "") +
      '<span class="wl-q">' + esc(AUTO_PAGES[k]) + '</span><span class="auto-meta">' + meta(k) + "</span></a></li>"; }).join("") + "</ul>";
}
/* ---------- (2.12) A page people asked about, in the form of a drug's page ----------
   The senior author, 17 November 2026, of kanna and Mitragyna javanica (two drugs he asked about that had no page): "our ai has
   to create this pages in a perfect coherent format to the rest of the website (and find pictures for them, their different forms
   etc. if the pictures have not been verified and the ai is uncertain then we could have a small disclaimer". So a page the
   system started has a drug page's header (its picture, its name), a line that says who made it, and a drug page's menu of
   parts: what it looks like (the pictures the system found: only CC0 and CC BY, each with its maker; a small line says that no
   person has checked them), what people ask (the listed questions, in our words, each with the way to be told when it is
   answered), and what the system has written. It is shown as soon as people ask, before there is an answer. Nothing on it
   says what the drug is or does: the species under the name is GBIF's own record, and the class it is filed under is not shown.
   (These are declarations, not constants: the page's first route runs before this file's constants exist.) */
function autoShell(k) { return (typeof AUTO_SHELL === "object" && AUTO_SHELL && AUTO_SHELL[k]) || null; }
function autoPics(k) { return (typeof AUTO_PICS === "object" && AUTO_PICS && AUTO_PICS[k]) || []; }
function autoAskedQ(id) { if (typeof AUTO_SHELL !== "object" || !AUTO_SHELL) return ""; for (const k of Object.keys(AUTO_SHELL)) { const x = AUTO_SHELL[k].asked.find(a => a.id === id); if (x) return x.q; } return ""; }
// the page's name inside a sentence: "kanna", "anabolic steroids and other body-building drugs"; a species' name and a name in capitals as written
function autoLow(k) { const n = String(AUTO_PAGES[k]).replace(/\s*\(.*\)$/, ""), sh = autoShell(k); return (sh && sh.science.some(s => norm(s.name) === norm(n))) || !/^[A-Z][a-z]+\b/.test(n) ? n : n.charAt(0).toLowerCase() + n.slice(1); }
function autoKindWord(kind) { return kind === "fungus" ? "fungus" : "plant"; }
function autoPicAlt(p) { return p.species + ", the " + autoKindWord(p.kind) + (p.country ? ", seen in " + inCtry(p.country) : ""); }
function autoPicImg(p, size, alt, lazy) { const d = p[size]; return '<img class="ph" src="img/auto/' + esc(p.file) + "-" + size + '.webp" width="' + d[0] + '" height="' + d[1] + '" alt="' + esc(alt) + '"' + (lazy ? ' loading="lazy" decoding="async"' : "") + ">"; }
// who made a picture, its licence, and where it is kept (the licences ask for this)
function autoPicCredit(p) {
  const inat = /^https:\/\/www\.inaturalist\.org\//.test(p.page), who = p.maker || (inat ? "iNaturalist" : "its record");
  return (p.page ? '<a href="' + esc(p.page) + '" target="_blank" rel="noopener">' + esc(who) + "</a>" : esc(who)) + ", " +
    (p.licence_url ? '<a href="' + esc(p.licence_url) + '" target="_blank" rel="noopener">' + esc(p.licence) + "</a>" : esc(p.licence)) + (p.maker && inat ? ", via iNaturalist" : "");
}
function autoLooksHtml(k) {
  const pics = autoPics(k); if (!pics.length) return "";
  const kinds = [...new Set(pics.map(p => p.kind))];
  return '<ul class="looks auto-looks">' + pics.map(p => '<li class="look hasph"><span class="look-ph">' + autoPicImg(p, "t", autoPicAlt(p), true) + '</span><span class="look-t"><b>The ' + autoKindWord(p.kind) + "</b><span><i>" + esc(p.species) + "</i>" +
      (p.country ? ". Seen in " + esc(inCtry(p.country)) + "." : "") + "</span></span></li>").join("") + "</ul>" +
    '<details class="look-credits"><summary>Photo credits</summary><p>' + pics.map((p, i) => "Photo " + (i + 1) + ": " + autoPicCredit(p)).join("; ") + ".</p></details>" +
    // (the site's rule for every gallery, docs/WRITING-RULES.md: it shows examples; the same thing can look different and different things the same)
    '<p class="look-note auto-picnote">Our system found these pictures by itself. They come from GBIF, an open record of plants and fungi that people saw and named. A person here has not checked them yet. They are examples: ' +
      (kinds.length === 1 && kinds[0] === "fungus" ? "the same fungus can look different, and different fungi can look the same" : kinds.length === 1 ? "the same plant can look different, and different plants can look the same" : "the same species can look different, and different species can look the same") +
      ". A picture cannot tell you what you have. " + phToggle() + "</p>";
}
// the listed questions a reader keeps on this device (the list under "Your questions": the key is ASK_KEY's, read here because this may be drawn before that constant exists)
function autoKept() { try { const x = JSON.parse(localStorage.getItem("pk-asked") || "[]"); return new Set((Array.isArray(x) ? x : []).filter(it => it && it.w).map(it => it.w)); } catch (e) { return new Set(); } }
function autoAskedHtml(k) {
  const sh = autoShell(k), asked = sh ? sh.asked : []; if (!asked.length) return "";
  const kept = autoKept();
  return '<ul class="wl auto-asked">' + asked.map(a => '<li class="wl-i"><span class="wl-q">' + esc(a.q) + "</span>" +
    (a.answer && isAuto(a.answer) ? '<a class="wl-b" href="#auto/q-' + esc(a.answer) + '" data-sheet="' + esc(a.answer) + '">Read what our system wrote</a>'
      : '<span class="wl-n">Not answered yet</span>' + (kept.has(a.id) ? '<span class="wl-s">' + icon("check") + "We will tell you on this device</span>" : '<button type="button" class="wl-b" data-want-keep="' + esc(a.id) + '">Tell me when it is answered</button>')) + "</li>").join("") + "</ul>" +
    '<p class="auto-sec">' + (asked.length === 1 ? "This question is on our list. Our system looks for research on it by itself." : "These questions are on our list. Our system looks for research on them by itself.") + "</p>";
}
function autoPageHtml(k) {
  const name = AUTO_PAGES[k], sh = autoShell(k) || { name, science: [], asked: [] }, pics = autoPics(k), ids = autoFor("new:" + k), base = "auto/p-" + k, low = autoLow(k);
  const kind = sh.science.length ? sh.science[0].kind : "", ph = pics[0] || null, secs = [], open = sh.asked.filter(a => !(a.answer && isAuto(a.answer))).length;
  if (pics.length) secs.push({ id: "p-looks", name: "What does it look like?", chip: "Looks", icon: "eye", n: pics.length + (pics.length === 1 ? " picture" : " pictures"), line: "Not yet checked by a person", body: autoLooksHtml(k) });
  if (sh.asked.length) secs.push({ id: "p-asked", name: "What people ask", chip: "Questions", icon: "message", n: sh.asked.length + (sh.asked.length === 1 ? " question" : " questions"),
    line: !open ? "Answered by our system" : open === sh.asked.length ? "Not answered yet" : open + " not answered yet", body: autoAskedHtml(k) });
  if (ids.length) secs.push({ id: "p-auto", name: "Written by our system", chip: "By our system", icon: "book", n: ids.length + (ids.length === 1 ? " answer" : " answers"), line: "Not yet checked by a person",
    body: '<p class="auto-sec">Our system wrote these by itself from research papers and official health pages it found and read. A person has not checked them yet.</p>' + autoListHtml(ids, false) });
  const aka = sh.science.filter(s => norm(s.name) !== norm(name));
  const head = '<header class="dh' + (ph ? " hasph" : "") + (name.length > 24 ? " long" : "") + '">' + (ph ? '<figure class="dh-ph">' + autoPicImg(ph, "m", autoPicAlt(ph), false) + (pics.length > 1 ? '<a class="dh-forms" href="#' + base + '/part-p-looks">See all ' + pics.length + " pictures</a>" : "") + "</figure>" : "") +
    '<div class="dh-t">' + (kind ? '<p class="dh-fam">' + icon(kind === "fungus" ? "mushroom" : "leaf") + (kind === "fungus" ? "Fungus" : "Plant") + "</p>" : "") + "<h1>" + esc(name) + "</h1>" +
    (aka.length ? '<p class="dh-aka">' + aka.map(s => "<i>" + esc(s.name) + "</i>").join(", ") + "</p>" : "") + "</div></header>";
  const top = '<p class="auto-top" role="note">' + icon("bulb") + "<span>People asked about " + esc(low) + ", and the site had no page. Our system started this one by itself" +
    (ids.length ? " and wrote what is on it. A person has not checked it yet." : ". It has not written an answer yet. A person has not checked this page.") + "</span></p>";
  // one part is shown at once; two or more are behind the menu, as on a drug's page
  const body = secs.length > 1 ? secPageHtml(name.replace(/\s*\(.*\)$/, ""), secs, "")
    : secs.map(x => '<section class="sec auto-one" id="' + x.id + '" aria-labelledby="' + x.id + '-h"><h2 id="' + x.id + '-h" tabindex="-1"><span class="sec-ic">' + icon(x.icon) + "</span>" + esc(x.name) + '</h2><div class="sec-b">' + x.body + "</div></section>").join("");
  const ask = '<section class="sec fbline" aria-label="Ask or report"><p><b>Ask about ' + esc(low) + ".</b> Type your question in the box at the top. If the site cannot answer it yet, you can send it to us with one tap.</p><div class=\"fb-two\">" +
    '<button type="button" data-ask-fill="' + esc(low) + '">' + icon("search") + 'Ask a question</button><button type="button" data-fb="issue">' + icon("flag") + "Report a mistake</button></div></section>";
  return head + top + body + ask + '<p class="auto-back"><a class="go" href="#auto">Everything written by our system</a></p>';
}
function autoPage(started) {
  const box = document.getElementById("auto-list"); if (!box) return;
  const head = document.querySelector("#view-auto .pagetitle"), lede = document.querySelector("#view-auto .lede"), how = document.querySelector("#view-auto .auto-how");
  const pg = document.getElementById("auto-page"), main = document.getElementById("auto-main");
  if (started && pg && typeof AUTO_PAGES === "object" && AUTO_PAGES && AUTO_PAGES[started]) {            // one started page, in the form of a drug's page (2.12)
    pg.dataset.base = "auto/p-" + started; pg.innerHTML = autoPageHtml(started); pg.hidden = false; if (main) main.hidden = true;
    applyPhotoPref(); return;
  }
  if (pg) { pg.hidden = true; pg.innerHTML = ""; delete pg.dataset.base; }
  if (main) main.hidden = false;
  if (head) head.textContent = "Written by our system";
  if (lede) lede.textContent = "Answers our system wrote by itself, from research papers and official health pages it found and read. A person has not checked them yet. Each one says so and shows its sources.";
  if (how) how.hidden = false;
  const ids = typeof AUTO === "object" && AUTO ? Object.keys(AUTO).sort((a, b) => (AUTO[b].made || "").localeCompare(AUTO[a].made || "") || a.localeCompare(b)) : [];
  const st = autoStartedListHtml();
  box.innerHTML = st + (ids.length ? (st ? '<h2 class="auto-h">Every answer</h2>' : "") + '<p class="auto-n">' + ids.length + (ids.length === 1 ? " answer" : " answers") + ", the newest first.</p>" + autoListHtml(ids, true)
    : st ? '<h2 class="auto-h">Every answer</h2><p class="muted">No answer is shown right now.</p>' : '<p class="muted">Nothing yet. The first answers appear here as soon as the system has written them.</p>');
}
if (typeof document !== "undefined") {
  { const pg = document.getElementById("auto-page"); if (!(pg && pg.dataset.base)) autoPage(); }   // (a started page the first route has just drawn stays)
  // (2.12) "Ask a question" on a started page: its name is put in the box, and the reader goes on from there
  document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("button[data-ask-fill]"); if (!b) return;
    e.preventDefault(); const s = document.getElementById("search"); if (!s) return; s.value = b.dataset.askFill + " ";
    if (s.scrollIntoView) s.scrollIntoView({ block: "center" }); setTimeout(() => { s.focus({ preventScroll: true }); try { s.setSelectionRange(s.value.length, s.value.length); } catch (err) { /* the cursor stays where the browser puts it */ } }, 0); });
  // every picture the system found is also named among the site's photo credits (About us)
  { const el = document.getElementById("photo-credits"); if (el && typeof AUTO_PICS === "object" && AUTO_PICS) el.insertAdjacentHTML("beforeend", Object.keys(AUTO_PICS).map(k => AUTO_PICS[k].map(p =>
      "<li><b>" + esc(AUTO_PAGES[k] || k) + ":</b> the " + autoKindWord(p.kind) + " <i>" + esc(p.species) + '</i>, found by our system. <span class="phcredit">Photo: ' + autoPicCredit(p) + "</span></li>").join("")).join("")); }
  document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("button[data-auto-report]"); if (!b) return;
    e.preventDefault(); const id = b.dataset.autoReport; if (EV.open) closeEvidence(); openFeedback("issue", "#auto/q-" + id, ""); });
}

/* ---------- On our list (site 2.5, 15 November 2026). The senior author: "there is room for growth if we don't depend on the
   users' emails but make the site understand on its own what the users want added in the website in-app and not via email";
   and, the same evening: "i just want the website to be perfect".
   - The list (data/site/wanted.json; const WANTED from the build: the items the site does not answer yet) is public: its own
     page, "On our list". A question typed in the search box that is like one of them (insWant: matched on this device) gets
     "Not answered yet. A question like yours is on our list".
   - Counting. For such a question the device sends one thing: the number of the list item (POST api/want { id }). Never the
     words typed, no name, no cookie; the site's program keeps a count for each item and nothing about who asked. It is sent
     once per item per visit (sessionStorage), only after the card has stood for a moment or Enter was pressed, only where
     the card says "We count how many people ask this", and not at all when the reader has switched counting off (About us,
     Privacy), when the browser asks not to be tracked (Global Privacy Control, Do Not Track) or where the site's store is
     not switched on. The scout reads the counts (scripts/auto), so the editors see what people are waiting for.
   - "Tell me when it is answered" puts the listed question in "Your questions" (on this device); it turns green when a later
     version of the site answers it. ---------- */
const WANT_API = "api/want", WANT_OFF = "pk-count", WANT_KEY = "pk-want", WANT_WAIT = 2500;
const wantAsked = () => navigator.globalPrivacyControl === true || navigator.doNotTrack === "1" || window.doNotTrack === "1";   // the browser asks sites not to track
function wantOff() { try { if (localStorage.getItem(WANT_OFF) === "0") return true; } catch (e) { /* no storage: the browser's own wish decides */ } return wantAsked(); }
const wantOn = () => ASK_ON === true && !wantOff();
function wantDone() { try { const x = JSON.parse(sessionStorage.getItem(WANT_KEY) || "[]"); return new Set(Array.isArray(x) ? x : []); } catch (e) { return wantDone.mem || (wantDone.mem = new Set()); } }
function wantCount(id) {
  if (!wantOn() || !/^w_[a-z0-9_]{1,40}$/.test(String(id))) return false;
  const done = wantDone(); if (done.has(id)) return false; done.add(id);
  try { sessionStorage.setItem(WANT_KEY, JSON.stringify([...done])); } catch (e) { wantDone.mem = done; }
  try { fetch(WANT_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ id }), keepalive: true }).catch(() => {}); } catch (e) { /* not counted: nothing depends on it */ }
  return true;
}
const wantItems = () => (typeof WANTED !== "undefined" && Array.isArray(WANTED) ? WANTED : INS.list ? INS.list.ids.map((id, i) => [id, INS.list.q[i]]) : []);
const wantQ = id => (wantItems().find(x => x[0] === id) || [])[1] || "";
// the list's own page: every question on it, each with the way to be told when it is answered
function wantedPage() {
  const box = document.getElementById("wanted-list"); if (!box) return;
  const items = wantItems(), kept = new Set(askedList().filter(it => it.w).map(it => it.w));
  box.innerHTML = items.length ? '<ul class="wl">' + items.map(([id, q]) => '<li class="wl-i"><span class="wl-q">' + esc(q) + "</span>" +
    (kept.has(id) ? '<span class="wl-s">' + icon("check") + "We will tell you on this device</span>" : '<button type="button" class="wl-b" data-want-keep="' + esc(id) + '">Tell me when it is answered</button>') + "</li>").join("") + "</ul>"
    : '<p class="muted">Nothing is on the list right now.</p>';
}
if (typeof document !== "undefined") {
  wantedPage(); window.addEventListener("hashchange", () => { if (location.hash === "#wanted") wantedPage(); });
  // (2.16.1) the switch beside it: looking research up by itself, on or off on this device
  { const sw2 = document.getElementById("auto-switch"), st2 = document.getElementById("auto-state");
    if (sw2) { const draw2 = () => { sw2.checked = autoOn(); if (st2) st2.textContent = sw2.checked ? "On." : "Off on this device."; };
      sw2.addEventListener("change", () => { try { if (sw2.checked) localStorage.removeItem(AUTO_OFF); else localStorage.setItem(AUTO_OFF, "0"); } catch (e) { /* this page only */ } draw2(); });
      draw2(); } }
  // the switch in About us > Privacy: counting on or off on this device
  const sw = document.getElementById("count-switch"), st = document.getElementById("count-state");
  if (sw) {
    const draw = () => { let off = false; try { off = localStorage.getItem(WANT_OFF) === "0"; } catch (e) { /* no storage */ }
      sw.checked = !off && !wantAsked(); sw.disabled = wantAsked();
      if (st) st.textContent = wantAsked() ? "Off: your browser asks sites not to track you." : sw.checked ? "On." : "Off on this device."; };
    sw.addEventListener("change", () => { try { if (sw.checked) localStorage.removeItem(WANT_OFF); else localStorage.setItem(WANT_OFF, "0"); } catch (e) { /* this page only */ } draw(); });
    draw();
  }
}

// for the checks (scripts/ux/insight_check.js, scripts/insight/parity.js): the same functions the search box uses
window.pkInsight = {
  state: () => INS.state, load: insightLoad, encode: t => insEncode(t), expand: t => insExpand(t), mask: t => insMask(t), named: t => insNamed(t), times: () => INS.times.slice(),
  embed: t => insEmbed(t).then(v => Array.from(v)), tiers: () => Object.assign({}, INS.t), weights: () => Object.assign({}, INS.wt), judge: () => JSON.parse(JSON.stringify(INS.judge)),
  read: (t, ctx) => { const r = insRead(t, ctx || {}); return { core: r.core, depth: r.depth, note: r.note, routes: r.routes.map(x => x.kind), groups: r.groups }; },
  rank: (t, ctx) => insRank(t, ctx || {}).then(r => ({ q: r.q, core: r.core, depth: r.depth, note: r.note, emergency: r.emergency, routes: r.routes.map(x => ({ kind: x.kind, t: x.t, href: x.href, el: x.el || null, mix: x.mix || null })),
    best: r.best, related: r.related, judge: r.judge || null, want: r.want || null, unf: r.unf || "", demoted: !!r.demoted, stranger: r.stranger || "", read: r.read || [], ms: r.ms })),
  say: (t, ctx) => insRank(t, ctx || {}).then(r => insSay(r)),   // (the words a screen reader hears: scripts/ux/say.js)
  scope: t => insScope(t), unfinished: (t, on) => insUnfinished(t, !!on), unknown: t => insUnknown(t), spell: t => insSpell(t), listed: () => (INS.list ? INS.list.ids.slice() : [])
};
