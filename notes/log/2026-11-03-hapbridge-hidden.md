# HapBridge hidden from the manuscript, 2026-11-03 (author decision)

HapBridge is a bioRxiv preprint (Nov 2025, v4 Jan 2026) with little public use (GitHub Humonex/HapBridge:
2 stars, 1 fork, no issues, no release, not on Bioconda; checked 2026-11-03). LongHap (bioRxiv 2026, on
Bioconda, compares itself with LongPhase) stays. The HapBridge results are hidden, not deleted, in case a
reviewer asks for them.

- Figures: `HIDE = {"hb"}` in `figures-source/make_results_figs.py` removes HapBridge from Fig. 3d,e,
  Supplementary Fig. 16e and Supplementary Table 17 (rows and caption). Empty the set to show it again.
- Results: "four phasers that use 5mC" became "three"; the HapBridge sentence is an `[author-hidden]` comment.
- Methods: "Four further phasers" became "Three"; the HapBridge input clause is an `[author-hidden]` comment.
- Discussion: "than MethPhaser and HapBridge, which post-process" became "than MethPhaser, which post-processes".
- Supplementary: Table 5 row commented out; Supplementary Fig. 16 caption names MethPhaser and LongHap only.
- Supplementary Data 1: the 6 HapBridge rows of sheet `Other_phasers` moved to
  `notes/competitors/hapbridge_hidden_rows.tsv` (rows renumbered, 71 → 65; other sheets unchanged);
  `build_sheet.py` leaves HapBridge out; the sheet description in `Supplementary.tex` no longer names it.
  With `HIDE` emptied, `_other_phasers()` reads the TSV back.
- Kept: the Introduction citation (related work, not a result), the bib entry and `notes/competitors/`.
