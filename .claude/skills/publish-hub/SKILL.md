---
name: publish-hub
description: Rebuild and republish the LongPhase 2 manuscript hub artifact (https://claude.ai/artifact/339iTVSwod8JqKgQASYfZm). Use ONLY when the user explicitly asks to publish or update the hub — never as a side effect of editing, building or committing.
---

# Publish the manuscript hub

Same pattern as `../../multimodal/multimodal-diagnosis-paper/notes/hub/build_hub.py`. The URL
never changes. Needs poppler (`pdfinfo`, `pdftoppm`) and `rsvg-convert`.

Before publishing, check that the stat boxes, flags and captions in `notes/hub/build_hub.py`
match the manuscript (figure count, supplementary counts, the "Open before submission" items
from README).

1. `make`, then confirm `grep -c undefined main.log Supplementary.log` prints 0 for both.
2. `python3 notes/hub/build_hub.py` → writes `hub-build/` (gitignored): `index.html`, both PDFs,
   `pages/main-NN.jpg` / `pages/supp-NN.jpg` at 110 dpi, `figures/figN.png` and `figures/suppfigN.png`,
   plus `files.json` (publish list) and `files_with_removals.json` (same plus `null` for page paths a
   longer earlier build may have left behind).
3. In a new session, first run the Artifact tool with `action: list`, `scope: files` on that URL
   (required before a republish is accepted).
4. Publish `hub-build/index.html` with `url` = that URL, `root: hub-build`, `files` = the list printed
   by the script; add `null` entries for any page path the listing shows but the new build lacks.
   Omit `icon` on a redeploy. Report the link and version number.

If the publish is refused because the live version has not been viewed, do not pass `force: true`
without the user's explicit go-ahead.
