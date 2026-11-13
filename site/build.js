// Builds the single-file prototype from the data/ JSON files (source of truth) + src/ (template, styles, app code).
// Also injects evidence-map counts parsed from search-logs/*_DOI-LIST.md.
const fs = require("fs"); const path = require("path");
// Every author–year citation in prose must resolve to a reference (scripts/check_citations.js); a failure is reported, not fatal.
try { require("child_process").execFileSync("node", [path.join(__dirname, "..", "scripts", "check_citations.js")], { stdio: "inherit" }); } catch (e) { console.error("WARNING: unresolved in-text citations (see above)"); }
const ROOT = path.join(__dirname, "..");
const { trimQuotes } = require(path.join(__dirname, "..", "scripts", "quote_limits.js"));
const src = p => fs.readFileSync(path.join(__dirname, "src", p), "utf8");
const loadAll = dir => fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => f.endsWith(".json")).sort().flatMap(f => { const j = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); return Array.isArray(j) ? j : [j]; }) : [];
const refs = loadAll(path.join(ROOT, "data/references"));
// Drug-checking services cite web pages read on a date: each source becomes an auxiliary reference (APA popover and link), kept out of the site's reference counts
const drugCheck = JSON.parse(fs.readFileSync(path.join(ROOT, "data/site/drug-checking.json"), "utf8")); delete drugCheck._note;
const dcRef = (src, id) => { src.ref = id;
  refs.push({ id, type: "webpage", title: src.title || src.url, author: [{ literal: src.publisher || "Unknown publisher", short: src.publisher || "Source" }], issued: { "date-parts": [[]] }, URL: src.url,
    accessed: { "date-parts": [String(src.read_on || "").split("-").map(Number)] }, _aux: true,
    verification: { status: "metadata-verified", metadata_source: "publisher", verified_on: src.read_on, retraction_check: { status: "not-checked", note: "Web page" } } }); };
drugCheck.services.forEach((sv, i) => (sv.sources || []).forEach((src, j) => dcRef(src, "dc-" + i + "_s" + j)));
// countries where only a report mentions drug checking or kit handouts: a sourced line, not a service
(drugCheck.countries_reported || []).forEach((cr, i) => (cr.sources || []).forEach((src, j) => dcRef(src, "dcr-" + i + "_s" + j)));
const cards = Object.fromEntries(loadAll(path.join(ROOT, "data/study-cards")).map(c => { const { id, ...rest } = c; return [id, rest]; }));
const claimsAll = loadAll(path.join(ROOT, "data/claims"));
// Publication rule: a claim is shown only in a version whose anchors a second reader has checked. While a first reader's new
// anchors wait, the last checked version (data/claims/_published/, kept by scripts/snapshot_published.py) is shown instead.
const publishedClaims = Object.fromEntries(loadAll(path.join(ROOT, "data/claims/_published")).map(c => [c.id, c]));
const held = [];
const unseen = [];
let claims = claimsAll.map(c => { const waiting = c.evidence.filter(e => e.anchor_status === "ai-located" || e.anchor_status === "unchecked").length;
  if (waiting && publishedClaims[c.id]) { held.push(c.id + " (" + waiting + " anchors wait; showing " + publishedClaims[c.id].version + " instead of " + c.version + ")"); return publishedClaims[c.id]; }
  // a new claim with no checked version yet is not shown at all until a second reader has checked its anchors
  if (waiting) { unseen.push(c.id); return null; }
  return c; }).filter(Boolean);
