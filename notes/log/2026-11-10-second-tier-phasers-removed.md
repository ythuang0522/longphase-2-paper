# TinkerHap, Margin, Ralphi and GCphase removed; data kept, 2026-11-10

Author decision (option B): no second-tier phasers in the manuscript; keep their data in the repository in
case a reviewer asks. Before this change they were absent from Results, Discussion and the main figures
(2026-10-13, 2026-10-28) but still in Methods and the Supplementary.

## Removed
- Methods: the fourth paragraph of "Comparison with other methods" (TinkerHap, Margin, Ralphi, GCphase) and
  "comparisons with TinkerHap and HiPhase" in "Statistics and reproducibility".
- Supplementary Table 1: Margin and Ralphi blocks; title "six" → "four configurations"; legend sentences
  on Margin, Ralphi and GCphase.
- Supplementary Table 4: TinkerHap rows in three blocks; legend "HiPhase has no SNV-only mode…".
- Supplementary Table 17: Margin and Ralphi columns and the legend sentence.
- Supplementary Table 19: Margin, Ralphi and TinkerHap rows.
- Supplementary Fig. 19 (Margin and Ralphi): removed; it was the last figure, so no number changes. There
  are 18 Supplementary figures, all cited in the main text.
- Supplementary Data 1 text: figure list without Fig. 19; `Other_phasers` description without TinkerHap.
- `supplementary.xlsx`: 16 TinkerHap rows of `Other_phasers` (47 → 31 runs, No. renumbered) and the three
  trailing column blocks of `SNV_Detail` (margin_v231, ralphi, gcphase; columns AJ–BG).
- Kept: the Margin sentences of the Introduction (related work) and the hidden Results comment.

## Kept in the repository
- `notes/competitors/tinkerhap_hidden_rows.tsv` (16 rows, sheet format).
- `notes/competitors/margin_ralphi_gcphase_hidden_columns.tsv` (60 runs, 10–20x, 8 columns per tool).
- `notes/competitors/second_tier_removed_comparisons.tex.md` (8 removed source passages, verbatim).
- `notes/heldout/` (held-out values of Margin and Ralphi), `figures/supp/suppfig10_more_tools.pdf`,
  scripts in `notes/competitors/scripts/`.
- A copy of the workbook before the change is not in the repository; `git show HEAD:supplementary.xlsx`
  gives the last committed version.

## How it is done
- `HIDE = {"hb", "lh", "th", "margin", "ralphi", "gc"}` in `figures-source/make_results_figs.py`; Tables 1,
  4 and 17, the `Other_phasers` archive loader and the call of `sfig10()` follow it.
- `results_data.py` reads the archived `SNV_Detail` columns, so removing keys from `HIDE` restores the
  tables and Supplementary Fig. 19 without the workbook.
- `notes/competitors/build_sheet.py`: the three TinkerHap run definitions are commented out.
- Tables regenerated with `tables(); sv_table()` only (no figure regenerated).

## Checks
- Workbook: every cell value of the 13 other sheets is unchanged; `SNV_Detail` columns A–AI unchanged;
  `Other_phasers` rows of the other tools unchanged apart from No.
- Regenerated tables: only `snvall.tex`, `otherphasers.tex` and `heldout.tex` changed.
- PDF text scan: no TinkerHap or GCphase in main.pdf or Supplementary.pdf; Ralphi only as an Introduction
  citation (reference list); Margin only in the Introduction and in "PEPPER-Margin-DeepVariant".
- `make`: no undefined reference, no overfull box; main 28 pages, Supplementary 44 pages.
