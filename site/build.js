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
/* Speed (13 November 2026; the senior author: "every time I open the website… a few seconds pass"). The page was 12.6 MB of
   script, most of it read only on the answer sheet and the research pages. It now carries a light index of everything the start
   page, the drug pages, search and the quiz read; the rest is published next to it and fetched when a view needs it (see "What
   loads when" in app.core.js): data/full-<substance>.json (each claim's full text and grading, what each source says and where,
   the drug's law rows, the sources of its names and its study cards' notes), data/refs.json (every reference in full) and
   data/figures.json (the official figures). */
// the page leaves out what it never shows (each claim's changelog, and who located or checked each anchor and when); the data files keep it
const shownClaims = claims.map(c => { const { changelog, ...rest } = c; return Object.assign(rest, { evidence: c.evidence.map(e => { const { located_by, located_on, checked_by, checked_on, check_note, ...ee } = e; return ee; }) }); });
const SECONDHAND = /\b(second-hand|as summari[sz]ed|as relayed)\b/i;   // the test draftWhy() in app.views.js makes on the statement
const LIGHT_CLAIM = ["id", "substance", "section", "plain", "status", "version", "relation", "pair", "documents_retraction"];
// a claim in the page: what lists, cards, flags and search read; each anchor as [reference, study card, role, anchor status]
const lightClaim = c => { const o = {};
  LIGHT_CLAIM.forEach(k => { if (c[k] != null) o[k] = c[k]; });
  o.grade = { certainty: c.grade.certainty, starting_level: c.grade.starting_level }; o.verification = { status: c.verification.status };
  o.ev = c.evidence.map(e => [e.reference, e.study_card || 0, e.role, e.anchor_status]);
  if (!c.plain) o.title = String(c.statement || "").split(/(?<=[.;])\s/)[0].slice(0, 200);   // search finds a claim without a plain line by its opening words
  if (c.debate) o.debate = 1;                                      // "Researchers disagree" shows before the debate itself is fetched
  if (SECONDHAND.test(c.statement || "")) o.secondhand = 1;        // the reason an early draft gives, before its statement is fetched
  return o; };
// the rest of a claim, in its substance's file: every other field, the grading's domains and reasoning, and each anchor's text and place
const heavyClaim = c => { const o = {};
  Object.entries(c).forEach(([k, v]) => { if (!LIGHT_CLAIM.includes(k) && !["grade", "verification", "evidence"].includes(k)) o[k] = v; });
  const { certainty, starting_level, ...g } = c.grade, { status, ...v } = c.verification;
  o.grade = g; o.verification = v;
  o.evidence = c.evidence.map(e => { const { reference, study_card, role, anchor_status, ...rest } = e; return rest; });
  return o; };
const legalDocs = loadAll(path.join(ROOT, "data/legal")).map(d => Object.assign({}, d, { entries: d.entries.map(e => { const { source_title, history, ...ee } = e; return ee; }) }));
const identityDocs = loadAll(path.join(ROOT, "data/identity"));
// what search and the drug pages read of a drug's names (all names, street names and members' names); the sources and forms are in its file
const lightIdentity = d => ({ substance: d.substance, names: d.names, street_names: d.street_names, verification: d.verification,
  members: (d.members || []).map(m => ({ name: m.name, inn: m.inn, synonyms: m.synonyms, cas: m.cas })) });
// a reference in the page: what in-text labels, links and source lists need (every author's surname, the year, the title); the full record is in data/refs.json
const lightRef = r => { const o = { id: r.id, author: (r.author || []).map(a => { const x = a.literal != null ? { literal: a.literal } : { family: a.family }; if (a.short) x.short = a.short; return x; }), issued: r.issued, title: r.title };
  ["year_suffix", "no_author", "short_title", "DOI", "_aux"].forEach(k => { if (r[k] != null) o[k] = r[k]; });
  if (!r.DOI && r.URL) o.URL = r.URL;
  return o; };
const epiRows = epiAll.map(r => ({ id: r.id, value: r.value, unit: r.unit, interval: r.interval || null, measure: r.measure, def: trimQuotes(r.measure_definition, r.value), substance: r.substance, population: r.population, geography: r.geography, data_year: r.data_year, source: r.source, edition: r.source_edition_year, where: trimQuotes(r.page_or_table, r.value), url: r.url, status: r.verification.status, verified_on: r.verification.verified_on || null, label: r.display && r.display.label || null, file: r._file }));
const epiMap = (() => { const q = site("epi-substance-map.json"); delete q._note; return q; })();
// how many checked figures each drug page has (the drug list and the research page's contents read it before the figures are fetched)
const figureCount = {}; epiRows.filter(r => r.status === "verified").forEach(r => (epiMap[r.substance] || []).forEach(s => { figureCount[s] = (figureCount[s] || 0) + 1; }));
// each substance's file: its claims' full text, its law rows, its names' sources and its study cards' notes
const full = {}, fullOf = s => (full[s] = full[s] || { claims: {} });
shownClaims.forEach(c => { fullOf(c.substance).claims[c.id] = heavyClaim(c); });
legalDocs.forEach(d => { fullOf(d.substance).legal = d; });
identityDocs.forEach(d => { const { names, street_names, verification, ...rest } = d; fullOf(d.substance).identity = rest; });
Object.entries(cards).forEach(([id, c]) => { if (!c.substance || !(c.what_would_settle_it || c.verification.source_read)) return; const f = fullOf(c.substance); (f.cards = f.cards || {})[id] = { what_would_settle_it: c.what_would_settle_it || null, source_read: c.verification.source_read || "" }; });
let simpleShown = null;
/* Sourced lines (first aid, test kits, each drug's description): a line goes on the page with the anchors a second reader has
   checked at the source ("confirmed", or "partly" / "corrected" where the line was then rewritten to what the source says).
   A line whose anchors all still wait for that check is left out and listed here (CLAUDE.md: nothing unverified). */
