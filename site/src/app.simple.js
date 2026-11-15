/* ---------- The simple layer (senior author, 23 October: "it should not overwhelm the average user; my mother must
   understand it"). Every drug page asks the same questions in the same order, one at a time, in plain words, with a photo
   first and the evidence one tap away. The full evidence page stays at #s-<drug>/evidence. ---------- */

const FAMPLAIN = (typeof FAMILIES_PLAIN !== "undefined" && FAMILIES_PLAIN) || { families: {} };
const famPlain = cls => (FAMPLAIN.families || {})[cls] || null;
const MIXFOR = (typeof MIX_DRUGS !== "undefined" && MIX_DRUGS) || {};
// the answers on test kits that each drug's Test it first card shows, in the editors' order (data/site/kits-for.json:
// navigation only, it asserts nothing), and, the other way round, the drug pages each answer belongs to
const KITSBY = (typeof KITS_FOR !== "undefined" && KITS_FOR) || {};
const KITSFOR = {}; Object.entries(KITSBY).forEach(([slug, ids]) => ids.forEach(id => { (KITSFOR[id] = KITSFOR[id] || []).push(slug); }));
const DC = "drug-checking", GEN = "general";  // the drug checking page and the facts page carry answers of their own

/* Which part of the page a topic of questions belongs to */
function topicZone(t) {
  if (/^before|day after|after stopping/i.test(t)) return "after";  // before and during use, after-effects and what people do about them, and the weeks after stopping (decisions p-day-after, p-before-during-after)
  if (/feel/i.test(t)) return "feel";
  if (/mix/i.test(t)) return "mix";
  if (/as a medicine|treatment/i.test(t)) return "med";
  return "risk";
}
// questions of a drug, as [claimId, question, topic], only for answers that are on the site
function drugQuestions(slug) {
  return (QUESTIONS[slug] || []).flatMap(g => g.items.map(([id, q]) => [id, q, g.topic])).filter(([id]) => claimById[id]);
}
// one from each topic first, then the rest: the first few questions cover the most ground
function roundRobin(items) {
  const by = []; const keys = [];
  items.forEach(it => { const k = it[2]; let i = keys.indexOf(k); if (i < 0) { keys.push(k); by.push([]); i = keys.length - 1; } by[i].push(it); });
  const out = []; for (let r = 0; out.length < items.length; r++) by.forEach(list => { if (list[r]) out.push(list[r]); });
  return out;
}
// what people ask about most first (the senior author, 13 November: put what people actually ask first, "if something is too
// clinical and boring, people leave"). DEMAND scores an answer up to 100 by how much the most popular questions people post
// ask about it (data/site/demand.json); the other answers have no score (-1 here). A list in this order keeps every answer:
// the scored ones first, highest first, then the rest, each in the order it had.
const demandOf = id => { const d = typeof DEMAND !== "undefined" && DEMAND[id]; return d && typeof d.score === "number" ? d.score : -1; };
const byDemand = items => items.map((it, i) => [it, i]).sort((a, b) => demandOf(b[0][0]) - demandOf(a[0][0]) || a[1] - b[1]).map(([it]) => it);
function mixQuestions(slug) {
  const own = drugQuestions(slug).filter(([, , t]) => topicZone(t) === "mix");
  const fromMix = (QUESTIONS.interactions || []).flatMap(g => g.items).filter(([id]) => claimById[id] && (MIXFOR[id] || []).includes(slug)).map(([id, q]) => [id, q, "mix"]);
  const seen = new Set(); return own.concat(fromMix).filter(([id]) => !seen.has(id) && seen.add(id));
}

// the catch reads on from "But": "But the volunteers were healthy", keeping capitals on names and acronyms
const BUT_LC = new Set("The Only These This That Those One It Its Most Nobody There Neither Scans Both Many Almost Each How All Researchers Some No Not Studies Study Flatness Compared None They Fewer Very In We Three Two Four Five Small Death Healthy Voluntary Smoking Alcohol People Few Little Even Results Data After Before When While Without With Among Women Men Children Users Trials Animal Animals Long Short Most Much Older Younger A Another For Gene Mostly Whether Six Seven Eight Nine Ten Twelve".split(" "));
// after "But", an ordinary first word is lowercased ("But strength was guessed…"); names of places, peoples and languages keep their capital
const BUT_KEEP = new Set("Swedish Danish Norwegian Finnish Dutch German French Greek Italian Spanish British English Scottish Welsh Irish American Australian Canadian European Brazilian Swiss Sweden Denmark Norway Finland Germany France Greece Italy Spain Britain England Scotland Wales Ireland America Australia Canada Europe Brazil Switzerland London Basel".split(" "));
const butText = t => { const w = String(t).split(/[ ,:;]/)[0]; return BUT_LC.has(w) || (/^[A-Z][a-z'’-]+$/.test(w) && !BUT_KEEP.has(w)) ? t.charAt(0).toLowerCase() + t.slice(1) : t; };
// The key number of a short answer in bold, so the eye lands on it first (signals help readers find the point: WRITING-RULES,
// Schneider et al. 2018; Lorch 1989). Takes escaped text; years, the "100" of "a few in 100" and a bare small number are skipped.
const CUE_RE = /\b((?:about|around|nearly|almost|over|under|more than|less than|fewer than|up to|at least|roughly|only|just)\s+)?(\d+(?:[.,]\d+)*(?:\s*(?:to|-|–)\s*\d+(?:[.,]\d+)*)?)(\s*(?:%|per ?cent\b|in\s+(?:every\s+)?\d+(?:[.,]\d+)*|out of\s+\d+(?:[.,]\d+)*|of\s+\d+(?:[.,]\d+)*|times\b|hours?\b|days?\b|weeks?\b|months?\b|years?\b|minutes?\b|nights?\b|grams?\b))?(?![\w-])/gi;
function cueNum(h) {
  for (const m of String(h).matchAll(CUE_RE)) {
    const [all, qual, num, unit] = m, before = h.slice(Math.max(0, m.index - 7), m.index);
    if (/^(?:1[89]|20)\d\d(?:\s*(?:to|-|–)\s*(?:(?:1[89]|20)\d\d|\d\d))?$/.test(num)) continue;
    if (/&#?$/.test(before)) continue;                                   // the digits of an escaped character (&#39;)
    if (/\b(?:in|of)\s$/.test(before)) continue;
    if (!qual && !unit && /^\d$/.test(num)) continue;
    return h.slice(0, m.index) + '<b class="cue">' + all + "</b>" + h.slice(m.index + all.length);
  }
  return h;
}
// an answer whose plain words are being rewritten for its new version: a short note and the way to the full answer
const REWRITING = id => '<p class="ask-short rewriting">We are rewriting this answer in plain words.</p><p><a class="ask-all" href="#' + id + '">Read the full answer on the research page</a></p>';
/* One question and its answer (redesign 2, 13 November: every answer had the same four parts, repeated 20 to 40 times a
   page). Closed, a card shows the question, the short answer and how sure the research is, the bars with their words; one
   tap opens the rest: the catch ("But") first, then the picture of the numbers, "How do we know?" and the way to the
   evidence, and at the end up to three answers to read next. */
function ansHtml(id, q, pre, rn) {
  const c = claimById[id]; if (!c) return "";
  const sp = (SIMPLE.claims || {})[id];
  if (!sp) return '<details class="ask" id="' + (pre || "ask-") + id + '"><summary><span class="ask-q">' + esc(q) + '</span><span class="ask-i" aria-hidden="true"></span></summary><div class="ask-a">' + REWRITING(id) + "</div></details>";
  return '<details class="ask' + (wasSeen(id) ? " seen" : "") + '" id="' + (pre || "ask-") + id + '" data-cid="' + id + '"><summary><span class="ask-h"><span class="ask-q">' + esc(q) + '</span><span class="ask-s">' + cueNum(esc(sp.short)) + '</span><span class="ask-m">' + meterHtml(c.grade.certainty, true) + "</span></span>" +
    '<span class="ask-seen" title="You have read this">' + icon("check") + '</span><span class="ask-i" aria-hidden="true"></span></summary><div class="ask-a">' + answerBody(id, c, sp, true) + (rn || "") + "</div></details>";
}
/* One answer, in the order a reader needs it (senior author, 1 November: "so many words that I get lost"): the short answer,
   its catch and the picture first; how sure the research is and the evidence in one line; "How do we know?" one tap away,
   with compact source labels; the sources themselves, the full references and "Report a mistake" live in the evidence.
   In a card (card = true) the short answer and the bars are already on the closed card, so the open card starts with the
   catch, and "How do we know?" shows at once instead of folding a third time (redesign 2: two levels, no third). */
function answerBody(id, c, sp, card) {
  const flags = [c.verification.status === "draft" ? '<span class="flag early">' + icon("alert") + "Early draft: " + esc(draftWhy(c)) + "</span>" : "",
    c.debate ? '<a class="flag debate" href="#' + esc(id) + '" data-focus-src="debate">' + icon("scale") + "Researchers disagree: read both sides</a>" : ""].filter(Boolean).join("");
  const how = sp.how && sp.how.length ? '<ul class="ask-howl">' + sp.how.map((t, i) => "<li>" + esc(t) + howSrcHtml(sp, i, false, id) + "</li>").join("") + "</ul>" : "";
  return (card ? "" : '<p class="ask-short">' + cueNum(esc(sp.short)) + "</p>") + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + (sp.freq ? freqHtml(sp.freq, card) : dotPicHtml(sp.short)) +
    (flags ? '<p class="ask-flags">' + flags + "</p>" : "") +
    (how ? (card ? '<div class="ask-how"><p class="ask-howk">How do we know?</p>' + how + "</div>" : '<details class="ask-how"><summary>How do we know?</summary>' + how + "</details>") : "") +
    '<div class="ask-foot">' + (card ? "" : meterHtml(c.grade.certainty, true)) + '<span class="ask-acts"><button type="button" class="ask-share" data-share="' + esc(id) + '" aria-label="Share this answer">' + icon("share") + '<span class="ask-share-t">Share</span></button><a class="ask-ev" href="#' + id + '">The evidence ' + icon("arrow") + "</a></span></div>" + helpLine(sp);
}
/* Numbers as pictures (redesign 2): a short answer that says "N in 100" (a whole number from 1 to 99, never a range such as
   "43 to 49 in 100") shows 100 dots with N filled, labelled in the same words ("About 9 in 100"); the dots are hidden from
   screen readers, which read the words. An answer with a picture of its own (data/site/simple.json freq) keeps that one. */
const FREQ_QUAL = /\b(about|around|nearly|almost|over|under|more than|fewer than|less than|up to|at least|roughly|only|just)\s+$/i;
function shortFreq(t) {
  t = String(t || "");
  for (const m of t.matchAll(/(\d+) in 100(?![\d,.]?\d)/g)) {
    const n = +m[1], before = t.slice(Math.max(0, m.index - 24), m.index), after = t.slice(m.index + m[0].length);
    if (n < 1 || n > 99 || /[\d.,]$/.test(before)) continue;
    if (/\b(?:to|and|or|from|between)\s+$|[–-]\s*$/i.test(before) || /^\s*(?:to|-|–)\s*\d/.test(after)) continue;
    const q = before.match(FREQ_QUAL), w = (q ? q[1] + " " : "") + n + " in 100";
    return { n, words: w.charAt(0).toUpperCase() + w.slice(1) };
  }
  return null;
}
function dotPicHtml(t) {
  const f = shortFreq(t); if (!f) return "";
  return '<div class="freq dotpic"><div class="freq-row">' + dotsHtml(f.n, 100) + "<span><b>" + esc(f.words) + "</b></span></div></div>";
}
// answers a reader has opened, remembered on this device only, so a long list shows where they have been (no tracking)
let SEEN_SET = null;
function seenSet() { if (SEEN_SET) return SEEN_SET; try { SEEN_SET = new Set(JSON.parse(localStorage.getItem("pk-read") || "[]")); } catch (e) { SEEN_SET = new Set(); } return SEEN_SET; }
function wasSeen(id) { return seenSet().has(id); }
function markSeen(id) { const r = seenSet(); if (r.has(id)) return; r.add(id); try { localStorage.setItem("pk-read", JSON.stringify([...r].slice(-800))); } catch (e) {} }
document.addEventListener("toggle", e => { const d = e.target; if (!d.matches || !d.matches("details.ask[open]") || !d.dataset.cid) return; markSeen(d.dataset.cid); d.classList.add("seen"); if (d.closest("#drug2")) pageProgress(); }, true);
/* The drug page a reader was on is remembered, with its answers (on this device only), so that the start page can offer to
   pick up where they left off and say how many of its answers they have opened. (The count on the drug page itself went with
   2.3: a section's row says how many answers it holds.) */
function pageAskIds() { return [...new Set([...document.querySelectorAll("#drug2 details.ask[data-cid]")].map(d => d.dataset.cid))]; }
function pageProgress() {
  const ids = pageAskIds(); if (!renderedDrug || ids.length < 4) return;
  try { localStorage.setItem("pk-last", JSON.stringify({ s: renderedDrug, ids })); } catch (e) { /* not kept */ }
}
function lastPage() { try { const x = JSON.parse(localStorage.getItem("pk-last") || "null"); return x && subBySlug[x.s] && Array.isArray(x.ids) && x.ids.length ? x : null; } catch (e) { return null; } }
// "Share": the phone's own share sheet where there is one, otherwise the link is copied; Pharmakon itself sends nothing anywhere
document.addEventListener("click", async e => {
  const b = e.target.closest && e.target.closest("button.ask-share"); if (!b) return;
  const id = b.dataset.share, d = b.closest("details.ask"), sh = document.querySelector("#shared-body .sh-q");
  const q = d ? (d.querySelector(".ask-q") || {}).textContent || "" : sh && sh.dataset.cid === id ? sh.textContent : anyQuestion(id) || "";
  // the address opens only this answer (#a/<page>/<claim>), so whoever gets the link sees what was meant
  const h = location.hash, c = claimById[id];
  const ctx = h.startsWith("#a/") ? h.split("/")[1] : renderedDrug && h.startsWith("#s-") ? renderedDrug : h.startsWith("#facts") ? "facts" : h.startsWith("#checking") ? "checking" :
    c && c.substance === "interactions" ? "mixing" : c && c.substance === GEN ? "facts" : c && c.substance === DC ? "checking" : c && subBySlug[c.substance] ? c.substance : "home";
  const url = location.origin + location.pathname + "#a/" + ctx + "/" + id;
  const t = b.querySelector(".ask-share-t");
  const done = msg => { if (!t) return; t.textContent = msg; b.classList.add("said"); clearTimeout(b._t); b._t = setTimeout(() => { t.textContent = "Share"; b.classList.remove("said"); }, 2200); };
  if (navigator.share) { try { await navigator.share({ title: "Pharmakon: " + q, text: q, url }); } catch (err) { /* closed by the reader */ } return; }
  try { await navigator.clipboard.writeText(url); done("Link copied"); } catch (err) { done("Copy failed"); }
});
// Read next and At a glance: an answer on the page the reader is on opens where it is (the one they were reading closes),
// revealed if it was folded away, without changing the address, so Back still leaves the page; an answer on another page
// opens there, through its own address
document.addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("a[data-open]"); if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  const nx = document.getElementById(a.dataset.open); if (!nx || !nx.closest(".view.active")) return;
  e.preventDefault();
  const cur = a.closest("details.ask"); if (cur && cur !== nx) cur.open = false;
  const more = nx.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const mb = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (mb) mb.remove(); }
  if ("open" in nx) nx.open = true;
  // a jump, kept clear of the sticky bars while the page settles (a smooth scroll this far can end under the topic chips)
  scrollToEl(nx); const sm = nx.querySelector("summary"); if (sm) sm.focus({ preventScroll: true }); else { nx.setAttribute("tabindex", "-1"); nx.focus({ preventScroll: true }); }
});
// an early draft says so where its evidence is shown, with the reason (METHODS §12, publication at launch)
function earlyLine(c) {
  return c.verification.status === "draft" ? '<p class="ask-early">Early draft: ' + esc(draftWhy(c)) + ".</p>" : "";
}
// an answer that mentions suicide ends with one quiet line to help, apart from the evidence (decision s-help-pointer)
function helpLine(sp) {
  const t = [sp.short, sp.but, ...(sp.how || [])].join(" ");
  return /suicid/i.test(t) ? '<p class="ask-help">' + icon("phone") + '<span>If you are thinking about suicide, you can get help now: <a href="#emergency">emergency numbers where you are</a>.</span></p>' : "";
}
/* One shared answer (senior author, 6 November: a shared link opened the whole page, so whoever received it could not
   tell what the sender meant to share). The Share button's address is #a/<page>/<claim>: it opens only that question and
   its answer, then the way to the rest of the page it came from, and three more of its questions. */
const SHARE_CTX = { facts: GEN, checking: DC, mixing: "interactions" };
function sharedPlace(ctx, id) {
  const c = claimById[id], key = SHARE_CTX[ctx] || ctx;
  if (key === GEN) return { key, href: "#facts", more: "More facts about drug use", q: x => "#facts/q-" + x };
  if (key === DC) return { key, href: "#checking", more: "More about drug checking", q: x => "#checking/q-" + x };
  if (key === "interactions") return { key, href: "#interactions", more: "More about mixing drugs", q: x => "#" + x };
  const slug = subBySlug[key] ? key : c && subBySlug[c.substance] ? c.substance : null;
  return slug ? { key: slug, href: "#s-" + slug, more: "More about " + subBySlug[slug].name, q: x => "#s-" + slug + "/q-" + x } : { key: null, href: "#home", more: "More from Pharmakon", q: x => "#" + x };
}
function sharedQuestion(key, id) {
  for (const g of QUESTIONS[key] || []) for (const [cid, q] of g.items) if (cid === id) return q;
  return anyQuestion(id) || "";
}
function renderShared(ctx, id) {
  const c = claimById[id], box = document.getElementById("shared-body"); if (!c || !box) return null;
  const pl = sharedPlace(ctx, id), q = sharedQuestion(pl.key, id), sp = (SIMPLE.claims || {})[id];
  const list = pl.key ? (QUESTIONS[pl.key] || []).flatMap(g => g.items).filter(([x]) => claimById[x]) : [];
  const at = list.findIndex(([x]) => x === id), others = at < 0 ? list.slice(0, 3) : list.slice(at + 1).concat(list.slice(0, at)).slice(0, 3);
  box.innerHTML = '<p class="sh-from">Shared from Pharmakon</p><h1 class="sh-q" data-cid="' + esc(id) + '">' + esc(q) + "</h1>" +
    '<div class="open-a sh-a">' + (sp ? answerBody(id, c, sp) : REWRITING(id)) + "</div>" +
    '<p class="sh-go"><a class="sh-more" href="' + pl.href + '">' + esc(pl.more) + " " + icon("arrow") + "</a></p>" +
    (others.length ? '<h2 class="sh-oh">Other questions</h2><ul class="sh-others">' + others.map(([x, oq]) => '<li><a href="' + pl.q(x) + '">' + esc(oq) + "</a></li>").join("") + "</ul>" : "");
  markSeen(id);
  return q || "Shared answer";
}
// a single answer, shown open: the short answer, its catch, and "How do we know?"
function openAnswer(id, rn) {
  const c = claimById[id], sp = (SIMPLE.claims || {})[id]; if (!c) return "";
  if (!sp) return '<div class="open-a" id="ask-' + id + '">' + REWRITING(id) + "</div>";
  return '<div class="open-a" id="ask-' + id + '">' + answerBody(id, c, sp) + (rn || "") + "</div>";
}
// a short list with the rest one tap away (about four things at a time); page is the page the list is on (a drug's slug,
// GEN, DC or "interactions"), for the addresses of the answers to read next
function askList(items, key, first, pre, page) {
  const n = first || 4, shown = items.slice(0, n), rest = items.slice(n);
  const rn = i => readNextHtml(items[i][0], nextInTopic(items, i), page, pre);
  return '<div class="asks">' + shown.map(([id, q], i) => ansHtml(id, q, pre, rn(i))).join("") +
    (rest.length ? '<div class="asks-more" id="more-' + key + '" hidden>' + rest.map(([id, q], i) => ansHtml(id, q, pre, rn(n + i))).join("") + '</div><button type="button" class="morebtn" data-more="more-' + key + '">' + rest.length + " more question" + (rest.length === 1 ? "" : "s") + "</button>" : "") + "</div>";
}
/* Read next (redesign 2; Wikipedia: each page invites the next click): at the end of an open answer, up to three other
   answers, titles only: the next ones in its topic (in the list's order; from the topic's start, only the ones not opened
   yet), then one from a "Myths and facts" topic on any page, its own page first and one not opened yet first. */
function nextInTopic(items, i) {
  const t = items[i][2] || "", same = items.map((it, j) => [it, j]).filter(([it, j]) => j !== i && (it[2] || "") === t && (SIMPLE.claims || {})[it[0]]);
  return same.filter(([, j]) => j > i).concat(same.filter(([it, j]) => j < i && !wasSeen(it[0]))).slice(0, 2).map(([it]) => it);
}
// the page an answer is asked on (the one preferred, else its own drug's, else any page that asks it), and its address there
const PAGE_OF = new Map();
function answerPageKey(id, prefer) {
  const k0 = id + "|" + (prefer || ""); if (PAGE_OF.has(k0)) return PAGE_OF.get(k0);
  const c = claimById[id], has = k => k && Array.isArray(QUESTIONS[k]) && QUESTIONS[k].some(g => g.items.some(([x]) => x === id));
  const k = [prefer, c && c.substance].concat(Object.keys(QUESTIONS)).find(has) || (c && c.substance) || null;
  PAGE_OF.set(k0, k); return k;
}
const answerAddr = (id, prefer) => sharedPlace(answerPageKey(id, prefer) || "", id).q(id);
const askPre = page => page === GEN ? "fx-" : page === "interactions" ? "mx-" : "ask-";   // how each page names its answers
let MYTHS = null;
function mythList() {
  if (!MYTHS) MYTHS = Object.entries(QUESTIONS).flatMap(([k, gs]) => (Array.isArray(gs) ? gs : []).filter(g => /^myths? and facts$/i.test(g.topic))
    .flatMap(g => g.items.filter(([id]) => claimById[id] && (SIMPLE.claims || {})[id]).map(([id, q]) => ({ k, id, q }))));
  return MYTHS;
}
function readNextHtml(id, nexts, page, pre) {
  const out = nexts.map(([x, q]) => ({ q, href: answerAddr(x, page), dom: (pre || "ask-") + x, id: x }));
  const myths = mythList().filter(m => m.id !== id && !out.some(o => o.id === m.id));
  if (myths.length) {
    const rank = m => (m.k === page ? 0 : 2) + (wasSeen(m.id) ? 1 : 0), best = Math.min(...myths.map(rank)), cands = myths.filter(m => rank(m) === best);
    const m = cands[[...id].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) >>> 0, 7) % cands.length];   // the same answer always suggests the same one
    out.push({ q: m.q, href: sharedPlace(m.k, m.id).q(m.id), dom: (m.k === page ? pre || "ask-" : askPre(m.k)) + m.id, id: m.id });
  }
  if (!out.length) return "";
  return '<div class="rn"><p class="rn-k">Read next</p><ul class="rn-l">' + out.map(o => '<li><a href="' + esc(o.href) + '" data-open="' + esc(o.dom) + '"><span>' + esc(o.q) + "</span>" + icon("arrow") + "</a></li>").join("") + "</ul></div>";
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("button.morebtn"); if (!b) return;
  const box = document.getElementById(b.dataset.more); if (!box) return;
  box.hidden = false; b.remove(); const d = box.querySelector("details.ask summary"); if (d) d.focus();
});

