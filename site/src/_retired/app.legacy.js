/* ---------- APA 7 rendering (prototype; production uses citeproc-js with the APA CSL style) ---------- */
const refById = Object.fromEntries(REFS.map(r => [r.id, r]));
const cardById = STUDY_CARDS;
const claimById = Object.fromEntries(CLAIMS.map(c => [c.id, c]));

function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function initials(given) {
  if (!given) return "";
  return given.trim().split(/\s+/).map(part => part.split("-").map(p => p ? p[0].toUpperCase() + "." : "").join("-")).join(" ");
}
function authorEntry(a) { return a.literal ? a.literal : (a.family + (a.given ? ", " + initials(a.given) : "")); }
function apaAuthors(list) {
  const names = list.map(authorEntry);
  if (names.length === 1) return names[0];
  if (names.length <= 20) return names.slice(0, -1).join(", ") + ", & " + names[names.length - 1];
  return names.slice(0, 19).join(", ") + ", … " + names[names.length - 1];
}
function year(ref) { return ref.issued && ref.issued["date-parts"] ? ref.issued["date-parts"][0][0] : "n.d."; }
function dash(p) { return String(p).replace(/-/g, "–"); }
function apaReference(ref) {
  const y = year(ref);
  const link = ref.DOI ? "https://doi.org/" + ref.DOI : (ref.URL || "");
  const au = apaAuthors(ref.author);
  let html = esc(au) + (au.endsWith(".") ? "" : ".") + " (" + y + "). ";
  if (ref.type === "article-journal") {
    html += esc(ref.title) + ". <i>" + esc(ref["container-title"]) + (ref.volume ? ", " + esc(ref.volume) : "") + "</i>" + (ref.issue ? "(" + esc(dash(ref.issue)) + ")" : "") + (ref.page ? ", " + esc(dash(ref.page)) : "") + ". ";
  } else if (ref.type === "report") {
    html += "<i>" + esc(ref.title) + "</i>. " + (ref.publisher && ref.publisher !== ref.author[0].literal ? esc(ref.publisher) + ". " : "");
  } else {
    html += "<i>" + esc(ref.title) + "</i>. ";
  }
  if (link) html += '<a href="' + esc(link) + '" target="_blank" rel="noopener">' + esc(link) + "</a>";
  return html;
}
// In-text form with APA 7 disambiguation: extend surnames until the form is unique among the cited set.
function inTextLabel(ref, pool) {
  const au = ref.author.map(a => a.literal || a.family);
  const y = year(ref);
  if (au.length === 1) return (ref.author[0].short || au[0]) + ", " + y;
  if (au.length === 2) return au[0] + " & " + au[1] + ", " + y;
  const rivals = pool.filter(r => r.id !== ref.id && year(r) === y && (r.author[0].literal || r.author[0].family) === au[0] && r.author.length >= 3);
  let k = 1;
  const prefix = (r, n) => r.author.slice(0, n).map(a => a.literal || a.family).join("|");
  while (k < au.length - 1 && rivals.some(r => prefix(r, k) === prefix(ref, k))) k++;
  if (k === 1) return au[0] + " et al., " + y;
  return au.slice(0, k).join(", ") + ", et al., " + y;
}
function cite(id) {
  const ref = refById[id];
  if (!ref) return '<span class="placeholder">[missing reference: ' + esc(id) + "]</span>";
  return '<a class="pop" href="#ref-' + esc(id) + '" data-ref="' + esc(id) + '">(' + esc(inTextLabel(ref, REFS)) + ")</a>";
}
// Replace author-year mentions inside debate prose with live citations: (Hart et al., 2012) → link.
function liveCites(text) {
  return esc(text).replace(/\(([^()]*?\d{4}[a-z]?)\)/g, (m, inner) => {
    const parts = inner.split(";").map(s => s.trim());
    const out = parts.map(p => {
      const found = REFS.find(r => inTextLabel(r, REFS) === p);
      return found ? '<a class="pop" href="#ref-' + found.id + '" data-ref="' + found.id + '">' + esc(p) + "</a>" : esc(p);
    });
    return "(" + out.join("; ") + ")";
  });
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

/* ---------- Views ---------- */
const views = ["home", "substances", "methamphetamine", "methods", "about"];
function route() {
  let h = (location.hash || "#home").slice(1);
  if (h.startsWith("ref-")) { show("methamphetamine"); const el = document.getElementById(h); if (el) el.scrollIntoView({ block: "center" }); return; }
  if (h.startsWith("sec-")) { show("methamphetamine"); const el = document.getElementById(h); if (el) { el.open = true; el.scrollIntoView({ block: "start" }); } return; }
  if (!views.includes(h)) h = "home";
  show(h);
  window.scrollTo({ top: 0 });
}
function show(name) {
  views.forEach(v => { const el = document.getElementById("view-" + v); if (el) el.classList.toggle("active", v === name); });
  document.querySelectorAll("nav.main a").forEach(a => { if (a.dataset.view === name) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
}

/* Home */
function renderHome() {
  const statsEl = document.getElementById("stats");
  statsEl.innerHTML = EPI.map(e => {
    const ref = refById[e.source];
    const link = ref ? (ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL) : "#";
    const srcLabel = ref ? (ref.author[0].short || ref.author[0].literal || (ref.author[0].family + (ref.author.length > 1 ? " et al." : ""))) + ", " + year(ref) : e.source;
    return '<div class="stat"><div class="value num">' + esc(e.value) + '</div><div class="label">' + esc(e.label) + '</div><div class="prov">' + esc(e.measure) + '<br>Source: <a href="' + esc(link) + '" target="_blank" rel="noopener">' + esc(srcLabel) + '</a> · <span class="badge ' + (e.status === "verified" ? "verified" : "draft") + '">' + (e.status === "verified" ? "verified" : "draft · awaiting PDF check") + "</span></div></div>";
  }).join("");
  const classes = {};
  SUBSTANCES.forEach(s => { (classes[s.cls] = classes[s.cls] || []).push(s); });
  document.getElementById("classgrid").innerHTML = Object.keys(classes).map(c => '<div class="classcard"><h3>' + esc(c) + "</h3><ul>" + classes[c].map(s => '<li><a href="' + (s.status === "draft" ? "#methamphetamine" : "#substances") + '" class="' + s.status + '">' + esc(s.name) + "</a></li>").join("") + "</ul></div>").join("");
  const nRefs = REFS.length, nCards = Object.keys(STUDY_CARDS).length, nClaims = CLAIMS.length;
  document.getElementById("progress").innerHTML = [
    ["0 / 30", "Tier-1 monographs published"], ["1", "monograph in draft (methamphetamine)"], [nClaims, "draft claims"], [nCards, "first-pass study cards"], [nRefs, "references, metadata verified against Crossref"], ["0", "excerpts verified against a PDF"]
  ].map(p => '<div class="p"><b class="num">' + p[0] + "</b><span>" + p[1] + "</span></div>").join("");
}

/* Substances */
let activeClass = "All";
function renderSubstances() {
  const classes = ["All"].concat([...new Set(SUBSTANCES.map(s => s.cls))]);
  document.getElementById("filters").innerHTML = classes.map(c => '<button class="chip" data-cls="' + esc(c) + '" aria-pressed="' + (c === activeClass) + '">' + esc(c) + "</button>").join("");
  document.querySelectorAll("#filters .chip").forEach(b => b.addEventListener("click", () => { activeClass = b.dataset.cls; renderSubstances(); }));
  const list = SUBSTANCES.filter(s => activeClass === "All" || s.cls === activeClass);
  document.getElementById("subgrid").innerHTML = list.map(s => '<a class="subcard" href="' + (s.status === "draft" ? "#methamphetamine" : "#substances") + '"><div class="row"><span class="cls">' + esc(s.cls) + '</span><span class="badge ' + s.status + '">' + (s.status === "draft" ? "draft v0.1" : "planned") + "</span></div><h3>" + esc(s.name) + '</h3><div class="mech">' + esc(s.mech) + "</div></a>").join("");
}

/* Monograph */
function claimHtml(c) {
  const ev = c.evidence.map(e => '<div class="ex"><div><span class="role ' + e.role + '">' + e.role + "</span> <q>" + esc(e.excerpt) + '</q></div><div class="src">' + cite(e.reference) + "<br>" + esc(e.page) + "<br>" + (e.excerpt_verified ? "verified" : '<span class="placeholder">not verified</span>') + "</div></div>").join("");
  const citeList = [...new Set(c.evidence.map(e => e.reference))].map(cite).join(" ");
  const cardLinks = [...new Set(c.evidence.map(e => e.study_card))].map(sc => { const r = refById[cardById[sc].reference]; return '<button type="button" data-card="' + esc(sc) + '">Study card: ' + esc(r ? (r.author[0].short || r.author[0].literal || r.author[0].family) + " " + year(r) : sc) + "</button>"; }).join("");
  return '<article class="claim ' + c.status + '" id="' + c.id + '">' +
    '<div class="text">' + esc(c.statement) + " " + citeList + "</div>" +
    '<div class="cert"><div class="grade">' + gradeDots(c.grade.certainty) + '<span class="lvl">' + esc(gradeLabel(c.grade.certainty)) + " certainty</span></div>" +
    '<div><span class="badge ' + c.status + '">' + esc(c.status.replace("-", " ")) + "</span></div>" +
    '<details class="why"><summary>Why this rating</summary><p class="mono">' + esc(gradeDomains(c.grade)) + "</p><p>" + esc(c.grade.reasoning) + "</p></details></div>" +
    '<div class="pecotable"><div><b>Population</b>' + esc(c.population) + "</div><div><b>Exposure</b>" + esc(c.exposure) + "</div><div><b>Comparator</b>" + esc(c.comparator) + "</div><div><b>Outcome</b>" + esc(c.outcome) + "</div><div><b>Magnitude</b>" + esc(c.magnitude) + "</div></div>" +
    '<div class="tools">' + cardLinks + '<button type="button" data-toggle="ev-' + c.id + '">Evidence excerpts (' + c.evidence.length + ")</button>" + '<span class="verif">' + esc(c.verification.status.toUpperCase()) + " · v" + esc(c.version) + "</span></div>" +
    '<div class="evid" id="ev-' + c.id + '" hidden>' + ev + "</div>" +
    "</article>";
}
function debateHtml(d) {
  return '<section class="debate"><header><span class="badge contested">contested</span><h3>' + esc(d.question) + "</h3></header>" +
    '<div class="cols"><div class="col yes"><h4>Strongest evidence for yes</h4>' + liveCites(d.evidence_yes) + '</div><div class="col no"><h4>Strongest evidence for no</h4>' + liveCites(d.evidence_no) + "</div></div>" +
    '<div class="full"><h4>What neither side\'s evidence can show</h4>' + esc(d.neither_can_show) + "</div>" +
    '<div class="full reading"><h4>The editors\' reading</h4>' + esc(d.editors_reading) + "</div>" +
    '<div class="full"><h4>What would settle it</h4>' + esc(d.what_would_settle_it) + "</div></section>";
}
function renderMonograph() {
  const m = MONO;
  document.getElementById("mono-title").textContent = m.name;
  document.getElementById("mono-inn").textContent = "INN: " + m.inn;
  document.getElementById("mono-status").innerHTML = '<span class="badge ' + m.status + '">' + m.status + " · v" + m.version + "</span>";
  document.getElementById("mono-meta").innerHTML = "<span>Last systematic search: <b>" + (m.dates.last_search || "not yet run") + "</b></span><span>Last senior review: <b>" + (m.dates.last_review || "none") + "</b></span><span>Authors: <b>" + m.authors.map(a => a.name).join("; ") + "</b></span><span>Conflicts of interest: <b>" + m.authors.map(a => a.coi).join("; ") + "</b></span>";
  document.getElementById("mono-tags").innerHTML = m.classes.concat(m.mechanisms).map(t => '<span class="tag">' + esc(t) + "</span>").join("");
  const g = m.at_a_glance;
  document.getElementById("glance").innerHTML = '<div class="box wide"><h3>Mechanism</h3><p>' + esc(g.mechanism_line) + "</p></div>" +
    '<div class="box"><h3>Best established (highest certainty on this page)</h3><ol>' + g.best_established.map(id => '<li><a href="#' + id + '">' + esc(claimById[id].statement.split(/[;:.]/)[0]) + ".</a></li>").join("") + "</ol></div>" +
    '<div class="box"><h3>Largest uncertainties</h3><ol>' + g.largest_uncertainties.map(id => '<li><a href="#' + id + '">' + esc(claimById[id].statement.split(/[;:.]/)[0]) + ".</a></li>").join("") + "</ol></div>" +
    '<div class="box wide"><h3>Legal status (summary)</h3><p>' + esc(g.legal_summary) + "</p></div>";
  const secs = m.sections.filter(s => s.number !== 1);
  document.getElementById("toc").innerHTML = secs.map(s => '<a href="#sec-' + s.number + '" class="' + (s.claims.length ? "" : "empty") + '"><span class="n">' + s.number + "</span>" + esc(s.title) + "</a>").join("") + '<a href="#sec-16"><span class="n">16</span>References</a><a href="#sec-17"><span class="n">17</span>Changelog</a>';
  const chev = '<svg class="chev" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 4l6 6-6 6"/></svg>';
  const openByDefault = [4, 9, 14];
  document.getElementById("sections").innerHTML = secs.map(s => {
    let body = "";
    if (s.number === 14) {
      body = s.claims.map(id => claimById[id].debate ? debateHtml(claimById[id].debate) : "").join("");
    } else {
      body = s.claims.map(id => claimHtml(claimById[id])).join("");
    }
    if (s.no_evidence_note) body += '<p class="note' + (s.senior_author_only ? " senior" : "") + '">' + (s.senior_author_only ? '<span class="badge senior">senior author only</span> ' : "") + esc(s.no_evidence_note) + "</p>";
    if (!s.claims.length && !s.no_evidence_note) body += '<p class="note">No claims drafted yet.</p>';
    return '<details class="sec" id="sec-' + s.number + '"' + (openByDefault.includes(s.number) ? " open" : "") + '><summary><span class="n">' + s.number + "</span><h2>" + esc(s.title) + '</h2><span class="count">' + (s.number === 14 ? s.claims.length + " question" + (s.claims.length === 1 ? "" : "s") : s.claims.length + " claim" + (s.claims.length === 1 ? "" : "s")) + "</span>" + chev + '</summary><div class="sec-body">' + body + "</div></details>";
  }).join("") +
  '<details class="sec" id="sec-16" open><summary><span class="n">16</span><h2>References</h2><span class="count">generated from the claims above</span>' + chev + '</summary><div class="sec-body"><div class="reflist" id="reflist"></div></div></details>' +
  '<details class="sec" id="sec-17"><summary><span class="n">17</span><h2>Changelog</h2><span class="count">' + m.changelog.length + "</span>" + chev + '</summary><div class="sec-body">' + m.changelog.map(c => '<p class="note"><span class="mono">v' + esc(c.version) + " · " + esc(c.date) + "</span> — " + esc(c.change) + "</p>").join("") + "</div></details>";
  // References: only those cited by claims on this page, alphabetical.
  const cited = new Set();
  m.sections.forEach(s => s.claims.forEach(id => claimById[id].evidence.forEach(e => cited.add(e.reference))));
  const refs = [...cited].map(id => refById[id]).filter(Boolean).sort((a, b) => apaAuthors(a.author).localeCompare(apaAuthors(b.author)) || year(a) - year(b));
  document.getElementById("reflist").innerHTML = refs.map(r => '<div class="ref" id="ref-' + r.id + '">' + apaReference(r) + '<span class="v">' + esc(r.verification.status) + " · Crossref " + esc(r.verification.verified_on || "") + " · retraction check: " + esc(r.verification.retraction_check ? r.verification.retraction_check.status : "—") + (r.notes ? " · note: " + esc(r.notes) : "") + "</span></div>").join("");
  // Wire interactions
  document.querySelectorAll("[data-toggle]").forEach(b => b.addEventListener("click", () => { const el = document.getElementById(b.dataset.toggle); el.hidden = !el.hidden; }));
  document.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => openCard(b.dataset.card)));
}

/* Popover */
let popEl = null, popTimer = null;
function showPop(a) {
  const ref = refById[a.dataset.ref]; if (!ref) return;
  hidePop();
  popEl = document.createElement("div"); popEl.className = "popover"; popEl.setAttribute("role", "dialog");
  const cards = Object.keys(cardById).filter(k => cardById[k].reference === ref.id);
  const link = ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL;
  popEl.innerHTML = '<div class="refline">' + apaReference(ref) + '</div><div class="acts">' + (link ? '<a href="' + esc(link) + '" target="_blank" rel="noopener">Open ' + (ref.DOI ? "DOI" : "source") + ' ↗</a>' : "") + cards.map(k => '<button type="button" data-card="' + k + '">Study card</button>').join("") + '<a href="#ref-' + ref.id + '">Reference list</a></div><div class="vline">' + esc(ref.verification.status) + (ref.verification.verified_on ? " · Crossref " + esc(ref.verification.verified_on) : "") + " · retraction check: " + esc(ref.verification.retraction_check ? ref.verification.retraction_check.status : "—") + (ref.verification.online_first_year ? " · online first " + ref.verification.online_first_year : "") + "</div>";
  document.body.appendChild(popEl);
  const r = a.getBoundingClientRect(); const pw = Math.min(420, window.innerWidth - 32);
  let left = r.left + window.scrollX; if (left + pw > window.innerWidth + window.scrollX - 16) left = window.innerWidth + window.scrollX - 16 - pw; if (left < 16) left = 16;
  popEl.style.left = left + "px"; popEl.style.top = (r.bottom + window.scrollY + 6) + "px"; popEl.style.width = pw + "px";
  popEl.addEventListener("mouseenter", () => clearTimeout(popTimer));
  popEl.addEventListener("mouseleave", scheduleHide);
  popEl.querySelectorAll("[data-card]").forEach(b => b.addEventListener("click", () => { openCard(b.dataset.card); hidePop(); }));
}
function hidePop() { if (popEl) { popEl.remove(); popEl = null; } }
function scheduleHide() { clearTimeout(popTimer); popTimer = setTimeout(hidePop, 250); }
document.addEventListener("mouseover", e => { const a = e.target.closest("a.pop"); if (a) { clearTimeout(popTimer); showPop(a); } });
document.addEventListener("mouseout", e => { const a = e.target.closest("a.pop"); if (a) scheduleHide(); });
document.addEventListener("focusin", e => { const a = e.target.closest("a.pop"); if (a) showPop(a); });
document.addEventListener("click", e => {
  const a = e.target.closest("a.pop");
  if (a) { e.preventDefault(); const ref = refById[a.dataset.ref]; const link = ref && (ref.DOI ? "https://doi.org/" + ref.DOI : ref.URL); if (link) window.open(link, "_blank", "noopener"); return; }
  if (popEl && !e.target.closest(".popover")) hidePop();
});
document.addEventListener("keydown", e => { if (e.key === "Escape") { hidePop(); closeCard(); } });

/* Drawer: study card */
function row(label, value) { return '<div class="card-row"><b>' + esc(label) + "</b><div>" + value + "</div></div>"; }
function fmt(v) { if (v == null || v === "") return '<span class="placeholder">[to be extracted]</span>'; return esc(String(v)).replace(/\[to be extracted from PDF\]|\[to be extracted\]/g, m => '<span class="placeholder">' + m + "</span>"); }
function sub(obj, keys) { return '<div class="sub">' + keys.filter(k => obj[k] != null && obj[k] !== "").map(k => "<span><i>" + esc(k.replace(/_/g, " ")) + ":</i> " + fmt(obj[k]) + "</span>").join("") + "</div>"; }
function openCard(id) {
  const c = cardById[id]; if (!c) return;
  const ref = refById[c.reference];
  const panel = document.querySelector("#drawer .panel");
  panel.innerHTML = '<button class="close" type="button" aria-label="Close">✕</button><header><span class="eyebrow">Study card · ' + esc(c.design.replace(/-/g, " ")) + ' · <span class="badge draft">' + esc(c.verification.status) + "</span></span><h2>" + esc(ref.title) + '</h2><div class="refline mono">' + apaReference(ref) + "</div></header>" +
    row("Design", esc(c.design_detail || "")) + row("Can establish", esc(c.can_establish)) + row("Cannot establish", esc(c.cannot_establish)) +
    row("Sample & recruitment", sub(Object.assign({}, c.sample, { n_by_group: c.sample.n_by_group ? Object.entries(c.sample.n_by_group).map(kv => kv[0] + " " + kv[1]).join("; ") : null }), ["n_total", "n_by_group", "recruitment", "inclusion_exclusion", "demographics", "attrition", "selection_effects"])) +
    row("Exposure measurement", sub(c.exposure, ["measurement", "dose_frequency_duration_route", "purity_known", "polysubstance", "abstinence_at_testing"])) +
    row("Comparison group", sub(c.comparison, ["controls", "matching", "unmeasured_premorbid", "controls_other_drug_use"])) +
    row("Outcome measures", sub(c.outcomes, ["instruments", "validity_norms", "operationalization", "n_outcomes_tested", "multiplicity_correction", "assessor_blinding"])) +
    row("Analysis & reporting", sub(c.analysis, ["effect_sizes", "covariates", "preregistration", "preregistration_detail", "selective_reporting", "power"])) +
    row("Interpretation gap", sub(c.interpretation_gap, ["results_show", "claimed", "gap_assessment"])) +
    row("Replication & timeline", (c.replication.timeline ? '<div class="timeline">' + c.replication.timeline.map(t => '<div class="t"><span class="y">' + t.year + "</span><span>" + esc(t.event) + (t.reference ? " " + cite(t.reference) : "") + "</span></div>").join("") + "</div>" : "") + '<p style="margin-top:6px"><i class="muted">status:</i> ' + esc(c.replication.status) + (c.replication.where_it_stands ? " — " + esc(c.replication.where_it_stands) : "") + "</p>") +
    row("Funding & interests", sub(c.funding, ["funder", "declared_conflicts", "affiliations_note"])) +
    row("What would settle it", esc(c.what_would_settle_it)) +
    row("Risk of bias — " + c.risk_of_bias.instrument, '<div class="rob">' + c.risk_of_bias.domains.map(d => '<div class="d"><span class="light ' + esc(d.judgment) + '"></span><span>' + esc(d.domain) + ": <b>" + esc(d.judgment.replace(/-/g, " ")) + "</b>" + (d.note ? ' <span class="muted">— ' + fmt(d.note) + "</span>" : "") + "</span></div>").join("") + '<div class="overall">OVERALL: ' + esc(c.risk_of_bias.overall.toUpperCase()) + " — " + esc(c.risk_of_bias.reasoning) + "</div></div>") +
    row("Verification", "First pass by " + esc(c.verification.first_pass_by) + " on " + esc(c.verification.first_pass_on) + (c.verification.reviewed_by ? "; reviewed by " + esc(c.verification.reviewed_by) : '; <span class="placeholder">senior review pending</span>'));
  document.getElementById("drawer").classList.add("open");
  panel.querySelector(".close").addEventListener("click", closeCard);
  panel.scrollTop = 0;
}
function closeCard() { document.getElementById("drawer").classList.remove("open"); }
document.querySelector("#drawer .scrim").addEventListener("click", closeCard);

/* Boot */
renderHome(); renderSubstances(); renderMonograph();
window.addEventListener("hashchange", route);
route();