// Senior gate (decision p-ways-of-taking): a claim in section 7 (ways of taking a drug: forms and routes compared) goes on the site only in a
// version the senior author has approved, recorded in data/verification/senior-gate.json as {claim_id: {version, decision, date, note}}.
// Until then it is left out of the page entirely (not hidden in it), with the study cards that only it cites.
const gatePath = path.join(ROOT, "data/verification/senior-gate.json");
const gate = fs.existsSync(gatePath) ? JSON.parse(fs.readFileSync(gatePath, "utf8")) : {}; delete gate._note;
const gated = [];
for (let i = 0; i < claims.length; i++) { const c = claims[i]; if (c.section !== 7) continue;
  const g = gate[c.id], ok = g && /^approved/.test(g.decision || "");
  if (ok && g.version === c.version) continue;
  if (ok && publishedClaims[c.id] && publishedClaims[c.id].version === g.version) { claims[i] = publishedClaims[c.id]; continue; }
  gated.push(c.id + " v" + c.version); claims[i] = null; }
for (let i = claims.length - 1; i >= 0; i--) if (!claims[i]) claims.splice(i, 1);
if (gated.length) console.error("NOTE: " + gated.length + " section 7 claims left out until the senior author approves them: " + gated.join(", "));
{ const shown = new Set(claims.flatMap(c => c.evidence.map(e => e.reference))), gatedRefs = new Set(claimsAll.filter(c => c.section === 7 && !claims.some(x => x.id === c.id)).flatMap(c => c.evidence.map(e => e.reference)));
  const out = Object.keys(cards).filter(k => gatedRefs.has(cards[k].reference) && !shown.has(cards[k].reference)); out.forEach(k => delete cards[k]);
  if (out.length) console.error("NOTE: " + out.length + " study cards left out with their section 7 claims: " + out.join(", ")); }