/* Photo credits for a set of forms in one short paragraph: which form, then its photo's author, licence and source */
function looksCredits(fl, byId) {
  const groups = new Map();
  fl.forEach(f => { const p = (f.photos || []).map(id => byId[id]).find(Boolean); if (!p) return;
    const k = photoCredit(p).replace(/^<span class="phcredit">Photo: /, "").replace(/<\/span>$/, ""); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(f.name); });
  // the credits every licence asks for, one tap away instead of a long paragraph under the photos
  return groups.size ? '<details class="look-credits"><summary>Photo credits</summary><p>' + [...groups].map(([k, names]) => esc(andList(names)) + ", " + k).join("; ") + ".</p></details>" : "";
}
/* What it looks like: every form, photo first */
function formsHtml(slug) {
  const fl = (FORMS[slug] || []).filter(f => f.name); if (!fl.length) return "";
  const byId = Object.fromEntries(PHOTOS.map(p => [p.id, p]));
  const ident = IDENTITY.find(d => d.substance === slug) || { sources: [] };
  return '<ul class="looks">' + fl.map(f => { const p = (f.photos || []).map(id => byId[id]).find(Boolean);
    return '<li class="look' + (p ? " hasph" : "") + '">' + (p ? '<span class="look-ph">' + photoImg(p, "t", p.alt, true) + "</span>" : '<span class="look-ic">' + icon(f.icon || "molecule") + "</span>") +
      '<span class="look-t"><b>' + esc(f.name) + "</b><span>" + esc(f.what || "") + "</span></span></li>"; }).join("") + "</ul>" +
    looksCredits(fl, byId) + '<p class="look-note">Looks don’t tell you what’s inside: the same drug can look different, and different drugs can look the same. ' + phToggle() + "</p>";
}

/* Your country: the law, the emergency number and drug checking where you are. Asked once, in the place it is needed,
   then remembered on this device only. The first guess comes from the device's time zone, worked out on the device and
   never sent anywhere; the reader confirms it ("Are you in Greece?") or picks another country. */
const ISO2UN = { AD: "Andorra", AE: "United Arab Emirates", AF: "Afghanistan", AG: "Antigua and Barbuda", AL: "Albania", AM: "Armenia", AO: "Angola", AR: "Argentina", AT: "Austria", AU: "Australia", AZ: "Azerbaijan",
  BA: "Bosnia and Herzegovina", BB: "Barbados", BD: "Bangladesh", BE: "Belgium", BF: "Burkina Faso", BG: "Bulgaria", BH: "Bahrain", BI: "Burundi", BJ: "Benin", BN: "Brunei Darussalam", BO: "Bolivia (Plurinational State of)",
  BR: "Brazil", BS: "Bahamas (The)", BT: "Bhutan", BW: "Botswana", BY: "Belarus", BZ: "Belize", CA: "Canada", CD: "Democratic Republic of the Congo", CF: "Central African Republic", CG: "Congo", CH: "Switzerland",
  CI: "Côte d'Ivoire", CK: "Cook Islands", CL: "Chile", CM: "Cameroon", CN: "China", CO: "Colombia", CR: "Costa Rica", CU: "Cuba", CV: "Cabo Verde", CY: "Cyprus", CZ: "Czech Republic", DE: "Germany", DJ: "Djibouti",
  DK: "Denmark", DM: "Dominica", DO: "Dominican Republic", DZ: "Algeria", EC: "Ecuador", EE: "Estonia", EG: "Egypt", ER: "Eritrea", ES: "Spain", ET: "Ethiopia", FI: "Finland", FJ: "Fiji", FM: "Micronesia (Federated States of)",
  FR: "France", GA: "Gabon", GB: "United Kingdom of Great Britain and Northern Ireland", GD: "Grenada", GE: "Georgia", GH: "Ghana", GM: "Gambia", GN: "Guinea", GQ: "Equatorial Guinea", GR: "Greece", GT: "Guatemala",
  GW: "Guinea-Bissau", GY: "Guyana", HN: "Honduras", HR: "Croatia", HT: "Haiti", HU: "Hungary", ID: "Indonesia", IE: "Ireland", IL: "Israel", IN: "India", IQ: "Iraq", IR: "Iran (Islamic Republic of)", IS: "Iceland",
  IT: "Italy", JM: "Jamaica", JO: "Jordan", JP: "Japan", KE: "Kenya", KG: "Kyrgyzstan", KH: "Cambodia", KI: "Kiribati", KM: "Comoros", KN: "St. Kitts and Nevis", KP: "Democratic People's Republic of Korea",
  KR: "Republic of Korea", KW: "Kuwait", KZ: "Kazakhstan", LA: "Lao People's Democratic Republic", LB: "Lebanon", LC: "St. Lucia", LI: "Liechtenstein", LK: "Sri Lanka", LR: "Liberia", LS: "Lesotho", LT: "Lithuania",
  LU: "Luxembourg", LV: "Latvia", LY: "Libya", MA: "Morocco", MC: "Monaco", MD: "Republic of Moldova", ME: "Montenegro", MG: "Madagascar", MH: "Marshall Islands", MK: "North Macedonia", ML: "Mali", MM: "Myanmar",
  MN: "Mongolia", MR: "Mauritania", MT: "Malta", MU: "Mauritius", MV: "Maldives", MW: "Malawi", MX: "Mexico", MY: "Malaysia", MZ: "Mozambique", NA: "Namibia", NE: "Niger", NG: "Nigeria", NI: "Nicaragua",
  NL: "Netherlands (Kingdom of the)", NO: "Norway", NP: "Nepal", NR: "Naoero", NU: "Niue", NZ: "New Zealand", OM: "Oman", PA: "Panama", PE: "Peru", PG: "Papua New Guinea", PH: "Philippines", PK: "Pakistan",
  PL: "Poland", PS: "State of Palestine", PT: "Portugal", PW: "Palau", PY: "Paraguay", QA: "Qatar", RO: "Romania", RS: "Serbia", RU: "Russian Federation", RW: "Rwanda", SA: "Saudi Arabia", SB: "Solomon Islands",
  SC: "Seychelles", SD: "Sudan", SE: "Sweden", SG: "Singapore", SI: "Slovenia", SK: "Slovakia", SL: "Sierra Leone", SM: "San Marino", SN: "Senegal", SO: "Somalia", SR: "Suriname", SS: "South Sudan",
  ST: "Sao Tome and Principe", SV: "El Salvador", SY: "Syrian Arab Republic", SZ: "Eswatini", TD: "Chad", TG: "Togo", TH: "Thailand", TJ: "Tajikistan", TL: "Timor-Leste", TM: "Turkmenistan", TN: "Tunisia", TO: "Tonga",
  TR: "Türkiye", TT: "Trinidad and Tobago", TV: "Tuvalu", TZ: "United Republic of Tanzania", UA: "Ukraine", UG: "Uganda", US: "United States of America", UY: "Uruguay", UZ: "Uzbekistan", VA: "Holy See",
  VC: "St. Vincent and the Grenadines", VE: "Venezuela (Bolivarian Republic of)", VN: "Viet Nam", VU: "Vanuatu", WS: "Samoa", YE: "Yemen", ZA: "South Africa", ZM: "Zambia", ZW: "Zimbabwe" };
// the time zones of each country's main cities (IANA names); a zone shared by several countries is left out
const TZ2 = { "Europe/Athens": "GR", "Europe/London": "GB", "Europe/Belfast": "GB", "Europe/Dublin": "IE", "Europe/Lisbon": "PT", "Atlantic/Madeira": "PT", "Atlantic/Azores": "PT", "Europe/Madrid": "ES", "Atlantic/Canary": "ES",
  "Africa/Ceuta": "ES", "Europe/Paris": "FR", "Europe/Brussels": "BE", "Europe/Amsterdam": "NL", "Europe/Luxembourg": "LU", "Europe/Berlin": "DE", "Europe/Zurich": "CH", "Europe/Vienna": "AT", "Europe/Rome": "IT",
  "Europe/Prague": "CZ", "Europe/Bratislava": "SK", "Europe/Warsaw": "PL", "Europe/Budapest": "HU", "Europe/Ljubljana": "SI", "Europe/Zagreb": "HR", "Europe/Belgrade": "RS", "Europe/Sarajevo": "BA", "Europe/Podgorica": "ME",
  "Europe/Skopje": "MK", "Europe/Tirane": "AL", "Europe/Sofia": "BG", "Europe/Bucharest": "RO", "Europe/Chisinau": "MD", "Europe/Kiev": "UA", "Europe/Kyiv": "UA", "Europe/Minsk": "BY", "Europe/Vilnius": "LT",
  "Europe/Riga": "LV", "Europe/Tallinn": "EE", "Europe/Helsinki": "FI", "Europe/Stockholm": "SE", "Europe/Oslo": "NO", "Europe/Copenhagen": "DK", "Atlantic/Reykjavik": "IS", "Europe/Moscow": "RU", "Europe/Samara": "RU",
  "Asia/Yekaterinburg": "RU", "Asia/Novosibirsk": "RU", "Asia/Vladivostok": "RU", "Europe/Istanbul": "TR", "Asia/Istanbul": "TR", "Asia/Nicosia": "CY", "Europe/Nicosia": "CY", "Asia/Famagusta": "CY", "Europe/Malta": "MT",
  "Europe/Monaco": "MC", "Europe/Andorra": "AD", "Europe/San_Marino": "SM", "Europe/Vatican": "VA", "Europe/Vaduz": "LI",
  "America/New_York": "US", "America/Chicago": "US", "America/Denver": "US", "America/Los_Angeles": "US", "America/Phoenix": "US", "America/Anchorage": "US", "America/Detroit": "US", "America/Boise": "US",
  "America/Indiana/Indianapolis": "US", "America/Kentucky/Louisville": "US", "Pacific/Honolulu": "US", "America/Toronto": "CA", "America/Vancouver": "CA", "America/Edmonton": "CA", "America/Winnipeg": "CA",
  "America/Halifax": "CA", "America/St_Johns": "CA", "America/Regina": "CA", "America/Montreal": "CA", "America/Mexico_City": "MX", "America/Cancun": "MX", "America/Monterrey": "MX", "America/Tijuana": "MX",
  "America/Merida": "MX", "America/Chihuahua": "MX", "America/Sao_Paulo": "BR", "America/Manaus": "BR", "America/Recife": "BR", "America/Fortaleza": "BR", "America/Bahia": "BR", "America/Belem": "BR",
  "America/Argentina/Buenos_Aires": "AR", "America/Buenos_Aires": "AR", "America/Argentina/Cordoba": "AR", "America/Argentina/Mendoza": "AR", "America/Santiago": "CL", "America/Bogota": "CO", "America/Lima": "PE",
  "America/Caracas": "VE", "America/Montevideo": "UY", "America/Asuncion": "PY", "America/La_Paz": "BO", "America/Guayaquil": "EC", "America/Panama": "PA", "America/Costa_Rica": "CR", "America/Guatemala": "GT",
  "America/El_Salvador": "SV", "America/Tegucigalpa": "HN", "America/Managua": "NI", "America/Havana": "CU", "America/Santo_Domingo": "DO", "America/Jamaica": "JM", "America/Port-au-Prince": "HT",
  "America/Port_of_Spain": "TT", "America/Barbados": "BB", "America/Nassau": "BS", "America/Belize": "BZ", "America/Guyana": "GY", "America/Paramaribo": "SR",
  "Asia/Tokyo": "JP", "Asia/Seoul": "KR", "Asia/Pyongyang": "KP", "Asia/Shanghai": "CN", "Asia/Urumqi": "CN", "Asia/Singapore": "SG", "Asia/Kuala_Lumpur": "MY", "Asia/Kuching": "MY", "Asia/Bangkok": "TH",
  "Asia/Jakarta": "ID", "Asia/Makassar": "ID", "Asia/Jayapura": "ID", "Asia/Manila": "PH", "Asia/Ho_Chi_Minh": "VN", "Asia/Saigon": "VN", "Asia/Kolkata": "IN", "Asia/Calcutta": "IN", "Asia/Karachi": "PK",
  "Asia/Dhaka": "BD", "Asia/Kathmandu": "NP", "Asia/Colombo": "LK", "Asia/Dubai": "AE", "Asia/Riyadh": "SA", "Asia/Qatar": "QA", "Asia/Kuwait": "KW", "Asia/Bahrain": "BH", "Asia/Muscat": "OM", "Asia/Tehran": "IR",
  "Asia/Baghdad": "IQ", "Asia/Amman": "JO", "Asia/Beirut": "LB", "Asia/Damascus": "SY", "Asia/Jerusalem": "IL", "Asia/Tel_Aviv": "IL", "Asia/Gaza": "PS", "Asia/Hebron": "PS", "Asia/Kabul": "AF",
  "Asia/Tashkent": "UZ", "Asia/Samarkand": "UZ", "Asia/Almaty": "KZ", "Asia/Bishkek": "KG", "Asia/Dushanbe": "TJ", "Asia/Ashgabat": "TM", "Asia/Baku": "AZ", "Asia/Tbilisi": "GE", "Asia/Yerevan": "AM",
  "Asia/Ulaanbaatar": "MN", "Asia/Yangon": "MM", "Asia/Rangoon": "MM", "Asia/Phnom_Penh": "KH", "Asia/Vientiane": "LA", "Asia/Brunei": "BN", "Asia/Thimphu": "BT", "Asia/Dili": "TL", "Indian/Maldives": "MV",
  "Australia/Sydney": "AU", "Australia/Melbourne": "AU", "Australia/Brisbane": "AU", "Australia/Perth": "AU", "Australia/Adelaide": "AU", "Australia/Hobart": "AU", "Australia/Darwin": "AU", "Australia/Canberra": "AU",
  "Pacific/Auckland": "NZ", "Pacific/Fiji": "FJ", "Pacific/Port_Moresby": "PG", "Pacific/Apia": "WS", "Pacific/Tongatapu": "TO", "Pacific/Efate": "VU", "Pacific/Guadalcanal": "SB",
  "Africa/Cairo": "EG", "Africa/Johannesburg": "ZA", "Africa/Lagos": "NG", "Africa/Nairobi": "KE", "Africa/Casablanca": "MA", "Africa/Algiers": "DZ", "Africa/Tunis": "TN", "Africa/Tripoli": "LY", "Africa/Accra": "GH",
  "Africa/Abidjan": "CI", "Africa/Dakar": "SN", "Africa/Addis_Ababa": "ET", "Africa/Kampala": "UG", "Africa/Dar_es_Salaam": "TZ", "Africa/Kinshasa": "CD", "Africa/Lubumbashi": "CD", "Africa/Luanda": "AO",
  "Africa/Maputo": "MZ", "Africa/Harare": "ZW", "Africa/Lusaka": "ZM", "Africa/Windhoek": "NA", "Africa/Gaborone": "BW", "Africa/Khartoum": "SD", "Africa/Juba": "SS", "Africa/Kigali": "RW", "Africa/Douala": "CM",
  "Africa/Mogadishu": "SO", "Africa/Asmara": "ER", "Africa/Djibouti": "DJ", "Africa/Bamako": "ML", "Africa/Ouagadougou": "BF", "Africa/Niamey": "NE", "Africa/Ndjamena": "TD", "Africa/Conakry": "GN",
  "Africa/Freetown": "SL", "Africa/Monrovia": "LR", "Africa/Lome": "TG", "Africa/Porto-Novo": "BJ", "Africa/Libreville": "GA", "Africa/Brazzaville": "CG", "Africa/Bangui": "CF", "Africa/Malabo": "GQ",
  "Africa/Maseru": "LS", "Africa/Mbabane": "SZ", "Africa/Blantyre": "MW", "Africa/Bujumbura": "BI", "Africa/Nouakchott": "MR", "Africa/Banjul": "GM", "Africa/Bissau": "GW", "Atlantic/Cape_Verde": "CV",
  "Indian/Antananarivo": "MG", "Indian/Mauritius": "MU", "Indian/Mahe": "SC", "Indian/Comoro": "KM" };
