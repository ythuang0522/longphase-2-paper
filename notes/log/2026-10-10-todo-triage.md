# Todo triage, 2026-10-10 (author)

**Todo triage, 2026-10-10 (author).** Removed as not blocking: the Methods `\todo`s on the per-run
threshold sweep and trade-off panel (Supplementary Method 4 gives the criterion and the result), on
region-filter commands and a metric table (scoring used no benchmark BED; Methods and Supplementary
Method 6 define eligibility, numerators, denominators and blocks), and on the v5.0q chr1–22 command
and source data (author: a Nature paper does not print the awk command; the chr1–22 restriction is
stated in Methods and Supplementary Table 5; the awk provenance comment stays).
- Supplementary Fig. 9 (calibration placeholder) removed with its `\todo` in Supplementary Method 3;
  no sentence cited it. Supplementary Figs. 10–15 are now 9–14: literal references renumbered in
  `sections/results.tex`, `Supplementary.tex` (Supplementary Data 1), source comments,
  `make_results_figs.py` section headers and CLAUDE.md. The PDF file names (`suppfig10_*`–`suppfig15_*`)
  keep their old numbers. Earlier entries in this log use the old numbers.
- Still open: the MethPhaser N50 sentence (waits for JHL, issue #5), SV and 5mC counts to
  Supplementary Data 1 (`q10_sv_mod.tsv`), `analyze_unphased.py` and the training/analysis scripts
  in the public repository.
- Supplementary Method 2: the scanner-constant `\todo` replaced by a "Choice of constants" paragraph
  (author: inspection of HG002 clipping profiles at CNV segments with many false SNV calls, no sweep;
  A from the read length; absolute counts at every coverage; sensitivity not assessed).
- Supplementary Method 2, "State": the ramp state no longer cites breakage–fusion–bridge cycles (a
  tumour-genome mechanism; the scanner was designed on HG002, author 2026-10-10).
- Supplementary Table 5, MethPhaser row: command line added from `notes/methphaser/README.md`
  (haplotag v2.0.2, primary records, `meth_phaser_parallel` `-vc`/`-g`, post-processing, the local
  `str()` fix and the VCF repair by `fix_methphaser_vcf.py`).