if (held.length) console.error("NOTE: " + held.length + " claims shown at their last checked version: " + held.join("; "));
if (unseen.length) console.error("NOTE: " + unseen.length + " new claims not shown until their anchors are second-read: " + unseen.join(", "));
const monos = loadAll(path.join(ROOT, "data/monographs"));
const site = f => JSON.parse(fs.readFileSync(path.join(ROOT, "data/site", f), "utf8"));
const epiAll = ["europe", "global", "greece", "us"].flatMap(n => { const p = path.join(ROOT, "data/epidemiology", n + ".json"); return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, "utf8")).map(r => Object.assign({ _file: n }, r)) : []; });
const mapsPath = path.join(ROOT, "data/evidence-maps.json");
const maps = fs.existsSync(mapsPath) ? JSON.parse(fs.readFileSync(mapsPath, "utf8")) : {};
const data = [
  "const EVIDENCE_MAPS = " + JSON.stringify(maps) + ";",
  "const REFS = " + JSON.stringify(refs) + ";",
  // Study cards are most of the page's weight and are read one at a time: the page carries a small index (what counts, labels and
  // the research-gap lines need) and each substance's full cards are published next to it as data/cards-<substance>.json, loaded when a card is opened.
  "const STUDY_CARDS = " + JSON.stringify(Object.fromEntries(Object.entries(cards).map(([id, c]) => [id, { reference: c.reference, substance: c.substance, design: c.design, what_would_settle_it: c.what_would_settle_it || null, verification: { status: c.verification.status, source_read: c.verification.source_read || "" } }]))) + ";",
  // the page leaves out what it never shows (each claim's changelog, and who located or checked each anchor and when); the data files keep it
  "const CLAIMS = " + JSON.stringify(claims.map(c => { const { changelog, ...rest } = c; return Object.assign(rest, { evidence: c.evidence.map(e => { const { located_by, located_on, checked_by, checked_on, check_note, ...ee } = e; return ee; }) }); })) + ";",
  "const MONO = " + JSON.stringify(monos.find(m => m.slug === "methamphetamine") || monos[0]) + ";",
  "const MONOS = " + JSON.stringify(monos) + ";",
  "const SUBSTANCES = " + JSON.stringify(site("substances.json")) + ";",
  "const EPI = " + JSON.stringify(site("landing-stats.json")) + ";",
  "const CLASSES = " + JSON.stringify(site("classes.json")) + ";",
  "const FAMILIES_PLAIN = " + JSON.stringify(site("families-plain.json")) + ";",
  // links to harm reduction groups and official leaflets, each fetched and checked (data/site/harm-links.json; decision p-no-doses)
  // Staying safer: home tests, where kits can be had, first aid by family; only lines a second reader checked (decision s-stay-safer)
  "const STAY_SAFER = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/stay-safer.json"); if (!fs.existsSync(f)) return { tests: {}, signs: {} };
    const d = JSON.parse(fs.readFileSync(f, "utf8")), slim = l => Object.assign({ line: l.line, anchors: (l.anchors || []).map(a => a.reference ? { ref: a.reference } : { publisher: a.publisher, title: a.title, url: a.url }) }, l.kind ? { kind: l.kind } : {}); // a paper is cited by its reference id; kind: where the drug page shows a first-aid line (calm, help, aid)
    const mapL = o => Object.fromEntries(Object.entries(o || {}).map(([k, v]) => [k, v.map(slim)]));
    return { checked_note: d.checked_note, tests: { common: (d.tests.common || []).map(slim), drugs: mapL(d.tests.drugs), more: mapL(d.tests.more), where: mapL(d.tests.where), none_found: d.tests.none_found || [], none_validated: d.tests.none_validated || [] },
      signs: Object.fromEntries(Object.entries(d.signs || {}).map(([k, v]) => [k, mapL(v)])) }; })()) + ";",
  // Where to get tests, country by country: only records a second reader confirmed (data/site/tests-world.json; decision p-kits-world)
  "const TESTS_WORLD = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/tests-world.json"); if (!fs.existsSync(f)) return { sellers: [], post: [], free: [], law: [] };
    const d = JSON.parse(fs.readFileSync(f, "utf8")), a = l => (l || []).map(x => ({ publisher: x.publisher, title: x.title, url: x.url }));
    const line = x => Object.assign({}, x, { anchors: a(x.anchors) });
    return { sellers: d.sellers.map(x => Object.assign({}, x, { anchors: a(x.anchors), pointers: a(x.pointers), warning: x.warning ? line(x.warning) : null })), post: d.post.map(line), free: d.free.map(line), law: d.law.map(line) }; })()) + ";",
  "const HARM_LINKS = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/harm-links.json")) ? site("harm-links.json") : { drugs: {} }) + ";",
  // what each study's funding or authors' ties were, flagged where they bear on the finding (data/site/funding-flags.json, keyed by study card)
  "const FUNDING_FLAGS = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/funding-flags.json")) ? site("funding-flags.json") : {}) + ";",
  // how much people ask about each answer's question (data/site/demand.json, from real questions; used to put the most-asked answers first)
  "const DEMAND = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/demand.json")) ? (() => { const q = site("demand.json"); return q.claims || {}; })() : {}) + ";",
  "const MIX_DRUGS = " + JSON.stringify((() => { const q = site("mix-drugs.json"); delete q._note; return q; })()) + ";",
  // which drug pages each answer on test kits belongs to (navigation only; data/site/kits-for.json)
  "const KITS_FOR = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/kits-for.json"); if (!fs.existsSync(f)) return {}; const q = JSON.parse(fs.readFileSync(f, "utf8")); delete q._note; return q; })()) + ";",
  "const ALIASES = " + JSON.stringify(site("aliases.json")) + ";",
  "const ALIASES_EL = " + JSON.stringify(site("aliases-el.json")) + ";",
  "const GLOSSARY = " + JSON.stringify(site("glossary.json")) + ";",
  "const DECISIONS = " + JSON.stringify(site("decisions.json")) + ";",
  "const FEEL_LITTLE = " + JSON.stringify((() => { const q = site("feel-little.json"); delete q._note; return q; })()) + ";",
  "const INTERACTION_TOPICS = " + JSON.stringify((() => { const q = site("interaction-topics.json"); delete q._note; return q; })()) + ";",
  "const EPI_ALL = " + JSON.stringify(epiAll.map(r => ({ id: r.id, value: r.value, unit: r.unit, interval: r.interval || null, measure: r.measure, def: trimQuotes(r.measure_definition, r.value), substance: r.substance, population: r.population, geography: r.geography, data_year: r.data_year, source: r.source, edition: r.source_edition_year, where: trimQuotes(r.page_or_table, r.value), url: r.url, status: r.verification.status, verified_on: r.verification.verified_on || null, label: r.display && r.display.label || null, file: r._file }))) + ";",
  "const EPI_MAP = " + JSON.stringify((() => { const q = site("epi-substance-map.json"); delete q._note; return q; })()) + ";",
  "const IDENTITY = " + JSON.stringify(loadAll(path.join(ROOT, "data/identity"))) + ";",
  "const LEGAL = " + JSON.stringify(loadAll(path.join(ROOT, "data/legal")).map(d => Object.assign({}, d, { entries: d.entries.map(e => { const { source_title, history, ...ee } = e; return ee; }) }))) + ";",
  "const QUESTIONS = " + JSON.stringify((() => { const q = site("questions.json"); delete q._note; for (const [slug, groups] of Object.entries(q)) { const m = monos.find(x => x.slug === slug); if (!m) continue; const inMono = new Set(m.sections.flatMap(x => x.claims)); const asked = groups.flatMap(g => g.items.map(i => i[0])); const missing = [...inMono].filter(id => !asked.includes(id)), extra = asked.filter(id => !inMono.has(id)), dup = asked.filter((id, i) => asked.indexOf(id) !== i); if (missing.length || extra.length || dup.length) console.error("WARNING: questions.json for " + slug + ": missing " + missing.join(", ") + "; not in the monograph " + extra.join(", ") + "; twice " + dup.join(", ")); } return q; })()) + ";",
  "const SIMPLE = " + JSON.stringify((() => { const q = site("simple.json"); delete q._note;
    // reading level of the simplest layer (Flesch-Kincaid grade, rough syllable count): warn above grade 7
    const syl = w => { w = w.toLowerCase().replace(/[^a-z]/g, ""); if (!w) return 0; if (w.length <= 3) return 1; w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, "").replace(/^y/, ""); const m = w.match(/[aeiouy]{1,2}/g); return m ? m.length : 1; };
    const grade = t => { const words = t.split(/\s+/).filter(Boolean); const sents = Math.max(1, (t.match(/[.!?]+/g) || []).length); const sy = words.reduce((a, w) => a + syl(w), 0); return 0.39 * words.length / sents + 11.8 * sy / words.length - 15.59; };
    // targets (docs/WRITING-RULES.md): short and But lines and True-or-false statements about grade 6 or below; How-we-know points about grade 8 or below.
    // Drug and medicine names push the score up; a line kept above target for that reason is listed in the build log, not changed.
    const over = [];
    for (const [id, c] of Object.entries(q.claims || {})) { for (const k of ["short", "but"]) { const g = grade(c[k] || ""); if (g > 6) over.push(id + "." + k + " " + g.toFixed(1)); } (c.how || []).forEach((t, i) => { const g = grade(t); if (g > 8) over.push(id + ".how[" + i + "] " + g.toFixed(1)); }); }
    for (const [slug, list] of Object.entries(q.tf || {})) list.forEach((x, i) => { const g = grade(x.statement); if (g > 6) over.push("tf." + slug + "[" + i + "] " + g.toFixed(1)); });
    if (over.length) console.error("NOTE: " + over.length + " plain-language lines read above their target grade (most because of drug or medicine names): " + over.join("; "));
    // a simple line written from an older version of its claim is left out until it is rewritten (the site then shows the claim's own plain text)
    const ver = Object.fromEntries(claims.map(c => [c.id, c.version])); const stale = [];
    for (const [id, c] of Object.entries(q.claims || {})) if (c.v && ver[id] && c.v !== ver[id]) { stale.push(id + " (" + c.v + " → " + ver[id] + ")"); delete q.claims[id]; }
    for (const id of Object.keys(q.claims || {})) if (!ver[id]) delete q.claims[id]; // a claim not on the page (waiting for a second reader or the senior gate) takes its simple lines with it
    // the sources named after each "How we know" point must match the points and the claim's own evidence
    const evOf = Object.fromEntries(claims.map(c => [c.id, new Set(c.evidence.map(e => e.reference))])); const badSrc = [];
    for (const [id, c] of Object.entries(q.claims || {})) if (c.how_src) {
      if (!Array.isArray(c.how_src) || c.how_src.length !== (c.how || []).length || c.how_src.some(l => !Array.isArray(l) || l.some(r => !evOf[id] || !evOf[id].has(r)))) { badSrc.push(id); delete c.how_src; }
    }
    if (badSrc.length) console.error("WARNING: sources of 'How we know' points left out (they no longer match the points or the evidence): " + badSrc.join(", "));
    if (stale.length) console.error("NOTE: " + stale.length + " simple lines left out until rewritten for the claim's new version: " + stale.join(", "));
    for (const [slug, list] of Object.entries(q.tf || {})) q.tf[slug] = list.filter(x => { const ok = x.v && ver[x.claim] && x.v === ver[x.claim] && q.claims[x.claim]; if (!ok) console.error("NOTE: True-or-false statement on " + x.claim + " left out until rewritten for the claim's new version"); return ok; });
    // quick questions follow the same rule: written from one version of a claim, shown only while that version stands
    for (const [slug, list] of Object.entries(q.quiz || {})) q.quiz[slug] = list.filter(x => { const ok = x.v && ver[x.claim] && x.v === ver[x.claim] && q.claims[x.claim] && Array.isArray(x.options) && x.options.length === 3 && [0, 1, 2].includes(x.answer); if (!ok) console.error("NOTE: Quick question on " + x.claim + " left out until rewritten for the claim's new version"); return ok; });
    return q; })()) + ";",
  "const WORLD_LAW = " + JSON.stringify((() => { const q = site("world-law.json"); delete q._note; return q; })()) + ";",
  "const DRUGCHECK = " + JSON.stringify(drugCheck) + ";",
  "const EMERGENCY = " + JSON.stringify((() => { const q = site("emergency.json"); delete q._note; return q; })()) + ";",
  "const CURRENCY = " + JSON.stringify((() => { const q = site("currency.json"); delete q._note;
    // a newer study a first reader has read, but that is not yet in the version shown, is 'being checked'
    const cited = Object.fromEntries(claims.map(c => [c.id, new Set(c.evidence.map(e => e.reference))]));
    for (const [id, k] of Object.entries(q.claims || {})) for (const x of k.yes || []) if (x.read && !(cited[id] && cited[id].has(x.ref))) { x.checking = x.read; delete x.read; }
    return q; })()) + ";",
  "const PLANNED_QUESTIONS = " + JSON.stringify((() => { const q = site("planned-questions.json"); delete q._note; return q; })()) + ";",
  "const FORMS = " + JSON.stringify((() => { const q = site("forms.json"); delete q._note; return q; })()) + ";",
  // Photos of what each drug looks like: records from data/site/photos.json, sizes from the web copies made by scripts/build_photos.py
  "const PHOTOS = " + JSON.stringify((() => { const man = path.join(__dirname, "photos", "manifest.json"); const sizes = fs.existsSync(man) ? JSON.parse(fs.readFileSync(man, "utf8")) : {};
    const out = site("photos.json").photos.filter(p => sizes[p.id] && !p.hold).map(p => ({ id: p.id, drug: p.drug, form: p.form, detail: p.detail, alt: p.alt, header: p.header, medicine_example: p.medicine_example, credit: p.credit, changes: p.changes, m: sizes[p.id].m.slice(0, 2), t: sizes[p.id].t.slice(0, 2) }));
    const left = site("photos.json").photos.filter(p => !sizes[p.id]).map(p => p.id); if (left.length) console.error("WARNING: photos without web copies (run scripts/build_photos.py): " + left.join(", "));
    return out; })()) + ";"
].join("\n");
const VERSION = site("version.json");
const data2 = data + "\nconst SITE_VERSION = " + JSON.stringify(VERSION.site) + ";\nconst PROTOCOL_VERSION = " + JSON.stringify(VERSION.protocol) + ";";
const js = [data2, src("app.core.js"), src("app.simple.js"), src("app.views.js")].join("\n\n");
// Refuse to build a page whose script does not parse (a syntax error would blank the site at runtime).
try { new Function(js); } catch (e) { console.error("SYNTAX ERROR in the page script: " + e.message); process.exit(1); }
// The three files share one scope, so a function declared twice silently replaces the first one everywhere: refuse it.
{ const seen = {}, dup = [];
  [["app.core.js", src("app.core.js")], ["app.simple.js", src("app.simple.js")], ["app.views.js", src("app.views.js")]].forEach(([f, t]) => {
    for (const m of t.matchAll(/^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=/gm)) { const n = m[1] || m[2]; if (seen[n]) dup.push(n + " (" + seen[n] + ", " + f + ")"); else seen[n] = f; } });
  if (dup.length) { console.error("DUPLICATE top-level names in the page script: " + dup.join("; ")); process.exit(1); } }