function guessCountry() {
  let iso = null;
  try { iso = TZ2[Intl.DateTimeFormat().resolvedOptions().timeZone] || null; } catch (e) { iso = null; }
  // no time zone match: the region in the device's languages (en-US is left out, as it is the default on many devices everywhere)
  if (!iso) for (const l of (navigator.languages || [navigator.language || ""])) { const m = String(l).match(/^[a-z]{2,3}-([A-Z]{2})$/); if (m && m[1] !== "US" && ISO2UN[m[1]]) { iso = m[1]; break; } }
  const un = iso && ISO2UN[iso];
  return un && WL_COUNTRIES.some(c => c.name === un) ? un : null;
}
// the everyday name: "Russia", not "Russia (Russian Federation)"
const shortCtry = un => ctryName(un).replace(/\s*\(.*\)$/, "");
// in a sentence, some names take "the": "in the United Kingdom", "to the Netherlands"
const THE_C = new Set(["United Kingdom", "United States", "Netherlands", "Philippines", "United Arab Emirates", "Dominican Republic", "Central African Republic", "Democratic Republic of the Congo", "Bahamas", "Gambia", "Comoros", "Maldives", "Marshall Islands", "Solomon Islands", "Holy See"]);
const inCtry = un => (THE_C.has(shortCtry(un)) ? "the " : "") + shortCtry(un);
const CTRY_ALT = { "Viet Nam": ["Vietnam"], "Türkiye": ["Turkey"], "Czech Republic": ["Czechia"], "Côte d'Ivoire": ["Ivory Coast"], "Cabo Verde": ["Cape Verde"], "Eswatini": ["Swaziland"], "Myanmar": ["Burma"],
  "Timor-Leste": ["East Timor"], "Holy See": ["Vatican"], "Naoero": ["Nauru"] };
function sameCountry(name, un) { const n = norm(name); return [un, ctryName(un), shortCtry(un)].concat(CTRY_ALT[un] || []).some(x => norm(x) === n); }
function emFor(un) { return EMERGENCY.countries.find(c => [c.country].concat(c.aka || []).some(n => sameCountry(n, un))) || null; }
function dcFor(un) { return DRUGCHECK.services.filter(s => sameCountry(s.country, un)); }
const dcSearchedNone = un => (DRUGCHECK.countries_searched_none_found || []).some(n => sameCountry(n, un));
// a report says checking or kit handouts exist, but no service page was found: shown as a sourced line
const dcReported = un => (DRUGCHECK.countries_reported || []).find(r => sameCountry(r.country, un)) || null;
const telOf = x => x.tel || x.n.replace(/\s+/g, "");

let cqSeq = 0;
function ctrySelectHtml(id) {
  return '<select class="ctry2" id="' + id + '"><option value="">Choose your country</option>' + WL_COUNTRIES.map(c => '<option value="' + esc(c.name) + '"' + (c.name === PREF_COUNTRY ? " selected" : "") + ">" + esc(ctryName(c.name)) + "</option>").join("") + "</select>";
}
/* The country question where an answer depends on it, or the country already chosen with a way to change it.
   heading: the chosen country is the heading of the part (the emergency and drug checking pages) */
function countryAsk(heading) {
  const id = "cq-" + (++cqSeq), sel = '<span class="cq-sel" hidden><label class="sr" for="' + id + '">Your country</label>' + ctrySelectHtml(id) + "</span>";
  if (PREF_COUNTRY) {
    const where = icon("pin") + "<span>" + esc(shortCtry(PREF_COUNTRY)) + "</span>";
    return '<div class="cq set">' + (heading ? '<h2 class="cq-where">' + where + "</h2>" : '<p class="cq-where">' + where + "</p>") + '<button type="button" class="cq-change">Change country</button>' + sel + "</div>";
  }
  const g = guessCountry(), why = '<p class="cq-why">So we can show what applies where you are. Your answer stays on this device.</p>';
  if (g) return '<div class="cq ask"><p class="cq-q">' + icon("pin") + "<span>Are you in <b>" + esc(shortCtry(g)) + '</b>?</span></p><p class="cq-btns"><button type="button" class="cq-yes" data-c="' + esc(g) + '">Yes</button><button type="button" class="cq-change">Another country</button></p>' + sel + why + "</div>";
  return '<div class="cq ask"><p class="cq-q">' + icon("pin") + '<label for="' + id + '">Where are you?</label></p>' + ctrySelectHtml(id) + why + "</div>";
}
document.addEventListener("click", e => {
  const y = e.target.closest && e.target.closest(".cq button.cq-yes"); if (y) { setCountry(y.dataset.c, y); return; }
  const c = e.target.closest && e.target.closest(".cq button.cq-change"); if (!c) return;
  const sel = c.closest(".cq").querySelector(".cq-sel"); if (!sel) return;
  sel.hidden = false; c.hidden = true; const s = sel.querySelector("select"); if (s) s.focus();
});
document.addEventListener("change", e => { const s = e.target.closest && e.target.closest("select.ctry2"); if (s && s.value) setCountry(s.value, s); });
function setCountry(un, from) {
  PREF_COUNTRY = un || "";
  try { if (un) localStorage.setItem("pk-country", un); else localStorage.removeItem("pk-country"); } catch (err) { /* lasts for this visit */ }
  const host = from && from.closest("[id]"), hostId = host && (host.closest(".sf, .sec, #em-mine, #dc-mine") || host).id;
  refreshCountryParts();
  // keep the reader where they were: on the answer that just appeared
  const where = hostId && document.querySelector("#" + CSS.escape(hostId) + " .cq-where, #" + CSS.escape(hostId) + " .say");
  if (where) { where.setAttribute("tabindex", "-1"); where.focus({ preventScroll: true }); }
}
// every place that depends on the country, updated at once
function refreshCountryParts() {
  const page = document.getElementById("drug2");
  if (page && renderedDrug) {
    const law = page.querySelector("#d-law .sec-b"); if (law) { law.innerHTML = lawHtml(renderedDrug); lawWait(); }
    const h = page.querySelector("#d-help .sec-b"); if (h) h.innerHTML = helpHtml();
    const t = page.querySelector("#d-kits .sec-b"); if (t) t.innerHTML = testHtml();
  }
  renderEmMine(); renderDcMine();
}

/* What the law says where you are, in one plain line; the treaty and the law text with their sources are one tap away */
const NOT_READ = /^([^:]{1,60}: )?Not (found|confirmed)/;
const pageWord = slug => { const n = ((subBySlug[slug] || {}).name || slug).replace(/\s*\(.*\)$/, ""); return slug === "salvia-divinorum" || !/^[A-Z][a-z]/.test(n) ? n : n.charAt(0).toLowerCase() + n.slice(1); };
const andList = xs => xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + (xs.some(x => / and /.test(x)) ? ", and " : " and ") + xs[xs.length - 1];
// "morphine", "cannabis and cannabis resin", but "MDMA", "Delta-9-THC" and "Salvia divinorum" as written
const lcName = n => /^[A-Z][a-z-]+$/.test(n) || /^[A-Z][a-z-]+ (and|or|leaf|resin|oil|seeds?)\b/.test(n) ? n.charAt(0).toLowerCase() + n.slice(1) : n;
function lawPlain(slug, un) {
  const nm = shortCtry(un), what = pageWord(slug), rows = natRows(slug, un), listed = rows.filter(e => !NOT_READ.test(e.status));
  if (listed.length) {
    // the name each row is about ("MDMA: Table Α΄, item 20"), or the page's own name when the row does not start with one
    const names = [...new Set(listed.map(e => { const m = String(e.status).match(/^([^:]{1,60}): /); return m && !/^(Listed|Named|Covered|Not named|Table)\b/.test(m[1]) ? lcName(m[1]) : what; }))];
    return "In " + inCtry(un) + ", the law controls " + (names.length <= 3 ? andList(names) : names.slice(0, 2).join(", ") + " and " + (names.length - 2) + " more") + ".";
  }
  const after = rows.length ? " We could not yet confirm what its own law says." : " We have not read its own law yet.";
  const convs = unConvsFor(slug) || [], c = WORLD_LAW.countries.find(x => x.name === un);
  if (!convs.length) return "The UN drug treaties do not list " + what + ", so each country’s own law decides." + (rows.length ? " We could not yet confirm what " + inCtry(un) + "’s law says." : " We have not read " + inCtry(un) + "’s law on it yet.");
  const joined = c ? convs.filter(k => c[k] && c[k].status === "party").length : 0, many = convs.length > 1;
  const Nm = inCtry(un).charAt(0).toUpperCase() + inCtry(un).slice(1);
  if (joined === convs.length) return Nm + " has joined the UN " + (many ? "treaties that list " : "treaty that lists ") + what + ", so it agreed to control it." + after;
  if (joined) return Nm + " has joined one of the UN treaties that list " + what + "." + after;
  return Nm + " has not joined the UN " + (many ? "treaties that list " : "treaty that lists ") + what + "." + after;
}
function lawHtml(slug) {
  if (!LEGAL.some(d => d.substance === slug)) return '<p class="say">We have not read the law on this drug yet.</p>';
  if (!PREF_COUNTRY) return countryAsk();
  // the law rows come with the drug's file (speed): a quiet line until they arrive, then this part is drawn again (lawWait)
  if (!legalReady(slug)) return countryAsk() + '<div class="lawwait" data-law="' + esc(slug) + '"></div>';
  return countryAsk() + '<p class="say">' + esc(lawPlain(slug, PREF_COUNTRY)) + '</p><details class="lawmore"><summary>What the law says, with its sources</summary><div class="lawmore-b">' +
    countryOut(slug, PREF_COUNTRY) + '<p class="small"><a href="#law">Treaties, country by country</a></p></div></details>';
}
function lawWait() {
  document.querySelectorAll(".lawwait[data-law]").forEach(box => { const slug = box.dataset.law; box.removeAttribute("data-law");
    whenReady(() => loadFull(slug), box, "The law", () => { const sec = box.closest(".sec-b"); if (sec && renderedDrug === slug) sec.innerHTML = lawHtml(slug); }); });
}
/* Sourced lines for the drug page (data/site/stay-safer.json, descriptions.json): official and non-profit pages and
   papers, each line checked at its source by a second AI reader before it is shown: what to do if it gets too much, by
   drug family; what home tests can show; and each drug's short description. */
const SAFE = (typeof STAY_SAFER !== "undefined" && STAY_SAFER) || { tests: {}, signs: {} };
const NO_SIGNS = ["nicotine", "caffeine"];
/* The source of a line, as small chips after it (senior author, 15 November: "the sources should be apparent for each
   respective fact without creating visual clutter"): one chip per publisher, by its short name: the acronym where the
   publisher has one (HSE, ADF, CDC, WHO, FRANK), otherwise the first words of its name. A tap or hover shows the publisher,
   the pages read and their links (showSrcl, with the other popovers). A paper is named by its first author and year and
   opens its full reference, as the sources of "How do we know?" do. At most three chips; a line with more sources shows two
   and "+n". The list of sources that closed each part ("Sources (26)") is gone: every line carries its own. */
const PUB_ACR = /^[A-Z][A-Z0-9&]{1,8}$/;
let PUB_AKA = null;   // a publisher's name → its acronym, learned from the names that carry one ("Alcohol and Drug Foundation (ADF)")
function pubParts(p) {
  let s = String(p || "").trim();
  // a page by named authors: "Abrams, M. (Network for Public Health Law)" is cited here by the body in the brackets
  const by = s.match(/^[A-Z][\p{L}'’-]+, [A-Z]\..*?\(([^)]+)\)\s*$/u); if (by) s = by[1].split(/[,;]/)[0].trim();
  const m = s.match(/^(.*?)\s*\(([^)]*)\)/), lead = (m ? m[1] : s).trim(), inner = m ? m[2].split(/[,;]/)[0].trim() : "";
  return { lead, inner };
}
function pubShort(p) {
  if (!PUB_AKA) { PUB_AKA = {};
    const learn = x => { const { lead, inner } = pubParts(x); if (PUB_ACR.test(inner) && !PUB_ACR.test(lead)) PUB_AKA[lead.toLowerCase()] = inner; else if (PUB_ACR.test(lead) && inner) PUB_AKA[inner.toLowerCase()] = lead; };
    const walk = o => { if (Array.isArray(o)) o.forEach(walk); else if (o && typeof o === "object") { if (typeof o.publisher === "string") learn(o.publisher); Object.values(o).forEach(walk); } };
    [SAFE, typeof TESTS_WORLD !== "undefined" ? TESTS_WORLD : null, typeof DESCRIPTIONS !== "undefined" ? DESCRIPTIONS : null, FAMPLAIN.source].forEach(walk); }
  const { lead, inner } = pubParts(p);
  if (PUB_ACR.test(lead)) return lead;
  if (PUB_ACR.test(inner)) return inner;
  if (PUB_AKA[lead.toLowerCase()]) return PUB_AKA[lead.toLowerCase()];
  const first = lead.split(/\s[–—\/]\s|,\s/)[0].trim() || lead;
  if (first.length <= 28) return first;
  const words = first.split(" "), out = []; for (const w of words) { if (out.concat(w).join(" ").length > 26) break; out.push(w); }
  return out.join(" ") + "…";
}
const SRCL = [], SRCL_AT = new Map();
function lineSrc(anchors) {
  const groups = [];   // in the order the sources are first named: a paper by its reference, web pages by their publisher
  (anchors || []).forEach(a => {
    if (a.ref) { if (refById[a.ref] && !groups.some(g => g.ref === a.ref)) groups.push({ ref: a.ref }); return; }
    if (!a.url) return;
    const pub = a.publisher || "Source", short = pubShort(pub); let g = groups.find(x => !x.ref && x.short === short);
    if (!g) { g = { short, pub, pages: [] }; groups.push(g); }
    if (!g.pages.some(x => x.url === a.url)) g.pages.push({ title: a.title || a.url, url: a.url });
  });
  if (!groups.length) return "";
  const reg = gs => { const k = gs.map(g => g.ref ? "ref:" + g.ref : g.pub + "|" + g.pages.map(x => x.url).join("|")).join("||"); if (!SRCL_AT.has(k)) { SRCL_AT.set(k, SRCL.length); SRCL.push(gs); } return SRCL_AT.get(k); };
  const chip = g => g.ref
    ? '<a class="pop srcl" href="' + esc(refLink(refById[g.ref])) + '" target="_blank" rel="noopener" data-ref="' + esc(g.ref) + '" aria-label="Source: ' + esc(inTextLabel(refById[g.ref], REFS)) + '">' + esc(shortLabel(refById[g.ref])) + "</a>"
    : '<button type="button" class="srcl" data-srcl="' + reg([g]) + '" aria-label="Source: ' + esc(g.pub) + '">' + esc(g.short) + "</button>";
  const shown = groups.length > 3 ? groups.slice(0, 2) : groups, rest = groups.slice(shown.length);
  return ' <span class="srcs2">' + shown.map(chip).join("") + (rest.length ? '<button type="button" class="srcl" data-srcl="' + reg(rest) + '" aria-label="' + rest.length + ' more sources">+' + rest.length + "</button>" : "") + "</span>";
}
// a list of sourced lines, each with its chips
const srcList = ls => '<ul class="sf-list">' + ls.map(l => "<li>" + esc(l.line) + lineSrc(l.anchors) + "</li>").join("") + "</ul>";
/* Each drug's description, under its name (senior author, 15 November: "each drug page should have a description for each
   drug that makes you understand what it is and its sources are validated"): two to four short lines from
   data/site/descriptions.json, shown as one short paragraph, each line with its sources. Until a drug has one, the line of
   its family stands in (data/site/families-plain.json, from the Alcohol and Drug Foundation's Drug Wheel); the pages
   that skip the family line (nicotine, caffeine) show none. */
function descHtml(slug) {
  const lines = ((typeof DESCRIPTIONS !== "undefined" && DESCRIPTIONS) || {})[slug];
  if (lines && lines.length) return '<p class="dh-desc">' + lines.map(l => "<span>" + esc(l.line) + lineSrc(l.anchors) + "</span>").join(" ") + "</p>";
  const s = subBySlug[slug], fp = s && famPlain(s.cls), own = (FAMPLAIN.drugs || {})[slug];
  if (!fp || (FAMPLAIN.skip || []).includes(slug)) return "";
  return '<p class="dh-desc"><span>' + esc(own ? own.line : fp.line) + lineSrc(FAMPLAIN.source ? [FAMPLAIN.source] : []) + "</span></p>";
}
/* If it gets too much (senior author, 15 November: "we should not just write about what to do if it is too much for another
   person but what to do yourself if it's too much for you. going or calling the hospital should be the last on the list
   like a last resort ... we have to begin with what users find most useful"; "we don't want to freak people out"). Top to
   bottom: for you (the family's own lines for the reader, once they are written and checked; nothing until then); for a
   friend, what helps (the calm and help lines, then first aid, in the order of the data: for opioids, naloxone first), what
   not to do, and last, when to call an ambulance, with the reader's emergency number where their country is known and a
   quiet link to the numbers by country. No box, nothing at the top of the page, nothing repeated. Every line carries its
   sources. Each line's place is its "kind" in data/site/stay-safer.json. */
const helpSigns = slug => { const s = subBySlug[slug]; return s && !NO_SIGNS.includes(slug) ? (SAFE.signs || {})[s.cls] || null : null; };
const helpTitle = () => "If it gets too much";
function helpHtml(slug) {
  slug = slug || renderedDrug;
  const fam = helpSigns(slug); if (!fam) return "";
  const kind = x => x.kind || "calm", ww = fam.while_waiting || [], self = fam.self || [], dn = fam.do_not || [], cn = fam.call_now || [];
  const helps = ww.filter(x => kind(x) !== "aid").concat(ww.filter(x => kind(x) === "aid"));
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  return (self.length ? '<h3 class="hp-h">For you</h3>' + srcList(self) : "") +
    '<h3 class="hp-h">For a friend</h3>' +
    (helps.length ? '<h4 class="sf-k">What helps</h4>' + srcList(helps) : "") +
    (dn.length ? '<h4 class="sf-k">What not to do</h4>' + srcList(dn) : "") +
    (cn.length ? '<h4 class="sf-k">Call an ambulance if</h4>' + srcList(cn) : "") +
    (em ? '<p class="hp-num">The emergency number in ' + esc(inCtry(PREF_COUNTRY)) + ' is <a href="tel:' + esc(telOf(em.numbers[0])) + '"><b>' + esc(em.numbers[0].n) + "</b></a>. " + srcIcons(em.numbers[0].src) + "</p>" : "") +
    '<p class="hp-more"><a href="#emergency">Emergency numbers by country</a></p>';
}
/* Where to get tests, country by country (data/site/tests-world.json; decision p-kits-world): what a source says about
   the law on test kits, free tests, sellers that ship there (only those a harm reduction group, drug checking service or
   health body points people to), and testing by post inside that country. Every line has its source and a second reading. */
const KW = (typeof TESTS_WORLD !== "undefined" && TESTS_WORLD) || { sellers: [], post: [], free: [], law: [] };
const EU_MEMBERS = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands (Kingdom of the)", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"];
function shipsTo(sel, un) {
  const sh = sel.ships || {}, has = l => (l || []).some(n => n === un || (n === "European Union" && EU_MEMBERS.includes(un)));
  if (sel.based_in === un) return true;
  if (sh.kind === "worldwide") return true;
  if (sh.kind === "worldwide-except") return !has(sh.except);
  if (sh.kind === "list" || sh.kind === "domestic-only") return has(sh.countries);
  return false;
}
// the seller's own page for one drug's kits, where a second reader confirmed it (data/site/kit-links.json, matched to
// the seller's row by name); otherwise the seller's shop
const KITL = (typeof KIT_LINKS !== "undefined" && KIT_LINKS) || {};
const kitLink = (sel, slug) => (slug && (KITL[norm(sel.name)] || {})[slug]) || null;
// what there is for one country, each line with its sources: free tests, the sellers that say they send there (those with a
// page for this drug's kits first), testing by post, and what the law says about kits. On a drug's Test kits section and on
// the drug checking page.
function kitsWhere(un, slug) {
  const nm = esc(inCtry(un)), law = KW.law.filter(x => x.country === un), free = KW.free.filter(x => x.country === un), post = KW.post.filter(x => x.country === un);
  const sellers = KW.sellers.filter(x => shipsTo(x, un)).sort((a, b) => !!kitLink(b, slug) - !!kitLink(a, slug) || (b.based_in === un) - (a.based_in === un) || (b.kind === "harm reduction non-profit") - (a.kind === "harm reduction non-profit") || a.name.localeCompare(b.name));
  const where = x => x.region && !String(x.line).includes(x.region) ? " (" + esc(x.region) + ")" : "";
  const li = x => "<li>" + esc(x.line) + where(x) + lineSrc(x.anchors) + "</li>";
  const row = x => { const k = kitLink(x, slug);
    return '<li class="kit-row"><a class="kit-go" href="' + esc(k ? k.url : x.url) + '" target="_blank" rel="noopener"><span class="kit-n">' + esc(x.name) + "</span>" + (k && k.label ? '<span class="kit-l">' + esc(k.label) + "</span>" : "") + icon("arrow") + "</a>" +
      '<span class="kit-s">' + esc(x.sells_line) + (x.based_in === un ? ", in " + nm : x.based_in_short ? ", " + esc(x.based_in_short) : "") + lineSrc((x.anchors || []).concat(x.pointers || [])) + "</span></li>"; };
  const warn = sellers.filter(x => x.warning);
  return {
    sellers: sellers.length ? '<ul class="kit-rows">' + sellers.map(row).join("") + '</ul><p class="kit-note">Harm reduction groups or health services point people to these sellers. We have not tested their kits.' +
      (warn.length ? " Some say they do not refund parcels that customs hold or refuse." + lineSrc(warn.flatMap(x => x.warning.anchors || [])) : "") + "</p>"
      : '<p class="say small">We have not found a seller that says it sends test kits to ' + nm + ".</p>",
    free: free.length ? '<h4 class="sf-k">Free tests</h4><ul class="sf-list">' + free.map(li).join("") + "</ul>" : "",
    post: post.length ? '<h4 class="sf-k">Testing by post</h4><ul class="sf-list">' + post.map(li).join("") + "</ul>" : "",
    law: law.length ? '<details class="sf-more"><summary>Test kits and the law in ' + nm + '</summary><ul class="sf-list">' + law.map(li).join("") + "</ul></details>"
      : '<p class="say small">We have not found what the law in ' + nm + " says about test kits.</p>"
  };
}
// the graded answers on test kits that belong to this drug's tests (at most two), each opening its evidence over the page,
// and the way to every answer on the drug checking page
function kitAnswersHtml(slug) {
  const all = drugQuestions(DC); if (!all.length) return "";
  const qOf = Object.fromEntries(all.map(([id, q]) => [id, q]));
  const mine = (KITSBY[slug] || []).filter(id => qOf[id] && (SIMPLE.claims || {})[id]).slice(0, 2).map(id => [id, qOf[id]]);
  const link = '<a href="#checking/kits">' + (mine.length ? "Every answer on test kits" : "Do home test kits work? What studies found") + "</a>";
  if (!mine.length) return '<p class="sf-evl">' + icon("book") + link + "</p>";
  return '<details class="sf-more sf-ev"><summary>Do these tests work? ' + (mine.length === 1 ? "One answer" : mine.length + " answers") + " from studies</summary>" + mine.map(([id, q]) => { const c = claimById[id], sp = SIMPLE.claims[id];
    return '<a class="sf-ans" href="#' + id + '"><span class="sf-aq">' + esc(q) + '</span><span class="sf-as">' + esc(sp.short) + "</span>" +
      (sp.but ? '<span class="sf-ab"><b>But</b> ' + esc(butText(sp.but)) + "</span>" : "") + '<span class="sf-af">' + meterHtml(c.grade.certainty, true) + '<span class="in-go">The evidence ' + icon("arrow") + "</span></span></a>"; }).join("") +
    '<p class="sf-evl">' + icon("book") + link + "</p></details>";
}
/* Do home test kits work? Every graded answer on drug checking (the senior author's question, 26 October), on the drug
   checking page: In short first, then the questions by topic; each answer's evidence opens over the page. */
