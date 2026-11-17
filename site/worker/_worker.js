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
    if (at !== "/api/ask" && at !== "/api/want") return url.pathname.startsWith("/api/") ? json({ ok: false, error: "not found" }, 404) : env.ASSETS.fetch(request);
    const store = env.QUESTIONS;
    if (at === "/api/want") return want(request, url, store);
    if (request.method === "GET") return json({ ok: !!store, find: true, auto: !!store });   // 200 either way: a missing store is a state, not an error in the reader's console
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
