# Figure 5: WhatsHap phasing errors and recall

Author-approved terminology changes, 2026-11-11.

- Figure 5d: title "WhatsHap phasing errors"; keys "Unphased by LongPhase 2"
  and "All phased by WhatsHap"; Y-axis "Incorrectly phased SNVs (%)".
  The caption retains the assessable benchmark-SNV populations and identifies
  block-wise Hamming comparison as the error definition.
- Figure 5f: "Recall" replaces "Completeness". The benchmark-SNV Y-axis is unchanged.
- Results now names precision, recall and their harmonic mean F1 explicitly,
  including the HiFi comparison. Discussion uses recall consistently.
- Methods and Supplementary Method 6 define "Recall (phasing completeness)":
  benchmark heterozygous variants matched in position and alleles and phased,
  divided by all benchmark heterozygous variants of that class. Phase correctness
  is not required. F1 therefore does not measure phase correctness.
- Supplementary Note 1, Fig. 6a and its caption, Fig. 18's caption, and Tables 1
  and 3 use the same terminology. GNN error-class metrics retain their distinct
  definitions. Table and figure data and calculations are unchanged.

Validation:

- Regenerated Figure 5, Supplementary Fig. 6 and the generated tables from
  `figures-source/make_results_figs.py`. Only Tables 1 and 3 changed.
- Compiled Supplementary.pdf (44 pages), then main.pdf (28 pages), with the
  latex-compile skill and the installed TeX Live toolchain. Both passed.
- No undefined references, missing characters or overfull boxes. Remaining
  messages concern underfull text boxes and LaTeX's automatic h-to-ht float placement.
- Rendered both full figures and all their panels at higher resolution. Rendered
  and inspected Figure 5 on main.pdf page 13, its final figure/caption crops,
  the revised main-text pages, and the affected Supplementary definition,
  table and figure pages. No visible text collisions or clipping.
- Exported text-preserving SVGs from the same final Matplotlib figures for
  browser QA. Playwright checked 139 and 91 text elements, respectively:
  none extended beyond the canvas or intended panel bounds. Axis-aligned box
  overlap candidates for rotated/multiline labels and densely spaced chromosome
  ticks were visually checked; the rendered text remains separate.
- Arial and Arial Bold are embedded in Figure 5. Independent text and visual
  reviews passed; `git diff --check` passed.

Temporary QA scripts, renders and browser reports are under `tmp/terminology-qa/`.