function dcKitsHtml() {
  const qs = drugQuestions(DC); if (!qs.length) return "";
  const groups = (QUESTIONS[DC] || []).map(g => [g.topic, g.items.filter(([id]) => claimById[id])]).filter(([, it]) => it.length);
  // no draft banner (the senior author's decision of 13 November 2026: he holds editorial responsibility for what is published; METHODS §12, 0.3.2)
  const draft = "";
  return '<h2 id="dc-kits-h">' + icon("flask") + "<span>Do home test kits work?</span></h2>" +
    '<p class="say">What studies found when test strips and colour tests were checked in a laboratory, and what people did after testing.</p>' + draft +
    inShortHtml(qs, [], { hid: "dck-in-h", tag: "h3" }) +
    groups.map(([t, it], i) => '<h3 class="qh">' + esc(t) + "</h3>" + askList(it, "dck-" + i, 4, null, DC)).join("");
}
/* ---------- Facts about drug use: the answers about no single drug (women and men, genes and family, the words used about
   people, starting young), with their own In short and quiz (the senior author, 31 October: general facts such as men and
   women and telescoping, with a critical eye). Claims of substance "general"; questions in data/site/questions.json. ---------- */
function renderFacts() {
  const box = document.getElementById("facts-box"); if (!box) return;
  const qs = drugQuestions(GEN);
  if (!qs.length) { box.innerHTML = '<p class="say">The first answers are being checked. They will appear here soon.</p>'; return; }
  const topics = []; qs.forEach(([, , t]) => { if (!topics.includes(t)) topics.push(t); });
  // with many topics, the same "On this page" chips as a drug page (they jump without changing the address)
  const chips = topics.length >= 4 ? '<nav class="chips" aria-label="On this page">' + topics.map((t, i) => '<a href="#facts-t' + i + '" data-go="facts-t' + i + '">' + esc(t) + "</a>").join("") + "</nav>" : "";
  box.innerHTML = (inShortHtml(qs, [], { hid: "facts-in-h" }) || "") + chips +
    topics.map((t, i) => '<section class="sec" id="facts-t' + i + '" aria-labelledby="facts-t' + i + '-h"><h2 id="facts-t' + i + '-h">' + esc(t) + '</h2><div class="sec-b">' +
      askList(qs.filter(([, , tt]) => tt === t), "facts" + i, 4, "fx-", GEN) + "</div></section>").join("") +
    // the page's own Myth or fact? deck, when it has at least 3 statements
    (mfCount(mfPagePool(GEN)) >= 3 ? '<section class="sec quizsec" aria-labelledby="facts-quiz-h"><h2 id="facts-quiz-h">Myth or fact?</h2><div class="qz2 mf" id="qz-facts"></div></section>' : "");
  mfStart("qz-facts", GEN);
}
function openFact(id) {
  const d = document.getElementById("fx-" + id); if (!d) return false;
  const more = d.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
  d.open = true; setTimeout(() => scrollToEl(d), 30); return true;
}
// the menu item and the home card appear once the page has answers
function factsLinks() { const on = drugQuestions(GEN).length > 0; document.querySelectorAll("[data-facts]").forEach(el => { el.hidden = !on; }); }
function renderDcKits() { const box = document.getElementById("dc-kits"); if (!box) return; const h = dcKitsHtml(); box.innerHTML = h; box.hidden = !h; }
/* Test kits, a section of its own near the end of a drug page (senior author, 15 November: "the test kits are low priority
   and should be very discreetly kept inside the website"; "individualized for each drug ... if a user wants to buy something
   they should be able to buy it immediately and it should be at the top"; "each respective fact about the test kits should
   be cited"). Buying first: one row per seller that says it sends to the reader's country, each straight to that seller's
   page for this drug's kits where we have it; then the facts about the tests; what a home test cannot tell; the answers
   from studies; and drug checking services. The country is the one the reader chose, or until then the one their device's
   time zone suggests, with a way to change it. Every line carries its sources. */
function testHtml(slug) {
  slug = slug || renderedDrug;
  const T = SAFE.tests || {}, own = (T.drugs || {})[slug] || [], none = (T.none_found || []).includes(slug), common = T.common || [];
  const more = (T.more || {})[slug] || [], unproven = (T.none_validated || []).includes(slug), name = esc(pageWord(slug));
  const un = PREF_COUNTRY || guessCountry() || "", nm = un ? esc(inCtry(un)) : "", kw = un ? kitsWhere(un, slug) : null;
  let h = "";
  // a kit is worth buying only where a home test works for this drug
  if (!unproven && own.length) {
    h += '<h3 class="tk-h">Test kits for ' + name + "</h3>" +
      (un ? '<div class="cq set tk-cq"><p class="cq-where">' + icon("pin") + "<span>Sellers that say they send to <b>" + esc(shortCtry(un)) + '</b></span></p><button type="button" class="cq-change">' + (PREF_COUNTRY ? "Change country" : "Another country") + '</button><span class="cq-sel" hidden><label class="sr" for="tk-ctry">Your country</label>' + ctrySelectHtml("tk-ctry") + "</span></div>" + kw.sellers + kw.free
        : countryAsk());
  }
  if (own.length) {
    // tests are named, but none has been shown to work for this drug: said first, so nobody takes a colour for proof
    h += '<h3 class="tk-h">' + (unproven ? "No home test has been shown to work for " + name : "Home tests") + "</h3>" + srcList(unproven ? own : own.slice(0, 3));
    const extra = (unproven ? [] : own.slice(3)).concat(more);
    if (extra.length) h += '<details class="sf-more"><summary>More about these tests</summary>' + srcList(extra) + "</details>";
    h += kitAnswersHtml(slug);
    if (common.length) h += '<h3 class="tk-h">What home tests can’t tell you</h3>' + srcList(common);
  } else if (none) {
    h += '<p class="say">We have not found a home test for ' + name + ".</p>" + srcList((common[3] ? [common[3]] : []).concat(more)) + kitAnswersHtml(slug);
  }
  // a lab check tells you more than any home test: the services where the reader is, and testing by post
  h += '<h3 class="tk-h">Drug checking</h3>';
  if (un) { const sv = dcFor(un);
    h += sv.length ? '<p class="say small">' + sv.length + " service" + (sv.length === 1 ? "" : "s") + " in " + nm + ' that test a sample for you. <a href="#checking">See where</a></p>'
      : '<p class="say small">We have not found a drug checking service in ' + nm + ' yet. <a href="#checking">Drug checking by country</a></p>';
    h += kw.post + (own.length && !unproven ? kw.law : "");
  } else h += '<p><a class="go" href="#checking">Drug checking by country</a></p>';
  return h;
}

/* Staying safer: test it, where to read about doses, and who to call. We do not write doses or how to take a drug
   (decision p-no-doses); harm reduction groups that do are linked, and licensed medicines link to their official leaflet. */
const HARM = (typeof HARM_LINKS !== "undefined" && HARM_LINKS) || { drugs: {} };
/* The senior author's own words on doses (senior author, 23 October 20:34: "yes" to a space where he writes them).
   Stored in the site's database at doses/<drug>; only the owner can write; every reader sees it. The AI co-editor
   does not write, edit or check this text (decision p-no-doses). */
