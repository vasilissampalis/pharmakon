/* ---------- APA 7 rendering (prototype; production uses citeproc-js with the APA CSL style) ---------- */
const refById = Object.fromEntries(REFS.map(r => [r.id, r]));
const cardById = STUDY_CARDS;
const claimById = Object.fromEntries(CLAIMS.map(c => [c.id, c]));

function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function initials(given) {
  if (!given) return "";
  return given.trim().split(/\s+/).map(part => {
    // run-together initials as Crossref sometimes gives them: "W.S.", "M.G.", "PT", "AC" → one initial per letter
    if (/^([A-Z]\.){2,}$/.test(part) || /^[A-Z]{2,3}$/.test(part) || /^([A-Z]\.)+[A-Z]$/.test(part)) return part.replace(/\./g, "").split("").map(ch => ch + ".").join(" ");
    return part.split("-").map(p => p ? p[0].toUpperCase() + "." : "").join("-");
  }).join(" ");
}
function authorEntry(a) { return a.literal ? a.literal : (a.family + (a.given ? ", " + initials(a.given) : "") + (a.suffix ? ", " + a.suffix : "")); }
function apaAuthors(list) {
  const names = list.map(authorEntry);
  if (names.length === 1) return names[0];
  if (names.length <= 20) return names.slice(0, -1).join(", ") + ", & " + names[names.length - 1];
  return names.slice(0, 19).join(", ") + ", … " + names[names.length - 1];
}
// APA 7: undated works are "n.d."; two works by the same author in the same year (or both undated) take a, b
// suffixes ("2020a", "n.d.-a"), stored as year_suffix on the reference.
function year(ref) {
  const dp = ref.issued && ref.issued["date-parts"];
  const y = dp && dp[0] && dp[0].length ? dp[0][0] : "n.d.";
  return ref.year_suffix ? y + (y === "n.d." ? "-" : "") + ref.year_suffix : y;
}
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
// APA 7: a retrieval date for undated pages whose content is designed to change (contact pages, lists of numbers).
function retrieved(ref) {
  const dp = ref.accessed && ref.accessed["date-parts"] && ref.accessed["date-parts"][0];
  if (!dp || dp.length !== 3 || !String(year(ref)).startsWith("n.d.")) return "";
  return "Retrieved " + MONTHS[dp[1] - 1] + " " + dp[2] + ", " + dp[0] + ", from ";
}
function dash(p) { return String(p).replace(/-/g, "–"); }
// APA 7: a title in another language is followed by its English translation in square brackets, not italicized.
function italicTitle(t) {
  const m = String(t || "").match(/^(.*?)( \[[^\]]+\])$/);
  return m ? "<i>" + esc(m[1]) + "</i>" + esc(m[2]) : "<i>" + esc(t) + "</i>";
}
// Sort key for APA reference lists: undated works (n.d.) before dated ones, then by year, then by a/b suffix.
function yearKey(ref) {
  const y = String(year(ref)), m = y.match(/^(\d{4})-?([a-z]?)$/), n = y.match(/^n\.d\.(?:-([a-z]))?$/);
  return m ? [+m[1], m[2] || ""] : [-1, (n && n[1]) || ""];
}
function byYear(a, b) { const ka = yearKey(a), kb = yearKey(b); return (ka[0] - kb[0]) || ka[1].localeCompare(kb[1]); }
function apaReference(ref) {
  const y = year(ref);
  const link = ref.DOI ? "https://doi.org/" + ref.DOI : (ref.URL || "");
  const au = apaAuthors(ref.author);
  const endP = t => /[.?!]$/.test(String(t || "").trim()) ? "" : ".";
  // APA 7 §9.12: a work with no author starts with its title, which is then not repeated
  let html = ref.no_author ? esc(ref.title) + endP(ref.title) + " (" + y + "). " : esc(au) + (au.endsWith(".") ? "" : ".") + " (" + y + "). ";
  if (ref.type === "article-journal") {
    html += (ref.no_author ? "" : esc(ref.title) + endP(ref.title) + " ") + "<i>" + esc(ref["container-title"]) + (ref.volume ? ", " + esc(ref.volume) : "") + "</i>" + (ref.issue ? "(" + esc(dash(ref.issue)) + ")" : "") + (ref.page ? ", " + esc(dash(ref.page)) : ref.number ? ", Article " + esc(ref.number) : "") + ". ";
    if (!ref.volume && !ref.page && !ref.number) html += "Advance online publication. ";
  } else {
    // reports and web pages: italic title, then the report number and a bracketed description (APA 7), then the publisher or site when it is not the author
    const extra = (ref.number ? " (" + esc(ref.number) + ")" : "") + (ref.genre ? " [" + esc(ref.genre) + "]" : "");
    html += italicTitle(ref.title) + extra + (extra ? "." : endP(ref.title)) + " " + (ref.publisher && ref.publisher !== ref.author[0].literal ? esc(ref.publisher) + ". " : "");
  }
  if (link) html += (ref.DOI ? "" : retrieved(ref)) + '<a href="' + esc(link) + '" target="_blank" rel="noopener">' + esc(link) + "</a>";
  // APA 7: a retracted article keeps its own details, then the retraction in parentheses (from the notice's Crossref record)
  const rn = ref.retraction_notice;
  if (rn) html += " (Retraction published " + esc(rn.year) + ", <i>" + esc(rn["container-title"]) + (rn.volume ? ", " + esc(rn.volume) : "") + "</i>" + (rn.issue ? "[" + esc(rn.issue) + "]" : "") + (rn.page ? ", " + esc(dash(rn.page)) : "") + ")";
  return html;
}
// In-text form with APA 7 disambiguation: extend surnames until the form is unique among the cited set.
// APA 7: a work with no author is cited by the first few words of its title, in title case and quotation marks
const MINOR_WORDS = new Set("a an and as at but by for if in nor of off on or per so the to up via yet".split(" "));
function shortTitleCase(title) {
  const head = String(title || "").split(/[:.?!]/)[0].trim().split(/\s+/);
  const words = head.length > 5 ? head.slice(0, 4) : head;
  return words.map((w, i) => (i > 0 && MINOR_WORDS.has(w.toLowerCase())) ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
}
function inTextLabel(ref, pool) {
  const au = ref.author.map(a => a.literal || a.family);
  const y = year(ref);
  if (ref.no_author) return "\u201C" + (ref.short_title || shortTitleCase(ref.title)) + ",\u201D " + y;
  if (au.length === 1) return (ref.author[0].short || au[0]) + ", " + y;
  if (au.length === 2) return au[0] + " & " + au[1] + ", " + y;
  const rivals = pool.filter(r => r.id !== ref.id && year(r) === y && (r.author[0].literal || r.author[0].family) === au[0] && r.author.length >= 3);
  let k = 1;
  const prefix = (r, n) => r.author.slice(0, n).map(a => a.literal || a.family).join("|");
  while (k < au.length - 1 && rivals.some(r => prefix(r, k) === prefix(ref, k))) k++;
  if (k === 1) return au[0] + " et al., " + y;
  return au.slice(0, k).join(", ") + ", et al., " + y;
}
// where a citation leads when clicked: the article's own page (its DOI), or the source's address
function refLink(ref) { return ref.DOI ? "https://doi.org/" + ref.DOI : (ref.URL || "#ref-" + ref.id); }
function cite(id) {
  const ref = refById[id];
  if (!ref) return '<span class="placeholder">[missing reference: ' + esc(id) + "]</span>";
  return '<a class="pop" href="' + esc(refLink(ref)) + '" target="_blank" rel="noopener" data-ref="' + esc(id) + '">(' + esc(inTextLabel(ref, REFS)) + ")</a>";
}
// Several works in one parenthesis, in alphabetical order (APA 7): (Author A, 2001; Author B, n.d.).
function cites(ids) {
  const items = ids.map(id => [id, refById[id]]);
  if (items.some(([, r]) => !r)) return items.map(([id]) => cite(id)).join(" ");
  items.sort((a, b) => inTextLabel(a[1], REFS).localeCompare(inTextLabel(b[1], REFS)));
  return "(" + items.map(([id, r]) => '<a class="pop" href="' + esc(refLink(r)) + '" target="_blank" rel="noopener" data-ref="' + esc(id) + '">' + esc(inTextLabel(r, REFS)) + "</a>").join("; ") + ")";
}
// Replace author-year mentions inside debate prose with live citations: (Hart et al., 2012) → link.
function liveCites(text) {
  return esc(text).replace(/\(([^()]*?\d{4}[a-z]?)\)/g, (m, inner) => {
    // split at the semicolons between citations, not at the one inside an escaped "&amp;" ("Curran &amp; Morgan, 2000")
    const parts = inner.split(/(?<!&(?:amp|lt|gt|quot|#39));/).map(s => s.trim());
    // the text is already escaped, so compare escaped labels ("Curran &amp; Morgan, 2000") and do not escape p again
    const link = (p, shown) => {
      const found = REFS.find(r => esc(inTextLabel(r, REFS)) === p);
      return found ? '<a class="pop" href="' + esc(refLink(found)) + '" target="_blank" rel="noopener" data-ref="' + esc(found.id) + '">' + shown + "</a>" : null;
    };
    const out = parts.map(p => {
      const one = link(p, p);
      if (one) return one;
      // APA 7: the same authors with several years, "(Hughes &amp; Stevens, 2010, 2012)": one link per year
      const multi = p.match(/^(.*?), (\d{4}[a-z]?(?:, \d{4}[a-z]?)+)$/);
      if (!multi) return p;
      const years = multi[2].split(", ");
      const links = years.map((y, i) => link(multi[1] + ", " + y, i === 0 ? multi[1] + ", " + y : y));
      return links.every(Boolean) ? links.join(", ") : p;
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
