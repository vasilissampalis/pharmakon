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
   POST /api/answer {q, names, words} -> a written answer within seconds, where the Workers AI binding (AI) exists: one to three
                               sentences from the summaries of those papers, each with its paper's own words and link, every one
                               passed by the code's own checks (site 2.18; its full account stands above the code, below).
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
export function readFind(body) {
  const uniq = a => [...new Set(a.filter(Boolean))];
  const names = uniq((Array.isArray(body && body.names) ? body.names : []).slice(0, 12).map(findName)).slice(0, 6);
  const words = uniq((Array.isArray(body && body.words) ? body.words : []).slice(0, 12).map(findWord)).filter(w => !names.includes(w)).slice(0, 6);
  if (!names.length) return { error: "no name" };
  return { names, words, held: names.concat(words).some(t => FIND_HELD.test(t)) };
}
export function findQueries(names, words) {
  const field = (ts, titleOnly) => "(" + ts.map(t => titleOnly ? `TITLE:"${t}"` : `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")";
  const tail = ' AND LANG:eng NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"';
  const rev = ' AND (PUB_TYPE:"review" OR PUB_TYPE:"systematic review" OR PUB_TYPE:"meta-analysis")';
  const core = field(names) + (words.length ? " AND " + field(words) : "");
  return [core + rev + tail, core + tail, field(names, true) + rev + tail];   // reviews on the question; any paper on it; reviews of the drug itself
}
export function findPaper(r) {
  if (!r || typeof r !== "object") return null;
  const t = clean(String(r.title || "").replace(/<[^>]+>/g, "")).replace(/\.$/, "").slice(0, 300); if (t.length < 8) return null;
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
  const get = env.FETCH || fetch, seen = new Set(), out = [];
  const ask = async q => {
    const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 7000);
    try {
      const res = await get(EPMC + "?query=" + encodeURIComponent(q) + "&format=json&resultType=lite&pageSize=8", { headers: { accept: "application/json", "user-agent": "pharmakon.world (contact@pharmakon.world)" }, signal: ctl.signal, cf: { cacheTtl: 86400, cacheEverything: true } });
      if (!res.ok) return [];
      const d = await res.json(); return ((d && d.resultList && d.resultList.result) || []).map(findPaper).filter(Boolean);
    } catch (e) { return []; } finally { clearTimeout(timer); }
  };
  try {
    const qs = findQueries(r.names, r.words), [a, b] = await Promise.all([ask(qs[0]), ask(qs[1])]);
    let all = a.concat(b); if (all.length < 3) all = all.concat(await ask(qs[2]));
    for (const p of all) { const k = p.doi || p.pmid; if (seen.has(k)) continue; seen.add(k); out.push(p); if (out.length >= 6) break; }
    return json({ ok: true, papers: out });
  } catch (e) { return json({ ok: false, error: "search" }, 502); }
}
// ---- a written answer within seconds (POST /api/answer; site 2.18, 18 November 2026; docs/AUTOMATION.md, decision 31)
/* The senior author, 17 November 2026: "people are used to get responses instantly. We have to make an ai which is able to do that for
   questions it does not know"; and, of the list of papers that 2.16 shows: "we have to make instant as good as getting answers from a very
   good claude api. whatever it takes."
   What it is. For a question about a drug that the site has no answer to, this server reads the SUMMARIES of the papers Europe PMC finds
   (their abstracts; never a paper's full text) with one language model run by Cloudflare itself (Workers AI, bound to this site as AI: the
   only place a reader's words go besides this server), and gives back one to three sentences, each saying what ONE paper found, each with
   that paper's own words beside it (at most 15, copied) and its link. It is shown to the reader under its own label ("written just now by
   our system from the summaries of these papers ... no person has checked it"), never as an answer of ours: nothing of it enters the
   site's data, and the question still goes to the lane, which reads the papers themselves and passes its checks.
   What the code decides, not the model (a sentence that fails any of these is thrown away; with none left, nothing is shown):
     1. its paper is one of those given, and its quoted words stand in that paper's summary, character for character, 4 to 15 words;
     2. it says what kind of paper it rests on, as Europe PMC files it (a review, a trial, a study, a case report), and no other year;
     3. every number in it stands in that summary (or is the paper's year);
     4. no amount, dose or timing; no advice ("should", "safe", "recommended", "try", "avoid", "you"); nothing on making an effect stronger;
        no way of taking compared with another;
     5. a word that makes a finding bigger or surer ("proves", "all", "most", "causes", "cures", "effective", "significantly" ...) only
        where the summary itself has that word;
     6. a summary about animals or cells and not about people: the sentence says so;
     7. it bears on the question (a key word of the question stands in it or in its quoted words), where the question has key words.
   Not answered here: a question about dying, overdose, amounts, pregnancy, children or suicide (FIND_HELD: these wait for a person), and a
   question research summaries cannot answer (the law, prices, drug tests).
   What it costs: Cloudflare's free allowance is 10,000 neurons a day for the whole account, shared with the machine lane. This endpoint
   stops by itself at IA.neurons a day (and IA.answers new answers); the lane stops at its own share (scripts/auto/llm.py: OUR_LIMIT).
   On Cloudflare's free plan a used-up allowance ends in an error, never in a charge. An answer once written is kept for 30 days and
   given again for the same question (no model is asked twice).
   What is kept (key "ia:<fingerprint>"): the drug's names and key words, the sentences that passed with their papers, the sentences the
   checks refused with the reason (never shown to a reader), the model's name and the time; never the reader's sentence. So that the editors can read everything the system wrote this way. And the day's count
   ("ian:<day>": neurons and answers). Nothing is logged. */
export const IA = { v: 1, writer: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", price: [26668, 204805], neurons: 3500, answers: 60, kept: 30 * 86400, papers: 5, chars: 1500, room: 420 };
const IA_NOT_RESEARCH = /\b(legal\w*|illegal\w*|law|laws|lawful|police|arrest\w*|prison|jail|court|customs|border|airport|price|prices|cost|costs|cheap\w*|buy|buying|bought|order\w*|dealers?|vendors?|drug tests?|test positive|urine|piss test|hair test|workplace test|screening test)\b/i;
const IA_SYS = `You help Pharmakon, a free drug encyclopedia, tell a reader at once what published research says about their question. You get the question and the SUMMARIES (abstracts) of a few papers, numbered. Nobody has read the full papers. Use only the summaries: what you know yourself does not count.

Write 1 to 3 findings that bear on the question, the most direct first, each from a different summary. For each finding give:
"n": the number of the ONE summary it comes from.
"quote": the words of that summary that carry the finding, copied exactly, character for character, 5 to 15 words from one sentence.
"text": ONE plain sentence, at most 30 words, for a reader with no science training, saying what that paper found or says. Begin with the kind of paper and its year exactly as given in the brackets: "A 2021 review says ...", "A 2013 trial found ...", "A 2019 study found ...", "A 2018 case report describes ...". Say who was studied when the summary says so (people and how many; rats; mice; cells). Say only what the quoted words and their sentence say: not more certain, not wider, not bigger. Keep "may", "might", "suggests" where the summary has them.

Rules. No amounts, doses, milligrams or timing. No advice: never "should", "safe", "recommended", "try", "avoid", never "you". Nothing on how to take, prepare or mix anything, or on making an effect stronger. Never say a drug treats, cures, helps or works unless the summary's own words say so, and then as what the paper says. When a summary is about animals or cells, say so. Do not judge people who use drugs. If the summaries do not bear on the question, answer {"enough": false, "findings": []}.

Answer with JSON only: {"enough": true, "findings": [{"n": 1, "quote": "...", "text": "..."}]}`;
const IA_SCHEMA = { type: "object", properties: { enough: { type: "boolean" }, findings: { type: "array", items: { type: "object", properties: { n: { type: "integer" }, quote: { type: "string" }, text: { type: "string" } }, required: ["n", "quote", "text"] } } }, required: ["enough", "findings"] };
const iaFlat = s => clean(String(s == null ? "" : s).replace(/<[^>]+>/g, " ")).toLowerCase().replace(/[‘’‚′`]/g, "'").replace(/[“”„″]/g, '"').replace(/[‐-―−]/g, "-").replace(/\s+/g, " ");
const iaWords = s => iaFlat(s).match(/[a-z0-9][a-z0-9'-]*/g) || [];
// a paper with a summary long enough to say something: what findPaper keeps, and the summary cut at the end of a sentence
export function iaPaper(r) {
  const p = findPaper(r); if (!p) return null;
  let ab = clean(String((r && r.abstractText) || "").replace(/<[^>]+>/g, " ")); if (ab.length < 250) return null;
  if (ab.length > IA.chars) { const cutAt = ab.lastIndexOf(". ", IA.chars); ab = ab.slice(0, cutAt > 600 ? cutAt + 1 : IA.chars); }
  return Object.assign(p, { ab });
}
const IA_KIND = { "Review of studies": /\breview\b|\bmeta-analysis\b/i, "Review": /\breview\b/i, "Trial": /\btrial\b|\bstudy\b/i, "Case report": /\bcase\b/i, "Study": /\bstudy\b|\bsurvey\b|\banalysis\b|\bexperiment\b|\bpaper\b|\breport\b/i };
const IA_AMOUNT = /\d\s?(?:mg|mcg|µg|μg|ug|g|kg|ml|iu|units?)\b|\b(?:milligrams?|micrograms?|grams?|dos(?:e|es|age|ages|ing|ed)|every \d+ (?:minutes?|hours?)|redos\w*)\b/i;   // (how often somebody uses, "daily", is not an amount: it stays)
const IA_ADVICE = /\b(?:should|shouldn't|must|ought|recommend\w*|advis\w*|try|tries|avoid\w*|safe|safely|safer|safest|safety|harmless|best|ideal|you|your|yours|yourself|we|our)\b/i;
const IA_STRONGER = /\b(?:potentiat\w*|boost\w*|stronger|strongest|intensif\w*|enhanc\w*|synerg\w*|combin\w* with|mix\w* with|together with)\b/i;
const IA_ROUTE = /\b(?:oral\w*|smok\w*|inject\w*|snort\w*|intranasal\w*|insufflat\w*|intraven\w*|sublingual\w*|rectal\w*|vap\w*|edibles?|eaten|eating|swallow\w*|chew\w*|inhal\w*)\b/i, IA_THAN = /\b(?:than|compared|versus|vs|faster|slower|quicker)\b/i;
const IA_MORE = /\b(?:prov(?:e|es|ed|en)|definite\w*|certain\w*|clear(?:ly)?|always|never|all|every|everyone|everybody|nobody|none|most|majority|cur(?:e|es|ed)|treat(?:s|ed|ment)?|heal(?:s|ed)?|guarantee\w*|significan\w*|strong(?:ly)?|powerful\w*|dramatic\w*|very|highly|extremely|greatly|caus(?:e|es|ed)|leads? to|prevent\w*|protect\w*|effective\w*|works?|worked|help(?:s|ed|ful)?|improv\w*|reduc\w*|lower\w*|rais\w*|increas\w*|decreas\w*|common\w*|rare\w*|often|usually|addictive|dependence|toxic\w*|dangerous\w*|harm\w*|benefi\w*)\b/gi;
const IA_ANIMAL = /\b(?:rats?|mice|mouse|rodents?|zebrafish|in vitro|cell lines?|cultured cells|animals?|murine|preclinical)\b/i, IA_PEOPLE = /\b(?:participants?|patients?|volunteers?|humans?|men|women|adults?|people|subjects|students|respondents|users|individuals|persons)\b/i, IA_SAYS_ANIMAL = /\b(?:rats?|mice|mouse|animals?|cells?|lab|laboratory|zebrafish|rodents?|test tube)\b/i;
const IA_NUMWORD = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety", 100: "(?:one |a )?hundred" };
const iaStem = w => (w.length > 6 ? w.slice(0, 5) : w.replace(/(?:es|s|ed)$/, ""));
/* One finding through the gates: the cleaned line, or null. papers: the ones given to the model, in their order; words: the question's key words. */
export function iaCheck(f, papers, words) {
  const no = why => ({ line: null, why });
  if (!f || typeof f !== "object") return no("not a finding");
  const n = Number(f.n), p = Number.isInteger(n) && n >= 1 && n <= papers.length ? papers[n - 1] : null; if (!p) return no("a paper that was not given");
  let text = clean(f.text).replace(/^["'“]+|["'”]+$/g, ""); const quote = clean(f.quote).replace(/^["'“‘.\s]+|["'”’\s]+$/g, "");
  const tw = iaWords(text), qw = iaWords(quote);
  if (/[<>{}\[\]\\]|https?:/i.test(text + quote)) return no("markup or a link");
  if (tw.length < 6 || tw.length > 36) return no("the sentence is too short or too long");
  if (qw.length < 4 || qw.length > 15) return no("the quoted words are fewer than 4 or more than 15");
  if (!/[.!?]$/.test(text)) text += ".";
  const src = iaFlat(p.ab), all = iaFlat(p.t + ". " + p.ab);
  if (!src.includes(iaFlat(quote))) return no("the quoted words are not in the paper's summary");            // 1. its paper's own words, copied
  if (!IA_KIND[p.kind].test(text.split(/\s+/).slice(0, 9).join(" "))) return no("it does not name its kind of paper (" + p.kind.toLowerCase() + ")");   // 2. the kind of paper it rests on
  const years = text.match(/\b(?:19|20)\d\d\b/g) || []; if (years.some(y => y !== p.y)) return no("another year than the paper's");   //    and no other year than the paper's
  for (const num of text.match(/\d+(?:[.,]\d+)?/g) || []) { if (num === p.y) continue;                             // 3. its numbers (a number the summary writes as a word counts: "sixteen" for 16)
    if (!new RegExp("(?:^|[^0-9.,])" + num.replace(/[.,]/g, "[.,]") + "(?:$|[^0-9])").test(all) && !(IA_NUMWORD[num] && new RegExp("\\b" + IA_NUMWORD[num] + "\\b").test(all))) return no("a number the summary does not hold (" + num + ")"); }
  if (FIND_HELD.test(text)) return no("dying, overdose, amounts, pregnancy or children");                      // 4. no amounts, no advice, nothing on making an effect stronger
  if (IA_AMOUNT.test(text)) return no("an amount, a dose or timing");
  { const m = text.match(IA_ADVICE); if (m) return no("advice, or speaking to the reader (" + m[0].toLowerCase() + ")"); }
  if (IA_STRONGER.test(text)) return no("making an effect stronger, or mixing");
  if (IA_ROUTE.test(text) && IA_THAN.test(text)) return no("a way of taking compared with another");          //    no way of taking compared with another
  const stems = new Set((all.match(/[a-z]+/g) || []).map(iaStem));
  for (const m of text.toLowerCase().match(IA_MORE) || []) { if (!m.split(/\s+/).every(w => w === "to" || stems.has(iaStem(w)))) return no("a word the summary does not have (" + m + ")"); }   // 5. no word bigger or surer than the summary's own
  if (IA_ANIMAL.test(all) && !IA_PEOPLE.test(all) && !IA_SAYS_ANIMAL.test(text)) return no("a summary about animals or cells, not said");   // 6. animals or cells: said
  if (words && words.length) { const hay = new Set(tw.concat(qw).map(iaStem)); if (!words.some(w => hay.has(iaStem(w)))) return no("it does not bear on the question"); }   // 7. it bears on the question
  return { line: { t: text, quote, n, kind: p.kind, y: p.y, j: p.j, doi: p.doi, pmid: p.pmid }, why: "" };
}
export const iaGate = (f, papers, words) => iaCheck(f, papers, words).line;
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
    const get = env.FETCH || fetch, seen = new Set(), papers = [];
    const ask = async q => {
      const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 7000);
      try {
        const res = await get(EPMC + "?query=" + encodeURIComponent(q) + "&format=json&resultType=core&pageSize=6", { headers: { accept: "application/json", "user-agent": "pharmakon.world (contact@pharmakon.world)" }, signal: ctl.signal, cf: { cacheTtl: 86400, cacheEverything: true } });
        if (!res.ok) return [];
        const d = await res.json(); return ((d && d.resultList && d.resultList.result) || []).map(iaPaper).filter(Boolean);
      } catch (e) { return []; } finally { clearTimeout(timer); }
    };
    const qs = findQueries(rf.names, rf.words), [a, b] = await Promise.all([ask(qs[0]), ask(qs[1])]);
    let all = a.concat(b); if (all.length < 2) all = all.concat(await ask(qs[2]));
    for (const p of all) { const k = p.doi || p.pmid; if (seen.has(k)) continue; seen.add(k); papers.push(p); if (papers.length >= IA.papers) break; }
    const keep = async (lines, why, cost, drop) => {   // what was written (or that nothing passed) is kept, and the day's count
      const rec = Object.assign({ v: IA.v, at: new Date().toISOString(), names: rf.names, words: rf.words, lines, model: IA.writer }, why ? { why } : {}, drop && drop.length ? { drop: drop.slice(0, 6) } : {});
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
    const lines = [], from = new Set(), drop = [];   // drop: what the model wrote that the checks refused, with the reason: kept beside the answer, for the editors
    for (const f of parsed.enough === false ? [] : parsed.findings.slice(0, 6)) { const c = iaCheck(f, papers, rf.words), l = c.line;
      if (!l) { drop.push({ t: clean(f && f.text).slice(0, 300), why: c.why }); continue; }
      if (from.has(l.n) || lines.length >= 3) continue; from.add(l.n); lines.push(l); }
    const rec = await keep(lines, lines.length ? "" : parsed.enough === false ? "the summaries do not bear on the question" : "nothing passed the checks", cost, drop);
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
