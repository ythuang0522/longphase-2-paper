# Fig. 3a–c redrawn as option B, Supplementary Fig. 17 added, 2026-10-26 (author decision)

The author found Fig. 3c of option 2 (two small coverage axes, six crossing lines each) ugly and hard to
read and asked for alternatives at high-profile journal standard. Three draft PNGs were shown (A: a, b as
before with both inputs; B: a, b SNVs + SVs only; C: a, b error rate against coverage); each had a new
dot-and-range panel c. The author chose B.

- a nanopore, b PacBio HiFi: SV error rate against SVs phased correctly, SNV + SV input only, one point
  per coverage, coverage of the ends on WhatsHap.
- c: SV error rate by platform and size, SNV + SV input. Rows: nanopore and PacBio HiFi, each 50 bp–1 kb
  and ≥ 1 kb; marker = median over coverages, line = range over coverages. 1–10 kb and ≥ 10 kb are pooled
  because only 20–47 SVs ≥ 10 kb are phased per run (with three classes, HiPhase looked lower than
  LongPhase 2 at ≥ 10 kb on HiFi data from a few errors).
- The SNV + indel + SV input moved to the new Supplementary Fig. 17 (`sfig17_sv_indels()`,
  `suppfig17_sv_indels.pdf`), a, b as Fig. 3a,b. No renumbering: it follows Supplementary Fig. 16.
- Fig. 3 legend a–c, CLAUDE.md and README updated. Helpers `sv_err()`, `sv_tradeoff()`, `sv_sizes()` in
  `make_results_figs.py`.
