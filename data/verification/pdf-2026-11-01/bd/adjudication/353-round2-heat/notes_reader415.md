Independent source/arithmetic notes — reader415 — 2026-11-10

Scope and independence
Read only the assigned brief, tasks_reader415.json, claims_reader415.json, and originals named there. No cards, previous findings/ledgers/plans/history, outside sources, or delegated work. No changes outside assigned output directory and tmp/pdfs/reader415/. No claims or ratings changed.

Original PDF access and rendering
Marzuk original: six PDF pages = printed 1795–1800. Poppler text extraction returned six form feeds; scientific reading was by all six own 150dpi page images. Own 300dpi fitz renders cover printed 1796–1799, and all four figures/two tables were inspected at that scale. Crandall original: seven PDF pages = printed 785–791. Own text extraction plus all seven own 150dpi page images read. Own 300dpi fitz renders cover printed 786–789. All three figures inspected at 300dpi; independent quantitative readings used crops retaining that pixel scale. Poppler warnings did not prevent readable page images. No repair or alteration of either original PDF was made.

Anchor 4 — Marzuk threshold construction
Printed 1796 right column: weather data cover 1990–1995; all certified hyperthermia deaths in that same six-year interval are sampled, excluding unintentional drug-overdose classification. Of 48 certified hyperthermia deaths, 10 had benzoylecgonine; their daily maximum temperatures had median 30.9°C, range 17.2–39.4°C (mean 29.6°C, SD6.1°C). Index sample is explicitly January 1, 1990 to December 31, 1992, 1096 days and 1382 fatal cocaine overdoses. The plot is cumulative in temperature (deaths on days at or above each given threshold), rather than one independent estimate per temperature bin. Printed 1797 left-column continuation explicitly bases 31.1°C on BOTH the hyperthermia-date median and index-sample plot. Hot-day rule includes the current or preceding day’s maximum reaching the threshold. Statistical Analysis then uses 1993–1995 as a distinct index-sample validation window. The overlap of the OTHER threshold input (hyperthermia dates 1990–1995) with validation dates is direct; lack of wholly demonstrated independence is an editorial inference, not proof of how much bias occurred. Proposed extraction is accurately scoped and located.

Anchor 10 — Crandall temperature response
Printed 787 Statistical Analysis specifies two-way repeated-measures analysis for responses during heat stress. Printed 788 Results third paragraph gives P<.001 for augmented progressive esophageal temperature under cocaine; no final temperature values or final temperature difference are stated in the text. Figure 1 legend identifies solid cocaine/dotted lidocaine, mean ±SE, P<.001 for cocaine versus lidocaine. At final time near 38min, own tick-calibrated Figure 1 bottom panel gives ~37.79°C and ~37.55°C; their difference is ~.24°C. Endpoint means and SE bars were distinguished. Plot readout is approximate, not raw exact means or a risk threshold. Proposed extraction confirmed.

Anchor 12 — Crandall conductance, sweat, and significance labels
Printed 786 Measurements explicitly defines conductance as laser-Doppler signal / mean arterial pressure and says forearm is not covered by heating suit. Printed 787 assesses maximum with local skin42°C for30min, averages the final minutes, calculates maximum conductance using mean arterial pressure, and normalizes each site to its maximum. This is a pressure-adjusted conductance index, not skin flow alone.
Printed 788 Results explicitly says highest common esophageal temperature37.86°C, conductance49±9 vs70±5%maximum (P=.03), sweat.8±.2 vs1.0±.1mg/cm²/min (P=.04), cocaine versus lidocaine. Study enrolled7; the particular number contributing at this highest temperature is not separately given. Text-versus-plot endpoint values differ, but mechanisms of averaging/available participants cannot be reconstructed from this article.
Own Figure 2 upper panel final solid value ~54.2%; final dotted ~66.8%, consistent with about54–55 versus67. Lower panel solid endpoint ~.86mg/cm²/min, dotted endpoint ~1.05mg/cm²/min. The latter is a modest correction to proposed1.07; it is visibly lower than1.07 against both full-axis and nearest-tick calibration. Figure 2 legend expressly identifies cocaine versus lidocaine and mean±SE. Its P<.01 label does not name an endpoint/temperature or exact model term. Printed 787 Statistical Analysis describes two-way repeated-measures comparisons throughout heat stress. Thus “does not identify its statistical contrast” is too broad: group contrast IS specified; endpoint and model term are not. Do not call P<.01 versus.03/.04 a proven error for an identical endpoint comparison. Figure1 mean lidocaine endpoint ~37.55°C is indeed below37.86°C; this alone cannot diagnose why Figure2/text differ.

Independent pixel arithmetic
All coordinates below refer to my own 300dpi crops in tmp/pdfs/reader415/. Pixel y increases downward. Tick centers were manually inspected and checked against black horizontal tick strokes. Each linear calibration uses all labelled y ticks; small nonuniform spacing in the scan and stroke width mean these are approximate, with more digits retained below only for reproducibility. Endpoint coordinates are mean-line locations, not SE-bar tips.

{
  "label": "Crandall Figure 1 core, crop crandall300-4-core.png",
  "tick_y": [
    24.5,
    217.5,
    418.5,
    618.5
  ],
  "tick_values": [
    38.0,
    37.6,
    37.2,
    36.8
  ],
  "endpoint_y_cocaine_lidocaine": [
    127,
    248
  ],
  "intercept": 38.04492888319858,
  "slope": -0.0020169785244678173,
  "calibrated_endpoints_cocaine_lidocaine": [
    37.78877261059117,
    37.54471820913056
  ]
}

{
  "label": "Crandall Figure 2 conductance, crop crandall300-5-conductance.png",
  "tick_y": [
    35,
    209.5,
    388.5,
    565.5,
    742
  ],
  "tick_values": [
    80,
    60,
    40,
    20,
    0
  ],
  "endpoint_y_cocaine_lidocaine": [
    263,
    151
  ],
  "intercept": 83.85258943923871,
  "slope": -0.1129930158187031,
  "calibrated_endpoints_cocaine_lidocaine": [
    54.135426278919795,
    66.79064405061455
  ]
}

{
  "label": "Crandall Figure 2 sweat, crop crandall300-5-sweat.png",
  "tick_y": [
    30,
    259,
    499.5,
    736.5
  ],
  "tick_values": [
    1.2,
    0.8,
    0.4,
    0
  ],
  "endpoint_y_cocaine_lidocaine": [
    229,
    118
  ],
  "intercept": 1.246123215822928,
  "slope": -0.0016947494185519418,
  "calibrated_endpoints_cocaine_lidocaine": [
    0.8580255989745333,
    1.046142784433799
  ]
}

For Figure1 core, x ticks at approximately[32,129,222,317,409,503,598,691,788] represent[0,5,10,15,20,25,30,35,40]min; final curve x≈753 corresponds to38.1min. The two temperatures differ by about.244°C before rounding. For Figure2 conductance, using 0–80 directly yields the same ~54 and67% endpoints. For Figure2 sweat, the nearest0.8/1.2 interval alone gives lidocaine about1.05, consistent with the full-axis fit. No inferential statistics were recomputed from digitized plots.

Verdicts: confirmed2; corrected1; wrong-location0; not-found0. Output: out_reader415.json.
