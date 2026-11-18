/* Pharmakon's one small piece of server (site 2.4, 15 November 2026): the question a reader chooses to send with
   "Ask us to check it", and, since site 2.17 (18 November 2026), the question the page sends by itself when the site has
   no answer to it (the senior author, 17 November 2026, 23:38: "it should send the question immediately in every instance
   and the user should be notified"; the page tells the reader as it happens, and the reader can switch it off).
   Cloudflare Pages runs this file for /api/* only (_routes.json beside it); every other address
   of the site is a fixed file, served as before, and never reaches this code.

   Kept, in the Workers KV store bound as QUESTIONS: the question's words (at most 200 characters), the drug pages it was
   asked on, the site version, the first and last day it was asked, and how many times (in all, and on that last day). Not kept and not logged: the
   address a request came from, the browser, any cookie (the site sets none). A question that holds a link, an email
   address or a long run of digits is refused, so that nobody's contact details are stored by mistake.

   GET  /api/ask            -> {"ok": true}  when the store is bound; {"ok": false} when it is not (the page asks once,
                               to know whether it can send; without the store it falls back to its email form). With it,
                               "find": true: this server can look up published research (POST /api/find, below)
   POST /api/ask {q, d, v}  -> {"ok": true}  the question is kept (or counted again when it was already there);
                               503 without the store
   POST /api/ask {q, d, v, a: 1} -> the same for a question the page sent by itself. It is kept apart (keys "aq:"), for
                               180 days, and its words are never written into the public repository: the scout reads such
                               questions in a run's own memory and keeps only OUR wording of what was asked
                               (scripts/auto/fetch_questions.py --auto; scripts/auto/ask.py). When someone has already
                               chosen to send the very same question, it is counted there instead. These stop at 250 a
                               day, so that they can never crowd out a question someone chose to send.
   POST /api/want {id}      -> {"ok": true}  one more person asked a question that is on the site's public list of
                               questions not answered yet (site 2.5). Only the list item's number arrives ("w_0041"):
                               never the person's words. Kept: the number, a count, the last day.
   POST /api/find {names, words} -> {"ok": true, "papers": [...]}  (site 2.16, 17 November 2026; the senior author: "answers take
                               too long to get responses and people are used to get responses instantly ... our ai should be able to
                               find answers almost instantly"). Published research on a drug, looked up at once in Europe PMC, the
                               open index of medical research (https://europepmc.org; its public search service, no key). What
                               arrives: the names of a drug (up to 6) and plain key words (up to 6), chosen on the reader's device;
                               never the reader's sentence. What goes out to Europe PMC: those names and words, from this server (the
                               reader's address is not passed on). What comes back to the page: for up to 6 papers the title, the
                               authors, the journal, the year, the kind of paper, whether it is free to read, and its link. Nothing is
                               kept or logged here; Cloudflare keeps Europe PMC's reply for a day so the same search is not asked
                               twice. No model reads anything: these are records of papers, shown as "not read by us yet". Words about
                               dying, overdose, amounts, pregnancy or children are not looked up (such questions wait for a person).
   POST /api/answer {q, names, words} -> what the papers say, within seconds, where the Workers AI binding (AI) exists: for up to
                               three of those papers, the paper's own words on the question (at most 15, from its summary) with
                               its kind, year and link; a model chooses, this code cuts and checks (sites 2.18 and 2.19; its full
                               account stands above the code, below).
   An address with a slash at its end ("/api/ask/") is taken as the same address. */
