/* ---------- Monograph registry ---------- */
const TEMPLATE_SECTIONS = [
  [2, "Identity and nomenclature"], [3, "Pharmacology"], [4, "Neuroscience"], [5, "Effects"], [6, "Acute risks"],
  [7, "Routes of administration and practical risk reduction"], [8, "Dependence and patterns of use"], [9, "Long-term effects"],
  [10, "Epidemiology"], [11, "Harm-reduction interventions"], [12, "Treatment and therapeutic research"], [13, "Legal status"],
  [14, "Contested questions"], [15, "Research gaps"]
];
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
  mix: circ(9, 12, 6) + circ(15, 12, 6)
};
function icon(name, cls) { const d = ICONS[name]; return d ? '<svg class="ic' + (cls ? " " + cls : "") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>' : ""; }
/* One colour and one icon per drug family (the families are the site's classes) */
const FAMILY = { "Stimulants": { k: "stim", icon: "bolt" }, "Depressants": { k: "dep", icon: "moon" }, "Entactogens": { k: "ent", icon: "heart" }, "Classic psychedelics": { k: "psy", icon: "eye" }, "Atypical psychedelics": { k: "apsy", icon: "burst" }, "Dissociatives": { k: "dis", icon: "orbit" }, "Opioids": { k: "opi", icon: "poppy" }, "Cannabinoids": { k: "can", icon: "leaf" }, "Inhalants": { k: "inh", icon: "wind" } };
function fam(cls) { return FAMILY[cls] || { k: "oth", icon: "molecule" }; }
function famChip(cls) { const f = fam(cls); return '<span class="famchip f-' + f.k + '">' + icon(f.icon) + esc(cls) + "</span>"; }
/* How strong the evidence is: the GRADE level as signal bars and words; the GRADE term stays in the title */
const CERT_WORDS = { high: "Strong evidence", moderate: "Moderate evidence", low: "Limited evidence", "very-low": "Very limited evidence" };
function meterHtml(cert, small) {
  const n = { high: 4, moderate: 3, low: 2, "very-low": 1 }[cert] || 1;
  return '<span class="meter m' + n + (small ? " sm" : "") + '" title="GRADE certainty: ' + esc(String(cert).replace("-", " ")) + '"><span class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="mw">' + esc(CERT_WORDS[cert] || cert) + "</span></span>";
}
function meterDots(cert) { const n = { high: 4, moderate: 3, low: 2, "very-low": 1 }[cert] || 1; return '<span class="meter m' + n + ' xs" title="' + esc(CERT_WORDS[cert] || cert) + '"><span class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="sr">' + esc(CERT_WORDS[cert] || cert) + "</span></span>"; }
const META_SOURCE = { crossref: "Crossref", publisher: "publisher's page", pubmed: "PubMed", manual: "entered by hand" };
function monographFor(slug) {
  if (slug === MONO.slug) return MONO;
  const full = MONOS.find(x => x.slug === slug); if (full) return full;  // every drug with a written monograph
  const s = subBySlug[slug]; if (!s) return null;
  return {
    slug: s.slug, name: s.name, inn: "", classes: [s.cls], mechanisms: [s.mech], tier: 1, version: "0.0.0", status: "planned",
    dates: { last_search: null, last_review: null }, authors: MONO.authors,
    at_a_glance: null,
    sections: TEMPLATE_SECTIONS.map(t => ({ number: t[0], title: t[1], claims: [], senior_author_only: t[0] === 7,
      no_evidence_note: t[0] === 7 ? "Not written yet. This section will be added by the senior author after a legal review, to the same citation standard as every other section." : "Not written yet. The evidence map lists the papers this section will be built from; nothing is written until they have been read in full." })),
    changelog: []
  };
}

/* ---------- Routing ---------- */
const PAGE_VIEWS = ["home", "substances", "drug", "shared", "monograph", "numbers", "interactions", "checking", "facts", "emergency", "law", "methods", "about", "glossary", "howto", "review", "quiz", "notfound"];
const PAGE_TITLES = { home: "", shared: "Shared answer", facts: "Facts about drug use", substances: "Find a drug", numbers: "Statistics", interactions: "Mixing drugs", emergency: "Emergency numbers", checking: "Drug checking", law: "Drug treaties by country", methods: "Methods", about: "About", glossary: "Glossary", howto: "How to read this site", review: "Review queue", quiz: "Myth or fact?", notfound: "Page not found" };
let currentSlug = MONO.slug, renderedSlug = null;
function setTitle(t) { document.title = t ? t + " · Pharmakon" : "Pharmakon: what the research says about drugs"; }
// after a page change, keyboard and screen-reader users start at the page heading
function focusHeading(view) { const h = document.querySelector("#view-" + view + " h1"); if (h) { h.setAttribute("tabindex", "-1"); try { h.focus({ preventScroll: true }); } catch (e) { h.focus(); } } }
function openAround(el) { for (let d = el && el.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true; }
function openSection(id) { const el = document.getElementById(id); if (!el) return; if (el.tagName === "DETAILS") el.open = true; const d = el.closest("details"); if (d) d.open = true; scrollToEl(el); }
let routedOnce = false;
function route() {
  let h = (location.hash || "#home").slice(1);
  const first = !routedOnce; routedOnce = true;
  if (typeof EV !== "undefined" && EV.open) closeEvidence(true);
  // a link to a section, a claim or a reference opens the full evidence; the plain page address opens the reader's choice
  setMode(/^(cl_|sec-|ref-)/.test(h) || /^s-[a-z0-9-]+\/(sec-\d+|not-yet|evidence)$/.test(h) ? "full" : /^s-[a-z0-9-]+\/q-/.test(h) ? "quick" : PREF_MODE);
  // one shared answer: #a/<page>/<claim>, the Share button's address (only that answer, then the way to the rest)
  if (h.startsWith("a/")) {
    const m = h.match(/^a\/([a-z0-9-]+)\/(cl_[a-z0-9_]+)$/), t = m && renderShared(m[1], m[2]);
    if (t) { show("shared"); setTitle(t); window.scrollTo({ top: 0 }); focusHeading("shared"); return; }
    renderNotFound(h.slice(2)); show("notfound"); setTitle(PAGE_TITLES.notfound); window.scrollTo({ top: 0 }); focusHeading("notfound"); return;
  }
  // substance pages, optionally with a section: #s-ketamine or #s-ketamine/sec-13 (the substance is always in the address)
  if (h.startsWith("s-")) {
    const mm = h.slice(2).match(/^([a-z0-9-]+)(?:\/(sec-\d+|not-yet|evidence|q-cl_[a-z0-9_]+|part-d-[a-z]+))?$/);
    const slug = mm ? mm[1] : h.slice(2), sec = mm && mm[2];
    if (!mm || !monographFor(slug)) { renderNotFound(h.slice(2)); show("notfound"); setTitle(PAGE_TITLES.notfound); window.scrollTo({ top: 0 }); focusHeading("notfound"); return; }
    // the simple page answers first (#s-mdma, #s-mdma/q-cl_...); the evidence page is one tap away (#s-mdma/evidence, sections, claims)
    if (subBySlug[slug] && (!sec || sec.startsWith("q-") || sec.startsWith("part-"))) {
      if (renderedDrug !== slug) renderDrug(slug);
      show("drug"); setTitle(subBySlug[slug].name);
      if (sec && sec.startsWith("part-")) { const el = document.getElementById(sec.slice(5)); if (el) { setTimeout(() => scrollToEl(el), 30); const hh = el.querySelector("h2"); if (hh) { hh.setAttribute("tabindex", "-1"); hh.focus({ preventScroll: true }); } return; } }
      if (sec && sec.startsWith("q-") && openAsk(sec.slice(2))) return;
      if (sec && claimById[sec.slice(2)]) { location.replace("#" + sec.slice(2)); return; }
      window.scrollTo({ top: 0 }); if (!first) focusHeading("drug"); return;
    }
    // a research page waits for its files the first time (renderMonograph), then opens where the address points
    if (sec === "evidence") { show("monograph"); setTitle((monographFor(slug) || {}).name + ": the research"); window.scrollTo({ top: 0 }); renderMonograph(slug, () => { if (!first) focusHeading("monograph"); }); return; }
    show("monograph"); setTitle((monographFor(slug) || {}).name); window.scrollTo({ top: 0 });
    renderMonograph(slug, () => {
      if (sec && sec.startsWith("q-")) { const d = document.getElementById("qa-" + sec.slice(2)); if (d) { showAllTopics(d); d.open = true; setTimeout(() => scrollToEl(d), 30); const sm = d.querySelector("summary"); if (sm) sm.focus({ preventScroll: true }); } }
      else if (sec) openSection(sec); else if (!first) focusHeading("monograph");
    });
    return;
  }
  if (h.startsWith("ref-")) { show("monograph"); renderMonograph(currentSlug, () => { const el = document.getElementById(h); if (el) el.scrollIntoView({ block: "center" }); }); return; }
  // older links without the substance (#sec-13) open that section of the page last shown
  if (h.startsWith("sec-")) { show("monograph"); setTitle((monographFor(currentSlug) || {}).name); renderMonograph(currentSlug, () => openSection(h)); return; }
  if (h.startsWith("mix-")) { renderInteractions(); show("interactions"); setTitle("Mixing drugs"); const el = document.getElementById(h); if (el) { openAround(el); scrollToEl(el); } return; }
  // Facts about drug use: #facts, #facts/q-<claim>, and a bare claim address of a general answer (a shared link)
  if (h === "facts" || h.startsWith("facts/q-") || (h.startsWith("cl_") && claimById[h] && claimById[h].substance === GEN)) {
    renderFacts(); show("facts"); setTitle(PAGE_TITLES.facts);
    const id = h.startsWith("cl_") ? h : h.startsWith("facts/q-") ? h.slice(8) : null;
    if (id && openFact(id)) { if (h.startsWith("cl_")) setTimeout(() => openEvidence(h, null, null), 60); return; }
    window.scrollTo({ top: 0 }); if (!first) focusHeading("facts"); return;
  }
  // the answers on test kits: on the drug checking page (#checking/kits, #checking/q-<claim>); a bare claim address opens there too
  if (h === "checking/kits" || h.startsWith("checking/q-") || (h.startsWith("cl_") && claimById[h] && claimById[h].substance === "drug-checking")) {
    renderDcKits(); show("checking"); setTitle("Do home test kits work?");
    const id = h.startsWith("cl_") ? h : h.startsWith("checking/q-") ? h.slice(11) : null;
    const box = document.getElementById("dc-kits"), d = id ? document.getElementById("ask-" + id) : null;
    if (d) { const more = d.closest(".asks-more"); if (more && more.hidden) { more.hidden = false; const b = document.querySelector('button.morebtn[data-more="' + more.id + '"]'); if (b) b.remove(); }
      d.open = true; setTimeout(() => scrollToEl(d), 30); const sm = d.querySelector("summary"); if (sm) sm.focus({ preventScroll: true }); }
    else if (box && !box.hidden) { setTimeout(() => scrollToEl(box), 30); const hh = box.querySelector("h2"); if (hh) { hh.setAttribute("tabindex", "-1"); hh.focus({ preventScroll: true }); } }
    else window.scrollTo({ top: 0 });
    return;
  }
  // a mixing answer's own address opens that answer in plain words, with its evidence over it (senior author, 6 November:
  // the full table opened instead, with a long paragraph "like reading the paper")
  if (h.startsWith("cl_") && claimById[h] && claimById[h].substance === "interactions") { renderInteractions(); const t = renderShared("mixing", h); show("shared"); setTitle(t || "Mixing drugs"); window.scrollTo({ top: 0 }); setTimeout(() => openEvidence(h, null, null), 60); return; }
  // a drug without a written monograph lists no claims in its full layer: an answer's own address opens its drug page with
  // the answer's evidence over it (a shared link, or one typed in)
  if (h.startsWith("cl_") && claimById[h] && subBySlug[claimById[h].substance] && (monographFor(claimById[h].substance) || {}).status === "planned") {
    const c = claimById[h]; if (renderedDrug !== c.substance) renderDrug(c.substance); show("drug"); setTitle(subBySlug[c.substance].name);
    openAsk(h); setTimeout(() => openEvidence(h, null, null), 60); return;
  }
  if (h.startsWith("cl_")) { const c = claimById[h]; if (c) { show("monograph"); setTitle((monographFor(c.substance) || {}).name); renderMonograph(c.substance, () => { const el = document.getElementById(h); if (el) { const d = el.closest("details"); if (d) d.open = true; const det = el.querySelector("details.cdetail"); if (det) det.open = true; scrollToEl(el); } }); } return; }
  if (h.startsWith("g-")) { show("glossary"); setTitle(PAGE_TITLES.glossary); const el = document.getElementById(h); if (el) scrollToEl(el); return; }
  // a country chosen in the search: #checking/c-Greece, #emergency/c-Greece, #law/c-Greece
  const cm = h.match(/^(emergency|checking|law)\/c-(.+)$/);
  if (cm) { show(cm[1]); setTitle(PAGE_TITLES[cm[1]]); window.scrollTo({ top: 0 }); openCountry(cm[1], decodeURIComponent(cm[2])); return; }
  if (!PAGE_VIEWS.includes(h) || h === "notfound" || h === "monograph") h = "home";
  show(h); setTitle(PAGE_TITLES[h]);
  // pages that read files fetched when needed draw on their first visit (speed, 13 November)
  if (h === "numbers") showNumbers();
  if (h === "howto") showHowto();
  if (h === "review") whenReady(() => Promise.all(FULL_FILES.map(loadFull).concat(loadRefs(), loadJson("decisions.json", d => Object.assign(DECISIONS, d)))), document.getElementById("review-list"), "The review queue", renderReview);
  // the Myth or fact? page: the same deck as the start page, endless (senior author, 14 November: one format everywhere)
  if (h === "quiz") { if (!MF.quizpage) mfStart("quizpage"); else mfRefresh("quizpage"); }
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
  document.getElementById("notfound-body").innerHTML = '<p>There is no page at this address' + (q ? ' (<span class="mono">' + esc(q) + "</span>)" : "") + ". " + (near.length ? "Did you mean " + near.map(s => '<a href="#s-' + s.slug + '">' + esc(s.name) + "</a>").join(" or ") + "?" : "") + '</p><p><a href="#substances">All 30 drugs</a> · use the search box above · <a href="#emergency">Emergency numbers</a></p>';
}
function show(name) {
  PAGE_VIEWS.forEach(v => { const el = document.getElementById("view-" + v); if (el) el.classList.toggle("active", v === name); });
  document.body.classList.toggle("on-emergency", name === "emergency");
  document.querySelectorAll("nav.main a, .topbar .sosbtn").forEach(a => { if (a.dataset.view === name) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
  document.querySelectorAll("details.navmore").forEach(d => { d.open = false; d.querySelector("summary").classList.toggle("cur", !!d.querySelector('a[aria-current="page"]')); });
  closeSearch(); placeSearch(name); updateSticky();
}
/* Sticky bars (senior author, 6 November: a question opened from a shared link, from "Next question" or after a refresh
   started half hidden, and he had to scroll up to read it). The top bar sticks on wide screens, a drug page's topic chips
   stick under it, and on phones the evidence page's contents bar sticks at the top. Their heights are measured: the chips
   sit right under the top bar (--bar-h), and the page's scroll padding (--stick-h) keeps every target clear of all of
   them, for our own jumps and the browser's alike. */
try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) { /* the browser keeps its own */ }
function stickyH(el) {
  if (!el || !el.getClientRects().length) return 0;
  const s = getComputedStyle(el); if (s.position !== "sticky" && s.position !== "fixed") return 0;
  const r = el.getBoundingClientRect(); return r.width > 0.6 * window.innerWidth ? Math.round(r.height) : 0;  // a side column covers nothing
}
function updateSticky() {
  const bar = stickyH(document.querySelector(".topbar"));
  const below = [".view.active .drug2 .chips", ".view.active .mono-layout > .toc"].reduce((m, q) => Math.max(m, stickyH(document.querySelector(q))), 0);
  const root = document.documentElement.style;
  root.setProperty("--bar-h", bar + "px"); root.setProperty("--stick-h", (bar + below + 10) + "px");
}
window.addEventListener("resize", () => { clearTimeout(updateSticky._t); updateSticky._t = setTimeout(updateSticky, 120); }, { passive: true });
// Scroll so that an element starts just below the sticky bars. A jump from a link or a refresh is kept in place for a
// moment while photos and fonts arrive, unless the reader scrolls first.
function scrollToEl(el, smooth) {
  if (!el || !el.getClientRects().length) return;
  updateSticky();
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  el.scrollIntoView({ block: "start", behavior: smooth && !reduce ? "smooth" : "auto" });
  if (smooth && !reduce) return;
  const ac = typeof AbortController !== "undefined" ? new AbortController() : null; let n = 0, stop = false;
  ["wheel", "touchstart", "keydown", "pointerdown"].forEach(t => window.addEventListener(t, () => { stop = true; if (ac) ac.abort(); }, ac ? { passive: true, signal: ac.signal } : { passive: true, once: true }));
  const tick = () => {
    if (stop || ++n > 15) { if (ac) ac.abort(); return; }
    updateSticky();
    const off = el.getBoundingClientRect().top - (parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0);
    if (Math.abs(off) > 3) window.scrollBy(0, off);
    setTimeout(tick, 100);
  };
  setTimeout(tick, 100);
}

/* ---------- Home ---------- */
function statTile(e) {
  const ref = refById[e.source];
  const link = ref ? (ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL) : "#";
  const srcLabel = ref ? (ref.author[0].short || ref.author[0].literal || (ref.author[0].family + (ref.author.length > 1 ? " et al." : ""))) + ", " + year(ref) : e.source;
  return '<div class="stat"><div class="value num">' + esc(e.value) + '</div><div class="label">' + esc(e.label) + '</div><div class="prov">' + esc(e.measure) + '<br>Source: <a href="' + esc(link) + '" target="_blank" rel="noopener">' + esc(srcLabel) + '</a> · <span class="badge ' + (e.status === "verified" ? "verified" : "draft") + '">' + (e.status === "verified" ? "verified" : "draft · awaiting PDF check") + "</span></div></div>";
}
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
function drugTile(s) {
  const f = fam(s.cls), names = documentedNames(s.slug).slice(0, 3), ph = headerPhoto(s.slug);
  return '<a class="dtile f-' + f.k + (ph ? " hasph" : "") + '" href="#s-' + s.slug + '">' + (ph ? '<span class="dt-ph">' + photoImg(ph, "t", "", true) + "</span>" : "") + '<span class="dt-top">' + icon(f.icon) + '<span class="dt-st ' + s.status + '">' + esc(pageStateLabel(s.slug)) + '</span></span><span class="dt-name">' + esc(s.name) + "</span>" + (names.length ? '<span class="dt-al">' + esc(names.join(" · ")) + "</span>" : "") + "</a>";
}
const POPULAR = ["cannabis", "alcohol", "mdma", "cocaine", "ketamine", "methamphetamine", "ghb-gbl", "benzodiazepines", "psilocybin", "lsd", "heroin", "fentanyl-and-analogues", "nitrous-oxide", "synthetic-cathinones"];

/* ---------- Substances ---------- */
let activeClass = "All";
function renderSubstances() {
  const classes = ["All"].concat(CLASSES.map(c => c.name).filter(n => SUBSTANCES.some(s => s.cls === n)));
  document.getElementById("filters").innerHTML = classes.map(c => '<button class="chip' + (c === "All" ? "" : " famchip f-" + fam(c).k) + '" data-cls="' + esc(c) + '" aria-pressed="' + (c === activeClass) + '">' + (c === "All" ? "" : icon(fam(c).icon)) + esc(c === "All" ? "All 30" : c) + "</button>").join("");
  document.querySelectorAll("#filters .chip").forEach(b => b.addEventListener("click", () => { activeClass = b.dataset.cls; renderSubstances(); }));
  const list = SUBSTANCES.filter(s => activeClass === "All" || s.cls === activeClass);
  document.getElementById("subgrid").innerHTML = list.map(drugTile).join("");
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
/* The currency check: newer studies found that could change a finding (pointers, not yet read) */
const TYPE_WORD = { "meta-analysis": "meta-analysis", "systematic review": "systematic review", "RCT": "randomized trial", "cohort": "cohort study", "other": "study" };
function currencyHtml(c, short) {
  const k = CURRENCY.claims && CURRENCY.claims[c.id]; if (!k) return "";
  const when = new Date(CURRENCY.checked_on + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  if (!k.yes.length) return short ? "" : '<p class="currency ok">' + icon("search") + "Searched for newer research on " + esc(when) + ": no newer study found that is likely to change this (titles and abstracts screened" + (k.maybe ? "; " + k.maybe + " related " + (k.maybe === 1 ? "study" : "studies") + " listed for reading" : "") + ").</p>";
  const unread = k.yes.filter(x => !x.read && !x.checking), checking = k.yes.filter(x => x.checking), done = k.yes.filter(x => x.read);
  const readOn = done.length ? new Date(done[0].read + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) : "";
  const listOf = xs => xs.map(x => '<a href="https://doi.org/' + esc(x.doi) + '" target="_blank" rel="noopener">' + esc(String(x.first_author || "").split(" ")[0]) + " et al., " + esc(x.year) + "</a> (" + esc(TYPE_WORD[x.type] || x.type) + ")").join("; ");
  if (checking.length && !unread.length) return '<p class="currency new">' + icon("alert") + (short ? "Newer research may change this answer: " + checking.length + " newer " + (checking.length === 1 ? "study has" : "studies have") + " been read and " + (checking.length === 1 ? "is" : "are") + " being checked." : "Newer research found on " + esc(when) + " has been read and is being checked by a second reader before it is added: " + listOf(checking) + "." + (done.length ? " Already added: " + listOf(done) + "." : "")) + "</p>";
  if (!unread.length) return short ? "" : '<p class="currency ok">' + icon("search") + "Searched for newer research on " + esc(when) + ": " + (done.length === 1 ? "the newer study found was" : "the " + done.length + " newer studies found were") + " read in full on " + esc(readOn) + " and added here: " + listOf(done) + ".</p>";
  return '<p class="currency new">' + icon("alert") + (short ? "Newer research may change this answer: " + unread.length + " newer " + (unread.length === 1 ? "study" : "studies") + " not yet read" + (done.length ? " (" + done.length + " more already read and added)" : "") + "." : "Newer research that could change this finding was found on " + esc(when) + " and has not yet been read: " + listOf(unread) + "." + (done.length ? " Read in full on " + esc(readOn) + " and added here: " + listOf(done) + "." : "")) + "</p>";
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
    '<div class="evid" id="ev-' + c.id + '" hidden>' + ev + "</div>" +
    "</details>" +
    currencyHtml(c) +
    '<div class="stampline"><span class="senior-slot" data-senior="' + c.id + '"></span><span class="verif" title="Verification step: ' + esc(LADDER_WORDS[c.verification.status] || c.verification.status) + ' (Methods, verification ladder)">' + esc(readerStamp(c.verification.status, c)) + " · v" + esc(c.version) + "</span></div>" +
    "</article>";
}
function debateHtml(d) {
  return '<section class="debate"><header><span class="badge contested">contested</span><h3>' + esc(d.question) + "</h3></header>" +
    '<div class="cols"><div class="col yes"><h4>Strongest evidence for yes</h4>' + inPieces(d.evidence_yes, liveCites) + '</div><div class="col no"><h4>Strongest evidence for no</h4>' + inPieces(d.evidence_no, liveCites) + "</div></div>" +
    '<div class="full"><h4>What neither side\'s evidence can show</h4>' + inPieces(d.neither_can_show, liveCites) + "</div>" +
    '<div class="full reading"><h4>The editors\' reading</h4>' + inPieces(d.editors_reading, liveCites) + "</div>" +
    '<div class="full"><h4>What would settle it</h4>' + inPieces(d.what_would_settle_it, liveCites) + "</div></section>";
}


/* ---------- Sections 2 and 13: identity and legal status (sourced facts, not graded claims) ---------- */
const READ_VIA = { WebFetch: "WebFetch", browser: "the app's browser", PDF: "the PDF on file" };
const PUB_SHORT = { "National Institute of Standards and Technology (NIST)": "NIST Chemistry WebBook", "WHO Collaborating Centre for Drug Statistics Methodology": "WHO ATC/DDD Index", "European Union Drugs Agency (EUDA)": "EUDA", "U.S. Drug Enforcement Administration": "DEA", "Australian Institute of Health and Welfare": "AIHW", "National Center for Biotechnology Information (PubChem)": "PubChem", "U.S. Drug Enforcement Administration, Diversion Control Division (Drug & Chemical Evaluation Section)": "DEA Diversion Control Division", "U.S. National Institute on Drug Abuse": "NIDA", "International Narcotics Control Board (copy held by the HRB National Drugs Library, Ireland)": "INCB", "DailyMed, U.S. National Library of Medicine": "DailyMed", "U.S. Food and Drug Administration": "FDA", "Office of the Federal Register (eCFR)": "eCFR", "European Medicines Agency": "EMA", "European Monitoring Centre for Drugs and Drug Addiction (now EUDA)": "EMCDDA", "European Monitoring Centre for Drugs and Drug Addiction (now EUDA); Publications Office of the European Union": "EMCDDA", "U.S. Drug Enforcement Administration (Federal Register, via govinfo.gov)": "Federal Register" };
function titleShort(t) { return String(t || "").replace(/^(ATC\/DDD Index|eCFR|Alcohol, tobacco & other drugs in Australia): /, "").split(" (CAS")[0].split(", NIST")[0].split(", PubChem")[0].split(" (")[0]; }
function srcLinks(ids, srcs) {
  const list = (ids || []).map(id => srcs.find(x => x.id === id) || { id: id });
  const pub = s => PUB_SHORT[s.publisher] || s.publisher || "";
  const pubs = list.map(pub), dup = p => p && pubs.filter(x => x === p).length > 1;
  return list.map(s => {
    if (!s.url) return esc(s.id);
    const when = (String(s.date || "").match(/^(?:19|20)\d\d(?:-\d\d){0,2}\b/) || [""])[0]; // only a date the source itself carries (not "Undated (bibliography to 2006)")
    const label = !pub(s) ? s.title : dup(pub(s)) ? pub(s) + ": " + titleShort(s.title) : pub(s);
    const tip = (s.publisher ? s.publisher + ". " : "") + s.title + (s.date ? " (" + s.date + ")" : "") + (s.read_via ? " · read through " + (READ_VIA[s.read_via] || s.read_via) : "") + (s.accessed ? " on " + s.accessed : "");
    return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener" title="' + esc(tip) + '">' + esc(label) + (when ? ", " + esc(when) : "") + "</a>";
  }).join("; ");
}
function identityHtml(slug) {
  const d = IDENTITY.find(x => x.substance === slug); if (!d) return "";
  const n = d.names || {}; const S = d.sources || [];
  const rows = [["INN", n.inn], ["IUPAC name", n.iupac], ["CAS numbers", n.cas, "<br>"], ["Formula", n.formula], ["Molar mass", n.molar_mass], ["Synonyms", n.synonyms, "; "]].filter(r => r[1] && r[1].length).map(r => [r[0], Array.isArray(r[1]) ? r[1].map(esc).join(r[2]) : esc(r[1])]);
  const via = [...new Set(S.map(s => s.read_via).filter(Boolean))];
  // what a reader looks for first: the names people use, what it looks like, what drug checking found; then the chemistry
  let h = '<div class="facts">';
  if ((d.members || []).length) h += '<p class="covers"><b>This page covers:</b> ' + d.members.map(mb => esc(mb.name)).join(", ") + ".</p>";
  if ((d.street_names || []).length) h += "<h3>Street names, as documented by monitoring bodies</h3><ul>" + d.street_names.map(f => "<li>" + esc(f.names.join(", ")) + " — " + esc(f.region) + (f.period ? ", " + esc(f.period) : "") + ' <span class="src">(' + srcLinks(f.source_ids, S) + ")</span></li>").join("") + "</ul>";
  if ((d.forms || []).length) h += "<h3>Forms</h3><ul>" + d.forms.map(f => "<li><b>" + esc(f.form) + "</b>" + (f.detail ? " — " + esc(f.detail) : "") + ' <span class="src">(' + srcLinks(f.source_ids, S) + ")</span></li>").join("") + "</ul>";
  const dc = (d.drug_checking || []).filter(f => !f.hold), held = (d.drug_checking || []).length - dc.length;
  if (dc.length) h += "<h3>What drug checking has found</h3><ul>" + dc.map(f => "<li>" + esc(f.finding) + (f.where_when ? " — " + esc(f.where_when) : "") + ' <span class="src">(' + srcLinks(f.source_ids, S) + ")</span></li>").join("") + "</ul>";
  if (held) h += (dc.length ? "" : "<h3>What drug checking has found</h3>") + '<p class="note">' + held + " finding" + (held === 1 ? "" : "s") + " from drug-checking papers " + (held === 1 ? "is" : "are") + " held back until " + (held === 1 ? "its paper has" : "their papers have") + " been read in full text (Methods §12.1).</p>";
  h += '<details class="chem"><summary>Chemical names and identifiers (for chemists and clinicians)</summary>';
  if (rows.length) h += '<div class="tablewrap"><table class="kv">' + rows.map(r => "<tr><th>" + esc(r[0]) + "</th><td>" + r[1] + "</td></tr>").join("") + (n.source_ids ? '<tr><th>Source</th><td>' + srcLinks(n.source_ids, S) + "</td></tr>" : "") + "</table></div>";
  if ((d.members || []).length) h += "<h3>Members covered on this page</h3>" + '<div class="tablewrap"><table class="members"><tr><th>Substance</th><th>CAS number</th><th>Formula</th><th>Molar mass</th><th>Source</th></tr>' + d.members.map(mb => '<tr><td data-label="Substance"><b>' + esc(mb.name) + "</b>" + (mb.inn ? '<div class="muted small">' + (/^INN\b/.test(mb.inn) ? "" : "INN: ") + esc(mb.inn) + "</div>" : "") + ((mb.synonyms || []).length ? '<div class="muted small">Also: ' + mb.synonyms.map(esc).join("; ") + "</div>" : "") + (mb.note ? '<div class="muted small">' + esc(mb.note) + "</div>" : "") + '</td><td data-label="CAS number">' + (mb.cas || []).map(esc).join("<br>") + '</td><td data-label="Formula">' + esc(mb.formula || "") + '</td><td data-label="Molar mass">' + esc(mb.molar_mass || "") + '</td><td data-label="Source"><span class="src">' + srcLinks(mb.source_ids, S) + "</span></td></tr>").join("") + "</table></div>";
  h += "</details>";
  h += '<details class="srcnote howchecked"><summary>How these facts were checked</summary><div class="muted small">Sourced facts, not graded claims. Each item names its source (point at a source for its title and how it was read). ' + (via.length === 1 && via[0] === "WebFetch" ? "The pages were read through WebFetch, a fetch tool that answers through a summarizing model (Methods §12.1). " : "") + (d.verification === "ai-checked" ? "A second AI reader then re-read every page without seeing this section and confirmed each item, or corrected it (checked " + esc(d.checked_on || "") + "); the senior author has not yet checked it." : "The section stays a draft until a second reader and the senior author have checked it (compiled " + esc(d.compiled_on) + ").") + "</div></details>";
  return h + "</div>";
}

function gapsHtml(slug) {
  const cl = CLAIMS.filter(c => c.substance === slug);
  const deb = cl.filter(c => c.debate);
  const cs = Object.entries(STUDY_CARDS).filter(([id, k]) => k.substance === slug && k.what_would_settle_it);
  const m = monographFor(slug) || MONO; const s15 = (m.sections || []).find(x => x.number === 15) || {};
  const pq = s15.priority_questions || [];
  if (!deb.length && !cs.length && !pq.length) return "";
  let h = '<div class="facts">';
  if (pq.length) h += "<h3>Priority questions this page cannot yet answer</h3><ol>" + pq.map(q => "<li><b>" + esc(q.question) + "</b><br>Needs: " + esc(q.needs) + "</li>").join("") + "</ol>" + (s15.not_yet_covered ? '<p><b>Not yet covered on this page:</b> ' + esc(s15.not_yet_covered) + "</p>" : "") + (s15.no_evidence_note ? '<p class="note">' + esc(s15.no_evidence_note) + "</p>" : "");
  h += '<p class="note">Generated from the debate boxes and the study cards: the studies that have not been done and would answer the open questions. They are also the encyclopedia\'s research agenda.</p>';
  if (deb.length) h += "<h3>The contested questions</h3><ol>" + deb.map(c => '<li><b><a href="#' + c.id + '">' + esc(c.debate.question) + "</a></b><br>" + esc(c.debate.what_would_settle_it) + "</li>").join("") + "</ol>";
  const weak = cl.filter(c => c.grade.certainty === "very-low" && !c.debate);
  if (weak.length) h += "<h3>Questions where the evidence is of very low certainty</h3><ul>" + weak.map(c => '<li><a href="#' + c.id + '">' + esc(c.outcome.charAt(0).toUpperCase() + c.outcome.slice(1)) + "</a> — " + esc(c.population) + ' <span class="muted small">(section ' + c.section + (c.verification.status === "draft" ? ", draft" : "") + ")</span></li>").join("") + "</ul>";
  if (cs.length) h += "<details><summary>What each study card says would settle its question (" + cs.length + ")</summary><ul>" + cs.map(([id, k]) => "<li>" + esc(k.what_would_settle_it) + ' <span class="src">(' + cite(k.reference) + ")</span></li>").join("") + "</ul></details>";
  return h + "</div>";
}
function legalOrder(entries) { const rank = e => /United Nations/.test(e.jurisdiction) ? 0 : /European Union/.test(e.jurisdiction) ? 1 : 2; return entries.slice().sort((a, b) => rank(a) - rank(b) || a.jurisdiction.localeCompare(b.jurisdiction)); }
function legalRow(e) {
  return '<tr><td data-label="Status">' + esc(e.status) + (e.note ? '<details class="srcnote"><summary>How this row was read</summary><div class="muted small">' + esc(e.note) + "</div></details>" : "") + '</td><td data-label="Instrument"><a href="' + esc(e.source_url) + '" target="_blank" rel="noopener">' + esc(e.instrument) + "</a>" + (e.source_date ? '<div class="muted small">' + esc(e.source_date) + "</div>" : "") + '</td><td data-label="Medical use"' + (e.medical_use ? "" : ' class="empty"') + '>' + esc(e.medical_use || "—") + '</td><td data-label="Checked">' + esc(e.checked_on) + '<div class="muted small"' + (e.checked_by ? ' title="' + esc(e.checked_by) + '"' : "") + '>' + esc(e.verification) + "</div></td></tr>";
}
function legalHtml(slug) {
  const d0 = LEGAL.find(x => x.substance === slug); if (!d0) return ""; const entries = legalOrder(d0.entries);
  // one group per jurisdiction: the UN and the EU open, each country folded (pick your country above to see it at once)
  const groups = []; entries.forEach(e => { const g = groups[groups.length - 1]; if (g && g.j === e.jurisdiction) g.rows.push(e); else groups.push({ j: e.jurisdiction, rows: [e] }); });
  const head = "<tr><th>Status</th><th>Instrument</th><th>Medical use</th><th>Checked</th></tr>";
  return '<div class="facts">' + countryLawHtml(slug, "ctry-full") + '<p class="note">What each law or official list says, on the day we checked. Not legal advice: laws change, and the official text is what counts. \u201cNot found\u201d means we could not check every list, not that the drug is legal there.</p>' +
    '<details class="lawmore"><summary>How we checked</summary><p class="note">Each row says how far it was checked: draft (read once), ai-checked (read twice, and both readings agreed) or senior-verified (checked by the senior author). ' + groups.length + " countries and bodies, read on " + esc(d0.compiled_on) + ".</p></details>" +
    groups.map(g => '<details class="lawgrp"' + (/United Nations|European Union/.test(g.j) ? " open" : "") + "><summary><b>" + esc(g.j) + '</b> <span class="muted small">' + g.rows.length + (g.rows.length === 1 ? " row" : " rows") + '</span></summary><div class="tablewrap"><table>' + head + g.rows.map(legalRow).join("") + "</table></div></details>").join("") + "</div>";
}

function glanceItem(id) {
  const c = claimById[id]; if (!c) return "";
  return '<li><p>' + esc(claimText(c)) + '</p><div class="qmeta">' + meterHtml(c.grade.certainty, true) + '<span class="badge ' + c.status + '">' + esc(statusLabel(c.status)) + '</span><a class="see" href="#' + id + '">See the evidence ' + icon("arrow") + "</a></div></li>";
}

/* ---------- Quick answers: the reader's first layer of a drug page ---------- */
const FORM_ICON = [[/crystal/i, "crystal"], [/powder/i, "powder"], [/capsule/i, "capsule"], [/tablet|pill/i, "tablet"], [/blotter|paper/i, "blotter"], [/liquid|solution/i, "drop"], [/mushroom|fruiting/i, "mushroom"], [/cact/i, "cactus"], [/leaf|leaves|herb|plant/i, "leaf"], [/resin|hash/i, "block"], [/\bgas\b|canister|cartridge|charger/i, "canister"]];
function formIcon(name) { for (const [re, ic] of FORM_ICON) if (re.test(name)) return ic; return null; }
// the first statement of a sourced row (up to its first ";" or full stop); the full row is one tap away in section 13
function firstClause(t) { return String(t || "").split(/;\s|\.\s/)[0].replace(/\.$/, ""); }
function basicsHtml(m) {
  const base = "#s-" + m.slug + "/", d = IDENTITY.find(x => x.substance === m.slug), L = LEGAL.find(x => x.substance === m.slug), figs = figuresFor(m.slug);
  const more = (sec, label) => '<a class="more" href="' + base + sec + '">' + esc(label) + " " + icon("arrow") + "</a>";
  const cards = [];
  // What it looks like: every form people meet (data/site/forms.json), each with what it is, its sources and a photo where a free
  // one exists; with photos hidden, each form shows its symbol
  const FM = FORMS[m.slug] || [], phById = Object.fromEntries(PHOTOS.map(p => [p.id, p])), S = d ? d.sources || [] : [];
  if (FM.length) {
    const tile = f => { const p = (f.photos || []).map(id => phById[id]).find(Boolean);
      return '<li class="ftile' + (p ? " hasph" : "") + '">' + (p ? '<span class="ft-ph">' + photoImg(p, "t", null, true) + "</span>" : "") + '<span class="ft-ic">' + icon(ICONS[f.icon] ? f.icon : "tag", "big") + "</span>" +
        '<span class="ft-t"><b>' + esc(f.name) + "</b>" + esc(f.what) + (f.src && f.src.length && S.length ? ' <span class="src">(' + srcLinks(f.src, S) + ")</span>" : "") + "</span>" + (p ? photoCredit(p) : "") + "</li>"; };
    const anyPh = FM.some(f => (f.photos || []).some(id => phById[id]));
    cards.push('<section class="bcard wide phcard" id="ph-' + esc(m.slug) + '"><h3>' + icon("tag") + "What it looks like</h3>" + '<ul class="ftiles">' + FM.map(tile).join("") + "</ul>" +
      '<p class="phnote">' + (anyPh ? '<span class="ph-only">Each photo is one example. ' + (FM.some(f => (f.photos || []).some(id => phById[id] && phById[id].medicine_example)) ? "Medicines look different from one maker and one country to another. " : "") + "</span>" : "") + 'The same drug can look different, and different drugs can look the same: <a href="#checking">looks don’t tell you what’s inside</a>.' + (anyPh ? " " + phToggle() : "") + "</p>" +
      (d ? more("sec-2", "Names, forms and their sources") : "") + "</section>");
  } else if (d) {
    const forms = (d.forms || []).map(f => [f, formIcon(f.form)]).filter(p => p[1]);
    if (forms.length) cards.push('<section class="bcard"><h3>' + icon("tag") + 'What it looks like</h3><ul class="forms">' + forms.map(([f, ic]) => "<li>" + icon(ic, "big") + "<span>" + esc(f.form) + "</span></li>").join("") + "</ul>" + more("sec-2", "Names, forms and their sources") + "</section>");
  }
  if (d) {
    const dc = (d.drug_checking || []).filter(f => !f.hold);
    if (dc.length) cards.push('<section class="bcard wide"><h3>' + icon("flask") + 'What drug checking has found</h3><ul class="dc">' + dc.map(f => "<li>" + esc(f.finding) + (f.where_when ? '<span class="where-when">' + esc(f.where_when) + "</span>" : "") + "</li>").join("") + "</ul>" + '<a class="more" href="#checking">Find a drug-checking service ' + icon("arrow") + "</a>" + more("sec-2", "Sources") + "</section>");
  }
  if (L && L.entries.length) cards.push('<section class="bcard"><h3>' + icon("scale") + 'The law</h3><ul class="law">' + legalOrder(L.entries).filter(e => /United Nations|European Union/.test(e.jurisdiction)).slice(0, 4).map(e => "<li><b>" + esc(e.jurisdiction) + "</b><span>" + esc(firstClause(e.status)) + "</span></li>").join("") + "</ul>" + countryLawHtml(m.slug, "ctry-quick") + more("sec-13", "Every country we have read, in full, with sources") + "</section>");
  if (figs.length) { const top = topFigures(m.slug, 3);
    cards.push('<section class="bcard"><h3>' + icon("chart") + 'Official figures</h3>' + (top.length ? '<ul class="figmini">' + top.map(r => { const f = figParts(r); return '<li><b class="num">' + esc(fmtValue(r)) + "</b><span>" + esc(f.what) + " · " + esc(f.place.replace(/^Worldwide$/, "worldwide")) + ", " + esc(figYear(r)) + "</span></li>"; }).join("") + "</ul>" : '<p class="note">No figures yet for ' + (PREF_COUNTRY ? esc(shortCtry(PREF_COUNTRY)) + " or " : "") + "the world as a whole.</p>") +
      more("sec-10", top.length < figs.length ? "All " + figs.length + " figures, by place, with sources" : "Sources") + "</section>"); }
  return cards.length ? '<h2 class="qh">The basics</h2><div class="bgrid">' + cards.join("") + "</div>" : "";
}
function questionFor(slug, id) { for (const g of QUESTIONS[slug] || []) for (const [cid, q] of g.items) if (cid === id) return q; return null; }
function qlinkItem(slug, id) {
  const c = claimById[id]; if (!c) return ""; const q = questionFor(slug, id);
  if (!q) return glanceItem(id);
  return '<li><button type="button" class="qlink" data-q="' + c.id + '">' + esc(q) + "</button>" + meterHtml(c.grade.certainty, true) + "</li>";
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("button.qlink"); if (!b) return;
  const d = document.getElementById("qa-" + b.dataset.q); if (!d) return;
  showAllTopics(d); d.open = true; scrollToEl(d, true); const sm = d.querySelector("summary"); if (sm) sm.focus({ preventScroll: true });
});
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
/* ---------- Key facts: a few cards first (bottom line first; about four things at a time; swipe through) ---------- */
function deckHtml(m) {
  const g = m.at_a_glance; if (!g) return "";
  const items = (g.best_established || []).map(id => ["known", id]).concat((g.largest_uncertainties || []).map(id => ["open", id])).filter(([, id]) => claimById[id]);
  if (!items.length) return "";
  const card = ([kind, id], i) => { const c = claimById[id], sp = (SIMPLE.claims || {})[id], q = questionFor(m.slug, id) || "";
    return '<article class="kf ' + kind + '" data-i="' + i + '"' + (i ? " hidden" : "") + ' aria-label="Fact ' + (i + 1) + " of " + items.length + '">' +
      '<p class="kf-k">' + (kind === "known" ? icon("check") + "What studies found" : icon("alert") + "Not known yet") + '<span class="kf-n">' + (i + 1) + " / " + items.length + "</span></p>" +
      (q ? '<p class="kf-q">' + esc(q) + "</p>" : "") + '<p class="kf-a">' + esc(sp ? sp.short : (claimText(c))) + "</p>" +
      (sp ? '<p class="kf-but"><b>But</b> ' + esc(sp.but) + "</p>" : "") +
      '<div class="kf-f">' + meterHtml(c.grade.certainty, true) + '<button type="button" class="qlink kf-go" data-q="' + id + '">See why ' + icon("arrow") + "</button></div></article>"; };
  return '<section class="deck" aria-label="Key facts" tabindex="-1"><div class="deck-h"><h2 class="qh">' + items.length + ' key facts</h2><p class="muted small">Swipe, or use the arrows.</p></div>' +
    '<div class="deck-cards" aria-live="polite">' + items.map(card).join("") + "</div>" +
    '<div class="deck-nav"><button type="button" class="deck-btn" data-d="-1" aria-label="Previous fact">' + icon("arrow") + '</button><span class="deck-dots" aria-hidden="true">' + items.map((_, i) => "<i" + (i ? "" : ' class="on"') + "></i>").join("") + '</span><button type="button" class="deck-btn next" data-d="1" aria-label="Next fact">' + icon("arrow") + "</button></div></section>";
}
function deckGo(deck, d) {
  const cards = [...deck.querySelectorAll(".kf")], cur = cards.findIndex(c => !c.hidden), n = (cur + d + cards.length) % cards.length;
  cards.forEach((c, i) => { c.hidden = i !== n; }); deck.querySelectorAll(".deck-dots i").forEach((dot, i) => dot.classList.toggle("on", i === n));
}
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".deck-btn"); if (b) deckGo(b.closest(".deck"), +b.dataset.d); });
document.addEventListener("keydown", e => { const deck = e.target.closest && e.target.closest(".deck"); if (!deck || (e.key !== "ArrowLeft" && e.key !== "ArrowRight")) return; e.preventDefault(); deckGo(deck, e.key === "ArrowLeft" ? -1 : 1); });
let deckTouchX = null;
document.addEventListener("touchstart", e => { if (e.target.closest && e.target.closest(".deck-cards")) deckTouchX = e.touches[0].clientX; }, { passive: true });
document.addEventListener("touchend", e => { if (deckTouchX == null) return; const dx = e.changedTouches[0].clientX - deckTouchX; const deck = e.target.closest && e.target.closest(".deck"); deckTouchX = null; if (deck && Math.abs(dx) > 40) deckGo(deck, dx < 0 ? 1 : -1); }, { passive: true });
/* ---------- Answers opened so far, kept in this browser only (a small reward for exploring) ---------- */
function readSet(slug) { try { return new Set(JSON.parse(localStorage.getItem("pk-read-" + slug) || "[]")); } catch (e) { return new Set(); } }
function markRead(slug, id) { const r = readSet(slug); if (r.has(id)) return r; r.add(id); try { localStorage.setItem("pk-read-" + slug, JSON.stringify([...r])); } catch (e) { /* not kept */ } return r; }
function progressHtml(slug, total) { const n = [...readSet(slug)].filter(id => claimById[id]).length; return '<div class="readprog" data-total="' + total + '"><div class="rp-bar" aria-hidden="true"><i style="width:' + Math.round(100 * n / Math.max(1, total)) + '%"></i></div><span class="rp-t">You have opened <b>' + n + "</b> of " + total + " answers</span></div>"; }
function updateProgress(slug) { document.querySelectorAll("#quick .readprog").forEach(el => { const total = +el.dataset.total, n = [...readSet(slug)].filter(id => claimById[id]).length; el.querySelector(".rp-bar i").style.width = Math.round(100 * n / Math.max(1, total)) + "%"; el.querySelector(".rp-t").innerHTML = "You have opened <b>" + n + "</b> of " + total + " answers" + (n === total ? " — all of them!" : ""); }); }
document.addEventListener("toggle", e => { const d = e.target; if (!(d.matches && d.matches("details.qa")) || !d.open) return; const id = d.id.replace(/^qa-/, ""); const c = claimById[id]; if (!c) return; markRead(c.substance, id); updateProgress(c.substance); }, true);
/* ---------- Topics: show one group of questions at a time (fewer choices on screen) ---------- */
function showAllTopics(d) { const g = d && d.closest(".qgroup"); if (g && g.hidden) { const all = document.querySelector('#quick .tchip[data-t="all"]'); if (all) all.click(); } }
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".tchip"); if (!b) return; const t = b.dataset.t;
  document.querySelectorAll(".tchip").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  document.querySelectorAll("#quick .qgroup").forEach(g => { g.hidden = t !== "all" && g.dataset.t !== t; }); });
