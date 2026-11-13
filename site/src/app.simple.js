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
/* One question and its answer. Tap the question; the short answer and its catch come first; "How do we know?" holds the rest. */
function ansHtml(id, q, pre, next) {
  const c = claimById[id]; if (!c) return "";
  const sp = (SIMPLE.claims || {})[id];
  if (!sp) return '<details class="ask" id="' + (pre || "ask-") + id + '"><summary><span class="ask-q">' + esc(q) + '</span><span class="ask-i" aria-hidden="true"></span></summary><div class="ask-a">' + REWRITING(id) + "</div></details>";
  return '<details class="ask' + (wasSeen(id) ? " seen" : "") + '" id="' + (pre || "ask-") + id + '" data-cid="' + id + '"><summary><span class="ask-q">' + esc(q) + "</span>" + '<span class="ask-seen" title="You have read this">' + icon("check") + "</span>" + meterDots(c.grade.certainty) + '<span class="ask-i" aria-hidden="true"></span></summary><div class="ask-a">' +
    answerBody(id, c, sp) + (next ? '<button type="button" class="ask-next" data-next="' + esc((pre || "ask-") + next[0]) + '"><span>Next question</span><span class="ask-nq">' + esc(next[1]) + "</span>" + icon("arrow") + "</button>" : "") + "</div></details>";
}
/* One answer, in the order a reader needs it (senior author, 1 November: "so many words that I get lost"): the short answer,
   its catch and the picture first; how sure the research is and the evidence in one line; "How do we know?" one tap away,
   with compact source labels; the sources themselves, the full references and "Report an issue" live in the evidence. */
function answerBody(id, c, sp) {
  const flags = [c.verification.status === "draft" ? '<span class="flag early">' + icon("alert") + "Early draft: " + esc(draftWhy(c)) + "</span>" : "",
    c.debate ? '<a class="flag debate" href="#' + esc(id) + '" data-focus-src="debate">' + icon("scale") + "Researchers disagree: read both sides</a>" : ""].filter(Boolean).join("");
  return '<p class="ask-short">' + cueNum(esc(sp.short)) + "</p>" + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + freqHtml(sp.freq) +
    (flags ? '<p class="ask-flags">' + flags + "</p>" : "") +
    (sp.how && sp.how.length ? '<details class="ask-how"><summary>How do we know?</summary><ul class="ask-howl">' + sp.how.map((t, i) => "<li>" + esc(t) + howSrcHtml(sp, i, false, id) + "</li>").join("") + "</ul></details>" : "") +
    '<div class="ask-foot">' + meterHtml(c.grade.certainty, true) + '<span class="ask-acts"><button type="button" class="ask-share" data-share="' + esc(id) + '" aria-label="Share this answer">' + icon("share") + '<span class="ask-share-t">Share</span></button><a class="ask-ev" href="#' + id + '">The evidence ' + icon("arrow") + "</a></span></div>" + helpLine(sp);
}
// answers a reader has opened, remembered on this device only, so a long list shows where they have been (no tracking)
let SEEN_SET = null;
function seenSet() { if (SEEN_SET) return SEEN_SET; try { SEEN_SET = new Set(JSON.parse(localStorage.getItem("pk-read") || "[]")); } catch (e) { SEEN_SET = new Set(); } return SEEN_SET; }
function wasSeen(id) { return seenSet().has(id); }
function markSeen(id) { const r = seenSet(); if (r.has(id)) return; r.add(id); try { localStorage.setItem("pk-read", JSON.stringify([...r].slice(-800))); } catch (e) {} }
document.addEventListener("toggle", e => { const d = e.target; if (!d.matches || !d.matches("details.ask[open]") || !d.dataset.cid) return; markSeen(d.dataset.cid); d.classList.add("seen"); if (d.closest("#drug2")) pageProgress(); }, true);
/* How many of a drug page's answers the reader has opened (WRITING-RULES, "small rewards for exploring"): a bar and a count,
   kept on this device only. The page is also remembered, so the home page can offer to pick up where the reader left off. */
function pageAskIds() { return [...new Set([...document.querySelectorAll("#drug2 details.ask[data-cid]")].map(d => d.dataset.cid))]; }
function pageProgress() {
  const el = document.getElementById("pgprog"); if (!el) return;
  const ids = pageAskIds(), total = ids.length, n = ids.filter(wasSeen).length;
  if (total < 4) { el.hidden = true; return; }
  el.hidden = false;
  el.innerHTML = '<div class="rp-bar" aria-hidden="true"><i style="width:' + Math.round(100 * n / total) + '%"></i></div><p class="rp-t">' +
    (n ? "You have opened <b>" + n + "</b> of " + total + " answers on this page" + (n === total ? ". All of them!" : ".") : "<b>" + total + "</b> answers on this page. Tap a question to open it.") + "</p>";
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
// "Next question": closes this answer and opens the next one in the same list, revealing it if it was folded away
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("button.ask-next"); if (!b) return;
  const cur = b.closest("details.ask"), nx = document.getElementById(b.dataset.next); if (!nx) return;
  const more = nx.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const mb = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (mb) mb.remove(); }
  if (cur) cur.open = false; nx.open = true;
  scrollToEl(nx, true); const sm = nx.querySelector("summary"); if (sm) sm.focus({ preventScroll: true });
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
function openAnswer(id) {
  const c = claimById[id], sp = (SIMPLE.claims || {})[id]; if (!c) return "";
  if (!sp) return '<div class="open-a" id="ask-' + id + '">' + REWRITING(id) + "</div>";
  return '<div class="open-a" id="ask-' + id + '">' + answerBody(id, c, sp) + "</div>";
}
// a short list with the rest one tap away (about four things at a time)
function askList(items, key, first, pre) {
  const n = first || 4, shown = items.slice(0, n), rest = items.slice(n);
  const nx = i => items[i + 1] || null;
  return '<div class="asks">' + shown.map(([id, q], i) => ansHtml(id, q, pre, nx(i))).join("") +
    (rest.length ? '<div class="asks-more" id="more-' + key + '" hidden>' + rest.map(([id, q], i) => ansHtml(id, q, pre, nx(n + i))).join("") + '</div><button type="button" class="morebtn" data-more="more-' + key + '">' + rest.length + " more question" + (rest.length === 1 ? "" : "s") + "</button>" : "") + "</div>";
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
    const law = page.querySelector("#d-law .sec-b"); if (law) law.innerHTML = lawHtml(renderedDrug);
    const h = page.querySelector("#d-help .sec-b"); if (h) h.innerHTML = helpHtml();
    const top = page.querySelector(".dh-help"); if (top) top.outerHTML = helpTopLine(renderedDrug);
    const t = page.querySelector("#sf-test .sf-b"); if (t) t.innerHTML = testHtml();
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
  return countryAsk() + '<p class="say">' + esc(lawPlain(slug, PREF_COUNTRY)) + '</p><details class="lawmore"><summary>What the law says, with its sources</summary><div class="lawmore-b">' +
    countryOut(slug, PREF_COUNTRY) + '<p class="small"><a href="#law">Treaties, country by country</a></p></div></details>';
}
/* Sourced lines for Staying safer (data/site/stay-safer.json): official and non-profit pages, each line checked by a
   second AI reader before it is shown; what home tests can show, where kits can be had, and first aid by drug family */