// The free store takes 1,000 writes a day and a question kept or counted costs two, so at most 400 are taken in a day.
// One question is counted at most 20 times a day: nobody is known here, so this is what keeps one sender from making a
// question look much asked (the scout orders its list by these counts).
const MAX_Q = 200, MAX_A_DAY = 400, MAX_SAME_A_DAY = 20;
// Counts for the list (/api/want) share the day's 400 and stop at 300, so that they can never crowd out a question
// someone chose to send; one list item is counted at most 60 times a day.
const MAX_WANT_UNTIL = 300, MAX_WANT_SAME_A_DAY = 60;
// A question the page sent by itself (site 2.17): room for 250 of the day's 400, kept 180 days
const MAX_AUTO_UNTIL = 250, AUTO_KEPT = 180 * 86400;
const json = (o, status) => new Response(JSON.stringify(o), { status: status || 200, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const clean = s => String(s == null ? "" : s).normalize("NFKC").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim();
// the characters a record writes as codes ("p &lt; 0.05"): read back after the tags are out
const unEnt = s => String(s).replace(/&(?:#(\d{1,6})|#x([0-9a-f]{1,5})|(amp|lt|gt|quot|apos|nbsp));/gi, (m, d, h, n) => { try { return d ? String.fromCodePoint(Number(d)) : h ? String.fromCodePoint(parseInt(h, 16)) : ({ amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " })[n.toLowerCase()]; } catch (e) { return " "; } });
async function keyOf(text) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, "0")).join("").slice(0, 20);
}
export function readQuestion(body) {
  const q = clean(body && body.q).slice(0, MAX_Q);
  const d = clean(body && body.d).toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 40), v = clean(body && body.v).replace(/[^0-9.]/g, "").slice(0, 12);
  if (q.length < 8 || q.split(" ").length < 2 || !/\p{L}{2}/u.test(q)) return { error: "too short" };
  if (/https?:\/\/|www\.|[^\s@]+@[^\s@]+\.[a-z]{2,}|<\s*[a-z!/]/i.test(q)) return { error: "no links or addresses" };
  if (/\d[\d\s().+-]{7,}\d/.test(q)) return { error: "no long numbers" };
  return { q, d, v, a: !!(body && (body.a === 1 || body.a === true)) };
}
// ---- published research, looked up at once (POST /api/find)
const EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search";
export const FIND_HELD = /\b(pregnan\w*|breast-?feed\w*|child|children|kids?|bab(y|ies)|infants?|teen\w*|minors?|suicid\w*|kill\w*|die[sd]?|dying|deaths?|dead|deadly|overdos\w*|lethal|fatal\w*|dos(e|es|age|ing)|mg|milligrams?|grams?|micrograms?)\b/i;
const findName = s => { s = clean(s).toLowerCase(); return /^[a-z0-9][a-z0-9 ,.'+()\-]{1,58}[a-z0-9)]$/.test(s) && !/["\\:]/.test(s) ? s : ""; };
const findWord = s => { s = clean(s).toLowerCase(); return /^[a-z]{3,24}$/.test(s) ? s : ""; };
// (2.19) a key word may come with the word papers use for it, as one entry: "appetite|hungry". The two are one thing asked for, in two ways.
export function readFind(body) {
  const uniq = a => [...new Set(a.filter(Boolean))];
  const names = uniq((Array.isArray(body && body.names) ? body.names : []).slice(0, 12).map(findName)).slice(0, 6);
  const groups = (Array.isArray(body && body.words) ? body.words : []).slice(0, 12).map(e => uniq(String(e == null ? "" : e).split("|").slice(0, 3).map(findWord)).filter(w => !names.includes(w))).filter(g => g.length).slice(0, 6);
  const words = uniq(groups.flat());
  if (!names.length) return { error: "no name" };
  return { names, words, groups, held: names.concat(words).some(t => FIND_HELD.test(t)) };
}
/* What Europe PMC is asked (its own search words). groups: the question's key words, each an array of the ways it is said (a plain list of words is
   taken as one way each). (2.19, after the first trial with real questions) Every key word must stand in a paper's title or summary, not any one of
   them: "does modafinil improve memory" asked for papers with "improve" OR "memory" and got reviews on sleepiness and stroke. A key word is asked for
   in its one and its many ("migraines", "migraine"): the search takes a quoted word as it is written. */
const FIND_SPELL = "colour color|behaviour behavior|tumour tumor|flavour flavor|odour odor|labour labor|vapour vapor|anaemia anemia|anaesthesia anesthesia|anaesthetic anesthetic|haemorrhage hemorrhage|oedema edema|diarrhoea diarrhea|oestrogen estrogen|ageing aging|centre center|fibre fiber|analogue analog|programme program|grey gray|sulphate sulfate|leukaemia leukemia".split("|").map(p => p.split(" "));
// a word as papers may write it: its one and its many ("migraines", "migraine") and its other spelling ("colour", "color"; "-ise", "-ize")
export function findForms(w) {
  const out = new Set([w]); if (/ies$/.test(w) && w.length > 5) out.add(w.slice(0, -3) + "y"); else if (/[^su]s$/.test(w) && w.length > 4) out.add(w.slice(0, -1));
  for (const f of [...out]) { for (const [a, b] of FIND_SPELL) { if (f === a) out.add(b); else if (f === b) out.add(a); else if (f === a + "s") out.add(b + "s"); else if (f === b + "s") out.add(a + "s"); }
    const z = f.replace(/is(e|ed|es|ing|ation|ations)$/, "iz$1"), s = f.replace(/iz(e|ed|es|ing|ation|ations)$/, "is$1"); if (z !== f) out.add(z); if (s !== f) out.add(s); }
  return [...out];
}
export function findQueries(names, groups) {
  const field = (ts, titleOnly) => "(" + ts.map(t => titleOnly ? `TITLE:"${t}"` : `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")";
  const gs = (groups || []).map(g => [...new Set((Array.isArray(g) ? g : [g]).flatMap(findForms))]).filter(g => g.length);
  const tail = ' AND LANG:eng NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"';
  const rev = ' AND (PUB_TYPE:"review" OR PUB_TYPE:"systematic review" OR PUB_TYPE:"meta-analysis")';
  const strict = field(names) + gs.map(g => " AND " + field(g)).join(""), loose = gs.length > 1 ? field(names) + " AND " + field([...new Set(gs.flat())]) : "";
  // reviews on the very question; any paper on it; (with two key words or more) reviews and papers that hold any one of them; reviews of the drug itself
  return { strictRev: strict + rev + tail, strict: strict + tail, looseRev: loose ? loose + rev + tail : "", loose: loose ? loose + tail : "", nameRev: field(names, true) + rev + tail };
}
/* The papers on a drug and a question's key words, the best first: the most cited reviews on the very question and the papers Europe PMC ranks first
   for it, asked together; wider only where that found too little. core: with their summaries (for /api/answer), else the plain records. */
async function findPapers(env, names, groups, core, most) {
  const get = env.FETCH || fetch, read = core ? iaPaper : findPaper;
  const ask = async (q, cited) => {
    if (!q) return [];
    const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 7000);
    try {
      const res = await get(EPMC + "?query=" + encodeURIComponent(q) + "&format=json&resultType=" + (core ? "core" : "lite") + "&pageSize=" + (core ? 6 : 8) + (cited ? "&sort=CITED%20desc" : ""), { headers: { accept: "application/json", "user-agent": "pharmakon.world (contact@pharmakon.world)" }, signal: ctl.signal, cf: { cacheTtl: 86400, cacheEverything: true } });
      if (!res.ok) return cited ? ask(q, false) : [];   // (should the service not take the order asked for, it is asked once more without it)
      const d = await res.json(); return ((d && d.resultList && d.resultList.result) || []).map(read).filter(Boolean);
    } catch (e) { return []; } finally { clearTimeout(timer); }
  };
  const Q = findQueries(names, groups), [a, b] = await Promise.all([ask(Q.strictRev, true), ask(Q.strict, false)]);
  const seen = new Set(), out = [], add = list => { for (const p of list) { const k = p.doi || p.pmid; if (!seen.has(k)) { seen.add(k); out.push(p); } } };
  add(a.slice(0, 2)); add(b); add(a.slice(2));                                 // the two most cited reviews first, then the papers ranked first, then the other reviews
  if (out.length < 3 && Q.looseRev) add(await ask(Q.looseRev, true));
  if (out.length < 3 && Q.loose) add(await ask(Q.loose, false));
  if (out.length < 2) add(await ask(Q.nameRev, true));
  return out.slice(0, most);
}
export function findPaper(r) {
  if (!r || typeof r !== "object") return null;
  const t = clean(unEnt(String(r.title || "").replace(/<[^>]+>/g, ""))).replace(/\.$/, "").slice(0, 300); if (t.length < 8) return null;
  const types = String(r.pubType || (r.pubTypeList && r.pubTypeList.pubType ? [].concat(r.pubTypeList.pubType).join("; ") : "")).toLowerCase();
  const doi = /^10\.\d{4,9}\/[^\s"<>]{1,200}$/.test(String(r.doi || "")) ? String(r.doi) : "", pmid = /^\d{1,9}$/.test(String(r.pmid || "")) ? String(r.pmid) : "";
  if (!doi && !pmid) return null;
  return { t, a: clean(r.authorString || "").slice(0, 120), j: clean(r.journalTitle || (r.journalInfo && r.journalInfo.journal && r.journalInfo.journal.title) || "").slice(0, 120), y: /^(19|20)\d\d$/.test(String(r.pubYear || "")) ? String(r.pubYear) : "",
    doi, pmid, oa: r.isOpenAccess === "Y", kind: /meta-analysis|systematic review/.test(types) ? "Review of studies" : /review/.test(types) ? "Review" : /randomized controlled trial|clinical trial/.test(types) ? "Trial" : /case reports/.test(types) ? "Case report" : "Study" };
}
async function find(request, url, env) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  const origin = request.headers.get("origin");
  if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
  let body = null;
  try { const t = await request.text(); if (t.length > 2000) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const r = readFind(body); if (r.error) return json({ ok: false, error: r.error }, 422);
  if (r.held) return json({ ok: true, held: true, papers: [] });
  try { return json({ ok: true, papers: await findPapers(env, r.names, r.groups, false, 6) }); }
  catch (e) { return json({ ok: false, error: "search" }, 502); }
}
// ---- what the papers say, within seconds (POST /api/answer; sites 2.18 and 2.19, 18 November 2026; docs/AUTOMATION.md, decision 31)
/* The senior author, 17 November 2026: "people are used to get responses instantly. We have to make an ai which is able to do that for
   questions it does not know"; and, of the list of papers that 2.16 shows: "we have to make instant as good as getting answers from a very
   good claude api. whatever it takes."
   What it is. For a question about a drug that the site has no answer to, this server reads the SUMMARIES of the papers Europe PMC finds
   (their abstracts; never a paper's full text) with one language model run by Cloudflare itself (Workers AI, bound to this site as AI: the
   only place a reader's words go besides this server). The model CHOOSES: up to three papers that bear on the question and, in each, the
   sentence that carries what the paper found. What the reader is shown is the PAPER'S OWN WORDS from that sentence (at most 15 in a
   row, chosen by this code, never by the model), with the paper's kind, year, journal and link, and "in animals or cells, not in
   people" where the sentence or the whole summary is about those (or that the summary covers such work too, where it covers both and
   the sentence does not say). It is shown under its own label and is never an answer of ours: nothing of it enters the site's data,
   and the question still goes to the lane, which reads the papers themselves and passes its checks.
   Why the papers' words and not the model's (site 2.19). Version 1 (site 2.18) let the model write a plain sentence for each finding,
   kept only when its quoted words stood in the summary and its numbers and strong words too. On 18 November it was tried with the real
   model on 18 of the editor's questions before any reader met it (data/auto/instant/trial-20261118T0005-0001.json): of 19 sentences
   that passed, the editor found about six that said more than their paper ("may ameliorate laboratory stress/anxiety responding"
   became "ameliorates anxiety"; "GHB/GBL" became "GHB and GBL are used together"; a review of microdosing became "LSD caused no lasting
   personality benefits"). That is the rate the lane's exam found for free models (decision 23), and it is not one this site shows. A
   paper's own words cannot say more than the paper. So the model still writes its plain sentence, the code checks it far more strictly
   (below: every word of it must stand in the very sentence it rests on), and it is KEPT for the editors with the verdict, but it is
   not shown (IA.plain is false) until an exam of such sentences says it may be.
   What the code decides, not the model. A finding is thrown away unless:
     1. its paper is one of those given, and the words the model points to stand in that paper's summary, character for character;
     2. the paper bears on the question, where the question has key words: one of them, or a word papers use for it, stands in the
        sentence pointed to, in the paper's title or elsewhere in its summary (which of the three is kept, for the editors);
     3. its sentence does not speak of animals or cells and of people at once (a part of it could then be read as the other);
     4. there are 15 words of that sentence, in a row and holding the words pointed to, that leave out no word the sentence turns on
        (iaWindow: before them a no, a question or an aim, "is claimed to", or a "may" they do not hold themselves; after them a no, a
        question or a "but": "there was no evidence that | the extract reduced anxiety" is shown with its "no evidence", or not at all)
        and that hold no amount, dose or timing and nothing about dying, overdose, pregnancy or children.
   And the model's plain sentence counts as sound (kept for the exam; shown only once IA.plain is true) only if, besides: it names the
   kind of paper it rests on and no other year; every number in it is in its source sentence; it holds no advice, nothing on making an
   effect stronger, no way of taking compared with another; EVERY word of it stands in its source sentence or in the paper's title (or
   is a small word, a word for the kind of paper, or one of the drug's names); a "may" of the source is kept; a "no" is neither gained
   nor lost; and a summary about animals or cells is called that.
   Not answered here: a question about dying, overdose, amounts, pregnancy, children or suicide (FIND_HELD: these wait for a person), and a
   question research summaries cannot answer (the law, prices, drug tests).
   What it costs: Cloudflare's free allowance is 10,000 neurons a day for the whole account, shared with the machine lane. This endpoint
   stops by itself at IA.neurons a day (and IA.answers new answers); the lane stops at its own share (scripts/auto/llm.py: OUR_LIMIT).
   On Cloudflare's free plan a used-up allowance ends in an error, never in a charge. What was found for a question is kept for 30 days
   and given again for the same question (no model is asked twice).
   What is kept (key "ia:<fingerprint>"): the drug's names and key words, the papers' words shown with their papers, the model's plain
   sentences with the code's verdict on each, what was refused with the reason (never given to a reader), the model's name and the time;
   never the reader's sentence. So that the editors can read everything the system chose and wrote this way. And the day's count
   ("ian:<day>": neurons and answers). Nothing is logged. */
export const IA = { v: 2, writer: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", price: [26668, 204805], neurons: 3500, answers: 60, kept: 30 * 86400, papers: 5, chars: 1500, room: 420, plain: false };
const IA_NOT_RESEARCH = /\b(legal\w*|illegal\w*|law|laws|lawful|police|arrest\w*|prison|jail|court|customs|border|airport|price|prices|cost|costs|cheap\w*|buy|buying|bought|order\w*|dealers?|vendors?|drug tests?|test positive|urine|piss test|hair test|workplace test|screening test)\b/i;
const IA_SYS = `You help Pharmakon, a free drug encyclopedia, show a reader at once what published research says about their question. You get the question and the SUMMARIES (abstracts) of a few papers, numbered. Nobody has read the full papers. Use only the summaries: what you know yourself does not count.

Pick 1 to 3 summaries that bear most directly on the question, the most direct first. From each, pick the ONE sentence that carries what the paper found or concluded about the question: a sentence of results or conclusions, not one of background and not one that only says what the paper set out to do. For each give:
"n": the summary's number.
"quote": 6 to 15 words copied exactly, character for character, from that one sentence: the words that carry the finding. Keep "may", "might", "not", "no" when they belong to it.
"text": the same finding as ONE plain sentence of at most 30 words. Begin with the kind of paper and its year exactly as given in the brackets: "A 2021 review says ...", "A 2013 trial found ...", "A 2019 study found ...". Use only words that stand in that sentence or in the paper's title, besides small words: you may leave words out, you may not add any. Keep "may", "might", "suggests", "not", "no" wherever the sentence has them. When the summary is about animals or cells, say so.

Do not pick a sentence about an amount, a dose, or about dying. No advice, never "you". If no summary bears on the question, answer {"enough": false, "findings": []}.

Answer with JSON only: {"enough": true, "findings": [{"n": 1, "quote": "...", "text": "..."}]}`;
const IA_SCHEMA = { type: "object", properties: { enough: { type: "boolean" }, findings: { type: "array", items: { type: "object", properties: { n: { type: "integer" }, quote: { type: "string" }, text: { type: "string" } }, required: ["n", "quote", "text"] } } }, required: ["enough", "findings"] };
const iaFlat = s => clean(String(s == null ? "" : s).replace(/<[^>]+>/g, " ")).toLowerCase().replace(/[‘’‚′`]/g, "'").replace(/[“”„″]/g, '"').replace(/[‐-―−]/g, "-").replace(/\s+/g, " ");
const iaWords = s => iaFlat(s).match(/[a-z0-9][a-z0-9'-]*/g) || [];
// a paper with a summary long enough to say something: what findPaper keeps, and the summary cut at the end of a sentence
export function iaPaper(r) {
  const p = findPaper(r); if (!p) return null;
  let ab = clean(unEnt(String((r && r.abstractText) || "").replace(/<h4[^>]*>[^<]{0,80}<\/h4>/gi, " ").replace(/<[^>]+>/g, " "))); if (ab.length < 250) return null;
  if (ab.length > IA.chars) { const cutAt = ab.lastIndexOf(". ", IA.chars); ab = ab.slice(0, cutAt > 600 ? cutAt + 1 : IA.chars); }
  return Object.assign(p, { ab });
}
const IA_KIND = { "Review of studies": /\breview\b|\bmeta-analysis\b/i, "Review": /\breview\b/i, "Trial": /\btrial\b|\bstudy\b/i, "Case report": /\bcase\b/i, "Study": /\bstudy\b|\bsurvey\b|\banalysis\b|\bexperiment\b|\bpaper\b|\breport\b/i };
const IA_AMOUNT = /\d\s?(?:mg|mcg|µg|μg|ug|g|kg|ml|iu|units?)\b|\b(?:milligrams?|micrograms?|grams?|dos(?:e|es|age|ages|ing|ed)|every \d+ (?:minutes?|hours?)|redos\w*)\b/i;   // (how often somebody uses, "daily", is not an amount: it stays)
const IA_ADVICE = /\b(?:should|shouldn't|must|ought|recommend\w*|advis\w*|try|tries|avoid\w*|safe|safely|safer|safest|safety|harmless|best|ideal|you|your|yours|yourself|we|our)\b/i;
const IA_STRONGER = /\b(?:potentiat\w*|boost\w*|stronger|strongest|intensif\w*|enhanc\w*|synerg\w*|combin\w* with|mix\w* with|together with)\b/i;
const IA_ROUTE = /\b(?:oral\w*|smok\w*|inject\w*|snort\w*|intranasal\w*|insufflat\w*|intraven\w*|sublingual\w*|rectal\w*|vap\w*|edibles?|eaten|eating|swallow\w*|chew\w*|inhal\w*)\b/i, IA_THAN = /\b(?:than|compared|versus|vs|faster|slower|quicker)\b/i;
const IA_ANIMAL = /\b(?:rats?|mice|mouse|rodents?|zebrafish|in vitro|cell lines?|cultured cells|animals?|murine|preclinical)\b/i, IA_PEOPLE = /\b(?:participants?|patients?|volunteers?|humans?|men|women|adults?|people|subjects|students|respondents|users|individuals|persons)\b/i, IA_SAYS_ANIMAL = /\b(?:rats?|mice|mouse|animals?|cells?|lab|laboratory|zebrafish|rodents?|test tube)\b/i;
const IA_NUMWORD = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety", 100: "(?:one |a )?hundred" };
const IA_HEDGE = /\b(?:may|might|could|can|suggest\w*|appear\w*|seem\w*|potential\w*|possibl\w*|preliminary|limited|likely|tend\w*|uncertain\w*|unclear|inconclusive|mixed|inconsistent)\b/i, IA_HEDGE_OUT = /\b(?:may|might|could|can|suggests?|suggested|appears?|seems?|possibly|potential\w*|preliminary|limited|likely|unclear|uncertain|inconclusive|mixed)\b/i;
const IA_NEG = /\b(?:no|not|never|without|neither|nor|none|lack\w*|fail\w*|absen\w*|cannot|n't)\b|\w+n't\b/i;
// a key word of a question, and how papers say the same thing: the beginnings of words to look for in a paper's sentence
const IA_NEAR = { addiction: ["addict", "depend", "misus", "abus", "withdraw"], addictive: ["addict", "depend", "misus", "abus", "withdraw"], depression: ["depress"], anxiety: ["anxi", "stress"], sleep: ["sleep", "insomn", "wakeful", "sedat"], appetite: ["appetit", "hunger", "hungry", "food intake", "feeding"], hungry: ["appetit", "hunger", "hungry", "food intake", "feeding"],
  memory: ["memor", "cognit", "amnes"], attention: ["attenti", "cognit", "concentrat"], concentrate: ["attenti", "cognit", "concentrat"], cognitive: ["cognit", "memor", "attenti"], pain: ["pain", "analges"], psychoactive: ["psychoactiv", "intoxic", "euphor", "hallucin", "stimul", "sedat", "psychotrop"], adverse: ["advers", "harm", "risk", "toxic", "side effect"] };
const iaNearStems = w => IA_NEAR[w] || [...new Set(findForms(w).map(f => f.length > 7 ? f.slice(0, 6) : f.length > 5 ? f.slice(0, 5) : f.length > 4 ? f.slice(0, 4) : f))];
// the small words a plain sentence may add to its source's own: words that carry no finding, the words for a kind of paper, and words that claim less
const IA_FRAME = new Set(("a an the of in on at to for from by with and or but that which who whom whose than as is are was were be been being it its their they this these those there into over under after before during while when where also both either " +
  "says said say found finds find reports reported report describes described describe suggests suggested suggest shows showed show review reviews trial trials study studies survey paper papers analysis case reports meta-analysis has have had not no may might can could").split(" "));
const iaRoot = w => { if (w.length > 4) w = w.replace(/(?:ies|ied)$/, "y").replace(/(?:ing|ed|es|s)$/, ""); return w.length > 6 ? w.slice(0, 6) : w; };
/* The model's plain sentence, against the very sentence of the summary it rests on: sound (ok) or not, and why not. src: that sentence. */
export function iaPlain(text, src, p, names) {
  const no = why => ({ t: text, ok: false, why });
  text = clean(text).replace(/^["'“]+|["'”]+$/g, ""); if (text && !/[.!?]$/.test(text)) text += ".";
  const tw = iaWords(text), all = iaFlat(p.t + ". " + src);
  if (/[<>{}\[\]\\]|https?:/i.test(text)) return no("markup or a link");
  if (tw.length < 6 || tw.length > 36) return no("too short or too long");
  if (!IA_KIND[p.kind].test(text.split(/\s+/).slice(0, 9).join(" "))) return no("it does not name its kind of paper (" + p.kind.toLowerCase() + ")");
  if ((text.match(/\b(?:19|20)\d\d\b/g) || []).some(y => y !== p.y)) return no("another year than the paper's");
  for (const num of text.match(/\d+(?:[.,]\d+)?/g) || []) { if (num === p.y) continue;
    if (!new RegExp("(?:^|[^0-9.,])" + num.replace(/[.,]/g, "[.,]") + "(?:$|[^0-9])").test(all) && !(IA_NUMWORD[num] && new RegExp("\\b" + IA_NUMWORD[num] + "\\b").test(all))) return no("a number its source sentence does not hold (" + num + ")"); }
  if (FIND_HELD.test(text)) return no("dying, overdose, amounts, pregnancy or children");
  if (IA_AMOUNT.test(text)) return no("an amount, a dose or timing");
  { const m = text.match(IA_ADVICE); if (m) return no("advice, or speaking to the reader (" + m[0].toLowerCase() + ")"); }
  if (IA_STRONGER.test(text)) return no("making an effect stronger, or mixing");
  if (IA_ROUTE.test(text) && IA_THAN.test(text)) return no("a way of taking compared with another");
  const roots = new Set((all.match(/[a-z]+/g) || []).concat((names || []).join(" ").toLowerCase().match(/[a-z]+/g) || []).map(iaRoot));
  for (const w of text.toLowerCase().match(/[a-z]+/g) || []) { if (w.length < 3 || IA_FRAME.has(w) || roots.has(iaRoot(w))) continue; return no("a word that is not in its source sentence (" + w + ")"); }
  if (IA_HEDGE.test(src) && !IA_HEDGE_OUT.test(text)) return no("its source says may, it does not");
  if (IA_NEG.test(src) !== IA_NEG.test(text)) return no("a no gained or lost");
  if (IA_ANIMAL.test(iaFlat(p.t + ". " + p.ab)) && !IA_PEOPLE.test(iaFlat(p.t + ". " + p.ab)) && !IA_SAYS_ANIMAL.test(text)) return no("a summary about animals or cells, not said");
  return { t: text, ok: true, why: "" };
}
// the sentences of a summary, each without the label some summaries set before it ("RESULTS: ...", "Conclusions: ...")
// (a sentence is not cut after "vs.", "e.g.", "et al." or a single letter: cut there, a "no" could fall into another piece than the words it governs)
const IA_ABBR = /(?:^|[\s(])(?:e\.g|i\.e|vs|et al|approx|fig|figs|dr|mr|mrs|ms|prof|no|nos|vol|ca|cf|resp|incl|st|jr|sr|inc|ltd|u\.s|u\.k|[a-z])\.$/i;
export const iaSents = ab => { const out = []; for (const p of String(ab || "").split(/(?<=[.!?])\s+(?=[A-Z0-9(\["'“])/)) { if (out.length && IA_ABBR.test(out[out.length - 1])) out[out.length - 1] += " " + p; else out.push(p); }
  return out.map(s => s.trim().replace(/^[A-Z][A-Za-z]*(?:[ /&-]+[A-Za-z]+){0,3}:\s+(?=[A-Z0-9"'“(])/, "")).filter(Boolean); };
/* Words on which a sentence turns. Left out of the words that are shown, they would let those words say more than their sentence does, or its
   opposite: "there was no evidence that | the extract reduced anxiety", "we examined whether | ...", "is claimed to | ...", "... | but this was not
   significant", "these results suggest that | ..." (2.19). */
const IA_T_NEG = /^(?:no|not|never|without|neither|nor|none|lack\w*|fail\w*|absen\w*|cannot|unable|unlikely|\w+n't|non-?[a-z-]+|insignificant\w*|ineffective\w*|insufficient\w*|unsupported|unproven|unfounded|unchanged|unaffected|little|few|weak|rarely|seldom|hardly|scarcely|only|solely|contrary|refut\w*|disprov\w*|contradict\w*|doubt\w*|myths?|false|falsely|incorrect\w*|misconception\w*)$/, IA_T_ASK = /^(?:whether|if|unclear|unknown|uncertain|hypothes\w*|aim\w*|objectives?|purpose|investigat\w*|examin\w*|assess\w*|evaluat\w*|explor\w*|determin\w*|tested|testing|questions?|debat\w*|controvers\w*|remains?|remained)$/;
const IA_T_SAID = /^(?:claim\w*|believ\w*|thought|purport\w*|alleg\w*|anecdot\w*|reputed\w*|tradition\w*|market\w*|advertis\w*|promot\w*|said|supposed\w*|so-called|popular\w*|folk|rumou?r\w*)$/, IA_T_MAY = /^(?:may|might|could|suggest\w*|appear\w*|seem\w*|possibl\w*|potential\w*|preliminary|limited|likely|tend\w*|inconclusive|mixed|inconsistent)$/;
const IA_T_BUT = /^(?:but|however|although|though|except|unless|despite|nevertheless|nonetheless)$/;
/* Which words of a sentence are shown: at most 15 in a row, holding the words pointed to (toks[a..b]). Of all such runs, the one that reads best
   (from the start of the sentence or of a part of it, to its end) among those that leave out no word the sentence turns on (before them: a no, a
   question or an aim, "is claimed to", and a "may" where they hold none themselves; after them: a no, a question, a "but") and that hold no amount
   and nothing that waits for a person. Gives [first, last], or null where there is no such run: then nothing of the sentence is shown. */
export function iaWindow(toks, a, b) {
  const n = toks.length, low = toks.map(t => t.toLowerCase().replace(/’/g, "'").replace(/[^a-z'-]/g, "").replace(/^['-]+|['-]+$/g, ""));
  const neg = low.map(t => IA_T_NEG.test(t)), ask = low.map(t => IA_T_ASK.test(t)), said = low.map(t => IA_T_SAID.test(t)), may = low.map(t => IA_T_MAY.test(t)), but = low.map(t => IA_T_BUT.test(t));
  const edge = i => i >= 0 && (/[,;:)]$/.test(toks[i]) || low[i] === "that" || (i > 0 && /[,;:]$/.test(toks[i - 1]) && /^(?:and|but|or)$/.test(low[i])));   // a part of the sentence ends with this word ("..., and | the colour ...")
  const hang = /^(?:the|a|an|of|in|on|at|to|for|by|with|and|or|but|that|which|who|whose|as|than|from|into|onto|upon|over|under|between|among|across|during|after|before|about|against|within|through|via|per|versus|vs|when|where|while|because|since|its|their|this|these|those|is|are|was|were|be|been|has|have|had|not|no|more|less|very|both)$/, lame = /^(?:of|and|or|but|than|that|which|who|whose|as|to|is|are|was|were)$/;
  let best = null, top = -1e9;
  for (let s = Math.max(0, b - 14); s <= a; s++) {
    let pre = false, preMay = false; for (let i = 0; i < s; i++) { if (neg[i] || ask[i] || said[i]) pre = true; if (may[i]) preMay = true; }
    if (pre) break;                                                              // (every later start leaves that word out as well)
    for (let e = b; e <= Math.min(n - 1, s + 14); e++) {
      let out = false; for (let i = e + 1; i < n; i++) if (neg[i] || ask[i] || but[i]) { out = true; break; }
      if (out) continue;
      if (preMay) { let has = false; for (let i = s; i <= e; i++) if (may[i]) { has = true; break; } if (!has) continue; }
      const text = toks.slice(s, e + 1).join(" "); if (FIND_HELD.test(text) || IA_AMOUNT.test(text) || /https?:|www\.|\S@\S/i.test(text)) continue;
      const open = (text.match(/\(/g) || []).length !== (text.match(/\)/g) || []).length;
      const score = (s === 0 ? 6 : edge(s - 1) ? 4 : 0) + (e === n - 1 ? 6 : edge(e) ? 3 : 0) + (e - s + 1) / 2 - (e < n - 1 && hang.test(low[e]) ? 8 : 0) - (s > 0 && lame.test(low[s]) ? 3 : 0) - (open ? 2 : 0);
      if (score >= top) { top = score; best = [s, e]; }   // (of two that read equally well, the later: what follows the words pointed to is the rest of the finding)
    }
  }
  return best;
}
/* One finding through the gates. Gives { line, plain, why }: line is what a reader may be shown (the paper's own words: quote; its paper; animal;
   and t, the model's plain sentence, only where IA.plain allows it and the sentence is sound); plain is the verdict on the model's sentence, for
   the editors; why says why a finding was thrown away. papers: the ones given to the model, in their order; words: the question's key words. */
export function iaCheck(f, papers, words, names) {
  const no = why => ({ line: null, plain: null, why });
  if (!f || typeof f !== "object") return no("not a finding");
  const n = Number(f.n), p = Number.isInteger(n) && n >= 1 && n <= papers.length ? papers[n - 1] : null; if (!p) return no("a paper that was not given");
  const quote = clean(f.quote).replace(/^["'“‘.\s…]+|["'”’\s…]+$/g, ""), fq = iaFlat(quote);
  if (/<\s*[a-z!\/]|https?:|www\./i.test(quote)) return no("markup or a link");
  if (iaWords(quote).length < 2) return no("fewer than two words pointed to");
  // 1. the words pointed to stand in the summary, character for character: the sentence they stand in, and where in it
  let src = "", at = -1; for (const s of iaSents(p.ab)) { const i = iaFlat(s).indexOf(fq); if (i >= 0) { src = s; at = i; break; } }
  if (!src) return no("the words pointed to are not in the paper's summary");
  // 2. it bears on the question
  // (the model chose the sentence; the code asks that a key word of the question, or a word papers use for it, stands in that sentence, in the paper's
  // title or elsewhere in its summary, and keeps which: so that the editors can see how the lines found by title or summary alone read)
  let by = "";
  if (words && words.length) { const has = hay => words.some(w => iaNearStems(w).some(st => hay.includes(st))); by = has(iaFlat(src)) ? "s" : has(iaFlat(p.t)) ? "t" : has(iaFlat(p.ab)) ? "p" : ""; if (!by) return no("its paper does not bear on the question"); }
  // 3. animals or cells, or people: by the sentence where it says so, else by the whole summary. A sentence that speaks of both is not shown in part
  const fs = iaFlat(src), flatAll = iaFlat(p.t + ". " + p.ab), sa = IA_ANIMAL.test(fs), sp = IA_PEOPLE.test(fs) || /\b(?:clinical|placebo|double-blind)\b/.test(fs), pa = IA_ANIMAL.test(flatAll), pp = IA_PEOPLE.test(flatAll);
  if (sa && sp) return no("its sentence speaks of animals or cells and of people at once");
  // 4. the paper's own words that are shown: at most 15 of that sentence, in a row, chosen here
  const toks = src.split(/\s+/), a = Math.min(toks.length - 1, fs.slice(0, at).split(" ").length - 1), b = Math.min(toks.length - 1, a + fq.split(" ").length - 1, a + 14);
  const w = iaWindow(toks, a, b); if (!w) return no("no 15 words of its sentence can be shown without leaving out a word the sentence turns on, or without an amount, dying, overdose, pregnancy or children");
  const shown = (w[0] > 0 ? "…" : "") + toks.slice(w[0], w[1] + 1).join(" ").replace(/^[,;:\s]+|[,;:.\s]+$/g, "") + (w[1] < toks.length - 1 ? "…" : "");
  const plain = iaPlain(f.text, src, p, names);
  return { line: Object.assign({ quote: shown, n, kind: p.kind, y: p.y, j: p.j, doi: p.doi, pmid: p.pmid }, sa || (!sp && pa && !pp) ? { animal: true } : !sp && pa && pp ? { mixed: true } : {}, IA.plain && plain.ok ? { t: plain.t } : {}), plain, why: "", by };
}
export const iaGate = (f, papers, words, names) => iaCheck(f, papers, words, names).line;
// the model's reply, whatever shape the service gives it: a string, or an object already parsed
export function iaParse(out) {
  let v = out && typeof out === "object" ? (out.response !== undefined ? out.response : out.output_text !== undefined ? out.output_text : out.choices && out.choices[0] && out.choices[0].message ? out.choices[0].message.content : out.result !== undefined ? out.result : null) : out;
  if (v && typeof v === "object" && v.response !== undefined) v = v.response;
  if (typeof v === "string") { const a = v.indexOf("{"), b = v.lastIndexOf("}"); if (a < 0 || b <= a) return null; try { v = JSON.parse(v.slice(a, b + 1)); } catch (e) { return null; } }
  return v && typeof v === "object" && Array.isArray(v.findings) ? v : null;
}
const iaCost = (out, sent, got) => { const u = (out && out.usage) || {}, i = Number(u.prompt_tokens) || Math.ceil(sent / 3.6), o = Number(u.completion_tokens) || Math.ceil(got / 3.6); return i * IA.price[0] / 1e6 + o * IA.price[1] / 1e6; };
async function answer(request, url, env) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  // only this site's own pages: here a browser must say where the request comes from (a model's time is the one thing that could be used up)
  let host = ""; try { host = new URL(request.headers.get("origin") || "").host; } catch (e) { host = ""; }
  if (host !== url.host) return json({ ok: false, error: "origin" }, 403);
  let body = null;
  try { const t = await request.text(); if (t.length > 2500) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const rq = readQuestion(body); if (rq.error) return json({ ok: false, error: rq.error }, 422);
  const rf = readFind(body); if (rf.error) return json({ ok: false, error: rf.error }, 422);
  if (rf.held || FIND_HELD.test(rq.q)) return json({ ok: true, held: true });
  if (IA_NOT_RESEARCH.test(rq.q)) return json({ ok: true, none: true, why: "not a question for research summaries" });
  const store = env.QUESTIONS, ai = env.AI;
  if (!ai || !store || typeof ai.run !== "function") return json({ ok: true, off: true });
  try {
    const key = "ia:" + (await keyOf("v" + IA.v + "|" + rq.q.toLowerCase() + "|" + rf.names.join(",")));
    const had = await store.get(key, "json");
    if (had && had.v === IA.v && Array.isArray(had.lines)) return json(had.lines.length ? { ok: true, answer: { lines: had.lines, at: had.at }, again: true } : { ok: true, none: true, why: had.why || "nothing passed", again: true });
    const day = new Date().toISOString().slice(0, 10), dk = "ian:" + day, used = (await store.get(dk, "json")) || { n: 0, a: 0 };
    if ((used.n || 0) + 160 > IA.neurons || (used.a || 0) >= IA.answers) return json({ ok: true, full: true });
    // the papers' summaries, from Europe PMC (the same search as /api/find, with the summaries)
    const papers = await findPapers(env, rf.names, rf.groups, true, IA.papers);
    const keep = async (lines, why, cost, drop, plain) => {   // what was found (or that nothing passed) is kept, and the day's count
      const rec = Object.assign({ v: IA.v, at: new Date().toISOString(), names: rf.names, words: rf.words, lines, model: IA.writer }, why ? { why } : {}, drop && drop.length ? { drop: drop.slice(0, 6) } : {}, plain && plain.length ? { plain } : {});
      try { await store.put(key, JSON.stringify(rec), { expirationTtl: IA.kept }); if (cost > 0) await store.put(dk, JSON.stringify({ n: Math.round(((used.n || 0) + cost) * 10) / 10, a: (used.a || 0) + 1 }), { expirationTtl: 3 * 86400 }); } catch (e) { /* not kept: the answer is still given */ }
      return rec;
    };
    if (!papers.length) return json({ ok: true, none: true, why: "no summaries found" });
    const user = "QUESTION: " + rq.q + "\nNAMES OF THE DRUG: " + rf.names.join(", ") + "\n\nSUMMARIES\n" + papers.map((p, i) => "[" + (i + 1) + "] (" + (p.kind === "Review of studies" ? "review of studies" : p.kind.toLowerCase()) + ", " + (p.y || "year not given") + (p.j ? ", " + p.j : "") + ") " + p.t + "\n" + p.ab).join("\n\n");
    const messages = [{ role: "system", content: IA_SYS }, { role: "user", content: user }], sent = IA_SYS.length + user.length;
    let out = null, cost = 0;
    try { out = await ai.run(IA.writer, { messages, max_tokens: IA.room, temperature: 0, response_format: { type: "json_schema", json_schema: IA_SCHEMA } }); }
    catch (e) {   // the service could not keep to the form (its own words: "JSON Mode couldn't be met"), or does not know it: asked once more in plain words
      if (/allocation|quota|limit|capacity|4006|3036|429/i.test(String(e && e.message))) return json({ ok: true, full: true });
      try { out = await ai.run(IA.writer, { messages, max_tokens: IA.room, temperature: 0 }); } catch (e2) { return json({ ok: true, none: true, why: "the model could not be asked" }); }
    }
    const parsed = iaParse(out); cost = iaCost(out, sent, JSON.stringify(parsed || "").length + 40);
    if (!parsed) { await keep([], "no reply in the form asked for", cost); return json({ ok: true, none: true, why: "no reply in the form asked for" }); }
    const lines = [], from = new Set(), drop = [], plain = [];   // drop: what the checks refused, with the reason; plain: the model's own sentences with the code's verdict. Both for the editors, beside the answer
    for (const f of parsed.enough === false ? [] : parsed.findings.slice(0, 6)) { const c = iaCheck(f, papers, rf.words, rf.names), l = c.line;
      if (!l) { drop.push({ t: clean(f && f.text).slice(0, 300), q: clean(f && f.quote).slice(0, 200), why: c.why }); continue; }
      if (from.has(l.n) || lines.length >= 3) continue; from.add(l.n); lines.push(l); plain.push(Object.assign({ n: l.n, t: c.plain.t.slice(0, 300), ok: c.plain.ok, why: c.plain.why }, c.by === "t" ? { rel: "title" } : c.by === "p" ? { rel: "summary" } : {})); }
    const rec = await keep(lines, lines.length ? "" : parsed.enough === false ? "the summaries do not bear on the question" : "nothing passed the checks", cost, drop, plain);
    return json(lines.length ? { ok: true, answer: { lines, at: rec.at } } : { ok: true, none: true, why: rec.why });
  } catch (e) { return json({ ok: true, none: true, why: "error" }); }
}
// one more person asked a question that is on the public list: the item's number, counted
async function want(request, url, store) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  if (!store) return json({ ok: false, error: "no store" }, 503);
  const origin = request.headers.get("origin");
  if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
  let body = null;
  try { const t = await request.text(); if (t.length > 200) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const id = String((body && body.id) || "");
  if (!/^w_[a-z0-9_]{1,40}$/.test(id)) return json({ ok: false, error: "id" }, 422);
  try {
    const day = new Date().toISOString().slice(0, 10), key = "w:" + id, had = await store.get(key, "json");
    if (had && had.last === day && (had.dn || 1) >= MAX_WANT_SAME_A_DAY) return json({ ok: true });   // counted enough for today: nothing is written
    const ck = "count:" + day, n = parseInt((await store.get(ck)) || "0", 10) || 0;
    if (n >= MAX_WANT_UNTIL) return json({ ok: true, full: true });   // the day's room is kept for questions people send
    await store.put(ck, String(n + 1), { expirationTtl: 3 * 86400 });
    const rec = had ? { n: (had.n || 1) + 1, dn: had.last === day ? (had.dn || 1) + 1 : 1, first: had.first || day, last: day } : { n: 1, dn: 1, first: day, last: day };
    await store.put(key, JSON.stringify(rec));
    return json({ ok: true });
  } catch (e) { return json({ ok: false, error: "store" }, 503); }
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url), at = url.pathname.replace(/\/+$/, "");   // "/api/ask/" is "/api/ask"
    if (at === "/api/find") return find(request, url, env);
    if (at === "/api/answer") return answer(request, url, env);
    if (at !== "/api/ask" && at !== "/api/want") return url.pathname.startsWith("/api/") ? json({ ok: false, error: "not found" }, 404) : env.ASSETS.fetch(request);
    const store = env.QUESTIONS;
    if (at === "/api/want") return want(request, url, store);
    if (request.method === "GET") return json({ ok: !!store, find: true, auto: !!store, quick: !!(store && env.AI) });   // 200 either way: a missing store is a state, not an error in the reader's console
    if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
    if (!store) return json({ ok: false, error: "no store" }, 503);
    // only this site's own pages may send
    const origin = request.headers.get("origin");
    if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
    let body = null;
    try { const t = await request.text(); if (t.length > 2000) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
    const r = readQuestion(body); if (r.error) return json({ ok: false, error: r.error }, 422);
    try {
      const day = new Date().toISOString().slice(0, 10), hash = await keyOf(r.q.toLowerCase());
      // a question the page sent by itself is kept apart ("aq:"), unless someone has already chosen to send that very question ("q:"): then it is counted there
      let key = "q:" + hash, had = await store.get(key, "json"), auto = false;
      if (r.a && !had) { auto = true; key = "aq:" + hash; had = await store.get(key, "json"); }
      if (had && had.last === day && (had.dn || 1) >= MAX_SAME_A_DAY) return json({ ok: true, again: true });   // counted enough for today: nothing is written
      const ck = "count:" + day, n = parseInt((await store.get(ck)) || "0", 10) || 0;
      if (n >= (auto ? MAX_AUTO_UNTIL : MAX_A_DAY)) return json({ ok: false, error: "full for today" }, 429);
      await store.put(ck, String(n + 1), { expirationTtl: 3 * 86400 });
      const opts = auto ? { expirationTtl: AUTO_KEPT } : undefined;
      if (had) {
        had.n = (had.n || 1) + 1; had.dn = had.last === day ? (had.dn || 1) + 1 : 1; had.last = day;
        if (r.d && !(had.d || []).includes(r.d)) had.d = (had.d || []).concat(r.d).slice(0, 5);
        await store.put(key, JSON.stringify(had), opts); return json({ ok: true, again: true });
      }
      await store.put(key, JSON.stringify(Object.assign({ q: r.q, d: r.d ? [r.d] : [], v: r.v, first: day, last: day, n: 1, dn: 1 }, auto ? { a: 1 } : {})), opts);
      return json({ ok: true });
    } catch (e) { return json({ ok: false, error: "store" }, 503); }
  }
};
