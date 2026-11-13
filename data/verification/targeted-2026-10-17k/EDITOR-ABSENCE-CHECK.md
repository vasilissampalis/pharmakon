# Editor's check of the absence claims in the sponsor's briefing (2026-10-17)

AI reader 44 confirmed tasks 24, 62, 70 and 94 from the briefing document's text layer. It noted that the document's 74 pages that are images only were not searched. These anchors say the document does not report something:
- a blinding survey or any measure of expectancy;
- results of the UFEC health-care-use measure, or the follow-up's health-economics data;
- the interim psychotherapy, medicines and illicit MDMA use collected at follow-up.

The editor rendered the 74 image-only pages at 150 dpi, ran them through OCR (tesseract), and searched the text for these terms:
- "blinding survey", "guess" and "expectan";
- "UFEC" and "health econ";
- "illicit", "interim psycho" and "psychotherap";
- "retract", "Mithoefer", "Jerome", "Feduccia" and "Ponte".

Results:
- **UFEC** appears only on p. 50, as the measure's definition in the table of measures.
- **"illicit"** appears only on p. 103, in the risk-management plan (education on substitution with illicit MDMA).
- **"psychotherapy"** appears only in descriptions of the treatment programme (pp. 16, 28, 29, 41, 42).
- **None of the other terms** appears.

The absence anchors therefore hold for the image-only pages as well, within the limits of OCR. The OCR text is in `scratchpad/editor_ocr/` and was not used for anything else.
