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
   - Enter opens the sheet for the question as asked: the person's own words as the heading, each best answer in full under
     it; "full evidence", "the studies", "in detail" open "How do we know?"; "short", "tl;dr", "eli5" keep to the short
     answer and its But. No guess first, anywhere. No emergency line, except when the question is an emergency.
   - An answer linked from outside its own page opens in this sheet, over the page (Myth or fact's "Read the answer", the
     start page, a shared answer's other questions), and Back returns to exactly where the reader was.
   - Next questions ("People also ask" here, "Read next" on the pages) are the nearest answers by meaning, never from another
     drug, without the ones already opened in this visit (const INS_NEXT, put at the head of the page by site/build.js). ---------- */
const INS = { state: "idle", tries: 0, cache: new Map(), seq: 0, timer: 0, times: [], queue: Promise.resolve(), run: null, view: null, back: null, from: null, go: null, want: null };
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
  INS.state = "loading"; INS.tries++;
  const base = INS_BASE(), get = (u, how) => fetch(u).then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r[how](); });
  const runtime = insScript(base + "ort.wasm.min.js").then(() => {
    const ort = window.ort; ort.env.wasm.numThreads = 1; ort.env.wasm.proxy = false; ort.env.wasm.wasmPaths = base; ort.env.logLevel = "error"; return ort; });
  const told = get(base + INS_MODEL, "arrayBuffer"); told.catch(() => {});
  INS.loading = Promise.all([get("data/insight.json", "json"), get(base + "vocab.txt", "text"), runtime])
    .then(([data, vocab, ort]) => (data.model === INS_MODEL ? told : get(base + data.model, "arrayBuffer"))
      .then(b => ort.InferenceSession.create(new Uint8Array(b), { executionProviders: ["wasm"], graphOptimizationLevel: "all" }))
      .then(s => { insPrepare(data, vocab); INS.session = s; return insEmbed("warm up"); }))
    .then(() => { INS.state = "ready"; insightReady(); return true; })
    // offline or an old browser: the word search goes on alone; one more try on the next visit to the box
    .catch(() => { INS.state = INS.tries < 2 ? "idle" : "off"; INS.loading = null; return false; });
  return INS.loading;
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
const insRx = n => n.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&");
function insPrepare(d, vocabText) {
  INS.dim = d.dim; INS.ids = d.ids; INS.rows = d.rows; INS.wt = d.weights; INS.t = d.tiers; INS.judge = d.judge;
  INS.W = insRows(d.W, d.dim); INS.M = insRows(d.M, d.dim); INS.S = insRows(d.S, d.dim);
  INS.idx = new Map(d.ids.map((id, i) => [id, i]));
  INS.about = d.about.map(xs => new Set(xs.map(k => d.slugs[k])));   // the drugs each answer is about
  // the names that name a drug in a question (build_index.py's names_table: the longest first), and the drugs each stands for
  INS.nameOf = new Map(d.names.map(([n, xs]) => [n, xs.map(k => d.slugs[k])]));
  INS.nameRe = new RegExp("(?<![\\p{L}\\p{N}_])(" + d.names.map(([n]) => insRx(n)).join("|") + ")(?![\\p{L}\\p{N}_])", "giu");
  // word overlap (TF-IDF as scripts/insight/eval_match.py's Lexical): a word's weight is log(1 + N / documents with it)
  const N = d.docs.length, df = new Map();
  d.docs.forEach(t => new Set(insTok(t)).forEach(w => df.set(w, (df.get(w) || 0) + 1)));
  INS.idf = new Map([...df].map(([w, n]) => [w, Math.log(1 + N / n)]));
  INS.post = new Map();   // word -> [answer, weight in its unit-length vector]
  d.docs.forEach((t, i) => { const v = new Map(); insTok(t).forEach(w => v.set(w, (v.get(w) || 0) + INS.idf.get(w)));
    const n = Math.sqrt([...v.values()].reduce((a, x) => a + x * x, 0)) || 1; v.forEach((x, w) => { if (!INS.post.has(w)) INS.post.set(w, []); INS.post.get(w).push([i, x / n]); }); });
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
    return { slug: s.slug, canon: s.name.split(" (")[0], re: new RegExp("(?<![\\p{L}\\p{N}_])(?:" + alt + ")(?![\\p{L}\\p{N}_])", "u") };
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
const insCap = t => t.charAt(0).toUpperCase() + t.slice(1);
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
  if (INS_RE.test.test(q)) {
    if (about && !NO_TEST.includes(about)) add("test", INS_PLACE.test(about), drugName(about), "Test kits for " + pageWord(about));
    else add("test", INS_PLACE.checking(), "Drug checking", "Drug checking and test kits");
  }
  const w = (q.match(INS_RE.what) || [])[1], slug = w && INS.any.get(w.toLowerCase().replace(/[.!?]+$/, "").trim());
  if (slug && subBySlug[slug] && !out.length) add("page", INS_PLACE.page(slug), "Drug · " + subBySlug[slug].cls, subBySlug[slug].name, { whole: true });
  return out;
}