const ANCHOR_OK = new Set(["confirmed", "partly", "corrected"]);
const slimLine = l => Object.assign({ line: l.line, anchors: (l.anchors || []).filter(a => ANCHOR_OK.has(a.check)).map(a => a.reference ? { ref: a.reference } : { publisher: a.publisher, title: a.title, url: a.url }) }, l.kind ? { kind: l.kind } : {}, Array.isArray(l.only) ? { only: l.only } : {});   // only: the drug pages a "For you" line is shown on (written for those)
const sourcedLines = (list, what) => (list || []).map(slimLine).filter(l => { if (l.anchors.length) return true; console.error("NOTE: a line of " + what + " is left out until a second reader has checked a source for it: " + String(l.line).slice(0, 70)); return false; });
const data = [
  "const EVIDENCE_MAPS = " + JSON.stringify(maps) + ";",
  "const REFS = " + JSON.stringify(refs.map(lightRef)) + ";",
  // Study cards are read one at a time: the page carries a small index (what counts and labels need) and each substance's full
  // cards are published next to it as data/cards-<substance>.json, loaded when a card is opened; the research-gap lines come with the substance's file.
  "const STUDY_CARDS = " + JSON.stringify(Object.fromEntries(Object.entries(cards).map(([id, c]) => [id, { reference: c.reference, substance: c.substance, design: c.design, verification: { status: c.verification.status }, full: c.verification.source_read && !/^abstract/i.test(c.verification.source_read) ? 1 : 0 }]))) + ";",
  "const CLAIMS = " + JSON.stringify(shownClaims.map(lightClaim)) + ";",
  // the substances that have a file of their own (data/full-<substance>.json), and each drug page's number of checked figures
  "const FULL_FILES = " + JSON.stringify(Object.keys(full).sort()) + ";",
  "const FIGURE_COUNT = " + JSON.stringify(figureCount) + ";",
  "const MONO = " + JSON.stringify(monos.find(m => m.slug === "methamphetamine") || monos[0]) + ";",
  "const MONOS = " + JSON.stringify(monos) + ";",
  "const SUBSTANCES = " + JSON.stringify(site("substances.json")) + ";",
  "const EPI = " + JSON.stringify(site("landing-stats.json")) + ";",
  "const CLASSES = " + JSON.stringify(site("classes.json")) + ";",
  "const FAMILIES_PLAIN = " + JSON.stringify(site("families-plain.json")) + ";",
  // links to harm reduction groups and official leaflets, each fetched and checked (data/site/harm-links.json; decision p-no-doses)
  // Staying safer: home tests, where kits can be had, first aid by family; only lines a second reader checked (decision s-stay-safer).
  // (How these lines are checked is said once, on the Methods page, not under each list: site 2.3.)
  "const STAY_SAFER = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/stay-safer.json"); if (!fs.existsSync(f)) return { tests: {}, signs: {} };
    const d = JSON.parse(fs.readFileSync(f, "utf8")), slim = slimLine; // a paper is cited by its reference id; kind: where the drug page shows a first-aid line (calm, help, aid)
    const mapL = o => Object.fromEntries(Object.entries(o || {}).map(([k, v]) => [k, sourcedLines(v, "stay-safer " + k)]));
    return { tests: { common: (d.tests.common || []).map(slim), drugs: mapL(d.tests.drugs), more: mapL(d.tests.more), where: mapL(d.tests.where), none_found: d.tests.none_found || [], none_validated: d.tests.none_validated || [] },
      signs: Object.fromEntries(Object.entries(d.signs || {}).map(([k, v]) => [k, mapL(v)])) }; })()) + ";",
  // Where to get tests, country by country: only records a second reader confirmed (data/site/tests-world.json; decision p-kits-world)
  "const TESTS_WORLD = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/tests-world.json"); if (!fs.existsSync(f)) return { sellers: [], post: [], free: [], law: [] };
    const d = JSON.parse(fs.readFileSync(f, "utf8")), a = l => (l || []).map(x => ({ publisher: x.publisher, title: x.title, url: x.url }));
    const line = x => Object.assign({}, x, { anchors: a(x.anchors) });
    return { sellers: d.sellers.map(x => Object.assign({}, x, { anchors: a(x.anchors), pointers: a(x.pointers), warning: x.warning ? line(x.warning) : null })), post: d.post.map(line), free: d.free.map(line), law: d.law.map(line) }; })()) + ";",
  // Each drug's description under its name: two to four short sourced lines (data/site/descriptions.json, when it exists)
  "const DESCRIPTIONS = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/descriptions.json"); if (!fs.existsSync(f)) return {};
    const d = JSON.parse(fs.readFileSync(f, "utf8")).drugs || {};
    return Object.fromEntries(Object.entries(d).map(([slug, x]) => [slug, sourcedLines(x && x.lines, "the description of " + slug)]).filter(([, lines]) => lines.length)); })()) + ";",
  // A seller's own page for one drug's test kits (data/site/kit-links.json, when it exists): only links a second reader
  // confirmed, keyed by the seller's name as the drug page finds it (lower case, no accents)
  "const KIT_LINKS = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/kit-links.json"); if (!fs.existsSync(f)) return {};
    const d = JSON.parse(fs.readFileSync(f, "utf8")).sellers || {}, key = n => String(n == null ? "" : n).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim(), out = {};
    Object.values(d).forEach(x => { const links = Object.fromEntries(Object.entries((x && x.drugs) || {}).filter(([, l]) => l && /^https:\/\//.test(l.url || "") && ANCHOR_OK.has(l.check)).map(([slug, l]) => [slug, Object.assign({ url: l.url, label: l.label || "" }, x.lang ? { lang: x.lang } : {}, x.note ? { note: x.note } : {})]));
      if (x && x.name && Object.keys(links).length) out[key(x.name)] = links; });
    return out; })()) + ";",
  "const HARM_LINKS = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/harm-links.json")) ? site("harm-links.json") : { drugs: {} }) + ";",
  // what each study's funding or authors' ties were, flagged where they bear on the finding (data/site/funding-flags.json, keyed by study card)
  "const FUNDING_FLAGS = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/funding-flags.json")) ? site("funding-flags.json") : {}) + ";",
  // how much people ask about each answer's question (data/site/demand.json, from real questions; used to put the most-asked answers first)
  "const DEMAND = " + JSON.stringify(fs.existsSync(path.join(ROOT, "data/site/demand.json")) ? (() => { const q = site("demand.json"); return q.claims || {}; })() : {}) + ";",
  "const MIX_DRUGS = " + JSON.stringify((() => { const q = site("mix-drugs.json"); delete q._note; return q; })()) + ";",
  // which drug pages each answer on test kits belongs to (navigation only; data/site/kits-for.json)
  "const KITS_FOR = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/kits-for.json"); if (!fs.existsSync(f)) return {}; const q = JSON.parse(fs.readFileSync(f, "utf8")); delete q._note; return q; })()) + ";",
  // how the pages that are not one drug's page are cut into sections (data/site/pages.json; site 2.4)
  "const PAGES = " + JSON.stringify((() => { const f = path.join(ROOT, "data/site/pages.json"); if (!fs.existsSync(f)) return {}; const q = JSON.parse(fs.readFileSync(f, "utf8")); delete q._note; return q; })()) + ";",
  "const ALIASES = " + JSON.stringify(site("aliases.json")) + ";",
  "const ALIASES_EL = " + JSON.stringify(site("aliases-el.json")) + ";",
  "const GLOSSARY = " + JSON.stringify(site("glossary.json")) + ";",
  // the senior author's open decisions are read only on the review page: they arrive from data/decisions.json when it opens
  "const DECISIONS = {};",
  "const FEEL_LITTLE = " + JSON.stringify((() => { const q = site("feel-little.json"); delete q._note; return q; })()) + ";",
  "const INTERACTION_TOPICS = " + JSON.stringify((() => { const q = site("interaction-topics.json"); delete q._note; return q; })()) + ";",
  // the official figures arrive from data/figures.json when the statistics page or a research page needs them
  "const EPI_ALL = [];",
  "const EPI_MAP = " + JSON.stringify(epiMap) + ";",
  "const IDENTITY = " + JSON.stringify(identityDocs.map(lightIdentity)) + ";",
  // which drugs have law rows, and how many; the rows come with the drug's file
  "const LEGAL = " + JSON.stringify(legalDocs.map(d => ({ substance: d.substance, n: d.entries.length }))) + ";",
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
    /* Myth or fact: only the interesting cards, best first (senior author, 15 November: "less than half of them are interesting
       for most users. they feel a lot like an academic test"). data/site/tf-interest.json, when it exists, scores each statement
       (keyed by the first 12 hex characters of the SHA-1 of its words): a card under the cut for interest or for clarity is left
       out of every deck; the others carry their interest (i) and each deck lists them highest first (the page deals them in
       that order; equal scores as before). A card with no entry is shown as before. Until the file exists nothing changes. */
    { const tfi = path.join(ROOT, "data/site/tf-interest.json");
      if (fs.existsSync(tfi)) { const T = JSON.parse(fs.readFileSync(tfi, "utf8")), cut = T.cut || {}, items = T.items || {}; let out = 0, kept = 0, plain = 0;
        const key = t => require("crypto").createHash("sha1").update(String(t), "utf8").digest("hex").slice(0, 12), under = (v, c) => typeof c === "number" && typeof v === "number" && v < c;
        const iOf = x => typeof x.i === "number" ? x.i : -1;
        for (const [slug, list] of Object.entries(q.tf || {})) q.tf[slug] = list.filter(x => { const e = items[key(x.statement)]; if (!e) { plain++; return true; }
            if (under(e.interest, cut.interest) || under(e.clear, cut.clear)) { out++; return false; } if (typeof e.interest === "number") x.i = e.interest; kept++; return true; })
          .map((x, n) => [x, n]).sort((a, b) => iOf(b[0]) - iOf(a[0]) || a[1] - b[1]).map(p => p[0]);
        console.log("Myth or fact: " + out + " cards left out (under the cut in data/site/tf-interest.json: interest " + cut.interest + ", clear " + cut.clear + "); " + kept + " scored cards kept, " + plain + " without a score shown as before"); } }
    // "Why this rating" in plain words is read only on the answer sheet and the research pages: it travels with the claim's file (speed)
    const subOf = Object.fromEntries(shownClaims.map(c => [c.id, c.substance]));
    for (const [id, c] of Object.entries(q.claims || {})) if (c.rate && subOf[id]) { fullOf(subOf[id]).claims[id].rate = c.rate; delete c.rate; }
    simpleShown = q;   // the answers Insight indexes are exactly the ones with plain lines on the page (below)
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
// (site 2.6) the build's own stamp: the site now publishes itself, so the version number no longer tells one publishing from the
// next; the page asks its kept questions again once per stamp, and a small file beside the page (data/build.json) lets an open
// page learn that a newer one exists
const SITE_BUILD = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "");
/* The machine lane (site 2.6; docs/AUTOMATION.md; scripts/auto/lane.py): answers the system wrote by itself from papers it found
   and read, published before a person has checked them, each with its label. Only "published" records are shown, never one
   the senior author has taken down (data/auto/held.json), and each is looked at once more here, by code: a record that lacks a
   part or a source, or holds an amount of a drug, advice or a quotation, is left out and named. PK_AUTO_FIXTURE: the folder of
   pretend answers that scripts/ux/auto_check.js builds with (site/build_public.py refuses to publish such a build). */
