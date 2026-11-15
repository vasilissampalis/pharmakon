/* ---------- APA 7 rendering (prototype; production uses citeproc-js with the APA CSL style) ---------- */
const refById = Object.fromEntries(REFS.map(r => [r.id, r]));
const cardById = STUDY_CARDS;
// each anchor arrives as [reference, study card, role, anchor status] (site/build.js); the rest of it comes with its substance's file
CLAIMS.forEach(c => { if (c.ev) { c.evidence = c.ev.map(a => ({ reference: a[0], study_card: a[1] || null, role: a[2], anchor_status: a[3] })); delete c.ev; } });
const claimById = Object.fromEntries(CLAIMS.map(c => [c.id, c]));

/* ---------- What loads when (speed, 13 November 2026; the senior author: "every time I open the website… a few seconds pass").
   The page carries what the start page, the drug pages, search and the quiz read: every answer's plain words, grading and
   sources by name. The rest is fetched the first time a view needs it, as study cards already were: data/full-<substance>.json
   (each answer's precise statement, who was studied, the full rating reasoning, the debate, and what each source says and where;
   the drug's law rows; the sources of its names; its study cards' notes), data/refs.json (every reference in full, for the APA
   lists) and data/figures.json (the official figures). Each file is fetched once; a view waits with a quiet line, and if a file
   cannot be had it says so in one line with a way to try again. The current drug's file is fetched ahead once its page settles. */
const LOADS = {};
function loadJson(name, apply) {
  if (!LOADS[name]) LOADS[name] = fetch("data/" + name).then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(d => { apply(d); return true; }).catch(e => { delete LOADS[name]; throw e; });
  return LOADS[name];
}
const FULL_DONE = new Set();
let REFS_DONE = false, FIGURES_DONE = false;
function loadFull(sub) {
  if (!FULL_FILES.includes(sub) || FULL_DONE.has(sub)) return Promise.resolve(true);
  return loadJson("full-" + encodeURIComponent(sub) + ".json", d => {
    Object.entries(d.claims || {}).forEach(([id, h]) => { const c = claimById[id]; if (!c) return; const { grade, verification, evidence, rate, ...rest } = h;
      Object.assign(c, rest); Object.assign(c.grade, grade); Object.assign(c.verification, verification);
      if (rate && (SIMPLE.claims || {})[id]) SIMPLE.claims[id].rate = rate;   // "Why this rating" in plain words
      (evidence || []).forEach((e, i) => { if (c.evidence[i]) Object.assign(c.evidence[i], e); }); c.full = true; });
    if (d.legal) { const L = LEGAL.find(x => x.substance === d.legal.substance); if (L) Object.assign(L, d.legal); }
    if (d.identity) { const I = IDENTITY.find(x => x.substance === d.identity.substance); if (I) Object.assign(I, d.identity); }
    Object.entries(d.cards || {}).forEach(([id, x]) => { const k = cardById[id]; if (k) { k.what_would_settle_it = x.what_would_settle_it; k.verification.source_read = x.source_read; } });
    FULL_DONE.add(sub); });
}
function loadRefs() { return REFS_DONE ? Promise.resolve(true) : loadJson("refs.json", d => { Object.entries(d).forEach(([id, r]) => { if (refById[id]) Object.assign(refById[id], r); }); REFS_DONE = true; }); }
function loadFigures() { return FIGURES_DONE ? Promise.resolve(true) : loadJson("figures.json", d => { EPI_ALL.push(...d); FIGURES_DONE = true; }); }
// what the full text of some answers needs: their substances' files (and any others named), and the references in full
const subsOf = ids => ids.map(id => claimById[id] && claimById[id].substance).filter(Boolean);
function needFull(ids, subs) { return Promise.all([...new Set(subsOf(ids).concat(subs || []))].map(loadFull).concat(loadRefs())); }
const fullReady = (ids, subs) => REFS_DONE && subsOf(ids).concat(subs || []).every(s => FULL_DONE.has(s) || !FULL_FILES.includes(s));
// a part of a page that waits for its file: a quiet line now; the part itself, or one line with a retry, when the fetch ends
const waitHtml = what => '<p class="loading" role="status">' + esc(what) + "…</p>";
const failHtml = (what, retryId) => '<p class="loadfail" role="alert">' + esc(what) + ' could not be loaded. Check your connection and <button type="button" class="linklike" data-retry="' + esc(retryId) + '">try again</button>.</p>';
const RETRY = {};
function whenReady(load, box, what, draw) {
  if (!box) return;
  const id = "r" + Math.random().toString(36).slice(2, 8);
  box.innerHTML = waitHtml("Loading " + what.toLowerCase());
  RETRY[id] = () => whenReady(load, box, what, draw);
  load().then(() => { delete RETRY[id]; if (box.isConnected) draw(); }).catch(() => { if (box.isConnected) box.innerHTML = failHtml(what, id); });
}
// (scripts/check_citations.js reads this file outside a browser, for its APA labels: no page there)
if (typeof document !== "undefined") document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("[data-retry]"); if (!b || !RETRY[b.dataset.retry]) return; const f = RETRY[b.dataset.retry]; delete RETRY[b.dataset.retry]; f(); });
// the words a claim is listed and found by: its plain line, else its precise statement (when fetched), else its opening words
const claimText = c => c.plain || c.statement || c.title || c.id;
// the current drug's file (and the references) fetched ahead, once its page has settled, so its evidence opens at once
let AHEAD = null;
function fetchAhead(sub) {
  if (AHEAD === sub) return; AHEAD = sub;
  const go = () => { if (AHEAD !== sub) return; loadFull(sub).then(loadRefs).catch(() => { AHEAD = null; }); };
  const later = () => (window.requestIdleCallback ? requestIdleCallback(go, { timeout: 3000 }) : setTimeout(go, 1200));
  if (document.readyState === "complete") later(); else window.addEventListener("load", later, { once: true });
}