const DOSES = { owner: false, db: null, uid: null, docs: {}, editing: null };
(async () => {
  try {
    if (!window.claude || !window.claude.use) return;
    const [d, u] = await Promise.all([window.claude.use("db"), window.claude.use("user")]);
    if (!d) return;
    DOSES.db = d; DOSES.owner = u ? await u.isOwner() : false; DOSES.uid = u && u.id ? await u.id() : null;
    d.collection("doses").onSnapshot(snap => { const m = {}; snap.docs.forEach(x => { m[x.id] = x.data(); }); DOSES.docs = m; refreshDoses(); }, () => {});
    refreshDoses();
  } catch (e) { /* the page works without it */ }
})();
// the author's text as written: blank lines start a new paragraph, lines starting with "- " are a list
function authorText(t) {
  return String(t || "").trim().split(/\n\s*\n/).map(block => { const lines = block.split("\n").map(x => x.trim()).filter(Boolean);
    return lines.every(x => /^[-•] /.test(x)) ? "<ul>" + lines.map(x => "<li>" + esc(x.slice(2)) + "</li>").join("") + "</ul>" : "<p>" + lines.map(esc).join("<br>") + "</p>"; }).join("");
}
const linkify = t => esc(t).replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>').replace(/\bdoi:\s?(10\.[^\s<]+)/gi, (m, d) => '<a href="https://doi.org/' + d + '" target="_blank" rel="noopener">' + m + "</a>");
function seniorDosesHtml(slug) {
  const x = DOSES.docs[slug], has = x && String(x.text || "").trim();
  let h = "";
  if (has) h += '<div class="sa-doses"><p class="sa-by">Written by <a href="#about">our senior author</a>' + (x.updated ? " · updated " + esc(dcDate(String(x.updated).slice(0, 10))) : "") + '</p><div class="sa-text">' + authorText(x.text) + "</div>" +
    (String(x.sources || "").trim() ? '<details class="sa-src"><summary>Sources</summary><ul>' + String(x.sources).split("\n").map(l => l.trim()).filter(Boolean).map(l => "<li>" + linkify(l) + "</li>").join("") + "</ul></details>" : "") + "</div>";
  if (DOSES.owner) h += DOSES.editing === slug ?
    '<form class="sa-form" data-slug="' + esc(slug) + '"><label for="sa-text">Your text for readers</label><textarea id="sa-text" rows="10">' + esc(has ? x.text : "") + '</textarea>' +
    '<label for="sa-sources">Sources, one per line</label><textarea id="sa-sources" rows="4">' + esc(x && x.sources || "") + '</textarea><p class="sa-hint">Only you can see this box. A blank line starts a new paragraph; start a line with "- " for a list. Saving puts it on the page for every reader.</p>' +
    '<p class="sa-btns"><button type="submit" class="sa-save">Save</button><button type="button" class="sa-cancel">Cancel</button></p><p class="sa-status" aria-live="polite"></p></form>'
    : '<p><button type="button" class="sa-edit" data-slug="' + esc(slug) + '">' + (has ? "Edit your text" : "Write this part yourself") + "</button>" + (DOSES.saved === slug ? ' <span class="sa-status" role="status">Saved</span>' : "") + "</p>";
  return h;
}
function refreshDoses() {
  if (!renderedDrug) return;
  const card = document.getElementById("sf-dose"), body = dosesBody(renderedDrug);
  if (card) { card.querySelector(".sf-b").innerHTML = body; return; }
  // a drug with no links yet gets its Doses section as soon as the author's text or the owner's button exists: the page is
  // drawn again as it stood
  if (body && document.querySelector("#drug2 .secmenu")) { const open = openSec(), y = window.scrollY; renderDrug(renderedDrug); if (open) showSec(open); window.scrollTo(0, y); }
}
document.addEventListener("click", e => {
  const ed = e.target.closest && e.target.closest("button.sa-edit");
  if (ed) { DOSES.editing = ed.dataset.slug; DOSES.saved = null; refreshDoses(); const t = document.getElementById("sa-text"); if (t) t.focus(); return; }
  if (e.target.closest && e.target.closest("button.sa-cancel")) { DOSES.editing = null; refreshDoses(); }
});
document.addEventListener("submit", async e => {
  const f = e.target.closest && e.target.closest("form.sa-form"); if (!f) return;
  e.preventDefault();
  const st = f.querySelector(".sa-status"), slug = f.dataset.slug;
  if (!DOSES.db || !DOSES.owner) { st.textContent = "Saving works on the live site, signed in as its owner."; return; }
  try {
    await DOSES.db.doc("doses/" + slug).set({ text: document.getElementById("sa-text").value, sources: document.getElementById("sa-sources").value, updated: new Date().toISOString(), by: DOSES.uid });
    DOSES.editing = null; DOSES.saved = slug; refreshDoses(); const b = document.querySelector("button.sa-edit"); if (b) b.focus();
  } catch (err) { st.textContent = "Not saved (" + (err && err.code ? err.code : "unavailable") + "). Your text is still in the box; try again."; }
});
function harmLinksHtml(slug) {
  const d = (HARM.drugs || {})[slug]; if (!d) return "";
  // at most three pages per group, so the card stays short
  const site = (k, label) => Array.isArray(d[k]) && d[k].length ? d[k].slice(0, 3).map(x => '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(label + (d[k].length > 1 ? ": " + (x.label || x.title) : "")) + "</a>").join("") : "";
  const links = site("tripsit", "TripSit") + site("dancesafe", "DanceSafe") + site("psychonautwiki", "PsychonautWiki");
  const med = Array.isArray(d.medlineplus) && d.medlineplus.length ? '<p class="say small">Official leaflet for the medicine: ' + d.medlineplus.map(x => '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.medicine) + "</a>").join(", ") + " (MedlinePlus, US National Library of Medicine)</p>" : "";
  if (!links && !med) return "";
  const own = DOSES.docs[slug] && String(DOSES.docs[slug].text || "").trim();
  return (links ? '<p class="say">' + (own ? "Harm reduction groups that publish doses:" : "We don’t list doses. These harm reduction groups do:") + '</p><p class="hlinks">' + links + '</p><p class="small muted">Run by others. We have not checked their pages.</p>' : "") + med;
}
const dosesBody = slug => seniorDosesHtml(slug) + harmLinksHtml(slug);
const NO_TEST = ["alcohol", "caffeine", "nicotine", "nitrous-oxide", "alkyl-nitrites-and-inhalants"];

/* The emergency and drug checking pages: your country first; every other country one tap away */
function renderEmMine() {
  const box = document.getElementById("em-mine"); if (!box) return;
  if (!PREF_COUNTRY) { box.innerHTML = countryAsk(true); return; }
  const em = emFor(PREF_COUNTRY), nm = esc(inCtry(PREF_COUNTRY));
  if (!em) { box.innerHTML = countryAsk(true) + '<p class="say">We have not checked the emergency number for ' + nm + " yet. We add a country only after checking its number with an official source.</p>"; return; }
  const x = em.numbers[0], others = em.numbers.slice(1);
  box.innerHTML = countryAsk(true) + '<a class="callbtn" href="tel:' + esc(telOf(x)) + '">' + icon("phone") + "<span>Call <b>" + esc(x.n) + "</b></span></a>" +
    '<p class="mine-note">' + (x.note ? esc(x.note) + ". " : "") + "The emergency number in " + nm + " " + srcIcons(x.src) + "</p>" +
    (others.length || em.more ? '<ul class="em-more mine-more">' + others.map(y => '<li><a class="em-n" href="tel:' + esc(telOf(y)) + '">' + esc(y.n) + '</a><span class="mm-t">' + esc(y.note || "Also the emergency number") + " " + srcIcons(y.src) + "</span></li>").join("") +
      (em.more || []).map(y => '<li><a class="em-n" href="tel:' + esc(telOf(y)) + '">' + esc(y.n) + '</a><span class="mm-t">' + esc(y.what) + " " + srcIcons(y.src) + "</span></li>").join("") + "</ul>" : "");
}
// the drug checking page: test kits for the reader's country, with their sources one tap away
function kitsBox(un) { const kw = kitsWhere(un); return '<section class="kw-box"><h2 class="qh">Test kits in ' + esc(inCtry(un)) + "</h2>" + kw.free + kw.sellers + kw.post + kw.law + "</section>"; }
function renderDcMine() {
  const box = document.getElementById("dc-mine"); if (!box) return;
  if (!PREF_COUNTRY) { box.innerHTML = countryAsk(true); return; }
  const s = dcFor(PREF_COUNTRY), nm = esc(inCtry(PREF_COUNTRY));
  const rep = dcReported(PREF_COUNTRY);
  if (!s.length) { box.innerHTML = countryAsk(true) + '<p class="say">' + (rep ? "We have not found a drug checking service in " + nm + " yet." : dcSearchedNone(PREF_COUNTRY) ? "We searched and have not found a drug checking service in " + nm + " yet. One may still exist." : "We have not searched for drug checking in " + nm + " yet.") + "</p>" +
    (rep ? '<p class="dc-rep">' + esc(rep.line) + " " + srcIcons(rep.sources.map(x => x.ref)) + "</p>" : "") + kitsBox(PREF_COUNTRY); return; }
  const order = x => (x.active === "yes" ? 0 : x.active === "closed" ? 2 : 1), open = s.filter(x => x.active !== "closed").length;
  const all = s.slice().sort((a, b) => order(a) - order(b) || a.name.localeCompare(b.name)), first = all.slice(0, 4), rest = all.slice(4);
  box.innerHTML = countryAsk(true) + '<p class="say">' + (open ? open + " service" + (open === 1 ? "" : "s") + " in " + nm : "We found no drug checking service running in " + nm + ". This one has closed:") + '</p><div class="mine-list">' + first.map(dcCard).join("") + "</div>" +
    (rest.length ? '<div class="mine-list" id="dc-mine-more" hidden>' + rest.map(dcCard).join("") + '</div><button type="button" class="morebtn" data-more="dc-mine-more">' + rest.length + " more in " + nm + "</button>" : "") + kitsBox(PREF_COUNTRY);
}

/* In short: three answers on the first screen, no tapping needed (senior author, 26 October: people want something useful
   at once). The first question of each topic, in the editors' order of topics (data/site/questions.json), with its catch
   and how sure the research is; tapping one opens all its evidence over the page. */
function inShortHtml(qs, skip, opt) {
  // an answer the page already shows open (a single "What does it feel like?") is not repeated here
  // early drafts only when the page has too few answers past the first rung (In short is the simple layer's At a glance, METHODS §8)
  const can = qs.filter(([id]) => (SIMPLE.claims || {})[id] && !(skip || []).includes(id)), firm = can.filter(([id]) => claimById[id].verification.status !== "draft");
  const picks = roundRobin(firm.length >= 2 ? firm : can).slice(0, 3);
  if (picks.length < 2) return "";
  // another page can carry its own In short (the drug checking page): its own heading id and level
  const hid = (opt && opt.hid) || "in-h", tag = (opt && opt.tag) || "h2";
  return '<section class="inshort2" aria-labelledby="' + hid + '"><' + tag + ' id="' + hid + '">In short</' + tag + '><ul class="in-list">' + picks.map(([id, q]) => {
    const c = claimById[id], sp = SIMPLE.claims[id];
    return '<li><a class="in-a" href="#' + id + '"><span class="in-q">' + esc(q) + '</span><span class="in-s">' + cueNum(esc(sp.short)) + "</span>" +
      (sp.but ? '<span class="in-but"><b>But</b> ' + esc(butText(sp.but)) + "</span>" : "") + '<span class="in-f">' + meterHtml(c.grade.certainty, true) + '<span class="in-go">The evidence ' + icon("arrow") + "</span></span></a></li>";
  }).join("") + '</ul><p class="in-key">' + meterDots("moderate") + "<span>The bars show how sure the research is. Four bars is the strongest.</span></p></section>";
}
// the first clause of a short answer, where there is room for one line only (Insight's results): cut where a clause ends, at about 60 characters, with an ellipsis, and never
// inside a number ("about 1 in 6", "43 to 49 in 100"). A short opening and its colon read on ("Slightly: about half a point
// less pain…"); a comma after an opening phrase ("In lab studies,"), or around a short aside ("most of all daily"), is not
// where a clause ends; with no clause end in reach, the cut falls between whole words, never on a number or on a word that
// leads into the next one.
const GL_STOP = new Set(("a an the and or but nor so of to in into on onto at by for from with within without about after before between among over under per via than that which who whose whom " +
  "as is are was were be been being has have had do does did more most much many very their its his her our your own this these those not no when where while if they it them there " +
  "same such also still even both each every any some all least clearly mostly largely mainly usually really fully partly highly reliably strongly measurably").split(" "));
const GL_INTRO = /^(?:in|at|on|for|after|before|with|without|among|compared|of|from|over|under|within|during|across|by|since|until|unlike|like|despite|through|between|when|while|if|once|where|although|though|because|as|each|every|the (?:morning|day|night|week|year)s?)\b/i;
function glanceClause(t) {
  t = String(t || "").trim(); if (t.length <= 60) return t;
  const bound = /[.;:!?](?=\s)|\s[–—]\s/g;
  let m = bound.exec(t), first = m ? t.slice(0, m.index) : t.replace(/[.!?]$/, ""), lead = 0;
  while (m && t[m.index] === ":" && first.length <= 24) { lead = m.index + 2; m = bound.exec(t); first = m ? t.slice(0, m.index) : t.replace(/[.!?]$/, ""); }
  if (first.length <= 72) return first + (m ? "…" : "");
  const cs = [...first.matchAll(/, /g)].map(x => x.index).filter(p => p > lead);
  const ok = cs.filter((p, i) => p >= 25 && p <= 66 && !(i + 1 < cs.length && cs[i + 1] - p <= 26) && !(i > 0 && p - cs[i - 1] <= 26) && !(i === 0 && GL_INTRO.test(first.slice(lead))));
  if (ok.length) return first.slice(0, ok[ok.length - 1]) + "…";
  const all = first.split(" "), words = [];
  for (let len = -1; words.length < all.length && len + 1 + all[words.length].length <= 66;) len += 1 + all[words.length].length, words.push(all[words.length]);
  const bare = w => String(w || "").toLowerCase().replace(/^[("“‘]+|[,;:()"“”‘’]+$/g, "");
  while (words.length > 3) {
    const w = bare(words[words.length - 1]), nx = bare(all[words.length]);
    if (GL_STOP.has(w) || /\d/.test(w) || /[("“‘]$/.test(words[words.length - 1]) || (/^(?:around|nearly|almost|only|just|roughly|up|out)$/.test(w) && /^(?:\d|of$|to$)/.test(nx))) words.pop(); else break;
  }
  return words.join(" ").replace(/[,;:]+$/, "") + "…";
}

/* The page itself (site 2.3, 15 November 2026; the senior author: "either nothing shows or only the description of the drug
   shows ... you should be able to choose from the menu the section you want to read"; his brother, who used the site: "when
   he clicked on a section in the menu he would like then the section to pop up and when he clicks on another section the
   previous to close and the new to pop up so as not to get lost in all that info because then he won't want to read it").
   A drug page is its name, its other names, a short description with its sources, and the section menu: a list of large
   rows, each a section's name in people's words, how many answers it holds and a quiet line of what is inside. Choosing a
   row opens that section alone, and the list becomes a row of chips stuck under the header, with the drug's name first (the
   way back to the list); choosing another closes the first and opens the new one at its start; choosing the open one again
   closes it and brings the list back. The open section is in the address (#s-<drug>/part-<section>), so Back and Forward
   walk through them, and a link to a question (#s-<drug>/q-<claim>) opens its section with the question open and in view.
   Two levels only: section, then question; a section's topics are plain headings, and one question is open at a time.
   Gone with 2.2: "At a glance", the line "Someone unwell?" under the name, the count of answers opened, "Want the details?"
   and the research page it led to (Quick answers / Full evidence). */
const SEC_ICON = { "d-feel": "pulse", "d-mix": "mix", "d-after": "moon", "d-risk": "alert", "d-med": "plus", "d-looks": "eye", "d-law": "scale", "d-quiz": "bulb", "d-help": "heart", "d-kits": "flask", "d-doses": "book" };
/* The order of the sections, the same on every drug page so that it can be learned: the kinds of section that hold answers
   by how much people ask about them (the sum of the DEMAND scores of every drug's answers of that kind, worked out once),
   then what the drug looks like, the law and the page's own cards, and last the three to reach for when needed: if it gets
   too much, test kits, doses. */
let SEC_ORDER = null;
function secOrder() {
  if (SEC_ORDER) return SEC_ORDER;
  const sum = { "d-risk": 0, "d-after": 0, "d-mix": 0, "d-med": 0, "d-feel": 0 };
  SUBSTANCES.forEach(s => {
    drugQuestions(s.slug).forEach(([id, , t]) => { const z = topicZone(t); if (z !== "mix") sum["d-" + z] += Math.max(0, demandOf(id)); });
    mixQuestions(s.slug).forEach(([id]) => { sum["d-mix"] += Math.max(0, demandOf(id)); }); });
  return (SEC_ORDER = Object.keys(sum).sort((a, b) => sum[b] - sum[a]).concat(["d-looks", "d-law", "d-quiz", "d-help", "d-kits", "d-doses"]));
}
// a section's answers under their topics, as plain headings: the topics in the order of their most-asked answer, each topic's
// answers by how much people ask about them (DEMAND), equals in the editors' order. A section that runs in time (before,
// during and after) keeps its order; mixing is one list (its answers come from two pages); one topic needs no heading.
function secTopics(items, opt) {
  const flat = opt && opt.flat, timed = opt && opt.timed, names = [];
  if (flat) return [["", byDemand(items)]];
  items.forEach(x => { if (!names.includes(x[2])) names.push(x[2]); });
  const groups = names.map(t => [t, timed ? items.filter(x => x[2] === t) : byDemand(items.filter(x => x[2] === t))]);
  const top = g => Math.max(...g[1].map(x => demandOf(x[0])));
  return timed ? groups : groups.map((g, i) => [g, i]).sort((a, b) => top(b[0]) - top(a[0]) || a[1] - b[1]).map(p => p[0]);
}
function secAsks(groups, key, slug) {
  return groups.map(([t, it], i) => (groups.length > 1 ? '<h3 class="tp">' + esc(t) + "</h3>" : "") + askList(it, key + (groups.length > 1 ? "-" + i : ""), 999, null, slug)).join("");
}
// the quiet line of a row: the section's topics (the first three), or with one topic its first question
const secLine = groups => groups.length > 1 ? groups.slice(0, 3).map(g => g[0]).join(" · ") + (groups.length > 3 ? " · more" : "") : groups[0] && groups[0][1][0] ? groups[0][1][0][1] : "";
let renderedDrug = null;
function renderDrug(slug) {
  const s = subBySlug[slug], m = monographFor(slug); if (!s || !m) return;
  renderedDrug = slug; currentSlug = slug;
  const f = fam(s.cls), fp = famPlain(s.cls), ph = headerPhoto(slug), names = documentedNames(slug).slice(0, 3);
  const qs = drugQuestions(slug), zone = z => qs.filter(([, , t]) => topicZone(t) === z);
  const forms = (FORMS[slug] || []).filter(x => x.name), nForms = (FORMS[slug] || []).length, short = s.name.replace(/\s*\(.*\)$/, "");
  const S = {}, nAns = n => n + (n === 1 ? " answer" : " answers");
  const add = (id, name, chip, body, n, line) => { S[id] = { id, name, chip, body, n, line }; };
  const asks = (id, name, chip, items, key, opt, after) => { if (!items.length) return; const g = secTopics(items, opt); add(id, name, chip, secAsks(g, key, slug) + (after || ""), nAns(items.length), secLine(g)); };
  asks("d-risk", "What can go wrong?", "Risks", zone("risk"), "risk");
  // before and during use, then the day after, then the weeks after stopping (decisions p-day-after, p-before-during-after): a
  // time sequence keeps its order, and within its steps the questions run in time order too
  const after = zone("after");
  if (after.length) {
    const has = re => after.some(([, , t]) => re.test(t)), bef = has(/^before/i), day = has(/day after/i), stop = has(/after stopping/i);
    const ordered = [/^before/i, /day after/i, /after stopping/i].flatMap(re => after.filter(([, , t]) => re.test(t)));
    asks("d-after", bef ? (day || stop ? "Before, during and after" : "Before and during") : stop ? (day ? "The day after, and after stopping" : "After stopping") : "The day after",
      bef ? "Before & after" : day ? "Day after" : "After stopping", ordered, "after", { timed: true });
  }
  // mixing: the page's own answers and the mixing page's answers about this drug
  asks("d-mix", "Is it safe to mix?", "Mixing", mixQuestions(slug), "mix", { flat: true }, '<p><a class="go" href="#interactions">Mixing drugs: every answer we have</a></p>');
  // the drug as a medicine, or treatment in hospital or clinic (for example after a long PCP psychosis): the heading names which
  const med = zone("med"), medAs = med.some(([, , t]) => /as a medicine/i.test(t)), medTx = med.some(([, , t]) => /treatment/i.test(t) && !/as a medicine/i.test(t));
  asks("d-med", medAs ? (medTx ? "As a medicine, and treatment" : "Is it used as a medicine?") : "What can treatment do?", medAs ? "Medicine" : "Treatment", med, "med");
  asks("d-feel", "What does it feel like?", "Feels", zone("feel"), "feel");
  // what it looks like: photos first, and looks do not tell you what is inside
  if (forms.length) add("d-looks", "What does it look like?", "Looks", formsHtml(slug), forms.length + (forms.length === 1 ? " form" : " forms"), forms.slice(0, 3).map(x => x.name).join(" · ") + (forms.length > 3 ? " · more" : ""));
  if (LEGAL.some(d => d.substance === slug)) add("d-law", "Is it legal where I am?", "Law", lawHtml(slug), "", "What the law says in your country");
  // the page's own Myth or fact? deck (its statements only), when it has at least 3 (senior author, 14 November)
  const deckN = mfCount(mfPagePool(slug));
  if (deckN >= 3) add("d-quiz", "Myth or fact?", "Myth or fact?", '<div class="qz2 mf" id="qz-drug"></div>', deckN + " cards", "Guess first, then see what studies found");
  if (helpSigns(slug)) add("d-help", helpTitle(), "Too much", helpHtml(slug), "", "What helps, what not to do, and when to call an ambulance");
  // drug checking is for drugs bought on the street or online, not for drinks, coffee, cigarettes or gas canisters
  if (!NO_TEST.includes(slug)) { const T = SAFE.tests || {}, buy = ((T.drugs || {})[slug] || []).length && !(T.none_validated || []).includes(slug);
    add("d-kits", "Test kits", "Test kits", testHtml(slug), "", buy ? "Where to buy them, and what they can and can’t tell you" : "What home tests can and can’t tell you"); }
  // doses: the senior author's own text, and the harm reduction groups that publish them (decision p-no-doses)
  const doses = dosesBody(slug);
  if (doses) add("d-doses", "Doses", "Doses", '<div class="sf" id="sf-dose"><div class="sf-b">' + doses + "</div></div>", "", "Where to read about them");
  const secs = secOrder().map(id => S[id]).filter(Boolean);
  const row = x => '<button type="button" class="sm-b" id="sm-' + x.id + '" data-sec="' + x.id + '" aria-expanded="false" aria-controls="' + x.id + '"><span class="sm-ic" aria-hidden="true">' + icon(SEC_ICON[x.id] || "molecule") + "</span>" +
    '<span class="sm-t"><span class="sm-n">' + esc(x.name) + '</span><span class="sm-m">' + (x.n ? '<b class="sm-c">' + esc(x.n) + "</b>" : "") + (x.line ? '<span class="sm-l">' + esc(x.line) + "</span>" : "") + "</span></span>" +
    '<span class="sm-s">' + esc(x.chip) + '</span><span class="sm-go" aria-hidden="true">' + icon("arrow") + "</span></button>";
  // no draft banner (the senior author's decision of 13 November 2026: he holds editorial responsibility for what is published;
  // METHODS §12, 0.3.2); "not medical advice" stays in the footer and on the About page
  const h = '<header class="dh f-' + f.k + (ph ? " hasph" : "") + '">' + (ph ? '<figure class="dh-ph">' + photoImg(ph, "m", ph.alt, false) + (nForms > 1 && S["d-looks"] ? '<a class="dh-forms" href="#s-' + slug + '/part-d-looks">See all ' + nForms + " forms</a>" : "") + "</figure>" : "") +
    '<div class="dh-t"><p class="dh-fam">' + icon(f.icon) + esc(fp ? fp.word.charAt(0).toUpperCase() + fp.word.slice(1) : s.cls) + "</p><h1>" + esc(s.name) + "</h1>" +
    (names.length ? '<p class="dh-aka">Also called ' + names.map(esc).join(", ") + "</p>" : "") + "</div></header>" + descHtml(slug) +
    (secs.length ? '<nav class="secmenu" id="secmenu" aria-label="Sections of this page" data-open=""><button type="button" class="sm-up" data-sec="" aria-label="' + esc(short) + ': all sections">' + icon("arrow") + "<span>" + esc(short) + "</span></button>" + secs.map(row).join("") + "</nav>" +
      '<div class="secs">' + secs.map(x => '<section class="sec" id="' + x.id + '" aria-labelledby="' + x.id + '-h" hidden><h2 id="' + x.id + '-h" tabindex="-1"><span class="sec-ic">' + icon(SEC_ICON[x.id] || "molecule") + "</span>" + esc(x.name) + '</h2><div class="sec-b">' + x.body + "</div></section>").join("") + "</div>" : "") +
    fbLineHtml() + familyHtml(m);
  const box = document.getElementById("drug2"); box.className = "wrap drug2 f-" + f.k; box.innerHTML = h;  // the family colour runs through the whole page
  applyPhotoPref(); mfStart("qz-drug", slug); pageProgress();
  // the law part fills in when the drug's file arrives; the file is fetched ahead once the page settles, so the evidence opens at once
  lawWait(); fetchAhead(slug);
}
// the section that is open on the drug page ("" while the list shows), and showing one alone, or the list again
const openSec = () => { const nav = document.querySelector("#drug2 .secmenu"); return (nav && nav.dataset.open) || ""; };
function showSec(id) {
  const page = document.getElementById("drug2"), nav = page && page.querySelector(".secmenu"); if (!nav) return false;
  const sec = id ? document.getElementById(id) : null; if (id && !(sec && sec.parentElement && sec.parentElement.classList.contains("secs") && page.contains(sec))) return false;
  page.querySelectorAll(".secs > .sec").forEach(x => { x.hidden = x !== sec; });
  nav.querySelectorAll(".sm-b").forEach(b => b.setAttribute("aria-expanded", String(!!id && b.dataset.sec === id)));
  nav.dataset.open = id || ""; nav.classList.toggle("on", !!id);
  // the chip of the open section in view in its row
  const b = id && nav.querySelector('.sm-b[aria-expanded="true"]'); nav.scrollLeft = b ? Math.max(0, b.offsetLeft - (nav.clientWidth - b.offsetWidth) / 2) : 0;
  updateSticky();
  return true;
}
// where a drug page's address points (the router calls it once the page is drawn and shown): a question, a section, or the
// page itself. o.was: the section that was open when the reader was already on this page.
function drugGo(part, o) {
  if (part && part.startsWith("q-")) {
    const id = part.slice(2), d = document.getElementById("ask-" + id), sec = d && d.closest(".secs > .sec");
    if (d && sec) { showSec(sec.id); d.open = true; scrollToEl(d); const sm = d.querySelector("summary"); if (sm) sm.focus({ preventScroll: true }); return; }
    if (claimById[id]) { location.replace("#" + id); return; }   // an answer this page does not ask opens by its own address
  }
  if (part && part.startsWith("part-")) {
    const id = part.slice(5) === "d-safer" ? "d-kits" : part.slice(5);   // (d-safer: the part that held the test kits before 2.3)
    if (showSec(id)) { const sec = document.getElementById(id), hh = sec.querySelector("h2"); scrollToEl(sec); if (hh) hh.focus({ preventScroll: true }); return; }
  }
  showSec("");
  // back from a section: the list where the chips were, at the row just left; a fresh visit starts at the top
  const nav = document.querySelector("#drug2 .secmenu"), from = o && o.was && document.getElementById("sm-" + o.was);
  if (nav && from) { scrollToEl(nav); from.focus({ preventScroll: true }); return; }
  window.scrollTo({ top: 0 }); if (!(o && o.first)) focusHeading("drug");
}
// the section menu: a row or a chip opens its section; the open one, or the drug's name, brings the list back. The address
// carries it, so each choice is a step Back can undo.
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("#drug2 .secmenu [data-sec]"); if (!b || !renderedDrug) return;
  const id = b.dataset.sec, want = "#s-" + renderedDrug + (id && id !== openSec() ? "/part-" + id : "");
  if (location.hash === want) route(); else location.hash = want;
});
// One question open at a time (site 2.3): opening one closes the one open before it in the same section, and the question
// just opened is brought to the start of the screen (the answer closing above it would push it out of view).
document.addEventListener("toggle", e => {
  const d = e.target; if (!d.matches || !d.matches("details.ask[open]")) return;
  const box = d.closest(".sec") || d.closest(".view"); if (!box) return;
  box.querySelectorAll("details.ask[open]").forEach(x => { if (x !== d) x.open = false; });
  if (d.closest(".view.active")) scrollToEl(d, true);
}, true);
// chips that jump within a page without changing its address (the facts page's topics)
document.addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("[data-go]"); if (!a) return;
  const el = document.getElementById(a.dataset.go); if (!el) return;
  e.preventDefault(); scrollToEl(el); const hh = el.querySelector("h2"); if (hh) { hh.setAttribute("tabindex", "-1"); hh.focus({ preventScroll: true }); }
});
// A jump's target that is folded away is brought out first (scrollToEl calls this for every jump): the rest of a list behind
// its "more" button; on a drug page, the section the target is in (the address follows, as a step Back can undo).
function revealEl(el) {
  const more = el.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
  const sec = el.closest("#drug2 .secs > .sec");
  if (sec && sec.hidden && showSec(sec.id)) {
    const d = el.closest("details.ask[data-cid]"), want = "#s-" + renderedDrug + (d ? "/q-" + d.dataset.cid : "/part-" + sec.id);
    try { if (location.hash !== want) history.pushState(null, "", want); } catch (err) { /* the address stays as it was */ }
  }
}
function openAsk(id) {
  const d = document.getElementById("ask-" + id); if (!d) return false;
  if ("open" in d) d.open = true; setTimeout(() => scrollToEl(d), 30); return true;
}

/* ---------- Mixing: pick a drug, see what we know about mixing it ---------- */
let mixPick = "";
function renderMix2() {
  const box = document.getElementById("mix2"); if (!box) return;
  const all = (QUESTIONS.interactions || []).flatMap(g => g.items.map(([id, q]) => [id, q, g.topic])).filter(([id]) => claimById[id]);
  const has = new Set(all.flatMap(([id]) => MIXFOR[id] || []));
  const order = POPULAR.concat(SUBSTANCES.map(x => x.slug)).filter((x, i, a) => a.indexOf(x) === i && has.has(x) && subBySlug[x]);
  const items = mixPick ? all.filter(([id]) => (MIXFOR[id] || []).includes(mixPick)) : all;
  box.innerHTML = '<div class="mixchips" role="group" aria-label="Pick a drug"><button type="button" class="mixchip" data-mix="" aria-pressed="' + !mixPick + '">All</button>' +
    order.map(x => '<button type="button" class="mixchip" data-mix="' + x + '" aria-pressed="' + (x === mixPick) + '">' + esc(subBySlug[x].name.replace(/\s*\(.*\)$/, "")) + "</button>").join("") + "</div>" +
    '<p class="mix-n" aria-live="polite">' + items.length + " question" + (items.length === 1 ? "" : "s") + (mixPick ? " about " + esc(pageWord(mixPick)) : "") + "</p>" + askList(items, "mixp", 6, "mx-", "interactions");
}
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("button.mixchip"); if (!b) return; mixPick = b.dataset.mix; renderMix2(); const nb = document.querySelector('button.mixchip[data-mix="' + mixPick + '"]'); if (nb) nb.focus(); });

