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
   (site 2.21) A NEW question also starts the system's work at once, where the senior author has given this server the key for that (startWork, below).
   POST /api/ask {q, d, v, a: 1} -> the same for a question the page sent by itself. It is kept apart (keys "aq:"), for
                               180 days, and its words are never written into the public repository: the scout reads such
                               questions in a run's own memory and keeps only OUR wording of what was asked
                               (scripts/auto/fetch_questions.py --auto; scripts/auto/ask.py). When someone has already
                               chosen to send the very same question, it is counted there instead. These stop at 250 a
                               day, so that they can never crowd out a question someone chose to send.
   POST /api/want {id}      -> {"ok": true}  one more person asked a question that is on the site's public list of
                               questions not answered yet (site 2.5). Only the list item's number arrives ("w_0041"):
                               never the person's words. Kept: the number, a count, the last day.
   POST /api/find {names, words, def} -> {"ok": true, "papers": [...], "more": 1 when a search was still out}  (site 2.16, 17 November 2026; the senior author: "answers take
                               too long to get responses and people are used to get responses instantly ... our ai should be able to
                               find answers almost instantly"). Published research on a drug, looked up at once in Europe PMC, the
                               open index of medical research (https://europepmc.org; its public search service, no key), and, since
                               site 2.20, for each paper at most 15 of its own words on the question, cut from the end of its summary
                               by fixed rules: no model reads or writes anything. What arrives: the names of a drug (up to 6) and
                               plain key words (up to 6), chosen on the reader's device; never the reader's sentence. What goes out to
                               Europe PMC: those names and words, from this server (the reader's address is not passed on). What comes
                               back to the page: for up to 6 papers the title, the authors, the journal, the year, the kind of paper,
                               whether it is free to read, its link, and those words where the rules find them. Nothing is kept or
                               logged here. The full account stands above the code, below.
   GET  /api/asked?h=KEY[,KEY...][&w=ID[,ID...]] -> {"ok": true, "q": {KEY: ...}, "w": {ID: ...}}  (site 2.23, 19 November 2026; the senior author, 18 November,
                               23:42: "like 5 minutes pass and i don't have an answer from inside the website it should be answered almost
                               immediately"). What our system is doing for a question this reader sent: our own wording of it, what has been
                               done so far, and the answer itself the moment it is written and has passed every gate. KEY: the store's own key
                               of a sent question (20 hex; the page had it from POST /api/ask, or works it out from the question it sent);
                               ID: a question of our list that the reader asked to be told about. Read from one small file in the public
                               repository (data/auto/live.json, written by scripts/auto/live.py in a run of the system). Nothing is kept or
                               logged. The full account stands above the code, below.
   POST /api/answer         -> {"ok": true, "off": true}. Sites 2.18 and 2.19 asked a language model here; 2.20 does not.
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
  // (2.22) x: what the page had taken for the answer, where the reader pressed "Not what you asked?": an answer's id, or the address of a place of the site. Nothing else is taken
  const x0 = String((body && body.x) == null ? "" : body.x), x = /^(?:cl|au)_[a-z0-9_]{1,60}$/.test(x0) || /^#[a-z0-9][a-z0-9_\/-]{1,70}$/.test(x0) ? x0 : "";
  return Object.assign({ q, d, v, a: !!(body && (body.a === 1 || body.a === true)) }, x ? { x } : {});
}
// ---- published research, looked up at once, each paper with its own words on the question (POST /api/find; sites 2.16 to 2.20)
/* The senior author, 17 November 2026: "people are used to get responses instantly. We have to make an ai which is able to do that for
   questions it does not know"; and, of the list of papers that 2.16 showed: "we have to make instant as good as getting answers from a very
   good claude api. whatever it takes."
   What it is now (site 2.20, 18 November 2026). For a question about a drug that the site has no answer to, this server asks Europe PMC for
   the papers on the drug and the question's key words, and gives each paper back with, where the rules below find one, AT MOST 15 OF THE
   PAPER'S OWN WORDS on the question, cut out of the end of its summary (its results or conclusions). No language model reads, chooses or
   writes anything: fixed rules do, so the same question always gets the same words, a reader's sentence is sent to nobody, and nothing here
   can be used up or cost money.
   How it came to this (the full account: docs/AUTOMATION.md, decision 31).
     2.18 let a model (Cloudflare Workers AI, a free one) write a sentence for each paper. Tried with the real model on 18 of the editor's
     questions before any reader met it, about six of the 19 sentences that passed the rules said more than their paper.
     2.19 showed the paper's own words instead, the model only choosing the sentence. Tried on 26 questions: the words could no longer say
     more than the paper, but the model chose sentences about aims and methods, sentences cut loose from what they were about ("60.4%" of
     people given cocaine as a medicine bled, under "does cocaine cause nosebleeds"), and its own sentences were still wrong about four
     times in ten even where every word of them stood in the paper. It also took five seconds and a share of a free allowance.
     2.20 takes the model out. What a paper found stands at the end of its summary, in words that hold the question's key word: a rule can
     find that, at once and for nothing. Every paper is shown with its title, so the words always stand in their paper's own frame.
   Which papers (findQueries, findPapers): the drug's name must stand in a paper's TITLE (in trial 2 the most cited papers that only mention
   a drug read as answers: a meta-analysis on diabetes for "GHB", which is also glycated haemoglobin). Asked together: the most cited
   reviews of the drug that hold every key word; the most cited papers with the drug and every key word in their very title; the newest
   of those; and the papers that hold the drug and the key words anywhere. Wider only where that finds fewer than three.
   How long (findPapers). Europe PMC answers a search in a fraction of a second, but about one request in three hangs for two to ten
   seconds, whatever is asked (trials 6 to 9), and the same search asked again at that moment mostly comes back at once. So nobody waits
   for a search that hangs: the most cited are asked for again after 0.6 s and 1.3 s, and the first reply counts; the reader gets the
   list as soon as the most cited are back (with the newest, if they come within three tenths of a second), and after two seconds
   whatever three papers there are, with "more": 1: the page then asks once more a moment later and shows the whole list. A search that
   is still out finishes behind the reply, and every reply of Europe PMC is kept for a day (Cloudflare's cache), so that the same search
   is not made twice. "ms", "again", "won", "own" and "kept" in the reply are numbers for the editors: how long, how many askings,
   which one answered, how many came from what was kept. Nothing of a reader.
   Which words (iaPick, iaWindow). A paper gets words only where ALL of this holds:
     1. the sentence stands where papers say what they found: under a label for results or conclusions, or, in a summary without labels,
        in its later half; it is not a sentence about what the paper set out to do or how it was done;
     2. it holds a key word of the question (or a word papers use for it), and every key word stands in the sentence or the paper's title;
     3. the sentence names the drug; or the paper is about the drug (its name in the title) and the sentence says "the extract", "this
        compound", "its use". It does not point back to another sentence ("these effects", "in this context");
     4. it does not speak of animals or cells and of people at once (a part of it could be read as the other);
     5. there are at most 15 words of it, in a row and holding the key word, that leave out no word the sentence turns on: before them a
        "no" (not, never, without, fail, lack, non-significant, insufficient, little, few, only, contrary, myth ...), a question or an aim
        ("we examined whether"), what people say ("is claimed to"), the kind of evidence ("in case reports", "an open-label pilot"), or a
        "may" the words do not hold themselves; after them a "no", a question or a "but". "There was no evidence that the extract reduced
        anxiety" is shown with its "no evidence" or not at all. (A clause that opens the sentence with "Although ..." does not govern
        what follows its comma.) Where 15 words cannot hold such a word, nothing of that sentence is shown;
     6. those words hold no amount, dose or timing; nothing about dying, overdose, pregnancy or children; nothing on making an effect
        stronger or taking drugs together; no way of taking compared with another; no advice and no promise of safety ("should", "safe",
        "well tolerated"); no link; no statistics in signs (=, <, >); and they do not break off inside brackets.
   A line says "in animals or cells, not in people" where its sentence or its whole summary is about those, and that the summary covers
   such work too where it covers both and the sentence does not say which.
   For "what is X" the rule takes the sentence that says what the drug is ("X is a ...") from the start of a summary instead.
   Not looked up at all: words about suicide, self-harm or amounts (FIND_NEVER). Papers are listed but NO WORDS of them are shown (titles
   only) for what research summaries cannot settle for a reader (the law, prices, drug tests), and, since site 2.21, for a question about pregnancy or
   children (FIND_TITLES) and for a question that names no single drug (the page says so: titles); since site 2.22 also for a question of fact about
   dying or overdose (FIND_DEATH). The senior author, 18 November 2026, 22:15 Athens, of a question how many people die from heroin in one country, which got no
   research: "in general for question it does not know there should be instant searches available at least when the user is waiting". Until that
   day a key word about dying held the whole lookup. Which of those questions the PAGE does not send at all (an amount that kills, a way of dying, ending
   one's own life) is decided on the reader's device, which alone sees the sentence (app.insight.js, FIND_DEATH_NOT); here only the key words arrive. The senior author, 18 November 2026, 13:38 and 13:40
   Athens, of a question about mothers and their children's drug use that got no research: "we have to give instant search on this instance too". Until
   that day such a question was not looked up at all. What the rule may show of a paper's own words is unchanged: FIND_HELD stands in it as it did.
   What arrives: the names of a drug (up to 6) and plain key words (up to 6), chosen on the reader's device; never the reader's sentence.
   What goes out to Europe PMC: those names and words, from this server (the reader's address is not passed on). Nothing is kept or logged
   here; Cloudflare keeps Europe PMC's reply for a day so that the same search is not asked twice. */
const EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search";
export const FIND_HELD = /\b(pregnan\w*|breast-?feed\w*|child|children|kids?|bab(y|ies)|infants?|teen\w*|minors?|suicid\w*|kill\w*|die[sd]?|dying|deaths?|dead|deadly|mortalit\w*|overdos\w*|lethal|fatal\w*|dos(e|es|age|ing)|mg|milligrams?|grams?|micrograms?)\b/i;
// never looked up: suicide, self-harm, amounts. Looked up and listed by title only: pregnancy and children (2.21); dying and overdose (2.22: FIND_DEATH)
export const FIND_NEVER = /\b(suicid\w*|self-?harm\w*|lethal|ld50|dos(e|es|age|ing)|mg|mcg|milligrams?|grams?|micrograms?)\b/i;
export const FIND_DEATH = /\b(kill\w*|die[sd]?|dying|deaths?|dead|deadly|mortalit\w*|overdos\w*|fatal\w*|poisoning)\b/i;
export const FIND_TITLES = /\b(pregnan\w*|breast-?feed\w*|lactat\w*|child|children|childhood|kids?|bab(y|ies)|infants?|newborns?|toddlers?|teen\w*|adolescen\w*|minors?|youths?|underage|school\w*|f(?:o)?etus|f(?:o)?etal|prenatal|perinatal|maternal|mothers?|paternal|fathers?|parent\w*|p(?:a)?ediatric\w*)\b/i;
// (2.21) what research calls the subject of a question that names no single drug: these stand in the place of a drug's name (the page sends them)
const FIND_GEN_NAMES = new Set(["drug use", "substance use", "addiction", "substance use disorder", "drug overdose", "overdose"]);   // (2.22: overdose, where no drug is named)
const FIND_NOT_RESEARCH = /^(?:legal\w*|illegal\w*|law|laws|lawful|police|arrest\w*|prison|jail|court|customs|border|airport|price|prices|cost|costs|cheap\w*|buy|buying|bought|order\w*|dealers?|vendors?|urine|test|tests|tested|testing|screen\w*|detect\w*)$/i;
const findName = s => { s = clean(s).toLowerCase(); return /^[a-z0-9][a-z0-9 ,.'+()\-]{1,58}[a-z0-9)]$/.test(s) && !/["\\:]/.test(s) ? s : ""; };
const findWord = s => { s = clean(s).toLowerCase(); return /^[a-z]{3,24}$/.test(s) ? s : ""; };
// a key word may come with the word papers use for it, as one entry: "appetite|hungry". The two are one thing asked for, in two ways.
// def: the question asks what the drug is ("what is phenibut"); noq: papers are listed and no words of them are shown: its key words are about the law, prices or
// drug tests, or about pregnancy or children, or the page asked for titles only (t: 1: a question that names no single drug)
// also: what the drug's page is called, where the reader named a drug of its own ("xanax": benzodiazepines; "tramadol": prescription opioids): asked for
// only where the reader's own name finds fewer than three papers
export function readFind(body) {
  const uniq = a => [...new Set(a.filter(Boolean))];
  const names = uniq((Array.isArray(body && body.names) ? body.names : []).slice(0, 12).map(findName)).slice(0, 6);
  const also = uniq((Array.isArray(body && body.also) ? body.also : []).slice(0, 8).map(findName)).filter(n => !names.includes(n)).slice(0, 4);
  const groups = (Array.isArray(body && body.words) ? body.words : []).slice(0, 12).map(e => uniq(String(e == null ? "" : e).split("|").slice(0, 3).map(findWord)).filter(w => !names.includes(w))).filter(g => g.length).slice(0, 6);
  const words = uniq(groups.flat());
  if (!names.length) return { error: "no name" };
  return { names, also, words, groups, def: !!(body && (body.def === 1 || body.def === true)) && !groups.length, gen: names.every(n => FIND_GEN_NAMES.has(n)), noq: !!(body && (body.t === 1 || body.t === true)) || names.every(n => FIND_GEN_NAMES.has(n)) || words.some(w => FIND_NOT_RESEARCH.test(w)) || names.concat(also, words).some(t => FIND_TITLES.test(t) || FIND_DEATH.test(t)), held: names.concat(also, words).some(t => FIND_NEVER.test(t)) };
}
const FIND_SPELL = "colour color|behaviour behavior|tumour tumor|flavour flavor|odour odor|labour labor|vapour vapor|anaemia anemia|anaesthesia anesthesia|anaesthetic anesthetic|haemorrhage hemorrhage|oedema edema|diarrhoea diarrhea|oestrogen estrogen|ageing aging|centre center|fibre fiber|analogue analog|programme program|grey gray|sulphate sulfate|leukaemia leukemia".split("|").map(p => p.split(" "));
// a word as papers may write it: its one and its many ("migraines", "migraine") and its other spelling ("colour", "color"; "-ise", "-ize")
export function findForms(w) {
  const out = new Set([w]); if (/ies$/.test(w) && w.length > 5) out.add(w.slice(0, -3) + "y"); else if (/[^su]s$/.test(w) && w.length > 4) out.add(w.slice(0, -1));
  for (const f of [...out]) { for (const [a, b] of FIND_SPELL) { if (f === a) out.add(b); else if (f === b) out.add(a); else if (f === a + "s") out.add(b + "s"); else if (f === b + "s") out.add(a + "s"); }
    const z = f.replace(/is(e|ed|es|ing|ation|ations)$/, "iz$1"), s = f.replace(/iz(e|ed|es|ing|ation|ations)$/, "is$1"); if (z !== f) out.add(z); if (s !== f) out.add(s); }
  return [...out];
}
// a drug's name as papers may write it: in its one and its many ("benzodiazepines", "benzodiazepine"; "opioid", "opioids")
export function nameForms(n) {
  if (/[^a-z]/.test(n) || n.length < 5) return [n];
  return /s$/.test(n) ? (/(?:is|us|ss)$/.test(n) ? [n] : [n, n.slice(0, -1)]) : [n, n + "s"];
}
/* A short name that also stands for something else in medicine ("LSD": lysosomal storage diseases; "CBD": the common bile duct; "GHb": glycated
   haemoglobin; "DMT": disease-modifying therapy; "PCP": a pneumonia): a paper counts for it only where one of these words stands in its title or
   summary as well. (2.20, after the second trial: "is ghb the same as gbl" read a meta-analysis on diabetes.) */
const FIND_CTX = { lsd: "lysergic psychedelic psychedelics hallucinogen hallucinogens hallucinogenic", dmt: "dimethyltryptamine psychedelic psychedelics ayahuasca hallucinogen hallucinogens tryptamine", pcp: "phencyclidine",
  ghb: "hydroxybutyrate hydroxybutyric gbl butyrolactone oxybate", gbl: "butyrolactone ghb hydroxybutyrate", cbd: "cannabidiol cannabis cannabinoid cannabinoids", thc: "tetrahydrocannabinol cannabis cannabinoid cannabinoids",
  mda: "methylenedioxyamphetamine mdma ecstasy", dxm: "dextromethorphan", mxe: "methoxetamine", bzp: "benzylpiperazine", pma: "ecstasy mdma amphetamine", dph: "diphenhydramine", ket: "ketamine", meth: "methamphetamine", coke: "cocaine",
  crack: "cocaine", speed: "amphetamine amphetamines", ice: "methamphetamine", molly: "mdma ecstasy", acid: "lsd lysergic", weed: "cannabis marijuana", pot: "cannabis marijuana", spice: "cannabinoid cannabinoids",
  // (2.21.2, after the twelfth trial: "is addiction genetic" read a paper on the "oncogene addiction" of tumours; "does trauma lead to addiction" read one on food addiction)
  addiction: "drug drugs substance substances alcohol opioid opioids nicotine cocaine heroin cannabis dependence",
  salvia: "salvinorin divinorum", benzos: "benzodiazepine benzodiazepines", benzo: "benzodiazepine benzodiazepines", shrooms: "psilocybin psilocybe", mushrooms: "psilocybin psilocybe", poppers: "nitrite nitrites", ecstasy: "mdma methylenedioxymethamphetamine", nos: "nitrous",
  // (2.26.4; the senior author, 20 November 2026, 00:59: "it confused nitrous oxide with the nitrogen on earth": a question on laughing gas and nerve damage got papers on
  // the nitrogen cycle, nitrate in seawater and bacteria in soils) nitrous oxide is also a gas of the atmosphere and of soils: a paper counts only where it is about its use
  // as a drug or its harm to people (trial 16: with the words of anaesthesia, operating-room air and hospital gas pipes came in, and trials of anaesthesia for "is nos bad for you")
  "nitrous oxide": "recreational misuse abuse abusers inhalant inhalants neuropathy myelopathy myeloneuropathy neurological neurologic cobalamin b12 whippets nangs balloons laughing intoxication",
  nitrous: "recreational misuse abuse abusers inhalant inhalants neuropathy myelopathy myeloneuropathy neurological neurologic cobalamin b12 whippets nangs balloons laughing intoxication" };
/* What Europe PMC is asked (its own search words). groups: the question's key words, each an array of the ways it is said. Every key word must
   stand in a paper, not any one of them; the drug's name must stand in the paper's title, except in the widest search. */
const LOOSE_GENERIC = /^(?:adverse|adverse effects?|harmful|harms?|risks?|risky|effects?|side effects?|safety|safe|dangers?|dangerous|toxicity|toxic|health|bad)$/i;
export function findQueries(names, groups) {
  const any = ts => "(" + ts.map(t => `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")";
  const one = (n, inTitle) => { const fs = nameForms(n), core = inTitle ? (fs.length > 1 ? "(" + fs.map(f => `TITLE:"${f}"`).join(" OR ") + ")" : `TITLE:"${fs[0]}"`) : any(fs), ctx = FIND_CTX[n]; return ctx ? "(" + core + " AND " + any(ctx.split(" ")) + ")" : core; };
  const nm = inTitle => "(" + names.map(n => one(n, inTitle)).join(" OR ") + ")";
  const gs = (groups || []).map(g => [...new Set((Array.isArray(g) ? g : [g]).flatMap(findForms))]).filter(g => g.length);
  const key = inTitle => gs.map(g => " AND (" + g.map(t => inTitle ? `TITLE:"${t}"` : `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")").join("");
  const tail = ' AND LANG:eng NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"';
  const rev = '(PUB_TYPE:"review" OR PUB_TYPE:"systematic review" OR PUB_TYPE:"meta-analysis")';
  const kT = key(true).replace(/^ AND /, ""), kA = key(false).replace(/^ AND /, "");
  return { cited: nm(true) + (gs.length ? " AND ((" + kT + ") OR (" + kA + " AND " + rev + "))" : "") + tail,   // the drug in the title, and: every key word in the title too, or a review that holds every key word (asked for the most cited)
    onTitle: nm(true) + key(true) + tail,                                          // the drug and every key word in the very title (asked for the newest)
    wide: gs.length ? nm(false) + key(false) + tail : "",                          // the drug and every key word anywhere in title or summary (only where those found fewer than three)
    // any one key word (only where the others found fewer than three); (2.28.1, trial 18) not a word that stands in nearly every paper on a drug ("adverse",
    // "harmful", "risk", "effects"): with it, "can laughing gas canisters contain anything harmful" got papers on sedating children and on anaesthesia
    loose: gs.length > 1 ? nm(false) + " AND " + any([...new Set((gs.filter(g => !g.every(t => LOOSE_GENERIC.test(t))).length ? gs.filter(g => !g.every(t => LOOSE_GENERIC.test(t))) : gs).flat())]) + tail : "",
    genRev: gs.length ? nm(true) + key(false) + " AND " + rev + tail : "",          // (2.21) reviews with the subject in the title that hold every key word (a question that names no single drug)
    nameRev: nm(true) + " AND " + rev + tail,                                      // reviews of the drug itself (only where the others found fewer than two)
    anyTitle: nm(true) + tail };                                                   // without key words: the drug in the title, in Europe PMC's own order (what is there when the most cited are slow)
}
export function findPaper(r) {
  if (!r || typeof r !== "object") return null;
  const t = clean(unEnt(String(r.title || "").replace(/<[^>]+>/g, "")).replace(/<[^>]+>/g, "")).replace(/\.$/, "").slice(0, 300); if (t.length < 8) return null;   // (2.28.7) a tag written as entities ("&lt;b&gt;") is a tag too, once read: trial 21 showed "<b>Dose-dependent effects ..." as a title
  const types = String(r.pubType || (r.pubTypeList && r.pubTypeList.pubType ? [].concat(r.pubTypeList.pubType).join("; ") : "")).toLowerCase();
  const doi = /^10\.\d{4,9}\/[^\s"<>]{1,200}$/.test(String(r.doi || "")) ? String(r.doi) : "", pmid = /^\d{1,9}$/.test(String(r.pmid || "")) ? String(r.pmid) : "";
  if (!doi && !pmid) return null;
  return { t, a: clean(r.authorString || "").slice(0, 120), j: clean(r.journalTitle || (r.journalInfo && r.journalInfo.journal && r.journalInfo.journal.title) || "").slice(0, 120), y: /^(19|20)\d\d$/.test(String(r.pubYear || "")) ? String(r.pubYear) : "",
    doi, pmid, oa: r.isOpenAccess === "Y", kind: /meta-analysis|systematic review/.test(types) ? "Review of studies" : /review/.test(types) ? "Review" : /randomized controlled trial|clinical trial/.test(types) ? "Trial" : /case reports/.test(types) ? "Case report" : "Study" };
}
// ---- a paper's summary, read by rule
const iaFlat = s => clean(String(s == null ? "" : s).replace(/<[^>]+>/g, " ")).toLowerCase().replace(/[‘’‚′`]/g, "'").replace(/[“”„″]/g, '"').replace(/[‐-―−]/g, "-").replace(/\s+/g, " ");
// (a sentence is not cut after "vs.", "e.g.", "et al." or a single letter: cut there, a "no" could fall into another piece than the words it governs)
const IA_ABBR = /(?:^|[\s(])(?:e\.g|i\.e|vs|et al|approx|fig|figs|dr|mr|mrs|ms|prof|no|nos|vol|ca|cf|resp|incl|st|jr|sr|inc|ltd|u\.s|u\.k|[a-z])\.$/i;
export const iaSents = text => { const out = []; for (const p of String(text || "").split(/(?<=[.!?])\s+(?=[A-Z0-9(\["'“])/)) { if (out.length && IA_ABBR.test(out[out.length - 1])) out[out.length - 1] += " " + p; else out.push(p); } return out.map(s => s.trim()).filter(Boolean); };
// the part of a summary a label stands for: b background, a aim, m how it was done, r results, c conclusions; "" where the words are no label
const secOf = l => { l = String(l).toLowerCase(); if (l.split(/\s+/).length > 6) return "";
  return /ethnopharmacolog|background|introduction|context|^importance|rationale/.test(l) ? "b" : /objective|aim|purpose|goal|hypothes|question|areas covered|scope/.test(l) ? "a"
    : /result|finding/.test(l) && /method/.test(l) ? "r" : /main outcome|outcome measure|measure|method|design|setting|participant|patient|subject|intervention|procedure|source|selection|extraction|search|criteria|exposure|statistic|analysis|registration|funding|keyword|eligib|collection|material/.test(l) ? "m"
    : /conclusion|interpretation|implication|discussion|summary|significance|relevance|meaning|take-?home|key message|opinion/.test(l) ? "c" : /result|finding|outcome|observation|synthesis|case/.test(l) ? "r" : ""; };
/* A summary as its sentences, each with the part of the summary it stands in (from the labels some summaries carry: "<h4>Results</h4>",
   "CONCLUSIONS: ..."); the label itself is not part of a sentence. */
export function iaParts(raw) {
  const t = clean(unEnt(String(raw || "").slice(0, 9000).replace(/<h4[^>]*>\s*([^<]{1,80}?)\s*:?\s*<\/h4>/gi, (m, l) => " \u27E6" + l + "\u27E7 ").replace(/<[^>]+>/g, " "))).replace(/\s*\(ABSTRACT TRUNCATED[^)]*\)/gi, "");
  const out = []; let sec = "";
  for (const seg of t.split(/(?=\u27E6)/)) {
    let body = seg; const m = seg.match(/^\u27E6([^\u27E7]{1,80})\u27E7\s*/); if (m) { sec = secOf(m[1]); body = seg.slice(m[0].length); }
    for (let s of iaSents(body)) { const lm = s.match(/^([A-Z][A-Za-z /&,'’-]{2,60}):\s+(?=[A-Z0-9"'“(])/), ls = lm ? secOf(lm[1]) : "";
      if (ls) { sec = ls; s = s.slice(lm[0].length); }
      if (s.length > 12) out.push({ s, sec }); }
  }
  return out;
}
const IA_AMOUNT_UNIT = /^(?:mg|mcg|µg|μg|ug|g|kg|ml|iu|units?|milligrams?|micrograms?|grams?)$/;
const IA_ANIMAL = /\b(?:rats?|mice|mouse|rodents?|zebrafish|in vitro|ex vivo|in silico|cell lines?|cultured (?:cells|neurons)|cell cultures?|animals?|murine|pre-?clinical|horses?|equine|dogs?|canine|cats?|feline|pigs?|porcine|monkeys?|macaques?|primates?|rabbits?|sheep|hamsters?|guinea pigs?|drosophila|flies|worms?|elegans|veterinary|larvae|embryos?|organoids?|chicks?|chickens?|birds?|avian|pigeons?|frogs?|xenopus|oocytes?|synaptosom\w*|homogenates?|brain slices|transfected|transgenic|knockout|wild-type|vesicles)\b/i;
const IA_PEOPLE = /\b(?:participants?|patients?|volunteers?|humans?|men|women|adults?|people|subjects|students|respondents|users|individuals|persons|adolescents|outpatients|inpatients)\b/i;
// people for certain: "subjects", "individuals" and "adults" may be rats ("... in naive individuals", of a study in rats; "adult rats")
const IA_SURE = /\b(?:participants?|patients?|volunteers?|humans?|men|women|people|persons|students|respondents|outpatients|inpatients|users|consumers|smokers|drinkers|veterans|workers|clinical|placebo|double-blind)\b/i;
// a key word of a question, and the beginnings of the words papers use for the same thing
const IA_NEAR = { addiction: "addict dependence dependency dependent misuse abuse withdrawal craving", addictive: "addict dependence dependency dependent misuse abuse withdrawal craving", depression: "depress antidepress", anxiety: "anxi panic",
  sleep: "sleep insomn somnolen wakeful", appetite: "appetit hunger hungry feeding orexigen", hungry: "appetit hunger hungry feeding orexigen", memory: "memor amnes recall cognit", attention: "attenti concentrat vigilan cognit",
  concentrate: "attenti concentrat vigilan cognit", cognitive: "cognit memor attenti", pain: "pain analges nocicept", psychoactive: "psychoactiv intoxic euphor hallucin psychotrop", adverse: "advers harm risk toxic",
  serotonin: "seroton 5-ht 5ht", dopamine: "dopamin", cardiac: "cardi heart myocard arrhythm", heart: "cardi heart myocard arrhythm", hepatic: "hepat liver", liver: "hepat liver", renal: "renal kidney nephro", kidney: "renal kidney nephro",
  kidneys: "renal kidney nephro", pulmonary: "pulmon lung respirat", lung: "pulmon lung respirat", lungs: "pulmon lung respirat", epistaxis: "epistax nosebleed", nosebleeds: "epistax nosebleed", psychosis: "psychos psychot schizophren",
  personality: "personalit trait", fatigue: "fatigu tired", paranoia: "paranoi", sexual: "sexual libido erectile", dental: "dental teeth tooth bruxism caries", tremor: "tremor shak", sweating: "sweat hyperhidro diaphore",
  vomiting: "vomit emesis emetic nausea", academic: "academ scholast exam grade learning", students: "student academ" };
const iaStem = f => (f.length > 8 ? f.slice(0, f.length - 2) : f.length > 5 ? f.slice(0, f.length - 1) : f);
export const iaNearStems = w => (IA_NEAR[w] ? IA_NEAR[w].split(" ") : [...new Set(findForms(w).map(iaStem))]);
// a sentence about what the paper set out to do, or how it was done: not one that says what it found
const IA_AIM = /\b(?:aims?|aimed|objectives?|purpose|goal) (?:of|was|were|is|are|to)\b|\bwe (?:aimed|sought|set out|hypothesi[sz]ed)\b|\b(?:this|the present|the current|our) (?:study|paper|article|review|report|trial|work|chapter|analysis|survey|meta-analysis|systematic review|scoping review|narrative review) (?:might|may|could|should|aim|seek|sought|investigat|examin|explor|assess|evaluat|review|summari|describ|discuss|present|provid|focus|address|compar|test|was designed|is intended|will|outlin|synthesi|collat|map)\w*|\bto (?:determine|investigate|examine|assess|evaluate|explore|test|compare|characteri[sz]e|describe|review|summari[sz]e|identify|study|establish|clarify|elucidate) (?:whether|if|the|how|a|an)\b|\b(?:was|were) to\b|\bwe (?:also |then |further |first |next |finally |here |therefore |thus |now |briefly )?(?:investigated|examined|explored|assessed|evaluated|tested|studied|conducted|performed|reviewed|searched|surveyed|recruited|measured|compared|analy[sz]ed|estimated|genotyped|sequenced|calculated|computed|quantified|collected|obtained|applied|employed|randomi[sz]ed|assigned|administered|enrolled|included|excluded|selected|screened|interviewed|used|describe|present|discuss|summari[sz]e|review|outline|highlight|report (?:a|an|the|on|two|three|four|\d))\b/i;
const IA_HOW = /\b(?:manuscript|erratum|corrigendum|correction to|retract\w*|editors?|reviewers?|published online|interprofessional|this activity|continuing education)\b|\b(?:has|have) been (?:conducted|performed|reviewed|searched|summari[sz]ed|described|discussed|undertaken|carried out|collated|compiled)\b|\b(?:is|are) (?:also |then |further |briefly )?(?:reviewed|discussed|described|summari[sz]ed|presented|outlined|provided|highlighted|considered|addressed|explored)\b|\b(?:were|was) (?:also |then |subsequently |additionally )?(?:undertaken|carried out|genotyped|recruited|enrolled|randomi[sz]ed|randomly|assigned|allocated|administered|collected|measured|assessed|evaluated|analy[sz]ed|performed|conducted|searched|included|extracted|screened|obtained|recorded|interviewed|surveyed|asked|quantified|monitored|calculated)\b|\bparticipants (?:completed|received|underwent)\b|\b(?:pubmed|medline|embase|scopus|web of science|psycinfo|cochrane (?:library|central)|prisma|prospero|clinicaltrials\.gov|inclusion criteria|exclusion criteria|search strateg\w*|trial registration|funded by|copyright|all rights reserved)\b/i;
const IA_FOUND = /\b(?:found|show(?:s|ed|n)?|demonstrat\w*|reveal\w*|indicat\w*|suggest\w*|observ\w*|associat\w*|correlat\w*|linked|reduc\w*|increas\w*|decreas\w*|improv\w*|impair\w*|attenuat\w*|alleviat\w*|ameliorat\w*|worsen\w*|higher|lower|greater|fewer|significan\w*|conclud\w*|support\w*|confirm\w*|evidence|did not|does not|no (?:significant )?(?:difference|effect|evidence|association|change)s?|leads? to|led to|results? in|resulted in|caus\w*|produc\w*|induc\w*|yield\w*|prevent\w*|predict\w*|alter\w*|escalat\w*)\b/i;
// the drug, said without its name: "the extract", "this compound", "its use". (Never a bare "use" or "treatment": "Chronic METH use was ..." in a paper on MDMA
// and methamphetamine is about the other drug, and "His epistaxis was successfully treated" about a patient.)
const IA_REFERS = /\b(?:the|this|these|its|their|such) (?:[a-z-]+ )?(?:extracts?|drugs?|compounds?|substances?|plants?|herbs?|medications?|medicines?|supplements?)\b|\b(?:its|their) (?:[a-z-]+ )?(?:use|users?|consumption|intake|administration|ingestion|effects?)\b|\b(?:regular|chronic|long-term|short-term|heavy|daily|frequent|recreational|occasional|acute|repeated|prolonged|excessive|habitual|non-medical|illicit|continued|sustained|problematic) (?:use|users?|consumption|intake|administration|exposure)\b|^(?:use|users|consumption|intake|administration|exposure|withdrawal|dependence) /;
// a sentence that asks for more research, or says what something "will" bring, does not say what was found: not taken
// (after the sixth trial: "Research on ... may be warranted", "Clinical trials of ... are pending", "... understanding the impact on cognition is critical",
// "findings highlight potential intervention targets": what should be done or looked at next, not what was found)
const IA_MORE = /\b(?:further|more|future|additional|larger|longer) (?:\w+ ){0,2}(?:research|studies|study|work|trials?|investigations?|evidence|data)\b|\b(?:is|are|remains?|be) (?:needed|warranted|required|necessary|pending|ongoing|underway|planned)\b|\bwarrant(?:s|ed)?\b|\b(?:is|are|remains?) (?:critical|crucial|essential|vital|imperative|important)\b(?! (?:for|in) )|\bwill (?:be|help|provide|allow|enable|require|need)\b|\bto be (?:determined|established|elucidated|clarified|confirmed)\b|\b(?:highlight|underscore|underline|emphasi[sz]e|stress)(?:s|es|d|ed)? (?:the |a |an )?(?:\w+ )?(?:need|importance|necessity|urgency|potential)\b|\b(?:intervention|prevention|therapeutic|treatment) (?:targets?|strateg\w+|efforts?)\b|\b(?:implications?|recommendations?) for\b/i;
/* Words on which a sentence turns. Left out of the words that are shown, they would let those words say more than their sentence does, or its
   opposite. */
const IA_T_NEG = /^(?:no|not|never|without|neither|nor|none|lack\w*|fail\w*|absen\w*|cannot|unable|unlikely|\w+n't|non-?[a-z-]+|insignificant\w*|ineffective\w*|insufficient\w*|unsupported|unproven|unfounded|unchanged|unaffected|little|few|weak|rarely|seldom|hardly|scarcely|only|solely|contrary|refut\w*|disprov\w*|contradict\w*|doubt\w*|myths?|false|falsely|incorrect\w*|misconception\w*)$/;
const IA_T_ASK = /^(?:whether|if|unclear|unknown|uncertain|hypothes\w*|aim\w*|objectives?|purpose|investigat\w*|examin\w*|assess\w*|evaluat\w*|explor\w*|determin\w*|tested|testing|questions?|debat\w*|controvers\w*|remains?|remained|summari[sz]\w*|discuss\w*|describ\w*|overview|outlin\w*|conducted|performed|undertaken|searched|focus\w*|address\w*)$/;
const IA_T_SAID = /^(?:claim\w*|believ\w*|thought|purport\w*|alleg\w*|anecdot\w*|reputed\w*|tradition\w*|market\w*|advertis\w*|promot\w*|said|supposed\w*|so-called|popular\w*|folk|rumou?r\w*|perceiv\w*|expect\w*|assum\w*|presum\w*|speculat\w*|theor\w*|propos\w*|postulat\w*)$/;
const IA_T_DES = /^(?:case|cases|case-?reports?|case-?series|survey\w*|self-?report\w*|questionnaires?|interviews?|retrospective\w*|observational|uncontrolled|open-?label|pilot|exploratory|cross-?sectional|qualitative|simulat\w*|model+ing)$/;
const IA_T_MAY = /^(?:may|might|could|suggest\w*|appear\w*|seem\w*|possibl\w*|potential\w*|preliminary|limited|likely|tend\w*|inconclusive|mixed|inconsistent)$/;
const IA_T_BUT = /^(?:but|however|although|though|except|unless|despite|nevertheless|nonetheless)$/;
// a word of the paper that is never shown. NEVER: an amount or timing, taking drugs together, making an effect stronger (with FIND_HELD: dying and what waits for
  // a person): a sentence that holds one is not shown at all. SOFT: advice, or a promise of safety: the shown words go around it.
const IA_W_NEVER = /^(?:potentiat\w*|synerg\w*|co-?administ\w*|co-?use\w*|co-?ingest\w*|concurrent\w*|concomitant\w*|simultaneous\w*|polydrug|combination|combinations|mixture|mixtures|redos\w*|dos(?:e|es|age|ages|ing|ed))$/;
const IA_W_SOFT = /^(?:should|must|ought|recommend\w*|advis\w*|avoid\w*|abstain\w*|refrain\w*|safe|safely|safer|safest|safety|harmless|well-tolerated|tolerab\w*|tolerated)$/;
const IA_W_ROUTE = /^(?:oral\w*|smok\w*|inject\w*|snort\w*|intranasal\w*|insufflat\w*|intraven\w*|sublingual\w*|rectal\w*|vap\w*|edibles?|eaten|eating|swallow\w*|chew\w*|inhal\w*)$/, IA_W_THAN = /^(?:than|compared|versus|vs|faster|slower|quicker|bioavailab\w*|onset|peak)$/;
// words that only lead in to what a sentence says: a run of words may begin after them
const IA_W_LIGHT = /^(?:we|it|they|there|this|these|those|the|our|a|an|in|conclusion|conclusions|summary|overall|thus|therefore|hence|together|taken|altogether|collectively|finally|moreover|furthermore|additionally|also|however|results?|findings?|data|study|studies|analysis|analyses|evidence|authors?|present|current|here|research|generally|largely|mostly|broadly|consistently|was|were|is|are|has|have|been|found|show(?:s|ed|n)?|indicat(?:e|es|ed)|demonstrat(?:e|es|ed)|conclud(?:e|es|ed)|report(?:s|ed)?|observ(?:e|ed)|reveal(?:s|ed)?|provid(?:e|es|ed)|support(?:s|ed)?|confirm(?:s|ed)?|that|of|for|to|some|further|strong|clear|new|first|direct|good|initial|growing|increasing|accumulating|emerging|converging|consistent|compelling|robust|substantial|considerable|ample)$/;
const IA_W_HANG = /^(?:the|a|an|of|in|on|at|to|for|by|with|and|or|but|that|which|who|whose|as|than|from|into|onto|upon|over|under|between|among|across|during|after|before|about|against|within|through|via|per|versus|vs|when|where|while|because|since|its|their|this|these|those|is|are|was|were|be|been|has|have|had|not|no|more|less|very|both|any|some|all|each|every|many|most|several|other|another|such|same|certain|various|either|neither|two|three|four|five|six)$/, IA_W_LAME = /^(?:of|and|or|but|than|that|which|who|whose|as|to|is|are|was|were)$/;
// the paper itself and the people or animals it studied ("this study", "these patients", "in this sample"); other things a "this" may stand before without
// pointing at another sentence ("this drug", "at this time"); what may follow a "this" that is the subject ("This suggests that ...", "those who ...")
const IA_W_SELF = /^(?:study|studies|trial|trials|review|reviews|analysis|analyses|reanalysis|meta-analysis|sample|samples|cohort|cohorts|survey|surveys|series|report|reports|paper|article|experiment|experiments|investigation|work|research|literature|case|cases|population|populations|data|dataset|findings|results|observations|evidence|group|groups|setting)$/;
const IA_W_THING = /^(?:drug|drugs|compound|compounds|substance|substances|plant|plants|herb|herbs|extract|extracts|medication|medications|medicine|medicines|agent|agents|class|kind|type|time|point|stage|age)$/;
const IA_W_AFTER_THIS = /^(?:with|who|whose|that|which|of|is|are|was|were|may|might|could|would|can|has|have|had|suggests?|suggested|indicates?|indicated|shows?|showed|demonstrates?|demonstrated|supports?|supported|confirms?|confirmed|implies|imply|means?|provides?|provided|highlights?|reveals?|revealed|raises?|adds?|extends?|led|leads?|makes?|made)$/;
// how a part of a sentence begins that says when or of whom the rest holds ("When used daily, ...", "Among adults with ..., ..."), and words after "In", "On",
// "By" that only join sentences ("In contrast, ...", "On the other hand, ...")
const IA_W_WHEN = /^(?:when|where|under|at|unless|once|whenever|during|after|before|following|upon|until)$/, IA_W_WHOM = /^(?:in|among|amongst|for|within|across|with|by|on)$/;
const IA_W_DISC = /^(?:addition|contrast|conclusion|conclusions|summary|general|particular|fact|brief|short|total|sum|turn|parallel|essence|other|all|part|line|keeping|agreement|accordance|support|example|instance|average|contrary|balance|regard|respect|terms|view|light|comparison|closing|practice|principle|theory|reality|recent|retrospect|response)$/;
/* Which words of a sentence are shown: at most 15 in a row, holding toks[a..b] (the key word). Of all such runs, the one that reads best (from the
   start of the sentence or of a part of it, to its end; naming the drug) among those that the rules allow (points 5 and 6 above). Gives
   [first, last, how well it reads], or null where there is no such run: then nothing of the sentence is shown. opt: { stems, names } for what reads best. */
export function iaWindow(toks, a, b, opt) {
  const n = toks.length, o = opt || {}, stems = (o.stems || []).filter(s => !/\s/.test(s)), names = (o.names || []).flatMap(x => nameForms(x.split(" ")[0]));
  const low = toks.map(t => t.toLowerCase().replace(/[‐-―−]/g, "-").replace(/’/g, "'").replace(/[^a-z0-9'/-]/g, "").replace(/^['/-]+|['/-]+$/g, ""));
  const cum = f => { const c = new Array(n + 1); c[0] = 0; for (let i = 0; i < n; i++) c[i + 1] = c[i] + (f(i) ? 1 : 0); return c; }, cnt = (c, s, e) => c[e + 1] - c[s];
  const num = i => /\d/.test(toks[i]);
  const cPre = cum(i => IA_T_NEG.test(low[i]) || IA_T_ASK.test(low[i]) || IA_T_SAID.test(low[i]) || IA_T_DES.test(low[i])), cMay = cum(i => IA_T_MAY.test(low[i])), cPost = cum(i => IA_T_NEG.test(low[i]) || IA_T_BUT.test(low[i])), cAsk = cum(i => IA_T_ASK.test(low[i]));
  const nb = new Array(n + 1); nb[n] = n; for (let i = n - 1; i >= 0; i--) nb[i] = /[,;]$/.test(toks[i]) ? i : nb[i + 1];   // the next word that ends a part of the sentence
  // never: an amount or timing, dying and what waits for a person, taking drugs together or making an effect stronger. Such a word often carries the
  // condition or the people a finding is about ("at high doses", "in children", "together with alcohol"): cut around it, the rest would say more than
  // the sentence. So a sentence that holds one, or compares ways of taking, is not shown at all.
  const never = i => IA_W_NEVER.test(low[i]) || FIND_HELD.test(low[i]) || /dos(?:e|age|ing)/.test(low[i]) || /\d(?:mg|mcg|µg|μg|ug|kg|ml|iu)\b/i.test(toks[i]) || (i > 0 && num(i - 1) && IA_AMOUNT_UNIT.test(low[i]))
    || /^(?:potenc(?:y|ies)|high-potency|low-potency|(?:high|low)-(?:thc|cbd)|(?:thc|cbd)-rich)$/.test(low[i]) || (/^(?:high|low|rich|higher|lower|richer)$/.test(low[i]) && low[i + 1] === "in")   // (how strong a product is: an amount in other words. "cannabis high in cannabidiol")
    || (/^(?:combin\w*|mix\w*|together)$/.test(low[i]) && low[i + 1] === "with") || (low[i] === "every" && i + 2 < n && num(i + 1) && /^(?:minutes?|hours?)$/.test(low[i + 2]));
  let route = false, than = false; for (let i = 0; i < n; i++) { if (never(i)) return null; if (IA_W_ROUTE.test(low[i])) route = true; if (IA_W_THAN.test(low[i])) than = true; }
  if (route && than) return null;
  // (numbers in brackets are statistics, "(SMD 0.5; 95% CI 0.1 to 0.9)", "(76.9%)": gone around like those in signs. A name is not: "(2C-B)", "(5-HT)")
  const stat = new Array(n).fill(false); for (let i = 0; i < n; i++) { if (!/^[(\[]/.test(toks[i])) continue; let d = 0, j = i; for (; j < n; j++) { for (const ch of toks[j]) { if (ch === "(" || ch === "[") d++; else if (ch === ")" || ch === "]") d--; } if (d <= 0) break; }
    j = Math.min(j, n - 1); let numeric = false; for (let k = i; k <= j; k++) if (/^[(\[]?[\d.,]+%?[)\];,.]*$/.test(toks[k])) numeric = true; if (numeric) for (let k = i; k <= j; k++) stat[k] = true; i = j; }
  const cBad = cum(i => IA_W_SOFT.test(low[i]) || stat[i] || /https?:|www\.|\S@\S|[=<>±~]/i.test(toks[i]));   // (advice or a promise of safety, a link, statistics in signs or in brackets: the shown words go around them)
  // (after the sixth trial: "In this context caffeine has been shown to increase anxiety", "... may be susceptible to these positive effects") Words that point
  // back to another sentence ("these effects", "this context", "such cases") are not shown: what they point to is not there. Not meant: "this study", "these
  // patients", "this drug", "those who ...", and a "This suggests that ...", after which a run may begin.
  const cBack = cum(i => /^(?:this|these|those|such)$/.test(low[i]) && !(low[i] === "such" && low[i + 1] === "as") && !IA_W_AFTER_THIS.test(low[i + 1] || "")
    && ![1, 2, 3].some(k => i + k < n && (IA_W_SELF.test(low[i + k]) || IA_W_THING.test(low[i + k]) || IA_PEOPLE.test(low[i + k]) || IA_SURE.test(low[i + k]) || IA_ANIMAL.test(low[i + k])) && !toks.slice(i + 1, i + k).some(t => /[,;:.]$/.test(t))));
  const cOpen = cum(i => /[(\[]/.test(toks[i])), cClose = cum(i => /[)\]]/.test(toks[i])), many = i => (toks[i].match(/[(\[]/g) || []).length !== (toks[i].match(/[)\]]/g) || []).length;
  const cUneven = cum(i => many(i)), paren = (s, e) => { let d = 0; for (let i = s; i <= e; i++) { for (const ch of toks[i]) { if (ch === "(" || ch === "[") d++; else if (ch === ")" || ch === "]") { d--; if (d < 0) return false; } } } return d === 0; };
  // (a word that most likely says what happened: "reduced", "was", "may", "did"; a run of words without one is a piece of a sentence, not a finding)
  const cVerb = cum(i => /^(?:is|are|was|were|be|been|has|have|had|did|does|do|may|might|can|could|will|would|found|shows?|shown|suggests?|indicates?|reveals?|reports?|links?|leads?|led|results?|yields?|prevents?|predicts?|alters?|affects?|remains?|appears?|seems?|occurs?|differs?|rose|fell|lowers?|exerts?|supports?|confirms?|persists?|develops?|reduces?|increases?|decreases?|improves?|impairs?|causes?|produces?|induces?|changes?|raises?|declines?|drops?|falls?|rises?|lasts?|acts?|binds?|blocks?|releases?|depletes?|damages?|protects?|worsens?|eases?|relieves?|triggers?|poses?|plays?|carr(?:y|ies)|helps?|works?|makes?|gives?|takes?|provides?|exhibits?|displays?|possess(?:es)?|represents?|contributes?|mediates?|modulates?|enhances?|inhibits?|activates?|stimulates?|elevates?|disrupts?|promotes?|exacerbates?|mitigates?|facilitates?|[a-z]{3,}ed)$/.test(low[i]));
  const cKey = cum(i => { const parts = low[i].split(/[-/]/); return stems.some(st => (st.includes("-") ? low[i].startsWith(st) : parts.some(p => p.startsWith(st)))); }), cName = cum(i => { const x = low[i].replace(/'s$/, ""); return names.includes(x) || x.split(/[-/]/).some(p => names.includes(p)); });   // ("MDMA-assisted", "caffeine-containing": the name in a joined word)
  // where the sentence says the drug without its name: [where that begins, its noun] ("the extract", "this compound", "its use", "regular consumption"; "Use ..." at the start)
  const refs = []; for (let i = 0; i < n; i++) { const p1 = low[i - 1] || "", p2 = low[i - 2] || "", det = /^(?:the|this|these|its|their|such)$/, own = /^(?:its|their)$/;
    if (/^(?:extracts?|drugs?|compounds?|substances?|plants?|herbs?|medications?|medicines?|supplements?)$/.test(low[i])) { if (det.test(p1)) refs.push([i - 1, i]); else if (det.test(p2)) refs.push([i - 2, i]); }
    else if (/^(?:use|users?|consumption|intake|administration|ingestion|exposure|effects?)$/.test(low[i])) { if (own.test(p1)) refs.push([i - 1, i]); else if (own.test(p2)) refs.push([i - 2, i]);
      else if (low[i] !== "effects" && low[i] !== "effect" && (i === 0 || /^(?:regular|chronic|long-term|short-term|heavy|daily|frequent|recreational|occasional|acute|repeated|prolonged|excessive|habitual|non-medical|illicit|continued|sustained|problematic)$/.test(p1))) refs.push([Math.max(0, i - 1), i]); }
    else if (i === 0 && /^(?:withdrawal|dependence)$/.test(low[i])) refs.push([0, 0]); }
  // a clause that opens the sentence with "Although ..." does not govern what follows its comma
  let free = -1; if (/^(?:although|though|while|whereas|despite|notwithstanding)$/.test(low[0]) || (low[0] === "even" && low[1] === "though")) { for (let i = 1; i < n - 1; i++) if (/,$/.test(toks[i])) { free = i; break; } }
  const edgeAt = i => i >= 0 && i < n && (/[,;:]$/.test(toks[i]) || low[i] === "that" || (i > 0 && /[,;:]$/.test(toks[i - 1]) && (low[i] === "but" || (/^(?:and|or)$/.test(low[i]) && /^(?:the|this|these|those|it|they|there|we|he|she|its|their|a|an|no)$/.test(low[i + 1] || "")))));   // a part of the sentence ends with this word (", and the colour ..." begins a new part; ", and anxiety symptoms" is the last of a list; a closing bracket ends no part: "... in the catechol-O-methyltransferase (COMT) | gene moderated ...")
  /* (2.20, after the third trial) Whole parts of the sentence only. The run ENDS where the sentence ends or a part of it does (a comma, a semicolon, a closing
     bracket; before an opening one): "... revealed subjective anxiety levels | to be significantly lower" was shown without its last words and said nothing.
     It BEGINS where the sentence or a part of it begins; or after words that only lead in ("We found | no evidence that ...", "there was | no ..."): cut
     after anything else, the words would lose whom or what they are about ("Carriers of the allele were | most likely to ... if they used cannabis"). */
  const startOk = new Array(n).fill(false), partOf = new Array(n).fill(0); { let c = 0, light = true;
    for (let i = 0; i < n; i++) { if (i === 0 || edgeAt(i - 1)) { c = i; light = true; } partOf[i] = c; startOk[i] = i === c || light; if (!IA_W_LIGHT.test(low[i]) && !IA_ANIMAL.test(low[i])) light = false; } }   // (a word for animals or cells may be left before the run: the line itself then says "in animals or cells")
  // where a run may end before the sentence does: at a comma, semicolon or closing bracket after which the sentence only adds something (", with ...", ", which ...",
  // ", suggesting ...", "(p ..."), not where what follows is still needed ("Anxiety, which had been rated weekly, | fell ..."; a list: "anxiety, | depression and stress")
  // (after the seventh trial: "Negative changes in physical activity, sleep, | smoking and alcohol intake were ..." was cut inside a list: "smoking" is no "suggesting")
  const addsWord = i => /^(?:with|while|whereas|which|who|where|when|consistent|compared|particularly|especially|including|further|thereby|thus|possibly|probably|likely|as|although|though|but|however|suggesting|indicating|demonstrating|showing|supporting|implying|highlighting|leading|resulting|reflecting|confirming|revealing|providing|raising|making|causing|producing|allowing|representing|accounting|ranging|underscoring|pointing|contributing)$/.test(low[i])
    || /^(?:regardless|irrespective|independent|independently)$/.test(low[i])
    || (/^(?:and|or)$/.test(low[i]) && (/^(?:the|this|these|those|it|they|there|we|its|their|no|a|an)$/.test(low[i + 1] || "")
      // (", and reduced the sleep shifts", ", and treatment is ...", ", and chlorogenic acid reversed ...", ", and support the view that ...": a second thing found, or a new clause)
      || [1, 2, 3].some(k => /^(?:is|are|was|were|has|have|had|did|does|may|might|can|could|will|would|remains?|remained|suggests?|indicates?|shows?|demonstrates?|supports?|confirms?|reveals?|provides?|highlights?|implies|imply|[a-z]{4,}ed)$/.test(low[i + k] || "") && !toks.slice(i + 1, i + k).some(t => /[,;:]$/.test(t)))));
  // (after the sixth trial: "... accounting for 40/52 | (76.9%) of cases", "... number needed to treat | (NNT) of 3") What stands in brackets only adds where the
  // sentence ends after the brackets, or a part of it does, or what follows them adds itself
  const closeAt = k => { let d = 0; for (let j = k; j < n; j++) { for (const ch of toks[j]) { if (ch === "(" || ch === "[") d++; else if (ch === ")" || ch === "]") d--; } if (d <= 0) return j; } return n - 1; };
  const adds = i => i < n && (/^[(\[]/.test(toks[i]) ? (j => j >= n - 1 || /[,;:.]$/.test(toks[j]) || adds(j + 1))(closeAt(i)) : addsWord(i));
  const endOk = e => e === n - 1 || o.head || ((/[,;:]$/.test(toks[e]) || (/[)\]]$/.test(toks[e]) && !/[(\[]/.test(toks[e])) || /^[(\[]/.test(toks[e + 1])) && adds(e + 1));   // (o.head: for what a drug is, the head of the sentence is enough)
  /* (after the sixth trial: "... that among adults with treatment-resistant depression, | ketamine can produce rapid ... antidepressant effects") The part before
     the run may say of whom or when the sentence holds: "Among adults with ..., ...", "When used daily, ...", "During withdrawal, ...". Cut after it, the words
     would say it of everyone, always. So a run does not begin after such a part (it may begin with it). Not meant: the study itself ("In this randomized trial
     of sixty adults, ...": the paper's title and kind say that); "In rats, ..." (the line's own mark says it); "In contrast, ..."; "After the drug, ..." (the
     drug itself is what the question is about); and "Although ...,". */
  const scopeAt = (k, e) => { if (k > e || !(IA_W_WHEN.test(low[k]) || IA_W_WHOM.test(low[k]))) return false; const rest = low.slice(k + 1, e + 1);
    if (rest.some(w => IA_W_SELF.test(w))) return false;
    if (rest.every(w => /^(?:the|this|a|an|its|their|of|drug|drugs|extract|compound|substance|plant|medication|administration|treatment|use|intake|ingestion|exposure|consumption)$/.test(w) || names.includes(w))) return false;   // ("After the drug, ...", "After kanna, ...": only the drug itself)
    if (rest.some(w => IA_ANIMAL.test(w)) && !rest.some(w => /^(?:with|who|whose|those)$/.test(w))) return false;
    return !(IA_W_WHOM.test(low[k]) && rest.slice(0, 2).some(w => IA_W_DISC.test(w))); };
  const scoped = s => { let e = partOf[s] - 1;
    while (e >= 0 && !/[;:]$/.test(toks[e])) { let c = e; while (c > 0 && !/[,;:]$/.test(toks[c - 1])) c--;   // the part [c..e] before the run, and the ones before it
      if (scopeAt(/^(?:and|but|or)$/.test(low[c]) ? c + 1 : c, e)) return true;
      for (let i = c; i < e; i++) if (low[i] === "that" && scopeAt(i + 1, e)) return true;   // ("We found that among adults with ..., | ...")
      e = c - 1; }
    return false; };
  const opener = /^(?:to|although|though|while|whereas|if|when|given|because|since|despite|as|in|by|with|after|before|during|for|among|across|based|using|following|considering|regarding|compared|unlike|like|notwithstanding)$/.test(low[0]);
  let first = n - 1; for (let i = 0; i < n; i++) if (/[,;:]$/.test(toks[i])) { first = i; break; }   // where the sentence's opening part ends
  let best = null, top = -1e9;
  for (let s = Math.max(0, b - 14); s <= a; s++) {
    const from = s > free ? free + 1 : 0;   // (what stands before this is not counted)
    if (!startOk[s] || cPre[s] - cPre[from] > 0 || cBad[s] > 0 || (s > 0 && (scoped(s) || cnt(cBack, partOf[s], s - 1) > 0))) continue;   // ("In this | context kanna has ...": not after words that point back)
    // (after the seventh trial: "..., and more effective than lidocaine with epinephrine, for | the prevention of epistaxis associated with nasotracheal intubation") A part
    // that begins with a preposition, after a comma, hangs on what stands before it: a run that begins inside it says nothing by itself
    if (partOf[s] > 0 && s > partOf[s] && /^(?:for|in|on|at|by|with|from|into|during|after|before|among|between|through|via|per|about|against|within|under|over|of|to|as|than|including|such)$/.test(low[partOf[s]])) continue;   // (advice or a promise of safety before them: what follows is what is advised or promised, and is not shown)
    // not with a word that hangs on what was cut ("which may also apply ...", "characterized by ...", "becoming ..."), and not with the items of a list ("..., | mood disorders, and withdrawal symptoms ...")
    if (s > 0 && (IA_W_LAME.test(low[s]) || /^(?:for|in|on|at|by|with|from|into|during|after|before|among|between|through|via|per|about|against|within|under|over)$/.test(low[s]) || (/(?:ing|ed)$/.test(low[s]) && low[s].length > 5 && !low[s].includes("-"))   // ("MDMA-assisted therapy is ..." begins with a joined word that says which therapy, not with a word that hangs)
      || (/[,;]$/.test(toks[s - 1]) && [0, 1, 2].some(k => s + k < n && /,$/.test(toks[s + k]))) || (low[s - 1] === "that" && cVerb[s + 1] - cVerb[s] > 0))) continue;   // ("affinities that | might augment ...": the words would lack what they are said of)
    const preMay = cMay[s] - cMay[from] > 0;
    for (let e = b; e <= Math.min(n - 1, s + 14); e++) {
      if (!endOk(e) || e - s < 3) continue;
      if (s === 0 && opener && e <= first && e < n - 1) continue;   // (only the part that opens the sentence, "Despite its addictive properties, ...": it leads up to what is said, and says nothing yet)
      if (cPost[n] - cPost[e + 1] > 0 || cAsk[Math.min(n, nb[e] + 1)] - cAsk[e + 1] > 0) continue;   // after them: a "no" or a "but" anywhere; a question or an aim up to the next comma (", which should be examined in ..." adds, it does not take back)
      if (cnt(cBad, s, e) > 0 || cnt(cBack, s, e) > 0 || (preMay && cnt(cMay, s, e) === 0)) continue;
      if ((cnt(cOpen, s, e) > 0 || cnt(cClose, s, e) > 0) && (cnt(cUneven, s, e) > 0 || cnt(cOpen, s, e) !== cnt(cClose, s, e)) && !paren(s, e)) continue;
      if (cnt(cVerb, s, e) === 0) continue;   // (no word that says what happened: a piece of a sentence, not a finding)
      // (after the seventh trial: "Because caffeine is an adenosine receptor antagonist, these results suggest that | some panic disorder patients may have abnormalities in
      // neuronal systems involving adenosine") The run itself names the drug or says "the extract", "its use": else it is about something else, even in a sentence that names the drug
      if (names.length && !o.head && cnt(cName, s, e) === 0 && !refs.some(([from, at]) => from >= s - 1 && at <= e)) continue;
      // what reads best: more of the sentence, from where a part of it begins, to the sentence's end above all (the last words carry what was found), with the
      // key word and the drug's name in it
      const score = (e - s + 1) + (s === 0 || edgeAt(s - 1) ? 8 : 0) + (e === n - 1 ? 10 : endOk(e) && !o.head ? 4 : 0) + (cnt(cKey, s, e) > 0 ? 5 : 0) + (cnt(cName, s, e) > 0 ? 5 : 0) - (e < n - 1 && IA_W_HANG.test(low[e]) ? 8 : 0);
      if (score >= top) { top = score; best = [s, e, score]; }   // (of two that read equally well, the later: what follows the key word is the rest of the finding)
    }
  }
  return best;
}
const iaRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
/* A paper's own words on the question, by rule: { q: the words, an: 1 where they are about animals or cells and not people, 2 where the summary
   covers both and the sentence does not say which; i, n: which sentence of how many (for the editors' trials) }, or null. p: findPaper's record
   with ab, the summary as Europe PMC gives it. groups: the question's key words; names: the drug's; def: the question asks what the drug is.
   note: for the editors' trials only, a function that is told why a paper got no words (in the rule's terms; never a word of the summary). */
export function iaPick(p, groups, names, def, note) {
  const say = typeof note === "function" ? note : () => {};
  const parts = iaParts(p && p.ab), n = parts.length; if (!n) { say("its summary is empty"); return null; }
  const forms = (names || []).flatMap(nameForms), nameRe = forms.length ? new RegExp("(?:^|[^a-z0-9])(?:" + forms.map(iaRe).join("|") + ")(?:$|[^a-z0-9])") : /$^/;
  const G = (groups || []).map(g => [...new Set(g.flatMap(iaNearStems))]).filter(s => s.length), allStems = [...new Set(G.flat())];
  if (!def && !G.length) { say("the question has no key word (only the drug's name)"); return null; }
  const has = (st, lowToks) => lowToks.some(t => (st.includes("-") ? t.startsWith(st) : t.split(/[-/]/).some(x => x.startsWith(st))));
  const lows = s => s.toLowerCase().replace(/[‐-―−]/g, "-").split(/\s+/).map(t => t.replace(/’/g, "'").replace(/[^a-z0-9'/-]/g, "").replace(/^['-]+|['-]+$/g, ""));
  const flatT = iaFlat(p.t), titleLow = lows(p.t), titleNamed = nameRe.test(flatT), flatAll = iaFlat(p.t + ". " + parts.map(x => x.s).join(" ")), pa = IA_ANIMAL.test(flatAll), pp = IA_PEOPLE.test(flatAll) || IA_SURE.test(flatAll), ta = IA_ANIMAL.test(flatT) && !IA_SURE.test(flatT);   // (ta: the title says animals or cells, and names no people)
  if (FIND_HELD.test(flatT)) { say("its title is about dying, overdose, amounts, pregnancy or children"); return null; }   // (the paper as a whole is about what waits for a person)
  const labelled = parts.some(x => x.sec), cands = [];
  const defRe = def && forms.length ? new RegExp("(?:^|[^a-z0-9])(?:" + forms.map(iaRe).join("|") + ")(?:[^a-z0-9][^.;:]{0,70}?)? (?:is|are) (?:a|an|the|one) ") : null;
  const why = { key: 0, aim: 0, early: 0, all: 0, about: 0 };
  parts.forEach((x, i) => {
    const fs = iaFlat(x.s), lt = lows(x.s), aim = IA_AIM.test(x.s) || IA_HOW.test(x.s) || /\?$/.test(x.s);
    if (def) {   // what the drug is: said at the start of a summary of a paper about it
      if (aim || !titleNamed || !defRe.test(fs) || !(x.sec === "b" || x.sec === "" ? i < Math.max(2, Math.ceil(n / 3)) : false)) return;
      cands.push({ i, x, fs, lt, score: -i });
      return;
    }
    const hit = G.filter(st => st.some(s => has(s, lt))); if (!hit.length) return;                        // it holds a key word
    why.key++;
    if (aim || IA_MORE.test(fs)) { why.aim++; return; }                                                   // it says what was found: not what was set out, how it was done, or that more research is needed
    if (!G.every(st => st.some(s => has(s, lt) || has(s, titleLow)))) { why.all++; return; }              // every key word stands in it or in the title
    const where = x.sec === "c" ? 6 : x.sec === "r" ? 4 : labelled ? -1 : i >= n - 2 ? 5 : i >= (n <= 4 ? 1 : Math.floor(n / 2)) ? 3 : -1; if (where < 0) { why.early++; return; }   // where papers say what they found (a summary of four sentences or fewer: anywhere after its first)
    // it names the drug; or the paper is about the drug (its name in the title) and the sentence says "the extract", "this compound", "its use". (After the sixth
    // trial: of twelve sentences that named neither, ten were about something else: the other drug of a comparison, a patient, a method.)
    if (!nameRe.test(fs) && !(titleNamed && IA_REFERS.test(fs))) { why.about++; return; }
    cands.push({ i, x, fs, lt, score: where + (hit.length - 1) * 3 + (IA_FOUND.test(fs) ? 2 : 0) + (nameRe.test(fs) ? 1 : 0) });
  });
  if (!cands.length) say(def ? "no sentence at its start says what the drug is" : !why.key ? "no sentence holds a key word of the question" : "of " + why.key + " sentence(s) that hold a key word: " + [why.aim && why.aim + " say what was set out or how it was done", why.early && why.early + " stand before the results", why.all && why.all + " lack another key word (and the title does too)", why.about && why.about + " do not name the drug"].filter(Boolean).join(", "));
  cands.sort((u, v) => v.score - u.score || v.i - u.i);
  for (const c of cands.slice(0, 4)) {
    const sa = IA_ANIMAL.test(c.fs), sp = IA_SURE.test(c.fs); if (sa && sp) { say("a sentence with the key word speaks of animals or cells and of people at once"); continue; }
    const toks = c.x.s.split(/\s+/), lt = c.lt, spans = []; if (lt.length !== toks.length) continue;
    if (def) { const first = forms.map(f => f.split(" ")[0]), k = lt.findIndex(t => first.includes(t) || first.includes(t.replace(/[^a-z0-9-].*$/, ""))); if (k >= 0) spans.push([k, k, 0]); }
    else { const firsts = []; for (const st of G) { const k = lt.findIndex(t => st.some(s => has(s, [t]))); if (k >= 0) firsts.push(k); }
      if (firsts.length > 1 && Math.max(...firsts) - Math.min(...firsts) <= 14) spans.push([Math.min(...firsts), Math.max(...firsts), 3]);   // every key word of the question in one run, where they stand close enough
      lt.forEach((t, k) => { if (spans.length < 6 && allStems.some(s => has(s, [t]))) spans.push([k, k, 0]); }); }   // (a key word may stand more than once in the sentence)
    let w = null; for (const [a, b, more] of spans) { const got = iaWindow(toks, a, b, { stems: allStems, names, head: !!def }); if (got && (!w || got[2] + more > w[2])) w = [got[0], got[1], got[2] + more]; }
    if (!w) { say("a sentence with the key word (" + (c.x.sec || "no label") + ", " + toks.length + " words) has no 15 words in a row that pass the rules: a word it turns on, an amount, a held word", c.i); continue; }
    const q = (w[0] > 0 ? "…" : "") + toks.slice(w[0], w[1] + 1).join(" ").replace(/^[,;:\s]+|[,;:.\s]+$/g, "") + (w[1] < toks.length - 1 ? "…" : "");
    // animals or cells: where the sentence says so; where the title does and names no people ("... in naive and cocaine-experienced rats": its "naive individuals"
    // are rats); where the whole summary does. 2: the summary covers both, and the sentence does not say which
    return { q, an: sa ? 1 : ta ? (sp ? 2 : 1) : sp || !pa ? 0 : pp ? 2 : 1, i: c.i, n, sec: c.x.sec };
  }
  return null;
}
/* The papers on a drug and a question's key words, the best first, each with its own words on the question where the rules find them.
   Gives { papers, more, ms, again, won, own, kept }: more: the most cited were still out when the list was given (the page asks once more a moment later);
   and, for the editors, numbers only: ms: when each of the three searches was in (null: not yet); again: how many askings were repeated; won: which asking
   of each search answered (0 the first); own: how long that asking itself took; kept: how many searches were answered from what was kept. */
const FIND_A = [600, 1300], FIND_B = [900, 1700], FIND_GRACE = 300, FIND_SOON = 2000, FIND_LAST = 3000, FIND_ALL = 5600, FIND_GEN = 5000;
// (2.21.1) a search is left to finish for FIND_KILL ms behind the reply (Cloudflare lets a request work for 30 seconds after its reply); FIND_OUT: the end of the
// address under which the cache holds the note that a search is out; FIND_STILL: what such a search gives a later request that waited for it in vain
const FIND_KILL = 28000, FIND_OUT = "&out=1", FIND_STILL = { still: true };
async function findPapers(env, r, most, ctx) {
  const get = env.FETCH || fetch, began = Date.now(), left = () => FIND_ALL - (Date.now() - began);
  // Europe PMC's replies are kept for a day where the site runs (Cloudflare's cache, by the search's address), so that the same search is not made twice:
  // for the next reader with that question, and for this page when it asks again. (env.CACHE: a stand-in, in the tests and trials.)
  let cache = env.CACHE || null; if (!cache) { try { cache = (typeof caches !== "undefined" && caches.default) || null; } catch (e) { cache = null; } }
  /* One search, begun at once; nobody is made to wait for it. What makes a question slow (trials 6 to 9, and the site's own publishing runs): Europe PMC
     answers a search in a fifth to a half of a second (from the site's own server, which opens a new connection each time, in a half to nine tenths), but
     about one request in three hangs for two to ten seconds, whatever is asked; the same search asked again at that moment comes back at once seven times
     in ten. So a search that is not back after a while is asked a second time, and later a third (`again`: after how long), and whichever reply comes first
     counts; each asking is written with its first words in another order, so that it is a request of its own and does not wait behind the one that hangs.
     An asking that is still out when the list is given is left to finish behind the reply (ctx.waitUntil), and its answer is kept.
     (2.21.1, 18 November 2026, 15:40 Athens: Europe PMC took 24 to 27 seconds for every search, asked from the senior author's own computer too. The site's
     server gave each search up after 20 seconds, so none was ever kept; and each later asking of the page asked every search anew, up to nine requests a
     question to a service that was already struggling.) A search is now left to finish for 28 seconds, and while it is out it is not asked a second time by
     a later request: a note in the cache says that it is out (FIND_OUT: half a minute at most, taken away at once when the search fails), and the later request waits
     for the reply where it will be kept. Such a search counts as "still out" (the reply says more), never as "found nothing". */
  // live: { on } of the round that asks; once its list has gone out (on: false), a search that is still out may finish, and is kept, but is not asked again
  // noted: a search of the question's first round (the one the page's earlier request has certainly begun): only for those is the note that a search is out
  // written and read (Cloudflare counts every call to its cache with the requests: 50 in all for one request on the free plan)
  const start = (q, sort, size, again, live, noted) => {
    const s = { done: !q, v: q ? null : [], ms: null, again: 0, won: null, own: null, kept: 0, p: null, wait: false, failed: false };
    if (!q) { s.p = Promise.resolve(s.v); return s; }
    const t0 = Date.now(), ctl = new AbortController(), tries = [], marks = [], qq = "query=" + encodeURIComponent(q);
    const read = text => { const d = JSON.parse(text); return ((d && d.resultList && d.resultList.result) || []).map(x => { const p = findPaper(x); return p ? Object.assign(p, { ab: String((x && x.abstractText) || "") }) : null; }).filter(Boolean); };
    const once = async (order, k) => { const tail = "&pageSize=" + size + (order ? "&sort=" + order : ""), key = EPMC + "?" + qq + "&format=json&resultType=core" + tail, t1 = Date.now();
      /* (also before a later asking: the first may have come in meanwhile, in this request or in the page's one before) */
      if (cache) { let hit = null; try { hit = await cache.match(key); } catch (e) { hit = null; } if (hit) { const list = read(await hit.text()); s.kept = 1; return { list, k, own: Date.now() - t1 }; }
        if (k === 0 && noted) { const mark = key + FIND_OUT; let out = null; try { out = await cache.match(mark); } catch (e) { out = null; }
          if (out) { s.wait = true;   // (2.21.1) this very search is out already (asked by this page a moment ago): not asked again, awaited where its reply will be kept
            for (let n = 0; n < 8 && live.on && Date.now() - began < FIND_ALL; n++) { await new Promise(d => setTimeout(d, 400)); try { hit = await cache.match(key); } catch (e) { hit = null; }
              if (hit) { const list = read(await hit.text()); s.kept = 1; return { list, k, own: Date.now() - t1 }; } }
            return FIND_STILL; }
          const note = Promise.resolve().then(() => cache.put(mark, new Response("1", { headers: { "cache-control": "public, max-age=30" } }))).catch(() => {}); marks.push([mark, note]); if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(note); } }
      const res = await get(k === 0 ? key : EPMC + "?" + (k === 1 ? "format=json&" + qq + "&resultType=core" : "resultType=core&format=json&" + qq) + tail, { headers: { accept: "application/json", "user-agent": "pharmakon.world (contact@pharmakon.world)" }, signal: ctl.signal });
      if (!res.ok) return order ? once("", k) : null;   // (should the service not take the order asked for, it is asked once more without it)
      const text = await res.text(), list = read(text);
      if (cache) { const put = Promise.resolve().then(() => cache.put(key, new Response(text, { headers: { "content-type": "application/json", "cache-control": "public, max-age=86400" } }))).catch(() => {}); if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(put); }
      return { list, k, own: Date.now() - t1 };
    };
    const run = k => { const p = once(sort, k).catch(() => null); tries.push(p); return p; };
    s.p = new Promise(done => {
      let open = 0, fin = false, refused = false; const later = [], kill = setTimeout(() => ctl.abort(), FIND_KILL);
      const end = v => { fin = true; later.forEach(t => clearTimeout(t)); s.v = v ? v.list : null; if (v) { s.won = v.k; s.own = v.own; } else s.failed = true; s.done = true; s.ms = Date.now() - t0; done(s.v); };   // (failed: Europe PMC said no, or could not be reached: that is not "found nothing")
      const got = v => { open--; if (open === 0) clearTimeout(kill);
        if (v === FIND_STILL) { if (!fin) { fin = true; later.forEach(t => clearTimeout(t)); done(null); } return; }   // still out, asked by an earlier request: not done, not refused (the reply says more)
        if (v === null) refused = true; if (fin || (v === null && open > 0)) return; end(v); };
      open++; run(0).then(got);
      (again || []).forEach((ms, k) => later.push(setTimeout(() => { if (fin || !live.on || s.wait) return; if (refused) { if (open === 0) end(null); return; } open++; s.again++; run(k + 1).then(got); }, ms)));
    });
    // (behind the reply: every asking is left to finish)
    const after = s.p.then(() => Promise.all(tries)).then(vs => Promise.all(marks.map(([m, put]) => (s.failed && cache && typeof cache.delete === "function" ? put.then(() => cache.delete(m)).catch(() => {}) : null))).then(() => vs));   // (a search that FAILED must not leave its note behind: the next request may ask it again at once. One that came back is kept, and its note is never read again; it goes by itself)
    if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(after); else after.catch(() => {});
    return s;
  };
  const got = s => (s.done && s.v) || [];   // (not back yet, or refused: nothing)
  const seen = new Set(), out = [], add = list => { for (const p of list) { if (!p) continue; const k = p.doi || p.pmid; if (!seen.has(k)) { seen.add(k); out.push(p); } } };
  const all = r.names.concat(r.also || []), stems = r.groups.map(g => [...new Set(g.flatMap(iaNearStems))]);
  const onTopic = p => { const lt = iaFlat(p.t).split(/[^a-z0-9-]+/); return stems.every(st => st.some(s => lt.some(w => (s.includes("-") ? w.startsWith(s) : w.split("-").some(x => x.startsWith(s)))))); };
  let more = false, down = false, ms = null, again = 0, won = [], own = [], kept = 0;
  /* Three searches are asked together: the most cited papers with the drug in their title that hold the key words (in the title, or as a review); the
     newest papers with drug and key words in the title; and, as what is there when those two are slow or find little, the papers that hold the drug and
     the key words anywhere, in Europe PMC's own order. Of the most cited, those with the key words in their very title come first.
     When the list is given: as soon as the most cited are back, with the newest if they are back too or come within three tenths of a second (the newest are
     one paper of the six: nobody waits for them longer, and the list is not changed for them afterwards; they are kept for the next reader); after two
     seconds without the most cited, whatever three papers there are, and the reply says that more is to come; after three seconds, whatever there is. */
  /* (2.21) A question that names no single drug ("drug use", "substance use" in the place of a name). The eleventh trial asked such questions the way a drug's
     are asked and found the right papers for most, but each of the three searches took two to ten seconds at Europe PMC (the subject stands in hundreds of
     thousands of papers), the second and third askings doubled that load, and a question with five key words found nothing. So for these: two plain
     searches, each asked ONCE (the reviews with the subject in the title that hold every key word; the papers with subject and key words in the very title),
     both for the most cited, and one patient reply (FIND_GEN) in the place of a quick thin one. Titles only: readFind says so (noq). */
  const roundGen = async names => { const Q = findQueries(names, r.groups), live = { on: true };
    const G = start(Q.genRev, "CITED%20desc", 6, [], live, true), T = start(Q.onTitle, "CITED%20desc", 6, [], live, true); let t = null;
    await Promise.race([Promise.all([G.p, T.p]), new Promise(d => { t = setTimeout(d, Math.max(300, Math.min(FIND_GEN, left()))); })]); clearTimeout(t); live.on = false;
    const g = got(G), tt = got(T);
    add([tt[0], g[0], tt[1], g[1], tt[2], g[2]].concat(tt.slice(3), g.slice(3)));
    if (!G.done || !T.done) more = true;
    if (G.failed || T.failed) down = true;
    if (!ms) { ms = [G.ms, T.ms, null]; won = [G.won, T.won, null]; own = [G.own, T.own, null]; }
    kept += G.kept + T.kept; };
  const round = async (names, noted) => { const Q = findQueries(names, r.groups), live = { on: true };
    // (2.28.20) a question with no key word ("what is hhc", "is delta 8 safe", "what does fly agaric do"): reviews of the drug, the most cited, beside its most
    // cited papers, and first. Before this its most cited papers alone came, often old studies in animals or of the plant's biology (trials 32 and 33)
    const A = start(Q.cited, "CITED%20desc", 8, FIND_A, live, noted), C = start(r.groups.length ? Q.onTitle : Q.nameRev, r.groups.length ? "P_PDATE_D%20desc" : "CITED%20desc", r.groups.length ? 2 : 3, FIND_B, live, noted), W = start(Q.wide || Q.anyTitle, "", 4, FIND_B, live, noted);
    const known = (...ss) => new Set(ss.flatMap(got).map(p => p.doi || p.pmid)).size;
    await new Promise(go => { let grace = false, soon = false, fin = false; const timers = [];
      const look = last => { if (fin) return;
        if (last || (A.done && C.done && (W.done || known(A, C) >= 3)) || (A.done && grace && known(A, C) >= 3) || (soon && known(A, C, W) >= 3)) { fin = true; timers.forEach(clearTimeout); go(); } };
      A.p.then(() => { timers.push(setTimeout(() => { grace = true; look(); }, FIND_GRACE)); look(); }); C.p.then(() => look()); W.p.then(() => look());
      timers.push(setTimeout(() => { soon = true; look(); }, FIND_SOON), setTimeout(() => look(true), Math.max(300, Math.min(FIND_LAST, left())))); });
    live.on = false;
    const a = got(A), c = got(C), w = got(W);
    const first = stems.length ? a.filter(onTopic) : a, rest = stems.length ? a.filter(p => !onTopic(p)) : [];
    if (!r.groups.length) add([c[0], first[0], c[1], first[1], first[2], c[2]].concat(first.slice(3)));   // (2.28.20) no key word: the reviews first
    else add([first[0], first[1], rest[0], first[2], c[0], rest[1], first[3], rest[2], c[1]].concat(first.slice(4), rest.slice(3)));
    if (out.length < 3) add(w);
    if (!A.done || (!r.groups.length && !C.done) || (out.length < 3 && (!C.done || !W.done))) more = true;   // (2.28.20) no key word: the reviews are worth asking again for
    if (A.failed || (out.length < 3 && (C.failed || W.failed))) down = true;
    if (!ms) { ms = [A, C, W].map(s => s.ms); won = [A, C, W].map(s => s.won); own = [A, C, W].map(s => s.own); }
    again += A.again + C.again + W.again; kept += A.kept + C.kept + W.kept; };
  // one wider search, where the three found too little
  const one = async (q, sort, size) => { if (!q || left() < 600) return []; const live = { on: true }, s = start(q, sort, size, FIND_B, live); let t = null;
    await Promise.race([s.p, new Promise(d => { t = setTimeout(d, Math.max(300, Math.min(FIND_LAST, left()))); })]); clearTimeout(t); live.on = false; if (!s.done) more = true; if (s.failed) down = true; again += s.again; kept += s.kept; return got(s); };
  if (r.gen) { await roundGen(r.names); const papers = out.slice(0, most).map(p => ({ t: p.t, a: p.a, j: p.j, y: p.y, doi: p.doi, pmid: p.pmid, oa: p.oa, kind: p.kind })); return { papers, more, down, ms: ms || [], again, won, own, kept }; }
  await round(r.names, true);
  // wider, only where the searches are back and found too little (a search that is still out is not "too little": the page asks again)
  if (!more && out.length < 3 && all.length > r.names.length && left() > 600) await round(all);   // (the name the reader wrote found too little: with what its page is called)
  const Q = findQueries(all, r.groups);
  if (!more && out.length < 3 && Q.loose) add(await one(Q.loose, "CITED%20desc", 4));
  if (!more && out.length < 2 && r.groups.length) add(await one(Q.nameRev, "CITED%20desc", 4));
  const papers = out.slice(0, most).map(p => { let pick = null; try { pick = r.noq ? null : iaPick(p, r.groups, all, r.def); } catch (e) { pick = null; }
    const o = { t: p.t, a: p.a, j: p.j, y: p.y, doi: p.doi, pmid: p.pmid, oa: p.oa, kind: p.kind }; if (pick) { o.q = pick.q; if (pick.an) o.an = pick.an; } return o; });
  return { papers, more, down, ms: ms || [], again, won, own, kept };
}
async function find(request, url, env, ctx) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  const origin = request.headers.get("origin");
  if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
  let body = null;
  try { const t = await request.text(); if (t.length > 2000) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const r = readFind(body); if (r.error) return json({ ok: false, error: r.error }, 422);
  if (r.held) return json({ ok: true, held: true, papers: [] });
  try { const f = await findPapers(env, r, 6, ctx); return json(Object.assign({ ok: true, papers: f.papers }, f.more ? { more: 1 } : {}, f.down ? { down: 1 } : {}, r.noq ? { titles: 1 } : {}, { ms: f.ms, again: f.again, won: f.won, own: f.own, kept: f.kept })); }
  catch (e) { return json({ ok: false, error: "search" }, 502); }
}
/* (site 2.21, 18 November 2026; the senior author, 13:34 Athens: "can the answers get ... answered by themselves? and can they get answered almost instantly?
   one day or two is too ... much"; 14:44, of the look that was to come every five minutes: "if it can be every minute or 30 seconds or even a few seconds it
   would be even better ... whatever is best".) Best is no clock at all: a NEW question starts the system's work the moment it arrives. GitHub is asked to
   start the workflow that reads the store and writes the answer (.github/workflows/auto.yml); its own clock comes every five minutes at best and often much
   later (on 18 November it did not come for 25 minutes). This runs only where the senior author has given this server a key that may do exactly that and
   nothing else (env.GH_RUN_TOKEN: a fine-grained token for this one repository, "Actions: read and write"); without the key nothing here runs.
   At most one request in RUN_EVERY seconds from one of Cloudflare's places (a note in its cache, never in the store: no write is spent on it); the workflow
   itself lets one run wait behind the one that is working, so a question that arrives while a run works is read by the next. No word of the question
   leaves this server for it: the request names the workflow and the branch, nothing else. */
const RUN_EVERY = 20, RUN_NOTE = "https://pharmakon.world/__run-asked", RUN_LAST = "run:last";
async function startWork(env, store) {
  const token = String((env && env.GH_RUN_TOKEN) || "").trim(); if (!token) return "off";
  let what = "failed";
  try {
    let cache = env.CACHE || null; if (!cache) { try { cache = (typeof caches !== "undefined" && caches.default) || null; } catch (e) { cache = null; } }
    if (cache) { if (await cache.match(RUN_NOTE)) return "lately"; await cache.put(RUN_NOTE, new Response("1", { headers: { "cache-control": "public, max-age=" + RUN_EVERY } })); }
    const r = await fetch("https://api.github.com/repos/vasilissampalis/pharmakon/actions/workflows/auto.yml/dispatches", { method: "POST", body: JSON.stringify({ ref: "main" }),
      headers: { authorization: "Bearer " + token, accept: "application/vnd.github+json", "x-github-api-version": "2022-11-28", "user-agent": "pharmakon-site", "content-type": "application/json" } });
    what = r.status === 204 ? "asked" : "refused " + r.status;
  } catch (e) { what = "failed"; }
  /* (2.21.3) What GitHub said to the last start is kept in one small note (run:last), written only when it changes, so that a key that has run out or was taken
     away is SEEN: the publishing's own check reads it (GET /api/ask?run=1) and writes it into its notes. No word of any question is in it. */
  try { if (store) { const had = await store.get(RUN_LAST, "json"); if (!had || had.what !== what) await store.put(RUN_LAST, JSON.stringify({ what, since: new Date().toISOString() })); } } catch (e) { /* the note is a convenience */ }
  return what;
}
/* (site 2.23, 19 November 2026) What our system is doing for a question a reader sent, and the answer the moment it is written.
   The senior author, 18 November 2026, 23:42 Athens: "the site is taking too long to answer my pending questions... i persist on this like 5 minutes pass and
   i don't have an answer from inside the website it should be answered almost immediately". Until this version the page of a reader who had sent a question
   said "sent" and nothing more: it learned of an answer only from a new version of the site, and only when the reader opened it again.
   A run of the system now writes one small file as it works (data/auto/live.json; scripts/auto/live.py): for each sent question, by the store's own key
   and never by its words, the listed question it became in OUR wording, what has been done (worded; so many papers and official pages found; being written;
   why there is no answer yet), and, for an answer that passed every gate of the lane AND the last look of the site's own build, the answer in the very form
   the page holds it. This server reads that file from the public repository: through GitHub's own service with the key the senior author gave it for starting
   the work (GH_RUN_TOKEN: it reads here only what everybody can read), else the plain copy GitHub serves to everyone (which can be some minutes old). It is
   kept LIVE_EVERY seconds at this place of Cloudflare's, so GitHub is asked at most that often however many readers wait.
   What arrives: keys of questions this reader's device sent before, and numbers of listed questions it keeps: no words. What goes back: only what belongs
   to those. Nothing is kept or logged. The answer shown this way is the same record the site publishes minutes later; it carries the same line, "Written by
   our system ... Not yet checked by a person." */
const LIVE_EVERY = 6, LIVE_NOTE = "https://pharmakon.world/__live-file";
const LIVE_API = "https://api.github.com/repos/vasilissampalis/pharmakon/contents/data/auto/live.json?ref=main", LIVE_RAW = "https://raw.githubusercontent.com/vasilissampalis/pharmakon/main/data/auto/live.json";
let LIVE_MEM = null;   // {at, d}: the file as this running copy of the server last read it
export function liveForget() { LIVE_MEM = null; }   // (for the tests)
async function liveFile(env) {
  const now = Date.now();
  if (LIVE_MEM && now - LIVE_MEM.at < LIVE_EVERY * 1000) return LIVE_MEM.d;
  let cache = (env && env.CACHE) || null; if (!cache) { try { cache = (typeof caches !== "undefined" && caches.default) || null; } catch (e) { cache = null; } }
  if (cache) { try { const hit = await cache.match(LIVE_NOTE); if (hit) { const d = await hit.json(); if (d && typeof d === "object") { LIVE_MEM = { at: now, d }; return d; } } } catch (e) { /* asked afresh */ } }
  const get = (env && env.LIVE_FETCH) || fetch, token = String((env && env.GH_RUN_TOKEN) || "").trim(); let d = null;
  const ok = x => x && typeof x === "object" && !Array.isArray(x) && x.q && typeof x.q === "object" ? x : null;
  if (token) { try { const r = await get(LIVE_API, { headers: { authorization: "Bearer " + token, accept: "application/vnd.github.raw+json", "x-github-api-version": "2022-11-28", "user-agent": "pharmakon-site" } }); if (r.ok) d = ok(await r.json()); } catch (e) { d = null; } }
  if (!d) { try { const r = await get(LIVE_RAW, { headers: { "user-agent": "pharmakon-site" } }); if (r.ok) d = ok(await r.json()); } catch (e) { d = null; } }
  if (!d) return LIVE_MEM ? LIVE_MEM.d : null;   // GitHub did not answer: what was read before stands
  LIVE_MEM = { at: now, d };
  if (cache) { try { await cache.put(LIVE_NOTE, new Response(JSON.stringify(d), { headers: { "content-type": "application/json", "cache-control": "public, max-age=" + LIVE_EVERY } })); } catch (e) { /* this place asks again */ } }
  return d;
}
const liveText = (s, n) => clean(s).slice(0, n);
function liveItem(d, id) {
  const it = d.items && typeof d.items === "object" ? d.items[id] : null; if (!it || typeof it !== "object") return null;
  const o = { id, our: liveText(it.q, 200), st: liveText(it.st, 12), say: liveText(it.say, 300) };
  if (it.n && typeof it.n === "object") o.n = { papers: Math.max(0, Math.min(99, +it.n.papers || 0)), pages: Math.max(0, Math.min(99, +it.n.pages || 0)) };
  if (Array.isArray(it.terms)) o.terms = it.terms.filter(x => typeof x === "string").map(x => liveText(x, 60)).filter(Boolean).slice(0, 6);
  if (it.at) o.at = liveText(it.at, 25);
  const w = d.working; if (w && Array.isArray(w.ids) && w.ids.includes(id)) o.working = liveText(w.since, 25);
  if (typeof it.aid === "string" && /^au_[a-z0-9_]{1,44}$/.test(it.aid)) { o.aid = it.aid; const a = d.answers && d.answers[it.aid]; if (a && typeof a === "object") o.ans = a; }
  return o;
}
async function asked(request, url, env) {
  if (request.method !== "GET") return json({ ok: false, error: "method" }, 405);
  const list = (k, re) => String(url.searchParams.get(k) || "").split(",").filter(x => re.test(x)).slice(0, 8);
  const hs = list("h", /^[0-9a-f]{20}$/), ws = list("w", /^w_[a-z0-9_]{1,40}$/);
  if (!hs.length && !ws.length) return json({ ok: false, error: "h" }, 422);
  const d = await liveFile(env); if (!d) return json({ ok: true, off: true });   // the file could not be read: the page goes on as it did before 2.23
  const out = { ok: true, at: liveText(d.at, 25), q: {}, w: {} };
  if (d.room === false) { out.room = false; out.room_at = liveText(d.room_at, 25); }
  for (const h of hs) { const e = d.q[h]; if (!e || typeof e !== "object") continue;
    if (typeof e.no === "string") { out.q[h] = { no: liveText(e.no, 300) }; continue; }
    const o = typeof e.id === "string" ? liveItem(d, e.id) : null; if (o) out.q[h] = o; }
  for (const id of ws) { const o = liveItem(d, id); if (o) out.w[id] = o; }
  return json(out);
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
  async fetch(request, env, ctx) {
    const url = new URL(request.url), at = url.pathname.replace(/\/+$/, "");   // "/api/ask/" is "/api/ask"
    if (at === "/api/find") return find(request, url, env, ctx);
    if (at === "/api/asked") return asked(request, url, env);
    if (at === "/api/answer") return json({ ok: true, off: true });   // (sites 2.18 and 2.19 asked a model here; since 2.20 the papers' own words come with /api/find, by rule. A page of those versions still open is told it is off)
    if (at !== "/api/ask" && at !== "/api/want") return url.pathname.startsWith("/api/") ? json({ ok: false, error: "not found" }, 404) : env.ASSETS.fetch(request);
    const store = env.QUESTIONS;
    if (at === "/api/want") return want(request, url, store);
    if (request.method === "GET") {   // what this server can do. 200 either way: a missing store is a state, not an error in the reader's console
      const can = { ok: !!store, find: true, auto: !!store, quick: false, live: true, start: !!String((env && env.GH_RUN_TOKEN) || "").trim() };   // (2.23) live: GET /api/asked says what the system is doing for a sent question   // (2.21.3) start: is the key there that starts the work when a question arrives (never the key itself)
      if (store && url.searchParams.get("run") === "1") { try { const s = await store.get(RUN_LAST, "json"); if (s && s.what) can.started = { what: String(s.what).slice(0, 40), since: String(s.since || "").slice(0, 24) }; } catch (e) { /* no note */ } }   // asked for by the publishing's check only: a page's own look reads nothing from the store
      return json(can);
    }
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
      if (had && had.last === day && (had.dn || 1) >= MAX_SAME_A_DAY) return json({ ok: true, again: true, k: hash });   // counted enough for today: nothing is written. (2.23) k: the question's key in the store, with which the page asks what became of it (GET /api/asked)
      const ck = "count:" + day, n = parseInt((await store.get(ck)) || "0", 10) || 0;
      if (n >= (auto ? MAX_AUTO_UNTIL : MAX_A_DAY)) return json({ ok: false, error: "full for today" }, 429);
      await store.put(ck, String(n + 1), { expirationTtl: 3 * 86400 });
      const opts = auto ? { expirationTtl: AUTO_KEPT } : undefined;
      if (had) {
        had.n = (had.n || 1) + 1; had.dn = had.last === day ? (had.dn || 1) + 1 : 1; had.last = day;
        if (r.d && !(had.d || []).includes(r.d)) had.d = (had.d || []).concat(r.d).slice(0, 5);
        if (r.x && !(had.x || []).includes(r.x)) had.x = (had.x || []).concat(r.x).slice(0, 5);   // (2.22) the answers a reader said do not answer this question
        await store.put(key, JSON.stringify(had), opts); return json({ ok: true, again: true, k: hash });
      }
      await store.put(key, JSON.stringify(Object.assign({ q: r.q, d: r.d ? [r.d] : [], v: r.v, first: day, last: day, n: 1, dn: 1 }, auto ? { a: 1 } : {}, r.x ? { x: [r.x] } : {})), opts);
      { const go = startWork(env, store).catch(() => "failed"); if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(go); }   // a new question: the system's work is started now (see startWork), behind the reply
      return json({ ok: true, k: hash });
    } catch (e) { return json({ ok: false, error: "store" }, 503); }
  }
};
