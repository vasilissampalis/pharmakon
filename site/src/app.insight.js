/* ---------- Insight (site 2.2.0, 14 November 2026; the senior author: the site should feel like your own thinking). The
   search box also understands a question asked in a reader's own words, on the reader's own phone: nothing typed leaves it.
   A small open model (all-MiniLM-L6-v2, int8; Apache-2.0) turns the question into numbers with ONNX Runtime Web (MIT), both
   published with the site, unmodified (site/insight/vendor; hashes in scripts/insight/MODELS.md), and those numbers are
   compared with every wording of every question on the site and its short answer, made into numbers with the same model when
   the site is built (data/insight.json, scripts/insight/build_index.py). Score: 0.7 x the best wording, 0.3 x the short answer,
   0.2 x the words in common; a street or brand name brings the drug's own name along (as scripts/insight/tune.py tuned it).
   The files (about 38 MB) are fetched only when someone puts the cursor in the search box or types in it, never with the page.
   Word search stays as it was and answers at once; when Insight is ready, the top of the results becomes "Answers that fit
   your question" (up to three checked answers, from a question of three words or more), or, when nothing fits well enough,
   "We haven't checked this yet" with the way to ask us. Nothing is ever written by the model: it only finds checked answers.
   An answer opened from there opens over the page: for an answer with a checked myth-or-fact statement, a guess first
   (skippable), then the reveal; safety answers (mixing, drug checking, section 6 Acute risks, overdose) open at once; then up
   to three next questions, and after four answers in a row a calm end. ---------- */
const INS = { state: "idle", tries: 0, cache: new Map(), seq: 0, timer: 0, times: [], queue: Promise.resolve(), run: null, view: null, back: null };
const INS_WAIT = 150;       // ms of no typing before a question is looked up (each keystroke still gets the word search at once)
const INS_WORDS = 3;        // a question of three words or more; a drug's name alone is for the word search
const INS_END = 4;          // the calm end comes after four answers in a row
const INS_BASE = () => new URL("insight/", document.baseURI).href;