const AUTO_DIR = process.env.PK_AUTO_FIXTURE ? path.resolve(process.env.PK_AUTO_FIXTURE) : path.join(ROOT, "data", "auto", "answers");
// what of the lane the site may show and say (data/auto/lane/policy.json). loop: true only once the half-hourly run is on and has
// been seen to answer questions visitors sent; until then the page does not promise it (PK_AUTO_LOOP=1: the checks' build)
const AUTO_POLICY = (() => { const f = path.join(ROOT, "data", "auto", "lane", "policy.json"); return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : {}; })();
const AUTO_LOOP = process.env.PK_AUTO_LOOP ? process.env.PK_AUTO_LOOP === "1" : AUTO_POLICY.loop === true;
// amounts: answers about amounts are shown only once the editor has read the first real ones the lane wrote (the checks' build shows its pretend ones)
const AUTO_AMOUNTS = process.env.PK_AUTO_FIXTURE ? true : AUTO_POLICY.amounts === true;
const startedPages = {};   // (2.8) {slug: name} of the pages the system started that have an answer to show
// (2.15.2) what our system has done so far with each listed question, in one word, for the reader's own list of sent questions: "new"
// (not tried yet), "trying" (2.21, lane 19: a try gave no answer, or one that a reader could not yet read, and the system is trying again by itself today),
// "tried" (no answer has passed the checks today; it is tried again another day), "nosource" (nothing that can be read is published on it),
// "editor" (written; one of the few kinds an editor reads before it shows: an amount, suicide, what to do in an emergency, an answer that differs from a checked one)
const AUTO_STATE = (() => {
  const out = {}; let st = {}, held = {};
  try { st = JSON.parse(fs.readFileSync(path.join(ROOT, "data/auto/lane/state.json"), "utf8")).items || {}; } catch (e) { st = {}; }
  try { held = JSON.parse(fs.readFileSync(path.join(ROOT, "data/auto/held.json"), "utf8")); } catch (e) { held = {}; }
  const listed = [], todayUTC = new Date().toISOString().slice(0, 10), newestLane = +((fs.readFileSync(path.join(ROOT, "scripts", "auto", "lane.py"), "utf8").match(/^LANE = (\d+)/m) || [])[1]) || Math.max(1, ...Object.values(st).map(s => +(s && s.lane) || 1));   // the lane as it is now (scripts/auto/lane.py, LANE)
  // how many sources the finders hold for a question (the papers that can be read, the official pages)
  const sources = id => { let n = 0; for (const [f, k] of [["data/auto/papers/" + id + ".json", "can_read"], ["data/auto/official/found/" + id + ".json", "pages"]]) { try { n += (JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8"))[k] || []).length; } catch (e) { /* not searched yet */ } } return n; };
  for (const f of ["data/site/wanted.json", "data/auto/wanted-auto.json"]) { try { listed.push(...(JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8")).items || [])); } catch (e) { /* no such list yet */ } }
  for (const w of listed) { if (!w || !/^w_[a-z0-9_]{1,40}$/.test(String(w.id))) continue; const s = st[w.id];
    const nothing = s && s.status === "none" && !s.soft && /no source that can be read/.test(String(s.why || "")) && !sources(w.id);   // (not where a source or a search could not be fetched: "soft": that is tried again, and the page must not say that nothing is published)
    // (the lane tries a question again the same day by itself: at once after a fault that was not the answer's ("soft"), once or twice more with other models after an answer that did not pass ("n": tries today); an answer of an older lane is written again)
    const again = s && (!!s.soft || s.for === "again" || (+s.lane || 1) < newestLane || (s.last === todayUTC && (+s.n || 1) < 2));
    out[w.id] = !s ? "new" : s.status === "published" ? "" : s.status === "waiting" ? (s.for === "editor" ? "editor" : "trying") : nothing ? "nosource" : s.status === "none" ? (again ? "trying" : "tried") : "new";
    if (!out[w.id]) delete out[w.id]; }
  return out;
})();
const AUTO_SHOWN = (() => {
  // (2.21) a hold is of the version the editor read ("lane"): an answer written again by a newer lane is judged afresh by the gates and is not held by that entry
  const heldFile = path.join(ROOT, "data", "auto", "held.json"), heldOf = new Map((fs.existsSync(heldFile) ? (JSON.parse(fs.readFileSync(heldFile, "utf8")).held || []) : []).map(x => [x && x.id || x, x]));
  // (2.21.1) "run": the hold is of the one version that run wrote (made.run): an answer of the SAME lane written again with what the editor found is judged afresh and shown
  const held = { has: (id, lane, run) => { const h = heldOf.get(id); if (!h) return false; if (typeof h === "object" && h.run != null) return String(run || "") === String(h.run); return typeof h !== "object" || h.lane == null || (+lane || 1) <= +h.lane; } };
  const drugSlugs = new Set(site("substances.json").map(s => s.slug)), out = [], left = [];
  // an answer written by an older lane than data/auto/lane/policy.json allows is not shown (the lane writes it again)
  const minLane = +AUTO_POLICY.show_from_lane || 1; let older = 0, held_amounts = 0;
  const bad = /\b\d+(?:[.,]\d+)?\s?(?:mg|milligrams?|µg|ug|mcg|micrograms?|g|grams?|ml|pills?|tablets?|tabs?|capsules?|lines?|hits?|drops?)\b|\byou\s+(?:should|must|need to)\b|["“”]|\bre-?dos\w*/i;
  // (site 2.7, lane 3) an answer about amounts (docs/AUTOMATION.md, decision 11): its three lines are the code's own (data/auto/lane/lines.json),
  // and each amount stands in its source's own words, 15 at most, found in the longer quote the record keeps
  const LINES = (() => { const f = path.join(ROOT, "data", "auto", "lane", "lines.json"); return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : null; })();
  // (2.8) the pages the system may start, by name, and the general pages an answer can belong to (the page's own keys for them)
  const readJson = (...p) => { const f = path.join(ROOT, ...p); try { return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : null; } catch (e) { return null; } };
  const START_PAGES = new Set([].concat(((readJson("data", "auto", "filing.json") || {}).pages) || [], Object.keys(((readJson("data", "auto", "pages.json") || {}).pages) || {})));
  const GEN_HOMES = { facts: "general", numbers: "numbers", checking: "drug-checking", law: "law", interactions: "interactions" };
  const pageSlug = n => String(n).toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
  // (2.7.2) a count of drinks or units may be written as a word ("two drinks or less in a day"): the same pattern as scripts/auto/lane.py (AMT)
  const NUM = "(?:\\d+(?:[.,]\\d+)?|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one)(?=(?:\\s*(?:to|-|or)\\s*[\\w-]+)?\\s+(?:or\\s+(?:more|less|fewer)\\s+)?(?:standard\\s+)?(?:drinks?|units?)\\b))";
  const AMT = new RegExp("(?<![\\w.,\\/])" + NUM + "(?:\\s*(?:to|-|or)\\s*" + NUM + ")?(?:\\s+or\\s+(?:more|less|fewer))?\\s?(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|units?|standard drinks?|drinks?)\\b", "i");
  const flat = t => String(t || "").normalize("NFKC").replace(/[‘’‚′`]/g, "'").replace(/[“”„″]/g, '"').replace(/[‐‑‒–—−]/g, "-").replace(/\s+/g, " ").trim();
  // (2.8.1) the lane's own rules for what an amount's shown words never hold, kept here too: the build is the last gate. An amount for each
  // kilogram of body weight, however written ("3 mg/kg", "3 mg per kilogram", "6 mg kg(-1)"), and a summary's flattened signs ("mg day(-1)", "</=300 mg")
  const perKg = /\d\s?(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml)\s*(?:\/\s*(?:kg\b|kilo)|[·.]?\s*kg\b|\s+(?:of\s+[\w-]+\s+)?(?:per|for\s+each|for\s+every|a|each)\s+(?:kg\b|kilo))/i, oddSigns = /\(-?\d\)|[<>]\s?\/?\s?=|\^\s?-?\d|=\s?\/?[<>]/;
  const timing = /\bre-?dos\w*|\bevery\s+\d+(?:\s*(?:to|-|or)\s*\d+)?\s+(?:minutes?|hours?)\b|\b\d+\s+(?:minutes?|hours?)\s+(?:before|after|apart|later)\b|\bsupplement\w*|\byou\s+(?:should|must|need to)\b/i;
  for (const f of (fs.existsSync(AUTO_DIR) ? fs.readdirSync(AUTO_DIR) : []).filter(f => /^au_[a-z0-9_]+\.json$/.test(f)).sort()) {
    const a = JSON.parse(fs.readFileSync(path.join(AUTO_DIR, f), "utf8"));
    if (a.status !== "published" || held.has(a.id, a.lane, a.made && a.made.run)) continue;
    if ((+a.lane || 1) < minLane) { older++; continue; }
    if (a.kind === "amounts" && !AUTO_AMOUNTS) { held_amounts++; continue; }
    const part = k => (a.parts || []).filter(p => p.part === k || (k === "how" && /^how\d+$/.test(p.part))).map(p => String(p.text || "").trim()).filter(Boolean);
    // a source's reference: a paper's Crossref record (it has a DOI), or an official page's own (a web page with its body's name and its https address)
    const short = part("short")[0], but = part("but")[0], how = part("how"), first = part("first")[0] || "", amounts = a.kind === "amounts";
    const refs = (a.sources || []).map(s => s.ref).filter(r => r && r.id && r.title && Array.isArray(r.author) && r.author.length && (r.DOI || (r.type === "webpage" && /^https:\/\/[^\s"<>]+$/.test(r.URL || "") && r.author[0].literal)));
    const mf = (a.made || {}).from, from = mf && typeof mf === "object" ? { papers: +mf.papers || 0, summaries: +mf.summaries || 0, official: +mf.official || 0 } : { papers: refs.length, summaries: 0, official: 0 };
    const rows = amounts ? (a.parts || []).filter(p => /^row\d+$/.test(p.part)).map(p => ({ who: String(p.who || "").trim(), what: String(p.what || "").trim(), quote: String(p.quote || "").trim(), ref: p.source, read: p.read === "summary" ? "summary" : p.read === "page" ? "page" : "full", on: ((p.rests_on || [])[0] || {}).quote || "" })) : [];
    // (2.7.2) every amount an official body's guidance (a web page that is not a medicine's label): the answer may carry the But written for that
    const guidance = rows.length > 0 && !!(LINES && LINES.amounts_but_guidance) && rows.every(r => { const x = refs.find(y => y.id === r.ref); return !!x && x.type === "webpage" && x.genre !== "Drug label"; });
    const classLine = LINES ? ((Object.values(LINES.first).find(v => v.drugs.some(d => (a.drugs || []).includes(d))) || {}).text || "") : "";
    let why = !/^au_[a-z0-9_]+$/.test(a.id || "") || a.id + ".json" !== f ? "its name" : !a.question || !short || !but ? "a part is missing" : !refs.length || refs.length !== (a.sources || []).length ? "a source without its reference"
      : from.papers + from.summaries + from.official !== refs.length ? "its count of sources" : "";
    if (!why && !amounts) why = !how.length ? "a part is missing" : first ? "a line only an answer about amounts may carry" : [short, but].concat(how).some(t => bad.test(t)) ? "an amount, advice or a quotation in its text" : (a.parts || []).some(p => !(p.rests_on || []).length) ? "a sentence that rests on nothing" : "";
    if (!why && amounts) why = !LINES ? "the lines the code writes are missing" : short !== LINES.amounts || !(but === LINES.amounts_but || (guidance && but === LINES.amounts_but_guidance)) || first !== classLine ? "a line that is not the code's own" : !rows.length ? "no amount"
      : rows.some(r => !r.who || !r.what || !r.quote || r.quote.split(/\s+/).length > 15 || !AMT.test(r.quote) || !flat(r.on).includes(flat(r.quote)) || !refs.some(x => x.id === r.ref) || /["“”]/.test(r.who + r.what + r.quote) || AMT.test(r.who + " " + r.what) || timing.test(r.who + " " + r.what + " " + r.quote)) ? "an amount that is not in its source's own words, or too long, or with a time between uses"
      : rows.some(r => perKg.test(r.quote) || oddSigns.test(r.quote)) ? "an amount for each kilogram of body weight, or a notation that is not plain words" : "";
    if (why) { left.push(a.id + " (" + why + ")"); continue; }
    // (2.7.1) under a How-do-we-know line: its source's own words, 15 at most, so that a reader can compare. Shown only when they stand in
    // the longer quote the record keeps for that line and hold nothing the site never shows; otherwise the line stands without them
    const howq = amounts ? [] : (a.parts || []).filter(p => /^how\d+$/.test(p.part) && String(p.text || "").trim()).map(p => { const q = String(p.quote || "").trim();
      return q && q.split(/\s+/).length <= 15 && !/["“”]/.test(q) && !bad.test(q) && !timing.test(q) && (p.rests_on || []).some(r => flat(r.quote).includes(flat(q))) && refs.some(x => x.id === p.quote_ref) ? { q, ref: p.quote_ref } : null; });
    const drugs = (a.drugs || []).filter(d => drugSlugs.has(d));
    // (2.8) where the answer belongs (scripts/auto/place.py wrote it into the record; no model had a say): a drug's page; a page the system
    // starts for a drug that has none (its name must be one the filing knows: data/auto/filing.json, data/auto/pages.json); or one of the
    // general pages. Nothing the system writes belongs on the emergency page: that page is the senior author's.
    const home = String((a.place || {}).home || "");
    if (home === "emergency") { left.push(a.id + " (the emergency page is not written by the system)"); continue; }
    let page = drugs[0] || "general";
    if (!drugs.length && /^new:/.test(home)) { const name = home.slice(4);
      if (!START_PAGES.has(name)) { left.push(a.id + " (a page to start that the filing does not know)"); continue; }
      page = "new:" + pageSlug(name); startedPages[pageSlug(name)] = name; }
    else if (!drugs.length && drugSlugs.has(home)) page = home;
    else if (!drugs.length && GEN_HOMES[home]) page = GEN_HOMES[home];
    out.push(Object.assign({ id: a.id, q: a.question, ways: a.ways || [], short, but, how: amounts ? [] : how, howq, refs, from, made: (a.made || {}).on || "", complete: a.complete === true, wanted: (a.wanted || []).length, drugs, page, risk: typeof a.stakes === "string" && /^[a-z ,-]{3,40}$/.test(a.stakes) ? a.stakes : "" },   // (2.21, lane 19) risk: the answer is about dying, overdose, mixing, pregnancy or children: the page puts the way to the emergency numbers under it
      amounts ? { kind: "amounts", first, rows: rows.map(r => ({ who: r.who, what: r.what, quote: r.quote, ref: r.ref, read: r.read })) } : {}));
  }
  if (left.length) console.error("WARNING: machine-lane answers left out of the site: " + left.join("; "));
  if (older) console.log("machine lane: " + older + " answers written by an older lane are not shown (they will be written again)");
  if (held_amounts) console.log("machine lane: " + held_amounts + " answers about amounts are not shown yet (data/auto/lane/policy.json, amounts: the editor reads the first real ones first)");
  if (out.length) console.log("machine lane: " + out.length + " answers written by the system are shown, each with its label");
  if (Object.keys(startedPages).length) console.log("machine lane: " + Object.keys(startedPages).length + " pages started by the system are shown: " + Object.values(startedPages).join("; "));
  return out;
})();
// (2.12; the senior author, 17 November 2026, of kanna and Mitragyna javanica: "our ai has to create this pages in a perfect coherent
// format to the rest of the website (and find pictures for them ... if the pictures have not been verified and the ai is uncertain
// then we could have a small disclaimer") A page the system should start is shown as soon as people have asked about it, before
// there is an answer to show: its name, what the open list of species says it is, its pictures and what was asked.
// AUTO_SHELL: {slug: {name, science: [{name, kind, gbif}], asked: [{id, q, answer}]}}. The class a page is filed under is not
// shown (data/auto/filing.json: a filing says where an answer is listed; it is not a checked claim). science: the species that
// GBIF matched exactly for the page (scripts/auto/pictures.py) or for a name the system learned (scripts/auto/names_open.py).
// AUTO_PICS: the pictures the system found and fetched (data/auto/pictures.json, site/photos-auto): only CC0 and CC BY, each with
// its maker, licence and record; none was checked by a person, and the page says so. A picture is shown only once the editor has
// looked at it ("looked_by_editor") against the site's rules for photos (docs/WRITING-RULES.md, "Photos": never people or hands,
// the thing itself, nothing else that takes the eye); one the editor holds ("hold") is not shown. No program can judge that yet.
// AUTO_NAMES: the names that lead to such a page ({name: slug}): the page's own, the filing's, the learned ones, the species'.
// AUTO_FORMS (2.23.1, decision 35): for a form of a checked drug page that has no photo of its own, the first picture the system found
// for it (data/auto/pictures.json, "forms"; Wikimedia Commons) that the editor looked at, under the same rules; a checked photo always wins.
const AUTO_SHELL = {}, AUTO_PICS = {}, AUTO_NAMES = {}, AUTO_FORMS = {};
{ const rj = (...p) => { const f = path.join(ROOT, ...p); try { return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : null; } catch (e) { return null; } };
  const pageSlug = n => String(n).toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
  const web = u => (/^https:\/\/[^\s"'<>]+$/.test(String(u || "")) ? String(u) : ""), kindOf = k => (k === "fungus" ? "fungus" : "plant");
  const wq = {}; [rj("data", "site", "wanted.json"), rj("data", "auto", "wanted-auto.json")].forEach(d => ((d || {}).items || []).forEach(w => { wq[w.id] = w.q; }));
  const shown = new Set(AUTO_SHOWN.map(a => a.id)), picDir = path.join(__dirname, "photos-auto"), pics = {}, science = {};
  // a picture a page may show: its web copies made, looked at by the editor, not held, public domain, CC0, CC BY or (where nothing more open exists:
  // scripts/auto/pictures.py, RULE; his word of 19 November, 17:44) CC BY-SA, a maker named for CC BY and CC BY-SA
  const okPic = p => !!p && !!p.file && /^[a-z0-9-]+$/.test(p.file) && !!p.sizes && !p.hold && /^\d{4}-\d{2}-\d{2}$/.test(p.looked_by_editor || "") && /^(?:CC0 1\.0|CC BY(?:-SA)? (?:[1-4]\.0|2\.5)(?: [A-Z]{2})?|Public domain)$/.test(p.licence || "") &&
    (!/^CC BY/.test(p.licence) || !!p.maker) && fs.existsSync(path.join(picDir, p.file + "-m.webp")) && fs.existsSync(path.join(picDir, p.file + "-t.webp"));
  const picOf = (p, more) => Object.assign({ file: p.file, m: p.sizes.m.slice(0, 2), t: p.sizes.t.slice(0, 2), maker: String(p.maker || ""), licence: p.licence,
    licence_url: web(String(p.licence_url || "").replace(/^http:\/\//, "https://")), page: web(p.page) || web(p.record), src: p.source === "commons" ? "commons" : "gbif" }, more);
  const picDoc = rj("data", "auto", "pictures.json") || {};
  for (const [slug, e] of Object.entries(picDoc.pages || {})) {
    const list = [];
    for (const s of Object.values((e || {}).species || {})) {
      if (!s || !s.name) continue;
      if (s.gbif) (science[slug] = science[slug] || []).push({ name: String(s.name), kind: kindOf(s.kind), gbif: +s.gbif });
      // (a picture from a Commons category that is not a species is "an example" of what the category names: "Piracetam" on the page of nootropics)
      for (const p of s.pictures || []) if (okPic(p)) list.push(picOf(p, { species: String(s.name || e.name || slug), kind: s.kind === "thing" ? "thing" : kindOf(s.kind), country: String(p.country || "") }));
    }
    if (list.length) pics[slug] = list; }
  { const forms = site("forms.json"), have = new Set(site("photos.json").photos.filter(p => !p.hold).map(p => p.id));
    for (const e of Object.values(picDoc.forms || {})) {
      const f = e && Array.isArray(forms[e.drug]) ? forms[e.drug].find(x => x && x.id === e.form) : null;
      if (!f || (f.photos || []).some(id => have.has(id))) continue;
      const p = (e.pictures || []).find(okPic); if (p) (AUTO_FORMS[e.drug] = AUTO_FORMS[e.drug] || {})[e.form] = picOf(p, {}); }
    const nf = Object.values(AUTO_FORMS).reduce((n, x) => n + Object.keys(x).length, 0); if (nf) console.log("forms with a picture the system found (looked at by the editor): " + nf); }
  const learned = ((rj("data", "auto", "names", "learned.json") || {}).names) || {};
  for (const e of Object.values(learned)) { const slug = e && e.drug === true && e.source === "gbif" && /^\d+$/.test(String(e.id || "")) && (e.kind === "plant" || e.kind === "fungus") ? pageSlug(e.name) : "";
    if (slug && !science[slug]) science[slug] = [{ name: String(e.name), kind: e.kind, gbif: +e.id }]; }
  for (const [name, v] of Object.entries(((rj("data", "auto", "pages.json") || {}).pages) || {})) {
    const slug = pageSlug(name), asked = ((v || {}).listed || []).filter(id => wq[id]).map(id => ({ id, q: wq[id], answer: shown.has("au_" + id) ? "au_" + id : null }));
    if (!asked.length && !startedPages[slug]) continue;                    // a page is started because people ask
    AUTO_SHELL[slug] = { name, science: science[slug] || [], asked }; if (!startedPages[slug]) startedPages[slug] = name; if (pics[slug]) AUTO_PICS[slug] = pics[slug]; }
  const filing = rj("data", "auto", "filing.json") || {}, lead = (n, slug) => { const k = String(n).toLowerCase().replace(/\s+/g, " ").trim(); if (k.length >= 3 && slug && startedPages[slug] && !AUTO_NAMES[k]) AUTO_NAMES[k] = slug; };
  for (const [slug, name] of Object.entries(startedPages)) { if (!/[(),]/.test(name)) lead(name, slug); ((AUTO_SHELL[slug] || {}).science || []).forEach(s => lead(s.name, slug)); }
  for (const [n, v] of Object.entries(filing.names || {})) if (v && v.new) lead(n, pageSlug(v.new));
  for (const [k, e] of Object.entries(learned)) if (e && e.drug === true) lead(k, pageSlug(e.name || k));
  const fresh = Object.keys(AUTO_SHELL).filter(k => !AUTO_SHOWN.some(a => a.page === "new:" + k));
  if (fresh.length) console.log("machine lane: " + fresh.length + " pages people asked about are shown as started, with no answer yet (" + Object.keys(AUTO_PICS).length + " pages have pictures the system found): " + fresh.map(k => AUTO_SHELL[k].name).join("; "));
}
/* (2.22, 18 November 2026; the senior author: "the site should include all valid drug websites worldwide for every site ... to give instant answers when it
   does not have the answer ready".) OFFICIAL: for every drug of the site (and every page the system started), the pages of official bodies about it, from
   the list the machine lane reads for its own answers (data/auto/official/index.json: addresses and titles only, made by scripts/auto/official.py where a
   body's robots.txt allows it; sources.json names each body). The page shows them, as links, under a question it has no answer to (app.insight.js,
   insOfficialHtml). Nothing here is our text: a body's own page about the drug (main: 1; the page says "<body> on <drug>") or a page of the body whose
   address names the drug, under the body's own title for it.
   { made, src: {body: [its name, its country]}, by: {slug | "new:" + slug: [[body, address, title or "", main]]} }: a drug's own pages first, one a body
   (health services and agencies before information services, in the list's order), then up to thirty pages on a part of the subject. */
const OFFICIAL = (() => {
  const rj = (...p) => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, ...p), "utf8")); } catch (e) { return null; } };
  const idx = rj("data", "auto", "official", "index.json"), srcs = rj("data", "auto", "official", "sources.json"); if (!idx || !srcs) return null;
  const meta = {}; (srcs.sources || []).forEach((s, n) => { meta[s.id] = Object.assign({ n }, s); });
  const flat = s => String(s).toLowerCase().normalize("NFKD").replace(/\.(?:html?|aspx)$/, "").replace(/[^a-z0-9]+/g, " ").trim();
  const JUNK = /^(?:skip\b|cookie|here'?s how you know|search$|menu$|home$|visit the\b|section on\b)/i;   // what a page's navigation says, where the reader took it for the title
  const title = x => { const parts = String(x || "").split(" / ").map(s => s.replace(/[\u200b-\u200f\ufeff]/g, "").replace(/\s+/g, " ").trim()).filter(s => s && !JUNK.test(s)); let s = parts[0] || "";
    if (s.length > 90) s = s.slice(0, 88).replace(/\s+\S*$/, "") + "\u2026"; return s && s === s.toLowerCase() ? s.charAt(0).toUpperCase() + s.slice(1) : s; };
  const pages = [];
  for (const [id, v] of Object.entries(idx.sources || {})) { const m = meta[id]; if (!m || !v || !Array.isArray(v.pages)) continue;
    for (const pg of v.pages) { if (!pg || !/^https:\/\/[^\s"'<>]+$/.test(String(pg.u || ""))) continue; let seg = "", way = "";
      try { const parts = new URL(pg.u).pathname.replace(/\/+$/, "").split("/"); way = flat(decodeURIComponent(parts.join(" "))); seg = parts.pop() || ""; if (/^index\b/i.test(seg)) seg = parts.pop() || ""; seg = flat(decodeURIComponent(seg)); } catch (e) { seg = ""; }
      pages.push({ id, u: pg.u, seg, way, t: title(pg.t) }); } }
  // everyday words that are also street names name nothing in an address; a few names bodies use that the site's own lists do not hold
  const WEAK = new Set("drink pills crystal ice speed tabs brown lean glue toad robo balloons spice oat microdosing vaping pouches solvents butane acid coffee hash dabs edibles tina bufo salvia crack".split(" "));
  const MORE = { psilocybin: ["magic mushrooms"], "prescription-opioids": ["opioids", "opioid painkillers", "prescription opioids"], nicotine: ["smoking", "vaping", "e cigarettes"], "alkyl-nitrites-and-inhalants": ["poppers", "inhalants", "volatile substances"],
    "synthetic-cannabinoids": ["synthetic cannabis", "synthetic cannabinoids"], "nitrous-oxide": ["nitrous oxide"], "dmt-ayahuasca": ["dmt", "ayahuasca"], "salvia-divinorum": ["salvia divinorum"], cocaine: ["cocaine crack", "crack cocaine"] };
  const FILL = new Set("and or the of a drug drugs facts about information info".split(" "));
  const by = {}, used = new Set();
  const add = (key, names) => {
    names = [...new Set(names.map(flat).filter(n => n.length >= 3 && !WEAK.has(n)))]; if (!names.length) return;
    const isMain = seg => !!seg && (names.includes(seg) || names.some(a => names.some(b => a !== b && seg === a + b)) ||
      (names.some(n => seg === n || seg.startsWith(n + " ") || seg.endsWith(" " + n)) && seg.split(" ").every(w => FILL.has(w) || names.some(n => n.split(" ").includes(w)))));
    const has = s => names.some(n => (" " + s + " ").includes(" " + n + " "));
    const mains = {}, topics = [];
    for (const pg of pages) { if (isMain(pg.seg)) { if (!mains[pg.id] || pg.u.length < mains[pg.id].u.length) mains[pg.id] = pg; } else if (pg.t && has(pg.way)) topics.push(pg); }
    const order = (a, b) => (meta[a.id].tier || 9) - (meta[b.id].tier || 9) || meta[a.id].n - meta[b.id].n;
    const rows = Object.values(mains).sort(order).map(pg => [pg.id, pg.u, "", 1]).concat(topics.sort(order).slice(0, 30).map(pg => [pg.id, pg.u, pg.t, 0]));
    if (rows.length) { by[key] = rows; rows.forEach(r => used.add(r[0])); } };
  for (const s of site("substances.json")) add(s.slug, [s.slug.replace(/-/g, " ")].concat(String(s.name).split(/[()\/,;]| and /), site("aliases.json")[s.slug] || [], MORE[s.slug] || []));
  for (const [k, name] of Object.entries(startedPages)) add("new:" + k, [String(name).replace(/\s*\(.*\)$/, ""), k.replace(/-/g, " ")].concat(((AUTO_SHELL[k] || {}).science || []).map(x => x.name)));
  const src = {}; used.forEach(id => { const m = meta[id]; src[id] = [m.name || (m.site && !/^(?:Government of|GOV\.)/i.test(m.site) ? m.site : m.author), m.country === "international" ? "" : m.country || ""]; });
  const n = Object.keys(by).length; if (n) console.log("official pages: " + n + " drugs and started pages have pages of " + Object.keys(src).length + " official bodies to link to (" + Object.values(by).reduce((a, r) => a + r.length, 0) + " pages)");
  return n ? { made: idx.made || "", src, by } : null;
})();
const AUTO_OBJ = Object.fromEntries(AUTO_SHOWN.map(a => [a.id, Object.assign({ q: a.q, short: a.short, but: a.but, how: a.how, howq: a.howq.some(Boolean) ? a.howq : undefined, refs: a.refs, from: a.from, made: a.made, complete: a.complete, wanted: a.wanted, drugs: a.drugs, page: a.page }, a.risk ? { risk: a.risk } : {}, a.kind ? { kind: a.kind, first: a.first, rows: a.rows } : {})]));
const data2 = data + "\nconst OFFICIAL = " + JSON.stringify(OFFICIAL) + ";\nconst AUTO = " + JSON.stringify(AUTO_OBJ) +
  ";\nconst AUTO_STATE = " + JSON.stringify(AUTO_STATE) + ";\nconst AUTO_PAGES = " + JSON.stringify(startedPages) + ";\nconst AUTO_SHELL = " + JSON.stringify(AUTO_SHELL) + ";\nconst AUTO_PICS = " + JSON.stringify(AUTO_PICS) + ";\nconst AUTO_FORMS = " + JSON.stringify(AUTO_FORMS) + ";\nconst AUTO_NAMES = " + JSON.stringify(AUTO_NAMES) + ";\nconst AUTO_LOOP = " + JSON.stringify(AUTO_LOOP) + ";\nconst SITE_BUILD = " + JSON.stringify(SITE_BUILD) + ";\nconst SITE_VERSION = " + JSON.stringify(VERSION.site) + ";\nconst PROTOCOL_VERSION = " + JSON.stringify(VERSION.protocol) + ";";
const js = [data2, src("app.core.js"), src("app.simple.js"), src("app.views.js"), src("app.insight.js")].join("\n\n");
// Refuse to build a page whose script does not parse (a syntax error would blank the site at runtime).
try { new Function(js); } catch (e) { console.error("SYNTAX ERROR in the page script: " + e.message); process.exit(1); }
// (2.15) Old phones (Safari before 16.4) cannot read a look-behind in a pattern, and one written as a literal stops the whole page: refuse
// one anywhere but in insNb, which asks the browser first (site/src/app.insight.js).
{ const bad = [];
  ["app.core.js", "app.simple.js", "app.views.js", "app.insight.js"].forEach(f => src(f).split("\n").forEach((l, i) => { if (/\(\?<[!=]/.test(l) && !/^const INS_LB = |^function insNb\(/.test(l)) bad.push(f + ":" + (i + 1)); }));
  if (bad.length) { console.error("A LOOK-BEHIND in the page script (old phones cannot read it; use insNb): " + bad.join(", ")); process.exit(1); } }
// The three files share one scope, so a function declared twice silently replaces the first one everywhere: refuse it.
{ const seen = {}, dup = [];
  [["app.core.js", src("app.core.js")], ["app.simple.js", src("app.simple.js")], ["app.views.js", src("app.views.js")], ["app.insight.js", src("app.insight.js")]].forEach(([f, t]) => {
    for (const m of t.matchAll(/^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=/gm)) { const n = m[1] || m[2]; if (seen[n]) dup.push(n + " (" + seen[n] + ", " + f + ")"); else seen[n] = f; } });
  if (dup.length) { console.error("DUPLICATE top-level names in the page script: " + dup.join("; ")); process.exit(1); } }
const BUILD_DATE = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "Europe/Athens" });
const BUILD_DATE_LONG = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Athens" });
let html = src("index.template.html").replace("/*__CSS__*/", () => src("styles.css")).replace("/*__JS__*/", () => js).replace('<span id="build-date">16 Oct 2026</span>', () => '<span id="build-date">' + BUILD_DATE + "</span>")
  .replace(/\{\{SITE_VERSION\}\}/g, () => VERSION.site).replace(/\{\{PROTOCOL_VERSION\}\}/g, () => VERSION.protocol).replace(/\{\{BUILD_DATE_LONG\}\}/g, () => BUILD_DATE_LONG);
if (/\{\{[A-Z_]+\}\}/.test(html)) console.error("WARNING: unreplaced {{…}} placeholder in the template");
fs.mkdirSync(path.join(__dirname, "dist"), { recursive: true });
fs.writeFileSync(path.join(__dirname, "dist", "index.html"), html);
// (2.23) What the system's own state file is made from (scripts/auto/live.py; docs/AUTOMATION.md, decision 34): every answer written by the system
// that this build shows, in the very form the page holds it (it passed the build's own look, above: the last gate), and the word for what the system
// has done with each listed question. A run of the system reads this file right after it has written an answer, so that a reader who is waiting
// for that answer is shown it at once, before the site's next publishing. It is not a part of the published site (site/build_public.py copies
// folders it names, and this file is in none).
fs.writeFileSync(path.join(__dirname, "dist", "live-src.json"), JSON.stringify({ built: SITE_BUILD, site: VERSION.site, auto: AUTO_OBJ, state: AUTO_STATE }));
// the photo copies are published next to the page as supporting files (dist/img/<id>-m.webp, -t.webp)
const photoDir = path.join(__dirname, "photos"), imgDir = path.join(__dirname, "dist", "img");
{ const dataDir = path.join(__dirname, "dist", "data"); fs.mkdirSync(dataDir, { recursive: true });
  for (const f of fs.readdirSync(dataDir)) if (/^cards-.*\.json$/.test(f)) fs.unlinkSync(path.join(dataDir, f));
  const bySub = {}; for (const [id, c] of Object.entries(cards)) (bySub[c.substance || "other"] = bySub[c.substance || "other"] || {})[id] = c;
  for (const [sub, cs] of Object.entries(bySub)) fs.writeFileSync(path.join(dataDir, "cards-" + sub + ".json"), JSON.stringify(cs));
  console.log("wrote", Object.keys(bySub).length, "card files to dist/data:", Object.entries(bySub).map(([k, v]) => k + " " + Object.keys(v).length).join(", "));
  // the parts fetched when a view needs them (speed, above): each substance's file, every reference in full, the official figures
  for (const f of fs.readdirSync(dataDir)) if (/^full-.*\.json$/.test(f)) fs.unlinkSync(path.join(dataDir, f));
  for (const [sub, d] of Object.entries(full)) fs.writeFileSync(path.join(dataDir, "full-" + sub + ".json"), JSON.stringify(d));
  fs.writeFileSync(path.join(dataDir, "refs.json"), JSON.stringify(Object.fromEntries(refs.map(r => [r.id, r]))));
  fs.writeFileSync(path.join(dataDir, "figures.json"), JSON.stringify(epiRows));
  fs.writeFileSync(path.join(dataDir, "decisions.json"), JSON.stringify(site("decisions.json")));
  fs.writeFileSync(path.join(dataDir, "build.json"), JSON.stringify({ build: SITE_BUILD, site: VERSION.site }));
  /* Insight (site 2.2.0, 14 November 2026): the search that understands a question, on the reader's own phone. The model
     and its runtime (site/insight/vendor: the model named in site/insight/model.json and ONNX Runtime Web, unmodified;
     where they came from and their hashes: scripts/insight/MODELS.md) are published next to the page in dist/insight/,
     fetched only when someone uses the search box; every answer's wordings, made into vectors by the same model, are in
     dist/data/insight.json (scripts/insight/build_index.py). */
  { const vend = path.join(__dirname, "insight", "vendor"), out = path.join(__dirname, "dist", "insight");
    // 2.3: the model's file name is written in one place (site/insight/model.json); every licence and notice in the folder travels with the files
    const model = JSON.parse(fs.readFileSync(path.join(__dirname, "insight", "model.json"), "utf8")).file;
    const runtime = ["ort.wasm.min.js", "ort-wasm-simd-threaded.mjs", "ort-wasm-simd-threaded.wasm", model, "vocab.txt"];
    const files = runtime.concat(fs.existsSync(vend) ? fs.readdirSync(vend).filter(f => /^(LICENSE|NOTICE)/.test(f)).sort() : []);
    if (fs.existsSync(out)) fs.rmSync(out, { recursive: true });
    if (runtime.every(f => fs.existsSync(path.join(vend, f)))) {
      fs.mkdirSync(out, { recursive: true }); files.forEach(f => fs.copyFileSync(path.join(vend, f), path.join(out, f)));
      const QS = site("questions.json"); delete QS._note;
      const pagesOf = {}, wordsOf = {};
      for (const [slug, groups] of Object.entries(QS)) (groups || []).forEach(g => (g.items || []).forEach(it => { if (!it[0]) return; (pagesOf[it[0]] = pagesOf[it[0]] || []).includes(slug) || pagesOf[it[0]].push(slug); if (it[1]) (wordsOf[it[0]] = wordsOf[it[0]] || []).push(it[1]); }));
      const byId = Object.fromEntries(shownClaims.map(c => [c.id, c]));
      // 2.3: the drugs each answer is about (a best match must be about the drug a question names; next questions keep to the
      // same drug): the drug pages that ask it, the drugs a mixing answer is shown for, the drugs whose tests a test-kit answer covers
      const drugSlugs = new Set(site("substances.json").map(s => s.slug)), aboutOf = {}, isAbout = (id, slug) => { if (drugSlugs.has(slug)) (aboutOf[id] = aboutOf[id] || new Set()).add(slug); };
      const fileOr = (f, d) => fs.existsSync(path.join(ROOT, "data/site", f)) ? site(f) : d;
      Object.entries(pagesOf).forEach(([id, ps]) => ps.forEach(p => isAbout(id, p)));
      Object.entries(fileOr("mix-drugs.json", {})).forEach(([id, ps]) => { if (Array.isArray(ps)) ps.forEach(p => isAbout(id, p)); });
      Object.entries(fileOr("kits-for.json", {})).forEach(([slug, ids]) => { if (Array.isArray(ids)) ids.forEach(id => isAbout(id, slug)); });
      const answers = Object.entries((simpleShown || {}).claims || {}).filter(([id]) => byId[id]).map(([id, sp]) => ({ id, substance: byId[id].substance, section: byId[id].section,
        pages: pagesOf[id] || [byId[id].substance], about: [...(aboutOf[id] || (drugSlugs.has(byId[id].substance) ? [byId[id].substance] : []))].sort(),
        wordings: [...new Set((sp.q ? [sp.q] : []).concat(wordsOf[id] || []))], short: sp.short }));
      // 2.6: the machine lane's answers are found by the search box as every answer is: by their question and its other wordings
      AUTO_SHOWN.forEach(a => answers.push({ id: a.id, substance: a.page, section: 0, pages: [a.page], about: a.drugs.slice().sort(), wordings: [...new Set([a.q].concat(a.ways))], short: a.short }));
      const input = path.join(__dirname, "insight", ".cache", "index-input.json"), nextFile = path.join(__dirname, "insight", ".cache", "next.json");
      // 2.5: the questions not answered yet (data/site/wanted.json), for the page's second look when no answer fits
      const wanted = (fileOr("wanted.json", { items: [] }).items || []).map(w => ({ id: w.id, q: w.q, ways: w.ways || [], drugs: w.drugs || [] }));
      fs.mkdirSync(path.dirname(input), { recursive: true }); fs.writeFileSync(input, JSON.stringify({ answers, wanted }));
      if (fs.existsSync(nextFile)) fs.unlinkSync(nextFile);
      const r = require("child_process").spawnSync("python3", ["-I", path.join(ROOT, "scripts", "insight", "build_index.py"), input, path.join(dataDir, "insight.json"), nextFile], { stdio: ["ignore", "inherit", "inherit"], env: Object.assign({}, process.env, { PK_NODE: process.execPath }) });
      if (r.status !== 0) { console.error("WARNING: Insight's index was not built (scripts/insight/build_index.py failed): the search box answers by words only"); if (fs.existsSync(path.join(dataDir, "insight.json"))) fs.unlinkSync(path.join(dataDir, "insight.json")); }
      // 2.3: what the page itself is told, at the head of its script: the model's file name (so its download starts at once;
      // the index names its model too, and the page goes by the index if the two ever differ), how many MB the reader's
      // browser fetches once, and each answer's next questions (the nearest by meaning, never from another drug), so that
      // "Read next" and the answer sheet's "People also ask" need none of Insight's files
      else if (fs.existsSync(nextFile)) {
        const pageFile = path.join(__dirname, "dist", "index.html"), mark = "\nconst SITE_VERSION = ", page = fs.readFileSync(pageFile, "utf8");
        const bytes = runtime.reduce((a, f) => a + fs.statSync(path.join(vend, f)).size, fs.statSync(path.join(dataDir, "insight.json")).size);
        // 2.5: the questions on our list, as the index kept them (an item the site answers by now is left out there): [id, question]
        const wl = JSON.parse(fs.readFileSync(path.join(dataDir, "insight.json"), "utf8")).wanted, listed = wl ? wl.ids.map((id, i) => [id, wl.q[i]]) : [];
        // (2.6: a machine-lane answer is never offered as a next question of a checked answer; it keeps its own next questions)
        // (2.21.2: but under another answer by the system it is: on a page the system started, kanna's two answers offered nothing, each being the other's only neighbour)
        const nx = JSON.parse(fs.readFileSync(nextFile, "utf8")); nx.next = nx.next.map((l, i) => (l || []).filter(j => !/^au_/.test(nx.ids[j]) || /^au_/.test(nx.ids[i])));
        const told = "\nconst INS_MODEL = " + JSON.stringify(model) + ";\nconst INS_MB = " + Math.round(bytes / 1e6) + ";\nconst INS_NEXT = " + JSON.stringify(nx) + ";\nconst WANTED = " + JSON.stringify(listed) + ";";
        if (page.split(mark).length === 2) fs.writeFileSync(pageFile, page.replace(mark, () => told + mark));
        else console.error("WARNING: the page's script has no place for what Insight tells it (const SITE_VERSION not found once): the search box answers by words only, and Read next falls back to the next questions of the topic");
      }
    } else console.error("WARNING: site/insight/vendor is incomplete: Insight is left out and the search box answers by words only"); }
  const kb = f => (fs.statSync(path.join(dataDir, f)).size / 1024).toFixed(0) + " KB";
  console.log("wrote", Object.keys(full).length, "substance files to dist/data (largest " + Object.keys(full).map(s => "full-" + s + ".json").sort((a, b) => fs.statSync(path.join(dataDir, b)).size - fs.statSync(path.join(dataDir, a)).size).slice(0, 3).map(f => f + " " + kb(f)).join(", ") + "), refs.json " + kb("refs.json") + ", figures.json " + kb("figures.json")); }
// (2.12) the pictures the system found for the pages it started: only the ones a page shows are published (dist/img/auto/)
{ const from = path.join(__dirname, "photos-auto"), to = path.join(__dirname, "dist", "img", "auto"); if (fs.existsSync(to)) fs.rmSync(to, { recursive: true, force: true });
  const files = Object.values(AUTO_PICS).flat().concat(Object.values(AUTO_FORMS).flatMap(x => Object.values(x))).flatMap(p => [p.file + "-m.webp", p.file + "-t.webp"]);
  if (files.length) { fs.mkdirSync(to, { recursive: true }); files.forEach(f => fs.copyFileSync(path.join(from, f), path.join(to, f))); console.log("copied", files.length, "files of pictures the system found to dist/img/auto"); } }
if (fs.existsSync(photoDir)) { fs.mkdirSync(imgDir, { recursive: true }); const n = fs.readdirSync(photoDir).filter(f => f.endsWith(".webp")).map(f => fs.copyFileSync(path.join(photoDir, f), path.join(imgDir, f))).length; console.log("copied", n, "photo files to dist/img"); }
console.log("built dist/index.html", (html.length / 1024).toFixed(1) + " KB;", refs.length, "refs,", Object.keys(cards).length, "cards,", claims.length, "claims; evidence maps:", Object.keys(maps).length);
