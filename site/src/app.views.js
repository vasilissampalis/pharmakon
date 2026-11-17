/* ---------- Drugs ---------- */
const subBySlug = Object.fromEntries(SUBSTANCES.map(s => [s.slug, s]));
// A claim whose supporting anchors all cite narrative reviews stays draft (METHODS §6.3).
function narrativeOnly(c) {
  const sup = c.evidence.filter(e => e.role === "supports");
  return sup.length > 0 && sup.every(e => cardById[e.study_card] && cardById[e.study_card].design === "narrative-review");
}
// why a draft is still a draft, in the reader's words: it rests on reviews whose figures are second-hand (narrative reviews, or a
// statement such as the AHA's that gives no search or appraisal and says so in the claim), or a source is still to be read or re-read
function draftWhy(c) {
  // (the page carries the statement's test as a flag, set by site/build.js, until the statement itself is fetched)
  if (narrativeOnly(c) || c.secondhand || /\b(second-hand|as summari[sz]ed|as relayed)\b/i.test(c.statement || "")) return "it rests on reviews, so its figures are second-hand";
  if (c.evidence.some(e => !/^(ai-checked|senior-verified)$/.test(e.anchor_status))) return "not every source has been checked by a second reader yet";
  return "it rests on few studies so far";
}
/* ---------- Icons, drawn for this site (24×24, stroked; generic shapes only) ---------- */
const circ = (x, y, r) => "M" + (x - r) + " " + y + "a" + r + " " + r + " 0 1 0 " + 2 * r + " 0a" + r + " " + r + " 0 1 0 " + (-2 * r) + " 0";
const ICONS = {
  message: "M5 4h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z", flag: "M5 21V4M5 4h11l-2 4 2 4H5",
  bolt: "M13 2 4 14h7l-1 8 9-12h-7l1-8z", moon: "M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z",
  heart: "M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z", eye: "M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" + circ(12, 12, 3),
  burst: "M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8",
  orbit: circ(12, 12, 3) + "M3 12c0-2.5 4-4.5 9-4.5s9 2 9 4.5-4 4.5-9 4.5-9-2-9-4.5z",
  poppy: circ(12, 8, 4.5) + circ(12, 8, 1.2) + "M12 12.5V22M12 17.5c-2.2 0-3.6-1-4.5-2.6", leaf: "M5 19C5 10 11 4 20 4c0 9-6 15-15 15zM5 19l8-8",
  wind: "M3 8h10a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7",
  molecule: circ(6, 7, 2.2) + circ(18, 9, 2.2) + circ(10, 18, 2.2) + "M8.2 7.3l7.6 1.2M6.8 9.1l2.4 6.8M16.6 10.9l-5 5.3",
  pulse: "M2 12h4l3-8 4 16 3-8h6", alert: "M12 3 2 21h20L12 3zM12 10v5M12 18h.01",
  brain: "M9.5 4A3 3 0 0 0 6.6 6.3 3 3 0 0 0 4.5 11a3 3 0 0 0 .8 4.6A3 3 0 0 0 9.5 20V4zM14.5 4a3 3 0 0 1 2.9 2.3A3 3 0 0 1 19.5 11a3 3 0 0 1-.8 4.6 3 3 0 0 1-4.2 4.4V4z",
  bulb: "M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z",
  mind: "M14 21v-3h2a3 3 0 0 0 3-3v-2l2-.5-2-4A7 7 0 1 0 7 15v6", loop: "M17 2l3 3-3 3M20 5H8a5 5 0 0 0 0 10h1M7 22l-3-3 3-3M4 19h12a5 5 0 0 0 0-10h-1",
  plus: circ(12, 12, 9) + "M12 8v8M8 12h8", chart: "M4 20V11M10 20V5M16 20v-6M2 20h20",
  scale: "M12 3v18M7 21h10M4 7h16M7 7l-3 7a3 3 0 0 0 6 0L7 7zM17 7l-3 7a3 3 0 0 0 6 0l-3-7z",
  flask: "M9 3h6M10 3v6l-5.6 9.5A1.7 1.7 0 0 0 5.9 21h12.2a1.7 1.7 0 0 0 1.5-2.5L14 9V3", tag: "M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8zM7.5 7.5h.01",
  phone: "M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z",
  speaker: "M11 5 6 9H2v6h4l5 4V5zM15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14", stop: "M7 7h10v10H7z", arrow: "M5 12h14M13 6l6 6-6 6", share: "M12 3v12M8 7l4-4 4 4M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7",
  book: "M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4V4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7V4z", check: "M5 12.5l4.5 4.5L19 7.5", x: "M6 6l12 12M18 6L6 18", search: circ(11, 11, 7) + "M21 21l-5-5",
  crystal: "M12 2 5 9l7 13 7-13-7-7zM5 9h14M9 9l3 13 3-13-3-7-3 7", powder: "M3 19h18M5 19c1-5 4-8 7-8s6 3 7 8M9 7h.01M12 5h.01M15 7h.01",
  tablet: circ(12, 12, 8) + "M7 12h10", capsule: "M10.5 20.5a5 5 0 0 1-7-7l10-10a5 5 0 0 1 7 7l-10 10zM8.5 8.5l7 7", drop: "M12 2.7 6.3 9.6a7 7 0 1 0 11.4 0L12 2.7z",
  blotter: "M4 4h16v16H4zM4 12h16M12 4v16", mushroom: "M3 11a9 7 0 0 1 18 0H3zM9 11v8a3 3 0 0 0 6 0v-8",
  cactus: "M12 21V5a2 2 0 0 1 4 0v8M12 13H9a2 2 0 0 1-2-2V8M16 10h1a2 2 0 0 0 2-2V7M8 21h8", block: "M12 2 3 7v10l9 5 9-5V7l-9-5zM3 7l9 5 9-5M12 12v10",
  canister: "M8 6h8v14a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2V6zM10 2h4v4h-4z",
  pin: "M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z" + circ(12, 9, 2.5),
  mix: circ(9, 12, 6) + circ(15, 12, 6),
  people: circ(8, 8, 3) + circ(16.5, 9, 2.5) + "M2.5 20c0-3.3 2.4-5.5 5.5-5.5s5.5 2.2 5.5 5.5M15 14.6c3.4-.6 6.5 1.4 6.5 5.4", globe: circ(12, 12, 9) + "M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18",
  search: "M4 11a7 7 0 1 0 14 0 7 7 0 1 0-14 0M21 21l-5-5", clock: circ(12, 12, 9) + "M12 7v5l3 2"
};
function icon(name, cls) { const d = ICONS[name]; return d ? '<svg class="ic' + (cls ? " " + cls : "") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>' : ""; }
/* One colour and one icon per drug family (the families are the site's classes) */
const FAMILY = { "Stimulants": { k: "stim", icon: "bolt" }, "Depressants": { k: "dep", icon: "moon" }, "Entactogens": { k: "ent", icon: "heart" }, "Classic psychedelics": { k: "psy", icon: "eye" }, "Atypical psychedelics": { k: "apsy", icon: "burst" }, "Dissociatives": { k: "dis", icon: "orbit" }, "Opioids": { k: "opi", icon: "poppy" }, "Cannabinoids": { k: "can", icon: "leaf" }, "Inhalants": { k: "inh", icon: "wind" } };
function fam(cls) { return FAMILY[cls] || { k: "oth", icon: "molecule" }; }
/* How strong the evidence is: the GRADE level as signal bars and words; the GRADE term stays in the title */
const CERT_WORDS = { high: "Strong evidence", moderate: "Moderate evidence", low: "Limited evidence", "very-low": "Very limited evidence" };
function meterHtml(cert, small) {
  const n = { high: 4, moderate: 3, low: 2, "very-low": 1 }[cert] || 1;
  return '<span class="meter m' + n + (small ? " sm" : "") + '" title="GRADE certainty: ' + esc(String(cert).replace("-", " ")) + '"><span class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="mw">' + esc(CERT_WORDS[cert] || cert) + "</span></span>";
}
function meterDots(cert) { const n = { high: 4, moderate: 3, low: 2, "very-low": 1 }[cert] || 1; return '<span class="meter m' + n + ' xs" title="' + esc(CERT_WORDS[cert] || cert) + '"><span class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="sr">' + esc(CERT_WORDS[cert] || cert) + "</span></span>"; }
const META_SOURCE = { crossref: "Crossref", publisher: "publisher's page", pubmed: "PubMed", manual: "entered by hand" };

/* ---------- Routing ---------- */
const PAGE_VIEWS = ["home", "substances", "drug", "shared", "numbers", "interactions", "checking", "facts", "emergency", "law", "methods", "about", "glossary", "howto", "wanted", "auto", "review", "quiz", "notfound"];
const PAGE_TITLES = { home: "", shared: "Shared answer", facts: "Big questions about drugs", substances: "All drugs", numbers: "Statistics", interactions: "Is it safe to mix?", emergency: "Emergency numbers", checking: "Drug checking", law: "Drug treaties by country", methods: "How we check facts", about: "About us", glossary: "Words explained", howto: "How to read this site", wanted: "On our list", auto: "Written by our system", review: "Review queue", quiz: "Myth or fact?", notfound: "Page not found" };
let currentSlug = MONO.slug;   // the drug page last shown (the review queue lists its claims)
function setTitle(t) { document.title = t ? t + " · Pharmakon" : "Pharmakon: what the research says about drugs"; }
// after a page change, keyboard and screen-reader users start at the page heading
function focusHeading(view) { const h = document.querySelector("#view-" + view + " h1"); if (h) { h.setAttribute("tabindex", "-1"); try { h.focus({ preventScroll: true }); } catch (e) { h.focus(); } } }
function openAround(el) { for (let d = el && el.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true; }
let routedOnce = false;
/* ---------- Where you were (site 2.4, 15 November 2026; the senior author: "we want the user never to feel like they are lost
   and try to get to where they were before in relevance to where they are now"; "there should be a button so as to be able
   to go back to the landing page and in general where i was before"). Every step a reader takes on the site (a page, a
   section of a page) is kept in a short list for this tab only (sessionStorage; nothing is sent anywhere): its address, its
   name, how far down the reader was and which question was open. Two things use it. A line under the top bar of every page
   but the start page says where Back leads ("Back to Cannabis"), and going Back or Forward, by that line or by the
   browser's own buttons, puts the page as it was: the same place, the same question open. A reload does the same. ---------- */
const NAV_KEY = "pk-nav";
const NAV = (() => { try { const x = JSON.parse(sessionStorage.getItem(NAV_KEY) || "null"); if (x && Array.isArray(x.list) && typeof x.idx === "number") return x; } catch (e) { /* this visit only */ } return { idx: -1, list: [] }; })();
let NAV_CUR = null, NAV_REPLACING = false, NAV_TRAVERSE = false, NAV_HOLD = 0, NAV_MOVED = false;
function navStore() { try { sessionStorage.setItem(NAV_KEY, JSON.stringify(NAV)); } catch (e) { /* this page only */ } }
// what the page being left looked like: how far down, and the question that was open
function navLeave() {
  const e = NAV.list[NAV.idx]; if (!e || e.id !== NAV_CUR) return;
  e.y = Math.round(window.scrollY);
  const d = document.querySelector(".view.active details.ask[open]"); e.q = d ? d.id : "";
  navStore();
}
// the step just arrived at: one already in the list (Back, Forward, a reload), or a new one after the step left
function navEnter() {
  let st = null; try { st = history.state; } catch (e) { /* none */ }
  const at = st && st.pk ? NAV.list.findIndex(x => x.id === st.pk) : -1;
  if (at >= 0) { NAV.idx = at; NAV_CUR = st.pk; NAV_TRAVERSE = true; }
  else {
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    if (NAV_REPLACING && NAV.idx >= 0) NAV.list[NAV.idx] = { id };
    else { NAV.list = NAV.list.slice(0, NAV.idx + 1); NAV.list.push({ id }); while (NAV.list.length > 60) NAV.list.shift(); NAV.idx = NAV.list.length - 1; }
    try { history.replaceState(Object.assign({}, st || {}, { pk: id }), ""); } catch (e) { /* the list still works for this page */ }
    NAV_CUR = id; NAV_TRAVERSE = false;
  }
  NAV_REPLACING = false;
}
// an address that takes the place of the one just asked for (an older address, a section's bare name)
function navReplace(url) { NAV_REPLACING = true; location.replace(url); }
// the name a step is known by: the page's title, with the open section's name
function navTitle() {
  const v = document.querySelector(".view.active"), name = v ? v.id.replace("view-", "") : "home";
  if (name === "home") return "Start page";
  const t = document.title.replace(/ · Pharmakon$/, ""), b = v.querySelector('.secpage .sm-b[aria-expanded="true"] .sm-s');
  return (t || PAGE_TITLES[name] || "the page before") + (b && b.textContent ? ": " + b.textContent : "");
}
function navCrumb() {
  const bar = document.getElementById("crumb"); if (!bar) return;
  const home = !!document.querySelector("#view-home.active"), prev = NAV.idx > 0 ? NAV.list[NAV.idx - 1] : null;
  if (home) { bar.hidden = true; bar.innerHTML = ""; return; }
  // inside a section opened from its own page's list, the first chip of the section menu already leads back to that list
  // ("← Statistics"): a second line saying the same thing just above it would be noise, so the line rests there
  const page = document.querySelector(".view.active .secpage"), sec = page ? openSec(page) : "";
  if (sec && prev && page.dataset.base && prev.h === "#" + page.dataset.base) { bar.hidden = true; bar.innerHTML = ""; return; }
  bar.innerHTML = prev && prev.h != null && prev.t
    ? '<a class="crumb-a" href="' + esc(prev.h || "#home") + '" data-nav-back>' + icon("arrow") + "<span>Back to " + esc(prev.t) + "</span></a>"
    : '<a class="crumb-a" href="#home">' + icon("arrow") + "<span>Start page</span></a>";
  bar.hidden = false;
}
// the page as it was: the question that was open, and the same place; kept there while the page settles, until the reader moves
function navRestore(e) {
  jumpStop(); NAV_HOLD = Date.now() + 500; NAV_MOVED = false;
  const d = e.q ? document.getElementById(e.q) : null;
  if (d && d.closest(".view.active") && "open" in d && !d.open) {
    const more = d.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
    d.open = true;
  }
  const put = () => { if (Math.abs(window.scrollY - e.y) > 2) window.scrollTo(0, e.y); };
  put(); [80, 250, 600, 1200].forEach(ms => setTimeout(() => { if (NAV_CUR === e.id && !NAV_MOVED) put(); }, ms));
}
function navAfter() {
  const e = NAV.list[NAV.idx]; if (!e) return;
  e.h = location.hash || "#home"; e.t = navTitle();
  navCrumb();
  if (NAV_TRAVERSE && typeof e.y === "number") navRestore(e);
  NAV_TRAVERSE = false; navStore();
}
if (typeof window !== "undefined") {
  window.addEventListener("scroll", () => { clearTimeout(navLeave._t); navLeave._t = setTimeout(navLeave, 250); }, { passive: true });
  window.addEventListener("pagehide", navLeave);
  ["wheel", "touchstart", "keydown", "pointerdown"].forEach(t => window.addEventListener(t, () => { NAV_MOVED = true; }, { passive: true, capture: true }));
  document.addEventListener("click", ev => {
    const a = ev.target.closest && ev.target.closest("a[data-nav-back]"); if (!a || ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    ev.preventDefault(); history.back();
  });
}
function route() { navLeave(); navEnter(); routeTo(); navAfter(); }
function routeTo() {
  let h = (location.hash || "#home").slice(1);
  const first = !routedOnce; routedOnce = true;
  jumpStop();   // a jump still being kept in place gives way to the new address
  if (typeof EV !== "undefined" && EV.open) closeEvidence(true);
  // one shared answer: #a/<page>/<claim>, the Share button's address (only that answer, then the way to the rest)
  if (h.startsWith("a/")) {
    const m = h.match(/^a\/([a-z0-9-]+)\/(cl_[a-z0-9_]+)$/), t = m && renderShared(m[1], m[2]);
    if (t) { show("shared"); setTitle(t); window.scrollTo({ top: 0 }); focusHeading("shared"); return; }
    renderNotFound(h.slice(2)); show("notfound"); setTitle(PAGE_TITLES.notfound); window.scrollTo({ top: 0 }); focusHeading("notfound"); return;
  }
  // a drug page: #s-ketamine, with a section (#s-ketamine/part-d-law) or a question (#s-ketamine/q-cl_...) open. Each drug has
  // one page (site 2.3; the senior author: "it is strange that in each drug page we have the Quick and Full version ... each
  // drug page should be one"): the addresses of the research page that stood beside it (/evidence, /sec-13, /not-yet) lead to
  // the page, its law or its looks.
  if (h.startsWith("s-")) {
    const mm = h.slice(2).match(/^([a-z0-9-]+)(?:\/(sec-\d+|not-yet|evidence|q-cl_[a-z0-9_]+|part-d-[a-z]+))?$/);
    const slug = mm ? mm[1] : h.slice(2), sec = mm && mm[2];
    if (!mm || !subBySlug[slug]) { renderNotFound(h.slice(2)); show("notfound"); setTitle(PAGE_TITLES.notfound); window.scrollTo({ top: 0 }); focusHeading("notfound"); return; }
    if (sec && !sec.startsWith("q-") && !sec.startsWith("part-")) { navReplace("#s-" + slug + (sec === "sec-13" ? "/part-d-law" : sec === "sec-2" ? "/part-d-looks" : "")); return; }
    const was = renderedDrug === slug && document.getElementById("view-drug").classList.contains("active") ? openSec() : "";
    if (renderedDrug !== slug) renderDrug(slug);
    show("drug"); setTitle(subBySlug[slug].name);
    drugGo(sec, { first, was }); return;
  }
  // a section's bare name (#d-help) is that section of the drug page last shown
  if (/^d-[a-z]+$/.test(h) && renderedDrug) { navReplace("#s-" + renderedDrug + "/part-" + h); return; }
  if (h.startsWith("mix-")) { renderInteractions(); show("interactions"); setTitle("Mixing drugs"); const el = document.getElementById(h); if (el) { openAround(el); scrollToEl(el); } return; }
  // Big questions about drugs (the general answers): #facts, a section (#facts/part-f-laws), a question (#facts/q-<claim>),
  // and a bare claim address of a general answer (a shared link), which opens the question with its evidence over it
  if (h === "facts" || h.startsWith("facts/") || (h.startsWith("cl_") && claimById[h] && claimById[h].substance === GEN)) {
    const page = document.getElementById("facts-box"), was = document.getElementById("view-facts").classList.contains("active") ? openSec(page) : "";
    renderFacts(); show("facts"); setTitle(PAGE_TITLES.facts);
    secGo(page, "facts", h.startsWith("cl_") ? "q-" + h : h.slice(6), { first, was });
    if (h.startsWith("cl_")) setTimeout(() => openEvidence(h, null, null), 60);
    return;
  }
  // Drug checking: #checking, a section (#checking/part-c-work), a question on test kits (#checking/q-<claim>; a bare claim
  // address opens there too, with its evidence over it), and the address the answers had before 2.4 (#checking/kits)
  if (h === "checking" || (h.startsWith("checking/") && !h.startsWith("checking/c-")) || (h.startsWith("cl_") && claimById[h] && claimById[h].substance === "drug-checking")) {
    const page = document.getElementById("dc-page"), was = document.getElementById("view-checking").classList.contains("active") ? openSec(page) : "";
    show("checking"); setTitle(PAGE_TITLES.checking);
    secGo(page, "checking", h.startsWith("cl_") ? "q-" + h : h === "checking/kits" ? "part-c-work" : h.slice(9), { first, was });
    if (h.startsWith("cl_")) setTimeout(() => openEvidence(h, null, null), 60);
    return;
  }
  // a mixing answer's own address opens that answer in plain words, with its evidence over it (senior author, 6 November:
  // the full table opened instead, with a long paragraph "like reading the paper")
  if (h.startsWith("cl_") && claimById[h] && claimById[h].substance === "interactions") { renderInteractions(); const t = renderShared("mixing", h); show("shared"); setTitle(t || "Mixing drugs"); window.scrollTo({ top: 0 }); setTimeout(() => openEvidence(h, null, null), 60); return; }
  // an answer's own address (a shared link, a search result, one typed in) opens the page that asks it, at the question, with
  // the answer's evidence over it
  if (h.startsWith("cl_") && claimById[h]) {
    const c = claimById[h], key = answerPageKey(h), slug = subBySlug[key] ? key : subBySlug[c.substance] ? c.substance : null;
    if (slug) {
      if (renderedDrug !== slug) renderDrug(slug);
      show("drug"); setTitle(subBySlug[slug].name);
      const d = document.getElementById("ask-" + h), sec = d && d.closest(".secs > .sec");
      if (d && sec) { showSec(sec.id); d.open = true; scrollToEl(d); } else { showSec(""); window.scrollTo({ top: 0 }); }
    } else { show("home"); setTitle(""); window.scrollTo({ top: 0 }); }
    setTimeout(() => openEvidence(h, null, null), 60); return;
  }
  if (h.startsWith("g-")) { show("glossary"); setTitle(PAGE_TITLES.glossary); const el = document.getElementById(h); if (el) { if ("open" in el) el.open = true; scrollToEl(el); } return; }
  // a country chosen in the search: #checking/c-Greece, #emergency/c-Greece, #law/c-Greece
  const cm = h.match(/^(emergency|checking|law)\/c-(.+)$/);
  if (cm) { show(cm[1]); setTitle(PAGE_TITLES[cm[1]]); window.scrollTo({ top: 0 }); if (cm[1] === "checking") showSec("c-near", document.getElementById("dc-page")); openCountry(cm[1], decodeURIComponent(cm[2])); return; }
  // (2.6) the answers the system wrote: the page that lists them, and one of them opened over it (#auto/q-au_...)
  const am = h.match(/^auto(?:\/q-(au_[a-z0-9_]+))?$/);
  if (am) { autoPage(); show("auto"); setTitle(PAGE_TITLES.auto); if (!am[1]) { window.scrollTo({ top: 0 }); if (!first) focusHeading("auto"); } else if (isAuto(am[1])) setTimeout(() => { if (!EV.open) openInsight(am[1], null, true); }, 80); return; }
  // (2.8) a page the system started: #auto/p-kava; (2.12) in the form of a drug's page, with its parts: #auto/p-kanna/part-p-looks
  const ap = h.match(/^auto\/p-([a-z0-9-]{1,60})(?:\/(part-[a-z0-9-]+))?$/);
  if (ap && typeof AUTO_PAGES === "object" && AUTO_PAGES && AUTO_PAGES[ap[1]]) {
    const pg = document.getElementById("auto-page"), same = !!pg && !pg.hidden && pg.dataset.base === "auto/p-" + ap[1], was = same && document.getElementById("view-auto").classList.contains("active") ? openSec(pg) : "";
    if (!same) autoPage(ap[1]);
    show("auto"); setTitle(AUTO_PAGES[ap[1]]);
    if (pg && pg.querySelector(".secmenu")) secGo(pg, "auto", ap[2] || "", { first, was });
    else { const sec = ap[2] && pg ? pg.querySelector("#" + ap[2].slice(5)) : null; if (sec) scrollToEl(sec); else { window.scrollTo({ top: 0 }); if (!first) focusHeading("auto"); } }
    return;
  }
  // a page of sections: #methods, #methods/part-m-search (the text pages), #numbers/part-n-europe (the statistics)
  const sp = h.match(/^(howto|methods|about|numbers)(?:\/(part-[a-z0-9-]+))?$/);
  if (sp) {
    const view = sp[1], page = document.querySelector("#view-" + view + " .secpage"), was = page && document.getElementById("view-" + view).classList.contains("active") ? openSec(page) : "";
    show(view); setTitle(PAGE_TITLES[view]);
    if (view === "numbers") { showNumbers(sp[2] || "", { first, was }); return; }
    if (page) secGo(page, view, sp[2] || "", { first, was }); else { window.scrollTo({ top: 0 }); if (!first) focusHeading(view); }
    return;
  }
  if (!PAGE_VIEWS.includes(h) || h === "notfound" || h === "drug" || h === "shared") h = "home";
  show(h); setTitle(PAGE_TITLES[h]);
  // pages that read files fetched when needed draw on their first visit (speed, 13 November)
  if (h === "review") whenReady(() => Promise.all(FULL_FILES.map(loadFull).concat(loadRefs(), loadJson("decisions.json", d => Object.assign(DECISIONS, d)))), document.getElementById("review-list"), "The review queue", renderReview);
  // the Myth or fact? page: the same deck as the start page, endless (senior author, 14 November: one format everywhere)
  if (h === "quiz") mfQuizPage();
  if (h === "home") { homeCont(); mfRefresh("tf"); }
  window.scrollTo({ top: 0 });
  if (!first) focusHeading(h);
}
/* Unknown addresses get a page of their own, never another drug's page */
function editDistance(a, b) {
  if (Math.abs(a.length - b.length) > 3) return 9;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i].concat(Array(b.length).fill(0)));
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length];
}
function renderNotFound(asked) {
  const q = String(asked || "").toLowerCase().replace(/\/.*$/, "");
  const near = SUBSTANCES.map(s => [Math.min(editDistance(q, s.slug), editDistance(q, s.name.toLowerCase())), s]).filter(p => p[0] <= 3).sort((a, b) => a[0] - b[0]).slice(0, 3).map(p => p[1]);
  document.getElementById("notfound-body").innerHTML = '<p>There is no page at this address' + (q ? ' (<span class="mono">' + esc(q) + "</span>)" : "") + ". " + (near.length ? "Did you mean " + near.map(s => '<a href="#s-' + s.slug + '">' + esc(s.name) + "</a>").join(" or ") + "?" : "") + '</p><p><a href="#substances">All 30 drugs</a> · use the search box above</p>';
}
function show(name) {
  PAGE_VIEWS.forEach(v => { const el = document.getElementById("view-" + v); if (el) el.classList.toggle("active", v === name); });
  document.body.classList.toggle("on-emergency", name === "emergency");
  document.querySelectorAll("nav.main a, .topbar .sosbtn").forEach(a => { if (a.dataset.view === name) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
  document.querySelectorAll("details.navmore").forEach(d => { d.open = false; d.querySelector("summary").classList.toggle("cur", !!d.querySelector('a[aria-current="page"]')); });
  closeSearch(); placeSearch(name); updateSticky();
}
/* Where a jump lands (site 2.3, 15 November 2026; the senior author: "the cut you see in the picture when you click on a link
   and can't see the question ... i want to see where the section or question starts this is a generalized bug whenever you
   click on a link on the website"). The bars stuck to the top were measured, but a bar narrower than 60% of the window was
   taken for a side column: on a window wider than about 1500 px a drug page's chips (892 px) were left out, and every jump
   there ended with its first lines under them. Now one place decides it for every jump on the site (scrollToEl): the bars
   that sit over the target are measured (the top bar; a drug page's section menu and the facts page's chips under it; in
   an answer sheet, the sheet's own bar), their sum is kept in one variable (--stick-h, which every target also carries as
   its scroll-margin-top, for the browser's own jumps), the target is placed just under them, and placed again while the
   layout settles (a photo or a font arriving, a file drawn, an answer closing above it), until the reader scrolls, taps or
   types. A target folded away is opened first (revealEl). */
try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) { /* the browser keeps its own */ }
const STICK_GAP = 10;
function stickyH(el) {
  if (!el || !el.getClientRects().length) return 0;
  const s = getComputedStyle(el); return s.position === "sticky" || s.position === "fixed" ? Math.round(el.getBoundingClientRect().height) : 0;
}
// how much of the top of the window the stuck bars take over a target (over the widest content, with no target)
function updateSticky(target) {
  const bar = stickyH(document.querySelector(".topbar")); let below = 0;
  const tr = target && target.getClientRects().length ? target.getBoundingClientRect() : null;
  document.querySelectorAll(".view.active .secmenu, .view.active nav.chips").forEach(n => {
    if (target && n.contains(target)) return;
    const h = stickyH(n); if (!h) return;
    const r = n.getBoundingClientRect(); if (tr && (r.right <= tr.left + 1 || r.left >= tr.right - 1)) return;   // beside the target, not over it
    below = Math.max(below, h); });
  const root = document.documentElement.style;
  root.setProperty("--bar-h", bar + "px"); root.setProperty("--stick-h", (bar + below + STICK_GAP) + "px");
  return bar + below + STICK_GAP;
}
window.addEventListener("resize", () => { clearTimeout(updateSticky._t); updateSticky._t = setTimeout(() => updateSticky(), 120); }, { passive: true });
let JUMP = null;   // the jump being kept in place
function jumpStop() { if (JUMP) JUMP.stop(); }
function scrollToEl(el, smooth) {
  if (!el) return;
  if (NAV_HOLD > Date.now()) return;   // the page is being put back as it was (Back, Forward, a reload): nothing else moves it
  if (typeof revealEl === "function") revealEl(el);
  if (!el.getClientRects().length) return;
  jumpStop();
  const box = el.closest(".drawer .panel");   // an answer sheet scrolls inside itself, under its own bar
  const offset = () => box ? stickyH(box.querySelector(".ev-bar")) + STICK_GAP : updateSticky(el);
  const delta = () => el.getBoundingClientRect().top - (box ? box.getBoundingClientRect().top : 0) - offset();
  const place = () => { const d = delta(); if (Math.abs(d) > 1) { if (box) box.scrollTop += d; else window.scrollBy(0, d); } };
  // a short move the eye can follow glides (an answer opening where it is); a long one, or with less motion asked for, jumps
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches, d0 = delta();
  const glide = !!smooth && !reduce && !box && Math.abs(d0) < window.innerHeight;
  if (glide) window.scrollBy({ top: d0, behavior: "smooth" }); else place();
  const t0 = Date.now(), offs = []; let dead = false, raf = 0, ro = null, timers = [];
  const stop = () => { if (dead) return; dead = true; offs.forEach(f => f()); if (ro) ro.disconnect(); timers.forEach(clearTimeout); if (raf) cancelAnimationFrame(raf); if (JUMP && JUMP.el === el) JUMP = null; };
  const again = () => { if (dead || (glide && Date.now() - t0 < 420)) return; if (!el.isConnected || !el.getClientRects().length) { stop(); return; } place(); };
  const soon = () => { if (dead || raf) return; raf = requestAnimationFrame(() => { raf = 0; again(); }); };
  const on = (target, type, fn, opts) => { target.addEventListener(type, fn, opts); offs.push(() => target.removeEventListener(type, fn, opts)); };
  ["wheel", "touchstart", "touchmove", "keydown", "pointerdown", "mousedown"].forEach(t => on(window, t, stop, { passive: true, capture: true }));
  on(document, "load", soon, true);   // a photo arriving
  if (typeof ResizeObserver !== "undefined") { ro = new ResizeObserver(soon); ro.observe(document.body); if (box && box.firstElementChild) ro.observe(box); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(soon, () => {});
  timers = [glide ? 450 : 60, 160, 320, 640, 1000, 1600, 2600, 4000].map((ms, i, a) => setTimeout(i === a.length - 1 ? () => { again(); stop(); } : again, ms));
  JUMP = { el, stop };
}

/* ---------- Home ---------- */
/* A drug as a tile: its family's colour and icon, its name, the street names documented by two or more sources */
/* ---------- Photos of what each drug looks like (data/site/photos.json): free licences, each with its credit.
   Several forms of one drug help people recognise it; no people and no drugs being used; one switch hides them all,
   remembered on this device only (docs/WRITING-RULES.md, "Photos"). ---------- */
const photosFor = slug => PHOTOS.filter(p => p.drug === slug);
const headerPhoto = slug => photosFor(slug).find(p => p.header) || photosFor(slug)[0] || null;
let photosHidden = false;
// v2 key (25 October): photos show again for everyone once, since a hidden setting was easy to miss; the banner below now says when they are hidden
try { photosHidden = localStorage.getItem("pk-photos-v2") === "hidden"; } catch (e) { /* storage blocked: photos stay on */ }
function applyPhotoPref() {
  document.documentElement.classList.toggle("nophotos", photosHidden);
  document.querySelectorAll("button.phtoggle").forEach(b => { b.textContent = photosHidden ? "Show drug photos" : "Hide drug photos"; b.setAttribute("aria-pressed", String(photosHidden)); });
  const ban = document.getElementById("phbanner"); if (ban) ban.hidden = !photosHidden;  // never hidden without saying so
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("button.phtoggle"); if (!b) return;
  photosHidden = !photosHidden; try { localStorage.setItem("pk-photos-v2", photosHidden ? "hidden" : "shown"); } catch (err) { /* not remembered after this visit */ }
  applyPhotoPref();
});
const phToggle = () => '<button type="button" class="phtoggle linklike" aria-pressed="' + photosHidden + '">' + (photosHidden ? "Show drug photos" : "Hide drug photos") + "</button>";
function photoImg(p, size, alt, lazy) { const d = p[size]; return '<img class="ph" src="img/' + p.id + "-" + size + '.webp" width="' + d[0] + '" height="' + d[1] + '" alt="' + esc(alt == null ? p.alt : alt) + '"' + (lazy ? ' loading="lazy" decoding="async"' : "") + ">"; }
function photoCredit(p) {
  const c = p.credit;
  const via = c.source === "Wikimedia Commons" ? ", via Wikimedia Commons" : c.source === "Flickr" ? ", via Flickr" : "";
  return '<span class="phcredit">Photo: <a href="' + esc(c.file_page) + '" target="_blank" rel="noopener">' + esc(c.author) + "</a>, " + (c.licence_url ? '<a href="' + esc(c.licence_url) + '" target="_blank" rel="noopener">' + esc(c.licence_label) + "</a>" : esc(c.licence_label)) + via + (p.changes ? " (" + esc(p.changes) + ")" : "") + "</span>";
}
function photoFig(p, size, label, detail) {
  return '<figure class="phfig">' + photoImg(p, size, null, true) + "<figcaption><b>" + esc(label || p.form) + "</b>" + ((detail !== undefined ? detail : p.detail) ? ' <span class="muted">' + esc(detail !== undefined ? detail : p.detail) + "</span>" : "") + photoCredit(p) + "</figcaption></figure>";
}
const POPULAR = ["cannabis", "alcohol", "mdma", "cocaine", "ketamine", "methamphetamine", "ghb-gbl", "benzodiazepines", "psilocybin", "lsd", "heroin", "fentanyl-and-analogues", "nitrous-oxide", "synthetic-cathinones"];

/* ---------- Substances ---------- */
let activeClass = "All";
function renderSubstances() {
  const classes = ["All"].concat(CLASSES.map(c => c.name).filter(n => SUBSTANCES.some(s => s.cls === n)));
  document.getElementById("filters").innerHTML = classes.map(c => '<button class="chip' + (c === "All" ? "" : " famchip f-" + fam(c).k) + '" data-cls="' + esc(c) + '" aria-pressed="' + (c === activeClass) + '">' + (c === "All" ? "" : icon(fam(c).icon)) + esc(c === "All" ? "All 30" : c) + "</button>").join("");
  document.querySelectorAll("#filters .chip").forEach(b => b.addEventListener("click", () => { activeClass = b.dataset.cls; renderSubstances(); }));
  const list = SUBSTANCES.filter(s => activeClass === "All" || s.cls === activeClass);
  // (site 2.4) the same picture cards as the start page, two across on a phone: the page was one large tile per row, some 12,000 pixels of it
  document.getElementById("subgrid").innerHTML = list.map(s => drugCardHtml(s, 0)).join("");
  // (2.8) under the drugs: the pages our system started, with their label (only under "All": they have no family a person gave them)
  const more = document.getElementById("sub-started");
  if (more) more.innerHTML = activeClass === "All" ? autoStartedListHtml() : "";
}

/* ---------- Claims ---------- */
const ANCHOR_LABEL = { "unchecked": "not yet located in the full text", "ai-located": "located in the full text (AI)", "ai-checked": "re-found blind (AI reader 2)", "senior-verified": "checked by the senior author" };
/* ---------- Glossary hints inside claims: the first use of a technical term opens its definition ---------- */
const GL_PATTERNS = [
  [/\b(?:odds ratios?|hazard ratios?|relative risks?)\b/i, "Odds ratio, relative risk, hazard ratio"],
  [/\b(?:OR|HR|RR)\b(?= ?[\d(])/, "Odds ratio, relative risk, hazard ratio"],
  [/\b95% CI\b|\bconfidence intervals?\b/i, "Confidence interval"],
  [/\bSMD\b|\bHedges(?:&#39;)? g\b|\bCohen(?:&#39;)?s d\b/, "Effect size (d, g, SMD)"],
  [/\bnumber needed to treat\b|\bNNT\b/i, "Absolute risk and number needed to treat (NNT)"],
  [/\bstandardi[sz]ed mortality ratios?\b|\bSMR\b/, "Standardized mortality ratio (SMR)"],
  [/\bhalf-li(?:fe|ves)\b/i, "Half-life"],
  [/\bdopamine transporters?\b|\bDAT\b/, "Dopamine transporter (DAT)"],
  [/\bVMAT2\b/, "VMAT2"],
  [/\bPET\b|\bSPECT\b/, "PET and SPECT"],
  [/\bgr[ae]y[- ]matter\b|\bvoxel-based morphometry\b/i, "Grey matter and voxel-based morphometry (VBM)"],
  [/I²/, "Heterogeneity (I²)"],
  [/\bplacebo\b/i, "Placebo, blinding and intention to treat"],
  [/\bpsycho(?:sis|tic)\b/i, "Psychosis and psychotic symptoms"],
  [/\beditors(?:&#39;)? calculation\b/i, "Editors' calculation"],
  [/\bwithin-person\b/i, "Within-person design"],
  [/\bcross-sectional\b/i, "Cross-sectional study"],
  [/\bmeta-analys[ie]s\b/i, "Systematic review and meta-analysis"],
  [/\bstandard deviations?\b|\bSD\b/, "Standard deviation (SD) and the normal range"],
  [/\bwithdrawal\b/i, "Withdrawal"],
  [/\btolerance\b/i, "Tolerance"],
  [/\bdependence\b/i, "Dependence and use disorder"],
  [/\bpost hoc\b/i, "Post hoc analysis"],
  [/\bconfound(?:ing|ers?|ed)\b|\badjust(?:ed|ment|ing)\b/i, "Confounding and adjustment"],
  [/\bregression to the mean\b/i, "Regression to the mean"],
  [/\bpractice effects?\b|\bfrom taking the tests a second time\b/i, "Practice effect"],
  [/\bextrapyramidal\b/i, "Extrapyramidal side effects"],
  [/\bfractional anisotropy\b/i, "Fractional anisotropy (DTI)"],
];
const GL_INDEX = Object.fromEntries(GLOSSARY.map((g, i) => [g.term, i]));
function glossify(escaped, used) {
  let segs = [{ t: escaped, tag: false }];
  for (const [re, term] of GL_PATTERNS) {
    if (used.has(term) || !(term in GL_INDEX)) continue;
    for (let k = 0; k < segs.length; k++) {
      if (segs[k].tag) continue;
      const m = segs[k].t.match(re);
      if (!m) continue;
      const t = segs[k].t, a = m.index, b = a + m[0].length;
      segs.splice(k, 1, { t: t.slice(0, a), tag: false }, { t: '<button type="button" class="gl" data-gl="' + GL_INDEX[term] + '">' + m[0] + "</button>", tag: true }, { t: t.slice(b), tag: false });
      used.add(term); break;
    }
  }
  return segs.map(x => x.t).join("");
}
/* The currency check (data/site/currency.json): an answer says when newer research that could change it has been found and is
   not in it yet (not read, or read and being checked). What the search found nothing for, or what has since been read and
   added, is no longer said under every answer (site 2.3): the date of the last search is in the version line. */
const TYPE_WORD = { "meta-analysis": "meta-analysis", "systematic review": "systematic review", "RCT": "randomized trial", "cohort": "cohort study", "other": "study" };
function currencyHtml(c, short) {
  const k = CURRENCY.claims && CURRENCY.claims[c.id]; if (!k || !k.yes.length) return "";
  const when = new Date(CURRENCY.checked_on + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  const unread = k.yes.filter(x => !x.read && !x.checking), checking = k.yes.filter(x => x.checking), done = k.yes.filter(x => x.read);
  const readOn = done.length ? new Date(done[0].read + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) : "";
  const listOf = xs => xs.map(x => '<a href="https://doi.org/' + esc(x.doi) + '" target="_blank" rel="noopener">' + esc(String(x.first_author || "").split(" ")[0]) + " et al., " + esc(x.year) + "</a> (" + esc(TYPE_WORD[x.type] || x.type) + ")").join("; ");
  if (checking.length && !unread.length) return '<p class="currency new">' + icon("alert") + (short ? "Newer research may change this answer: " + checking.length + " newer " + (checking.length === 1 ? "study has" : "studies have") + " been read and " + (checking.length === 1 ? "is" : "are") + " being checked." : "Newer research found on " + esc(when) + " has been read and is being checked by a second reader before it is added: " + listOf(checking) + "." + (done.length ? " Already added: " + listOf(done) + "." : "")) + "</p>";
  if (!unread.length) return "";
  return '<p class="currency new">' + icon("alert") + (short ? "Newer research may change this answer: " + unread.length + " newer " + (unread.length === 1 ? "study" : "studies") + " not yet read" + (done.length ? " (" + done.length + " more already read and added)" : "") + "." : "Newer research that could change this finding was found on " + esc(when) + " and has not yet been read: " + listOf(unread) + "." + (done.length ? " Read in full on " + esc(readOn) + " and added here: " + listOf(done) + "." : "")) + "</p>";
}
// the one quiet line for someone who cites an answer, inside its deepest fold: its version, and when newer research was last searched for
function versionLine(c) {
  const k = CURRENCY.claims && CURRENCY.claims[c.id];
  return '<p class="verline">Version ' + esc(c.version) + (k && CURRENCY.checked_on ? " · last search for newer research " + esc(new Date(CURRENCY.checked_on + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })) : "") + "</p>";
}
function claimHtml(c, opts) {
  const ev = c.evidence.map((e, i) => '<div class="ex" data-anchor="' + c.id + ":" + i + '"><div><span class="role ' + e.role + '">' + e.role + "</span> " + (e.extracted.startsWith("[") ? '<span class="placeholder">' + esc(e.extracted) + "</span>" : esc(e.extracted)) + (e.quote ? ' <q>' + esc(e.quote) + "</q>" : "") + '</div><div class="src">' + cite(e.reference) + "<br>" + esc(e.page) + (e.locator && !e.locator.startsWith("[") ? " · " + esc(e.locator) : "") + '<br><span class="anchor ' + e.anchor_status + '">' + esc(e.anchor_status === "ai-checked" && (e.check_mode === "targeted" || e.check_mode === "card-check") ? "checked at the stated place (second AI reader)" : (ANCHOR_LABEL[e.anchor_status] || e.anchor_status)) + "</span></div></div>").join("");
  const citeList = [...new Set(c.evidence.map(e => e.reference))].map(cite).join(" ");
  const cardIds = [...new Set(c.evidence.map(e => e.study_card))];
  const baseLabel = sc => { const r = refById[cardById[sc].reference]; return r ? (r.author[0].short || r.author[0].literal || r.author[0].family) + " " + year(r) : sc; };
  const labelCount = {}; cardIds.forEach(sc => { const l = baseLabel(sc); labelCount[l] = (labelCount[l] || 0) + 1; });
  const cardLinks = cardIds.map(sc => { const r = refById[cardById[sc].reference]; let l = baseLabel(sc); if (labelCount[l] > 1 && r) l += ", " + (r["container-title"] || "").replace(/^The /, "").split(/[:(]/)[0].trim() + (r.volume ? " " + r.volume : ""); return '<button type="button" data-card="' + esc(sc) + '">Study card: ' + esc(l) + "</button>"; }).join("");
  const glUsed = new Set();
  const nSrc = new Set(c.evidence.map(e => e.reference)).size;
  // the plain sentence and the certainty first; the precise sentence, the study details and the evidence one tap away
  return '<article class="claim ' + c.status + '" id="' + c.id + '">' +
    '<div class="text">' + '<p class="plain">' + glossify(esc(claimText(c)), glUsed) + "</p></div>" +
    '<div class="cert">' + meterHtml(c.grade.certainty) + '<span class="lvl">GRADE: ' + esc(gradeLabel(c.grade.certainty)) + " certainty</span>" +
    '<div><span class="badge ' + c.status + '" title="Protocol term: ' + esc(STATUS_PROTOCOL[c.status] || c.status) + '">' + esc(statusLabel(c.status)) + "</span></div>" +
    '<details class="why"><summary>Why this rating</summary>' + (((typeof SIMPLE !== "undefined" && SIMPLE.claims) || {})[c.id] && SIMPLE.claims[c.id].rate ? '<p class="why-plain">' + esc(SIMPLE.claims[c.id].rate) + "</p>" : "") + '<p class="mono">' + esc(gradeDomains(c.grade)) + "</p>" + inPieces(c.grade.reasoning, esc) + "</details></div>" +
    '<details class="cdetail"' + (opts && opts.open ? " open" : "") + '><summary>Precise statement, study details and sources (' + nSrc + ")</summary>" +
    // the precise statement in short pieces, words unchanged (senior author, 13 November: the long texts were "too overwhelming")
    '<div class="text"><div class="precise"><span class="reg">Precisely</span>' + inPieces(c.statement, t => glossify(esc(t), glUsed)) + '<p class="precise-cites">' + citeList + "</p></div></div>" +
    '<div class="pecotable"><div><b>Who was studied</b>' + esc(c.population) + "</div><div><b>Exposure</b>" + esc(c.exposure) + "</div><div><b>Compared with</b>" + esc(c.comparator) + "</div><div><b>What was measured</b>" + esc(c.outcome) + "</div><div><b>How big</b>" + inPieces(c.magnitude, esc) + "</div></div>" +
    '<div class="tools">' + cardLinks + '<button type="button" data-toggle="ev-' + c.id + '">Evidence anchors (' + c.evidence.length + ")</button>" + '<a href="#' + c.id + '" class="perma" title="Link to this claim" aria-label="Link to this claim">#</a><button type="button" class="report" data-report="' + c.id + '">Report a mistake</button></div>' +
    '<div class="evid" id="ev-' + c.id + '" hidden>' + ev + "</div>" + versionLine(c) +
    "</details>" +
    currencyHtml(c) +
    "</article>";
}
function questionFor(slug, id) { for (const g of QUESTIONS[slug] || []) for (const [cid, q] of g.items) if (cid === id) return q; return null; }
/* The simplest layer of a finding, drawn from data/site/simple.json: the short answer, its catch, numbers as pictures */
function srcChips(c) {
  const ids = [...new Set(c.evidence.filter(e => e.role !== "contradicts").map(e => e.reference).concat(c.evidence.map(e => e.reference)))].filter(id => refById[id]);
  const chip = id => { const r = refById[id]; const a = r.author[0]; const who = a.short || a.literal || a.family; return '<a class="pop srcchip" href="' + esc(refLink(r)) + '" target="_blank" rel="noopener" data-ref="' + esc(id) + '" aria-label="Source: ' + esc(inTextLabel(r, REFS)) + '">' + icon("book") + esc(who + " " + year(r)) + "</a>"; };
  return '<span class="srcs"><span class="srcs-k">Sources</span>' + ids.slice(0, 4).map(chip).join("") + (ids.length > 4 ? '<a class="srcmore" href="#' + c.id + '">+' + (ids.length - 4) + "</a>" : "") + "</span>";
}
function dotsHtml(n, of, cls) { let h = '<span class="dots100' + (of > 100 ? " d1000" : "") + " " + (cls || "") + '" aria-hidden="true">'; for (let i = 0; i < of; i++) h += "<i" + (i < n ? ' class="on"' : "") + "></i>"; return h + "</span>"; }
function freqHtml(f, flat) {
  if (!f) return "";
  const num = x => Number(x).toLocaleString("en-US");
  const row = (n, label) => '<div class="freq-row' + (f.of > 100 ? " wide" : "") + '">' + dotsHtml(n, f.of) + "<span><b>" + num(n) + " in " + num(f.of) + "</b> " + esc(label) + "</span></div>";
  // the picture and its one line first; comparisons and where the number comes from one tap away (senior author, 1 November);
  // inside an open answer card they show at once, since the card is already the second level (redesign 2: no third)
  const more = (f.compare ? '<p class="freq-note">' + esc(f.compare_k || "For comparison:") + " " + f.compare.map(([k, n]) => esc(k) + " " + num(n) + " in " + num(f.of)).join(", ") + ".</p>" : "") + (f.note ? '<p class="freq-note">' + esc(f.note) + "</p>" : "");
  return '<div class="freq">' + (f.title ? '<p class="freq-k">' + esc(f.title) + "</p>" : "") + (f.pairs ? f.pairs.map(([n, l]) => row(n, l)).join("") : row(f.n, f.what)) +
    (more ? (flat ? more : '<details class="freq-more"><summary>' + "More about this number" + "</summary>" + more + "</details>") : "") + "</div>";
}
function qaHtml(c, q) {
  const sp = (SIMPLE.claims || {})[c.id];
  return '<details class="qa" id="qa-' + c.id + '"><summary><span class="qq">' + esc(q) + "</span>" + meterHtml(c.grade.certainty, true) + '</summary><div class="qbody">' +
    (sp ? '<p class="short">' + esc(sp.short) + '</p><p class="but"><b>But</b> ' + esc(sp.but) + "</p>" + freqHtml(sp.freq) : '<p>' + esc(claimText(c)) + "</p>") +
    currencyHtml(c, true) +
    '<div class="qmeta"><span class="badge ' + c.status + '">' + esc(statusLabel(c.status)) + "</span>" + (c.verification.status === "draft" ? '<span class="badge early" title="' + esc(LADDER_WORDS.draft) + '">early draft: ' + esc(draftWhy(c)) + "</span>" : "") + srcChips(c) + "</div>" +
    (sp ? '<details class="how"><summary>How we know</summary>' + (sp.how && sp.how.length ? '<ul class="howlist">' + sp.how.map(t => "<li>" + esc(t) + "</li>").join("") + "</ul>" : "<p>" + esc(claimText(c)) + "</p>") + "</details>" : "") +
    debateLine(c) + '<a class="see" href="#' + c.id + '">Full evidence ' + icon("arrow") + "</a></div></details>";
}
/* Other drugs in the same family, one tap away */
function familyHtml(m) {
  const me = subBySlug[m.slug]; if (!me) return "";
  const sib = SUBSTANCES.filter(x => x.cls === me.cls && x.slug !== m.slug); if (!sib.length) return "";
  const f = fam(me.cls);
  return '<h2 class="qh">Same family: ' + esc(me.cls.toLowerCase()) + '</h2><div class="popular famsib">' + sib.map(x => '<a class="pchip f-' + f.k + '" href="#s-' + x.slug + '">' + icon(f.icon) + esc(x.name.replace(/ \(.*\)$/, "")) + "</a>").join("") + "</div>";
}
/* the "More" menu closes on a tap outside it or on Escape */
document.addEventListener("click", e => { document.querySelectorAll("details.navmore[open]").forEach(d => { if (!d.contains(e.target) || e.target.closest(".navmenu a")) d.open = false; }); });
document.addEventListener("keydown", e => { if (e.key !== "Escape") return; document.querySelectorAll("details.navmore[open]").forEach(d => { d.open = false; d.querySelector("summary").focus(); }); });
/* ---------- Figures (official statistics) ---------- */
const GEO_LABEL = { global: "World", europe: "Europe (EUDA)", greece: "Greece", us: "United States" };
// Whose figures a reader sees first: their own country's, then the world's, then their region's (the EU drugs agency
// reports for the EU countries, Norway and Türkiye); other places come last, under their own heading.
const GEO_COUNTRY = { greece: "Greece", us: "United States of America" };
const EUDA_AREA = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands (Kingdom of the)", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden", "Norway", "Türkiye"];
const GEO_ORDER = ["global", "europe", "greece", "us"];
function figRank(file) {
  if (GEO_COUNTRY[file] && GEO_COUNTRY[file] === PREF_COUNTRY) return 0;
  if (file === "global") return 1;
  if (file === "europe" && EUDA_AREA.includes(PREF_COUNTRY)) return 2;
  return 3;
}
// the place is shown beside each figure, so a survey's name ("..., Greek general population survey") is not repeated
function figYear(r) { const y = String(r.data_year).split(" (")[0]; return /^not stated/.test(y) ? "year not stated" : y; }
// what a figure counts: its own label, or its definition without the notes in brackets and after the first semicolon
const figNoPar = t => { let x = String(t || ""); for (let i = 0; i < 3; i++) x = x.replace(/\s*\([^()]*\)/g, ""); return x; };
function figLabel(r) {
  let t = (r.label || figNoPar(r.def).split(/; /)[0]).replace(/, (Greek|EU|European) general population survey$/, "").replace(/\b(lsd|mdma|ghb|gbl|thc|hhc|dmt|pcp|cbd)\b/g, x => x.toUpperCase());
  // a survey's name for a diagnosis, said plainly; the instrument stays named (glossary: "Dependence and use disorder")
  const m = !r.label && t.match(/^Past-year substance use disorder for (.+)$/i);
  if (m) t = "Had a use disorder for " + m[1] + " in the past year" + (/DSM-5/.test(String(r.def)) ? " (DSM-5)" : "");
  return t;
}
// one figure, each fact said once (senior author, 6 November: a web-survey figure named its survey, its period and its
// population twice over): the survey's name is dropped from the label when the place says it, the period note when the
// label says it, and the population when it repeats the label; "not applicable" populations and empty ones are not shown
const WEB_SURVEY = / \(European Web Survey on Drugs\)$/;
function figParts(r) {
  let what = figLabel(r), place = r.geography === "global" ? "Worldwide" : String(r.geography || ""), pop = String(r.population || "");
  const web = WEB_SURVEY.test(place);
  if (web) { place = place.replace(WEB_SURVEY, "") + ", online survey"; what = what.replace(/, European Web Survey on Drugs \d{4}/, ""); }
  if (/non-representative/.test(pop)) pop = "not a random sample";
  else if (/^not applicable|^$/.test(pop)) pop = "";
  const said = t => what.toLowerCase().includes(t);
  if (said("average")) place = place.replace(/ \(average\)$/, "");
  if (said("espad")) place = place.replace(/^ESPAD participating countries/, "ESPAD countries");
  const period = r.measure === "past-year-prevalence" ? (said("last 12 months") || said("last year") || said("last-year") || said("past year") || said("past-year") ? "" : "use in the last 12 months") :
    r.measure === "past-month-prevalence" ? (said("last 30 days") || said("last month") ? "" : "use in the last 30 days") : r.measure === "lifetime-prevalence" ? (said("ever") || said("lifetime") ? "" : "ever used") : "";
  return { what, place, pop, period };
}
/* ---------- Statistics (site 2.4, 15 November 2026; the senior author: the page "is heavy for the eye", "could be more
   understandable clear and simple at first glance"). The page is a menu of places (the reader's own country first); one
   opens at a time. Inside a place the figures stand under plain headings by what they count (people who use, people with a use disorder,
   hospital emergencies, treatment, deaths, seizures and the market, other), a drug can be chosen, and where three or more drugs were counted the same way
   (the same measure, year, people and place) they are drawn side by side as bars: like with like, at a glance. Each figure
   says its number in everyday words ("316 million people", "1 in 12"), then what it counts, then a quiet line of where,
   when and who; its source and the place in the source it was checked against are one tap away. No number is rounded:
   thousands become millions only by moving the point. ---------- */
let numbersDrawn = false;
function showNumbers(part, o) {
  const page = document.getElementById("num-page"); if (!page) return;
  const go = () => secGo(page, "numbers", part || "", o);
  if (numbersDrawn) { go(); return; }
  whenReady(loadFigures, document.getElementById("num-list") || page, "The figures", () => { numbersDrawn = true; renderNumbers(); go(); });
}
const FIG_KINDS = [["use", "How many people use it"], ["disorder", "How many people have a use disorder"], ["harm", "Hospital emergencies"], ["treat", "Treatment"], ["death", "Deaths"], ["supply", "Seizures and the drug market"], ["other", "Other figures"]];
function figKind(r) {
  if (/prevalence$/.test(r.measure)) return "use";
  if (r.measure === "treatment-entries") return "treat";
  if (r.measure === "deaths") return "death";
  if (r.measure === "seizures") return "supply";
  const d = String(r.def || "").toLowerCase(), u = String(r.unit || "").toLowerCase();
  if (/death|mortalit|years of life lost/.test(d + " " + u)) return "death";
  if (/drug-toxicity presentations|emergency (department|room|visit)|hospital (emergenc|presentation)/.test(d)) return "harm";
  if (/treatment|clients|agonist/.test(d)) return "treat";
  if (/purity|potency|price|tablet|production|laborator|seiz|offence|new psychoactive|substances (first )?(reported|detected|monitored)|\bthc\b|market/.test(d + " " + u)) return "supply";
  if (/^substances\b/.test(u)) return "supply";   // how many new drugs the warning systems have named
  if (/syringe/.test(d)) return "other";   // what was found in used syringes: not a count of people
  if (/use disorder|dependen/.test(d)) return "disorder";   // a diagnosis, not use: counted apart
  if (/\b(use|used|users|using|drinking|smok|inject)/.test(d)) return "use";
  return "other";
}
// A figure's number in everyday words, never rounded: { v: "316 million", u: "people" }. The data's units are the sources'
// own ("million persons", "one in N", "per 1 000 population", "persons (approximate: 'around 1 000')"); here they are said
// plainly. What the source's words add to a number is kept in front of it ("About 1,000", "More than 100", "Less than 1%",
// "Almost 4,100", "Half"); thousands become millions, or whole numbers, only by moving the point.
function figVal(r) {
  const f = x => x.toLocaleString("en-GB", { maximumFractionDigits: 6 });
  let u = String(r.unit || "");
  if (typeof r.value !== "number") return { v: String(r.value), u: u === "percent" ? "" : u };
  let pre = "";
  const q = u.match(/\s*\((?:(approximate|lower bound|upper bound): )?'([^']*)'\)\s*$/);
  if (q) { u = u.slice(0, q.index); const w = q[2].toLowerCase();
    if (/^half\b/.test(w) && r.value === 50) return { v: "Half", u: "" };
    pre = /^(almost|nearly)\b/.test(w) ? "Almost " : /^(over|more than)\b/.test(w) || q[1] === "lower bound" ? "More than " : /^(less than|under|fewer than)\b/.test(w) || q[1] === "upper bound" ? "Less than " : q[1] === "approximate" || /^(around|about|approximately|roughly)\b/.test(w) ? "About " : ""; }
  u = u.replace(/\s*\(unit word[^)]*\)/, "").replace(/\bpersons\b/g, "people").replace(/\bpopulation\b/g, "people").replace(/(\d) (\d{3})\b/g, "$1,$2").trim();
  if (u === "percent") return { v: pre + f(r.value) + "%", u: "" };
  if (/^percent change\b/.test(u)) return { v: (r.value > 0 ? "+" : r.value < 0 ? "\u2212" : "") + f(Math.abs(r.value)) + "%", u: "" };   // a rise or a fall: the line under it says of what, and between which years
  let m = u.match(/^percent (.+)$/); if (m) return { v: pre + f(r.value) + "%", u: m[1] };   // "24.6% THC"
  if (u === "one in N") return { v: "1 in " + f(r.value), u: "" };
  m = u.match(/^(thousand|million|billion) (.+)$/);
  if (m && m[1] === "thousand") return r.value >= 1000 ? { v: pre + f(r.value / 1000) + " million", u: m[2] } : { v: pre + f(Math.round(r.value * 1000)), u: m[2] };
  if (m) return { v: pre + f(r.value) + " " + m[1], u: m[2] };
  return { v: pre + f(r.value), u };
}
// who was counted, in a few words (the source's full wording is one tap away, with the source)
const figPop = t => { const x = figNoPar(t).replace(/^persons aged /, "ages ").replace(/^people aged /, "ages ").replace(/^population aged /, "ages ").replace(/^adults /, "adults, ages ").replace(/^young adults /, "young adults, ages ").trim(); return /^(general )?population$/.test(x) ? "" : x; };
const figSrc = r => { const ref = refById[r.source]; return ref ? (ref.author[0].short || ref.author[0].literal || ref.author[0].family) + ", " + year(ref) : r.source; };
/* One figure. Top to bottom: the drug (when the list holds several), the number in everyday words, what it counts, a quiet
   line of where, when and who, and the source, which opens to its link, the place in it the number was checked against
   and the source's full wording of who was counted. A caption written to follow its number ("of EU adults used cannabis
   in the last year") keeps its small first letter and reads on from the number. */
function figRow2(r, oneDrug) {
  const f = figParts(r), v = figVal(r), cont = /^[a-z]/.test(f.what);
  let unit = v.u;
  if (unit === "people" && r.measure === "deaths") unit = "deaths";
  if ((unit === "people" && (cont || /^(people|persons|americans)\b/i.test(f.what))) || (unit === "deaths" && cont && /death/.test(f.what))) unit = "";   // the caption says what is counted
  const what = cont ? f.what : f.what.charAt(0).toUpperCase() + f.what.slice(1), pop = f.pop ? figPop(f.pop) : "";
  const iv = r.interval && r.interval.low != null ? '<span class="f2-r">' + (/national estimates/.test(r.interval.type || "") ? "Range across countries: " : /as reported/.test(r.interval.type || "") ? "Range as reported: " : "Range: ") + esc(r.interval.low + "–" + r.interval.high) + (r.unit === "percent" ? "%" : "") + "</span>" : "";
  return '<div class="fig2"><div class="f2-n">' + (oneDrug ? "" : '<p class="f2-d">' + esc(r.substance.charAt(0).toUpperCase() + r.substance.slice(1)) + "</p>") + '<p class="f2-v num">' + esc(v.v) + (unit ? ' <span class="f2-u">' + esc(unit) + "</span>" : "") + iv + '</p></div><div class="f2-w"><p class="f2-t">' + esc(what) + (f.period ? ' <span class="muted">(' + esc(f.period) + ")</span>" : "") + "</p>" +
    '<p class="f2-m">' + esc(f.place) + " · " + esc(figYear(r)) + (pop ? " · " + esc(pop) : "") + "</p>" +
    '<details class="f2-src"><summary>' + esc(figSrc(r)) + '</summary><p><a href="' + esc(r.url) + '" target="_blank" rel="noopener">Open the source</a>' + (r.where ? ". " + esc((r.verified_on ? "Checked " + dcDate(r.verified_on) + " against: " : "Checked against: ") + r.where) : "") +
    (f.pop && (!pop || figNoPar(f.pop).trim() !== f.pop.trim()) ? (r.where && !/[.!?]["”']?$/.test(r.where) ? "." : "") + " Counted among: " + esc(f.pop) + "." : "") + "</p></details></div></div>";
}
// Three or more drugs counted the same way, side by side (like with like): one block per such set, the largest sets first.
// Where the same people were counted once as a share and once as a number, the share is drawn (it can be compared between
// places); totals ("any drug") stay out, so that no bar holds the others.
function figBars(rows, kind) {
  const sets = {}, base = r => [r.measure, figYear(r), r.population, r.geography].join("|");
  rows.forEach(r => { if (typeof r.value !== "number" || /^any /.test(r.substance) || (kind === "use" && !/prevalence$/.test(r.measure))) return;
    const k = base(r) + "|" + r.unit; (sets[k] = sets[k] || []).push(r); });
  let list = Object.values(sets).map(xs => { const seen = new Set(); return xs.slice().sort((a, b) => b.value - a.value).filter(r => !seen.has(r.substance) && seen.add(r.substance)); }).filter(xs => xs.length >= 3);
  list = list.filter(xs => xs[0].unit === "percent" || !list.some(ys => ys !== xs && ys[0].unit === "percent" && base(ys[0]) === base(xs[0])));
  return list.sort((a, b) => b.length - a.length).slice(0, 3).map(xs => {
      const r0 = xs[0], f = figParts(r0), max = xs[0].value || 1;
      const what = kind === "disorder" ? "Had a use disorder" + (xs.every(r => /^past-year/i.test(String(r.def || ""))) ? " in the last 12 months" : "")
        : r0.measure === "past-year-prevalence" ? "Used in the last 12 months" : r0.measure === "past-month-prevalence" ? "Used in the last 30 days" : "Ever used";
      return '<figure class="fbars"><figcaption><b>' + what + "</b> · " + esc(f.place) + ", " + esc(figYear(r0)) + (f.pop && figPop(f.pop) ? " · " + esc(figPop(f.pop)) : "") + '</figcaption><ul class="fb-l">' +
        xs.map(r => { const v = figVal(r); return '<li><span class="fb-n">' + esc(r.substance.charAt(0).toUpperCase() + r.substance.slice(1)) + '</span><span class="fb-b"><i style="width:' + Math.max(1.5, 100 * r.value / max).toFixed(1) + '%"></i></span><span class="fb-v num">' + esc(v.v) + "</span></li>"; }).join("") +
        '</ul><p class="fb-s">' + esc(figSrc(r0)) + (r0.unit === "percent" ? " · share of people" : " · numbers of " + esc(figVal(r0).u || r0.unit)) + "</p></figure>"; }).join("");
}
const NUM_SUB = {};   // the drug chosen in each place
function numPlaceHtml(g) {
  const all = EPI_ALL.filter(r => r.file === g && r.status === "verified"), sub = NUM_SUB[g] || "", rows = all.filter(r => !sub || r.substance === sub);
  const counts = {}; all.forEach(r => { counts[r.substance] = (counts[r.substance] || 0) + 1; });
  const subs = Object.keys(counts).sort((a, b) => a.localeCompare(b));
  const pick = subs.length > 3 ? '<p class="num-pick"><label for="num-sub-' + g + '">Show</label> <select id="num-sub-' + g + '" data-num-geo="' + g + '"><option value="">All drugs (' + all.length + " figures)</option>" +
    subs.map(x => '<option value="' + esc(x) + '"' + (x === sub ? " selected" : "") + ">" + esc(x.charAt(0).toUpperCase() + x.slice(1)) + " (" + counts[x] + ")</option>").join("") + "</select></p>" : "";
  const body = FIG_KINDS.map(([k, name]) => { const xs = rows.filter(r => figKind(r) === k); if (!xs.length) return "";
    const first = xs.slice(0, 8), rest = xs.slice(8), id = "num-more-" + g + "-" + k;
    return '<h3 class="tp">' + name + ' <span class="tp-n">' + xs.length + (xs.length === 1 ? " figure" : " figures") + "</span></h3>" + (k === "use" || k === "disorder" ? figBars(xs, k) : "") + '<div class="figs2">' + first.map(r => figRow2(r, !!sub)).join("") + "</div>" +
      (rest.length ? '<div class="figs2" id="' + id + '" hidden>' + rest.map(r => figRow2(r, !!sub)).join("") + '</div><button type="button" class="morebtn" data-more="' + id + '">' + rest.length + " more figure" + (rest.length === 1 ? "" : "s") + "</button>" : ""); }).join("");
  return pick + (body || '<p class="note">No figures for this choice.</p>');
}
function renderNumbers() {
  const page = document.getElementById("num-page"); if (!page) return;
  const geos = GEO_ORDER.filter(g => EPI_ALL.some(r => r.file === g && r.status === "verified")).sort((a, b) => figRank(a) - figRank(b) || GEO_ORDER.indexOf(a) - GEO_ORDER.indexOf(b));
  const NAME = { global: "The world", europe: "Europe", greece: "Greece", us: "United States" };
  const secs = geos.map(g => { const rows = EPI_ALL.filter(r => r.file === g && r.status === "verified"), who = [...new Set(rows.map(r => figSrc(r).replace(/, [^,]*$/, "")))];
    return { id: "n-" + g, name: NAME[g] || GEO_LABEL[g], chip: NAME[g] || GEO_LABEL[g], icon: g === "global" ? "globe" : "pin", n: rows.length + " figures", line: "From " + who.slice(0, 3).join(", ") + (who.length > 3 ? " and others" : ""), body: "" }; });
  page.innerHTML = secPageHtml("Statistics", secs, "secmenu-num");
  // a place is drawn the first time it is opened (Europe alone has close to 200 figures)
  geos.forEach(g => { const sec = document.getElementById("n-" + g); if (!sec) return; sec.dataset.lazy = "num-" + g; SEC_LAZY["num-" + g] = el => { el.querySelector(".sec-b").innerHTML = numPlaceHtml(g); }; });
}
document.addEventListener("change", e => { const sel = e.target.closest && e.target.closest("select[data-num-geo]"); if (!sel) return;
  const g = sel.dataset.numGeo, sec = document.getElementById("n-" + g); NUM_SUB[g] = sel.value; if (sec) { sec.querySelector(".sec-b").innerHTML = numPlaceHtml(g); const s2 = document.getElementById("num-sub-" + g); if (s2) s2.focus(); } });

/* ---------- Glossary ---------- */
/* The glossary (site 2.4; the senior author: "ALL pages should have an easy display ... click the clear titles ... the content
   should appear and if they click on another title the previous one closes"). It was every term's full text one under the
   other, some 16,000 pixels on a phone. Now each term is a row with its one-line meaning, from A to Z; a tap opens the full
   definition and its source, and the one open before it closes: the question cards of the drug pages, used here too. A
   term keeps its address (#g-<number in the data>), whatever its place in the list. */
function renderGlossary() {
  const order = GLOSSARY.map((g, i) => i).sort((a, b) => GLOSSARY[a].term.localeCompare(GLOSSARY[b].term, "en", { sensitivity: "base" }));
  document.getElementById("glossary-list").innerHTML = order.map(i => { const g = GLOSSARY[i];
    return '<details class="ask gterm" id="g-' + i + '" data-text="' + esc(norm(g.term + " " + (g.short || "") + " " + g.def)) + '"><summary><span class="ask-h"><span class="ask-q">' + esc(g.term) + "</span>" + (g.short ? '<span class="ask-s">' + esc(g.short) + "</span>" : "") + '</span><span class="ask-i" aria-hidden="true"></span></summary><div class="ask-a"><p>' + esc(g.def) + '</p><p class="gsrc">Source: ' + esc(g.source) + (g.ref ? " " + cite(g.ref) : "") + "</p></div></details>"; }).join("");
  const f = document.getElementById("gloss-filter");
  if (f && !f.dataset.wired) { f.dataset.wired = "1"; f.addEventListener("input", () => { const q = norm(f.value); let n = 0; document.querySelectorAll("#glossary-list .gterm").forEach(el => { const show = !q || q.split(" ").every(w => wordStart(el.dataset.text, w)); el.hidden = !show; if (show) n++; }); document.getElementById("gloss-count").textContent = q ? n + " of " + GLOSSARY.length + " terms" : ""; }); }
}

/* ---------- Interactions ---------- */
// Mixing claims (substance "interactions") carry a "pair" key ("ClassA|ClassB"); a cell is answered once it has a shown claim.
// a drug page's own mixing claim (for example methamphetamine with alcohol) also carries a pair key and shows here too
const MIX = () => CLAIMS.filter(c => c.pair);
const pairKey = (a, b) => INTERACTION_TOPICS[a + "|" + b] !== undefined || MIX().some(c => c.pair === a + "|" + b) ? a + "|" + b : b + "|" + a;
function renderInteractions() {
  const names = CLASSES.map(c => c.name).concat(["Prescribed medicines"]);
  const topic = (a, b) => INTERACTION_TOPICS[a + "|" + b] || INTERACTION_TOPICS[b + "|" + a] || "";
  const mix = MIX(), byPair = {};
  mix.forEach(c => (byPair[c.pair] = byPair[c.pair] || []).push(c));
  const cellFor = (a, b) => byPair[a + "|" + b] || byPair[b + "|" + a] || null;
  let h = '<table class="matrix"><thead><tr><th></th>' + names.map(n => "<th><span>" + esc(n) + "</span></th>").join("") + "</tr></thead><tbody>";
  names.forEach((r, i) => { h += "<tr><th>" + esc(r) + "</th>" + names.map((c, j) => { if (j < i) return '<td class="mirror"></td>'; const ans = cellFor(r, c), t = topic(r, c);
    if (ans) return '<td class="answered" title="' + esc(t) + '"><a href="#mix-' + esc(pairKey(r, c).replace("|", "--").replace(/ /g, "_")) + '" aria-label="' + esc(r + " with " + c + ": see the answer") + '">●</a></td>';
    return '<td class="' + (t ? "planned" : "na") + '" title="' + esc(t || "Not yet assessed") + '">' + (t ? "?" : "·") + "</td>"; }).join("") + "</tr>"; });
  document.getElementById("matrix").innerHTML = h + "</tbody></table>";
  const answered = Object.keys(byPair);
  document.getElementById("matrix-status").innerHTML = (answered.length ? "<b>" + answered.length + (answered.length === 1 ? " pair answered so far" : " pairs answered so far") + "</b> (marked ●; tap one to jump to its answer). " : "<b>Nothing here has been rated yet.</b> ") + "A ? marks a pair whose question is set, a · one not yet planned.";
  // answers first, each with its question, the short answer and the full evidence on this page
  const ans = answered.map(k => { const [a, b] = k.split("|"); const q = INTERACTION_TOPICS[k] || INTERACTION_TOPICS[b + "|" + a] || "";
    return '<section class="mixpair" id="mix-' + esc(k.replace("|", "--").replace(/ /g, "_")) + '"><h2>' + esc(a) + " × " + esc(b) + "</h2>" + (q ? '<p class="muted">' + esc(q) + "</p>" : "") +
      // the full evidence is drawn when its fold is first opened, once the answer's file has arrived (speed, 13 November)
      byPair[k].map(c => qaHtml(c, questionFor("interactions", c.id) || (SIMPLE.claims || {})[c.id] && SIMPLE.claims[c.id].short || claimText(c)) + '<details class="mixfull" data-full="' + esc(c.id) + '"><summary>Full evidence for this answer</summary><div class="mixfull-b"></div></details>').join("") + "</section>"; }).join("");
  const keys = Object.keys(INTERACTION_TOPICS).filter(k => !byPair[k]);
  document.getElementById("matrix-answers").innerHTML = ans;
  renderMix2();
  document.getElementById("matrix-topics").innerHTML = "<h2>" + (answered.length ? "Questions still being read" : "The questions the cells will answer") + "</h2><ol>" + keys.map(k => "<li><b>" + esc(k.replace("|", " × ")) + "</b> — " + esc(INTERACTION_TOPICS[k]) + "</li>").join("") + "</ol>";
}
document.addEventListener("toggle", e => {
  const d = e.target; if (!d.matches || !d.matches("details.mixfull[data-full][open]") || d.dataset.drawn) return;
  const c = claimById[d.dataset.full], box = d.querySelector(".mixfull-b"); if (!c || !box) return;
  whenReady(() => needFull([c.id]), box, "The full evidence", () => {
    d.dataset.drawn = "1"; box.innerHTML = claimHtml(c);
    box.querySelectorAll("[data-toggle]").forEach(b => b.addEventListener("click", () => { const el = document.getElementById(b.dataset.toggle); el.hidden = !el.hidden; }));
    box.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
    box.querySelectorAll("[data-report]").forEach(b => b.addEventListener("click", () => openReport(b.dataset.report)));
  });
}, true);

/* ---------- The law in every country: the UN treaty layer for all, national rows where checked ---------- */
const CTRY_DISPLAY = { "Naoero": "Nauru", "Republic of Korea": "South Korea (Republic of Korea)", "Democratic People's Republic of Korea": "North Korea (Democratic People's Republic of Korea)",
  "Lao People's Democratic Republic": "Laos (Lao People's Democratic Republic)", "Syrian Arab Republic": "Syria (Syrian Arab Republic)", "Russian Federation": "Russia (Russian Federation)",
  "Republic of Moldova": "Moldova (Republic of Moldova)", "United Republic of Tanzania": "Tanzania (United Republic of Tanzania)", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
  "United States of America": "United States", "Netherlands (Kingdom of the)": "Netherlands", "Czech Republic": "Czechia (Czech Republic)", "Brunei Darussalam": "Brunei (Brunei Darussalam)",
  "Bahamas (The)": "Bahamas", "State of Palestine": "Palestine (State of Palestine)", "Iran (Islamic Republic of)": "Iran", "Venezuela (Bolivarian Republic of)": "Venezuela",
  "Bolivia (Plurinational State of)": "Bolivia", "Micronesia (Federated States of)": "Micronesia", "Gambia (Republic of The)": "Gambia" };
const ctryName = n => CTRY_DISPLAY[n] || n;
const WL_COUNTRIES = WORLD_LAW.countries.filter(c => c.name !== "European Union").slice().sort((a, b) => ctryName(a.name).localeCompare(ctryName(b.name)));
const CONV = { c1961: { name: "1961 Single Convention on Narcotic Drugs", src: "VI-18" }, c1971: { name: "1971 Convention on Psychotropic Substances", src: "VI-16" }, c1988: { name: "1988 Convention against Illicit Traffic", src: "VI-19" } };
// which of the two scheduling treaties list at least one of this page's drugs (from the UN rows of the law section)
// a drug's law rows come with its file (speed): until then the page knows only that they exist, and how many
const legalReady = slug => { const L = LEGAL.find(x => x.substance === slug); return !L || !!L.entries; };
function unConvsFor(slug) {
  const L = LEGAL.find(x => x.substance === slug); if (!L) return null;
  const t = (L.entries || []).filter(e => /United Nations/.test(e.jurisdiction)).map(e => e.status).join(" | ");
  const out = [];
  if (/Schedules? [IVX]+(?: and [IVX]+)? of the Single Convention/.test(t)) out.push("c1961");
  if (/Schedules? [IVX]+(?: and [IVX]+)? of the Convention on Psychotropic Substances/.test(t)) out.push("c1971");
  return out;
}
let PREF_COUNTRY = (() => { try { return localStorage.getItem("pk-country") || ""; } catch (e) { return ""; } })();
function treatyLine(c, k) {
  const s = c[k], cv = CONV[k], src = srcIcons([WORLD_LAW.sources[cv.src].ref]);
  if (s.status === "party") return '<li class="tl yes">' + icon("check") + "<span>Party to the " + esc(cv.name) + (k === "c1961" && s.text === "unamended only" ? " (in its original 1961 text)" : "") + " since " + esc(String(s.date).slice(0, 4)) + ". " + src + "</span></li>";
  if (s.status === "signatory") return '<li class="tl part">' + icon("alert") + "<span>Signed the " + esc(cv.name) + " in " + esc(String(s.date).slice(0, 4)) + " but has not ratified it. " + src + "</span></li>";
  return '<li class="tl no">' + icon("x") + "<span>Not a party to the " + esc(cv.name) + ". " + src + "</span></li>";
}
function natRows(slug, unName) {
  const L = LEGAL.find(x => x.substance === slug); if (!L) return [];
  const want = norm(ctryName(unName)), want2 = norm(unName);
  // a "not found" from a reading that could not cover every list stays in the full table, but the picker does not show it,
  // so that a gap in our reading is never read as "not controlled"
  return (L.entries || []).filter(e => { const j = norm(e.jurisdiction); return (j === want || j === want2) && !(e.verification === "draft" && /^([^:]{1,60}: )?Not (found|confirmed)/.test(e.status)); });
}
const LAW_VER = { "ai-checked": "checked by a second AI reader", draft: "one AI reading, not checked yet", verified: "checked by our editor" };
function countryOut(slug, unName) {
  const c = WORLD_LAW.countries.find(x => x.name === unName); if (!c) return "";
  const convs = unConvsFor(slug) || [], rows = natRows(slug, unName), nm = esc(ctryName(unName));
  let h = '<p class="ctry-h">' + nm + "</p>";
  if (convs.length) h += '<ul class="tlist">' + convs.map(k => treatyLine(c, k)).join("") + '</ul><p class="small muted">Countries that are parties agree to control the drugs these treaties list. Each country\'s own law sets the rules, the penalties and any medical use.</p>';
  else h += '<p class="small">The UN drug treaties do not list this drug, so each country\'s own law decides.</p>';
  // when every row was read on the same day and checked the same way, that is said once under the list, not on each row
  const how = e => dcDate(e.checked_on) + "|" + (LAW_VER[e.verification] || e.verification), same = rows.length && rows.every(e => how(e) === how(rows[0]));
  h += rows.length ? '<p class="ctry-k">Its own law</p><ul class="law">' + rows.map(e => "<li><b>" + esc(e.status) + '</b><span><a href="' + esc(e.source_url) + '" target="_blank" rel="noopener">' + esc(String(e.instrument).split(/[,:(]/)[0]) + "</a>" + (same ? "" : " · read " + esc(dcDate(e.checked_on)) + " · " + esc(LAW_VER[e.verification] || e.verification)) + "</span></li>").join("") + "</ul>" +
      (same ? '<p class="small muted">Read on ' + esc(dcDate(rows[0].checked_on)) + ", " + esc(LAW_VER[rows[0].verification] || rows[0].verification) + ".</p>" : "")
    : '<p class="small muted">Its own law for this drug is not on this site yet. We add a country\'s law only after reading its official text.</p>';
  return h;
}
/* ---------- Country picker: the whole list opens under a country box, and typing narrows it (drug checking, emergency
   numbers, treaties), so nobody has to guess how a country is spelled ---------- */
function countryPicker(inputId, items, onPick) {
  const f = document.getElementById(inputId); if (!f || f.dataset.picker) return;
  f.dataset.picker = "1";
  const ul = document.createElement("ul"); ul.className = "cpick"; ul.id = inputId + "-pick"; ul.setAttribute("role", "listbox"); ul.setAttribute("aria-label", "Countries"); ul.hidden = true;
  (f.closest("p") || f).after(ul);
  f.setAttribute("role", "combobox"); f.setAttribute("aria-autocomplete", "list"); f.setAttribute("aria-expanded", "false"); f.setAttribute("aria-controls", ul.id);
  let act = -1, hits = [], picking = false;
  const render = () => {
    const q = norm(f.value);
    hits = items.filter(it => !q || it.k.split(" ").some(w => w.startsWith(q)) || it.k.includes(q));
    ul.innerHTML = hits.length ? hits.map((it, i) => '<li role="option" id="' + ul.id + "-" + i + '" data-i="' + i + '"' + (i === act ? ' aria-selected="true" class="on"' : "") + "><span>" + esc(it.name) + "</span>" + (it.note ? '<span class="cp-note">' + esc(it.note) + "</span>" : "") + "</li>").join("") : '<li class="none">No country by that name. Try its name in English.</li>';
    ul.hidden = false; f.setAttribute("aria-expanded", "true");
    if (act >= 0) { f.setAttribute("aria-activedescendant", ul.id + "-" + act); const li = document.getElementById(ul.id + "-" + act); if (li) li.scrollIntoView({ block: "nearest" }); } else f.removeAttribute("aria-activedescendant");
  };
  const close = () => { ul.hidden = true; f.setAttribute("aria-expanded", "false"); f.removeAttribute("aria-activedescendant"); act = -1; };
  const pick = it => { picking = true; f.value = it.name; f.dispatchEvent(new Event("input")); picking = false; close(); onPick(it.name); };
  f.addEventListener("focus", () => { act = -1; render(); });
  f.addEventListener("input", () => { if (picking) return; act = -1; if (document.activeElement === f) render(); });
  f.addEventListener("keydown", e => {
    if (e.key === "ArrowDown") { e.preventDefault(); if (ul.hidden) render(); act = Math.min(act + 1, hits.length - 1); render(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); act = Math.max(act - 1, 0); render(); }
    else if (e.key === "Enter") { const it = hits[act >= 0 ? act : 0]; if (it && !ul.hidden) { e.preventDefault(); pick(it); } }
    else if (e.key === "Escape") close();
  });
  ul.addEventListener("mousedown", e => { const li = e.target.closest("li[data-i]"); if (!li) return; e.preventDefault(); pick(hits[+li.dataset.i]); });
  document.addEventListener("click", e => { if (e.target !== f && !ul.contains(e.target)) close(); });
}
// a country chosen in the main search opens its page already narrowed to that country (#checking/c-Greece)
function openCountry(view, name) {
  const id = { emergency: "em-filter", checking: "dc-filter", law: "law-filter" }[view], f = document.getElementById(id); if (!f) return;
  const fold = f.closest("details"); if (fold) fold.open = true;
  f.value = name; f.dispatchEvent(new Event("input"));
  const v = document.getElementById("view-" + view), el = v && v.querySelector('[data-c="' + CSS.escape(name) + '"]');
  setTimeout(() => scrollToEl((el || f)), 30);
}
function renderLaw() {
  const tb = document.getElementById("law-list"); if (!tb) return;
  const cell = (c, k) => { const s = c[k]; if (!s) return "<td>·</td>"; return s.status === "party" ? '<td class="yes">' + icon("check") + esc(String(s.date).slice(0, 4)) + (k === "c1961" && s.text === "unamended only" ? " (1961 text)" : "") + "</td>" : s.status === "signatory" ? '<td class="part">signed ' + esc(String(s.date).slice(0, 4)) + ", not ratified</td>" : '<td class="no">not a party</td>'; };
  const all = WL_COUNTRIES.concat(WORLD_LAW.countries.filter(c => c.name === "European Union"));
  tb.innerHTML = all.map(c => '<tr data-c="' + esc(ctryName(c.name)) + '" data-k="' + esc(norm(c.name + " " + ctryName(c.name))) + '"><th scope="row">' + esc(ctryName(c.name)) + (c.name === "European Union" ? ' <span class="muted small">(not a country)</span>' : "") + "</th>" + cell(c, "c1961") + cell(c, "c1971") + cell(c, "c1988") + "</tr>").join("");
  const n = k => WORLD_LAW.countries.filter(c => c[k].status === "party").length;
  document.getElementById("law-sum").innerHTML = n("c1961") + " members for the 1961 treaty, " + n("c1971") + " for the 1971 treaty and " + n("c1988") + " for the 1988 treaty (one of them the European Union). Sources: " + srcIcons(["un-mtdsg_vi18", "un-mtdsg_vi15", "un-mtdsg_vi16", "un-mtdsg_vi19"]) + "; the totals agree with the International Narcotics Control Board " + srcIcons(["incb_2024"]) + ".";
  const f = document.getElementById("law-filter"), none = document.getElementById("law-none");
  f.addEventListener("input", () => { const q = norm(f.value); let shown = 0; tb.querySelectorAll("tr").forEach(tr => { const on = !q || tr.dataset.k.split(" ").some(w => w.startsWith(q)) || tr.dataset.k.includes(q); tr.hidden = !on; if (on) shown++; }); none.hidden = shown > 0; });
  countryPicker("law-filter", all.map(c => ({ name: ctryName(c.name), k: norm(c.name + " " + ctryName(c.name)) })).sort((a, b) => a.name.localeCompare(b.name)), name => openCountry("law", name));
  renderLawMine();
}
/* The treaties page starts with the reader's own country (site 2.4): three plain lines, one for each treaty, in place of a
   table of some 200 rows; the table of all countries is one tap away, with its filter. */
const LAW_TREATIES = [["c1961", "1961 treaty", "Narcotic drugs"], ["c1971", "1971 treaty", "Psychotropic substances"], ["c1988", "1988 treaty", "Drug trafficking"]];
function renderLawMine() {
  const box = document.getElementById("law-mine"); if (!box) return;
  if (!PREF_COUNTRY) { box.innerHTML = countryAsk(true); return; }
  const c = WORLD_LAW.countries.find(x => x.name === PREF_COUNTRY), nm = esc(inCtry(PREF_COUNTRY));
  if (!c) { box.innerHTML = countryAsk(true) + '<p class="say">We have no treaty record for ' + nm + ". The United Nations lists its member states and a few others.</p>"; return; }
  const line = ([k, name, what]) => { const s = c[k], y = s && s.date ? esc(String(s.date).slice(0, 4)) : "";
    const st = !s ? ["no", "No record"] : s.status === "party" ? ["yes", "Joined in " + y + (k === "c1961" && s.text === "unamended only" ? " (the 1961 text only)" : "")] : s.status === "signatory" ? ["part", "Signed in " + y + ", not ratified"] : ["no", "Not a party"];
    return '<li class="lm ' + st[0] + '"><span class="lm-t"><b>' + name + '</b><span class="lm-w">' + what + '</span></span><span class="lm-s">' + (st[0] === "yes" ? icon("check") : "") + st[1] + "</span></li>"; };
  box.innerHTML = countryAsk(true) + '<ul class="lawmine">' + LAW_TREATIES.map(line).join("") + '</ul><p class="mine-note">What the law of ' + nm + " says about a drug is on that drug's page, under The law. " + srcIcons(["un-mtdsg_vi18", "un-mtdsg_vi15", "un-mtdsg_vi16", "un-mtdsg_vi19"]) + "</p>";
}

/* ---------- Drug checking: services that test a sample and tell you what is in it ---------- */
const DC_TYPE = { "fixed site": "Fixed site", events: "At events", postal: "By post", mobile: "Mobile" };
const dcDate = d => { const t = new Date(String(d) + (String(d).length === 10 ? "T12:00:00" : "")); return isNaN(t) ? String(d) : t.toLocaleDateString("en-GB", { day: /^\d{4}-\d{2}-\d{2}$/.test(d) ? "numeric" : undefined, month: "short", year: "numeric" }); };
function dcCard(s) {
  const st = s.active === "yes" ? ["", "Running"] : s.active === "closed" ? ["closed", "Closed"] : ["unclear", "Not sure it is still running"];
  return '<article class="dcs ' + st[0] + '" data-k="' + esc(norm(s.country + " " + (s.city || "") + " " + s.name)) + '"><h3><a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.name) + "</a></h3>" +
    '<p class="dcs-where">' + esc(s.city || "") + "</p>" +
    '<p class="dcs-tags">' + (s.type || []).map(t => '<span class="tagchip">' + esc(DC_TYPE[t] || t) + "</span>").join("") + (s.cost === "free" ? '<span class="tagchip">Free</span>' : s.cost === "paid" ? '<span class="tagchip">Paid</span>' : "") + "</p>" +
    (s.method ? '<p class="small">How it tests: ' + esc(s.method) + "</p>" : "") +
    '<p class="small dcs-st">' + esc(st[1]) + (s.last_sign && s.last_sign.date ? '<span class="muted"> · latest sign ' + esc(dcDate(s.last_sign.date)) + "</span>" : "") + "</p>" +
    '<p class="small muted dcs-v">' + (s.verification === "ai-checked" ? "Confirmed in two sources" : "One source so far") + " " + srcIcons((s.sources || []).map(x => x.ref)) + "</p></article>";
}
/* Look-alikes: different drugs side by side (comparing similar things mixed together teaches the difference best, most of all
   with pictures), so no one takes a look for a test */
// like with like: loose white powders together, then pills together (senior author, 18 October)
const LOOKALIKES = [["White powders", [["cocaine-powder", "Cocaine"], ["ketamine-powder", "Ketamine"], ["3mmc-powder", "3-MMC", "a synthetic cathinone"], ["heroin-white", "Heroin"]]],
  ["Pills", [["mdma-pressed-pills", "Ecstasy"], ["oxycodone-tablet", "Oxycodone", "a medicine"], ["alprazolam-tablets", "Alprazolam (Xanax)", "a medicine"]]]];
function lookalikeHtml() {
  const byId = Object.fromEntries(PHOTOS.map(p => [p.id, p]));
  const rows = LOOKALIKES.map(([k, xs]) => [k, xs.filter(x => byId[x[0]])]).filter(r => r[1].length >= 2);
  if (!rows.length) return "";
  const kit = byId["reagent-test-kit"];
  return '<section class="lookalike" aria-label="Different drugs can look the same">' +
    rows.map(([k, xs]) => '<p class="forms-k">' + esc(k) + '</p><div class="phgal">' + xs.map(([id, label, detail]) => photoFig(byId[id], "t", label, detail || null)).join("") + "</div>").join("") +
    '<p class="phnote">Looks don’t tell you what’s inside. Drug checking tests a sample. ' + phToggle() + "</p>" +
    (kit ? '<p class="forms-k">Tests named below</p><div class="phgal">' + photoFig(kit, "t") + (byId["test-strip-pouches"] ? photoFig(byId["test-strip-pouches"], "t") : "") + "</div>" : "") + "</section>";
}
function renderChecking() {
  // the page as sections (site 2.4): the template holds each part's fixed markup (#dc-parts), moved into its section here
  const page = document.getElementById("dc-page"), parts = document.getElementById("dc-parts");
  if (page && parts) {
    const nC = new Set(DRUGCHECK.services.map(x => x.country)).size, nQ = drugQuestions(DC).length, lookH = lookalikeHtml();
    const secs = [
      { id: "c-near", name: "Where can I get a drug tested?", chip: "Services", icon: "pin", n: DRUGCHECK.services.length + " services", line: "In " + nC + " countries: at an address, at events or by post" },
      { id: "c-kits", name: "Test kits to use at home", chip: "Test kits", icon: "flask", n: "", line: "Who sells them where you are, and what the law says" },
      nQ ? { id: "c-work", name: "Do home test kits work?", chip: "Do they work?", icon: "search", n: nQ + (nQ === 1 ? " answer" : " answers"), line: "What studies found when strips and colour tests were checked" } : null,
      lookH ? { id: "c-look", name: "Different drugs can look the same", chip: "Look-alikes", icon: "eye", n: "", line: "White powders and pills, side by side" } : null
    ].filter(Boolean).map(x => Object.assign(x, { body: '<div data-slot="' + x.id + '"></div>' }));
    page.innerHTML = secPageHtml("Drug checking", secs, "secmenu-dc");
    secs.forEach(x => { const slot = page.querySelector('[data-slot="' + x.id + '"]'), part = parts.querySelector('[data-part="' + x.id + '"]'); if (slot && part) slot.replaceWith(...[...part.childNodes]); });
    parts.remove();
  }
  const list = document.getElementById("dc-list"); if (!list) return;
  const look = document.getElementById("dc-look"); if (look) look.innerHTML = lookalikeHtml();
  renderDcKits();
  const by = {}; DRUGCHECK.services.forEach(s => { (by[s.country] = by[s.country] || []).push(s); });
  const order = s => (s.active === "yes" ? 0 : s.active === "closed" ? 2 : 1);
  const countries = Object.keys(by).sort((a, b) => a.localeCompare(b));
  list.innerHTML = countries.map(c => '<section class="dc-c" data-c="' + esc(c) + '"><h2>' + esc(c) + ' <span class="muted small">' + by[c].length + "</span></h2>" + by[c].slice().sort((a, b) => order(a) - order(b) || a.name.localeCompare(b.name)).map(dcCard).join("") + "</section>").join("");
  const none = DRUGCHECK.countries_searched_none_found || [];
  const svcWord = n => n + " service" + (n === 1 ? "" : "s");
  // a closed service is listed (it shows what existed) but not counted as one you can use
  const svcNote = xs => { const open = xs.filter(s => s.active !== "closed").length, shut = xs.length - open; return open ? svcWord(open) + (shut ? ", " + shut + " closed" : "") : shut + " closed, none running found"; };
  countryPicker("dc-filter", countries.map(c => ({ name: c, k: norm(c + " " + by[c].map(s => s.city || "").join(" ")), note: svcNote(by[c]) }))
    .concat(none.filter(c => !by[c]).map(c => ({ name: c, k: norm(c), note: dcReported(c) ? "only a report mentions it" : "searched, none found yet" }))).sort((a, b) => a.name.localeCompare(b.name)), name => openCountry("checking", name));
  document.getElementById("dc-note").innerHTML = esc(DRUGCHECK.services.length + " services in " + countries.length + " countries so far, read on " + dcDate(DRUGCHECK.checked_on) + (DRUGCHECK.updated_on ? ", with additions on " + dcDate(DRUGCHECK.updated_on) : "") + ". A service is listed only after we read its own page or a report that describes it; “confirmed in two sources” means an independent source agreed.") +
    (none.length ? ' <details class="srcnote"><summary>Searched with none found: ' + none.length + " countries</summary><p>" + esc(none.slice().sort((a, b) => a.localeCompare(b)).join(", ")) + ". Some were covered by one search across several countries; a service may still exist there.</p></details>" : "");
  renderDcMine();
  const f = document.getElementById("dc-filter"), nf = document.getElementById("dc-none");
  f.addEventListener("input", () => { const q = norm(f.value); let shown = 0;
    list.querySelectorAll("section.dc-c").forEach(sec => { let any = 0; sec.querySelectorAll("article.dcs").forEach(a => { const on = !q || a.dataset.k.split(" ").some(w => w.startsWith(q)) || a.dataset.k.includes(q); a.hidden = !on; if (on) any++; }); sec.hidden = !any; shown += any; });
    nf.hidden = shown > 0;
    if (!shown) { const r = (DRUGCHECK.countries_reported || []).find(x => norm(x.country) === q); nf.innerHTML = r ? esc(r.line) + " " + srcIcons(r.sources.map(x => x.ref)) : "Nothing listed there yet. We add a service only after reading its own page or a report that describes it."; } });
}

/* ---------- Emergency numbers: one alphabetical list of countries, each number with its source ---------- */
// one book icon per line, whatever the number of sources: a line with two sources no longer shows two icons side by side
function srcIcons(ids) {
  const ok = (ids || []).filter(id => refById[id]); if (!ok.length) return "";
  const r = refById[ok[0]], labels = ok.map(id => inTextLabel(refById[id], REFS));
  return '<a class="pop srcico" href="' + esc(refLink(r)) + '" target="_blank" rel="noopener" data-ref="' + esc(ok[0]) + '"' + (ok.length > 1 ? ' data-refs="' + esc(ok.join(",")) + '"' : "") + ' aria-label="' + (ok.length > 1 ? "Sources: " : "Source: ") + esc(labels.join("; ")) + '">' + icon("book") + "</a>";
}
function renderEmergency() {
  const list = document.getElementById("em-list"); if (!list) return;
  const tel = x => x.tel || x.n.replace(/\s+/g, "");
  const num = x => '<span class="em-x"><a class="em-n" href="tel:' + esc(tel(x)) + '" aria-label="Call ' + esc(x.n) + '">' + esc(x.n) + '</a><span class="em-src">' + srcIcons(x.src) + "</span></span>";
  const notes = c => c.numbers.filter(x => x.note).map(x => '<span class="em-note">' + esc(x.note) + "</span>").join("");
  list.innerHTML = EMERGENCY.countries.map(c => '<li class="em" data-c="' + esc(c.country) + '" data-k="' + esc(norm([c.country].concat(c.aka || []).join(" "))) + '"><span class="em-c">' + esc(c.country) + '</span><span class="em-nums">' + c.numbers.map(num).join("") + "</span>" + notes(c) +
    // the ambulance line, the poison centre and support lines are shown, not folded away: they are what people do not already know
    (c.more ? '<ul class="em-more">' + c.more.map(x => '<li><a class="em-n" href="tel:' + esc(tel(x)) + '" aria-label="Call ' + esc(x.n) + '">' + esc(x.n) + "</a><span>" + esc(x.what) + '</span><span class="em-src">' + srcIcons(x.src) + "</span></li>").join("") + "</ul>" : "") + "</li>").join("");
  const f = document.getElementById("em-filter"), none = document.getElementById("em-none");
  const apply = () => { const q = norm(f.value); let shown = 0; list.querySelectorAll("li.em").forEach(li => { const on = !q || li.dataset.k.split(" ").some(w => w.startsWith(q)) || li.dataset.k.includes(q); li.hidden = !on; if (on) shown++; }); none.hidden = shown > 0; };
  f.addEventListener("input", apply);
  countryPicker("em-filter", EMERGENCY.countries.map(c => ({ name: c.country, k: norm([c.country].concat(c.aka || []).join(" ")), note: c.numbers.map(x => x.n).slice(0, 2).join(" · ") })).sort((a, b) => a.name.localeCompare(b.name)), name => openCountry("emergency", name));
  renderEmMine();
  document.getElementById("em-note").textContent = EMERGENCY.countries.length + " countries so far. Every number was checked against an official source on " + EMERGENCY.checked_on_long + "; point at the book icon to see the source. A country is added only after its number has been checked.";
}

/* ---------- Search ---------- */
let INDEX = [];
/* Names from the identity section (sourced), for search and for the page header */
function identityTerms(slug) {
  const d = IDENTITY.find(x => x.substance === slug); if (!d) return [];
  const n = d.names || {}; const casNo = t => (String(t).match(/^\s*(\d{2,7}-\d{2}-\d)/) || [])[1];
  return [n.inn, ...(n.synonyms || []), ...(n.cas || []).map(casNo)]
    .concat((d.members || []).flatMap(m => [m.name, m.inn, ...(m.synonyms || []), ...(m.cas || []).map(casNo)]))
    .concat((d.street_names || []).flatMap(x => x.names)).filter(Boolean);
}
// Street names documented by at least two different sources, most often documented first (at most five)
function documentedNames(slug) {
  const d = IDENTITY.find(x => x.substance === slug); if (!d) return [];
  const by = {};
  (d.street_names || []).forEach(x => x.names.forEach(nm => { const k = nm.toLowerCase().replace(/\s*\(.*\)$/, "").trim(); if (!k || k.length > 24) return; (by[k] = by[k] || { name: nm.replace(/\s*\(.*\)$/, "").trim(), src: new Set() }); x.source_ids.forEach(i => by[k].src.add(i)); }));
  return Object.values(by).filter(v => v.src.size >= 2).sort((a, b) => b.src.size - a.src.size).slice(0, 5).map(v => v.name);
}
/* Search: names and street names first (exact, then beginning of a word, then a one- or two-letter slip), then pages,
   then findings, open questions and terms. Words match at the start of a word only, so "ice" does not find "practice". */
function norm(s) { return String(s == null ? "" : s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ς/g, "σ").replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim(); }
const EMERGENCY_TERMS = ["overdose", "od", "emergency", "help", "ambulance", "poison", "poisoning", "poisoned", "naloxone", "narcan", "112", "166", "collapsed", "collapse", "unconscious", "not breathing", "breathing", "seizure", "seizures", "fit", "fitting", "overheating", "heatstroke", "chest pain", "1031", "1145", "911", "999", "helpline", "crisis", "εκτακτο", "βοηθεια", "ασθενοφορο", "δηλητηριαση", "υπερβολικη δοση", "εκαβ"].map(norm);
function wordStart(hay, w) { let i = hay.indexOf(w); while (i >= 0) { if (i === 0 || /[\s(\-\/,.;:'"«»]/.test(hay[i - 1])) return true; i = hay.indexOf(w, i + 1); } return false; }
function buildIndex() {
  SUBSTANCES.forEach(s => {
    const prime = [s.name].concat(ALIASES[s.slug] || [], ALIASES_EL[s.slug] || []).map(norm).filter(Boolean);
    const names = prime.concat(identityTerms(s.slug).map(norm)).filter(Boolean);
    INDEX.push({ type: "drug", kind: "Drug · " + s.cls, title: s.name, prime: new Set(prime), names: [...new Set(names)], text: norm(s.cls + " " + s.mech), href: "#s-" + s.slug });
  });
  // (2.12) the pages our system started for drugs people asked about that had no page: found by their names like any drug
  if (typeof AUTO_PAGES === "object" && AUTO_PAGES) Object.keys(AUTO_PAGES).forEach(k => {
    const names = [AUTO_PAGES[k]].concat(typeof AUTO_NAMES === "object" && AUTO_NAMES ? Object.keys(AUTO_NAMES).filter(n => AUTO_NAMES[n] === k) : []).map(norm).filter(Boolean);
    INDEX.push({ type: "drug", kind: "A page our system started", title: AUTO_PAGES[k], prime: new Set(names), names: [...new Set(names)], text: "", href: "#auto/p-" + k });
  });
  const asked = buildAnswerIndex();
  CLAIMS.filter(c => !asked.has(c.id)).forEach(c => INDEX.push({ type: "claim", kind: "Finding · " + (subBySlug[c.substance] ? subBySlug[c.substance].name : c.substance), title: claimText(c), t: norm(claimText(c)), text: norm(c.statement + " " + c.outcome + " " + c.exposure), href: "#" + c.id, badge: editorApproved(c) ? "Approved" : readerStamp(c.verification.status).split(":")[0], badgeCls: editorApproved(c) ? "ok" : "draft" }));
  GLOSSARY.forEach((g, i) => INDEX.push({ type: "term", kind: "Term", title: g.term, t: norm(g.term), text: norm(g.def), href: "#g-" + i }));
  // countries: where to get drug checking, the emergency numbers, the treaties
  const dcBy = {}; DRUGCHECK.services.forEach(s => { dcBy[s.country] = (dcBy[s.country] || 0) + 1; });
  EMERGENCY.countries.forEach(c => INDEX.push({ type: "country", kind: "Emergency numbers", title: c.country, names: [c.country].concat(c.aka || []).map(norm), href: "#emergency/c-" + encodeURIComponent(c.country), order: 0 }));
  Object.keys(dcBy).forEach(c => INDEX.push({ type: "country", kind: "Drug checking · " + dcBy[c] + " service" + (dcBy[c] === 1 ? "" : "s"), title: c, names: [norm(c)], href: "#checking/c-" + encodeURIComponent(c), order: 1 }));
  WL_COUNTRIES.forEach(c => INDEX.push({ type: "country", kind: "Drug treaties", title: ctryName(c.name), names: [norm(c.name), norm(ctryName(c.name))], href: "#law/c-" + encodeURIComponent(ctryName(c.name)), order: 2 }));
  Object.keys(PLANNED_QUESTIONS).forEach(slug => PLANNED_QUESTIONS[slug].forEach(q => INDEX.push({ type: "question", kind: "Open question · " + (subBySlug[slug] ? subBySlug[slug].name : slug), title: q, t: norm(q), text: norm(slug), href: "#s-" + slug, badge: "Not answered yet", badgeCls: "planned" })));
  [["Emergency numbers, country by country", "emergency", "emergency numbers overdose ambulance help poison centre support lines 112 911 999 000"], ["Drug checking services, country by country", "checking", "drug checking pill testing testing service analysis what is in my drug test kit"], ["Drug treaties by country", "law", "law legal treaties conventions un country illegal legal status"], ["Statistics: official figures", "numbers", "statistics numbers prevalence figures euda unodc nsduh world europe countries deaths treatment seizures"], ["How to read this site", "howto", "claims certainty dots status evidence study card plain precise"], ["Is it safe to mix? What happens when drugs are combined", "interactions", "combinations mixing interactions combos opioids benzodiazepines benzos alcohol gabapentin pregabalin methadone buprenorphine"], ["Words explained", "glossary", "glossary terms definitions words meaning"], ["How we check facts", "methods", "methods protocol search risk of bias grade verification corrections"], ["About us", "about", "about who we are ai statement name pharmakon"], ["On our list", "wanted", "questions not answered yet waiting list requests asked coming soon"], ["Written by our system", "auto", "machine written automatic answers not yet checked by a person ai system new"]].forEach(p => INDEX.push({ type: "page", kind: "Page", title: p[0], t: norm(p[0]), text: norm(p[2]), href: "#" + p[1], id: p[1] }));
}
function scoreItem(it, q, words, emergency, ctx) {
  if (it.type === "answer") return [ctx ? scoreAnswer(it, ctx) : 0, false];
  if (it.type === "drug") {
    let best = 0, fuzzy = false;
    for (const n of it.names) {
      // the page's own name and the editors' list of common names rank above names found only in the sourced records
      const pr = it.prime.has(n), chem = /\d/.test(n) || n.split(" ").length > 3;
      if (n === q) { best = Math.max(best, pr ? 1100 : 1000); continue; }
      if (q.length >= 2 && n.startsWith(q)) best = Math.max(best, (pr ? 700 : 650) - Math.min(60, n.length - q.length));
      // inside a name only for common names, not inside chemical names ("acid" should not find every "…ic acid")
      else if (q.length >= 2 && !chem && wordStart(n, q)) best = Math.max(best, pr ? 500 : 450);
      else if (words.length > 1 && !chem && words.every(w => wordStart(n, w))) best = Math.max(best, 440);
    }
    if (!best && q.length >= 4) {
      // a slip of one letter (two in longer words): the closest name wins
      const lim = q.length >= 6 ? 2 : 1; let dmin = 9;
      for (const n of it.names) for (const p of [n].concat(n.split(" "))) { if (Math.abs(p.length - q.length) <= lim) dmin = Math.min(dmin, editDistance(q, p)); }
      if (dmin <= lim) { best = 300 - 60 * dmin + (it.prime.size && [...it.prime].some(p => editDistance(q, p) === dmin) ? 20 : 0); fuzzy = true; }
    }
    if (!best && q.length >= 3 && words.every(w => wordStart(it.text, w))) best = 60;
    return [best, fuzzy];
  }
  if (it.type === "country") {
    if (q.length < 3) return [0, false];
    let sc = 0; for (const n of it.names) { if (n === q) sc = Math.max(sc, 900); else if (n.startsWith(q)) sc = Math.max(sc, 600); else if (wordStart(n, q)) sc = Math.max(sc, 420); }
    return [sc ? sc - it.order : 0, false];
  }
  if (it.type === "page") {
    if (it.id === "emergency" && emergency) return [2000, false];
    if (q.length < 2) return [0, false];
    let sc = 0; if (wordStart(it.t, q)) sc = 400; else if (words.every(w => wordStart(it.t, w) || wordStart(it.text, w))) sc = 120;
    return [sc, false];
  }
  if (q.length < 2) return [0, false];
  if (it.type === "term") { if (it.t === q) return [260, false]; if (wordStart(it.t, q)) return [90, false]; }
  let sc = 0;
  // the words that carry the question ("does cannabis cause psychosis": cannabis, cause, psychosis)
  const sw = words.filter(w => !SR_STOP.has(w)); if (!sw.length) return [0, false];
  for (const w of sw) { if (w.length < 2) continue; const inT = wordStart(it.t, w), inX = wordStart(it.text, w); if (!inT && !inX) return [0, false]; sc += (inT ? 30 + (it.t.startsWith(w) ? 10 : 0) : 0) + (inX ? 5 : 0); }
  return [sc, false];
}
let searchHits = [];
// a few real questions to try: for the most-looked-up drugs, the first checked question of a topic (the ones In short shows),
// one per drug, a new set on each visit; short ones only, and none that only makes sense after another ("What about…")
let SUGGEST = null;
function suggestHtml() {
  if (!SUGGEST) {
    const ok = ([id, q]) => claimById[id] && claimById[id].verification.status !== "draft" && (SIMPLE.claims || {})[id] && q.split(" ").length <= 10 && !/^(what about|and |or |but )/i.test(q);
    SUGGEST = shuffle(POPULAR.filter(sl => subBySlug[sl]).map(sl => { const top = roundRobin(drugQuestions(sl).filter(ok)).slice(0, 3); return top.length ? { sl, x: top[Math.floor(Math.random() * top.length)] } : null; }).filter(Boolean)).slice(0, 5);
  }
  return SUGGEST.length ? '<p class="sr-hint">Try a question like these</p>' + SUGGEST.map(({ sl, x }) => '<a class="sr-ans sr-sug" href="#s-' + sl + "/q-" + esc(x[0]) + '"><span class="k">' + esc(drugName(sl)) + '</span><span class="t">' + esc(x[1]) + "</span></a>").join("") : "";
}
function runSearch(raw) {
  const box = document.getElementById("search-results"); const live = document.getElementById("search-count");
  const q = norm(raw);
  // an empty box with the cursor in it shows a few real questions to try (recognition, not recall); otherwise it closes
  if (!q) { const sug = document.activeElement === document.getElementById("search") ? suggestHtml() : ""; box.innerHTML = sug; box.hidden = !sug; if (live) live.textContent = sug ? "Some questions you can ask" : ""; insightAfterSearch(raw); return; }
  const words = q.split(" ");
  // "help" or "breathing" inside a longer question is a question, not an emergency
  const emergency = EMERGENCY_TERMS.some(e => e === q || (q.length >= 3 && e.startsWith(q)) || (e.length >= 4 && wordStart(q, e) && (words.length <= 3 || !["help", "breathing", "crisis", "helpline"].includes(e))));
  const ctx = readQuery(q);
  searchHits = INDEX.map(it => { const [sc, fz] = scoreItem(it, q, words, emergency, ctx); return { sc, fz, it }; }).filter(p => p.sc > 0).sort((a, b) => b.sc - a.sc).slice(0, 12);
  const intents = intentHits(ctx); if (intents.length) searchHits = intents.concat(searchHits.filter(p => !intents.some(x => x.it.href === p.it.href))).slice(0, 12);
  // a question about a drug we have no answer for yet: its page, and the questions still open on it
  if (ctx.drugs.length && ctx.topic.length && !searchHits.some(p => p.it.type === "answer" || p.it.type === "intent")) {
    const pages = INDEX.filter(it => it.type === "drug" && ctx.drugs.some(d => it.href === "#s-" + d)).map(it => ({ sc: 500, fz: false, it }));
    searchHits = pages.concat(searchHits.filter(p => !pages.some(x => x.it === p.it))).slice(0, 12);
  }
  // a question gets its answer first, above the drug pages ("does weed help you sleep?")
  if (ctx.topic.length && !intents.length && searchHits.length && searchHits[0].it.type !== "answer") { const i = searchHits.findIndex(p => p.it.type === "answer" && p.sc >= 140); if (i > 0 && !(searchHits[0].it.type === "page" && emergency)) searchHits.unshift(searchHits.splice(i, 1)[0]); }
  // "Best answer" only when the answer matches the question well
  const bestOk = p => p && p.it.type === "answer" && p.sc >= 150 && (ctx.topic.length > 0 || ctx.groups.length > 1);
  const row = (p, i) => {
    const it = p.it;
    if (it.type === "answer") { const c = claimById[it.id], sp = (SIMPLE.claims || {})[it.id];
      const best = i === 0 && bestOk(p);
      return '<a class="sr-ans' + (best ? " best" : "") + '" href="' + esc(answerHref(it, ctx)) + '" data-cid="' + esc(it.id) + '"><span class="k">' + esc((best ? "Best answer · " : "Answer · ") + it.where) + '</span><span class="t">' + esc(it.title) + "</span>" +
        (sp ? '<span class="a">' + esc(sp.short) + "</span>" : "") + '<span class="m">' + meterHtml(c.grade.certainty, true) + "</span></a>"; }
    return '<a href="' + esc(it.href) + '"><span class="k">' + esc(it.kind) + (p.fz ? " · closest name" : "") + '</span><span class="t">' + esc(it.title.length > 140 ? it.title.slice(0, 137) + "…" : it.title) + "</span>" + (it.badge ? '<span class="badge ' + esc(it.badgeCls || "") + '">' + esc(it.badge) + "</span>" : "") + "</a>";
  };
  const asked = String(raw).trim(), askBtn = label => '<button type="button" class="linklike" data-ask="' + esc(asked) + '">' + label + "</button>";
  box.innerHTML = searchHits.length ? searchHits.map(row).join("") + '<p class="sr-ask">Not what you were looking for? ' + askBtn("Ask us") + "</p>"
    : '<p class="none">No match for “' + esc(asked) + '”. Try other words, a drug’s name or a street name, or see <a href="#substances">all 30 drugs</a>. Need help now? <a href="#emergency">Emergency numbers</a>.</p>' +
      '<p class="sr-ask"><b>Didn’t find your question?</b> ' + askBtn("Ask us") + ".</p>";
  box.hidden = false;
  if (live) live.textContent = searchHits.length ? searchHits.length + " result" + (searchHits.length === 1 ? "" : "s") : "No results";
  insightAfterSearch(raw);   // Insight (app.insight.js): the answers that fit a question, once it is ready
}
function closeSearch() { const box = document.getElementById("search-results"); if (box) { box.hidden = true; } }
const searchInput = document.getElementById("search");
searchInput.addEventListener("input", () => runSearch(searchInput.value));
searchInput.addEventListener("focus", () => runSearch(searchInput.value));
searchInput.addEventListener("keydown", e => { if (e.key === "ArrowDown") { const f = document.querySelector("#search-results a"); if (f) { e.preventDefault(); f.focus(); } return; } if (e.key === "Enter") { const first = norm(searchInput.value) && document.querySelector("#search-results a"); if (first) { e.preventDefault(); first.click(); } } if (e.key === "Escape") { searchInput.value = ""; closeSearch(); } });
document.getElementById("search-results").addEventListener("keydown", e => { const a = e.target.closest && e.target.closest("a"); if (!a) return; const all = [...document.querySelectorAll("#search-results a")], i = all.indexOf(a); if (e.key === "ArrowDown" && all[i + 1]) { e.preventDefault(); all[i + 1].focus(); } if (e.key === "ArrowUp") { e.preventDefault(); (all[i - 1] || searchInput).focus(); } if (e.key === "Escape") { searchInput.focus(); closeSearch(); } });
document.getElementById("search-results").addEventListener("click", e => { if (e.target.closest("a")) { searchInput.value = ""; closeSearch(); } });

/* ---------- Popover ---------- */
let popEl = null, popTimer = null, popWant = null;
// a reference's full APA entry comes with data/refs.json (speed): the first time, its popover opens once that has arrived,
// unless the reader has moved on meanwhile
function refsFirst(a, show) {
  if (REFS_DONE) return false;
  popWant = a; loadRefs().then(() => { if (popWant === a && a.isConnected) { popWant = null; show(a); } }).catch(() => { popWant = null; });
  return true;
}
function showPop(a) {
  if (a.dataset.refs) return showPops(a);
  const ref = refById[a.dataset.ref]; if (!ref) return;
  if (refsFirst(a, showPop)) return;
  hidePop();
  popEl = document.createElement("div"); popEl.className = "popover"; popEl.setAttribute("role", "dialog"); popEl.dataset.for = ref.id;
  const cards = Object.keys(cardById).filter(k => cardById[k].reference === ref.id);
  const link = ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL;
  popEl.innerHTML = '<div class="refline">' + apaReference(ref) + '</div><div class="acts">' + (link ? '<a href="' + esc(link) + '" target="_blank" rel="noopener">Open ' + (ref.DOI ? "DOI" : "source") + ' ↗</a>' : "") + cards.map(k => '<button type="button" data-card="' + k + '">Study card</button>').join("") + (document.getElementById("ref-" + ref.id) ? '<a href="#ref-' + ref.id + '">Reference list</a>' : "") + '</div><div class="vline">' + esc(ref.verification.status) + (ref.verification.verified_on ? " · " + esc(META_SOURCE[String(ref.verification.metadata_source || "").split(" ")[0]] || "metadata") + " " + esc(ref.verification.verified_on) : "") + " · retraction check: " + esc(ref.verification.retraction_check ? ref.verification.retraction_check.status : "—") + (ref.verification.online_first_year ? " · online first " + ref.verification.online_first_year : "") + "</div>";
  document.body.appendChild(popEl);
  const r = a.getBoundingClientRect(); const pw = Math.min(420, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
  popEl.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => { openCard(b.dataset.card); hidePop(); }));
}
function showPops(a) {
  const refs = a.dataset.refs.split(",").map(id => refById[id]).filter(Boolean); if (!refs.length) return;
  if (refsFirst(a, showPops)) return;
  hidePop();
  popEl = document.createElement("div"); popEl.className = "popover"; popEl.setAttribute("role", "dialog"); popEl.dataset.for = a.dataset.refs;
  popEl.innerHTML = '<p class="pops-h">' + refs.length + " sources</p>" + refs.map(ref => { const link = ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL; return '<div class="refline">' + apaReference(ref) + "</div>" + (link ? '<div class="acts"><a href="' + esc(link) + '" target="_blank" rel="noopener">Open ' + (ref.DOI ? "DOI" : "source") + " ↗</a></div>" : ""); }).join("");
  document.body.appendChild(popEl);
  const r = a.getBoundingClientRect(); const pw = Math.min(420, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
}
function showGloss(btn) {
  const g = GLOSSARY[+btn.dataset.gl]; if (!g) return;
  hidePop();
  popEl = document.createElement("div"); popEl.className = "popover gloss"; popEl.setAttribute("role", "dialog"); popEl.dataset.for = "gl-" + btn.dataset.gl;
  popEl.innerHTML = "<b>" + esc(g.term) + "</b>" + (g.short ? '<p class="gshort">' + esc(g.short) + "</p>" : "") + '<p class="muted">' + esc(g.def) + '</p><div class="acts"><a href="#g-' + btn.dataset.gl + '">Words explained</a></div>';
  document.body.appendChild(popEl);
  const r = btn.getBoundingClientRect(); const pw = Math.min(360, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
}
// the sources behind a line's chip (lineSrc): the publisher, the pages read and their links. Opened from the keyboard, the
// first link takes the focus, and Escape or tabbing past the end gives it back to the chip.
function showSrcl(btn, byKey) {
  const gs = SRCL[+btn.dataset.srcl]; if (!gs) return;
  hidePop();
  popEl = document.createElement("div"); popEl.className = "popover srclpop"; popEl.setAttribute("role", "dialog"); popEl.setAttribute("aria-label", gs.length === 1 ? "Source" : "Sources"); popEl.dataset.for = "srcl-" + btn.dataset.srcl;
  popEl.innerHTML = gs.map(g => { const r = g.ref && refById[g.ref];
    return r ? '<p class="sp-pub">' + esc(inTextLabel(r, REFS)) + '</p><ul><li><a href="' + esc(refLink(r)) + '" target="_blank" rel="noopener">' + esc(String(r.title || "").replace(/<[^>]+>/g, "")) + "</a></li></ul>"
      : '<p class="sp-pub">' + esc(g.pub) + "</p><ul>" + g.pages.map(x => '<li><a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.title) + "</a></li>").join("") + "</ul>"; }).join("");
  document.body.appendChild(popEl);
  const r = btn.getBoundingClientRect(); const pw = Math.min(360, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
  const links = [...popEl.querySelectorAll("a")];
  popEl.addEventListener("keydown", e => { const at = links.indexOf(document.activeElement);
    if (e.key === "Escape" || (e.key === "Tab" && (e.shiftKey ? at === 0 : at === links.length - 1))) { e.preventDefault(); e.stopPropagation(); hidePop(); if (btn.isConnected) btn.focus(); } });
  if (byKey && links[0]) links[0].focus({ preventScroll: true });
}
function hidePop() { clearTimeout(popTimer); popWant = null; if (popEl) { popEl.remove(); popEl = null; } }   // (a hide still waiting must not take the next popover with it)
function scheduleHide() { clearTimeout(popTimer); popTimer = setTimeout(hidePop, 250); }
const NO_HOVER = window.matchMedia ? window.matchMedia("(hover: none)").matches : false;
document.addEventListener("mouseover", e => { if (NO_HOVER) return; const a = e.target.closest("a.pop"); if (a) { clearTimeout(popTimer); showPop(a); return; } const g = e.target.closest("button.gl"); if (g) { clearTimeout(popTimer); showGloss(g); return; }
  const sc = e.target.closest("button.srcl"); if (sc) { clearTimeout(popTimer); if (!(popEl && popEl.dataset.for === "srcl-" + sc.dataset.srcl)) showSrcl(sc); } });
document.addEventListener("mouseout", e => { if (NO_HOVER) return; if (e.target.closest("a.pop") || e.target.closest("button.gl") || e.target.closest("button.srcl")) scheduleHide(); });
document.addEventListener("focusin", e => { if (NO_HOVER) return; const a = e.target.closest("a.pop"); if (a) { showPop(a); return; } const g = e.target.closest("button.gl"); if (g) showGloss(g); });
document.addEventListener("click", e => {
  const g = e.target.closest("button.gl");
  if (g) { e.preventDefault(); if (popEl && popEl.dataset.for === "gl-" + g.dataset.gl) hidePop(); else showGloss(g); return; }
  // a line's source chip: a tap shows its sources and a second tap puts them away (a mouse has already shown them: the click keeps them)
  const sc = e.target.closest("button.srcl");
  if (sc) { e.preventDefault(); const open = popEl && popEl.dataset.for === "srcl-" + sc.dataset.srcl; if (open && (NO_HOVER || e.detail === 0)) hidePop(); else if (!open || e.detail === 0) showSrcl(sc, e.detail === 0); return; }
  const a = e.target.closest("a.pop");
  if (a) {
    // touch screens: the first tap shows the full reference (APA 7, with its link, study card and checks); hovering does this on a desktop
    // one icon for several sources: a click shows them all (there is no single page to open)
    if (a.dataset.refs) { e.preventDefault(); if (popEl && popEl.dataset.for === a.dataset.refs) hidePop(); else showPop(a); return; }
    if (NO_HOVER && !(popEl && popEl.dataset.for === a.dataset.ref)) { e.preventDefault(); showPop(a); return; }
    // otherwise the link itself opens the article's page in a new tab
    if (/^https?:/.test(a.getAttribute("href") || "")) { hidePop(); return; }
    e.preventDefault(); const ref = refById[a.dataset.ref]; const link = ref && (ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL); if (link) window.open(link, "_blank", "noopener"); return;
  }
  if (popEl && !e.target.closest(".popover")) hidePop();
  if (!e.target.closest(".searchwrap")) closeSearch();
});
// Escape closes the top layer only: a study card, then the feedback panel, then the evidence sheet
document.addEventListener("keydown", e => {
  if (e.key !== "Escape") return; hidePop(); closeSearch();
  if (document.getElementById("drawer").classList.contains("open")) closeCard();
  else if (document.getElementById("report").classList.contains("open")) closeReport();
  else if (typeof EV !== "undefined" && EV.open) closeEvidence();
});

/* Reader-facing words. The protocol's own terms (Methods) stay in the data and in the title of each label. */
const STATUS_LABEL = { "replicated": "found by several teams", "replicated-same-team": "repeated by one team only", "single-study": "one study", "contested": "experts disagree", "mixed": "results point both ways", "retraction-dependent": "rests on a retracted study" };
const STATUS_PROTOCOL = { "replicated": "replicated", "replicated-same-team": "replicated by the same team", "single-study": "single study", "contested": "contested", "mixed": "mixed", "retraction-dependent": "retraction-dependent" };
function statusLabel(s) { return STATUS_LABEL[s] || String(s).replace(/-/g, " "); }
// what a reader needs to know about a claim's checks; the ladder step itself is in the label's title and in Methods
// the senior author's approval of a claim's answer, valid only for the version he approved (METHODS §12, 0.3.0)
function editorApproved(c) { const r = (c && c.senior_review) || {}; return (r.decision === "approved" || r.decision === "approved-with-edits") && (!r.claim_version || r.claim_version === c.version); }
function readerStamp(v, c) {
  if (v === "published") return "Published";
  if (v === "senior-reviewed") return "Checked by our editor";
  if (v === "flagged") return "Problem reported: being corrected";
  if (c && editorApproved(c)) return v === "draft" ? "Approved by our editor; early draft" : "Approved by our editor; sources checked by a second AI reader";
  return v === "draft" ? "Early version: sources still being checked" : "Sources checked by a second AI reader";
}
const LADDER_WORDS = { "draft": "draft (an anchor still to be located, or resting only on narrative reviews)", "metadata-verified": "references checked against Crossref", "ai-anchored": "every evidence anchor confirmed by a second AI reader", "anchor-verified": "every anchor checked by the senior author", "appraised": "every study card read by the senior author", "senior-reviewed": "signed off by the senior author", "published": "published", "flagged": "flagged after publication" };
/* ---------- Drawer: study card ---------- */
function row(label, value) { return '<div class="card-row"><b>' + esc(label) + "</b><div>" + value + "</div></div>"; }
function fmt(v) { if (v == null || v === "") return '<span class="placeholder">[to be extracted]</span>'; return esc(String(v)).replace(/\[to be extracted from PDF\]|\[to be extracted\]/g, m => '<span class="placeholder">' + m + "</span>"); }
function sub(obj, keys) { return '<div class="sub">' + keys.filter(k => obj[k] != null && obj[k] !== "").map(k => "<span><i>" + esc(k.replace(/_/g, " ")) + ":</i> " + fmt(obj[k]) + "</span>").join("") + "</div>"; }
// Full study cards live in data/cards-<substance>.json next to the page (site/build.js) and are fetched the first time one is opened.
const CARD_FILES = {};
function loadCardFile(sub) {
  if (!CARD_FILES[sub]) CARD_FILES[sub] = fetch("data/cards-" + encodeURIComponent(sub) + ".json").then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }).catch(e => { delete CARD_FILES[sub]; throw e; });
  return CARD_FILES[sub];
}
let cardOpener = null;
function openCard(id) {
  const k = cardById[id]; if (!k) return;
  if (!document.getElementById("drawer").classList.contains("open")) cardOpener = document.activeElement;
  const panel = document.querySelector("#drawer .panel"), drawer = document.getElementById("drawer");
  const shell = msg => { panel.innerHTML = '<button class="close" type="button" aria-label="Close">✕</button><p class="muted" role="status" style="margin-top:40px">' + msg + "</p>"; panel.querySelector(".close").addEventListener("click", closeCard); drawer.classList.add("open"); };
  const sub = k.substance || "other";
  shell("Opening the study card…");
  // (the card's own reference is shown in full, so the full references come too: data/refs.json, speed)
  Promise.all([loadCardFile(sub), loadRefs()]).then(([all]) => { if (!all[id]) { shell("This study card could not be found."); return; } renderCard(id, all[id]); })
    .catch(() => shell("The study card could not be loaded. Check your connection and try again."));
}
function renderCard(id, c) {
  const ref = refById[c.reference];
  const panel = document.querySelector("#drawer .panel");
  panel.innerHTML = '<button class="close" type="button" aria-label="Close">✕</button><div class="cardhead"><span class="eyebrow">Study card · ' + esc(c.design.replace(/-/g, " ")) + "</span><h2>" + esc(ref.title) + '</h2><div class="refline mono">' + apaReference(ref) + "</div></div>" +
    row("Design", esc(c.design_detail || "")) + row("Can establish", esc(c.can_establish)) + row("Cannot establish", esc(c.cannot_establish)) +
    ((c.key_findings || []).length ? row("Key findings", '<ol class="kf">' + c.key_findings.map(k => "<li>" + fmt(k.finding) + ' <span class="loc mono">' + esc(k.page || "") + (k.locator ? " · " + esc(k.locator) : "") + "</span></li>").join("") + "</ol>") : "") +
    row("Sample & recruitment", sub(Object.assign({}, c.sample, { n_by_group: c.sample.n_by_group ? Object.entries(c.sample.n_by_group).map(kv => kv[0] + " " + kv[1]).join("; ") : null }), ["n_total", "n_by_group", "recruitment", "inclusion_exclusion", "demographics", "attrition", "selection_effects"])) +
    row("Exposure measurement", sub(c.exposure, ["measurement", "dose_frequency_duration_route", "purity_known", "polysubstance", "abstinence_at_testing"])) +
    row("Comparison group", sub(c.comparison, ["controls", "matching", "unmeasured_premorbid", "controls_other_drug_use"])) +
    row("Outcome measures", sub(c.outcomes, ["instruments", "validity_norms", "operationalization", "n_outcomes_tested", "multiplicity_correction", "assessor_blinding"])) +
    row("Analysis & reporting", sub(c.analysis, ["effect_sizes", "covariates", "preregistration", "preregistration_detail", "selective_reporting", "power"])) +
    row("Interpretation gap", sub(c.interpretation_gap, ["results_show", "claimed", "gap_assessment"])) +
    ((c.reporting_issues || []).length ? row("Reporting issues", '<ol class="kf">' + c.reporting_issues.map(k => "<li>" + fmt(k.issue) + ' <span class="loc mono">' + esc(k.page || "") + "</span>" + (k.consequence ? '<br><span class="muted">Consequence: ' + esc(k.consequence) + "</span>" : "") + "</li>").join("") + "</ol>") : "") +
    row("Replication & timeline", (c.replication.timeline ? '<div class="timeline">' + c.replication.timeline.map(t => '<div class="t"><span class="y">' + t.year + "</span><span>" + esc(t.event) + (t.reference ? " " + cite(t.reference) : "") + "</span></div>").join("") + "</div>" : "") + '<p style="margin-top:6px"><i class="muted">status:</i> ' + esc(c.replication.status) + (c.replication.where_it_stands ? " — " + esc(c.replication.where_it_stands) : "") + "</p>") +
    row("Funding & interests", sub(c.funding, ["funder", "declared_conflicts", "affiliations_note"])) +
    row("What would settle it", esc(c.what_would_settle_it)) +
    row("Risk of bias — " + (c.risk_of_bias.instrument === "none-applicable" ? "no validated instrument (editors' narrative-review checklist)" : c.risk_of_bias.instrument === "editors-qualitative" ? "editors' qualitative checklist (domains adapted from CASP)" : c.risk_of_bias.instrument === "editors-report" ? "editors' checklist for reports by public bodies" : c.risk_of_bias.instrument), '<div class="rob">' + c.risk_of_bias.domains.map(d => '<div class="d"><span class="light ' + esc(d.judgment) + '"></span><span>' + esc(d.domain) + ": <b>" + esc(d.judgment.replace(/-/g, " ")) + "</b>" + (d.note ? ' <span class="muted">— ' + fmt(d.note) + "</span>" : "") + "</span></div>").join("") + '<div class="overall">OVERALL: ' + esc(c.risk_of_bias.overall.replace(/-/g, " ").toUpperCase()) + " — " + esc(c.risk_of_bias.reasoning) + "</div></div>") +
    row("Verification", verificationHtml(c.verification));
  document.getElementById("drawer").classList.add("open");
  panel.querySelector(".close").addEventListener("click", closeCard);
  panel.scrollTop = 0;
}
function verificationHtml(v) {
  const status = { "draft": /^abstract/i.test(v.source_read || "") ? "draft: written from the abstract; to be rewritten from the full text" : "draft", "first-pass": "first pass: one AI reader, from the full text", "ai-checked": "checked: a second AI reader re-read the source, and its findings were settled against it", "appraised": "appraised by the senior author" }[v.status] || v.status;
  let h = "<p><b>" + esc(status) + "</b></p><p>" + (v.source_read ? "Read from: " + esc(v.source_read) + ". " : "") + "First pass by " + esc(v.first_pass_by) + (v.first_pass_on ? " on " + esc(v.first_pass_on) : "") + "." +
    (v.checked_by ? " Checked by " + esc(v.checked_by) + (v.checked_on ? " on " + esc(v.checked_on) : "") + "." : "") +
    (v.reviewed_by ? " Reviewed by " + esc(v.reviewed_by) + (v.reviewed_on ? " on " + esc(v.reviewed_on) : "") + "." : ' <span class="placeholder">Senior review pending.</span>') + "</p>";
  const dis = v.disagreements || [], ed = v.editorial_corrections || [];
  if (dis.length) h += '<details class="vlog"><summary>Disagreements between readers and how they were resolved (' + dis.length + ")</summary>" + dis.map(d => '<div class="ve"><div class="mono">' + esc(d.field) + "</div><div><i>First reader:</i> " + esc(d.first_pass) + "</div><div><i>Second reader:</i> " + esc(d.reviewer) + "</div><div><i>Resolution:</i> " + esc(d.resolution) + "</div></div>").join("") + "</details>";
  if (ed.length) h += '<details class="vlog"><summary>Editorial corrections (' + ed.length + ")</summary>" + ed.map(d => '<div class="ve"><div class="mono">' + esc(d.date) + " · " + esc(d.field) + ": " + esc(d.from) + " → " + esc(d.to) + "</div><div>" + esc(d.reason) + "</div></div>").join("") + "</details>";
  return h;
}
function closeCard() { const d = document.getElementById("drawer"); if (!d.classList.contains("open")) return; d.classList.remove("open"); if (cardOpener && cardOpener.focus && document.contains(cardOpener)) cardOpener.focus({ preventScroll: true }); cardOpener = null; }
document.querySelector("#drawer .scrim").addEventListener("click", closeCard);


/* ---------- Feedback and issue reports (decision s-feedback-oct26) ----------
   Two equal choices: report inaccurate information, or share feedback. Nothing is sent from the page: the message is
   written out as an email to the editors, which the reader sends from their own email (app, Gmail or Outlook.com) or
   copies. So there is no form endpoint to abuse, no account, and no data leaves the device until the reader sends it. */
const FB_EMAIL = ["contact", "pharmakon.world"].join("@");   // assembled here so the address is not in the page as plain text for scrapers
const FB_MAX = 1500;
const FB = { mode: null, where: "", opener: null, used: false };
document.querySelectorAll("[data-email]").forEach(a => { a.href = "mailto:" + FB_EMAIL; if (a.dataset.email === "text") a.textContent = FB_EMAIL; });
// the page the reader is on, in words, and its address
function fbPage(where) {
  const h = String(where || location.hash || "#home").replace(/^#/, "");
  const title = h.startsWith("cl_") && claimById[h] ? (subBySlug[claimById[h].substance] ? subBySlug[claimById[h].substance].name + ": " : "") + "answer “" + (((SIMPLE.claims || {})[h] || {}).short || claimText(claimById[h])).slice(0, 90) + "”"
    : document.title.replace(/ · Pharmakon$/, "").replace(/^Pharmakon: .*/, "Start page");
  const short = h.startsWith("cl_") && claimById[h] ? (subBySlug[claimById[h].substance] ? subBySlug[claimById[h].substance].name : "Mixing drugs") + " answer" : title;
  return { title, short: short.length > 50 ? short.slice(0, short.lastIndexOf(" ", 50)) + "…" : short, url: location.origin + location.pathname + "#" + (h || "home") };
}
// "Ask a question or share an idea" and "Report a mistake" (senior author, 13 November: one place to ask, merged with ideas);
// a question typed into the search box that found nothing comes along as the start of the message
function openFeedback(mode, where, prefill) {
  FB.where = where || location.hash || "#home"; FB.opener = document.activeElement; closeSearch();
  const m = document.getElementById("report"); m.classList.add("open");
  document.getElementById("report-status").textContent = "";
  document.getElementById("fb-incl").checked = true;   // each time, the page the reader is on is included unless they untick it
  if (FB.used) { document.getElementById("report-message").value = ""; document.getElementById("report-source").value = ""; FB.used = false; }   // a message already written out is not reused
  if (prefill && !document.getElementById("report-message").value.trim()) document.getElementById("report-message").value = String(prefill).slice(0, FB_MAX);
  fbChoose(mode || null);
  setTimeout(() => { const f = mode ? document.getElementById("report-message") : document.querySelector(".fb-opt"); if (f) f.focus(); }, 50);
}
const openReport = where => openFeedback("issue", where);   // older buttons ("Report a mistake" under each claim)
function fbChoose(mode) {
  FB.mode = mode;
  document.querySelectorAll(".fb-opt").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === mode)));
  const form = document.getElementById("report-form"); form.hidden = !mode;
  if (!mode) return;
  const issue = mode === "issue";
  // one box and one button (senior author, 26 October: too many steps and too much text)
  document.getElementById("fb-msg-label").textContent = issue ? "What is wrong, and what should it say?" : "Your question or idea";
  document.getElementById("report-message").placeholder = issue ? "For example: the second answer says 12 people, but the study had 14." : "For example: is it true that ecstasy makes holes in your brain?";
  document.getElementById("fb-source-wrap").hidden = !issue;
  const p = fbPage(FB.where); document.getElementById("report-where").textContent = p.title;
  fbUpdate();
}
/* The email (site 2.4, 15 November 2026; the senior author sent himself one and asked whether its form "is as good as possible").
   Before: every email was called "Pharmakon: a question or idea (Start page)", so a mail program put different people's
   messages into one thread, and the message itself came after three lines about the page. Now the subject is a tag a filter
   can catch and the person's own first words ("[Pharmakon question] can i have hallucinations from alcohol?"); the body
   starts with the message; what the page adds stands under a line at the end, the last line in a fixed form a program can
   read (kind | page | site version). */
function fbText() {
  const msg = document.getElementById("report-message").value.trim(), src = document.getElementById("report-source").value.trim();
  const incl = document.getElementById("fb-incl").checked, p = fbPage(FB.where), issue = FB.mode === "issue";
  const one = msg.replace(/\s+/g, " "), head = one.length > 72 ? one.slice(0, one.lastIndexOf(" ", 70) > 30 ? one.lastIndexOf(" ", 70) : 70) + "…" : one;
  const subject = (issue ? "[Pharmakon mistake] " : "[Pharmakon question] ") + (head || (incl ? p.short : ""));
  const where = String(FB.where || "#home").replace(/^#/, "") || "home";
  const body = msg + "\n" + (issue && src ? "\nSource: " + src + "\n" : "") + "\n--\n" +
    (incl ? "About: " + p.title + "\n" + p.url + "\n" : "") +
    "pharmakon | " + (issue ? "mistake" : "question") + " | " + (incl ? where : "-") + " | " + SITE_VERSION;
  return { subject, body, msg };
}
function fbUpdate() {
  const t = fbText(), q = "?subject=" + encodeURIComponent(t.subject) + "&body=" + encodeURIComponent(t.body);
  document.getElementById("fb-mailto").href = "mailto:" + FB_EMAIL + q;
  document.getElementById("fb-gmail").href = "https://mail.google.com/mail/?view=cm&fs=1&to=" + encodeURIComponent(FB_EMAIL) + "&su=" + encodeURIComponent(t.subject) + "&body=" + encodeURIComponent(t.body);
  document.getElementById("fb-outlook").href = "https://outlook.live.com/mail/0/deeplink/compose?to=" + encodeURIComponent(FB_EMAIL) + "&subject=" + encodeURIComponent(t.subject) + "&body=" + encodeURIComponent(t.body);
  const n = document.getElementById("report-message").value.length; document.getElementById("fb-count").textContent = n + " / " + FB_MAX;
}
function fbReady(e) {
  const st = document.getElementById("report-status");
  if (!fbText().msg) { if (e) e.preventDefault(); st.textContent = "Write your message first."; document.getElementById("report-message").focus(); return false; }
  return true;
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("[data-fb]"); if (!b) return;
  e.preventDefault(); const menu = document.getElementById("menu"); if (menu && !menu.hidden && menu.contains(b)) { const mb = document.getElementById("menubtn"); if (mb) mb.click(); }
  openFeedback(b.dataset.fb || null, b.dataset.where ? "#" + b.dataset.where : location.hash, b.dataset.fbText || "");
});
document.querySelectorAll(".fb-opt").forEach(b => b.addEventListener("click", () => { fbChoose(b.dataset.mode); document.getElementById("report-message").focus(); }));
["report-message", "report-source", "fb-incl"].forEach(id => { const el = document.getElementById(id); el.addEventListener("input", fbUpdate); el.addEventListener("change", fbUpdate); });
document.getElementById("report-form").addEventListener("submit", e => e.preventDefault());
document.getElementById("fb-mailto").addEventListener("click", e => { if (!fbReady(e)) return; fbUpdate(); FB.used = true;
  document.getElementById("report-status").textContent = "Your email app should now open with the message written out. It is not sent until you press Send there. Nothing opened? Use Gmail, Outlook.com or Copy the message."; });
["fb-gmail", "fb-outlook"].forEach(id => document.getElementById(id).addEventListener("click", e => { if (!fbReady(e)) return; fbUpdate(); FB.used = true;
  document.getElementById("report-status").textContent = "A new tab opens with the email written out. It is not sent until you press Send there."; }));
document.getElementById("fb-copy").addEventListener("click", async () => {
  if (!fbReady()) return; const t = fbText(), all = "To: " + FB_EMAIL + "\nSubject: " + t.subject + "\n\n" + t.body, st = document.getElementById("report-status");
  FB.used = true;
  try { await navigator.clipboard.writeText(all); st.textContent = "Copied. Paste it into a new email to " + FB_EMAIL + " and press Send."; }
  catch (err) { const ta = document.createElement("textarea"); ta.value = all; document.body.appendChild(ta); ta.select(); let ok = false; try { ok = document.execCommand("copy"); } catch (x) { ok = false; } ta.remove();
    st.textContent = ok ? "Copied. Paste it into a new email to " + FB_EMAIL + " and press Send." : "Copying is blocked in this browser. Write to " + FB_EMAIL + " and paste your message there."; }
});
function closeReport() { const m = document.getElementById("report"); if (!m.classList.contains("open")) return; m.classList.remove("open"); if (FB.opener && FB.opener.focus) FB.opener.focus(); }
document.querySelector("#report .scrim").addEventListener("click", closeReport);
document.getElementById("report-close").addEventListener("click", closeReport);
// keep the keyboard inside the open panel
document.getElementById("report").addEventListener("keydown", e => {
  if (e.key !== "Tab") return; const f = [...document.querySelectorAll("#report .panel button, #report .panel a[href], #report .panel summary, #report .panel textarea, #report .panel input")].filter(x => !x.closest("[hidden]") && x.offsetParent !== null);
  if (!f.length) return; const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});
// the line at the end of each drug page
function fbLineHtml() {
  return '<section class="sec fbline" aria-label="Ask or report"><p><b>Didn’t find your question?</b> Ask us.</p><div class="fb-two">' +
    '<button type="button" data-fb="feedback">' + icon("message") + "Ask a question</button>" +
    '<button type="button" data-fb="issue">' + icon("flag") + "Report a mistake</button></div></section>";
}


/* ---------- Senior review queue (db: reviews/<claim>, anchors/<claim>; only the owner writes) ---------- */
const REVIEW = { db: null, owner: false, uid: null, reviews: {}, anchors: {}, cards: {}, decisions: {}, live: false };
const DECISION_LABEL = { "approved": "approved by the senior author", "approved-with-edits": "approved with edits by the senior author", "flagged": "flagged by the senior author", "pending": "awaiting senior review" };
(async () => {
  try {
    if (!window.claude || !window.claude.use) { reviewUnavailable(); return; }
    const [d, u] = await Promise.all([window.claude.use("db"), window.claude.use("user")]);
    if (!d) { reviewUnavailable(); return; }
    REVIEW.db = d; REVIEW.live = true;
    REVIEW.owner = u ? await u.isOwner() : false;
    REVIEW.uid = u && u.id ? await u.id() : null;
    if (REVIEW.owner) document.getElementById("nav-review").hidden = false;
    d.collection("reviews").onSnapshot(snap => { const m = {}; snap.docs.forEach(x => { m[x.id] = x.data(); }); REVIEW.reviews = m; onReviewData(); }, () => {});
    d.collection("anchors").onSnapshot(snap => { const m = {}; snap.docs.forEach(x => { m[x.id] = x.data(); }); REVIEW.anchors = m; onReviewData(); }, () => {});
    d.collection("cards").onSnapshot(snap => { const m = {}; snap.docs.forEach(x => { m[x.id] = x.data(); }); REVIEW.cards = m; onReviewData(); }, () => {});
    d.collection("decisions").onSnapshot(snap => { const m = {}; snap.docs.forEach(x => { m[x.id] = x.data(); }); REVIEW.decisions = m; renderDecisions(); }, () => {});
    renderReview();
  } catch (e) { reviewUnavailable(); }
})();
function reviewUnavailable() { const n = document.getElementById("review-unavailable"); if (n) n.hidden = false; }
// A decision taken on an earlier version of a claim does not carry over (Methods §5.5).
function currentDecision(c) { const r = REVIEW.reviews[c.id]; if (!r || !r.decision || r.decision === "pending") return null; return r.claim_version && r.claim_version !== c.version ? null : r.decision; }
function staleDecision(c) { const r = REVIEW.reviews[c.id]; return !!(r && r.decision && r.decision !== "pending" && r.claim_version && r.claim_version !== c.version); }
function reviewRank(c) {
  const g = ((MONOS.find(x => x.slug === c.substance) || MONO).at_a_glance || {}); const be = g.best_established || [], lu = g.largest_uncertainties || [];
  if (be.includes(c.id)) return be.indexOf(c.id);
  if (lu.includes(c.id)) return 10 + lu.indexOf(c.id);
  const cert = { "high": 0, "moderate": 1, "low": 2, "very-low": 3 }[c.grade.certainty];
  return (c.verification.status === "draft" ? 100 : 20) + cert * 10 + c.section / 100;
}
function anchorChecked(cid, i) { const a = REVIEW.anchors[cid]; return !!(a && a.checks && a.checks[String(i)] && a.checks[String(i)].ok); }
// The senior author's reading of a study card against its source (Methods §5.5): stored per card in the "cards" collection.
function cardRead(k) { const x = REVIEW.cards[k]; return !!(x && x.read); }
function cardShortLabel(k) { const r0 = cardById[k] && refById[cardById[k].reference]; return r0 ? (r0.author[0].short || r0.author[0].literal || r0.author[0].family) + (r0.author.length > 2 ? " et al." : "") + " " + year(r0) : k; }
function onReviewData() {
  document.querySelectorAll("[data-senior]").forEach(el => {
    const r = REVIEW.reviews[el.dataset.senior];
    const c = claimById[el.dataset.senior]; const cur = c ? currentDecision(c) : null;
    el.textContent = cur ? DECISION_LABEL[cur] + (r.date ? " · " + r.date : "") : "";
    el.className = "senior-slot" + (cur ? " " + cur : "");
  });
  document.querySelectorAll("[data-anchor]").forEach(el => {
    const [cid, i] = el.dataset.anchor.split(":");
    const badge = el.querySelector(".anchor");
    if (badge && anchorChecked(cid, i)) { badge.className = "anchor senior-verified"; badge.textContent = ANCHOR_LABEL["senior-verified"]; }
  });
  if (document.getElementById("view-review").classList.contains("active")) renderReview();
}
function anchorSourceLink(e) {
  const r = refById[e.reference]; if (!r) return "";
  if (e.source_read === "PDF" && r.verification && r.verification.pdf_path) return '<span class="mono">' + esc(r.verification.pdf_path.replace(/^PDFs\//, "DrugEncyclopedia/PDFs/")) + "</span>";
  if (r.PMCID) return '<a href="https://pmc.ncbi.nlm.nih.gov/articles/' + esc(r.PMCID) + '/" target="_blank" rel="noopener">PubMed Central</a>';
  return r.DOI ? '<a href="https://doi.org/' + esc(r.DOI) + '" target="_blank" rel="noopener">doi.org/' + esc(r.DOI) + "</a>" : "";
}
/* Decisions only the senior author can take (data/site/decisions.json; saved per item in the "decisions" collection) */
function renderDecisions() {
  const box = document.getElementById("review-decisions"); if (!box) return;
  const items = (DECISIONS && DECISIONS.items) || [];
  const done = it => { const x = REVIEW.decisions[it.id]; return !!(x && (Number.isInteger(x.choice) || (it.text && x.note))); };
  const n = items.filter(done).length;
  document.getElementById("dec-count").textContent = "(" + n + " of " + items.length + " decided)";
  const dis = REVIEW.owner && REVIEW.db ? "" : " disabled";
  let h = "", group = null;
  items.forEach(it => {
    if (it.group !== group) { group = it.group; h += "<h3>" + esc(group) + "</h3>"; }
    const x = REVIEW.decisions[it.id] || {};
    const links = (it.claims || []).filter(id => claimById[id]).map(id => '<a href="#' + id + '">' + esc((claimById[id].outcome || id).replace(/^./, ch => ch.toUpperCase())) + "</a>").join("; ");
    h += '<fieldset class="dec' + (done(it) ? " done" : "") + '" id="dec-' + it.id + '"><legend>' + esc(it.title) + "</legend>" +
      (it.detail || links ? '<p class="detail">' + esc(it.detail || "") + (links ? (it.detail ? " " : "") + "Claim" + ((it.claims || []).length > 1 ? "s" : "") + ": " + links + "." : "") + "</p>" : "") +
      (it.options || []).map((o, i) => '<label><input type="radio" name="dec-' + it.id + '" value="' + i + '" data-dec="' + it.id + '"' + (x.choice === i ? " checked" : "") + dis + "> " + esc(o) + (it.recommend === i ? '<span class="rec">recommended</span>' : "") + "</label>").join("") +
      (it.text ? '<textarea rows="2" data-dec-note="' + it.id + '" placeholder="Write it here"' + dis + ">" + esc(x.note || "") + "</textarea>" : '<input type="text" data-dec-note="' + it.id + '" placeholder="Note (optional)" value="' + esc(x.note || "") + '"' + dis + ">") +
      '<span class="saved" id="decs-' + it.id + '">' + (x.date ? "Saved " + esc(x.date) : "") + "</span></fieldset>";
  });
  box.innerHTML = h + (REVIEW.owner ? "" : '<p class="muted small">Read-only: only the owner saves decisions.</p>');
}
async function saveDecision(id) {
  const box = document.getElementById("dec-" + id); if (!box || !REVIEW.db) return;
  const r = box.querySelector("input[type=radio]:checked"); const note = box.querySelector("[data-dec-note]");
  const st = document.getElementById("decs-" + id);
  try {
    await REVIEW.db.doc("decisions/" + id).set({ choice: r ? Number(r.value) : null, note: note ? note.value.trim() : "", date: new Date().toISOString().slice(0, 10), by: REVIEW.uid });
    if (st) st.textContent = "Saved.";
  } catch (e) { if (st) st.textContent = "Could not save (" + (e && e.code ? e.code : "unavailable") + ")."; }
}
document.addEventListener("change", ev => {
  const t = ev.target; if (!t.matches || !REVIEW.owner) return;
  if (t.matches("[data-dec]")) saveDecision(t.dataset.dec);
  else if (t.matches("[data-dec-note]")) saveDecision(t.dataset.decNote);
});
let reviewSectionsFilled = false;
function renderReview() {
  renderDecisions();
  const list = document.getElementById("review-list"); if (!list) return;
  const sel = document.getElementById("review-section");
  const orderSel = document.getElementById("review-order"); const byRank = !orderSel || orderSel.value !== "section";
  const claims = CLAIMS.filter(c => c.substance === (currentSlug || "methamphetamine")).slice().sort((a, b) => byRank ? reviewRank(a) - reviewRank(b) : a.section - b.section);
  if (!reviewSectionsFilled) { [...new Set(claims.map(c => c.section))].forEach(n => { const o = document.createElement("option"); o.value = n; const sec = (MONO.sections || []).find(x => x.number === n); o.textContent = n + ". " + (sec ? sec.title : ""); sel.appendChild(o); }); reviewSectionsFilled = true; }
  const secF = sel.value, f = document.getElementById("review-filter").value;
  const decided = claims.filter(c => currentDecision(c)).length;
  const allA = claims.flatMap(c => c.evidence.map((e, i) => [c.id, i, e]));
  const checkable = allA.filter(([, , e]) => e.anchor_status !== "unchecked").length;
  const checked = allA.filter(([cid, i]) => anchorChecked(cid, i)).length;
  const allCards = [...new Set(claims.flatMap(c => c.evidence.map(e => e.study_card)))].filter(k => cardById[k]);
  document.getElementById("review-progress").innerHTML = '<div><b class="num">' + decided + " / " + claims.length + '</b> claims decided</div><div><b class="num">' + checked + " / " + checkable + '</b> located anchors checked by you</div><div><b class="num">' + allCards.filter(cardRead).length + " / " + allCards.length + '</b> study cards read against their sources</div><div><b class="num">' + (allA.length - checkable) + "</b> anchors still waiting for a PDF</div>" + (REVIEW.owner ? "" : '<div class="muted">Read-only: only the owner saves decisions.</div>');
  const shown = claims.filter(c => { const d = currentDecision(c); return (!secF || String(c.section) === secF) && (f === "all" || (f === "pending" ? !d : d && (f === "approved" ? /^approved/.test(d) : d === f))); });
  list.innerHTML = shown.length ? shown.map(c => {
    const r = REVIEW.reviews[c.id] || {}; const a = (REVIEW.anchors[c.id] || {}).checks || {};
    const rows = c.evidence.map((e, i) => { const ok = a[String(i)] && a[String(i)].ok; const note = (a[String(i)] && a[String(i)].note) || ""; const dis = e.anchor_status === "unchecked" || !REVIEW.owner;
      return '<li class="rv-a' + (ok ? " ok" : "") + '"><label><input type="checkbox" data-rv-check="' + c.id + ":" + i + '"' + (ok ? " checked" : "") + (dis ? " disabled" : "") + '> <span class="role ' + e.role + '">' + e.role + "</span> " + (e.extracted.startsWith("[") ? '<span class="placeholder">' + esc(e.extracted) + "</span>" : esc(e.extracted)) + '</label><div class="src">' + cite(e.reference) + " · " + esc(e.page) + (e.locator && !e.locator.startsWith("[") ? " · " + esc(e.locator) : "") + " · " + anchorSourceLink(e) + " · " + '<span class="anchor ' + (ok ? "senior-verified" : e.anchor_status) + '">' + esc(ok ? ANCHOR_LABEL["senior-verified"] : (ANCHOR_LABEL[e.anchor_status] || e.anchor_status)) + '</span></div><input type="text" class="rv-anote" data-rv-note="' + c.id + ":" + i + '" placeholder="Note on this anchor (optional)" value="' + esc(note) + '"' + (REVIEW.owner ? "" : " disabled") + "></li>"; }).join("");
    const allOk = c.evidence.every((e, i) => a[String(i)] && a[String(i)].ok);
    const cIds = [...new Set(c.evidence.map(e => e.study_card))].filter(k => cardById[k]);
    const cardsOk = cIds.every(cardRead);
    const cardRows = cIds.map(k => { const rd = cardRead(k); return '<li class="rv-c' + (rd ? " ok" : "") + '"><label><input type="checkbox" data-rv-card="' + k + '"' + (rd ? " checked" : "") + (REVIEW.owner ? "" : " disabled") + "> read against its source</label> " + '<button type="button" class="linklike" data-card="' + k + '">' + esc(cardShortLabel(k)) + "</button> " + '<span class="muted small">' + esc(cardById[k].verification.status) + "</span></li>"; }).join("");
    const canApprove = allOk && cardsOk && REVIEW.owner;
    const why = !allOk ? "Tick every anchor first" : !cardsOk ? "Mark every study card read first" : "";
    const cur = currentDecision(c);
    const g = (MONOS.find(x => x.slug === c.substance) || MONO).at_a_glance || {}; const where = (g.best_established || []).includes(c.id) ? "shown as best established" : (g.largest_uncertainties || []).includes(c.id) ? "shown as a largest uncertainty" : "";
    return '<article class="rv" id="rv-' + c.id + '"><header><span class="n">' + c.section + '</span><a href="#' + c.id + '">' + esc(c.id) + '</a><span class="grade">' + gradeDots(c.grade.certainty) + " " + esc(gradeLabel(c.grade.certainty)) + '</span><span class="badge ' + c.status + '">' + esc(statusLabel(c.status)) + "</span>" + (where ? '<span class="muted small">at a glance: ' + where + "</span>" : "") + (c.verification.status === "draft" ? '<span class="muted small">' + (narrativeOnly(c) ? "draft: rests only on narrative reviews" : "draft: an anchor is not yet located in a full text") + "</span>" : "") + (cur ? '<span class="senior-slot ' + esc(cur) + '">' + esc(DECISION_LABEL[cur] || cur) + (r.date ? " · " + esc(r.date) : "") + "</span>" : "") + (staleDecision(c) ? '<span class="senior-slot flagged">decided on v' + esc(r.claim_version) + "; the claim has changed since (now v" + esc(c.version) + "), please review again</span>" : "") + "</header>" +
      (c.plain ? '<p class="plain">' + esc(c.plain) + "</p>" : "") + '<details><summary>Precise statement, grading and reasoning</summary><p>' + esc(c.statement) + '</p><p class="mono">' + esc(gradeDomains(c.grade)) + "</p><p>" + esc(c.grade.reasoning) + "</p></details>" +
      '<ol class="rv-anchors">' + rows + "</ol>" +
      '<p class="rv-h">Study cards this claim rests on</p><ul class="rv-cards">' + cardRows + "</ul>" +
      '<div class="rv-decide"><textarea data-rv-dnote="' + c.id + '" rows="2" placeholder="Note for the co-editor: what to change, or why it is flagged"' + (REVIEW.owner ? "" : " disabled") + ">" + esc(r.note || "") + "</textarea>" +
      '<div class="rv-buttons">' +
        '<button type="button" class="primary" data-rv-decide="' + c.id + '" data-d="approved"' + (canApprove ? '' : ' disabled') + ' title="' + why + '">Approve</button>' +
        '<button type="button" data-rv-decide="' + c.id + '" data-d="approved-with-edits"' + (canApprove ? '' : ' disabled') + ' title="' + why + '">Approve with edits</button>' +
        '<button type="button" class="danger" data-rv-decide="' + c.id + '" data-d="flagged"' + (REVIEW.owner ? '' : ' disabled') + '>Flag</button>' +
        '<span class="rv-status" id="rvs-' + c.id + '"></span></div></div></article>';
  }).join("") : '<p class="note">Nothing to show with these filters.</p>';
}
async function saveAnchorChecks(cid) {
  const checks = {};
  document.querySelectorAll('[data-rv-check^="' + cid + ':"]').forEach(cb => { const i = cb.dataset.rvCheck.split(":")[1]; const n = document.querySelector('[data-rv-note="' + cid + ":" + i + '"]'); checks[i] = { ok: cb.checked, note: n ? n.value.trim() : "", date: new Date().toISOString().slice(0, 10) }; });
  await REVIEW.db.doc("anchors/" + cid).set({ checks: checks, by: REVIEW.uid, updated: new Date().toISOString() });
}
document.addEventListener("change", async ev => {
  const t = ev.target;
  if (t.matches && (t.matches("[data-rv-check]") || t.matches("[data-rv-note]")) && REVIEW.owner && REVIEW.db) {
    const cid = (t.dataset.rvCheck || t.dataset.rvNote).split(":")[0];
    const st = document.getElementById("rvs-" + cid);
    try { await saveAnchorChecks(cid); if (st) st.textContent = "Saved."; } catch (e) { if (st) st.textContent = "Could not save (" + (e && e.code ? e.code : "unavailable") + ")."; }
  }
  if (t.matches && t.matches("[data-rv-card]") && REVIEW.owner && REVIEW.db) {
    const k = t.dataset.rvCard;
    try { await REVIEW.db.doc("cards/" + k).set({ read: t.checked, date: new Date().toISOString().slice(0, 10), by: REVIEW.uid }); } catch (e) { t.checked = !t.checked; }
  }
  if (t.id === "review-section" || t.id === "review-filter" || t.id === "review-order") renderReview();
});
document.addEventListener("click", ev => {
  const k = ev.target.closest && ev.target.closest("#review-list [data-card]"); if (k) openCard(k.dataset.card);
});
document.addEventListener("click", async ev => {
  const b = ev.target.closest && ev.target.closest("[data-rv-decide]"); if (!b || !REVIEW.owner || !REVIEW.db) return;
  const cid = b.dataset.rvDecide, d = b.dataset.d; const c = claimById[cid];
  const note = (document.querySelector('[data-rv-dnote="' + cid + '"]') || {}).value || "";
  const st = document.getElementById("rvs-" + cid);
  if (d !== "approved" && !note.trim()) { if (st) st.textContent = d === "flagged" ? "Say what is wrong in the note first." : "Say what to change in the note first."; return; }
  try {
    await REVIEW.db.doc("reviews/" + cid).set({ decision: d, note: note.trim(), date: new Date().toISOString().slice(0, 10), claim_version: c.version, by: REVIEW.uid });
    if (st) st.textContent = "Saved.";
  } catch (e) { if (st) st.textContent = "Could not save (" + (e && e.code ? e.code : "unavailable") + ")."; }
});

/* ---------- The pages of running text as sections (site 2.4): How to read, Methods, About. Each block marked data-sections
   in the template is cut where its h2 headings are: what stands before the first heading stays as the page's opening, and
   every heading becomes a row of the page's menu with its text as the section (the same mechanism as a drug page). The row's
   quiet line is the start of the section's own text. ---------- */
function sectionize() {
  document.querySelectorAll(".prose[data-sections]").forEach(box => {
    const pre = box.dataset.sections, kids = [...box.children], first = kids.findIndex(k => k.tagName === "H2" && !k.closest(".inshort"));
    if (first < 0) return;
    const secs = []; let cur = null;
    kids.slice(first).forEach(k => { if (k.tagName === "H2") { cur = { name: k.textContent.trim(), nodes: [] }; secs.push(cur); } else cur.nodes.push(k); });
    const slug = t => norm(t).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").split("-").slice(0, 4).join("-");
    secs.forEach(x => { x.id = pre + "-" + slug(x.name); const tmp = document.createElement("div"); tmp.innerHTML = x.nodes.map(n => n.outerHTML).join(" ").replace(/<thead[\s\S]*?<\/thead>/g, " ").replace(/<[^>]+>/g, " "); /* (a table's column names are not the section's first words) */ const t = tmp.textContent.replace(/\s+/g, " ").replace(/ ([,.;:])/g, "$1").trim(); x.line = t.length > 96 ? t.slice(0, t.lastIndexOf(" ", 92)).replace(/[,;:.]$/, "") + "…" : t;
      x.chip = x.name.length > 26 ? x.name.split(/[,:]/)[0] : x.name; x.icon = "book"; x.body = '<div data-slot="' + x.id + '"></div>'; });
    const wrap = document.createElement("div"); wrap.className = "secpage"; wrap.dataset.base = box.dataset.base; wrap.innerHTML = secPageHtml(box.dataset.up || "All sections", secs);
    secs.forEach(x => { const slot = wrap.querySelector('[data-slot="' + x.id + '"]'); const holder = document.createElement("div"); holder.className = "prose"; x.nodes.forEach(n => holder.appendChild(n)); slot.replaceWith(holder); });
    kids.slice(first).forEach(k => { if (k.tagName === "H2") k.remove(); });
    box.after(wrap);
  });
}

/* ---------- Boot ---------- */
document.documentElement.lang = "en";
applyPhotoPref();
(function () { const el = document.getElementById("photo-credits"); if (!el) return; const name = s => (subBySlug[s] ? subBySlug[s].name : s === "safety-drug-checking" ? "Drug checking" : s);
  el.innerHTML = PHOTOS.slice().sort((a, b) => name(a.drug).localeCompare(name(b.drug))).map(p => "<li><b>" + esc(name(p.drug)) + ":</b> " + esc(p.form.toLowerCase()) + ". " + photoCredit(p) + "</li>").join(""); })();
// (the statistics page draws on its first visit, once its file has arrived)
buildIndex(); renderHome2(); factsLinks(); renderSubstances(); renderGlossary(); renderInteractions(); renderEmergency(); renderLaw(); renderChecking(); sectionize();
window.addEventListener("hashchange", route);
document.getElementById("skiplink").addEventListener("click", () => { const v = document.querySelector(".view.active"); const h = v && v.querySelector("h1"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } });
route();