/* ---------- Home: one question, a deck of myths and facts, three ways to get help, the drugs as pictures ---------- */
function renderHome2() {
  const grid = document.getElementById("dgrid"); if (!grid) return;
  const order = POPULAR.concat(SUBSTANCES.map(s => s.slug).filter(x => !POPULAR.includes(x)));
  grid.innerHTML = order.map(sl => subBySlug[sl]).filter(Boolean).slice(0, 12).map((s, i) => {
    const f = fam(s.cls), ph = headerPhoto(s.slug), names = documentedNames(s.slug).slice(0, 2);
    const nm = s.name.replace(/ \(.*\)$/, ""), longest = Math.max(...nm.split(/[\s/]+/).map(w => w.length));
    return '<a class="dcard f-' + f.k + (ph ? " hasph" : " noph") + '" href="#s-' + s.slug + '" style="--i:' + i + '">' + (ph ? '<span class="dc-ph">' + photoImg(ph, "m", "", true) + "</span>" : "") + '<span class="dc-ic">' + icon(f.icon) + "</span>" +
      '<span class="dc-t"><span class="dc-f">' + esc(s.cls) + '</span><span class="dc-n' + (longest > 10 ? " long" : "") + '">' + esc(nm) + "</span>" + (names.length ? '<span class="dc-a">' + esc(names.join(", ")) + "</span>" : "") + "</span></a>";
  }).join("") + (() => { const more = order.slice(12).map(sl => headerPhoto(sl)).filter(Boolean).slice(0, 4);
    return '<a class="dcard all' + (more.length === 4 ? " hasph" : "") + '" href="#substances" style="--i:12">' + (more.length === 4 ? '<span class="dc-mos">' + more.map(p => photoImg(p, "t", "", true)).join("") + "</span>" : "") +
      '<span class="dc-t"><span class="dc-n">All ' + SUBSTANCES.length + ' drugs</span><span class="dc-a">Search or browse by family</span></span></a>'; })();
  document.querySelectorAll(".do-ic[data-ic], .mi[data-ic]").forEach(el => { el.innerHTML = icon(el.dataset.ic); });
  homeCont();
  mfStart("tf");
}

// the last drug page the reader was on, and how far they got (this device only); the router calls it on every visit home
function homeCont() {
  const cont = document.getElementById("home-cont"), last = lastPage();
  if (cont) {
    if (last) {
      const s = subBySlug[last.s], n = last.ids.filter(wasSeen).length, total = last.ids.length, ph = headerPhoto(last.s), f = fam(s.cls);
      cont.innerHTML = '<a class="cont f-' + f.k + '" href="#s-' + last.s + '">' + (ph ? '<span class="cont-ph">' + photoImg(ph, "t", "", true) + "</span>" : '<span class="cont-ic">' + icon(f.icon) + "</span>") +
        '<span class="cont-t"><span class="cont-k">Pick up where you left off</span><span class="cont-n">' + esc(s.name.replace(/ \(.*\)$/, "")) + '</span><span class="cont-s">' +
        (n ? "You have opened " + n + " of " + total + " answers" : total + " answers to explore") + "</span>" + (n ? '<span class="rp-bar" aria-hidden="true"><i style="width:' + Math.round(100 * n / total) + '%"></i></span>' : "") + "</span>" + icon("arrow") + "</a>";
      cont.hidden = false;
    } else cont.hidden = true;
  }
}
/* ---------- Menu: everything else, one tap away ---------- */
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("#menubtn"), menu = document.getElementById("menu"); if (!menu) return;
  if (b) { const open = menu.hidden; menu.hidden = !open; b.setAttribute("aria-expanded", String(open)); if (open) { const a = menu.querySelector("a"); if (a) a.focus(); } return; }
  if (!menu.hidden && (e.target.closest("#menu a") || !e.target.closest("#menu"))) { menu.hidden = true; const mb = document.getElementById("menubtn"); if (mb) mb.setAttribute("aria-expanded", "false"); }
});
document.addEventListener("keydown", e => { if (e.key !== "Escape") return; const menu = document.getElementById("menu"); if (menu && !menu.hidden) { menu.hidden = true; const mb = document.getElementById("menubtn"); mb.setAttribute("aria-expanded", "false"); mb.focus(); } });
// on the home page the search box sits under the question; everywhere else it is in the top bar
function placeSearch(view) {
  const sw = document.getElementById("searchwrap"), slot = document.getElementById("home-search"), bar = document.getElementById("bar-search");
  if (!sw || !slot || !bar) return;
  const want = view === "home" ? slot : bar; if (sw.parentElement !== want) want.appendChild(sw);
  document.body.classList.toggle("on-home", view === "home");
}

/* ---------- One answer and all its evidence, over the page (senior author, 26 October: "All the evidence for this
   answer" took him to another drug's research page, full of tables, and he could not find where he was). The sheet
   opens over the page the reader is on; the Back button, Escape, a tap outside or the phone's own Back button close it
   and leave the reader exactly where they were. The full research page stays one link away for anyone who wants it. ---------- */
