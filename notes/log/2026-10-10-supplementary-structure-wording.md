# Supplementary structure and wording, 2026-10-10 (Codex; revised review plan)

**Supplementary structure and wording, 2026-10-10 (Codex; revised review plan).**
- Added all six Supplementary Methods to the contents page.
- Method 3 now separates the tuned constants from their selection history and refers
  to the main Methods for the voting rule and base-quality weighting. The same-individual
  tuning and non-held-out chromosome caveats remain explicit. Constants now use plain
  names rather than unused parameter symbols; their values are unchanged. Supplementary
  Fig. 2b points to the main Methods for the voting rules.
- Method 4 keeps the main Methods' use-first, training-second order. Its title now
  names features, architecture, inference, training, threshold selection and export. Scoring-zone
  and inference details have their own paragraph, and training augmentations follow
  labels and class balance/loss. Model values, equations and selection criteria are unchanged.
- Method 6 separates block intersection, switch errors/flips, Hamming distance,
  phased fraction and block N50. Each metric carries its own denominator; the duplicate
  switch-rate definition is removed. N50 now explicitly excludes query phase sets with
  fewer than two variants and uses their first-to-last variant spans independently of
  truth/query intersection, consistent with `../longphase/CompareProcess.cpp:487-504`.
  Method 6 starts on a fresh page to keep its heading with the metric definitions.
- Supplementary Data 1 has an unnumbered two-column inventory of its 11 sheets,
  defining all six composition codes (`lp_only`, `wh_only`, `lp_only_phase`,
  `lp_only_gnn`, `both`, `background`), run coverage and figure/table links. The
  distinction between `both` (unphased by both) and `background` (phased by both) is
  explicit, with their corresponding Table 17 row labels.
  Calls left unphased by both tools are correctly limited to the composition and depth
  sheets; the intervals sheet contains the two tool-only groups. The inventory uses
  `tabular`, so it does not advance the table counter.
- Shortened the Table 17 caption in `figures-source/make_results_figs.py` and ran
  its `tables()` function to regenerate `figures-source/supp_tables.tex`. The caption
  retains the call universe, benchmark categories, graph/GNN stage split and three-part
  table description; it refers to main Methods, "Analysis of unphased SNVs", for
  wrong phase, switch-error intervals and expected share. The caption now defines
  fold as inside divided by expected. No definitions were moved.
- Converted Table 5 to `longtable` with continuation headers and a wider Notes column,
  retaining every row verbatim. It now fits on page 12, including the full LongPhase 1.0
  commit and LongPhase 2 v2.1 commit `46ba470`, without footer overlap or clipping.
  Table 6 starts on page 13; the tables are in the correct order.

Validation: Supplementary.pdf rebuilt (36 pages; previously 35) and main.pdf rebuilt
(26 pages) with TeX Live. Revised Methods, contents, Tables 5–6 and 17, and Data 1 pages
were rendered and inspected. All 17 table labels/numbers are unchanged. All Table 5
rows are unchanged. The generated Tables 7–17 diff contains only the Table 17 caption;
all data rows are unchanged. Main PDF text is identical to the previous committed PDF.
No undefined references, undefined citations or missing characters; `git diff --check`
passes. The former Table 5 height warning is resolved. The existing Table 17 middle
column-width warning (9.25 pt), main title/affiliation and underfull warnings remain.
No figure artwork, numerical results, main manuscript source or internal notes changed.