const SAFE = (typeof STAY_SAFER !== "undefined" && STAY_SAFER) || { tests: {}, signs: {} };
const NO_SIGNS = ["nicotine", "caffeine"];
const OPEN_AID = ["Opioids", "Depressants"];  // drugs that can stop breathing: first aid shows open
const lineList = ls => '<ul class="sf-list">' + ls.map(l => "<li>" + esc(l.line) + "</li>").join("") + "</ul>";
function srcFold(lines) {
  const seen = new Map();
  lines.forEach(l => (l.anchors || []).forEach(x => { const k = x.ref ? "ref:" + x.ref : x.url; if (k && !seen.has(k) && (!x.ref || refById[x.ref])) seen.set(k, x); }));
  if (!seen.size) return "";
  // papers by author and year, with the full APA reference on the citation; web pages one line per publisher
  // (senior author, 26 October: a list of 40 sources was too long to look through)
  const all = [...seen.values()], byPub = new Map();
  all.filter(x => !x.ref).forEach(x => { const k = x.publisher || "Other pages"; if (!byPub.has(k)) byPub.set(k, []); byPub.get(k).push(x); });
  const items = all.filter(x => x.ref).map(x => "<li>" + cite(x.ref) + " " + esc(refById[x.ref].title) + "</li>")
    .concat([...byPub].map(([pub, xs]) => "<li><b>" + esc(pub) + "</b>: " + xs.map(x => '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.title) + "</a>").join("; ") + "</li>"));
  return '<details class="sf-src"><summary>Sources (' + all.length + ")</summary><ul>" + items.join("") +
    "</ul>" + (SAFE.checked_note ? '<p class="small muted">' + esc(SAFE.checked_note) + "</p>" : "") + "</details>";
}
/* If it gets too much (senior author, 26 October: the first-aid box must be calm and welcoming to a stressed person or
   carer, and fit the drug: no CPR line first on a cannabis page). Same sourced lines, in a kinder order: what helps
   first, then when to get help, and first aid one tap away. Where breathing can stop (opioids, alcohol, benzodiazepines,
   GHB), getting help and first aid stay first. Each line's place is its "kind" in data/site/stay-safer.json. */
const helpSigns = slug => { const s = subBySlug[slug]; return s && !NO_SIGNS.includes(slug) ? (SAFE.signs || {})[s.cls] || null : null; };
function helpTitle(slug) {
  const cls = (subBySlug[slug] || {}).cls;
  if (slug === "alcohol") return "If someone has drunk too much";
  return { Cannabinoids: "If it gets too much", "Classic psychedelics": "If a trip gets difficult", "Atypical psychedelics": "If a trip gets difficult",
    Opioids: "If someone has taken too much", Depressants: "If someone has taken too much" }[cls] || "If someone feels unwell";
}
// the emergency number where the reader is (checked against an official source), or the way to find it
function callLine() {
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  if (!em) return '<p class="hp-call">' + icon("phone") + '<span>Call your local emergency number. <a href="#emergency">Numbers by country</a></span></p>';
  return '<p class="hp-call"><a class="callbtn sm" href="tel:' + esc(telOf(em.numbers[0])) + '">' + icon("phone") + "<span>Call <b>" + esc(em.numbers[0].n) + "</b></span></a>" +
    '<span class="small muted">The emergency number in ' + esc(inCtry(PREF_COUNTRY)) + " " + srcIcons(em.numbers[0].src) + ' · <a href="#emergency">other numbers</a></span></p>';
}
function helpHtml(slug) {
  slug = slug || renderedDrug;
  const s = subBySlug[slug], fam = helpSigns(slug);
  if (!fam) return callLine();
  const kind = x => x.kind || "calm", ww = fam.while_waiting || [], dn = fam.do_not || [], cn = fam.call_now || [];
  const helpOnes = ww.concat(dn).filter(x => kind(x) === "help");
  const now = '<div class="hp-now"><p class="sf-k">Get help now if</p>' + lineList(cn) + callLine() + (helpOnes.length ? lineList(helpOnes) : "") + "</div>";
  let h;
  if (OPEN_AID.includes(s.cls)) h = now + (ww.length ? '<p class="sf-k">While you wait</p>' + lineList(ww) : "") + (dn.length ? '<p class="sf-k">Don’t</p>' + lineList(dn) : "");
  else {
    const calm = ww.filter(x => kind(x) === "calm"), avoid = dn.filter(x => kind(x) === "calm"), aid = ww.concat(dn).filter(x => kind(x) === "aid");
    h = (calm.length ? '<p class="sf-k">What helps</p>' + lineList(calm) : "") + (avoid.length ? '<p class="sf-k">What not to do</p>' + lineList(avoid) : "") + now +
      (aid.length ? '<details class="sf-more"><summary>First aid while you wait for help</summary>' + lineList(aid) + "</details>" : "");
  }
  return h + srcFold(cn.concat(ww, dn));
}
// one quiet line under the drug's name, in place of the box that was on every page (senior author, 26 October)
function helpTopLine(slug) {
  const em = PREF_COUNTRY ? emFor(PREF_COUNTRY) : null;
  return '<p class="dh-help">' + icon("phone") + "<span>Someone unwell? " + (helpSigns(slug) ? '<a href="#d-help" data-go="d-help">What to do</a> · ' : "") +
    (em ? 'Emergency: <a href="tel:' + esc(telOf(em.numbers[0])) + '">' + esc(em.numbers[0].n) + "</a>" : '<a href="#emergency">Emergency numbers</a>') + "</span></p>";
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
// one block for one country: on a drug's "Test it first" card and on the drug checking page
function kitsWhere(un) {
  const nm = esc(inCtry(un)), law = KW.law.filter(x => x.country === un), free = KW.free.filter(x => x.country === un), post = KW.post.filter(x => x.country === un);
  const sellers = KW.sellers.filter(x => shipsTo(x, un)).sort((a, b) => (b.based_in === un) - (a.based_in === un) || (b.kind === "harm reduction non-profit") - (a.kind === "harm reduction non-profit") || a.name.localeCompare(b.name));
  const used = law.concat(free, post, sellers.flatMap(x => [{ anchors: (x.anchors || []).concat(x.pointers || []) }].concat(x.warning ? [x.warning] : [])));
  const where = x => x.region && !String(x.line).includes(x.region) ? " (" + esc(x.region) + ")" : "";
  const li = x => "<li>" + esc(x.line) + where(x) + "</li>";
  // what people want first is where to get a kit (senior author, 26 October): free tests, then sellers, then testing by
  // post; what the law says about kits is one tap away
  let h = "";
  if (free.length) h += '<p class="sf-k2">Free tests</p><ul class="sf-list">' + free.map(x => "<li>" + esc(x.line) + where(x) + "</li>").join("") + "</ul>";
  if (sellers.length) {
    h += '<p class="kw-lead">Sellers that say they send to ' + nm + ':</p><ul class="kw-sellers">' + sellers.map(x => '<li><a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.name) + "</a> <span class=\"muted\">" + esc(x.sells_line) + (x.based_in === un ? ", in " + nm : x.based_in_short ? ", " + esc(x.based_in_short) : "") + "</span></li>").join("") + "</ul>" +
      '<p class="small muted">Harm reduction groups or health services point people to these sellers. We have not tested their kits.' + (sellers.some(x => x.warning) ? " Some say they do not refund parcels that customs hold or refuse." : "") + "</p>";
  } else h += '<p class="say small">We have not found a seller that says it sends test kits to ' + nm + ".</p>";
  if (post.length) h += '<p class="sf-k2">Testing by post</p><ul class="sf-list">' + post.map(x => "<li>" + esc(x.line) + "</li>").join("") + "</ul>";
  h += law.length ? '<details class="sf-more"><summary>Test kits and the law in ' + nm + '</summary><ul class="sf-list">' + law.map(li).join("") + "</ul></details>"
    : '<p class="say small">We have not found what the law in ' + nm + " says about test kits.</p>";
  return { html: h, used };
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
    groups.map(([t, it], i) => '<h3 class="qh">' + esc(t) + "</h3>" + askList(it, "dck-" + i, 4)).join("");
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
      askList(qs.filter(([, , tt]) => tt === t), "facts" + i, 4, "fx-") + "</div></section>").join("") +
    '<section class="sec quizsec" aria-labelledby="facts-quiz-h"><h2 id="facts-quiz-h">Test yourself</h2><div class="qz2" id="qz-facts"></div></section>';
  qzStart("qz-facts", GEN);
}
function openFact(id) {
  const d = document.getElementById("fx-" + id); if (!d) return false;
  const more = d.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
  d.open = true; setTimeout(() => scrollToEl(d), 30); return true;
}
// the menu item and the home card appear once the page has answers
function factsLinks() { const on = drugQuestions(GEN).length > 0; document.querySelectorAll("[data-facts]").forEach(el => { el.hidden = !on; }); }
function renderDcKits() { const box = document.getElementById("dc-kits"); if (!box) return; const h = dcKitsHtml(); box.innerHTML = h; box.hidden = !h; }
function testHtml(slug) {
  slug = slug || renderedDrug;
  const T = SAFE.tests || {}, own = (T.drugs || {})[slug] || [], none = (T.none_found || []).includes(slug), common = T.common || [];
  const more = (T.more || {})[slug] || [], unproven = (T.none_validated || []).includes(slug);
  // senior author, 26 October: lead with what people want (which test, and where to get one); the general points and
  // the sources come after, one tap away
  let h = "", used = [], folds = "";
  const key = common[2] ? [common[2]] : [], rest = common.filter((x, i) => i !== 2);
  const kits = !unproven && own.length;  // a kit is worth buying only where a home test works for this drug
  if (own.length) {
    // tests are named, but none has been shown to work for this drug: said first, so nobody takes a colour for proof
    h += '<p class="sf-k">' + (unproven ? "No home test has been shown to work for " + esc(pageWord(slug)) : "Home tests") + "</p>" + lineList(unproven ? own : own.slice(0, 3));
    if (!unproven && key.length) h += '<p class="sf-key">' + icon("alert") + "<span>" + esc(key[0].line) + "</span></p>";
    const extra = (unproven ? [] : own.slice(3)).concat(more);
    if (extra.length) folds += '<details class="sf-more"><summary>More about these tests</summary>' + lineList(extra) + "</details>";
    if (rest.length) folds += '<details class="sf-more"><summary>What home tests can’t tell you</summary>' + lineList(rest) + "</details>";
    used = own.concat(more, common);
  } else if (none) {
    h += '<p class="say small">We have not found a home test for ' + esc(pageWord(slug)) + ".</p>" + (common[3] ? lineList([common[3]]) : "");
    if (more.length) folds += '<details class="sf-more"><summary>More about these tests</summary>' + lineList(more) + "</details>";
    used = (common[3] ? [common[3]] : []).concat(more);
  }
  if (kits) {
    if (PREF_COUNTRY) { const kw = kitsWhere(PREF_COUNTRY); h += '<p class="sf-k">Where to get a kit in ' + esc(inCtry(PREF_COUNTRY)) + "</p>" + kw.html; used = used.concat(kw.used); }
    else h += '<p class="sf-k">Where to get a kit</p>' + countryAsk();
  }
  // what studies found about these tests (senior author, 26 October: are home test kits useful?), after where to get one
  if (own.length || none) h += kitAnswersHtml(slug);
  // a lab check tells you more than any home test: the services where the reader is
  let dc = '<p><a class="go" href="#checking">Drug checking by country</a></p>';
  if (PREF_COUNTRY) {
    const sv = dcFor(PREF_COUNTRY), nm = esc(inCtry(PREF_COUNTRY));
    dc = sv.length ? '<p class="sf-k">Drug checking in ' + nm + '</p><p class="say small">' + sv.length + " service" + (sv.length === 1 ? "" : "s") + ' that test a sample for you. <a href="#checking">See where</a></p>'
      : '<p class="say small">We have not found a drug checking service in ' + nm + ' yet. <a href="#checking">Drug checking by country</a></p>';
  }
  return h + dc + folds + srcFold(used);
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
  const card = document.getElementById("sf-dose");
  if (card) { card.querySelector(".sf-b").innerHTML = dosesBody(renderedDrug); return; }
  // a drug with no links yet gets the card as soon as the author's text or the owner's button exists
  const safer = document.querySelector("#d-safer .safer"); const body = dosesBody(renderedDrug);
  if (safer && body) { const sos = document.getElementById("sf-sos"); const div = document.createElement("div"); div.className = "sf"; div.id = "sf-dose"; div.innerHTML = "<h3>" + icon("book") + "<span>Doses</span></h3><div class=\"sf-b\">" + body + "</div>"; safer.insertBefore(div, sos); }
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
function saferHtml(slug) {
  const card = (id, ic, h, body) => '<div class="sf" id="' + id + '"><h3>' + icon(ic) + "<span>" + esc(h) + '</span></h3><div class="sf-b">' + body + "</div></div>";
  const doses = dosesBody(slug);
  // drug checking is for drugs bought on the street or online, not for drinks, coffee, cigarettes or gas canisters
  const test = !NO_TEST.includes(slug);
  // the same test-kit photo and the emergency box were on every drug page (senior author, 26 October): the photo is gone,
  // and what to do if someone is unwell has its own calm part further down, with one quiet line to it under the name
  if (!test && !doses) return "";
  return '<div class="safer">' + (test ? card("sf-test", "flask", "Test it first", testHtml(slug)) : "") + (doses ? card("sf-dose", "book", "Doses", doses) : "") + "</div>";
}

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
function kitsBox(un) { const kw = kitsWhere(un); return '<section class="kw-box"><h2 class="qh">Test kits in ' + esc(inCtry(un)) + "</h2>" + kw.html + srcFold(kw.used) + "</section>"; }
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

/* The page itself */
const SEC_ICON = { "d-safer": "check", "d-feel": "pulse", "d-mix": "mix", "d-after": "moon", "d-risk": "alert", "d-med": "plus", "d-looks": "eye", "d-law": "scale", "d-help": "heart" };
let renderedDrug = null;
function renderDrug(slug) {
  const s = subBySlug[slug], m = monographFor(slug); if (!s || !m) return;
  renderedDrug = slug; currentSlug = slug;
  const f = fam(s.cls), fp = famPlain(s.cls), ph = headerPhoto(slug), names = documentedNames(slug).slice(0, 3);
  const qs = drugQuestions(slug);
  const feel = qs.filter(([, , t]) => topicZone(t) === "feel"), risk = roundRobin(qs.filter(([, , t]) => topicZone(t) === "risk")), med = qs.filter(([, , t]) => topicZone(t) === "med"), mix = mixQuestions(slug), after = qs.filter(([, , t]) => topicZone(t) === "after");
  const nForms = (FORMS[slug] || []).length;
  const sec = (id, q, body, chip) => ({ id, q, body, chip });
  const secs = [];
  // 1. staying safer comes first (senior author, 23 October: "users have to gain practical knowledge first of all"):
  // which test and where to get one, and doses; what to do if someone is unwell has its own part below
  const safer = saferHtml(slug);
  if (safer) secs.push(sec("d-safer", "Staying safer", safer, "Stay safer"));
  // 2. what it looks like, right after staying safer: photos first, and looks do not tell you what is inside
  if (nForms) secs.push(sec("d-looks", "What does it look like?", formsHtml(slug), "Looks"));
  // 3. what it feels like: the drug's own checked answers, or what drugs of its family generally do
  const ownLine = (FAMPLAIN.drugs || {})[slug] || null, famLine = fp && !(FAMPLAIN.skip || []).includes(slug);
  secs.push(sec("d-feel", "What does it feel like?", feel.length === 1 ? openAnswer(feel[0][0]) : feel.length ? askList(feel, "feel", 2) :
    (famLine ? '<p class="say">' + esc(ownLine ? ownLine.line : fp.line) + '</p><p class="small muted">' + (ownLine ? "In general terms. " : "What drugs like " + esc(pageWord(slug)) + " generally do, not " + esc(pageWord(slug)) + " itself. ") +
      '<a href="' + esc(FAMPLAIN.source.url) + '" target="_blank" rel="noopener">Source: ' + esc(FAMPLAIN.source.publisher) + "</a></p>" : '<p class="say">Not written yet.</p>'), "Feels"));
  // 3. mixing, before the other risks: most drug deaths involve more than one drug
  secs.push(sec("d-mix", "Is it safe to mix?", (mix.length ? askList(mix, "mix", 3) : '<p class="say">We have not checked answers about mixing ' + esc(pageWord(slug)) + " yet.</p>") + '<p><a class="go" href="#interactions">Mixing drugs: every answer we have</a></p>', "Mixing"));
  // 4. the day after: after-effects as studies describe them, and whether what people do about them works (decision p-day-after)
  if (after.length) {
    const has = re => after.some(([, , t]) => re.test(t)), bef = has(/^before/i), day = has(/day after/i), stop = has(/after stopping/i);
    // before and during use first, then the day after, then the weeks after stopping (decision p-before-during-after)
    const ordered = [/^before/i, /day after/i, /after stopping/i].flatMap(re => after.filter(([, , t]) => re.test(t)));
    const title = bef ? (day || stop ? "Before, during and after" : "Before and during") : stop ? (day ? "The day after, and after stopping" : "After stopping") : "The day after";
    secs.push(sec("d-after", title, askList(ordered, "after", 3), bef ? "Before & after" : day ? "Day after" : "After stopping"));
  }
  // 5. what else can go wrong
  if (risk.length) secs.push(sec("d-risk", "What can go wrong?", askList(risk, "risk", 4), "Risks"));
  // 6. if it gets too much: calm help first, when to get help, first aid one tap away
  if (helpSigns(slug)) secs.push(sec("d-help", helpTitle(slug), helpHtml(slug), "If unwell"));
  // 5. as a medicine
  // the drug as a medicine, or treatment in hospital or clinic (for example after a long PCP psychosis): the heading names which
  const medAs = med.some(([, , t]) => /as a medicine/i.test(t)), medTx = med.some(([, , t]) => /treatment/i.test(t) && !/as a medicine/i.test(t));
  if (med.length) secs.push(sec("d-med", medAs ? (medTx ? "As a medicine, and treatment" : "Is it used as a medicine?") : "What can treatment do?", askList(med, "med", 3), medAs ? "Medicine" : "Treatment"));
  // 7. the law where you are
  secs.push(sec("d-law", "Is it legal where I am?", lawHtml(slug), "Law"));
  const nAns = qs.length + mix.filter(([id]) => claimById[id] && claimById[id].substance !== slug).length;
  const nCards = Object.values(STUDY_CARDS).filter(k => k.substance === slug).length;
  // no draft banner (the senior author's decision of 13 November 2026: he holds editorial responsibility for what is published;
  // METHODS §12, 0.3.2); "not medical advice" stays in the footer and on the About page
  const draft = "";
  const h = '<header class="dh f-' + f.k + (ph ? " hasph" : "") + '">' + (ph ? '<figure class="dh-ph">' + photoImg(ph, "m", ph.alt, false) + (nForms > 1 ? '<a class="dh-forms" href="#d-looks">See all ' + nForms + " forms</a>" : "") + "</figure>" : "") +
    '<div class="dh-t"><p class="dh-fam">' + icon(f.icon) + esc(fp ? fp.word.charAt(0).toUpperCase() + fp.word.slice(1) : s.cls) + "</p><h1>" + esc(s.name) + "</h1>" +
    (names.length ? '<p class="dh-aka">Also called ' + names.map(esc).join(", ") + "</p>" : "") + "</div></header>" + draft + helpTopLine(slug) +
    (inShortHtml(qs, feel.length === 1 ? [feel[0][0]] : []) || (qs.length ? '<p class="dh-key">' + meterDots("moderate") + "<span>The bars on each question show how sure the research is. Four bars is the strongest.</span></p>" : "")) +
    '<div class="readprog pgprog" id="pgprog" hidden></div>' +
    '<nav class="chips" aria-label="On this page">' + secs.map(x => '<a href="#' + x.id + '" data-go="' + x.id + '">' + esc(x.chip) + "</a>").join("") +
    // the page's own quiz sits at the end; a chip lets people jump to it (senior author, 12 November: make the site fun to use)
    (qs.length ? '<a href="#d-quiz" data-go="d-quiz">Quiz</a>' : "") + "</nav>" +
    secs.map(x => '<section class="sec" id="' + x.id + '" aria-labelledby="' + x.id + '-h"><h2 id="' + x.id + '-h"><span class="sec-ic">' + icon(SEC_ICON[x.id] || "molecule") + "</span>" + esc(x.q) + '</h2><div class="sec-b">' + x.body + "</div></section>").join("") +
    fbLineHtml() + '<section class="sec deep"><h2>Want the details?</h2><p class="say">' + (nAns ? nAns + (nAns === 1 ? " answer" : " answers") : "The plan for this page") + (nCards ? ", from " + nCards + (nCards === 1 ? " study" : " studies") + " read in full" : "") + ", with every source and how sure we are.</p><p><a class=\"go\" href=\"#s-" + slug + '/evidence">All the research on ' + esc(s.name) + "</a></p></section>" +
    '<section class="sec quizsec" id="d-quiz" aria-labelledby="d-quiz-h"><h2 id="d-quiz-h">Test yourself</h2><div class="qz2" id="qz-drug"></div></section>' +
    familyHtml(m);
  const box = document.getElementById("drug2"); box.className = "wrap drug2 f-" + f.k; box.innerHTML = h;  // the family colour runs through the whole page
  applyPhotoPref(); qzStart("qz-drug", slug); pageProgress();
}
// chips jump to their question without changing the address (so Back still leaves the page)
document.addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("[data-go], a.dh-forms"); if (!a) return;
  const id = a.dataset.go || "d-looks", el = document.getElementById(id); if (!el) return;
  e.preventDefault(); scrollToEl(el, true); const hh = el.querySelector("h2"); if (hh) { hh.setAttribute("tabindex", "-1"); hh.focus({ preventScroll: true }); }
});
function openAsk(id) {
  const d = document.getElementById("ask-" + id); if (!d) return false;
  const more = d.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
  if ("open" in d) d.open = true; setTimeout(() => scrollToEl(d), 30); return true;
}

/* ---------- Mixing: pick a drug, see what we know about mixing it ---------- */
let mixPick = "";
function renderMix2() {
  const box = document.getElementById("mix2"); if (!box) return;
  const all = (QUESTIONS.interactions || []).flatMap(g => g.items).filter(([id]) => claimById[id]);
  const has = new Set(all.flatMap(([id]) => MIXFOR[id] || []));
  const order = POPULAR.concat(SUBSTANCES.map(x => x.slug)).filter((x, i, a) => a.indexOf(x) === i && has.has(x) && subBySlug[x]);
  const items = mixPick ? all.filter(([id]) => (MIXFOR[id] || []).includes(mixPick)) : all;
  box.innerHTML = '<div class="mixchips" role="group" aria-label="Pick a drug"><button type="button" class="mixchip" data-mix="" aria-pressed="' + !mixPick + '">All</button>' +
    order.map(x => '<button type="button" class="mixchip" data-mix="' + x + '" aria-pressed="' + (x === mixPick) + '">' + esc(subBySlug[x].name.replace(/\s*\(.*\)$/, "")) + "</button>").join("") + "</div>" +
    '<p class="mix-n" aria-live="polite">' + items.length + " question" + (items.length === 1 ? "" : "s") + (mixPick ? " about " + esc(pageWord(mixPick)) : "") + "</p>" + askList(items, "mixp", 6, "mx-");
}
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("button.mixchip"); if (!b) return; mixPick = b.dataset.mix; renderMix2(); const nb = document.querySelector('button.mixchip[data-mix="' + mixPick + '"]'); if (nb) nb.focus(); });

/* ---------- Home: one question, three ways to get help, the drugs as pictures ---------- */
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
  qzStart("tf");
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
  const peco = '<dl class="ev-peco"><dt>Who was studied</dt><dd>' + sheetCites(c.population, refs) + "</dd><dt>What they took or did</dt><dd>" + sheetCites(c.exposure, refs) + "</dd><dt>Compared with</dt><dd>" + sheetCites(c.comparator, refs) +
    "</dd><dt>What was measured</dt><dd>" + sheetCites(c.outcome, refs) + "</dd><dt>How big</dt><dd>" + sheetCites(c.magnitude, refs) + "</dd></dl>";
  const home = c.substance === "interactions" ? '<a href="#interactions">Mixing drugs: every answer we have</a>' : c.substance === DC ? '<a href="#checking/kits">Test kits: every answer we have</a>' : subBySlug[c.substance] ? '<a href="#s-' + c.substance + '/evidence">All the research on ' + esc(subBySlug[c.substance].name) + "</a>" : "";
  return '<div class="ev-bar"><button type="button" class="ev-back">' + icon("arrow") + '<span>Back</span></button><span class="ev-eye">The evidence</span></div>' +
    '<h2 id="ev-title">' + esc(q || c.plain || c.statement) + "</h2>" +
    (sp ? '<p class="ask-short">' + esc(sp.short) + "</p>" + (sp.but ? '<p class="ask-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + freqHtml(sp.freq) + helpLine(sp) : '<p class="ask-short">' + esc(c.plain || c.statement) + "</p>") +
    '<div class="ev-cert"><p class="ev-k">How sure the research is</p>' + meterHtml(c.grade.certainty) + whyRating(c, sp, refs) + "</div>" +
    (sp && sp.how && sp.how.length ? '<h3 class="ev-h">How we know</h3><ul class="ev-how">' + sp.how.map((t, i) => "<li>" + esc(t) + howSrcHtml(sp, i, true, id) + "</li>").join("") + "</ul>" : "") +
    evDebateHtml(c, refs) +
    '<h3 class="ev-h">' + (refs.length === 1 ? "The source" : "The " + refs.length + " sources") + '</h3><p class="ev-sub small muted">Tap a source to see what it says for this answer, and where.</p><ul class="ev-refs">' + studies + "</ul>" +
    '<details class="sf-more"><summary>For researchers: the full finding and who was studied</summary><p class="ev-precise">' + sheetCites(c.statement, refs) + "</p>" + peco + "</details>" +
    currencyHtml(c) +
    '<p class="ev-stamp">' + esc(readerStamp(c.verification.status, c)) + " · version " + esc(c.version) + " · " + anchors.length + (anchors.length === 1 ? " finding" : " findings") + " from " + refs.length + (refs.length === 1 ? " source" : " sources") + "</p>" +
    '<p class="ev-foot"><button type="button" class="linklike" data-fb="issue" data-where="' + esc(id) + '">Report an issue with this answer</button>' + (home ? "<span>" + home + "</span>" : "") + "</p>";
}
// "Why this rating": the plain explanation first, in a sentence or two (senior author, 12 November: the GRADE reasoning read
// "like a robot" and was "not easy to digest"); the editors' full reasoning stays one tap further down, for researchers
function whyRating(c, sp, refs) {
  const full = "<p>" + sheetCites(c.grade.reasoning, refs) + '</p><p class="small muted">GRADE: ' + esc(gradeDomains(c.grade)) + "</p>";
  if (!sp || !sp.rate) return '<details class="sf-more ev-why"><summary>Why this rating</summary>' + full + "</details>";
  return '<details class="sf-more ev-why"><summary>Why this rating</summary><p class="ev-rate">' + esc(sp.rate) + '</p>' +
    '<details class="sf-more ev-why-full"><summary>The full reasoning, for researchers</summary>' + full + "</details></details>";
}
// a contested answer's debate box (METHODS §7) inside its evidence: the question, then both sides, what neither side can show,
// the editors' reading and what would settle it, each one tap away (the texts are long); citations open their source below
function evDebateHtml(c, refs) {
  const d = c.debate; if (!d) return "";
  const part = (t, h, cls) => t ? '<details class="sf-more evd-part' + (cls ? " " + cls : "") + '"><summary>' + h + "</summary><p>" + sheetCites(t, refs) + "</p></details>" : "";
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
  if (ref === "debate") { const box = document.getElementById("ev-debate"); if (box) { box.scrollIntoView({ block: "start" }); const s = box.querySelector("summary"); if (s) s.focus({ preventScroll: true }); } return; }
  const li = document.getElementById("ev-src-" + ref); if (!li) return;
  const d = li.querySelector("details"); if (d) d.open = true;
  li.classList.remove("hit"); void li.offsetWidth; li.classList.add("hit");
  li.scrollIntoView({ block: "start", behavior: window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  const sm = li.querySelector("summary"); if (sm) sm.focus({ preventScroll: true });
}
function openEvidence(id, opener, focusRef) {
  if (!claimById[id]) return false;
  const sh = document.getElementById("evsheet"), panel = sh && sh.querySelector(".panel"); if (!panel) return false;
  panel.innerHTML = evHtml(id); panel.scrollTop = 0;
  panel.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
  if (!EV.open) {
    EV.opener = opener || document.activeElement;
    // the phone's Back button closes the sheet instead of leaving the page
    try { history.pushState({ pkEvidence: id }, ""); EV.pushed = true; } catch (e) { EV.pushed = false; }
  }
  EV.id = id; EV.open = true; sh.classList.add("open"); document.documentElement.classList.add("sheet-open");
  hidePop(); closeSearch();
  const b = panel.querySelector(".ev-back"); if (b) b.focus({ preventScroll: true });
  if (focusRef) setTimeout(() => focusEvSource(focusRef), 60);
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

/* ---------- Quiz (senior author, 26 October: the same first question every visit; "completely random", and hundreds of
   questions). A new random order on every visit, with the questions a reader has not answered yet first (kept on this
   device only). Every question is built from checked data, so its answer is right by construction:
   - True or false, and Quick question: written for checked answers (data/site/simple.json, tf and quiz)
   - Which is the answer? a question from a drug page and three short answers, two of them from other topics of that drug
   - Which has stronger evidence? two checked answers whose research is rated differently (GRADE), at most one question in five
   Street names and drug families are no longer asked (senior author, 31 October: "more useful drug fact questions ... rather
   than boring questions like 'which drug is meow meow'"); the names stay on the drug pages and in search. ---------- */
const QZ_KEY = "pk-quiz-seen", QZ = {};
function qzSeen() { try { return new Set(JSON.parse(localStorage.getItem(QZ_KEY) || "[]")); } catch (e) { return new Set(); } }
function qzMark(key) { const s = qzSeen(); s.delete(key); s.add(key); try { localStorage.setItem(QZ_KEY, JSON.stringify([...s].slice(-800))); } catch (e) { /* this visit only */ } }
// questions answered wrongly come back (spaced retrieval: a missed question is asked again a few questions later, and early on
// the next visit, until it is answered right; kept on this device only)
const QZ_AGAIN = "pk-quiz-again";
function qzAgain() { try { return new Set(JSON.parse(localStorage.getItem(QZ_AGAIN) || "[]")); } catch (e) { return new Set(); } }
function qzAgainSet(key, on) { const s = qzAgain(); if (on) s.add(key); else s.delete(key); try { localStorage.setItem(QZ_AGAIN, JSON.stringify([...s].slice(-200))); } catch (e) { /* this visit only */ } }
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
const qzOk = id => !!(claimById[id] && (SIMPLE.claims || {})[id] && claimById[id].verification.status !== "draft");
const CERT_N = { high: 4, moderate: 3, low: 2, "very-low": 1 };
// options in a random order, with the right one tracked
function qzOpts(right, wrong) { const all = shuffle([right].concat(wrong)); return { options: all, answer: all.indexOf(right) }; }
let QZ_POOL = null;
function qzPool() {
  if (QZ_POOL) return QZ_POOL;
  const out = [], tf = SIMPLE.tf || {}, mc = SIMPLE.quiz || {};
  // the questions of each drug page, by topic, and the drug pages each answer is on
  const byDrug = {}, pagesOf = {};
  SUBSTANCES.forEach(s => { byDrug[s.slug] = drugQuestions(s.slug).filter(([id]) => qzOk(id)); byDrug[s.slug].forEach(([id]) => { (pagesOf[id] = pagesOf[id] || []).push(s.slug); }); });
  // the answers on test kits are asked among themselves, and first on the pages of the drugs whose tests they cover
  byDrug[DC] = drugQuestions(DC).filter(([id]) => qzOk(id)); byDrug[DC].forEach(([id]) => { pagesOf[id] = (KITSFOR[id] || []).length ? KITSFOR[id].slice() : [DC]; });
  // the general answers are asked on the facts page first, and everywhere else after the page's own drug
  byDrug[GEN] = drugQuestions(GEN).filter(([id]) => qzOk(id)); byDrug[GEN].forEach(([id]) => { pagesOf[id] = [GEN]; });
  const on = id => pagesOf[id] || [claimById[id].substance];
  Object.values(tf).flat().forEach(x => { if (qzOk(x.claim)) out.push({ key: "tf:" + x.claim + ":" + norm(x.statement).slice(0, 40), kind: "tf", drugs: on(x.claim), claim: x.claim, q: x.statement, why: x.why || "", options: ["True", "False"], answer: x.answer ? 0 : 1 }); });
  Object.values(mc).flat().forEach(x => { if (qzOk(x.claim)) { const o = qzOpts(x.options[x.answer], x.options.filter((_, j) => j !== x.answer)); out.push(Object.assign({ key: "mc:" + x.claim, kind: "mc", drugs: on(x.claim), claim: x.claim, q: x.q, why: x.why || "" }, o)); } });
  // Only written questions are asked (senior author, 12 November: every question must be one a person would find useful or
  // repeat to a friend). The generated "Which is the answer?" and "Which has stronger evidence?" questions were retired.
  QZ_POOL = out; return out;
}
// pages named for more than one drug: "Which family are benzodiazepines in?"
const PLURAL_PAGE = ["benzodiazepines", "nicotine", "synthetic-cathinones", "dmt-ayahuasca", "2c-x", "synthetic-cannabinoids", "fentanyl-and-analogues", "prescription-opioids", "methadone-buprenorphine", "alkyl-nitrites-and-inhalants"];
const QZ_KIND = { tf: ["bulb", "True or false?"], mc: ["bulb", "Quick question"], ans: ["search", "Which is the answer?"], sure: ["scale", "Which has stronger evidence?"], street: ["pin", "Street names"], family: ["molecule", "Drug families"] };
const drugName = slug => ((subBySlug[slug] || {}).name || slug).replace(/\s*\(.*\)$/, "");
// no two questions of the same kind in a row, where the pool allows it
function qzSpread(xs) { const left = xs.slice(), out = []; while (left.length) { const last = out.length ? out[out.length - 1].kind : null; let i = left.findIndex(x => x.kind !== last); if (i < 0) i = 0; out.push(left.splice(i, 1)[0]); } return out; }
/* One quiz across the whole visit (senior author, 6 November: a question came back in the same quiz, and "More questions"
   set his score back to 0). The score and the questions already asked are shared by every quiz box on the site for the
   rest of the visit (kept in this tab only); no question comes twice, and an answer asked one way is not asked again
   another way, until every question has been asked. Then the reader is told, and can start again in a new order.
   Questions never answered on this device come first, then the ones missed on an earlier visit, then the rest. */
const QZ_SESSION = "pk-quiz-session";
function qzLoad() { try { const x = JSON.parse(sessionStorage.getItem(QZ_SESSION) || "null"); if (x && Array.isArray(x.claims)) return x; } catch (e) { /* not kept */ } return { right: 0, done: 0, claims: [] }; }
let QZS = qzLoad();
function qzSave() { try { sessionStorage.setItem(QZ_SESSION, JSON.stringify(QZS)); } catch (e) { /* this page only */ } }
function qzScore() { return QZS.done ? QZS.right + " of " + QZS.done + " right" : ""; }
function qzOrder(slug) {
  const all = qzPool(), seen = qzSeen(), again = qzAgain(), asked = new Set(QZS.claims);
  const pool = all.filter(x => !asked.has(x.claim));
  const tier = x => !seen.has(x.key) ? 0 : again.has(x.key) ? 1 : 2;
  const fresh = xs => [0, 1, 2].flatMap(t => qzSpread(shuffle(xs.filter(x => tier(x) === t))));
  // one question per answer (a comparison of evidence strength uses up both of its answers)
  const once = xs => { const used = new Set(); return xs.filter(x => { if (used.has(x.claim) || (x.weak && used.has(x.weak))) return false; used.add(x.claim); if (x.weak) used.add(x.weak); return true; }); };
  if (!slug) return once(fresh(pool));
  // a drug page asks about that drug first (its own answers, then the test-kit answers shown on it), then goes on with the rest
  const own = x => x.drugs.includes(slug) && claimById[x.claim] && claimById[x.claim].substance !== DC, kit = x => x.drugs.includes(slug) && !own(x), other = x => !x.drugs.includes(slug);
  return once([own, kit, other].map(f => fresh(pool.filter(f))).flat());
}
function qzTotal() { return new Set(qzPool().map(x => x.claim)).size; }
// each box keeps the questions answered in it, so the reader can go back and forward through them (senior author,
// 6 November); pos is the one shown: an earlier answered question, or (pos = hist.length) the next new one
function qzStart(boxId, slug) { const box = document.getElementById(boxId); if (!box) return; QZ[boxId] = { slug: slug || null, order: qzOrder(slug), i: 0, hist: [], pos: 0 }; qzRender(boxId); }
function qzOptHtml(x, o) {
  if (x.kind === "sure") return '<span class="qz2-oq">' + esc(anyQuestion(o) || "") + '</span><span class="qz2-os">' + esc(SIMPLE.claims[o].short) + "</span>";
  if (x.kind === "street") return esc(drugName(o));
  if (x.kind === "family") return esc(famPlain(o).word.replace(/^an? /, "").replace(/^./, c => c.toUpperCase()));
  return esc(o);
}
// the next question not yet asked in this visit (another box may have asked it since this order was made)
function qzCurrent(st) { const asked = new Set(QZS.claims), used = x => asked.has(x.claim) || (x.weak && asked.has(x.weak)); while (st.i < st.order.length && used(st.order[st.i])) st.i++; return st.order[st.i] || null; }
function qzNav(st, answered) {
  const back = st.pos > 0 ? '<button type="button" class="qz2-prev">' + icon("arrow") + "<span>Previous</span></button>" : "";
  const fwd = answered ? '<button type="button" class="qz2-nb">' + (st.pos < st.hist.length - 1 ? "Next" : "Next question") + "</button>" : "";
  return back || fwd ? '<p class="qz2-next">' + back + fwd + "</p>" : "";
}
function qzRender(boxId) {
  const st = QZ[boxId], box = document.getElementById(boxId); if (!st || !box) return;
  const past = st.pos < st.hist.length ? st.hist[st.pos] : null, x = past ? past.x : qzCurrent(st);
  box.hidden = false;
  if (!x) {
    if (!st.order.length && !QZS.done) { box.hidden = true; return; }
    box.innerHTML = '<div class="qz2-top"><span class="qz2-k">' + icon("check") + "<span>All done</span></span>" + '<span class="qz2-score" aria-live="polite">' + qzScore() + "</span></div>" +
      '<p class="qz2-q">You have answered all ' + qzTotal() + " questions." + (QZS.done ? " You got " + QZS.right + " of " + QZS.done + " right." : "") + "</p>" +
      '<p class="qz2-next">' + (st.hist.length ? '<button type="button" class="qz2-prev">' + icon("arrow") + "<span>Previous</span></button>" : "") + '<button type="button" class="qz2-restart">Start again in a new order</button></p>';
    return;
  }
  const k = QZ_KIND[x.kind];
  box.innerHTML = '<div class="qz2-top"><span class="qz2-k">' + icon(k[0]) + "<span>" + esc(k[1]) + "</span></span>" + '<span class="qz2-score" aria-live="polite">' + qzScore() + "</span></div>" +
    '<p class="qz2-q" id="' + boxId + '-q">' + esc(x.q) + "</p>" +
    '<div class="qz2-opts ' + x.kind + '" role="group" aria-labelledby="' + boxId + '-q">' + x.options.map((o, j) => '<button type="button" class="qz2-o' + (past ? (j === x.answer ? " right" : "") + (j === past.j && !past.ok ? " wrong" : "") : "") + '" data-j="' + j + '"' + (past ? " disabled" : "") + ">" + qzOptHtml(x, o) + "</button>").join("") + "</div>" +
    '<div class="qz2-ans"' + (past ? "" : " hidden") + ">" + (past ? qzExplain(x, past.ok) + qzNav(st, true) : "") + "</div>" + (past ? "" : qzNav(st, false));
}
// a question's own reason that already says what the answer's 'But' says: the 'But' is not repeated
function qzSame(why, but) { if (!why) return false; const w = t => new Set(norm(t).replace(/[^\p{L}\p{N}\s]/gu, " ").split(/\s+/).filter(x => x.length > 3)), A = w(why), B = w(but); let n = 0; A.forEach(x => { if (B.has(x)) n++; }); return A.size > 0 && n / A.size >= 0.5; }
function qzExplain(x, ok) {
  const sp = x.claim ? SIMPLE.claims[x.claim] : null, c = x.claim ? claimById[x.claim] : null;
  const ev = id => '<a class="qz2-ev" href="#' + id + '">See the evidence ' + icon("arrow") + "</a>";
  const word = ok ? "Right!" : "Not quite.";
  if (x.kind === "tf" || x.kind === "mc") return '<p class="qz2-fb ' + (ok ? "ok" : "no") + '">' + word + (x.kind === "tf" ? " It is " + (x.answer === 0 ? "true." : "false.") : "") + "</p>" +
    '<p class="qz2-why">' + esc(x.why || sp.short) + "</p>" + (sp.but && !qzSame(x.why, sp.but) ? '<p class="qz2-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + '<div class="qz2-row">' + meterHtml(c.grade.certainty, true) + ev(x.claim) + "</div>";
  if (x.kind === "ans") return '<p class="qz2-fb ' + (ok ? "ok" : "no") + '">' + word + (ok ? "" : " The answer is the one marked.") + "</p>" + (sp.but ? '<p class="qz2-but"><b>But</b> ' + esc(butText(sp.but)) + "</p>" : "") + '<div class="qz2-row">' + meterHtml(c.grade.certainty, true) + ev(x.claim) + "</div>";
  if (x.kind === "sure") { const w = claimById[x.weak], sw = SIMPLE.claims[x.weak];
    return '<p class="qz2-fb ' + (ok ? "ok" : "no") + '">' + word + " The research is surer about the one marked.</p>" +
      '<ul class="qz2-pair"><li>' + meterHtml(c.grade.certainty, true) + "<span>" + esc(anyQuestion(x.claim) || sp.short) + "</span> " + ev(x.claim) + "</li><li>" + meterHtml(w.grade.certainty, true) + "<span>" + esc(anyQuestion(x.weak) || sw.short) + "</span> " + ev(x.weak) + "</li></ul>" +
      (sw.but ? '<p class="qz2-but"><b>Why the other is weaker:</b> ' + esc(sw.but) + "</p>" : ""); }
  if (x.kind === "street") return '<p class="qz2-fb ' + (ok ? "ok" : "no") + '">' + word + " “" + esc(x.name) + "” is a name for " + esc(pageWord(x.slug)) + '.</p><p><a class="qz2-ev" href="#s-' + x.slug + '">' + esc(drugName(x.slug)) + ": the page " + icon("arrow") + "</a></p>";
  if (x.kind === "family") { const fp = famPlain(subBySlug[x.slug].cls), many = PLURAL_PAGE.includes(x.slug);
    return '<p class="qz2-fb ' + (ok ? "ok" : "no") + '">' + word + " " + esc(drugName(x.slug)) + (many ? " are " + esc(fp.word.replace(/^an? /, "") + "s") : " is " + esc(fp.word)) + ".</p>" + '<p class="qz2-why">' + esc(fp.line) + '</p><p class="small muted"><a href="' + esc(FAMPLAIN.source.url) + '" target="_blank" rel="noopener">Source: ' + esc(FAMPLAIN.source.publisher) + "</a></p>"; }
  return "";
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest(".qz2-o"); if (b) {
    const box = b.closest(".qz2"), st = QZ[box.id]; if (!st || b.disabled || st.pos < st.hist.length) return;
    const x = qzCurrent(st); if (!x) return;
    const j = +b.dataset.j, ok = j === x.answer;
    QZS.done++; if (ok) QZS.right++; QZS.claims.push(x.claim); if (x.weak) QZS.claims.push(x.weak); qzSave();
    qzMark(x.key); qzAgainSet(x.key, !ok);
    st.hist.push({ x, j, ok }); st.pos = st.hist.length - 1; st.i++;
    box.querySelectorAll(".qz2-o").forEach(o => { o.disabled = true; o.classList.toggle("right", +o.dataset.j === x.answer); });
    if (!ok) b.classList.add("wrong");
    const old = box.querySelector(":scope > .qz2-next"); if (old) old.remove();
    const ans = box.querySelector(".qz2-ans");
    ans.innerHTML = qzExplain(x, ok) + qzNav(st, true); ans.hidden = false;
    box.querySelectorAll(".qz2-score").forEach(s => { s.textContent = qzScore(); });
    const fb = ans.querySelector(".qz2-fb"); if (fb) { fb.setAttribute("tabindex", "-1"); fb.focus({ preventScroll: true }); }
    return;
  }
  const nav = e.target.closest && e.target.closest(".qz2-nb, .qz2-prev, .qz2-restart"); if (!nav) return;
  const box = nav.closest(".qz2"), st = QZ[box.id]; if (!st) return;
  if (nav.classList.contains("qz2-restart")) { QZS = { right: 0, done: 0, claims: [] }; qzSave(); st.order = qzOrder(st.slug); st.i = 0; st.hist = []; st.pos = 0; }
  else if (nav.classList.contains("qz2-prev")) st.pos = Math.max(0, st.pos - 1);
  else st.pos = Math.min(st.hist.length, st.pos + 1);
  qzRender(box.id);
  const focus = box.querySelector(".qz2-o:not([disabled])") || box.querySelector(".qz2-nb, .qz2-restart, .qz2-prev"); if (focus) focus.focus({ preventScroll: true });
  const pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
  if (box.getBoundingClientRect().top < pad) scrollToEl(box, true);
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
    if (k === "test") { if (d && !NO_TEST.includes(d)) add("Test it first: which kit, and where to get one", "Staying safer · " + nm, "#s-" + d + "/part-d-safer"); add("Drug checking near you", "Drug checking", "#checking");
      if (drugQuestions(DC).length) add("Do home test kits work? What studies found", "Drug checking", "#checking/kits"); }
    if (k === "law") add(d ? "Is " + pageWord(d) + " legal where I am?" : "The law, country by country", d ? "The law · " + nm : "The law", d ? "#s-" + d + "/part-d-law" : "#law");
    if (k === "help") { if (d && helpSigns(d)) add(helpTitle(d), "What to do · " + nm, "#s-" + d + "/part-d-help"); add("Emergency numbers, country by country", "Get help", "#emergency"); }
    if (k === "dose" && d && dosesBody(d)) add("Doses: where to read about them", "Staying safer · " + nm, "#s-" + d + "/part-d-safer");
  });
  const seen = new Set(); return out.filter(x => !seen.has(x.it.href) && seen.add(x.it.href));
}