const EV = { id: null, open: false, opener: null, pushed: false };
// the question an answer has on the page the reader is on, or anywhere on the site
function anyQuestion(id) {
  const order = (renderedDrug ? [renderedDrug] : []).concat(Object.keys(QUESTIONS));
  for (const slug of order) for (const g of QUESTIONS[slug] || []) for (const [cid, q] of g.items) if (cid === id) return q;
  return null;
}
const ROLE_WORDS = { supports: "Supports the answer", qualifies: "Adds a limit or a detail", contradicts: "Points the other way" };
// an in-text citation that opens the source itself (no hover box inside the sheet)
// "Paid for by a company that sells alcohol", "An author has ties to ...": plain words for a flagged funder
function fundWords(f) {
  if (f.label) return f.label;  // the editor's plain sentence (data/site/funding-flags.json)
  const kind = f.kind === "industry" ? "a company with a stake in the result" : "a group that campaigns on drugs";
  if (f.what === "an author declared ties") return "An author declared ties to " + (f.who || kind);
  return (f.what === "paid for part of the study" ? "Partly paid for by " : "Paid for by ") + (f.who || kind) + (f.who ? " (" + kind + ")" : "");
}
const citeLink = (id, page) => { const r = refById[id]; if (!r) return ""; return '<a href="' + esc(refLink(r)) + '" target="_blank" rel="noopener">' + esc(inTextLabel(r, REFS)) + (page ? ", " + esc(page) : "") + "</a>"; };
// a study named in the sheet's text opens that study's place in the list of sources, with what it says for this answer
// (senior author, 31 October: "I should be able to find the evidence of its respective finding in the most user friendly way")
const evSrcLink = (id, text) => '<a class="evcite" href="#ev-src-' + esc(id) + '" data-src="' + esc(id) + '">' + text + "</a>";
let LABEL_REF = null;   // every reference by its escaped in-text label, built once
function sheetCites(text, refs) {
  if (!LABEL_REF) LABEL_REF = new Map(REFS.map(r => [esc(inTextLabel(r, REFS)), r]));
  let h = esc(text); const keep = [];
  const hold = html => { keep.push(html); return "\u0000" + (keep.length - 1) + "\u0000"; };
  const mine = refs.map(r => [r, esc(inTextLabel(refById[r], REFS))]).sort((a, b) => b[1].length - a[1].length);
  // narrative citations first: Morgan et al. (2009), Curran & Morgan (2000)
  for (const [r, lab] of mine) {
    const cut = lab.lastIndexOf(", "), narr = lab.slice(0, cut) + " (" + lab.slice(cut + 2) + ")";
    if (h.includes(narr)) h = h.split(narr).join(hold(evSrcLink(r, narr)));
  }
  // parenthetical citations, alone or with notes after them: (Grant et al., 2015; funded by ...; Hasin et al., 2007)
  const starts = (t, L) => t === L || t.startsWith(L + ",") || t.startsWith(L + " ") || t.startsWith(L + ":");
  h = h.replace(/\(([^()\u0000]{1,900})\)/g, (m, inner) => {
    if (!/\d{4}/.test(inner)) return m;
    return "(" + inner.split(";").map(part => {
      const lead = part.match(/^\s*/)[0], t = part.slice(lead.length);
      for (const [r, L] of mine) if (starts(t, L)) return lead + hold(evSrcLink(r, L)) + t.slice(L.length);
      const m2 = t.match(/^[^,]+(?:, [^,]+)*?, \d{4}[a-z]?/); const other = m2 && LABEL_REF.get(m2[0]);
      if (other) return lead + hold('<a class="pop" href="' + esc(refLink(other)) + '" target="_blank" rel="noopener" data-ref="' + esc(other.id) + '">' + m2[0] + "</a>") + t.slice(m2[0].length);
      // a source of this answer named later in the part: (McCrae et al., 2020, as cited by Halifax et al., 2024)
      let t2 = t, hit = false;
      for (const [r, L] of mine) { const i = t2.indexOf(L), after = t2.charAt(i + L.length);
        if (i > 0 && t2.charAt(i - 1) === " " && (after === "" || ",.: ".includes(after))) { t2 = t2.slice(0, i) + hold(evSrcLink(r, L)) + t2.slice(i + L.length); hit = true; } }
      return hit ? lead + t2 : part;
    }).join(";") + ")";
  });
  return h.replace(/\u0000(\d+)\u0000/g, (m, i) => keep[+i]);
}
// small labels after a "How we know" point, naming the studies it rests on (data/site/simple.json, how_src)
// "Gillespie 2021": the first author and the year, for a label that fits beside a sentence (the APA form is one tap away)
function shortLabel(ref) { const a = ref.author[0] || {}; return (a.short || a.literal || a.family || "") + " " + year(ref); }
function howSrcHtml(sp, i, inSheet, claimId) {
  const ids = ((sp.how_src || [])[i] || []).filter(r => refById[r]); if (!ids.length) return "";
  return '<span class="howsrc">' + ids.map(r => { const lab = inTextLabel(refById[r], REFS);
    return inSheet ? evSrcLink(r, esc(lab)) : '<a class="evcite" href="#' + esc(claimId) + '" data-focus-src="' + esc(r) + '" title="' + esc(lab) + '" aria-label="Source: ' + esc(lab) + '">' + esc(shortLabel(refById[r])) + "</a>"; }).join("") + "</span>";
}
function evHtml(id) {
  const c = claimById[id]; if (!c) return "";
  const sp = (SIMPLE.claims || {})[id], q = anyQuestion(id);
  const refs = [...new Set(c.evidence.map(e => e.reference))].filter(r => refById[r]).sort((a, b) => apaAuthors(refById[a].author).localeCompare(apaAuthors(refById[b].author)) || byYear(refById[a], refById[b]));
  const cardFor = r => { const e = c.evidence.find(x => x.reference === r && x.study_card && cardById[x.study_card]); return e ? e.study_card : null; };
  const said = e => (e.extracted && !e.extracted.startsWith("[")) || e.quote;
  const anchors = c.evidence.filter(said);
  // one list of sources: each opens to what it says for this answer, where, and how the study was done
  const studies = refs.map(r => {
    const ref = refById[r], sc = cardFor(r), mine = c.evidence.filter(e => e.reference === r && said(e)), link = refLink(ref);
    const lab = inTextLabel(ref, REFS), title = String(ref.title || "").replace(/<[^>]+>/g, "");
    // the flag is keyed by the card id the anchors name, so it shows even before that card's file has loaded
    const scId = (c.evidence.find(x => x.reference === r && x.study_card) || {}).study_card;
    const ff = scId && typeof FUNDING_FLAGS !== "undefined" ? FUNDING_FLAGS[scId] : null;
    // a funder with a stake shows on the closed row, so it is seen without opening the source (senior author, 12 November)
    const fundLine = ff ? '<span class="ev-src-fund">' + icon("alert") + "<span>" + esc(fundWords(ff)) + "</span></span>" : "";
    return '<li class="ev-src" id="ev-src-' + esc(r) + '"><details><summary><span class="ev-src-who">' + esc(lab) + '</span><span class="ev-src-t">' + esc(title) + '</span>' + fundLine + '<span class="ev-src-n">' +
      (mine.length ? mine.length + (mine.length === 1 ? " finding used here" : " findings used here") : "Cited here") + "</span></summary>" +
      '<div class="ev-src-b">' + (mine.length ? '<ul class="ev-quotes">' + mine.map(e => '<li><span class="ev-role ' + esc(e.role) + '">' + esc(ROLE_WORDS[e.role] || e.role) + "</span>" +
        (e.extracted && !e.extracted.startsWith("[") ? "<span>" + esc(e.extracted) + "</span>" : "") + (e.quote ? "<q>" + esc(e.quote) + "</q>" : "") +
        '<span class="ev-loc">' + esc([e.page, e.locator].filter(Boolean).join(", ")) + "</span></li>").join("") + "</ul>" : "") +
      '<p class="ev-apa">' + apaReference(ref) + "</p>" +
      '<p class="ev-src-acts">' + (/^https?:/.test(link) ? '<a href="' + esc(link) + '" target="_blank" rel="noopener">Open the paper ' + icon("arrow") + "</a>" : "") +
      (sc ? '<button type="button" class="ev-card" data-card="' + esc(sc) + '">How this study was done, and its limits</button>' : "") + "</p></div></details></li>";
  }).join("");
  const cites = t => sheetCites(t, refs);
  const peco = '<dl class="ev-peco"><dt>Who was studied</dt><dd>' + inPieces(c.population, cites) + "</dd><dt>What they took or did</dt><dd>" + inPieces(c.exposure, cites) + "</dd><dt>Compared with</dt><dd>" + inPieces(c.comparator, cites) +
    "</dd><dt>What was measured</dt><dd>" + inPieces(c.outcome, cites) + "</dd><dt>How big</dt><dd>" + inPieces(c.magnitude, cites) + "</dd></dl>";
  const home = c.substance === "interactions" ? '<a href="#interactions">Mixing drugs: every answer we have</a>' : c.substance === DC ? '<a href="#checking/kits">Test kits: every answer we have</a>' : subBySlug[c.substance] ? '<a href="#s-' + c.substance + '/evidence">All the research on ' + esc(subBySlug[c.substance].name) + "</a>" : "";
  return '<div class="ev-bar"><button type="button" class="ev-back">' + icon("arrow") + '<span>Back</span></button><span class="ev-eye">The evidence</span></div>' +
    '<h2 id="ev-title">' + esc(q || c.plain || c.statement) + "</h2>" +
    (sp ? '<p class="ask-short">' + esc(sp.short) + "</p>" + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + freqHtml(sp.freq) + helpLine(sp) : '<p class="ask-short">' + esc(c.plain || c.statement) + "</p>") +
    '<div class="ev-cert"><p class="ev-k">How sure the research is</p>' + meterHtml(c.grade.certainty) + whyRating(c, sp, refs) + "</div>" +
    (sp && sp.how && sp.how.length ? '<h3 class="ev-h">How we know</h3><ul class="ev-how">' + sp.how.map((t, i) => "<li>" + esc(t) + howSrcHtml(sp, i, true, id) + "</li>").join("") + "</ul>" : "") +
    evDebateHtml(c, refs) +
    '<h3 class="ev-h">' + (refs.length === 1 ? "The source" : "The " + refs.length + " sources") + '</h3><p class="ev-sub small muted">Tap a source to see what it says for this answer, and where.</p><ul class="ev-refs">' + studies + "</ul>" +
    // the researchers' text, one quiet tap away and in short pieces (senior author, 13 November: "too overwhelming, nobody will read it")
    '<details class="sf-more sf-sci"><summary>Scientific detail</summary><div class="ev-precise">' + inPieces(c.statement, cites) + "</div>" + peco + "</details>" +
    currencyHtml(c) +
    '<p class="ev-stamp">' + esc(readerStamp(c.verification.status, c)) + " · version " + esc(c.version) + " · " + anchors.length + (anchors.length === 1 ? " finding" : " findings") + " from " + refs.length + (refs.length === 1 ? " source" : " sources") + "</p>" +
    '<p class="ev-foot"><button type="button" class="linklike" data-fb="issue" data-where="' + esc(id) + '">Report a mistake in this answer</button>' + (home ? "<span>" + home + "</span>" : "") + "</p>";
}
// "Why this rating": the plain explanation first, in a sentence or two (senior author, 12 November: the GRADE reasoning read
// "like a robot" and was "not easy to digest"); the editors' full reasoning stays one tap further down, for researchers
function whyRating(c, sp, refs) {
  const full = inPieces(c.grade.reasoning, t => sheetCites(t, refs)) + '<p class="small muted">GRADE: ' + esc(gradeDomains(c.grade)) + "</p>";
  if (!sp || !sp.rate) return '<details class="sf-more ev-why"><summary>Why this rating</summary>' + full + "</details>";
  return '<details class="sf-more ev-why"><summary>Why this rating</summary><p class="ev-rate">' + esc(sp.rate) + '</p>' +
    '<details class="sf-more ev-why-full"><summary>The full reasoning, for researchers</summary>' + full + "</details></details>";
}
// a contested answer's debate box (METHODS §7) inside its evidence: the question, then both sides, what neither side can show,
// the editors' reading and what would settle it, each one tap away (the texts are long); citations open their source below
function evDebateHtml(c, refs) {
  const d = c.debate; if (!d) return "";
  const part = (t, h, cls) => t ? '<details class="sf-more evd-part' + (cls ? " " + cls : "") + '"><summary>' + h + "</summary>" + inPieces(t, x => sheetCites(x, refs)) + "</details>" : "";
  return '<section class="ev-debate" id="ev-debate" aria-labelledby="ev-debate-h"><h3 class="ev-h" id="ev-debate-h">Researchers disagree</h3><p class="evd-q">' + esc(d.question) + "</p>" +
    part(d.evidence_yes, "The strongest evidence for yes", "yes") + part(d.evidence_no, "The strongest evidence for no", "no") +
    part(d.neither_can_show, "What neither side’s evidence can show") + part(d.editors_reading, "Our reading", "reading") + part(d.what_would_settle_it, "What would settle it") + "</section>";
}
// a line under a contested answer that opens its evidence at the debate
function debateLine(c) {
  return c.debate ? '<p class="ask-debate">Researchers disagree about this. <a href="#' + esc(c.id) + '" data-focus-src="debate">Read both sides</a></p>' : "";
}
// open one source in the sheet: its place in the list, opened, briefly marked (or the debate box, for "debate")
function focusEvSource(ref) {
  if (ref === "debate") { const box = document.getElementById("ev-debate"); if (box) { scrollToEl(box); const s = box.querySelector("summary"); if (s) s.focus({ preventScroll: true }); } return; }
  const li = document.getElementById("ev-src-" + ref); if (!li) return;
  const d = li.querySelector("details"); if (d) d.open = true;
  li.classList.remove("hit"); void li.offsetWidth; li.classList.add("hit");
  scrollToEl(li);
  const sm = li.querySelector("summary"); if (sm) sm.focus({ preventScroll: true });
}
function openEvidence(id, opener, focusRef) {
  if (!claimById[id]) return false;
  const sh = document.getElementById("evsheet"), panel = sh && sh.querySelector(".panel"); if (!panel) return false;
  // the sheet reads the answer's full text and the references in full (speed, 13 November): the first time, it opens at once
  // with its Back button, the question and a quiet line, and fills in when they arrive
  const fill = () => {
    panel.innerHTML = evHtml(id); panel.scrollTop = 0;
    panel.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
    const b = panel.querySelector(".ev-back"); if (b) b.focus({ preventScroll: true });
    if (focusRef) setTimeout(() => focusEvSource(focusRef), 60);
  };
  const ready = fullReady([id]);
  if (!ready) { panel.innerHTML = '<div class="ev-bar"><button type="button" class="ev-back">' + icon("arrow") + '<span>Back</span></button><span class="ev-eye">The evidence</span></div>' +
    '<h2 id="ev-title">' + esc(anyQuestion(id) || claimText(claimById[id])) + '</h2><div class="ev-wait"></div>'; panel.scrollTop = 0; }
  if (!EV.open) {
    EV.opener = opener || document.activeElement;
    // the phone's Back button closes the sheet instead of leaving the page
    try { history.pushState({ pkEvidence: id }, ""); EV.pushed = true; } catch (e) { EV.pushed = false; }
  }
  EV.id = id; EV.open = true; sh.classList.add("open"); document.documentElement.classList.add("sheet-open");
  hidePop(); closeSearch();
  if (ready) fill();
  else { const b = panel.querySelector(".ev-back"); if (b) b.focus({ preventScroll: true });
    whenReady(() => needFull([id]), panel.querySelector(".ev-wait"), "The evidence", () => { if (EV.open && EV.id === id) fill(); }); }
  return true;
}
function closeEvidence(fromHistory) {
  if (!EV.open) return;
  EV.open = false; document.getElementById("evsheet").classList.remove("open"); document.documentElement.classList.remove("sheet-open");
  const back = EV.pushed && !fromHistory; EV.pushed = false;
  if (back) history.back();
  if (EV.opener && EV.opener.focus && document.contains(EV.opener)) EV.opener.focus({ preventScroll: true });
}
window.addEventListener("popstate", () => { if (EV.open) closeEvidence(true); });
document.addEventListener("click", e => {
  if (!e.target.closest) return;
  if (e.target.closest("#evsheet .ev-back") || e.target.closest("#evsheet > .scrim")) { e.preventDefault(); closeEvidence(); return; }
  // any link to an answer's evidence opens it over the page; the research page keeps its own links, and a link can still
  // be opened in a new tab
  const ec = e.target.closest("a.evcite[data-src]");
  if (ec && ec.closest("#evsheet")) { e.preventDefault(); focusEvSource(ec.dataset.src); return; }
  const a = e.target.closest('a[href^="#cl_"]');
  if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.classList.contains("perma") || a.closest("#view-monograph #full")) return;
  const id = a.getAttribute("href").slice(1); if (!claimById[id]) return;
  e.preventDefault(); openEvidence(id, a, a.dataset.focusSrc || null);
});
// the keyboard stays inside the open sheet
document.addEventListener("keydown", e => {
  if (e.key !== "Tab" || !EV.open || document.getElementById("drawer").classList.contains("open") || document.getElementById("report").classList.contains("open")) return;
  const f = [...document.querySelectorAll("#evsheet .panel button, #evsheet .panel a[href], #evsheet .panel summary")].filter(x => x.offsetParent !== null);
  if (!f.length) return; const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

/* ---------- What the Myth or fact? decks share (from the quiz before them: senior author, 26 October and 6 November). Kept on
   this device: the statements a reader has answered, so that new ones come first, and those missed, which come back early
   until answered right. Kept for the visit, in this tab: the answers already asked, so that no deck on any page asks one
   again until every statement has been dealt. One format everywhere (senior author, 14 November: Myth or fact "is more
   interesting"): the written multiple-choice questions (data/site/simple.json, quiz) are kept but no longer shown. ---------- */
const QZ_KEY = "pk-quiz-seen";
function qzSeen() { try { return new Set(JSON.parse(localStorage.getItem(QZ_KEY) || "[]")); } catch (e) { return new Set(); } }
function qzMark(key) { const s = qzSeen(); s.delete(key); s.add(key); try { localStorage.setItem(QZ_KEY, JSON.stringify([...s].slice(-800))); } catch (e) { /* this visit only */ } }
const QZ_AGAIN = "pk-quiz-again";
function qzAgain() { try { return new Set(JSON.parse(localStorage.getItem(QZ_AGAIN) || "[]")); } catch (e) { return new Set(); } }
function qzAgainSet(key, on) { const s = qzAgain(); if (on) s.add(key); else s.delete(key); try { localStorage.setItem(QZ_AGAIN, JSON.stringify([...s].slice(-200))); } catch (e) { /* this visit only */ } }
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
const qzOk = id => !!(claimById[id] && (SIMPLE.claims || {})[id] && claimById[id].verification.status !== "draft");
const drugName = slug => ((subBySlug[slug] || {}).name || slug).replace(/\s*\(.*\)$/, "");
// no two cards from the same page in a row, where the pool allows it
function qzSpread(xs, k) { k = k || "kind"; const left = xs.slice(), out = []; while (left.length) { const last = out.length ? out[out.length - 1][k] : null; let i = left.findIndex(x => x[k] !== last); if (i < 0) i = 0; out.push(left.splice(i, 1)[0]); } return out; }
const QZ_SESSION = "pk-quiz-session";
function qzLoad() { try { const x = JSON.parse(sessionStorage.getItem(QZ_SESSION) || "null"); if (x && Array.isArray(x.claims)) return x; } catch (e) { /* not kept */ } return { right: 0, done: 0, claims: [] }; }
let QZS = qzLoad();
function qzSave() { try { sessionStorage.setItem(QZ_SESSION, JSON.stringify(QZS)); } catch (e) { /* this page only */ } }
// a statement's own reason that already says what the answer's 'But' says: the 'But' is not repeated
function qzSame(why, but) { if (!why) return false; const w = t => new Set(norm(t).replace(/[^\p{L}\p{N}\s]/gu, " ").split(/\s+/).filter(x => x.length > 3)), A = w(why), B = w(but); let n = 0; A.forEach(x => { if (B.has(x)) n++; }); return A.size > 0 && n / A.size >= 0.5; }

/* ---------- Myth or fact? (redesign 2, 13 November; the senior author: the site "has so much info it is like the user gets
   tested in school", and a visitor would use it a little and leave). The first thing under the search box on the home page:
   a deck of 10 cards from the checked true-or-false statements (data/site/simple.json tf: only the ones the quiz may ask, so
   written for the claim's current version), in a new order on every visit, short statements (20 words or fewer) first,
   and among them the ones on what people ask about most (DEMAND, highest first), about as many myths as facts, one card
   per answer. Tap Myth or Fact and the card turns over where it is: the verdict, the statement, its why line, the answer's
   "But" (the reveal always carries it, as in the quiz, unless the why line already says it), the evidence bars and the way
   to the answer on its page. Then Next; after ten, Another 10. A plain count, no score,
   no streak, no timer. The same deck is the whole Myth or fact? page (endless: Another 10 never runs out, every statement
   comes round again in a new order) and the end of each drug page and of the facts page, there with that page's statements
   only (a page with fewer than 3 has none). A statement answered in one deck counts as asked in every other for the rest of
   the visit, and as seen on this device (senior author, 14 November: one format everywhere). ---------- */
const MF = {};
let MF_POOL = null;
function mfPool() {
  if (MF_POOL) return MF_POOL;
  const out = [];
  Object.entries(SIMPLE.tf || {}).forEach(([slug, list]) => list.forEach(x => { if (!qzOk(x.claim)) return;
    out.push({ key: "tf:" + x.claim + ":" + norm(x.statement).slice(0, 40), claim: x.claim, page: answerPageKey(x.claim, slug), q: x.statement, fact: !!x.answer, why: x.why || "", long: x.statement.split(/\s+/).length > 20 }); }));
  return (MF_POOL = out);
}
// n new cards: none asked this visit or dealt in this deck before; short ones first, and of each length those never answered
// on this device first, then those missed last time, then the rest; within each of these, the statements whose answers people
// ask about most first (DEMAND, highest first; equals, and the statements without a score after them, in a new order every
// time); a full deck takes about as many myths as facts
function mfDeal(st, n) {
  const asked = new Set(QZS.claims), seen = qzSeen(), again = qzAgain();
  let pool = st.pool.filter(x => !asked.has(x.claim) && !st.used.has(x.claim));
  if (!pool.length && n > 1) { st.used = new Set(); pool = st.pool; }   // every statement has been dealt: all of them again, in a new order
  const tier = x => (x.long ? 3 : 0) + (!seen.has(x.key) ? 0 : again.has(x.key) ? 1 : 2), one = new Set();
  const order = [0, 1, 2, 3, 4, 5].flatMap(t => shuffle(pool.filter(x => tier(x) === t)).sort((a, b) => demandOf(b.claim) - demandOf(a.claim))).filter(x => !one.has(x.claim) && one.add(x.claim));
  let deck = n > 1 ? order.filter(x => !x.fact).slice(0, n / 2).concat(order.filter(x => x.fact).slice(0, n / 2)) : order.slice(0, n);
  deck = deck.concat(order.filter(x => !deck.includes(x)).slice(0, n - deck.length));
  deck = qzSpread(shuffle(deck), "page");
  deck.forEach(x => st.used.add(x.claim));
  return deck;
}
// the statements of one page (a drug page: its own answers, the mixing answers and the test-kit answers it shows; the facts
// page: the general answers), each leading to the answer on that page where it is there; or (no page) every statement
function mfPagePool(page) {
  if (!page) return mfPool();
  const on = new Set(page === GEN ? drugQuestions(GEN).map(x => x[0]) : drugQuestions(page).map(x => x[0]).concat(mixQuestions(page).map(x => x[0]), KITSBY[page] || []));
  return mfPool().filter(x => on.has(x.claim)).map(x => Object.assign({}, x, { page: answerPageKey(x.claim, page) }));
}
const mfCount = pool => new Set(pool.map(x => x.claim)).size;
// a deck of 10 (fewer where a page has fewer statements); page: only that page's statements
function mfStart(boxId, page) {
  if (!document.getElementById(boxId)) return;
  const pool = mfPagePool(page), st = MF[boxId] = { pool, n: Math.min(10, mfCount(pool)), used: new Set(), cards: [], picks: [], pos: 0 };
  st.cards = mfDeal(st, st.n); mfRender(boxId);
}
// the card's "But" is left out when the why line already says it: as the quiz judges it, or when most of the shorter line's
// words are in the other (the deck is meant to be light; the full answer always carries the "But")
function mfSame(why, but) {
  if (qzSame(why, but)) return true;
  const w = t => new Set(norm(t).replace(/[^\p{L}\p{N}\s]/gu, " ").split(/\s+/).filter(x => x.length > 3)), A = w(why), B = w(but);
  let n = 0; A.forEach(x => { if (B.has(x)) n++; });
  return Math.min(A.size, B.size) > 0 && n / Math.min(A.size, B.size) >= 0.6;
}
// the page a card is about: its family's colour and icon, and its name
function mfWhere(page) {
  const s = subBySlug[page]; if (s) return { f: fam(s.cls), name: drugName(page) };
  return { f: { k: "oth", icon: page === GEN ? "book" : page === DC ? "flask" : page === "interactions" ? "mix" : "molecule" }, name: PAGE_TITLES[page === GEN ? "facts" : page === DC ? "checking" : "interactions"] || "" };
}
function mfCardHtml(boxId, st) {
  const x = st.cards[st.pos], p = st.picks[st.pos], c = claimById[x.claim], sp = SIMPLE.claims[x.claim], w = mfWhere(x.page), left = st.cards.length - 1 - st.pos;
  const top = '<div class="qz2-top"><span class="qz2-k">' + icon(w.f.icon) + "<span>" + esc(w.name) + '</span></span><span class="qz2-score">' + (st.pos + 1) + " of " + st.cards.length + "</span></div>";
  const opt = (v, t) => '<button type="button" class="qz2-o" data-v="' + v + '"' + (p ? " disabled" : "") + ">" + t + "</button>";
  // the card already answered (going back to it) shows turned, without turning again
  return '<div class="mf-card f-' + w.f.k + (p ? " flipped" : "") + (left > 1 ? " l2" : left ? " l1" : "") + '"><div class="mf-in">' +
    '<div class="mf-face mf-front">' + top + '<p class="qz2-q mf-q" id="' + boxId + '-q" tabindex="-1">' + esc(x.q) + "</p>" +
      '<div class="qz2-opts mf-opts" role="group" aria-labelledby="' + boxId + '-q">' + opt("myth", "Myth") + opt("fact", "Fact") + "</div></div>" +
    '<div class="mf-face mf-back ' + (x.fact ? "fact" : "myth") + '">' + top +
      '<p class="mf-v" tabindex="-1">' + icon(x.fact ? "check" : "x") + "<b>" + (x.fact ? "Fact" : "Myth") + '</b> <span class="mf-fb">' + (p ? (p.ok ? "Right!" : "Not quite.") : "") + "</span></p>" +
      '<p class="mf-said">“' + esc(x.q) + "”</p>" + '<p class="qz2-why">' + esc(x.why || sp.short) + "</p>" + (sp.but && !mfSame(x.why, sp.but) ? '<p class="qz2-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") +
      '<div class="qz2-row">' + meterHtml(c.grade.certainty, true) + '<a class="qz2-ev" href="' + esc(answerAddr(x.claim, x.page)) + '">Read the answer ' + icon("arrow") + "</a></div></div></div></div>";
}
const mfNavHtml = st => '<div class="mf-nav">' + (st.pos > 0 ? '<button type="button" class="qz2-prev">' + icon("arrow") + "<span>Previous</span></button>" : "") +
  (st.picks[st.pos] ? '<button type="button" class="qz2-nb">' + (st.pos < st.cards.length - 1 ? "Next" : st.n === 10 ? "Another 10" : "Again, in a new order") + "</button>" : "") + "</div>";
function mfRender(boxId) {
  const st = MF[boxId], box = document.getElementById(boxId); if (!st || !box) return;
  // a card dealt earlier whose answer has since been asked in the quiz gives way to a fresh one
  if (!st.picks[st.pos] && st.cards[st.pos] && QZS.claims.includes(st.cards[st.pos].claim)) { const y = mfDeal(st, 1)[0]; if (y) st.cards[st.pos] = y; }
  box.hidden = !st.cards.length; if (!st.cards.length) return;
  box.innerHTML = mfCardHtml(boxId, st) + mfNavHtml(st);
}
// back on the home page after the quiz: the card waiting to be answered may have been asked there meanwhile
function mfRefresh(boxId) { const st = MF[boxId]; if (st && !st.picks[st.pos] && st.cards[st.pos] && QZS.claims.includes(st.cards[st.pos].claim)) mfRender(boxId); }
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest(".mf .qz2-o, .mf .qz2-nb, .mf .qz2-prev"); if (!b) return;
  const box = b.closest(".mf"), st = MF[box.id]; if (!st) return;
  if (b.classList.contains("qz2-o")) {
    if (b.disabled || st.picks[st.pos]) return;
    const x = st.cards[st.pos], ok = (b.dataset.v === "fact") === x.fact;
    st.picks[st.pos] = { ok };
    if (!QZS.claims.includes(x.claim)) { QZS.claims.push(x.claim); qzSave(); }
    qzMark(x.key); qzAgainSet(x.key, !ok);
    const card = box.querySelector(".mf-card"), back = card.querySelector(".mf-back");
    card.querySelectorAll(".mf-front .qz2-o").forEach(o => { o.disabled = true; });
    back.querySelector(".mf-fb").textContent = ok ? "Right!" : "Not quite.";
    box.querySelector(".mf-nav").outerHTML = mfNavHtml(st);
    // the card turns away, shows its other side and turns back; with less motion, the sides simply swap
    let done = false;
    const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const turn = () => { if (done || !card.isConnected) return; done = true; card.classList.remove("out"); card.classList.add("flipped", "in"); back.querySelector(".mf-v").focus({ preventScroll: true });
      // the other side is longer: bring Next into view, clear of the feedback button
      const nav = box.querySelector(".mf-nav"), over = nav ? nav.getBoundingClientRect().bottom - (window.innerHeight - 76) : 0;
      if (over > 0) window.scrollBy({ top: over, behavior: reduce ? "auto" : "smooth" }); };
    if (reduce) turn();
    else { card.classList.add("out"); card.addEventListener("animationend", turn, { once: true }); setTimeout(turn, 400); }
    return;
  }
  if (b.classList.contains("qz2-prev")) st.pos = Math.max(0, st.pos - 1);
  else if (st.pos < st.cards.length - 1) st.pos++;
  else { st.cards = mfDeal(st, st.n); st.picks = []; st.pos = 0; }   // Another 10
  mfRender(box.id);
  const f = box.querySelector(st.picks[st.pos] ? ".mf-v" : ".mf-q"); if (f) f.focus({ preventScroll: true });
  if (box.getBoundingClientRect().top < updateSticky(box)) scrollToEl(box, true);
});

// the floating feedback button steps aside while the reader scrolls down (it covered the text), and comes back
// when they scroll up, stop near the top, or reach the end of the page
(function () {
  let lastY = window.scrollY, busy = false;
  window.addEventListener("scroll", () => {
    if (busy) return; busy = true;
    requestAnimationFrame(() => {
      const y = window.scrollY, roomy = !!(window.matchMedia && window.matchMedia("(min-width: 1500px)").matches);  // only where it sits beside the text
      const atEnd = window.innerHeight + y >= document.documentElement.scrollHeight - 60;
      if (roomy || y < 120 || atEnd || y < lastY - 6) document.body.classList.remove("fab-away");
      else if (y > lastY + 6) document.body.classList.add("fab-away");
      lastY = y; busy = false;
    });
  }, { passive: true });
})();

/* ---------- Answer-first search (senior author, 26 October: questions answered from the site's own content, like an AI
   would, but with no paid service). Everything runs on the device. Each question on the site and its short answer are
   searched with everyday words (weed is cannabis; "with", "and" or "together" mean mixing; "hooked" means dependence),
   small spelling slips are forgiven, and two drugs in one search go straight to what is known about mixing them. A result
   shows the answer itself and how sure the research is, and opens on its drug page. ---------- */
const SR_STOP = new Set("a an the is are was were be been being do does did doing can could will would should shall may might must i im me my mine we our you your yours it its it's of to in on at by for from about into over what whats which who whom whose why when where there here this that these those if or so than then get gets got getting take takes taking taken use uses using used have has had having any some much many very really just also please tell know want go goes going ok okay how".split(" "));
// everyday names the drug pages answer to, besides each drug's own names
const SR_NAMES = [["sleeping pills", "benzodiazepines"], ["sleeping pill", "benzodiazepines"], ["sleeping tablets", "benzodiazepines"], ["benzo", "benzodiazepines"], ["shrooms", "psilocybin"], ["mushrooms", "psilocybin"], ["magic mushrooms", "psilocybin"], ["laughing gas", "nitrous-oxide"], ["nos", "nitrous-oxide"], ["oxycodone", "prescription-opioids"], ["painkillers", "prescription-opioids"]];
// what people come to do, besides asking a question: test a drug, check the law, help someone, read about doses
const SR_INTENT = [
  ["test", ["test", "tests", "testing", "kit", "kits", "reagent", "strip", "strips", "drug check", "drug checking", "pill test", "pill testing"]],
  ["law", ["legal", "illegal", "law", "laws", "prison", "jail", "arrest", "arrested", "possession", "decriminal", "allowed"]],
  ["help", ["too much", "unwell", "bad trip", "freaking out", "freak out", "panic attack", "passed out", "pass out", "not waking", "wont wake", "won't wake", "what to do", "help someone", "help a friend", "greening out", "whitey", "too high", "overdosing"]],
  ["dose", ["dose", "doses", "dosage", "dosing", "how much should", "mg"]]
];
// everyday words and the words the answers use, as groups that match each other (the start of a word is enough)
const SR_SYN = [
  ["sleep", "insomnia", "asleep", "bedtime", "dream"], ["mix", "combin", "together", "crossfad", "cross-fad"], ["pregnan", "baby", "babies", "unborn", "fetus", "foetus", "birth"],
  ["addict", "dependen", "hooked", "habit", "use disorder"], ["withdraw", "stopping", "quit", "detox", "cold turkey", "coming off", "come off", "cutting down", "cut down"],
  ["overdos", "too much", "poison"], ["death", "die", "dying", "dead", "kill", "fatal", "lethal"], ["brain", "neuro", "nerve", "serotonin", "dopamine"],
  ["memory", "memories", "forget", "remember", "thinking", "cognit", "concentrat", "attention"], ["heart", "cardi", "chest", "blood pressure", "pulse"],
  ["driv", "car", "crash", "road"], ["hangover", "hungover", "morning after", "next day", "day after"], ["comedown", "come down", "crash", "low mood", "midweek"],
  ["anxi", "panic", "paranoi", "worr", "nervous"], ["depress", "sad", "low mood"], ["psychos", "psychotic", "schizophren", "hallucinat"],
  ["hot", "heat", "overheat", "temperature", "sweat"], ["water", "sodium", "salt", "hyponatr"], ["long", "last", "duration", "hours", "stay in"],
  ["test", "kit", "reagent", "strip", "drug check"], ["legal", "illegal", "law", "prison", "jail", "possession", "arrest"],
  ["therap", "treat", "medicine", "medical", "ptsd", "trial"], ["feel", "high", "effect", "experience"], ["safe", "danger", "risk", "harm", "bad for"],
  ["eye", "vision", "sight"], ["sick", "vomit", "nausea", "throw up", "hyperemesis"], ["teeth", "tooth", "dental", "jaw"], ["lung", "breath", "cough", "smok", "vap"],
  ["sex", "libido", "erect"], ["weight", "appetite", "hunger", "eat", "food"], ["kidney", "liver"], ["child", "kid", "teen", "young"]
];
const SR_MIX = ["mix", "mixing", "mixed", "combine", "combined", "combining", "combination", "together", "crossfade", "crossfading", "cross-fade"];
let SR_DRUGS = [], SR_VOCAB = new Set();
// the answers, one per question on the site: on which drug pages each is, and the words to search
function buildAnswerIndex() {
  const pages = {}, items = {};
  SUBSTANCES.forEach(s => drugQuestions(s.slug).concat(mixQuestions(s.slug)).forEach(([id, q, topic]) => {
    if (!(SIMPLE.claims || {})[id]) return;
    (pages[id] = pages[id] || []); if (!pages[id].includes(s.slug)) pages[id].push(s.slug);
    if (!items[id]) items[id] = { id, q, topic };
  }));
  (QUESTIONS.interactions || []).forEach(g => g.items.forEach(([id, q]) => { if (claimById[id] && (SIMPLE.claims || {})[id] && !items[id]) items[id] = { id, q, topic: g.topic }; }));
  // the answers on test kits live on the drug checking page; they are about the drugs whose tests they cover
  (QUESTIONS[DC] || []).forEach(g => g.items.forEach(([id, q]) => { if (claimById[id] && (SIMPLE.claims || {})[id] && !items[id]) items[id] = { id, q, topic: g.topic, dc: true }; }));
  (QUESTIONS[GEN] || []).forEach(g => g.items.forEach(([id, q]) => { if (claimById[id] && (SIMPLE.claims || {})[id] && !items[id]) items[id] = { id, q, topic: g.topic, gen: true }; }));
  Object.values(items).forEach(x => {
    const sp = SIMPLE.claims[x.id], about = [...new Set((pages[x.id] || []).concat(MIXFOR[x.id] || [], KITSFOR[x.id] || []))];
    const where = x.gen ? "Facts about drug use" : x.dc ? "Drug checking" : (MIXFOR[x.id] || []).length ? "Mixing" : about.length === 1 && subBySlug[about[0]] ? drugName(about[0]) : about.length > 1 ? "Several drugs" : "Mixing";
    const it = { type: "answer", id: x.id, title: x.q, where, pages: pages[x.id] || [], about, mix: !!(MIXFOR[x.id] || []).length || topicZone(x.topic || "") === "mix",
      tq: norm(x.q), ts: norm(sp.short), tt: norm(x.topic || ""), tx: norm([sp.but].concat(sp.how || []).join(" ")) };
    INDEX.push(it);
    (it.tq + " " + it.ts + " " + it.tt).split(/[^a-z0-9α-ω-]+/).forEach(w => { if (w.length >= 4) SR_VOCAB.add(w); });
  });
  // the names that point to a drug inside a question: its name, the editors' list of common names, and street names two
  // sources agree on; a spelling slip is forgiven only in a drug's own names (not "strips" for "trips")
  const seen = new Set();
  SUBSTANCES.forEach(s => {
    const main = [s.name, s.name.replace(/\s*\(.*\)$/, "")].concat(ALIASES[s.slug] || [], (s.name.match(/\(([^)]+)\)/) || ["", ""])[1].split(/,\s*/)).map(norm);
    const names = main.concat((ALIASES_EL[s.slug] || []).map(norm), documentedNames(s.slug).map(norm), SR_NAMES.filter(([, sl]) => sl === s.slug).map(([n]) => n));
    names.filter(n => n && n.length >= 2 && !/\d{3}/.test(n)).forEach(n => { const k = n + "|" + s.slug; if (!seen.has(k)) { seen.add(k); SR_DRUGS.push([n, s.slug, main.includes(n)]); } });
  });
  SR_DRUGS.sort((a, b) => b[0].length - a[0].length);
  return new Set(Object.keys(items));
}
const srWordEnd = (hay, i, len) => i + len >= hay.length || /[\s(\-\/,.;:'"?!«»]/.test(hay[i + len]);
// which drugs a search names, and what it asks about them
function readQuery(q) {
  let rest = " " + q + " "; const groups = [];
  const intents = SR_INTENT.filter(([, ws]) => ws.some(w => { const i = rest.indexOf(" " + w); return i >= 0 && srWordEnd(rest, i + 1, w.length); })).map(([k]) => k);
  const taken = new Set();
  for (const [n] of SR_DRUGS) {
    if (taken.has(n)) continue;
    let i = rest.indexOf(n);
    while (i > 0) { if (/[\s(\-\/,.;:'"«»]/.test(rest[i - 1]) && srWordEnd(rest, i, n.length)) break; i = rest.indexOf(n, i + 1); }
    if (i > 0) { taken.add(n); groups.push(SR_DRUGS.filter(([m]) => m === n).map(([, sl]) => sl)); rest = rest.slice(0, i) + " ".repeat(n.length) + rest.slice(i + n.length); }
  }
  const words = rest.split(/[\s,.;:?!]+/).filter(Boolean);
  // a slip in a drug's own name ("cannabs"), five letters or more
  words.slice().forEach(w => { if (w.length < 5 || SR_STOP.has(w) || SR_VOCAB.has(w)) return;
    const hit = SR_DRUGS.find(([n, , own]) => own && !n.includes(" ") && n.length >= 5 && Math.abs(n.length - w.length) <= 1 && editDistance(w, n) <= 1);
    if (hit) { groups.push([hit[1]]); words.splice(words.indexOf(w), 1); } });
  const drugs = [...new Set(groups.flat())], mixWord = words.some(w => SR_MIX.includes(w));
  const topic = words.filter(w => !SR_STOP.has(w) && !SR_MIX.includes(w) && !["and", "with", "plus", "or", "vs", "versus"].includes(w) && w.length >= 2).map(w => {
    // a slip in an everyday word: the closest word the answers use
    if (w.length < 5 || SR_VOCAB.has(w) || [...SR_VOCAB].some(v => v.startsWith(w))) return w;
    let best = null, bd = 9; SR_VOCAB.forEach(v => { if (Math.abs(v.length - w.length) <= 2) { const d = editDistance(w, v); if (d < bd) { bd = d; best = v; } } });
    return best && bd <= (w.length >= 8 ? 2 : 1) ? best : w;
  });
  const expand = w => { const out = new Set([w]); SR_SYN.forEach(g => { if (g.some(m => w.startsWith(m) || (m.startsWith(w) && w.length >= 4))) g.forEach(m => out.add(m)); }); return [...out]; };
  // the words that named a drug, as typed ("xylazine", "benzo"): an answer whose question uses the same word is the closer one
  return { drugs, groups, names: [...taken], mix: groups.length > 1 || mixWord, topic, forms: topic.map(expand), intents };
}
function scoreAnswer(it, ctx) {
  if (!ctx.drugs.length && !ctx.topic.length && !ctx.mix) return 0;
  // a drug named in the search: only answers about it; two drugs: answers about mixing them come first
  const hits = ctx.groups.filter(g => g.some(d => it.about.includes(d))).length;
  if (ctx.groups.length && !hits) return 0;
  let sc = hits * 90 + (ctx.mix && it.mix ? (ctx.groups.length > 1 && hits > 1 ? 160 : 60) : 0);
  // ties: an answer about this drug alone, whose question names it
  if (hits) sc += (it.about.length === 1 ? 8 : 0) + (ctx.drugs.some(d => it.tq.includes(norm(drugName(d)))) ? 10 : 0);
  const named = (ctx.names || []).some(n => wordStart(it.tq, n));
  if (named && it.where === "Drug checking") sc += 12;  // the test answers name their tests (xylazine, nitazene, fentanyl strips)
  // an answer on test kits is about the drugs whose tests it covers, but it answers only a search about testing
  if (it.where === "Drug checking" && !ctx.intents.includes("test") && !named && !ctx.topic.some(w => /^(test|kit|strip|reagent|check|marquis|mecke|colou?r|accura|reliab|false|nitazen|xylazin)/.test(w))) return 0;
  // "do strips work?", "are they accurate?": for a test, working means showing what is there
  if (it.where === "Drug checking" && ctx.topic.some(w => /^(work|accura|reliab)/.test(w)) && /\b(show|find|pick up|detect)/.test(it.tq)) sc += 36;
  let matched = 0;
  ctx.forms.forEach((forms, i) => {
    let best = 0;
    forms.forEach(f => { const own = f === ctx.topic[i];
      if (wordStart(it.tq, f)) best = Math.max(best, own ? 48 : 36); else if (wordStart(it.tt, f)) best = Math.max(best, own ? 26 : 20);
      else if (wordStart(it.ts, f)) best = Math.max(best, own ? 22 : 16); else if (wordStart(it.tx, f)) best = Math.max(best, 6); });
    if (best >= 16) matched++; sc += best;  // a word only in the fine print adds a little, but does not count as found
  });
  // most of what was asked has to be there
  if (ctx.topic.length && matched < Math.ceil(ctx.topic.length / 2)) return 0;
  if (!ctx.topic.length && !ctx.mix) sc = Math.min(sc, 80);  // a drug's name alone: its page first, then its answers
  if (!ctx.groups.length && sc < 30) return 0;  // a single passing word is not an answer
  return sc;
}
// an answer opens on the drug page the search was about, at its question; mixing answers not on a drug page open over the page
function answerHref(it, ctx) {
  if (it.where === "Drug checking") return "#checking/q-" + it.id;
  if (it.where === "Facts about drug use") return "#facts/q-" + it.id;
  const slug = ctx.drugs.find(d => it.pages.includes(d)) || it.pages[0];
  return slug ? "#s-" + slug + "/q-" + it.id : "#" + it.id;
}

// a search that is about doing something gets the place where it is done, first
function intentHits(ctx) {
  const d = ctx.drugs.length === 1 ? ctx.drugs[0] : null, nm = d ? drugName(d) : "", out = [];
  const add = (title, kind, href) => out.push({ sc: 3000, fz: false, it: { type: "intent", kind, title, href } });
  ctx.intents.forEach(k => {
    if (k === "test") { if (d && !NO_TEST.includes(d)) add("Test kits: which kit, and where to get one", "Test kits · " + nm, "#s-" + d + "/part-d-kits"); add("Drug checking near you", "Drug checking", "#checking");
      if (drugQuestions(DC).length) add("Do home test kits work? What studies found", "Drug checking", "#checking/kits"); }
    if (k === "law") add(d ? "Is " + pageWord(d) + " legal where I am?" : "The law, country by country", d ? "The law · " + nm : "The law", d ? "#s-" + d + "/part-d-law" : "#law");
    if (k === "help") { if (d && helpSigns(d)) add(helpTitle(d), "What to do · " + nm, "#s-" + d + "/part-d-help"); add("Emergency numbers, country by country", "Get help", "#emergency"); }
    if (k === "dose" && d && dosesBody(d)) add("Doses: where to read about them", "Doses · " + nm, "#s-" + d + "/part-d-doses");
  });
  const seen = new Set(); return out.filter(x => !seen.has(x.it.href) && seen.add(x.it.href));
}