/* "I barely felt it": checked answers on why some people feel little and take more, and what happens then (writing rule 0) */
function feelLittleHtml(slug) {
  const ids = ((typeof FEEL_LITTLE !== "undefined" && FEEL_LITTLE[slug]) || []).filter(id => claimById[id] && (SIMPLE.claims || {})[id]);
  if (ids.length < 2) return "";
  return '<section class="feellittle" aria-labelledby="fl-h"><h2 class="qh" id="fl-h">' + icon("pulse") + "\u201cI barely felt it\u201d</h2><p class=\"qsub muted\">" + esc(FEEL_LITTLE.intro) + '</p><ul class="fl-list">' + ids.map(id => '<li><span>' + esc(SIMPLE.claims[id].short) + '</span> <button type="button" class="qlink" data-q="' + id + '">How we know</button></li>').join("") + "</ul></section>";
}
function quickHtml(m) {
  // a topic whose answers are all still waiting for a second reader is not shown yet
  const groups = QUESTIONS[m.slug] ? QUESTIONS[m.slug].filter(g => g.items.some(([id]) => claimById[id])) : null;
  let h = deckHtml(m) + feelLittleHtml(m.slug);
  if (groups) { const total = groups.reduce((a, g) => a + g.items.filter(([id]) => claimById[id]).length, 0);
    h += '<h2 class="qh">Questions people ask</h2><p class="qsub muted">Pick a topic, then tap a question.</p>' +
      '<div class="tchips" role="group" aria-label="Topics"><button type="button" class="tchip" data-t="all" aria-pressed="true">All</button>' + groups.map((gr, i) => '<button type="button" class="tchip" data-t="' + i + '" aria-pressed="false">' + icon(gr.icon) + esc(gr.topic) + "</button>").join("") + "</div>" +
      progressHtml(m.slug, total) +
      groups.map((gr, i) => '<section class="qgroup" data-t="' + i + '"><h3>' + icon(gr.icon) + esc(gr.topic) + "</h3>" + (gr.sos ? sosLine() : "") + gr.items.map(([id, q]) => { const c = claimById[id]; return c ? qaHtml(c, q) : ""; }).join("") + "</section>").join(""); }
  h += basicsHtml(m);
  if (!groups && PLANNED_QUESTIONS[m.slug]) h += '<h2 class="qh">Questions this page will answer</h2><p class="qsub muted">Not answered yet: each needs its papers read in full first.</p><ol class="plannedq">' + PLANNED_QUESTIONS[m.slug].map(q => "<li>" + esc(q) + "</li>").join("") + "</ol>";
  h += familyHtml(m);
  return h;
}
/* Two layers on every drug page: Quick answers (default) and Full evidence; the reader's choice is remembered */
let PREF_MODE = (() => { try { return localStorage.getItem("pk-mode") === "full" ? "full" : "quick"; } catch (e) { return "quick"; } })();
function setMode(mode, remember) {
  const md = mode === "full" ? "full" : "quick", v = document.getElementById("view-monograph");
  if (v) v.dataset.mode = md;
  document.querySelectorAll(".modebtn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === md)));
  if (remember) { PREF_MODE = md; try { localStorage.setItem("pk-mode", md); } catch (e) { /* no storage: the choice lasts for this visit */ } }
}
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".modebtn"); if (b) setMode(b.dataset.mode, true); });
// "All its forms" under the page photo: the gallery is in Quick answers
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("[data-phall]"); if (!b) return; setMode("quick"); const el = document.getElementById("ph-" + b.dataset.phall); if (el) scrollToEl(el, true); });