function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function initials(given) {
  if (!given) return "";
  return given.trim().split(/\s+/).map(part => {
    // run-together initials as Crossref sometimes gives them: "W.S.", "M.G.", "PT", "AC" → one initial per letter
    if (/^([A-Z]\.){2,}$/.test(part) || /^[A-Z]{2,3}$/.test(part) || /^([A-Z]\.)+[A-Z]$/.test(part)) return part.replace(/\./g, "").split("").map(ch => ch + ".").join(" ");
    return part.split("-").map(p => p ? p[0].toUpperCase() + "." : "").join("-");
  }).join(" ");
}
function authorEntry(a) { return a.literal ? a.literal : (a.family + (a.given ? ", " + initials(a.given) : "") + (a.suffix ? ", " + a.suffix : "")); }
function apaAuthors(list) {
  const names = list.map(authorEntry);
  if (names.length === 1) return names[0];
  if (names.length <= 20) return names.slice(0, -1).join(", ") + ", & " + names[names.length - 1];
  return names.slice(0, 19).join(", ") + ", … " + names[names.length - 1];
}
// APA 7: undated works are "n.d."; two works by the same author in the same year (or both undated) take a, b
// suffixes ("2020a", "n.d.-a"), stored as year_suffix on the reference.
function year(ref) {
  const dp = ref.issued && ref.issued["date-parts"];
  const y = dp && dp[0] && dp[0].length ? dp[0][0] : "n.d.";
  return ref.year_suffix ? y + (y === "n.d." ? "-" : "") + ref.year_suffix : y;
}
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
// APA 7: a retrieval date for undated pages whose content is designed to change (contact pages, lists of numbers).
function retrieved(ref) {
  const dp = ref.accessed && ref.accessed["date-parts"] && ref.accessed["date-parts"][0];
  if (!dp || dp.length !== 3 || !String(year(ref)).startsWith("n.d.")) return "";
  return "Retrieved " + MONTHS[dp[1] - 1] + " " + dp[2] + ", " + dp[0] + ", from ";
}
function dash(p) { return String(p).replace(/-/g, "–"); }
// APA 7: a title in another language is followed by its English translation in square brackets, not italicized.
function italicTitle(t) {
  const m = String(t || "").match(/^(.*?)( \[[^\]]+\])$/);
  return m ? "<i>" + esc(m[1]) + "</i>" + esc(m[2]) : "<i>" + esc(t) + "</i>";
}
// Sort key for APA reference lists: undated works (n.d.) before dated ones, then by year, then by a/b suffix.
function yearKey(ref) {
  const y = String(year(ref)), m = y.match(/^(\d{4})-?([a-z]?)$/), n = y.match(/^n\.d\.(?:-([a-z]))?$/);
  return m ? [+m[1], m[2] || ""] : [-1, (n && n[1]) || ""];
}
function byYear(a, b) { const ka = yearKey(a), kb = yearKey(b); return (ka[0] - kb[0]) || ka[1].localeCompare(kb[1]); }
// APA 7: a web page takes the most exact date it gives ("2026, June 30"); every other work its year
function dateOf(ref) {
  const dp = ref.issued && ref.issued["date-parts"] && ref.issued["date-parts"][0];
  return ref.type === "webpage" && dp && dp.length >= 2 && dp[1] >= 1 && dp[1] <= 12 ? year(ref) + ", " + MONTHS[dp[1] - 1] + (dp.length > 2 ? " " + dp[2] : "") : year(ref);
}
function apaReference(ref) {
  const y = dateOf(ref);
  const link = ref.DOI ? "https://doi.org/" + ref.DOI : (ref.URL || "");
  const au = apaAuthors(ref.author);
  const endP = t => /[.?!]$/.test(String(t || "").trim()) ? "" : ".";
  // APA 7 §9.12: a work with no author starts with its title, which is then not repeated
  let html = ref.no_author ? esc(ref.title) + endP(ref.title) + " (" + y + "). " : esc(au) + (au.endsWith(".") ? "" : ".") + " (" + y + "). ";
  if (ref.type === "article-journal") {
    html += (ref.no_author ? "" : esc(ref.title) + endP(ref.title) + " ") + "<i>" + esc(ref["container-title"]) + (ref.volume ? ", " + esc(ref.volume) : "") + "</i>" + (ref.issue ? "(" + esc(dash(ref.issue)) + ")" : "") + (ref.page ? ", " + esc(dash(ref.page)) : ref.number ? ", Article " + esc(ref.number) : "") + ". ";
    if (!ref.volume && !ref.page && !ref.number) html += "Advance online publication. ";
  } else {
    // reports and web pages: italic title, then the report number and a bracketed description (APA 7), then the publisher or site when it is not the author
    const extra = (ref.number ? " (" + esc(ref.number) + ")" : "") + (ref.genre ? " [" + esc(ref.genre) + "]" : "");
    html += italicTitle(ref.title) + extra + (extra ? "." : endP(ref.title)) + " " + (ref.publisher && ref.publisher !== ref.author[0].literal ? esc(ref.publisher) + ". " : "");
  }
  if (link) html += (ref.DOI ? "" : retrieved(ref)) + '<a href="' + esc(link) + '" target="_blank" rel="noopener">' + esc(link) + "</a>";
  // APA 7: a retracted article keeps its own details, then the retraction in parentheses (from the notice's Crossref record)
  const rn = ref.retraction_notice;
  if (rn) html += " (Retraction published " + esc(rn.year) + ", <i>" + esc(rn["container-title"]) + (rn.volume ? ", " + esc(rn.volume) : "") + "</i>" + (rn.issue ? "[" + esc(rn.issue) + "]" : "") + (rn.page ? ", " + esc(dash(rn.page)) : "") + ")";
  return html;
}
// In-text form with APA 7 disambiguation: extend surnames until the form is unique among the cited set.
// APA 7: a work with no author is cited by the first few words of its title, in title case and quotation marks
const MINOR_WORDS = new Set("a an and as at but by for if in nor of off on or per so the to up via yet".split(" "));
function shortTitleCase(title) {
  const head = String(title || "").split(/[:.?!]/)[0].trim().split(/\s+/);
  const words = head.length > 5 ? head.slice(0, 4) : head;
  return words.map((w, i) => (i > 0 && MINOR_WORDS.has(w.toLowerCase())) ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
}
function inTextLabel(ref, pool) {
  const au = ref.author.map(a => a.literal || a.family);
  const y = year(ref);
  if (ref.no_author) return "\u201C" + (ref.short_title || shortTitleCase(ref.title)) + ",\u201D " + y;
  if (au.length === 1) return (ref.author[0].short || au[0]) + ", " + y;
  if (au.length === 2) return au[0] + " & " + au[1] + ", " + y;
  const rivals = pool.filter(r => r.id !== ref.id && year(r) === y && (r.author[0].literal || r.author[0].family) === au[0] && r.author.length >= 3);
  let k = 1;
  const prefix = (r, n) => r.author.slice(0, n).map(a => a.literal || a.family).join("|");
  while (k < au.length - 1 && rivals.some(r => prefix(r, k) === prefix(ref, k))) k++;
  if (k === 1) return au[0] + " et al., " + y;
  return au.slice(0, k).join(", ") + ", et al., " + y;
}
// where a citation leads when clicked: the article's own page (its DOI), or the source's address
function refLink(ref) { return ref.DOI ? "https://doi.org/" + ref.DOI : (ref.URL || "#ref-" + ref.id); }
function cite(id) {
  const ref = refById[id];
  if (!ref) return '<span class="placeholder">[missing reference: ' + esc(id) + "]</span>";
  return '<a class="pop" href="' + esc(refLink(ref)) + '" target="_blank" rel="noopener" data-ref="' + esc(id) + '">(' + esc(inTextLabel(ref, REFS)) + ")</a>";
}
// Several works in one parenthesis, in alphabetical order (APA 7): (Author A, 2001; Author B, n.d.).
function cites(ids) {
  const items = ids.map(id => [id, refById[id]]);
  if (items.some(([, r]) => !r)) return items.map(([id]) => cite(id)).join(" ");
  items.sort((a, b) => inTextLabel(a[1], REFS).localeCompare(inTextLabel(b[1], REFS)));
  return "(" + items.map(([id, r]) => '<a class="pop" href="' + esc(refLink(r)) + '" target="_blank" rel="noopener" data-ref="' + esc(id) + '">' + esc(inTextLabel(r, REFS)) + "</a>").join("; ") + ")";
}
// Replace author-year mentions inside debate prose with live citations: (Hart et al., 2012) → link.
function liveCites(text) {
  return esc(text).replace(/\(([^()]*?\d{4}[a-z]?)\)/g, (m, inner) => {
    // split at the semicolons between citations, not at the one inside an escaped "&amp;" ("Curran &amp; Morgan, 2000")
    const parts = inner.split(/(?<!&(?:amp|lt|gt|quot|#39));/).map(s => s.trim());
    // the text is already escaped, so compare escaped labels ("Curran &amp; Morgan, 2000") and do not escape p again
    const link = (p, shown) => {
      const found = REFS.find(r => esc(inTextLabel(r, REFS)) === p);
      return found ? '<a class="pop" href="' + esc(refLink(found)) + '" target="_blank" rel="noopener" data-ref="' + esc(found.id) + '">' + shown + "</a>" : null;
    };
    const out = parts.map(p => {
      const one = link(p, p);
      if (one) return one;
      // APA 7: the same authors with several years, "(Hughes &amp; Stevens, 2010, 2012)": one link per year
      const multi = p.match(/^(.*?), (\d{4}[a-z]?(?:, \d{4}[a-z]?)+)$/);
      if (!multi) return p;
      const years = multi[2].split(", ");
      const links = years.map((y, i) => link(multi[1] + ", " + y, i === 0 ? multi[1] + ", " + y : y));
      return links.every(Boolean) ? links.join(", ") : p;
    });
    return "(" + out.join("; ") + ")";
  });
}
/* Long research texts in short pieces (senior author, 13 November 2026: the full findings were "too overwhelming, nobody will
   read it"). The checked words stay exactly as they are; only the layout changes: the opening summary sentence on its own, then
   one paragraph per study (a paragraph ends where a citation closes a sentence), and a long paragraph whose parts are joined by
   semicolons becomes a list (the semicolons become the list's breaks). Splits never fall inside brackets. Short texts are left whole. */
const PIECE_ABBR = /(?:^|[\s(])(?:e\.g|i\.e|et al|vs|cf|approx|ca|No|Nos|Fig|Figs|Vol|pp?|St|Dr|Mr|Mrs|Ms|Prof|Inc|Ltd|Co|Jr|Sr|U\.S|U\.K|[A-Z])$/;
function pieceSplit(t, sep) {
  const out = []; let depth = 0, last = 0;
  for (let i = 0; i < t.length; i++) {
    const ch = t[i];
    if (ch === "(" || ch === "[") depth++;
    else if ((ch === ")" || ch === "]") && depth > 0) depth--;
    else if (depth === 0 && t.startsWith(sep, i)) { out.push(t.slice(last, i)); last = i + sep.length; i += sep.length - 1; }
  }
  out.push(t.slice(last)); return out.map(s => s.trim()).filter(Boolean);
}
function pieceSentences(t) {
  const out = []; let depth = 0, last = 0;
  for (let i = 0; i < t.length - 2; i++) {
    const ch = t[i];
    if (ch === "(" || ch === "[") depth++;
    else if ((ch === ")" || ch === "]") && depth > 0) depth--;
    else if (depth === 0 && ch === "." && t[i + 1] === " " && /[A-Z“"‘']/.test(t[i + 2]) && !PIECE_ABBR.test(t.slice(Math.max(0, i - 8), i))) { out.push(t.slice(last, i + 1)); last = i + 2; }
  }
  out.push(t.slice(last)); return out.map(s => s.trim()).filter(Boolean);
}
const pieceWords = s => s.split(/\s+/).filter(Boolean).length;
// a sentence that ends with a citation: (Grant & Dawson, 1997). or (Irons et al., 2015; Smith, 2001).
const pieceCited = s => /\([^()]*\b(?:1[89]|20)\d\d[a-z]?\b[^()]*\)\.$/.test(s);
function inPieces(text, cites) {
  const t = String(text == null ? "" : text).trim(); if (!t) return "";
  const tailM = t.match(/\s(Certainty: [^.]{1,40}\.(?:\s+Status: [^.]{1,40}\.)?)$/);
  const body = tailM ? t.slice(0, tailM.index).trim() : t;
  const sents = pieceSentences(body);
  if (pieceWords(body) < 90 || sents.length < 2 && pieceSplit(body, "; ").length < 3) return "<p>" + cites(t) + "</p>";
  const groups = []; let cur = [];
  // the opening summary stands alone (in bold) when it is short, cites nothing and more follows; a long opening finding stays running text
  let start = 0; if (sents.length > 2 && pieceWords(sents[0]) <= 32 && !pieceCited(sents[0]) && !/\(\D*\d{4}/.test(sents[0])) { groups.push({ lead: true, s: [sents[0]] }); start = 1; }
  for (let i = start; i < sents.length; i++) { cur.push(sents[i]); if (pieceCited(sents[i])) { groups.push({ s: cur }); cur = []; } }
  if (cur.length) { const prev = groups.length && !groups[groups.length - 1].lead ? groups[groups.length - 1] : null; if (prev) prev.s.push(...cur); else groups.push({ s: cur }); }
  // inside a paragraph, a long sentence made of three or more parts joined by semicolons becomes a list; the rest stays running text
  const listOf = sent => { const parts = pieceSplit(sent, "; "); if (pieceWords(sent) < 40 || parts.length < 3) return null;
    const first = pieceSplit(parts[0], ": "); let lead = "", items = parts;
    if (first.length >= 2) { const at = parts[0].indexOf(first[1], first[0].length); lead = parts[0].slice(0, at).trim(); items = [parts[0].slice(at)].concat(parts.slice(1)); }
    return { lead, items }; };
  const html = groups.map(g => {
    if (g.lead) return '<p class="pc-lead">' + cites(g.s.join(" ")) + "</p>";
    let out = "", run = [];
    const flush = () => { if (run.length) out += '<p class="pc-p">' + cites(run.join(" ")) + "</p>"; run = []; };
    // running text breaks between sentences once a paragraph passes about 90 words
    for (const sent of g.s) { const l = listOf(sent); if (!l) { if (run.length && pieceWords(run.join(" ") + " " + sent) > 90) flush(); run.push(sent); continue; }
      if (l.lead) run.push(l.lead); flush(); out += '<ul class="pc-list">' + l.items.map(x => "<li>" + cites(x) + "</li>").join("") + "</ul>"; }
    flush(); return '<div class="pc-group">' + out + "</div>";
  }).join("");
  return '<div class="pc">' + html + (tailM ? '<p class="pc-tail">' + cites(tailM[1]) + "</p>" : "") + "</div>";
}

/* ---------- GRADE ---------- */
const GRADE_LEVELS = { high: 4, moderate: 3, low: 2, "very-low": 1 };
function gradeDots(cert) {
  const n = GRADE_LEVELS[cert] || 1;
  let s = '<span class="dots" aria-hidden="true">';
  for (let i = 1; i <= 4; i++) s += '<i class="' + (i <= n ? "on" : "") + '"></i>';
  return s + "</span>";
}
function gradeLabel(cert) { return cert.replace("-", " "); }
function gradeDomains(g) {
  const d = g.domains; const parts = [];
  const down = ["risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"];
  const up = ["large_effect", "dose_response", "plausible_confounding"];
  down.forEach(k => { if (d[k] && d[k].levels) parts.push("−" + d[k].levels + " " + k.replace(/_/g, " ")); });
  up.forEach(k => { if (d[k] && d[k].levels) parts.push("+" + d[k].levels + " " + k.replace(/_/g, " ")); });
  return "starts " + g.starting_level + (parts.length ? " · " + parts.join(" · ") : " · no adjustments");
}