/* Loading, on first use. One thread (no cross-origin isolation is needed); the WebGPU build is never fetched. */
function insScript(src) {
  return new Promise((ok, fail) => { const s = document.createElement("script"); s.src = src; s.async = true; s.onload = () => ok(); s.onerror = () => fail(new Error("script " + src)); document.head.appendChild(s); });
}
function insightLoad() {
  if (INS.state !== "idle") return INS.loading || Promise.resolve(INS.state === "ready");
  if (typeof WebAssembly !== "object" || typeof BigInt64Array === "undefined" || typeof fetch !== "function") { INS.state = "off"; return Promise.resolve(false); }
  INS.state = "loading"; INS.tries++;
  const base = INS_BASE(), get = (u, how) => fetch(u).then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r[how](); });
  const session = insScript(base + "ort.wasm.min.js").then(() => {
    const ort = window.ort; ort.env.wasm.numThreads = 1; ort.env.wasm.proxy = false; ort.env.wasm.wasmPaths = base; ort.env.logLevel = "error";
    return get(base + "all-MiniLM-L6-v2-q8.onnx", "arrayBuffer").then(b => ort.InferenceSession.create(new Uint8Array(b), { executionProviders: ["wasm"], graphOptimizationLevel: "all" }));
  });
  INS.loading = Promise.all([get("data/insight.json", "json"), get(base + "vocab.txt", "text"), session])
    .then(([data, vocab, s]) => { insPrepare(data, vocab); INS.session = s; return insEmbed("warm up"); })
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
function insPrepare(d, vocabText) {
  INS.dim = d.dim; INS.ids = d.ids; INS.rows = d.rows; INS.th = d.threshold; INS.also = d.also; INS.wt = d.weights;
  INS.W = insRows(d.W, d.dim); INS.S = insRows(d.S, d.dim); INS.next = d.next;
  INS.idx = new Map(d.ids.map((id, i) => [id, i])); INS.safe = new Set((d.safety || []).map(i => d.ids[i]));
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
  // drug names (tune.py's expand): each drug's slug, the parts of its name and its street names of three letters or more
  INS.drugs = SUBSTANCES.map(s => {
    const ns = new Set([s.slug.replace(/-/g, " ")]);
    s.name.split(/[()\/,;]| and /).forEach(p => { p = p.trim().toLowerCase(); if (p.length >= 3) ns.add(p); });
    (ALIASES[s.slug] || []).forEach(a => { if (a.length >= 3) ns.add(a.toLowerCase()); });
    const alt = [...ns].sort((a, b) => b.length - a.length).map(n => n.replace(/[.*+?^${}()|[\]\\\/-]/g, "\\$&")).join("|");
    return { slug: s.slug, canon: s.name.split(" (")[0], re: new RegExp("(?<![\\p{L}\\p{N}_])(?:" + alt + ")(?![\\p{L}\\p{N}_])", "u") };
  }).sort((a, b) => (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0));
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

/* The match: every answer scored; the best three that fit, or none when the best is under the threshold */
async function insRank(q) {
  const t0 = performance.now(), v = await insEmbed(insExpand(q)), dim = INS.dim, nA = INS.ids.length;
  const best = new Float32Array(nA).fill(-1);
  for (let k = 0; k < INS.rows.length; k++) { let s = 0; const o = k * dim; for (let j = 0; j < dim; j++) s += v[j] * INS.W[o + j]; if (s > best[INS.rows[k]]) best[INS.rows[k]] = s; }
  const lex = new Float32Array(nA), qv = new Map();
  insTok(q).forEach(w => { if (INS.idf.has(w)) qv.set(w, (qv.get(w) || 0) + INS.idf.get(w)); });
  const qn = Math.sqrt([...qv.values()].reduce((a, x) => a + x * x, 0)) || 1;
  qv.forEach((x, w) => INS.post.get(w).forEach(([i, y]) => { lex[i] += (x / qn) * y; }));
  const sc = new Float32Array(nA);
  for (let i = 0; i < nA; i++) { let s = 0; const o = i * dim; for (let j = 0; j < dim; j++) s += v[j] * INS.S[o + j]; sc[i] = INS.wt.q * best[i] + INS.wt.short * s + INS.wt.words * lex[i]; }
  const order = [...sc.keys()].sort((a, b) => sc[b] - sc[a]).slice(0, 3);
  const top = sc[order[0]] >= INS.th ? order.filter((i, k) => k === 0 || sc[i] >= INS.also) : [];
  const ms = performance.now() - t0; INS.times.push(ms);
  return { top, best: sc[order[0]], scores: order.map(i => +sc[i].toFixed(4)), cand: order, ms };
}

/* In the search results */
const insQ = id => anyQuestion(id) || ((SIMPLE.claims || {})[id] || {}).q || claimText(claimById[id]);
const insWordsIn = q => (q.match(/[\p{L}\p{N}]+/gu) || []).length;
const insNoteText = () => "Runs on your " + (window.matchMedia && window.matchMedia("(pointer: coarse)").matches ? "phone" : "computer") + ". Nothing you type leaves it.";
function insFitHtml(q, res) {
  if (!res.top.length) return '<p class="sr-fit-none"><b>We haven’t checked this yet.</b> <button type="button" class="linklike" data-fb="feedback" data-fb-text="' + esc(q) + '">Ask us</button></p>';
  return '<div class="sr-fit"><p class="sr-fit-h">Answers that fit your question</p>' + res.top.map(i => {
    const id = INS.ids[i], c = claimById[id], sp = SIMPLE.claims[id], w = mfWhere(answerPageKey(id) || c.substance);
    return '<a class="sr-ans sr-fit-a" href="' + esc(answerAddr(id)) + '" data-insight="' + esc(id) + '"><span class="k">' + esc(w.name) + '</span><span class="t">' + esc(insQ(id)) +
      '</span><span class="a">' + esc(glanceClause(sp.short)) + '</span><span class="m">' + meterHtml(c.grade.certainty, true) + "</span></a>";
  }).join("") + "</div>";
}
function insInject(box, q, res) {
  box.querySelectorAll(".sr-fit, .sr-fit-none").forEach(e => e.remove());
  const html = insFitHtml(q, res);
  if (res.top.length) {   // an answer shown here is not repeated below, and "No match" no longer applies
    res.top.forEach(i => box.querySelectorAll('a.sr-ans[data-cid="' + INS.ids[i] + '"]').forEach(a => a.remove()));
    const none = box.querySelector(":scope > .none"); if (none) none.remove();
  } else if (box.querySelector(":scope > .none")) { const ask = box.querySelector(":scope > .sr-ask"); if (ask) ask.remove(); }
  // an emergency stays first; then these answers, under the quiet line
  const first = box.querySelector(":scope > a"), note = box.querySelector(":scope > .sr-note");
  if (first && first.getAttribute("href") === "#emergency" && first === box.querySelector(":scope > :not(.sr-note)")) first.insertAdjacentHTML("afterend", html);
  else if (note) note.insertAdjacentHTML("afterend", html); else box.insertAdjacentHTML("afterbegin", html);
  const live = document.getElementById("search-count");
  if (live) live.textContent = res.top.length ? res.top.length + " answer" + (res.top.length === 1 ? "" : "s") + " that fit your question" : "We haven’t checked this yet";
}
// called by runSearch after the word search has drawn its results
function insightAfterSearch(raw) {
  if (INS.state !== "ready") return;
  const box = document.getElementById("search-results"); if (!box || box.hidden) return;
  if (!box.querySelector(":scope > .sr-note")) box.insertAdjacentHTML("afterbegin", '<p class="sr-note">' + icon("mobile") + "<span>" + esc(insNoteText()) + "</span></p>");
  const q = String(raw || "").trim().replace(/\s+/g, " "); clearTimeout(INS.timer);
  if (insWordsIn(q) < INS_WORDS) { INS.seq++; return; }
  const key = q.toLowerCase(), have = INS.cache.get(key);
  if (have) { INS.seq++; insInject(box, q, have); return; }
  const seq = ++INS.seq;
  INS.timer = setTimeout(() => insRank(q).then(res => {
    INS.cache.set(key, res); if (INS.cache.size > 60) INS.cache.delete(INS.cache.keys().next().value);
    const s = document.getElementById("search"), b = document.getElementById("search-results");
    if (seq !== INS.seq || !s || s.value.trim().replace(/\s+/g, " ") !== q || !b || b.hidden) return;   // the reader has typed on
    insInject(b, q, res);
  }).catch(() => {}), INS_WAIT);
}
// once ready, the results already open take their answers
function insightReady() {
  const s = document.getElementById("search"), box = document.getElementById("search-results");
  if (s && box && !box.hidden && (document.activeElement === s || s.value.trim())) runSearch(s.value);
}
(function () {
  const s = document.getElementById("search"); if (!s) return;
  s.addEventListener("focus", insightLoad); s.addEventListener("input", insightLoad);
})();

/* One answer at a time, over the page (the sheet the evidence opens in, with its Back button and the phone's own Back) */
function insGuessFor(id) {
  if (INS.safe.has(id) || !qzOk(id) || QZS.claims.includes(id)) return null;
  const xs = mfPool().filter(x => x.claim === id); if (!xs.length) return null;
  const seen = qzSeen(); return xs.find(x => !seen.has(x.key)) || xs[0];
}
function insSos(id) {
  if (claimById[id].section !== 6 && !/overdos/i.test(insQ(id))) return "";
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  return '<p class="dh-help ins-sos">' + icon("phone") + "<span>Someone unwell? " + (em ? 'Emergency: <a href="tel:' + esc(telOf(em.numbers[0])) + '">' + esc(em.numbers[0].n) + "</a> · " : "") + '<a href="#emergency">Emergency numbers</a></span></p>';
}
function insNextHtml(id) {
  const had = new Set(INS.run.ids), nx = (INS.next[INS.idx.get(id)] || []).filter(x => !had.has(x) && claimById[x] && (SIMPLE.claims || {})[x]).slice(0, 3);
  if (!nx.length) return "";
  return '<div class="rn ins-next"><p class="rn-k">Next questions</p><ul class="rn-l">' + nx.map(x => '<li><a href="' + esc(answerAddr(x)) + '" data-insight-next="' + esc(x) + '"><span>' + esc(insQ(x)) + "</span>" + icon("arrow") + "</a></li>").join("") + "</ul></div>";
}
function insEndHtml() {
  const n = INS.run.ids.length;
  return '<div class="ins-end"><p class="ins-end-t">You’ve read ' + n + " answers</p><p class=\"ins-end-s\">Ask something else, or keep going with questions like these.</p>" +
    '<div class="ins-end-b"><button type="button" class="qz2-nb" data-ins-ask>Ask something else</button><button type="button" class="linklike" data-ins-more>Keep reading</button></div></div>';
}
function insHtml(id, st) {
  const c = claimById[id], sp = SIMPLE.claims[id], w = mfWhere(answerPageKey(id) || c.substance);
  const bar = '<div class="ev-bar"><button type="button" class="ev-back">' + icon("arrow") + '<span>Back</span></button><span class="ev-eye ins-eye">' + icon(w.f.icon) + "<span>" + esc(w.name) + "</span></span></div>";
  const head = '<h2 id="ev-title" tabindex="-1">' + esc(insQ(id)) + "</h2>";
  if (st.stage === "guess") return bar + '<div class="ins">' + head + '<div class="ins-guess"><p class="ins-k" id="ins-k">First, a guess: myth or fact?</p><p class="qz2-q ins-q">' + esc(st.x.q) + "</p>" +
    '<div class="qz2-opts mf-opts" role="group" aria-labelledby="ins-k"><button type="button" class="qz2-o" data-ins-guess="myth">Myth</button><button type="button" class="qz2-o" data-ins-guess="fact">Fact</button></div>' +
    '<button type="button" class="linklike ins-skip" data-ins-skip>Skip to the answer</button></div></div>';
  const x = st.x, verdict = x ? '<div class="ins-verdict ' + (x.fact ? "fact" : "myth") + (st.anim ? " just" : "") + '"><p class="mf-v" tabindex="-1">' + icon(x.fact ? "check" : "x") + "<b>" + (x.fact ? "Fact" : "Myth") + "</b>" +
    (st.pick ? ' <span class="mf-fb">' + (st.pick.ok ? "Right!" : "Not quite.") + "</span>" : "") + '</p><p class="mf-said">“' + esc(x.q) + "”</p>" + (x.why ? '<p class="qz2-why">' + esc(x.why) + "</p>" : "") + "</div>" : "";
  const addr = answerAddr(id), pl = sharedPlace(answerPageKey(id) || "", id);
  const page = /^#cl_/.test(addr) ? '<a class="qz2-ev" href="' + esc(pl.href) + '">' + esc(pl.more) + " " + icon("arrow") + "</a>" : '<a class="qz2-ev" href="' + esc(addr) + '">See it on the ' + esc(w.name) + " page " + icon("arrow") + "</a>";
  const tail = INS.run.ids.length - INS.run.more >= INS_END ? insEndHtml() : insNextHtml(id);
  // the answer as everywhere on the site: the short answer, its "But", the picture, an early draft's reason, How do we know?, the bars
  return bar + '<div class="ins">' + head + insSos(id) + verdict + '<div class="ins-ans">' + answerBody(id, c, sp, false) + "</div>" + '<p class="ins-page">' + page + "</p>" + tail + "</div>";
}
function insDraw(id, st, opener) {
  const sh = document.getElementById("evsheet"), panel = sh && sh.querySelector(".panel"); if (!panel) return false;
  if (!EV.open) { EV.opener = opener || document.activeElement; try { history.pushState({ pkEvidence: id }, ""); EV.pushed = true; } catch (e) { EV.pushed = false; } }
  // (an evidence still on its way for this sheet is not drawn over the answer: openEvidence draws only for its own EV.id)
  EV.id = "ins:" + id; EV.open = true; sh.classList.add("open"); document.documentElement.classList.add("sheet-open"); hidePop(); closeSearch();
  INS.view = { id, st }; INS.back = null;
  panel.innerHTML = insHtml(id, st); panel.scrollTop = 0;
  if (st.stage !== "guess") markSeen(id);
  const f = panel.querySelector(st.anim ? ".mf-v" : "#ev-title"); if (f) f.focus({ preventScroll: true });
  return true;
}
function openInsight(id, opener, fresh) {
  if (!claimById[id] || !(SIMPLE.claims || {})[id]) return false;
  if (fresh || !INS.run || !EV.open) INS.run = { ids: [], more: 0 };
  if (INS.run.ids[INS.run.ids.length - 1] !== id) INS.run.ids.push(id);
  const x = insGuessFor(id);
  return insDraw(id, x ? { stage: "guess", x } : { stage: "answer" }, opener);
}
// an answer that fits, tapped in the results: it opens over the page (a new tab, or a link opened another way, goes to its page)
document.getElementById("search-results").addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("a[data-insight]"); if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  if (openInsight(a.dataset.insight, a, true)) { e.preventDefault(); e.stopPropagation(); }
});
document.addEventListener("click", e => {
  const t = e.target.closest && e.target.closest("#evsheet [data-ins-guess], #evsheet [data-ins-skip], #evsheet [data-ins-ask], #evsheet [data-ins-more]");
  const v = INS.view; if (!t || !v || !EV.open) return;
  if (t.hasAttribute("data-ins-guess")) {
    const x = v.st.x, ok = (t.dataset.insGuess === "fact") === x.fact;
    if (!QZS.claims.includes(x.claim)) { QZS.claims.push(x.claim); qzSave(); }
    qzMark(x.key); qzAgainSet(x.key, !ok);
    insDraw(v.id, { stage: "answer", x, pick: { ok }, anim: true }); return;
  }
  if (t.hasAttribute("data-ins-skip")) { if (!QZS.claims.includes(v.id)) { QZS.claims.push(v.id); qzSave(); } insDraw(v.id, { stage: "answer", x: v.st.x }); return; }
  if (t.hasAttribute("data-ins-ask")) { closeEvidence(); const s = document.getElementById("search"); if (s) { s.value = ""; s.focus(); } return; }
  if (t.hasAttribute("data-ins-more")) { INS.run.more = INS.run.ids.length; const box = t.closest(".ins-end"); if (box) box.outerHTML = insNextHtml(v.id) || ""; const f = document.querySelector("#evsheet .ins-next a"); if (f) f.focus(); }
});
// before the page's own handlers (capture): a next question opens here (its address may be a mixing answer's evidence, which
// the evidence handler would open); the evidence opened from an answer here comes back to the answer with its Back button
document.addEventListener("click", e => {
  if (!e.target.closest || !EV.open) return;
  const sheet = document.getElementById("evsheet"), ins = sheet && sheet.querySelector(".panel .ins");
  const nx = ins && e.target.closest("#evsheet [data-insight-next]");
  if (nx) { if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); e.stopPropagation(); openInsight(nx.dataset.insightNext, null, false); return; }
  if (ins && e.target.closest('#evsheet .ins a[href^="#cl_"]')) { INS.back = INS.view; return; }
  if (!ins && INS.back && e.target.closest("#evsheet .ev-back")) {
    e.preventDefault(); e.stopPropagation();
    const v = INS.back; INS.back = null; insDraw(v.id, Object.assign({}, v.st, { anim: false }));
  }
}, true);
// for the checks (scripts/ux/insight_check.js, scripts/insight/parity.js): the same functions the search box uses
window.pkInsight = {
  state: () => INS.state, load: insightLoad, encode: t => insEncode(t), expand: t => insExpand(t), times: () => INS.times.slice(),
  embed: t => insEmbed(t).then(v => Array.from(v)),
  rank: t => insRank(t).then(r => ({ ids: r.top.map(i => INS.ids[i]), cand: r.cand.map(i => INS.ids[i]), scores: r.scores, best: r.best, ms: r.ms }))
};