/* ---------- Monograph ---------- */
const isPhone = () => !!(window.matchMedia && window.matchMedia("(max-width: 700px)").matches);
const isWide = () => !!(window.matchMedia && window.matchMedia("(min-width: 1000px)").matches);
function sosLine() { return '<p class="sosline">Someone unwell? Call your local emergency number. <a href="#emergency">Numbers by country</a></p>'; }
function sectionHasContent(m, x) {
  return !!(x.claims.filter(id => claimById[id]).length || (x.number === 10 && figureCount(m.slug)) || (x.number === 2 && IDENTITY.some(d => d.substance === m.slug)) || (x.number === 13 && LEGAL.some(d => d.substance === m.slug)) || (x.number === 15 && m.status !== "planned") || (x.number === 14 && m.status === "planned" && PLANNED_QUESTIONS[m.slug]));
}
// A research page reads its claims' full text, the references in full and the official figures: the first visit shows the
// drug's name and a quiet line while those files arrive (speed, 13 November), later visits draw at once. "then" runs once the
// page is drawn (to open a section or a claim), and not at all if the reader has gone elsewhere meanwhile.
let MONO_WANT = null;
function renderMonograph(slug, then) {
  const m = monographFor(slug) || MONO; MONO_WANT = m.slug; currentSlug = m.slug;
  const ids = m.sections.flatMap(x => x.claims).filter(id => claimById[id]);
  const done = () => { if (MONO_WANT !== m.slug) return; if (renderedSlug !== m.slug) drawMonograph(m.slug); if (then) then(); };
  if (renderedSlug === m.slug || (fullReady(ids, [m.slug]) && FIGURES_DONE)) { done(); return; }
  renderedSlug = null;
  document.getElementById("mono-title").textContent = m.name;
  ["crumbs", "mono-eyebrow", "mono-inn", "mono-status", "mono-notice", "quick", "mono-meta", "mono-tags", "toc"].forEach(id => { const el = document.getElementById(id); if (el) el.innerHTML = ""; });
  const mp = document.getElementById("mono-photo"); if (mp) mp.hidden = true;
  const tg = document.getElementById("toggle-detail"); if (tg) tg.hidden = true;
  whenReady(() => Promise.all([needFull(ids, [m.slug]), loadFigures()]), document.getElementById("sections"), "The research on " + m.name, done);
}
function drawMonograph(slug) {
  const m = monographFor(slug) || MONO; currentSlug = m.slug; renderedSlug = m.slug;
  const planned = m.status === "planned", base = "#s-" + m.slug + "/";
  const s = subBySlug[m.slug]; const em = s ? EVIDENCE_MAPS[s.folder] : null;
  document.getElementById("crumbs").innerHTML = '<a href="#home">Home</a> › <a href="#substances">Find a drug</a> › <span>' + esc(m.classes[0]) + "</span> › <b>" + esc(m.name) + "</b>";
  document.getElementById("mono-eyebrow").innerHTML = m.classes.map(famChip).join(" ");
  document.getElementById("mono-title").textContent = m.name;
  // the drug itself, in place of a symbol: one example of its commonest form, with its credit
  const hp = headerPhoto(m.slug), mp = document.getElementById("mono-photo");
  if (mp) {
    mp.hidden = !hp; mp.closest(".mono-head").classList.toggle("hasphoto", !!hp);
    mp.innerHTML = hp ? photoImg(hp, "m", null, false) + "<figcaption><b>" + esc(hp.form) + "</b>" + (hp.detail ? ' <span class="muted">' + esc(hp.detail) + "</span>" : "") + '<span class="phmore">One example. ' + (photosFor(m.slug).length > 1 ? '<button type="button" class="linklike" data-phall="' + esc(m.slug) + '">All its forms</button> · ' : "") + phToggle() + "</span>" + photoCredit(hp) + "</figcaption>" : "";
  }
  document.getElementById("mono-inn").textContent = m.inn ? "INN: " + m.inn : "";
  document.getElementById("mono-status").innerHTML = '<span class="badge ' + (planned ? "planned" : "draft") + '">' + esc(planned ? pageStateLabel(m.slug) : "Version " + m.version) + "</span>";
  const now = [];
  if (IDENTITY.some(d => d.substance === m.slug)) now.push('<a href="' + base + 'sec-2">Names and street names</a>');
  if (figuresFor(m.slug).length) now.push('<a href="' + base + 'sec-10">Official figures</a>');
  if (LEGAL.some(d => d.substance === m.slug)) now.push('<a href="' + base + 'sec-13">Legal status</a>');
  if (planned && PLANNED_QUESTIONS[m.slug]) now.push('<a href="' + base + 'sec-14">Open questions</a>');
  document.getElementById("mono-notice").innerHTML = (planned
    ? (hasQuickAnswers(m.slug)
      ? '<p class="notice"><b>Answers so far:</b> answers to questions people ask, each checked against its sources by a second AI reader, and names, official figures and legal status. The full write-up is not finished yet. Nothing here is medical advice.</p>'
      : '<p class="notice"><b>Basics only so far:</b> names and street names, official figures and legal status, each checked against official sources. The research sections are not written yet. Nothing here is medical advice.</p>')
    : '<p class="notice">This page describes research; it is not medical advice. <a href="#about">How this page was made</a></p>');
  document.getElementById("quick").innerHTML = quickHtml(m);
  document.getElementById("mono-meta").innerHTML = "<span>Last systematic search: <b>" + (m.dates.last_search || "not yet run") + "</b></span><span>Last senior review: <b>" + (m.dates.last_review || "none") + "</b></span><span>Reading list: <b>" + (em ? em.papers + " papers (" + em.tierA + " priority)" : "in preparation") + "</b></span><span>Read in full: <b>" + (function () { const cs = Object.values(STUDY_CARDS).filter(k => k.substance === m.slug); const pdf = cs.filter(k => /^PDF/.test((k.verification || {}).source_read || "")).length; const web = cs.filter(k => ((k.verification || {}).source_read || "") && !/^PDF/.test(k.verification.source_read) && !/^abstract/i.test(k.verification.source_read)).length; return (pdf + web) + " papers (" + pdf + " from PDFs, " + web + " from PubMed Central or the publisher)"; })() + "</b></span><span>Authors: <b>" + m.authors.map(a => a.name).join("; ") + "</b></span><span>Conflicts of interest: <b>" + m.authors.map(a => a.name + ", " + (a.coi || "not stated").toLowerCase()).join("; ") + "</b></span><span>AI assistance: <b>first-pass extraction, appraisal and drafting by Claude (Anthropic), and for some answers in November 2026 by ChatGPT (OpenAI), checked by a second AI reader and, before publication, by the senior author (Methods)</b></span>";
  const dn = documentedNames(m.slug);
  document.getElementById("mono-tags").innerHTML = dn.length ? '<span class="also">Also called</span>' + dn.map(a => '<span class="tag street" title="Documented by at least two monitoring bodies (section 2)">' + esc(a) + "</span>").join("") : "";
  const tg = document.getElementById("toggle-detail");
  if (tg) { tg.hidden = planned; tg.textContent = "Show every claim's precise statement"; tg.dataset.state = "closed"; }
  const secs = m.sections.filter(x => x.number !== 1);
  const shown = planned ? secs.filter(x => sectionHasContent(m, x)) : secs;
  const notYet = planned ? secs.filter(x => !sectionHasContent(m, x)) : [];
  document.getElementById("toc").innerHTML = shown.map(x => '<a href="' + base + "sec-" + x.number + '" class="' + (sectionHasContent(m, x) ? "" : "empty") + '"><span class="n">' + x.number + "</span>" + esc(x.title) + "</a>").join("") +
    (planned ? '<a href="' + base + 'not-yet" class="empty"><span class="n">·</span>Not written yet (' + (notYet.length + 2) + ")</a>" : '<a href="' + base + 'sec-16"><span class="n">16</span>References</a><a href="' + base + 'sec-17"><span class="n">17</span>Changelog</a>');
  const chev = '<svg class="chev" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 4l6 6-6 6"/></svg>';
  // phones: every section starts closed (the page is long); wider screens open the sections a reader most often needs
  const openByDefault = isPhone() ? [] : planned ? [2, 13] : [5, 6, 8, 14];
  document.getElementById("sections").innerHTML = shown.map(x => {
    const subh = Object.fromEntries((x.subheadings || []).map(h => [h.before, h.title]));
    // a claim not shown yet (its anchors wait for a second reader) is skipped
    let body = x.number === 14 ? x.claims.filter(id => claimById[id]).map(id => { const c = claimById[id]; return (c.debate ? debateHtml(c.debate) : "") + (c.section === 14 ? claimHtml(c) : '<p class="note">The claim behind this question, with its certainty rating and evidence anchors: <a href="#' + c.id + '">section ' + c.section + "</a>.</p>"); }).join("") : x.claims.filter(id => claimById[id]).map(id => (subh[id] ? '<h3 class="subhead">' + esc(subh[id]) + "</h3>" : "") + claimHtml(claimById[id])).join("");
    if (x.number === 14 && planned && PLANNED_QUESTIONS[m.slug]) body += '<div class="planned-q"><h3>Questions this monograph will answer</h3><ol>' + PLANNED_QUESTIONS[m.slug].map(q => "<li>" + esc(q) + "</li>").join("") + '</ol><p class="muted">Not answered yet. Each will be answered in the six-part debate format once its sources have been read: the strongest case for yes, the strongest case for no, what neither side\'s evidence can show, the editors\' reading, and what would settle it.</p></div>';
    if (x.number === 10) body = figuresHtml(m.slug) + body;
    if (x.number === 2 && IDENTITY.some(d => d.substance === m.slug)) { body = identityHtml(m.slug) + body; x = Object.assign({}, x, { no_evidence_note: null }); }
    if (x.number === 15 && !planned) { const gh = gapsHtml(m.slug); if (gh) { body = gh + body; x = Object.assign({}, x, { no_evidence_note: null }); } }
    if (x.number === 13 && LEGAL.some(d => d.substance === m.slug)) { body = legalHtml(m.slug) + body; x = Object.assign({}, x, { no_evidence_note: null }); }
    if (x.no_evidence_note) body += '<p class="note' + (x.senior_author_only ? " senior" : "") + '">' + esc(x.no_evidence_note) + "</p>";
    if (x.number === 6) body = sosLine() + body;
    if (!x.claims.filter(id => claimById[id]).length && !x.no_evidence_note && !sectionHasContent(m, x)) body += '<p class="note">Not written yet.</p>';
    const nq = x.number === 14 && planned && PLANNED_QUESTIONS[m.slug] ? PLANNED_QUESTIONS[m.slug].length : x.claims.filter(id => claimById[id]).length;
    const nf = x.number === 10 ? figuresFor(m.slug).length : 0;
    const nLegal = x.number === 13 ? ((LEGAL.find(d => d.substance === m.slug) || {}).entries || []).length : 0;
    const count = x.number === 13 && nLegal ? nLegal + " row" + (nLegal === 1 ? "" : "s") : x.number === 2 && IDENTITY.some(d => d.substance === m.slug) ? "names, forms, street names" : x.number === 15 && !planned ? "open questions" : x.number === 14 ? nq + " question" + (nq === 1 ? "" : "s") + (planned ? ", not answered yet" : "") : x.number === 10 && planned ? nf + " figure" + (nf === 1 ? "" : "s") : (x.claims.length ? x.claims.length + " claim" + (x.claims.length === 1 ? "" : "s") : "not written yet") + (nf ? " · " + nf + " figure" + (nf === 1 ? "" : "s") : "");
    return '<details class="sec" id="sec-' + x.number + '"' + (openByDefault.includes(x.number) ? " open" : "") + '><summary><span class="n">' + x.number + "</span><h2>" + esc(x.title) + '</h2><span class="count">' + count + "</span>" + chev + '</summary><div class="sec-body">' + body + "</div></details>";
  }).join("") +
  (planned
    ? '<details class="sec notyet" id="not-yet"><summary><span class="n">·</span><h2>Not written yet</h2><span class="count">' + (notYet.length + 2) + " sections</span>" + chev + '</summary><div class="sec-body"><ul class="notyet-list">' + notYet.map(x => "<li><b>" + x.number + "</b> " + esc(x.title) + (x.number === 7 ? " — to be added by the senior author after a legal review" : "") + "</li>").join("") + "<li><b>16</b> References</li><li><b>17</b> Changelog</li></ul>" +
      '<p class="note">' + (em ? "The reading list for " + esc(m.name) + " has " + em.papers + " papers. " : "") + "Nothing is written until its papers have been read in full; every claim will then be graded and its evidence checked." + "</p>" + sosLine() + '<div class="reflist" id="reflist" hidden></div></div></details>'
    : '<details class="sec" id="sec-16"' + (openByDefault.length ? " open" : "") + '><summary><span class="n">16</span><h2>References</h2><span class="count">generated from the claims above</span>' + chev + '</summary><div class="sec-body"><div class="reflist" id="reflist"></div></div></details>' +
      '<details class="sec" id="sec-17"><summary><span class="n">17</span><h2>Changelog</h2><span class="count">' + m.changelog.length + "</span>" + chev + '</summary><div class="sec-body">' + (m.changelog.length ? m.changelog.map(c => '<p class="note"><span class="mono">v' + esc(c.version) + " · " + esc(c.date) + "</span> — " + esc(c.change) + "</p>").join("") : '<p class="note">No versions yet.</p>') + "</div></details>");
  const cited = new Set();
  m.sections.forEach(x => x.claims.forEach(id => claimById[id] && claimById[id].evidence.forEach(e => cited.add(e.reference))));
  const refs = [...cited].map(id => refById[id]).filter(Boolean).sort((a, b) => apaAuthors(a.author).localeCompare(apaAuthors(b.author)) || byYear(a, b));
  document.getElementById("reflist").innerHTML = refs.length ? refs.map(r => '<div class="ref" id="ref-' + r.id + '">' + apaReference(r) + '<span class="v">' + esc(r.verification.status) + " · " + esc(({crossref: "Crossref", publisher: "publisher's page", pubmed: "PubMed", manual: "entered by hand"})[String(r.verification.metadata_source || "").split(" ")[0]] || "metadata") + " " + esc(r.verification.verified_on || "") + " · retraction check: " + esc(r.verification.retraction_check ? r.verification.retraction_check.status : "—") + (r.notes ? " · note: " + esc(r.notes) : "") + "</span></div>").join("") : '<p class="note">No references yet; the list is generated from claims.</p>';
  if (isWide()) document.querySelectorAll("#sections details.cdetail").forEach(d => { d.open = true; });
  document.querySelectorAll("#sections [data-toggle]").forEach(b => b.addEventListener("click", () => { const el = document.getElementById(b.dataset.toggle); el.hidden = !el.hidden; }));
  document.querySelectorAll("#sections [data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
  document.querySelectorAll("#sections [data-report]").forEach(b => b.addEventListener("click", () => openReport(b.dataset.report)));
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest("#toggle-detail"); if (!b) return;
  const open = b.dataset.state !== "open";
  document.querySelectorAll("#sections details.cdetail").forEach(d => { d.open = open; });
  b.dataset.state = open ? "open" : "closed"; b.textContent = open ? "Hide the precise statements" : "Show every claim's precise statement";
});


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
function figuresByPlace(slug) {
  const groups = {};
  figuresFor(slug).forEach(r => (groups[r.file] = groups[r.file] || []).push(r));
  return Object.keys(groups).sort((a, b) => figRank(a) - figRank(b) || GEO_ORDER.indexOf(a) - GEO_ORDER.indexOf(b)).map(f => ({ file: f, rank: figRank(f), rows: groups[f] }));
}
function figPlaceHead(g) { return g.rank === 0 ? "Where you are: " + GEO_LABEL[g.file] : g.file === "global" ? "Worldwide" : g.file === "europe" ? "Europe" : GEO_LABEL[g.file]; }
// the evidence page's figures section: grouped by place, the reader's own first; "other places" says so
function figuresHtml(slug) {
  const groups = figuresByPlace(slug); if (!groups.length) return "";
  const own = PREF_COUNTRY && !groups.some(g => g.rank === 0) ? '<p class="note">We have no figures for ' + esc(shortCtry(PREF_COUNTRY)) + " yet.</p>" : "";
  let seenOther = false;
  return '<div class="figwrap">' + own + groups.map(g => {
    const head = g.rank === 3 && !seenOther && groups[0].rank < 3 ? '<p class="figother">Other places</p>' : ""; if (g.rank === 3) seenOther = true;
    return head + '<h3 class="figplace">' + esc(figPlaceHead(g)) + '</h3><div class="figs">' + g.rows.map(r => figureRow(r, true)).join("") + "</div>";
  }).join("") + '<p class="note">Official figures, each checked against its source. Sources count in different ways, so compare only like with like.</p></div>';
}
// the basics card: only figures for where the reader is, the world and their region, never another country's
function topFigures(slug, n) {
  const groups = figuresByPlace(slug).filter(g => g.rank < 3), out = [];
  groups.forEach(g => { if (out.length < n) out.push(g.rows[0]); });
  groups.forEach(g => g.rows.slice(1).forEach(r => { if (out.length < n) out.push(r); }));
  return out;
}
function fmtValue(r) {
  const v = typeof r.value === "number" ? (r.unit === "percent" ? r.value.toLocaleString("en-GB", { maximumFractionDigits: 2 }) + "%" : r.value.toLocaleString("en-GB")) : String(r.value);
  const unit = r.unit === "percent" ? "" : " " + r.unit;
  return v + unit;
}
// the place is shown beside each figure, so a survey's name ("..., Greek general population survey") is not repeated
function figYear(r) { const y = String(r.data_year).split(" (")[0]; return /^not stated/.test(y) ? "year not stated" : y; }
function figLabel(r) { return (r.label || String(r.def).split(/ \(|; /)[0]).replace(/, (Greek|EU|European) general population survey$/, ""); }
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
  const period = r.measure === "past-year-prevalence" ? (said("last 12 months") || said("last year") || said("last-year") ? "" : "use in the last 12 months") :
    r.measure === "past-month-prevalence" ? (said("last 30 days") || said("last month") ? "" : "use in the last 30 days") : r.measure === "lifetime-prevalence" ? (said("ever") || said("lifetime") ? "" : "ever used") : "";
  return { what, place, pop, period };
}
function figureRow(r, onDrugPage) {
  const ref = refById[r.source];
  const src = ref ? (ref.author[0].short || ref.author[0].literal || ref.author[0].family) + ", " + year(ref) : r.source;
  const f = figParts(r);
  // say what a range is (glossary: prevalence)
  const iv = r.interval && r.interval.low != null ? '<div class="fr">' + (/national estimates/.test(r.interval.type || "") ? "Range across countries: " : /as reported/.test(r.interval.type || "") ? "Range as reported: " : "Range: ") + esc(r.interval.low + "–" + r.interval.high) + (r.unit === "percent" ? "%" : "") + "</div>" : "";
  return '<div class="fig"><div class="fv num">' + esc(fmtValue(r)) + iv + '</div><div class="fw"><div class="ft">' + esc(f.what) + (f.period ? ' <span class="muted small">(' + esc(f.period) + ")</span>" : "") + '</div><div class="fm">' + esc(f.place) + ", " + esc(figYear(r)) + (f.pop ? " · " + esc(f.pop) : "") + (onDrugPage ? "" : " · " + esc(r.substance)) + '</div><div class="fp">' + '<a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(src) + "</a>" + (r.where ? ' · <button type="button" class="where" aria-expanded="false" data-where="' + esc((r.verified_on ? "Checked " + dcDate(r.verified_on) + " against: " : "Checked against: ") + r.where) + '">checked against the source text</button>' : "") + "</div></div></div>";
}
// only figures checked against their source are shown (a few still wait for that check)
function figuresFor(slug) {
  return EPI_ALL.filter(r => r.status === "verified" && (EPI_MAP[r.substance] || []).includes(slug));
}
// how many there are, before the figures themselves have been fetched (site/build.js counts them)
const figureCount = slug => FIGURES_DONE ? figuresFor(slug).length : (FIGURE_COUNT[slug] || 0);
// the statistics page draws once its figures have arrived (speed: they are fetched the first time it is opened)
let numbersDrawn = false;
function showNumbers() { if (numbersDrawn) return; whenReady(loadFigures, document.getElementById("num-list"), "The figures", () => { numbersDrawn = true; renderNumbers(); }); }
let numbersGeo = "", numbersSub = "All";
function renderNumbers() {
  const geos = GEO_ORDER.filter(g => EPI_ALL.some(r => r.file === g && r.status === "verified"));
  if (!geos.includes(numbersGeo)) numbersGeo = geos.slice().sort((a, b) => figRank(a) - figRank(b))[0]; // opens on the reader's own country, else the world
  document.getElementById("num-geo").innerHTML = geos.map(g => '<button class="chip" data-geo="' + g + '" aria-pressed="' + (g === numbersGeo) + '">' + esc(GEO_LABEL[g]) + "</button>").join("");
  const inGeo = EPI_ALL.filter(r => r.file === numbersGeo && r.status === "verified");
  const subs = ["All"].concat([...new Set(inGeo.map(r => r.substance))].sort());
  if (!subs.includes(numbersSub)) numbersSub = "All";
  // one menu instead of a row of buttons: the sources' own categories, as they name them
  document.getElementById("num-sub").innerHTML = '<label class="selectlabel">Drug or category, as the source names it <select id="num-sub-sel">' + subs.map(sb => '<option value="' + esc(sb) + '"' + (sb === numbersSub ? " selected" : "") + ">" + esc(sb === "All" ? "All (" + inGeo.length + " figures)" : sb) + "</option>").join("") + "</select></label>";
  document.querySelectorAll("#num-geo .chip").forEach(b => b.addEventListener("click", () => { numbersGeo = b.dataset.geo; numbersSub = "All"; renderNumbers(); }));
  document.getElementById("num-sub-sel").addEventListener("change", e => { numbersSub = e.target.value; renderNumbers(); });
  const rows = inGeo.filter(r => numbersSub === "All" || r.substance === numbersSub);
  document.getElementById("num-count").textContent = rows.length + " figure" + (rows.length === 1 ? "" : "s") + ", each checked against its source";
  document.getElementById("num-list").innerHTML = rows.map(r => figureRow(r)).join("") || '<p class="note">No figures for this selection.</p>';
}