const BUILD_DATE = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "Europe/Athens" });
const BUILD_DATE_LONG = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Athens" });
let html = src("index.template.html").replace("/*__CSS__*/", () => src("styles.css")).replace("/*__JS__*/", () => js).replace('<span id="build-date">16 Oct 2026</span>', () => '<span id="build-date">' + BUILD_DATE + "</span>")
  .replace(/\{\{SITE_VERSION\}\}/g, () => VERSION.site).replace(/\{\{PROTOCOL_VERSION\}\}/g, () => VERSION.protocol).replace(/\{\{BUILD_DATE_LONG\}\}/g, () => BUILD_DATE_LONG);
if (/\{\{[A-Z_]+\}\}/.test(html)) console.error("WARNING: unreplaced {{…}} placeholder in the template");
fs.mkdirSync(path.join(__dirname, "dist"), { recursive: true });
fs.writeFileSync(path.join(__dirname, "dist", "index.html"), html);
// the photo copies are published next to the page as supporting files (dist/img/<id>-m.webp, -t.webp)
const photoDir = path.join(__dirname, "photos"), imgDir = path.join(__dirname, "dist", "img");
{ const dataDir = path.join(__dirname, "dist", "data"); fs.mkdirSync(dataDir, { recursive: true });
  for (const f of fs.readdirSync(dataDir)) if (/^cards-.*\.json$/.test(f)) fs.unlinkSync(path.join(dataDir, f));
  const bySub = {}; for (const [id, c] of Object.entries(cards)) (bySub[c.substance || "other"] = bySub[c.substance || "other"] || {})[id] = c;
  for (const [sub, cs] of Object.entries(bySub)) fs.writeFileSync(path.join(dataDir, "cards-" + sub + ".json"), JSON.stringify(cs));
  console.log("wrote", Object.keys(bySub).length, "card files to dist/data:", Object.entries(bySub).map(([k, v]) => k + " " + Object.keys(v).length).join(", ")); }
if (fs.existsSync(photoDir)) { fs.mkdirSync(imgDir, { recursive: true }); const n = fs.readdirSync(photoDir).filter(f => f.endsWith(".webp")).map(f => fs.copyFileSync(path.join(photoDir, f), path.join(imgDir, f))).length; console.log("copied", n, "photo files to dist/img"); }
console.log("built dist/index.html", (html.length / 1024).toFixed(1) + " KB;", refs.length, "refs,", Object.keys(cards).length, "cards,", claims.length, "claims; evidence maps:", Object.keys(maps).length);
