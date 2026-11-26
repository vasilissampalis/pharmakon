#!/usr/bin/env python3
"""Claim writer 757: plain lines and myth-or-fact items -> data/verification/pdf-2026-11-26/757_simple.json; prints grades."""
import json, re, sys

OUT = sys.argv[1]
V = "0.1.0"

simple = {
    "_note": ("Plain lines and myth-or-fact items by AI reader 757 (claim writer), round pdf-2026-11-26, 26 November 2026, "
              "written from the draft claims in data/claims/_incoming/pdf1126_w757.json (version 0.1.0); for the editor's "
              "merge into data/site/simple.json."),
    "claims": {
        "cl_benzo_liking": {
            "q": "Do benzos get you high, and who actually likes them?",
            "pages": ["benzodiazepines"],
            "short": ("Depends who you are. In one lab study, 27 of 36 people without drug problems mostly chose a dummy pill "
                      "over Valium. People with past drug problems almost always chose benzos."),
            "but": ("But those people were tested in other labs' studies, mostly with much bigger doses. So we can't tell "
                    "if their past made the difference."),
            "how": [
                ("In a 1980s study, 36 young volunteers with no history of drug problems (most had tried cannabis) tried Valium "
                 "and a dummy pill, then chose between them five times. Most picked the dummy pill, anxious or not."),
                ("Valium calmed them and made them sleepy and a bit muddled. It didn't raise their scores for euphoria. At "
                 "the higher dose they felt more tired and less cheerful than on the dummy pill."),
                ("A review of older lab studies found that people with a history of drug problems almost always chose benzos. "
                 "Moderate drinkers chose Valium more than light drinkers did. Anxious people chose benzos when they could "
                 "take them as needed."),
                ("Outside the lab, some people say they get high. In an older US school survey, about half of teens who took "
                 "calming pills without a prescription said they usually got high. In a newer adult survey, 12 in 100 who "
                 "misused benzos said getting high was their main reason."),
            ],
            "how_src": [["de-wit_1986"], ["de-wit_1986"], ["griffiths_1997"], ["griffiths_1997", "maust_2019"]],
            "rate": ("Small, old lab studies. The one read in full was careful, but the comparison between kinds of people "
                     "comes second-hand from a review of separate studies that used very different doses."),
            "v": V,
        },
        "cl_benzo_misuse_reasons": {
            "q": "Why do people misuse Xanax and other benzos?",
            "pages": ["benzodiazepines", "general"],
            "short": ("Mostly to relax or sleep, they say. In a big US survey, 47 in 100 people who misused benzos named "
                      "relaxing as the main reason, 27 sleep, and 12 getting high."),
            "but": ("It's what people told a survey. And 'misuse' here also counts taking more of your own pills than your "
                    "doctor said."),
            "how": [
                ("In a US survey in 2015 and 2016, about 13 in 100 adults had used a benzo in the past year. About 2 in 100 "
                 "had misused one. At ages 18 to 25, about half of all benzo use was misuse."),
                ("Misuse meant any use a doctor didn't direct. Most often (74 in 100) it was pills without a prescription. "
                 "Three in four had misused alprazolam (Xanax)."),
                ("Main reasons: relaxing 47 in 100, sleep 27, getting high 12, coping with feelings 10. These add up to a bit "
                 "over 100, and the paper doesn't say why."),
                ("About 69 in 100 got the pills from a friend or relative, mostly for free, and 20 in 100 from one doctor. "
                 "About 7 in 100 met the criteria for dependence."),
            ],
            "how_src": [["maust_2019"], ["maust_2019"], ["maust_2019"], ["maust_2019"]],
            "rate": ("One big national survey of US adults, chosen to stand for the whole country. But it's people's own "
                     "answers, nobody checked them, and people in institutions such as prisons, or in the military, weren't asked."),
            "v": V,
        },
    },
    "tf": {
        "benzodiazepines": [
            {"claim": "cl_benzo_liking",
             "statement": "Most people would pick Valium over a dummy pill.",
             "answer": False, "v": V,
             "why": ("In a lab study, most young volunteers without drug problems chose the dummy pill. It was one small "
                     "study, and people with a history of drug problems did choose benzos in other studies.")},
            {"claim": "cl_benzo_liking",
             "statement": "People with anxiety liked Valium more than others in a lab test.",
             "answer": False, "v": V,
             "why": ("In one small study, anxious volunteers neither chose nor liked it more, though it eased their anxiety. "
                     "Studies that let anxious people take it as needed did find a preference.")},
            {"claim": "cl_benzo_misuse_reasons",
             "statement": "Most people who misuse benzos say they do it to get high.",
             "answer": False, "v": V,
             "why": ("In a big US survey, 12 in 100 named getting high as their main reason. Relaxing (47 in 100) and sleep "
                     "(27) came first, by people's own account.")},
        ],
        "general": [
            {"claim": "cl_benzo_misuse_reasons",
             "statement": "Most people who misuse benzos are hooked on them.",
             "answer": False, "v": V,
             "why": ("In a big US survey, about 7 in 100 people who misused benzos met the criteria for dependence. 'Misuse' "
                     "there includes taking your own pills more often than prescribed.")},
        ],
    },
}


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    m = re.findall(r"[aeiouy]{1,2}", w)
    return len(m) if m else 1


def grade(t):
    words = [x for x in t.split() if x]
    sents = max(1, len(re.findall(r"[.!?]+", t)))
    sy = sum(syl(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * sy / len(words) - 15.59


for cid, c in simple["claims"].items():
    print(cid, "q words", len(c["q"].split()))
    for k in ("short", "but"):
        print("  ", k, round(grade(c[k]), 1), len(c[k].split()), "words")
    for i, t in enumerate(c["how"]):
        print("   how", i, round(grade(t), 1), len(t.split()), "words")
    print("   rate", len(c["rate"].split()), "words")
for page, lst in simple["tf"].items():
    for x in lst:
        print("tf", page, round(grade(x["statement"]), 1), len(x["statement"].split()), "|", x["statement"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(simple, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", OUT)