/* ---------- The match (2.3) ---------- */
/* The score. One small function with one clear input: the question's numbers (v: with the drug's own name brought along;
   mv: with the drug names taken out; q: its words) against every answer's rows. Out, for every answer: the first look
   (2.2.0's score: the best wording, the short answer, the words in common) and the topic score (the best wording with the
   drug names taken out). A second scoring step, a trained judge, goes here and nowhere else. */
function insScore(v, mv, q) {
  const dim = INS.dim, nA = INS.ids.length, W = INS.W, M = INS.M, S = INS.S, wt = INS.wt, rows = INS.rows;
  const bw = new Float32Array(nA).fill(-1), bw2 = new Float32Array(nA).fill(-1), topic = new Float32Array(nA).fill(-1), sh = new Float32Array(nA), lex = new Float32Array(nA), plain = new Float32Array(nA), qv = new Map();
  for (let k = 0, o = 0; k < rows.length; k++, o += dim) {
    let s = 0, t = 0; for (let j = 0; j < dim; j++) { s += v[j] * W[o + j]; t += mv[j] * M[o + j]; }
    const a = rows[k]; if (s > bw[a]) { bw2[a] = bw[a]; bw[a] = s; } else if (s > bw2[a]) bw2[a] = s;
    if (t > topic[a]) topic[a] = t;
  }
  insTok(q).forEach(w => { if (INS.idf.has(w)) qv.set(w, (qv.get(w) || 0) + INS.idf.get(w)); });
  const qn = Math.sqrt([...qv.values()].reduce((a, x) => a + x * x, 0)) || 1;
  qv.forEach((x, w) => INS.post.get(w).forEach(([i, y]) => { lex[i] += (x / qn) * y; }));
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
function insTiers(sc, groups) {
  const T = INS.t, wt = INS.wt, all = [];
  for (let i = 0; i < INS.ids.length; i++) {
    const has = g => g.some(s => INS.about[i].has(s)), on = groups.every(has), by = sc.plain[i] + wt.topic * sc.topic[i];
    all.push({ i, on, some: !groups.length || groups.some(has), by, key: by + (on ? wt.same : 0), plain: sc.plain[i], topic: sc.topic[i] });
  }
  all.sort((a, b) => b.key - a.key || a.i - b.i);
  const c = all[0]; let next = null; for (const x of all) if (x !== c && x.on && (next === null || x.by > next)) next = x.by;
  c.f = [sc.bw[c.i], Math.max(sc.bw2[c.i], 0), sc.sh[c.i], sc.lex[c.i], c.topic, c.by - (next === null ? 0 : next)]; c.p = insJudge(c.f);
  const best = c.on && c.p >= INS.judge.best ? [c] : [];
  return { first: c, best, related: all.filter(x => !best.includes(x) && x.plain >= T.related && x.topic >= T.near && x.some).slice(0, 3) };
}
// the page an answer is shown as being on: a drug the question names (or the page's own) when the answer is asked there
function insPageOf(id, groups, drug) {
  const want = groups.flat().concat(drug ? [drug] : []).find(s => (QUESTIONS[s] || []).some(g => g.items.some(([x]) => x === id)));
  return answerPageKey(id, want) || claimById[id].substance;
}
/* insRank(question, ctx): everything Insight understands of one question. ctx.drug: the drug whose page the reader is on.
   Out: q (as typed), core (without depth words: what was matched), depth ("", "full" or "short"), routes, best (0 to 2) and
   related (up to 3), each { id, page, plain, topic, off } (off: not about every drug asked about), and what the list and
   the sheet say when there is no best match: note ("none": we haven't checked exactly this yet, with the way to ask us;
   "blocked": the same line without it; "": nothing, the route says it). insRead is the part that needs no model: the depth
   words, the drugs named, the routes. */
function insRead(query, ctx) {
  const q = insClean(query), drug = ctx && ctx.drug && subBySlug[ctx.drug] ? ctx.drug : null, d = insDepth(q), named = insNamed(d.core);
  const res = { q, core: d.core, depth: d.depth, drug: named.length ? null : drug, groups: named.length ? named : drug ? [[drug]] : [], routes: [], best: [], related: [], note: "", emergency: false };
  if (insBlocked(d.core)) { res.note = "blocked"; return res; }
  res.routes = insRoutes(d.core, named, drug); res.emergency = res.routes.some(r => r.kind === "help");
  return res;
}
async function insRank(query, ctx) {
  const t0 = performance.now(), res = insRead(query, ctx);
  if (res.note === "blocked") { res.ms = performance.now() - t0; return res; }
  const whole = res.routes.some(r => r.whole);                 // the question is a drug's name and nothing more: its page is the answer
  if (!(whole && insWordsIn(res.core) < INS_WORDS)) {
    const drug = ctx && ctx.drug, tx = insTexts(res.core, drug), v = await insEmbed(tx.full), mv = tx.masked === tx.full ? v : await insEmbed(tx.masked);
    const tiers = insTiers(insScore(v, mv, res.core), tx.groups);
    const row = c => ({ id: INS.ids[c.i], page: insPageOf(INS.ids[c.i], tx.groups, drug), plain: +c.plain.toFixed(4), topic: +c.topic.toFixed(4), off: !c.on });
    res.best = tiers.best.map(row); res.related = res.emergency ? [] : tiers.related.map(row);   // an emergency gets its route and the answers that fit, nothing nearby
    res.judge = { id: INS.ids[tiers.first.i], p: tiers.first.p, f: tiers.first.f };              // (for the checks: the first candidate and the judge's number for it)
  }
  // with no best match, say so, unless a route already is the answer to what was asked (help, a dose, a test, the drug's page)
  if (!res.best.length && !res.routes.some(r => r.kind !== "mix")) res.note = "none";
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
  const d = insCtx().drug, want = d ? "Ask about " + pageWord(d) : insPlaceholder.own;
  if (s.getAttribute("placeholder") !== want) s.setAttribute("placeholder", want);
}

/* ---------- In the search results ---------- */
const insQ = (id, page) => (page && sharedQuestion(page, id)) || anyQuestion(id) || ((SIMPLE.claims || {})[id] || {}).q || claimText(claimById[id]);
const insNoteText = () => "Runs on your " + (window.matchMedia && window.matchMedia("(pointer: coarse)").matches ? "phone" : "computer") + (ASK_ON ? ". What you type stays on it, unless you ask us to check a question." : ". Nothing you type leaves it.");
const INS_ICON = { help: "heart", mix: "mix", dose: "book", test: "flask", page: "molecule" };
// the emergency number where the reader is, or the way to the numbers: shown with an emergency route, and nowhere else
function insSosHtml(cls) {
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  return '<p class="' + cls + '">' + icon("phone") + "<span>" + (em ? "Emergency number in " + esc(inCtry(PREF_COUNTRY)) + ': <a href="tel:' + esc(telOf(em.numbers[0])) + '">' + esc(em.numbers[0].n) + "</a> · " : "") +
    '<a href="#emergency">' + (em ? "Other numbers" : "Emergency numbers by country") + "</a></span></p>";
}
function insRouteHtml(r, cls) {
  return '<a class="' + cls + " r-" + r.kind + '" href="' + esc(r.href) + '" data-ins-route="' + r.kind + '"' + (r.el ? ' data-el="' + esc(r.el) + '"' : "") + (r.mix ? ' data-mix="' + esc(r.mix) + '"' : "") + ">" +
    '<span class="ri">' + icon(INS_ICON[r.kind] || "arrow") + '</span><span class="k">' + esc(r.k) + '</span><span class="t">' + esc(r.t) + '</span><span class="go">' + icon("arrow") + "</span></a>";
}
// "Ask us to check it": one tap (2.4, below: Your questions); where the page can send it, a quiet line says what is sent
const insAskBtn = (q, cls) => '<button type="button" class="' + cls + '" data-ask="' + esc(q) + '">Ask us to check it</button>' + (ASK_ON ? '<span class="ask-note">Sends only this question. No name, no address.</span>' : "");
function insRowHtml(x, best) {
  const c = claimById[x.id], sp = SIMPLE.claims[x.id], w = mfWhere(x.page);
  return '<a class="sr-ans sr-fit-a' + (best ? " sr-best" : "") + '" href="' + esc(answerAddr(x.id, x.page)) + '" data-insight="' + esc(x.id) + '" data-page="' + esc(x.page) + '"><span class="k">' + esc(w.name) + '</span><span class="t">' + esc(insQ(x.id, x.page)) +
    '</span><span class="a">' + (best ? cueNum(esc(sp.short)) : esc(glanceClause(sp.short))) + '</span><span class="m">' + meterHtml(c.grade.certainty, true) + "</span></a>";
}
function insFitHtml(res) {
  const routes = res.routes.map(r => insRouteHtml(r, "sr-route")).join("") + (res.emergency ? insSosHtml("sr-sos") : "");
  const best = res.best.length ? '<p class="sr-fit-h">Best match</p>' + res.best.map(x => insRowHtml(x, true)).join("") : "";
  const none = res.note ? '<p class="sr-fit-none"><b>We haven’t checked exactly this yet.</b>' + (res.note === "none" ? " " + insAskBtn(res.q, "linklike") : "") + "</p>" : "";
  const related = res.related.length ? '<p class="sr-fit-h">Related</p>' + res.related.map(x => insRowHtml(x, false)).join("") : "";
  return '<div class="sr-fit" data-q="' + esc(res.q) + '">' + routes + best + none + related + '<p class="sr-fit-h sr-words" hidden>More results</p></div>';
}
// what a screen reader hears when the answers arrive: the route, the tier, the question matched
function insSay(res) {
  const parts = res.routes.map(r => r.t);
  if (res.best.length) parts.push("Best match: " + res.best.map(x => insQ(x.id, x.page)).join("; "));
  else if (res.note) parts.push("We haven’t checked exactly this yet");
  if (res.related.length) parts.push(res.related.length + " related answer" + (res.related.length === 1 ? "" : "s"));
  return parts.join(". ");
}
function insInject(box, res) {
  box.querySelectorAll(".sr-fit").forEach(e => e.remove());
  // what Insight shows is not repeated by the word search below it, which no longer calls any of its rows the best answer
  res.best.concat(res.related).forEach(x => box.querySelectorAll('a.sr-ans[data-cid="' + x.id + '"]').forEach(a => a.remove()));
  res.routes.forEach(r => box.querySelectorAll(':scope > a[href="' + r.href + '"]').forEach(a => a.remove()));
  box.querySelectorAll(":scope > a.sr-ans.best").forEach(a => { a.classList.remove("best"); const k = a.querySelector(".k"); if (k) k.textContent = k.textContent.replace(/^Best answer/, "Answer"); });
  const none = box.querySelector(":scope > .none"), ask = box.querySelector(":scope > .sr-ask");
  if (none) none.remove();                                     // Insight has its own line for a question with no checked answer
  if (ask && (res.note || !box.querySelector(":scope > a"))) ask.remove();   // one way to ask us, not two (and none for what we do not answer)
  if (res.note === "blocked") box.querySelectorAll(":scope > a").forEach(a => { if (!/^#s-[a-z0-9-]+$/.test(a.getAttribute("href") || "")) a.remove(); });
  const note = box.querySelector(":scope > .sr-note");
  if (note) note.insertAdjacentHTML("afterend", insFitHtml(res)); else box.insertAdjacentHTML("afterbegin", insFitHtml(res));
  // the word search's own rows follow under a quiet label, so that none reads as part of the best match or the related answers
  const words = box.querySelector(".sr-fit .sr-words"); if (words) words.hidden = !box.querySelector(":scope > a") || !(res.routes.length || res.best.length || res.related.length || res.note);
  const live = document.getElementById("search-count"); if (live) live.textContent = insSay(res);
}
// called by runSearch after the word search has drawn its results
function insightAfterSearch(raw) {
  const box = document.getElementById("search-results"); if (!box || box.hidden) return;
  if (INS.state !== "ready") {   // saving data: one quiet line under the results offers it; once tapped, it says it is coming
    if (INS.state === "idle" && insSaver()) box.insertAdjacentHTML("beforeend", '<p class="sr-get"><button type="button" class="linklike" data-ins-get>' + esc(insGetText()) + "</button></p>");
    else if (INS.state === "loading" && (INS.byHand || INS.want)) box.insertAdjacentHTML("beforeend", '<p class="sr-get" role="status">' + (INS.byHand ? "Downloading, once: about " + insMB() + " MB…" : "One moment: getting ready to read your question…") + "</p>");
    return;
  }
  if (!box.querySelector(":scope > .sr-note")) box.insertAdjacentHTML("afterbegin", '<p class="sr-note">' + icon("mobile") + "<span>" + esc(insNoteText()) + "</span></p>");
  const q = insClean(raw); clearTimeout(INS.timer);
  if (insWordsIn(q) < INS_WORDS) { INS.seq++; return; }
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
  window.addEventListener("hashchange", () => { insPlaceholder(); insArrive(); });
  insPlaceholder();
})();
/* Enter (or the search key on a phone) opens the answer to the question as asked. Before the page's own handler, which
   opens the first result: that stays for a word or two (a drug's name goes to its page) and when Insight is not there. */
document.addEventListener("keydown", e => {
  if (e.key !== "Enter" || e.isComposing || !e.target || e.target.id !== "search") return;
  const q = insClean(e.target.value); if (insWordsIn(q) < INS_WORDS) return;
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
  const c = claimById[id], sp = SIMPLE.claims[id];
  if (depth === "short") return '<p class="ask-short">' + cueNum(esc(sp.short)) + "</p>" + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") +
    '<div class="ask-foot">' + meterHtml(c.grade.certainty, true) + '<span class="ask-acts"><a class="ask-ev" href="#' + esc(id) + '">The evidence ' + icon("arrow") + "</a></span></div>";
  const body = answerBody(id, c, sp, false);
  return depth === "full" ? body.replace('<details class="ask-how">', '<details class="ask-how" open>') : body;
}
const insPageLink = (id, page) => { const addr = answerAddr(id, page), w = mfWhere(page), pl = sharedPlace(page || "", id);
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
  const res = v.res, routes = res.routes.map(r => insRouteHtml(r, "ins-route")).join("") + (res.emergency ? insSosHtml("dh-help ins-sos") : "");
  const best = res.best.map((x, n) => { const w = mfWhere(x.page);
    return '<section class="ins-one" aria-labelledby="ins-l' + n + '"><p class="ins-l" id="ins-l' + n + '"><span class="ins-l-k">' + icon(w.f.icon) + "<span>Checked answer · " + esc(w.name) + '</span></span><span class="ins-l-q">' + esc(insQ(x.id, x.page)) + "</span></p>" +
      '<div class="ins-ans">' + insBodyHtml(x.id, res.depth) + "</div>" + insPageLink(x.id, x.page) + "</section>"; }).join("");
  const none = res.note ? '<div class="ins-none"><p class="ins-none-t">We haven’t checked exactly this yet.</p>' + (res.note === "none" ? insAskBtn(res.q, "qz2-nb ins-askus") : "") + "</div>" : "";
  const related = !res.best.length && res.related.length ? '<div class="rn ins-rel"><p class="rn-k">Related</p><ul class="rn-l">' + res.related.map(x => { const w = mfWhere(x.page);
    return '<li><a href="' + esc(answerAddr(x.id, x.page)) + '" data-insight-next="' + esc(x.id) + '" data-page="' + esc(x.page) + '"><span><span class="ins-rel-k">' + esc(w.name) + "</span>" + esc(insQ(x.id, x.page)) + "</span>" + icon("arrow") + "</a></li>"; }).join("") + "</ul></div>" : "";
  const from = (res.best.length ? res.best : res.related).map(x => x.id), shown = res.best.concat(res.related).map(x => x.id);
  return insBar("<span>Your question</span>") + '<div class="ins ins-asked' + (res.depth ? " ins-" + res.depth : "") + '"><h2 id="ev-title" class="ins-yours" tabindex="-1">' + esc(insCap(res.q.length > 240 ? res.q.slice(0, 237) + "…" : res.q)) + "</h2>" +
    routes + best + none + related + insTailHtml(from, shown, res.groups) + "</div>";
}
function insDraw(v, opener) {
  const sh = document.getElementById("evsheet"), panel = sh && sh.querySelector(".panel"); if (!panel) return false;
  if (!EV.open) { EV.opener = opener === undefined ? document.activeElement : opener; try { history.pushState({ pkEvidence: "insight", pk: NAV_CUR }, ""); EV.pushed = true; } catch (e) { EV.pushed = false; } }
  // (an evidence still on its way for this sheet is not drawn over the answer: openEvidence draws only for its own EV.id)
  EV.id = "ins:" + (v.kind === "one" ? v.id : "asked"); EV.open = true; sh.classList.add("open"); document.documentElement.classList.add("sheet-open"); hidePop(); closeSearch();
  INS.view = v; INS.back = null;
  panel.innerHTML = insHtml(v); panel.scrollTop = 0;
  (v.kind === "one" ? [v.id] : v.res.best.map(x => x.id)).forEach(id => { markSeen(id); insOpenedNow().add(id); });
  const f = panel.querySelector("#ev-title"); if (f) f.focus({ preventScroll: true });
  return true;
}
// a new run of answers starts when the sheet opens; each answer or question read in it counts one towards the calm end
function insCount(fresh) { if (fresh || !INS.run || !EV.open) INS.run = { n: 0, more: 0 }; INS.run.n++; }
// one answer (opt: page, depth, sos, opener, fresh, from)
function openInsight(id, opener, fresh, opt) {
  if (!claimById[id] || !(SIMPLE.claims || {})[id]) return false;
  opt = opt || {}; insCount(fresh);
  if (!EV.open) INS.from = opt.from || null;
  return insDraw({ kind: "one", id, page: opt.page || answerPageKey(id) || claimById[id].substance, depth: opt.depth || "", sos: !!opt.sos }, opener);
}
// what the search box and its results were when the sheet opened over them: Back puts them back as they were
function insFromSearch(id) { const s = document.getElementById("search"); return { value: s ? s.value : "", hash: location.hash, id: id || null }; }
// the answer to a question as asked (Enter). A question that is only a request for something else (a dose, a test, a drug's
// page, help now) and has no checked answer of its own goes straight to that place, as its row in the list would.
function insAsk(q) {
  const from = insFromSearch(null);
  return insAnswer(q, insCtx()).then(res => {
    if (!res.best.length && res.routes.length === 1 && res.routes[0].kind !== "mix") { insFollow(res.routes[0]); return res; }
    insCount(true); if (!EV.open) INS.from = from; insDraw({ kind: "asked", res }, null); return res;
  });
}
function insFollow(r) {
  const s = document.getElementById("search"); if (s) { s.value = ""; s.blur(); } closeSearch();
  INS.go = { at: Date.now(), el: r.el || null, mix: r.mix ? r.mix.split(",") : null };
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
  if (g.el) setTimeout(() => { const el = document.getElementById(g.el); if (!el || !el.closest(".view.active")) return; scrollToEl(el);
    const h = el.querySelector("h2, h3") || el; h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }, 60);
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
    INS.go = { at: Date.now(), el: a.dataset.el || null, mix: a.dataset.mix ? a.dataset.mix.split(",") : null };
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
let ASK_ON = (() => { try { const x = sessionStorage.getItem("pk-ask-on"); return x === "1" ? true : x === "0" ? false : null; } catch (e) { return null; } })();
function askProbe() {
  if (ASK_ON !== null) return Promise.resolve(ASK_ON);
  if (askProbe.p) return askProbe.p;
  return (askProbe.p = fetch(ASK_API, { headers: { accept: "application/json" } }).then(r => r.ok ? r.json() : null).then(j => !!(j && j.ok === true), () => false)
    .then(on => { ASK_ON = on; try { sessionStorage.setItem("pk-ask-on", on ? "1" : "0"); } catch (e) { /* this page only */ } return on; }));
}
function askedList() { try { const x = JSON.parse(localStorage.getItem(ASK_KEY) || "[]"); return Array.isArray(x) ? x.filter(it => it && typeof it.q === "string" && it.k) : []; } catch (e) { return []; } }
function askedSave(list) { try { localStorage.setItem(ASK_KEY, JSON.stringify(list.slice(-20))); } catch (e) { /* this visit only */ } }
function askedAdd(q, drug) {
  const text = insClean(q).slice(0, 200), k = text.toLowerCase(); if (k.length < 3) return null;
  const list = askedList(); let it = list.find(x => x.k === k);
  if (!it) { it = { k, q: text, d: drug || "", t: Date.now(), cv: SITE_VERSION, st: "wait", sent: 0 }; list.push(it); askedSave(list); }
  return it;
}
function askedSet(k, patch) { const list = askedList(), it = list.find(x => x.k === k); if (!it) return; Object.assign(it, patch); askedSave(list); }
function askedDrop(k) { askedSave(askedList().filter(x => x.k !== k)); }
function askedBox() {
  const box = document.getElementById("home-asked"); if (!box) return;
  const list = askedList().filter(it => it.st !== "ans" || claimById[it.id]);
  if (!list.length) { box.hidden = true; box.innerHTML = ""; return; }
  const x = it => '<button type="button" class="aq-x" data-asked-x="' + esc(it.k) + '" aria-label="Take this question off the list">' + icon("x") + "</button>";
  const row = it => it.st === "ans"
    ? '<li class="aq ans"><a class="aq-a" href="' + esc(answerAddr(it.id, it.p)) + '" data-sheet="' + esc(it.id) + '" data-asked-open="' + esc(it.k) + '"><span class="aq-k">' + icon("check") + 'Answered</span><span class="aq-q">' + esc(it.q) + '</span><span class="aq-go">Read the answer ' + icon("arrow") + "</span></a>" + x(it) + "</li>"
    : '<li class="aq wait"><span class="aq-a"><span class="aq-k">' + icon("clock") + (it.sent ? "We are checking" : "Kept on this device") + '</span><span class="aq-q">' + esc(it.q) + "</span></span>" + x(it) + "</li>";
  box.innerHTML = '<h2 class="aq-h">Your questions</h2><ul class="aq-l">' + list.filter(it => it.st === "ans").concat(list.filter(it => it.st !== "ans")).map(row).join("") + "</ul>";
  box.hidden = false;
  askedCheckSoon();
}
// a kept question is asked again once per new version of the site: a best match now means it has been answered
async function askedCheck() {
  if (INS.state !== "ready") return;
  const list = askedList(); let changed = false;
  for (const it of list) {
    if (it.st !== "wait" || it.cv === SITE_VERSION) continue;
    try { const res = await insRank(it.q, { drug: it.d && subBySlug[it.d] ? it.d : null });
      if (res.best.length) { it.st = "ans"; it.id = res.best[0].id; it.p = res.best[0].page; }
      it.cv = SITE_VERSION; changed = true; } catch (e) { /* asked again on the next visit */ }
  }
  if (changed) { askedSave(list); askedBox(); }
}
function askedCheckSoon() {
  if (askedCheckSoon.done || !askedList().some(it => it.st === "wait" && it.cv !== SITE_VERSION)) return;
  askedCheckSoon.done = true;
  const go = () => { if (INS.state === "ready") askedCheck(); else if (!insSaver()) insightLoad().then(ok => { if (ok) askedCheck(); }); };
  if (window.requestIdleCallback) requestIdleCallback(go, { timeout: 4000 }); else setTimeout(go, 1500);
}
document.addEventListener("click", async e => {
  if (!e.target.closest) return;
  const xb = e.target.closest("button[data-asked-x]"); if (xb) { askedDrop(xb.dataset.askedX); askedBox(); const h = document.querySelector("#home-asked .aq-h") || document.getElementById("search"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } return; }
  const op = e.target.closest("a[data-asked-open]"); if (op) { askedDrop(op.dataset.askedOpen); return; }   // read: it leaves the list (the sheet opens by its data-sheet)
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
    if (ok) { askedSet(it.k, { sent: 1 }); say("Sent. We will check it. It is kept under “Your questions” on the start page."); askedBox(); return; }
  }
  // the page cannot send it (the store is not switched on, or the connection failed): kept on this device, and the email form opens with it
  say("Kept under “Your questions” on this device. To send it to us, use the email form.");
  askedBox(); if (EV.open) closeEvidence(); openFeedback("feedback", location.hash, q);
}, true);
if (typeof window !== "undefined") { if (window.requestIdleCallback) requestIdleCallback(() => askProbe(), { timeout: 3000 }); else setTimeout(askProbe, 1200); }

// for the checks (scripts/ux/insight_check.js, scripts/insight/parity.js): the same functions the search box uses
window.pkInsight = {
  state: () => INS.state, load: insightLoad, encode: t => insEncode(t), expand: t => insExpand(t), mask: t => insMask(t), named: t => insNamed(t), times: () => INS.times.slice(),
  embed: t => insEmbed(t).then(v => Array.from(v)), tiers: () => Object.assign({}, INS.t), weights: () => Object.assign({}, INS.wt), judge: () => JSON.parse(JSON.stringify(INS.judge)),
  read: (t, ctx) => { const r = insRead(t, ctx || {}); return { core: r.core, depth: r.depth, note: r.note, routes: r.routes.map(x => x.kind), groups: r.groups }; },
  rank: (t, ctx) => insRank(t, ctx || {}).then(r => ({ q: r.q, core: r.core, depth: r.depth, note: r.note, emergency: r.emergency, routes: r.routes.map(x => ({ kind: x.kind, t: x.t, href: x.href, el: x.el || null, mix: x.mix || null })),
    best: r.best, related: r.related, judge: r.judge || null, ms: r.ms }))
};
