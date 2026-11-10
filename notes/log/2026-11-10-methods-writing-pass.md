# Methods writing review completed

2026-11-10. Author requested all fixes from the writing review. Changes are limited to
`sections/methods.tex`, the rebuilt `main.pdf`, and this log. No new measurements.

- Split dense paragraphs in read filtering, voting, benchmark scoring, evaluation metrics,
  SV evaluation and unphased-SNV analysis by purpose.
- Separated GNN inference from training and model selection. Shortened the feature list
  to its four groups and examples; full definitions remain in Supplementary Tables 12–13.
- Replaced the independent-test implication with explicit evaluation outside model fitting.
  Preserved the disclosure that these chromosomes contributed to label selection.
- Clarified read-level CpG classification, alignment exclusions, voting subjects and the
  exclusion of 5mC from read-based correction. Rewrote metric definitions with clear subjects.
- Separated SV input preparation, matching and scoring. Made the common type/size requirements
  and alternative position/overlap requirements explicit without changing thresholds.
- Rewrote the unphased-SNV comparison opening and separated classification, precision/F1,
  phase errors and genomic annotations. Restricted the replicate-1 statement to the relevant
  analyses; precision and F1 retain all SNV-only runs.
- Split Data availability by source, retaining all URLs. Preserved the author's subsequent
  TODO removals and revised Code availability statement.
- Independent text review found no substantive regression; its two residual grammar edits
  were applied. Numerical values, citations, cross-references and scientific qualifications
  were preserved.

Validation: rebuilt with the LaTeX compile skill using TeX Live; no undefined citations or
references, missing characters or overfull boxes. Methods PDF pages were rendered for visual
inspection. Underfull-box notices remain in URL-heavy text and the abstract.
