# Independent targeted source review — reader411

Read only this brief, tasks_reader411.json, claims_reader411.json (context) and the original PDFs named in the tasks. Do not read prior reader output, study cards, editorial plans/logs, or the parent conversation. You are a fresh independent checker who did not write these anchors.

Check each extraction and its page/locator/role against the source. Read surrounding passages, not search matches alone. Use your own text extraction and PDF renders (150 dpi body text; 300 dpi tables/figures). Estric PDF and printed page numbers match; Strickland printed472 is PDF1. Recompute counts and arithmetic when relevant; distinguish printed author claims from independently checked primary findings. Watch source scope, timing, overlap, uncertainty and comparisons. No web, absent supplements, invented analysis or practical advice.

Write ONLY out_reader411.json and your own supporting material in this directory. Do not modify claims or cards. Output schema:

    {"reader":"AI reader411 (ChatGPT/OpenAI; fresh isolated context)", "date":"2026-11-09", "independence":"...", "source_access":"...", "results":[{"n":1,"claim_id":"...","anchor_index":17,"verdict":"confirmed|corrected|wrong-location|not-found","note":"...","corrected_extracted":"only if needed, entire independently checked replacement", "corrected_page":"only if needed", "corrected_locator":"only if needed"}]}

Check ALL four tasks. A correction must itself have been verified at the source. State exactly which original pages/renders were read and any material not available. Flag potential effects on the surrounding statement separately; do not silently change ratings. Return a concise summary and output path when finished.
