# Supplementary writing review completed

2026-11-10. Author requested all fixes from the full Supplementary Methods and Note
writing review. No new measurements or benchmark runs.

- Split methylation linking, allele extraction, GNN labels, model selection and
  supplementary results into paragraphs with one purpose each. Method 3 was retained.
- Clarified 5hmC probability handling, candidate clipping-based intervals and the
  mismatch-load terminology.
- Corrected the attention-coefficient terminology, node embedding description and
  focal-loss probability definition. Distinguished onset labels from benchmark agreement.
- Corrected haplotagging tag-clearing scope against local v2.1.2 Git objects. Simplified
  the indel rules and made the zero-evidence case explicit.
- Distinguished discordant SNV pairs in the switch-error rate from the separate
  switch/flip decomposition. Used completeness consistently in metric definitions.
- Defined the excess SNV switch-error rate baseline in Supplementary Note 1 and
  described the indel-pair result as a rate reduction. Specified the 60-run scope of
  the 9.3-versus-8.0 correction cost and the units of the 9–17 error count.
- Added the label-selection qualification to the chromosome comparison and the
  training-table caption. Separated the HiFi evaluation from chromosome evaluation.
- Fixed stale N50 and HiPhase panel references. Updated the read-correction,
  filtering, scoring-zone and evaluation captions and the GNN rule cross-reference.
- Changed the F1 definition to precision and completeness in both the table generator
  and its generated SNV-only table. Numerical table cells and figures were unchanged.
- Independent review found no scientific regression. Its two wording suggestions and
  whitespace fixes were applied before the final build.

Validation: Supplementary.tex and main.tex built successfully with the LaTeX compile
skill and TeX Live. Supplementary.pdf has 46 pages; main.pdf has 29. No undefined
references/citations, missing characters or overfull boxes. The supplement retains
ordinary h-to-ht float-placement notices; the main document retains seven underfull
box notices. Visually inspected 21 supplement pages, including all Methods/Note pages,
changed tables and captions. Rotation-aware PDF bounds checks found no out-of-page
text blocks in either document. git diff --check passed.

Edited sources: Supplementary.tex, figures-source/make_results_figs.py and
figures-source/supp_tables/snvall.tex. Rebuilt both PDFs. Other pre-existing manuscript,
workbook and documentation edits were preserved. The full figure generator was not run.