/* ---------- Glossary ---------- */
function renderGlossary() {
  document.getElementById("glossary-list").innerHTML = GLOSSARY.map((g, i) => '<div class="gterm" id="g-' + i + '" data-text="' + esc(norm(g.term + " " + (g.short || "") + " " + g.def)) + '"><h2>' + esc(g.term) + "</h2>" + (g.short ? '<p class="gshort">' + esc(g.short) + "</p>" : "") + "<p>" + esc(g.def) + '</p><p class="gsrc">Source: ' + esc(g.source) + (g.ref ? " " + cite(g.ref) : "") + "</p></div>").join("");
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
  const em = EVIDENCE_MAPS["_Interactions"];
  const answered = Object.keys(byPair);
  document.getElementById("matrix-status").innerHTML = (answered.length ? "<b>" + answered.length + (answered.length === 1 ? " pair answered so far" : " pairs answered so far") + "</b> (marked ●; tap one to jump to its answer). " : "<b>Nothing here has been rated yet.</b> ") + esc((em ? "Reading list for mixing drugs: " + em.papers + " papers. " : "") + "A ? marks a pair whose question is set, a · one not yet planned.") + sosLine();
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

/* ---------- How to read: live example ---------- */
// the example is a full claim, so it draws once its file has arrived (on the page's first visit)
let howtoDrawn = false;
function showHowto() { if (howtoDrawn) return; whenReady(() => needFull(["cl_meth_psychosis_dose"]), document.getElementById("howto-example"), "The example", () => { howtoDrawn = true; renderHowto(); }); }
function renderHowto() {
  document.getElementById("howto-example").innerHTML = claimHtml(claimById["cl_meth_psychosis_dose"], { open: true });
  document.querySelectorAll("#howto-example [data-toggle]").forEach(b => b.addEventListener("click", () => { const el = document.getElementById(b.dataset.toggle); el.hidden = !el.hidden; }));
  document.querySelectorAll("#howto-example [data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
  document.querySelectorAll("#howto-example [data-report]").forEach(b => b.addEventListener("click", () => openReport(b.dataset.report)));
}

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
function ctrySelect(id) {
  return '<label class="ctrylabel" for="' + id + '">Your country</label><select class="ctry" id="' + id + '"><option value="">Choose a country</option>' + WL_COUNTRIES.map(c => '<option value="' + esc(c.name) + '"' + (c.name === PREF_COUNTRY ? " selected" : "") + ">" + esc(ctryName(c.name)) + "</option>").join("") + "</select>";
}
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
function countryLawHtml(slug, id) {
  return '<div class="ctrylaw" data-slug="' + esc(slug) + '">' + ctrySelect(id) + '<div class="ctry-out" aria-live="polite">' + (PREF_COUNTRY ? countryOut(slug, PREF_COUNTRY) : "") + '</div><p class="small"><a href="#law">Treaties, country by country</a></p></div>';
}
document.addEventListener("change", e => {
  const sel = e.target.closest && e.target.closest("select.ctry"); if (!sel) return;
  PREF_COUNTRY = sel.value; try { if (sel.value) localStorage.setItem("pk-country", sel.value); else localStorage.removeItem("pk-country"); } catch (err) { /* the choice lasts for this visit */ }
  document.querySelectorAll(".ctrylaw").forEach(box => { const s2 = box.querySelector("select.ctry"); if (s2 !== sel) s2.value = sel.value; box.querySelector(".ctry-out").innerHTML = sel.value ? countryOut(box.dataset.slug, sel.value) : ""; });
});
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
  return '<section class="lookalike" aria-labelledby="la-h"><h2 class="qh" id="la-h">Different drugs can look the same</h2>' +
    rows.map(([k, xs]) => '<p class="forms-k">' + esc(k) + '</p><div class="phgal">' + xs.map(([id, label, detail]) => photoFig(byId[id], "t", label, detail || null)).join("") + "</div>").join("") +
    '<p class="phnote">Looks don’t tell you what’s inside. Drug checking tests a sample. ' + phToggle() + "</p>" +
    (kit ? '<p class="forms-k">Tests named below</p><div class="phgal">' + photoFig(kit, "t") + (byId["test-strip-pouches"] ? photoFig(byId["test-strip-pouches"], "t") : "") + "</div>" : "") + "</section>";
}
function renderChecking() {
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
    INDEX.push({ type: "drug", kind: "Drug · " + s.cls, title: s.name, prime: new Set(prime), names: [...new Set(names)], text: norm(s.cls + " " + s.mech), href: "#s-" + s.slug, badge: pageStateLabel(s.slug), badgeCls: s.status });
  });
  const asked = buildAnswerIndex();
  CLAIMS.filter(c => !asked.has(c.id)).forEach(c => INDEX.push({ type: "claim", kind: "Finding · " + (subBySlug[c.substance] ? subBySlug[c.substance].name : c.substance), title: claimText(c), t: norm(claimText(c)), text: norm(c.statement + " " + c.outcome + " " + c.exposure), href: "#" + c.id, badge: editorApproved(c) ? "Approved" : readerStamp(c.verification.status).split(":")[0], badgeCls: editorApproved(c) ? "ok" : "draft" }));
  GLOSSARY.forEach((g, i) => INDEX.push({ type: "term", kind: "Term", title: g.term, t: norm(g.term), text: norm(g.def), href: "#g-" + i }));
  // countries: where to get drug checking, the emergency numbers, the treaties
  const dcBy = {}; DRUGCHECK.services.forEach(s => { dcBy[s.country] = (dcBy[s.country] || 0) + 1; });
  EMERGENCY.countries.forEach(c => INDEX.push({ type: "country", kind: "Emergency numbers", title: c.country, names: [c.country].concat(c.aka || []).map(norm), href: "#emergency/c-" + encodeURIComponent(c.country), order: 0 }));
  Object.keys(dcBy).forEach(c => INDEX.push({ type: "country", kind: "Drug checking · " + dcBy[c] + " service" + (dcBy[c] === 1 ? "" : "s"), title: c, names: [norm(c)], href: "#checking/c-" + encodeURIComponent(c), order: 1 }));
  WL_COUNTRIES.forEach(c => INDEX.push({ type: "country", kind: "Drug treaties", title: ctryName(c.name), names: [norm(c.name), norm(ctryName(c.name))], href: "#law/c-" + encodeURIComponent(ctryName(c.name)), order: 2 }));
  Object.keys(PLANNED_QUESTIONS).forEach(slug => PLANNED_QUESTIONS[slug].forEach(q => INDEX.push({ type: "question", kind: "Open question · " + (subBySlug[slug] ? subBySlug[slug].name : slug), title: q, t: norm(q), text: norm(slug), href: "#s-" + slug + "/sec-14", badge: "Not answered yet", badgeCls: "planned" })));
  [["Emergency numbers, country by country", "emergency", "emergency numbers overdose ambulance help poison centre support lines 112 911 999 000"], ["Drug checking services, country by country", "checking", "drug checking pill testing testing service analysis what is in my drug test kit"], ["Drug treaties by country", "law", "law legal treaties conventions un country illegal legal status"], ["Statistics: official figures", "numbers", "statistics numbers prevalence figures euda unodc nsduh world europe countries deaths treatment seizures"], ["How to read this site", "howto", "claims certainty dots status evidence study card plain precise"], ["Mixing drugs: what happens when drugs are combined", "interactions", "combinations mixing interactions combos opioids benzodiazepines benzos alcohol gabapentin pregabalin methadone buprenorphine"], ["Glossary", "glossary", "terms definitions words"], ["Methods", "methods", "protocol search risk of bias grade verification corrections"], ["About", "about", "who we are ai statement name pharmakon"]].forEach(p => INDEX.push({ type: "page", kind: "Page", title: p[0], t: norm(p[0]), text: norm(p[2]), href: "#" + p[1], id: p[1] }));
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
  if (!q) { const sug = document.activeElement === document.getElementById("search") ? suggestHtml() : ""; box.innerHTML = sug; box.hidden = !sug; if (live) live.textContent = sug ? "Some questions you can ask" : ""; return; }
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
      return '<a class="sr-ans' + (best ? " best" : "") + '" href="' + esc(answerHref(it, ctx)) + '"><span class="k">' + esc((best ? "Best answer · " : "Answer · ") + it.where) + '</span><span class="t">' + esc(it.title) + "</span>" +
        (sp ? '<span class="a">' + esc(sp.short) + "</span>" : "") + '<span class="m">' + meterHtml(c.grade.certainty, true) + "</span></a>"; }
    return '<a href="' + esc(it.href) + '"><span class="k">' + esc(it.kind) + (p.fz ? " · closest name" : "") + '</span><span class="t">' + esc(it.title.length > 140 ? it.title.slice(0, 137) + "…" : it.title) + "</span>" + (it.badge ? '<span class="badge ' + esc(it.badgeCls || "") + '">' + esc(it.badge) + "</span>" : "") + "</a>";
  };
  const asked = String(raw).trim(), askBtn = label => '<button type="button" class="linklike" data-fb="feedback" data-fb-text="' + esc(asked) + '">' + label + "</button>";
  box.innerHTML = searchHits.length ? searchHits.map(row).join("") + '<p class="sr-ask">Not what you were looking for? ' + askBtn("Ask us") + "</p>"
    : '<p class="none">No match for “' + esc(asked) + '”. Try other words, a drug’s name or a street name, or see <a href="#substances">all 30 drugs</a>. Need help now? <a href="#emergency">Emergency numbers</a>.</p>' +
      '<p class="sr-ask"><b>Didn’t find your question?</b> ' + askBtn("Ask us") + ". The questions people ask most are answered first.</p>";
  box.hidden = false;
  if (live) live.textContent = searchHits.length ? searchHits.length + " result" + (searchHits.length === 1 ? "" : "s") : "No results";
}
function closeSearch() { const box = document.getElementById("search-results"); if (box) { box.hidden = true; } }
const searchInput = document.getElementById("search");
searchInput.addEventListener("input", () => runSearch(searchInput.value));
searchInput.addEventListener("focus", () => runSearch(searchInput.value));
searchInput.addEventListener("keydown", e => { if (e.key === "ArrowDown") { const f = document.querySelector("#search-results a"); if (f) { e.preventDefault(); f.focus(); } return; } if (e.key === "Enter") { const first = norm(searchInput.value) && document.querySelector("#search-results a"); if (first) { e.preventDefault(); first.click(); } } if (e.key === "Escape") { searchInput.value = ""; closeSearch(); } });
document.getElementById("search-results").addEventListener("keydown", e => { const a = e.target.closest && e.target.closest("a"); if (!a) return; if (e.key === "ArrowDown" && a.nextElementSibling) { e.preventDefault(); a.nextElementSibling.focus(); } if (e.key === "ArrowUp") { e.preventDefault(); (a.previousElementSibling || searchInput).focus(); } if (e.key === "Escape") { searchInput.focus(); closeSearch(); } });
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
  popEl.innerHTML = "<b>" + esc(g.term) + "</b>" + (g.short ? '<p class="gshort">' + esc(g.short) + "</p>" : "") + '<p class="muted">' + esc(g.def) + '</p><div class="acts"><a href="#g-' + btn.dataset.gl + '">Glossary</a></div>';
  document.body.appendChild(popEl);
  const r = btn.getBoundingClientRect(); const pw = Math.min(360, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
}
function hidePop() { popWant = null; if (popEl) { popEl.remove(); popEl = null; } }
function scheduleHide() { clearTimeout(popTimer); popTimer = setTimeout(hidePop, 250); }
const NO_HOVER = window.matchMedia ? window.matchMedia("(hover: none)").matches : false;
document.addEventListener("mouseover", e => { if (NO_HOVER) return; const a = e.target.closest("a.pop"); if (a) { clearTimeout(popTimer); showPop(a); return; } const g = e.target.closest("button.gl"); if (g) { clearTimeout(popTimer); showGloss(g); } });
document.addEventListener("mouseout", e => { if (NO_HOVER) return; if (e.target.closest("a.pop") || e.target.closest("button.gl")) scheduleHide(); });
document.addEventListener("focusin", e => { if (NO_HOVER) return; const a = e.target.closest("a.pop"); if (a) { showPop(a); return; } const g = e.target.closest("button.gl"); if (g) showGloss(g); });
document.addEventListener("click", e => {
  const g = e.target.closest("button.gl");
  if (g) { e.preventDefault(); if (popEl && popEl.dataset.for === "gl-" + g.dataset.gl) hidePop(); else showGloss(g); return; }
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
// a page's state in plain words: draft monograph, or the basics only (names, figures, law)
// a page without a written monograph can still carry checked answers in Quick answers
function hasQuickAnswers(slug) { return (QUESTIONS[slug] || []).some(g => g.items.some(([id]) => claimById[id])); }
function pageStateLabel(slug) {
  const m = monographFor(slug); if (!m) return "";
  if (m.status !== "planned") return "Full write-up";
  if (hasQuickAnswers(slug)) return "Answers so far";
  const basics = IDENTITY.some(d => d.substance === slug) || LEGAL.some(d => d.substance === slug) || figureCount(slug);
  return basics ? "Basics only" : "Not written yet";
}
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
  panel.innerHTML = '<button class="close" type="button" aria-label="Close">✕</button><div class="cardhead"><span class="eyebrow">Study card · ' + esc(c.design.replace(/-/g, " ")) + ' · <span class="badge draft">' + esc(c.verification.status) + "</span></span><h2>" + esc(ref.title) + '</h2><div class="refline mono">' + apaReference(ref) + "</div></div>" +
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
function fbText() {
  const msg = document.getElementById("report-message").value.trim(), src = document.getElementById("report-source").value.trim();
  const incl = document.getElementById("fb-incl").checked, p = fbPage(FB.where), issue = FB.mode === "issue";
  const subject = (issue ? "Pharmakon: a mistake" : "Pharmakon: a question or idea") + (incl ? " (" + p.short + ")" : "");
  const body = (issue ? "Report a mistake" : "A question or idea") + "\n" +
    (incl ? "Page: " + p.title + "\nAddress: " + p.url + "\n" : "") + "\n" + msg + "\n" + (issue && src ? "\nSource: " + src + "\n" : "") +
    "\n(Sent from the feedback panel, Pharmakon version " + SITE_VERSION + ")";
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
  return '<section class="sec fbline" aria-label="Ask or report"><p><b>Didn’t find your question?</b> Ask us. The questions people ask most are answered first.</p><div class="fb-two">' +
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

/* ---------- Boot ---------- */
document.documentElement.lang = "en";
applyPhotoPref();
(function () { const el = document.getElementById("photo-credits"); if (!el) return; const name = s => (subBySlug[s] ? subBySlug[s].name : s === "safety-drug-checking" ? "Drug checking" : s);
  el.innerHTML = PHOTOS.slice().sort((a, b) => name(a.drug).localeCompare(name(b.drug))).map(p => "<li><b>" + esc(name(p.drug)) + ":</b> " + esc(p.form.toLowerCase()) + ". " + photoCredit(p) + "</li>").join(""); })();
// (the research pages, the statistics page and the how-to example draw on their first visit, once their files have arrived)
buildIndex(); renderHome2(); factsLinks(); renderSubstances(); renderGlossary(); renderInteractions(); renderEmergency(); renderLaw(); renderChecking();
window.addEventListener("hashchange", route);
document.getElementById("skiplink").addEventListener("click", () => { const v = document.querySelector(".view.active"); const h = v && v.querySelector("h1"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } });
route();

/* printing a monograph prints every section, open or not */
window.addEventListener("beforeprint", () => document.querySelectorAll("#view-monograph details.sec").forEach(d => { if (!d.open) { d.dataset.printOpened = "1"; d.open = true; } }));
window.addEventListener("afterprint", () => document.querySelectorAll('#view-monograph details.sec[data-print-opened="1"]').forEach(d => { d.open = false; delete d.dataset.printOpened; }));
