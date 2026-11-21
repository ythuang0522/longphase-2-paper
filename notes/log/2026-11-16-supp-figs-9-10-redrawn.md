# 2026-11-16 Supplementary Figs. 9 and 10 redrawn (options 9A and 10A)

Author: Supplementary Figs. 9 and 10 did not look professional. Options offered: 9A four steps,
9B one worked region, 9C style fix; 10A three steps, 10B two figures, 10C style fix. Draft PNGs of
9A, 9B, 10A and 10B are in `notes/drafts/2026-11-16-sfig9-10/`. Author chose 9A and 10A.

- New script `figures/supp/make_supp_schematics.py` (matplotlib, Arial, 160 mm, glyphs of Fig. 1)
  writes `suppfig7_modcall.pdf` (Supplementary Fig. 9) and `suppfig1_observations.pdf`
  (Supplementary Fig. 10) directly. `fig_s1()` and `fig_s7()` removed from `make_supp_figs.py`;
  their SVGs deleted, so the Makefile SVG→PDF rule no longer overwrites the two PDFs.
- Supplementary Fig. 9: a read classification, b candidate selection, c linkage test with the three
  stages, d merging and output (order of the Methods steps). Panel d checked against the source:
  `ModCallParsingBam.cpp` `applyCpGStrandPairGenotype()` pairs the forward-strand C at pos with the
  reverse-strand G at pos+1, and `ParsingBam.cpp` (METHParser) merges consecutive positions into one
  node, so the panel shows the two strands of one CpG, not two CpGs.
- Supplementary Fig. 10: a alignment selection (overlap ≥ 0.2 of combined span, shorter discarded;
  `PhasingGraph.cpp:748`), b allele extraction, c copy-number-aware filter (clip profile and two MR
  examples). No longer drawn: homopolymer SNV filter (text in Supplementary Note 1), tandem-repeat
  flag (already in Supplementary Fig. 11b), scanner state machine (Supplementary Note 1 text and
  table), order of operations. Example counts are illustrations.
- Legends of both figures rewritten; Supplementary Fig. 10 now at `\textwidth`; Supplementary
  Note 1 citation "Supplementary Fig. 10e,f" → "10c"; `[optional figure]` comment updated (d → c).
- CLAUDE.md figure-generation note updated.
