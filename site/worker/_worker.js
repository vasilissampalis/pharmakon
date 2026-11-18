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
   POST /api/find {names, words, def} -> {"ok": true, "papers": [...]}  (site 2.16, 17 November 2026; the senior author: "answers take
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
  return { q, d, v, a: !!(body && (body.a === 1 || body.a === true)) };
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
   Which words (iaPick, iaWindow). A paper gets words only where ALL of this holds:
     1. the sentence stands where papers say what they found: under a label for results or conclusions, or, in a summary without labels,
        in its later half; it is not a sentence about what the paper set out to do or how it was done;
     2. it holds a key word of the question (or a word papers use for it), and every key word stands in the sentence or the paper's title;
     3. the paper is about the drug (its name in the title) or the sentence names the drug;
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
   Not looked up at all: words about dying, overdose, amounts, pregnancy or children (FIND_HELD: such questions wait for a person). Papers
   are listed but no words are shown for what research summaries cannot settle for a reader (the law, prices, drug tests).
   What arrives: the names of a drug (up to 6) and plain key words (up to 6), chosen on the reader's device; never the reader's sentence.
   What goes out to Europe PMC: those names and words, from this server (the reader's address is not passed on). Nothing is kept or logged
   here; Cloudflare keeps Europe PMC's reply for a day so that the same search is not asked twice. */
const EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search";
export const FIND_HELD = /\b(pregnan\w*|breast-?feed\w*|child|children|kids?|bab(y|ies)|infants?|teen\w*|minors?|suicid\w*|kill\w*|die[sd]?|dying|deaths?|dead|deadly|mortalit\w*|overdos\w*|lethal|fatal\w*|dos(e|es|age|ing)|mg|milligrams?|grams?|micrograms?)\b/i;
const FIND_NOT_RESEARCH = /^(?:legal\w*|illegal\w*|law|laws|lawful|police|arrest\w*|prison|jail|court|customs|border|airport|price|prices|cost|costs|cheap\w*|buy|buying|bought|order\w*|dealers?|vendors?|urine|test|tests|tested|testing|screen\w*|detect\w*)$/i;
const findName = s => { s = clean(s).toLowerCase(); return /^[a-z0-9][a-z0-9 ,.'+()\-]{1,58}[a-z0-9)]$/.test(s) && !/["\\:]/.test(s) ? s : ""; };
const findWord = s => { s = clean(s).toLowerCase(); return /^[a-z]{3,24}$/.test(s) ? s : ""; };
// a key word may come with the word papers use for it, as one entry: "appetite|hungry". The two are one thing asked for, in two ways.
// def: the question asks what the drug is ("what is phenibut"); noq: its key words are about the law, prices or drug tests (papers are listed, no words shown)
// also: what the drug's page is called, where the reader named a drug of its own ("xanax": benzodiazepines; "tramadol": prescription opioids): asked for
// only where the reader's own name finds fewer than three papers
export function readFind(body) {
  const uniq = a => [...new Set(a.filter(Boolean))];
  const names = uniq((Array.isArray(body && body.names) ? body.names : []).slice(0, 12).map(findName)).slice(0, 6);
  const also = uniq((Array.isArray(body && body.also) ? body.also : []).slice(0, 8).map(findName)).filter(n => !names.includes(n)).slice(0, 4);
  const groups = (Array.isArray(body && body.words) ? body.words : []).slice(0, 12).map(e => uniq(String(e == null ? "" : e).split("|").slice(0, 3).map(findWord)).filter(w => !names.includes(w))).filter(g => g.length).slice(0, 6);
  const words = uniq(groups.flat());
  if (!names.length) return { error: "no name" };
  return { names, also, words, groups, def: !!(body && (body.def === 1 || body.def === true)) && !groups.length, noq: words.some(w => FIND_NOT_RESEARCH.test(w)), held: names.concat(also, words).some(t => FIND_HELD.test(t)) };
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
  salvia: "salvinorin divinorum", shrooms: "psilocybin psilocybe", mushrooms: "psilocybin psilocybe", poppers: "nitrite nitrites", ecstasy: "mdma methylenedioxymethamphetamine", nos: "nitrous" };
/* What Europe PMC is asked (its own search words). groups: the question's key words, each an array of the ways it is said. Every key word must
   stand in a paper, not any one of them; the drug's name must stand in the paper's title, except in the widest search. */
export function findQueries(names, groups) {
  const any = ts => "(" + ts.map(t => `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")";
  const one = (n, inTitle) => { const fs = nameForms(n), core = inTitle ? (fs.length > 1 ? "(" + fs.map(f => `TITLE:"${f}"`).join(" OR ") + ")" : `TITLE:"${fs[0]}"`) : any(fs), ctx = FIND_CTX[n]; return ctx ? "(" + core + " AND " + any(ctx.split(" ")) + ")" : core; };
  const nm = inTitle => "(" + names.map(n => one(n, inTitle)).join(" OR ") + ")";
  const gs = (groups || []).map(g => [...new Set((Array.isArray(g) ? g : [g]).flatMap(findForms))]).filter(g => g.length);
  const key = inTitle => gs.map(g => " AND (" + g.map(t => inTitle ? `TITLE:"${t}"` : `TITLE:"${t}" OR ABSTRACT:"${t}"`).join(" OR ") + ")").join("");
  const tail = ' AND LANG:eng NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"';
  const rev = ' AND (PUB_TYPE:"review" OR PUB_TYPE:"systematic review" OR PUB_TYPE:"meta-analysis")';
  return { reviews: nm(true) + key(false) + rev + tail,                            // reviews of the drug that hold every key word (asked for the most cited)
    onTitle: nm(true) + key(true) + tail,                                          // the drug and every key word in the very title (asked for the most cited, and for the newest)
    wide: gs.length ? nm(false) + key(false) + tail : "",                          // the drug and every key word anywhere in title or summary
    loose: gs.length > 1 ? nm(false) + " AND " + any([...new Set(gs.flat())]) + tail : "",   // any one key word (only where the others found fewer than three)
    nameRev: nm(true) + rev + tail };                                              // reviews of the drug itself (only where the others found fewer than two)
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
  const t = clean(unEnt(String(raw || "").slice(0, 9000).replace(/<h4[^>]*>\s*([^<]{1,80}?)\s*:?\s*<\/h4>/gi, (m, l) => " \u27E6" + l + "\u27E7 ").replace(/<[^>]+>/g, " ")));
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
const IA_ANIMAL = /\b(?:rats?|mice|mouse|rodents?|zebrafish|in vitro|ex vivo|in silico|cell lines?|cultured (?:cells|neurons)|cell cultures?|animals?|murine|preclinical|horses?|equine|dogs?|canine|cats?|feline|pigs?|porcine|monkeys?|macaques?|primates?|rabbits?|sheep|hamsters?|guinea pigs?|drosophila|flies|worms?|elegans|veterinary|larvae|embryos?|organoids?)\b/i;
const IA_PEOPLE = /\b(?:participants?|patients?|volunteers?|humans?|men|women|adults?|people|subjects|students|respondents|users|individuals|persons|adolescents|outpatients|inpatients)\b/i;
// a key word of a question, and the beginnings of the words papers use for the same thing
const IA_NEAR = { addiction: "addict dependence dependency dependent misuse abuse withdrawal craving", addictive: "addict dependence dependency dependent misuse abuse withdrawal craving", depression: "depress antidepress", anxiety: "anxi panic",
  sleep: "sleep insomn somnolen wakeful", appetite: "appetit hunger hungry feeding orexigen", hungry: "appetit hunger hungry feeding orexigen", memory: "memor amnes recall cognit", attention: "attenti concentrat vigilan cognit",
  concentrate: "attenti concentrat vigilan cognit", cognitive: "cognit memor attenti", pain: "pain analges nocicept", psychoactive: "psychoactiv intoxic euphor hallucin psychotrop", adverse: "advers harm risk toxic",
  serotonin: "seroton 5-ht 5ht", dopamine: "dopamin", cardiac: "cardi heart myocard arrhythm", heart: "cardi heart myocard arrhythm", hepatic: "hepat liver", liver: "hepat liver", renal: "renal kidney nephro", kidney: "renal kidney nephro",
  kidneys: "renal kidney nephro", pulmonary: "pulmon lung respirat", lung: "pulmon lung respirat", lungs: "pulmon lung respirat", epistaxis: "epistax nosebleed", nosebleeds: "epistax nosebleed", psychosis: "psychos psychot schizophren",
  personality: "personalit trait", fatigue: "fatigu tired", paranoia: "paranoi", sexual: "sexual libido erectile", dental: "dental teeth tooth bruxism caries", tremor: "tremor shak", sweating: "sweat hyperhidro diaphore",
  vomiting: "vomit emesis emetic nausea" };
const iaStem = f => (f.length > 8 ? f.slice(0, f.length - 2) : f.length > 5 ? f.slice(0, f.length - 1) : f);
export const iaNearStems = w => (IA_NEAR[w] ? IA_NEAR[w].split(" ") : [...new Set(findForms(w).map(iaStem))]);
// a sentence about what the paper set out to do, or how it was done: not one that says what it found
const IA_AIM = /\b(?:aims?|aimed|objectives?|purpose|goal) (?:of|was|were|is|are|to)\b|\bwe (?:aimed|sought|set out|hypothesi[sz]ed)\b|\b(?:this|the present|the current|our) (?:study|paper|article|review|report|trial|work|chapter|analysis|survey|meta-analysis|systematic review|scoping review|narrative review) (?:aim|seek|sought|investigat|examin|explor|assess|evaluat|review|summari|describ|discuss|present|provid|focus|address|compar|test|was designed|is intended|will|outlin|synthesi|collat|map)\w*|\bto (?:determine|investigate|examine|assess|evaluate|explore|test|compare|characteri[sz]e|describe|review|summari[sz]e|identify|study|establish|clarify|elucidate) (?:whether|if|the|how|a|an)\b|\b(?:was|were) to\b|\bwe (?:investigated|examined|explored|assessed|evaluated|tested|studied|conducted|performed|reviewed|searched|surveyed|recruited|measured|compared|analy[sz]ed|describe|present|discuss|summari[sz]e|review|report (?:a|an|the|on|two|three|four|\d))\b/i;
const IA_HOW = /\b(?:has|have) been (?:conducted|performed|reviewed|searched|summari[sz]ed|described|discussed|undertaken|carried out|collated|compiled)\b|\b(?:is|are) (?:reviewed|discussed|described|summari[sz]ed|presented|outlined|provided|highlighted|considered|addressed|explored)\b|\b(?:were|was) (?:recruited|enrolled|randomi[sz]ed|randomly|assigned|allocated|administered|collected|measured|assessed|evaluated|analy[sz]ed|performed|conducted|searched|included|extracted|screened|obtained|recorded|interviewed|surveyed|asked|quantified|monitored|calculated)\b|\bparticipants (?:completed|received|underwent)\b|\b(?:pubmed|medline|embase|scopus|web of science|psycinfo|cochrane (?:library|central)|prisma|prospero|clinicaltrials\.gov|inclusion criteria|exclusion criteria|search strateg\w*|trial registration|funded by|copyright|all rights reserved)\b/i;
const IA_FOUND = /\b(?:found|show(?:s|ed|n)?|demonstrat\w*|reveal\w*|indicat\w*|suggest\w*|observ\w*|associat\w*|correlat\w*|linked|reduc\w*|increas\w*|decreas\w*|improv\w*|impair\w*|attenuat\w*|alleviat\w*|ameliorat\w*|worsen\w*|higher|lower|greater|fewer|significan\w*|conclud\w*|support\w*|confirm\w*|evidence|did not|does not|no (?:significant )?(?:difference|effect|evidence|association|change)s?|leads? to|led to|results? in|resulted in|caus\w*|produc\w*|induc\w*|yield\w*|prevent\w*|predict\w*|alter\w*|escalat\w*)\b/i;
// a sentence that asks for more research says little of what was found: taken only where a summary has no better one
const IA_MORE = /\b(?:further|more|future|additional|larger|longer) (?:\w+ ){0,2}(?:research|studies|study|work|trials?|investigations?|evidence|data)\b|\b(?:is|are|remains?) (?:needed|warranted|required|necessary)\b/i;
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
const IA_W_SOFT = /^(?:should|must|ought|recommend\w*|advis\w*|safe|safely|safer|safest|safety|harmless|well-tolerated|tolerab\w*|tolerated)$/;
const IA_W_ROUTE = /^(?:oral\w*|smok\w*|inject\w*|snort\w*|intranasal\w*|insufflat\w*|intraven\w*|sublingual\w*|rectal\w*|vap\w*|edibles?|eaten|eating|swallow\w*|chew\w*|inhal\w*)$/, IA_W_THAN = /^(?:than|compared|versus|vs|faster|slower|quicker|bioavailab\w*|onset|peak)$/;
const IA_W_HANG = /^(?:the|a|an|of|in|on|at|to|for|by|with|and|or|but|that|which|who|whose|as|than|from|into|onto|upon|over|under|between|among|across|during|after|before|about|against|within|through|via|per|versus|vs|when|where|while|because|since|its|their|this|these|those|is|are|was|were|be|been|has|have|had|not|no|more|less|very|both|any|some|all|each|every|many|most|several|other|another|such|same|certain|various|either|neither|two|three|four|five|six)$/, IA_W_LAME = /^(?:of|and|or|but|than|that|which|who|whose|as|to|is|are|was|were)$/;
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
  const never = i => IA_W_NEVER.test(low[i]) || FIND_HELD.test(low[i]) || /\d(?:mg|mcg|µg|μg|ug|kg|ml|iu)\b/i.test(toks[i]) || (i > 0 && num(i - 1) && IA_AMOUNT_UNIT.test(low[i]))
    || (/^(?:combin\w*|mix\w*|together)$/.test(low[i]) && low[i + 1] === "with") || (low[i] === "every" && i + 2 < n && num(i + 1) && /^(?:minutes?|hours?)$/.test(low[i + 2]));
  let route = false, than = false; for (let i = 0; i < n; i++) { if (never(i)) return null; if (IA_W_ROUTE.test(low[i])) route = true; if (IA_W_THAN.test(low[i])) than = true; }
  if (route && than) return null;
  const cBad = cum(i => IA_W_SOFT.test(low[i]) || /https?:|www\.|\S@\S|[=<>±~]/i.test(toks[i]));   // (advice or a promise of safety, a link, statistics in signs: the shown words go around them)
  const cOpen = cum(i => /[(\[]/.test(toks[i])), cClose = cum(i => /[)\]]/.test(toks[i])), many = i => (toks[i].match(/[(\[]/g) || []).length !== (toks[i].match(/[)\]]/g) || []).length;
  const cUneven = cum(i => many(i)), paren = (s, e) => { let d = 0; for (let i = s; i <= e; i++) { for (const ch of toks[i]) { if (ch === "(" || ch === "[") d++; else if (ch === ")" || ch === "]") { d--; if (d < 0) return false; } } } return d === 0; };
  // (a word that most likely says what happened: "reduced", "was", "may", "did"; a run of words without one is a piece of a sentence, not a finding)
  const cVerb = cum(i => /^(?:is|are|was|were|be|been|has|have|had|did|does|do|may|might|can|could|will|would|found|shows?|shown|suggests?|indicates?|reveals?|reports?|links?|leads?|led|results?|yields?|prevents?|predicts?|alters?|affects?|remains?|appears?|seems?|occurs?|differs?|rose|fell|lowers?|exerts?|supports?|confirms?|persists?|develops?|reduces?|increases?|decreases?|improves?|impairs?|causes?|produces?|induces?|changes?|raises?|[a-z]{3,}ed)$/.test(low[i]));
  const cKey = cum(i => { const parts = low[i].split(/[-/]/); return stems.some(st => (st.includes("-") ? low[i].startsWith(st) : parts.some(p => p.startsWith(st)))); }), cName = cum(i => names.includes(low[i]) || names.includes(low[i].replace(/'s$/, "")));
  // a clause that opens the sentence with "Although ..." does not govern what follows its comma
  let free = -1; if (/^(?:although|though|while|whereas|despite|notwithstanding)$/.test(low[0]) || (low[0] === "even" && low[1] === "though")) { for (let i = 1; i < n - 1; i++) if (/,$/.test(toks[i])) { free = i; break; } }
  const edgeAt = i => i >= 0 && i < n && (/[,;:)\]]$/.test(toks[i]) || low[i] === "that" || (i > 0 && /[,;:]$/.test(toks[i - 1]) && /^(?:and|but|or)$/.test(low[i])));   // a part of the sentence ends with this word
  let best = null, top = -1e9;
  for (let s = Math.max(0, b - 14); s <= a; s++) {
    const from = s > free ? free + 1 : 0;   // (what stands before this is not counted)
    if (cPre[s] - cPre[from] > 0 || cBad[s] > 0) continue;   // (advice or a promise of safety before them: what follows is what is advised or promised, and is not shown)
    const preMay = cMay[s] - cMay[from] > 0;
    for (let e = b; e <= Math.min(n - 1, s + 14); e++) {
      if (cPost[n] - cPost[e + 1] > 0 || cAsk[Math.min(n, nb[e] + 1)] - cAsk[e + 1] > 0) continue;   // after them: a "no" or a "but" anywhere; a question or an aim up to the next comma (", which should be examined in ..." adds, it does not take back)
      if (cnt(cBad, s, e) > 0 || (preMay && cnt(cMay, s, e) === 0)) continue;
      if ((cnt(cOpen, s, e) > 0 || cnt(cClose, s, e) > 0) && (cnt(cUneven, s, e) > 0 || cnt(cOpen, s, e) !== cnt(cClose, s, e)) && !paren(s, e)) continue;
      // what reads best: a whole part of the sentence (from where one begins, to the sentence's end above all: the last words carry what was found), with the
      // key word and the drug's name in it, the words that lead up to the key word kept, and no small word left hanging at either end
      const score = (e - s + 1) + (s === 0 || edgeAt(s - 1) ? 8 : 0) + (e === n - 1 ? 10 : edgeAt(e) || /^[(\[]/.test(toks[e + 1]) ? 4 : 0) + (cnt(cKey, s, e) > 0 ? 5 : 0) + (cnt(cName, s, e) > 0 ? 5 : 0) + (cnt(cVerb, s, e) > 0 ? 6 : 0)
        - (e < n - 1 && IA_W_HANG.test(low[e]) ? 8 : 0) - (s > 0 && IA_W_LAME.test(low[s]) ? 8 : 0) - (s > 0 && !edgeAt(s - 1) && a - s < 3 ? 6 : 0) - (s > 0 && /[,;:]$/.test(toks[s]) ? 4 : 0);
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
  if (!def && !G.length) return null;
  const has = (st, lowToks) => lowToks.some(t => (st.includes("-") ? t.startsWith(st) : t.split(/[-/]/).some(x => x.startsWith(st))));
  const lows = s => s.toLowerCase().replace(/[‐-―−]/g, "-").split(/\s+/).map(t => t.replace(/’/g, "'").replace(/[^a-z0-9'/-]/g, "").replace(/^['-]+|['-]+$/g, ""));
  const flatT = iaFlat(p.t), titleLow = lows(p.t), titleNamed = nameRe.test(flatT), flatAll = iaFlat(p.t + ". " + parts.map(x => x.s).join(" ")), pa = IA_ANIMAL.test(flatAll), pp = IA_PEOPLE.test(flatAll);
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
    if (aim) { why.aim++; return; }                                                                       // it says what was found, not what was set out or how it was done
    if (!G.every(st => st.some(s => has(s, lt) || has(s, titleLow)))) { why.all++; return; }              // every key word stands in it or in the title
    const where = x.sec === "c" ? 6 : x.sec === "r" ? 4 : labelled ? -1 : i >= n - 2 ? 5 : i >= (n <= 4 ? 1 : Math.floor(n / 2)) ? 3 : -1; if (where < 0) { why.early++; return; }   // where papers say what they found (a summary of four sentences or fewer: anywhere after its first)
    if (!titleNamed && !nameRe.test(fs)) { why.about++; return; }                                         // about the drug
    cands.push({ i, x, fs, lt, score: where + (hit.length - 1) * 3 + (IA_FOUND.test(fs) ? 2 : 0) + (nameRe.test(fs) ? 1 : 0) - (IA_MORE.test(fs) ? 4 : 0) });
  });
  if (!cands.length) say(def ? "no sentence at its start says what the drug is" : !why.key ? "no sentence holds a key word of the question" : "of " + why.key + " sentence(s) that hold a key word: " + [why.aim && why.aim + " say what was set out or how it was done", why.early && why.early + " stand before the results", why.all && why.all + " lack another key word (and the title does too)", why.about && why.about + " do not name the drug (and the title does not)"].filter(Boolean).join(", "));
  cands.sort((u, v) => v.score - u.score || v.i - u.i);
  for (const c of cands.slice(0, 4)) {
    const sa = IA_ANIMAL.test(c.fs), sp = IA_PEOPLE.test(c.fs) || /\b(?:clinical|placebo|double-blind)\b/.test(c.fs); if (sa && sp) { say("a sentence with the key word speaks of animals or cells and of people at once"); continue; }
    const toks = c.x.s.split(/\s+/), lt = c.lt, spans = []; if (lt.length !== toks.length) continue;
    if (def) { const first = forms.map(f => f.split(" ")[0]), k = lt.findIndex(t => first.includes(t) || first.includes(t.replace(/'s$/, ""))); if (k >= 0) spans.push([k, k, 0]); }
    else { const firsts = []; for (const st of G) { const k = lt.findIndex(t => st.some(s => has(s, [t]))); if (k >= 0) firsts.push(k); }
      if (firsts.length > 1 && Math.max(...firsts) - Math.min(...firsts) <= 14) spans.push([Math.min(...firsts), Math.max(...firsts), 3]);   // every key word of the question in one run, where they stand close enough
      lt.forEach((t, k) => { if (spans.length < 6 && allStems.some(s => has(s, [t]))) spans.push([k, k, 0]); }); }   // (a key word may stand more than once in the sentence)
    let w = null; for (const [a, b, more] of spans) { const got = iaWindow(toks, a, b, { stems: allStems, names }); if (got && (!w || got[2] + more > w[2])) w = [got[0], got[1], got[2] + more]; }
    if (!w) { say("a sentence with the key word (" + (c.x.sec || "no label") + ", " + toks.length + " words) has no 15 words in a row that pass the rules: a word it turns on, an amount, a held word"); continue; }
    const q = (w[0] > 0 ? "…" : "") + toks.slice(w[0], w[1] + 1).join(" ").replace(/^[,;:\s]+|[,;:.\s]+$/g, "") + (w[1] < toks.length - 1 ? "…" : "");
    return { q, an: sa || (!sp && pa && !pp) ? 1 : !sp && pa && pp ? 2 : 0, i: c.i, n, sec: c.x.sec };
  }
  return null;
}
/* The papers on a drug and a question's key words, the best first, each with its own words on the question where the rules find them. Four
   searches are asked together; wider ones only where they found too little. */
async function findPapers(env, r, most) {
  const get = env.FETCH || fetch;
  const ask = async (q, sort, size) => {
    if (!q) return [];
    const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 7000);
    try {
      const res = await get(EPMC + "?query=" + encodeURIComponent(q) + "&format=json&resultType=core&pageSize=" + size + (sort ? "&sort=" + sort : ""), { headers: { accept: "application/json", "user-agent": "pharmakon.world (contact@pharmakon.world)" }, signal: ctl.signal, cf: { cacheTtl: 86400, cacheEverything: true } });
      if (!res.ok) return sort ? ask(q, "", size) : [];   // (should the service not take the order asked for, it is asked once more without it)
      const d = await res.json(); return ((d && d.resultList && d.resultList.result) || []).map(x => { const p = findPaper(x); return p ? Object.assign(p, { ab: String((x && x.abstractText) || "") }) : null; }).filter(Boolean);
    } catch (e) { return []; } finally { clearTimeout(timer); }
  };
  const seen = new Set(), out = [], add = list => { for (const p of list) { if (!p) continue; const k = p.doi || p.pmid; if (!seen.has(k)) { seen.add(k); out.push(p); } } };
  const all = r.names.concat(r.also || []);
  const round = async names => { const Q = findQueries(names, r.groups);
    const [a, b, c, d] = await Promise.all([ask(Q.reviews, "CITED%20desc", 4), ask(Q.onTitle, "CITED%20desc", 4), ask(Q.onTitle, "P_PDATE_D%20desc", 2), ask(Q.wide, "", 3)]);
    // the drug and the key words in the very title first, then the most cited reviews, in turn; then the newest; then the wider search
    add([b[0], a[0], b[1], a[1], c[0], d[0], b[2], a[2], c[1], d[1], b[3], a[3], d[2]]); };
  await round(r.names);
  if (out.length < 3 && all.length > r.names.length) await round(all);   // (the name the reader wrote found too little: with what its page is called)
  const Q = findQueries(all, r.groups);
  if (out.length < 3 && Q.loose) add(await ask(Q.loose, "CITED%20desc", 4));
  if (out.length < 2 && r.groups.length) add(await ask(Q.nameRev, "CITED%20desc", 4));
  return out.slice(0, most).map(p => { let pick = null; try { pick = r.noq ? null : iaPick(p, r.groups, all, r.def); } catch (e) { pick = null; }
    const o = { t: p.t, a: p.a, j: p.j, y: p.y, doi: p.doi, pmid: p.pmid, oa: p.oa, kind: p.kind }; if (pick) { o.q = pick.q; if (pick.an) o.an = pick.an; } return o; });
}
async function find(request, url, env) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  const origin = request.headers.get("origin");
  if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
  let body = null;
  try { const t = await request.text(); if (t.length > 2000) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const r = readFind(body); if (r.error) return json({ ok: false, error: r.error }, 422);
  if (r.held) return json({ ok: true, held: true, papers: [] });
  try { return json({ ok: true, papers: await findPapers(env, r, 6) }); }
  catch (e) { return json({ ok: false, error: "search" }, 502); }
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
    if (at === "/api/answer") return json({ ok: true, off: true });   // (sites 2.18 and 2.19 asked a model here; since 2.20 the papers' own words come with /api/find, by rule. A page of those versions still open is told it is off)
    if (at !== "/api/ask" && at !== "/api/want") return url.pathname.startsWith("/api/") ? json({ ok: false, error: "not found" }, 404) : env.ASSETS.fetch(request);
    const store = env.QUESTIONS;
    if (at === "/api/want") return want(request, url, store);
    if (request.method === "GET") return json({ ok: !!store, find: true, auto: !!store, quick: false });   // 200 either way: a missing store is a state, not an error in the reader's console
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
