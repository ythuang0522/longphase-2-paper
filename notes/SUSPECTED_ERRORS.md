# Suspected errors to verify (2026-10-06)

Each item is a suspicion raised while redesigning the Results, not a confirmed bug. Every one is
also a red `\todo{}` in the manuscript. Paths into `longphase/` refer to
[twolinin/longphase](https://github.com/twolinin/longphase), branch **JH** (line numbers checked at `f7bd878`, 2026-10-06; unchanged since `cc17fb1`).
`GNN source/` is local-only (gitignored); ask JHL for the files.

## Data and analysis inconsistencies

| # | Suspicion | Evidence | How to verify |
|---|---|---|---|
| 1 | **MethPhaser output equals its input.** Its switch errors, phased %, Hamming and N50 match the uncorrected SNV-only LongPhase 2 run to every printed digit at all six coverages. | `MethPhaserCompare.jsx` vs `supplementary.xlsx` → `SNV_Detail`, `longphase_v2.0.1`, replicate 1 (e.g. 10x: 2277, 78.11491, 6.92789, 939511). | Confirm the MethPhaser *output* VCF was scored and that MethPhaser ran to completion; diff its input and output VCFs. |
| 2 | **HiFi variant calls are coverage-independent.** 2,367,609–2,367,619 het SNVs from 10x to 50x. | `supplementary.xlsx` → `Variant_Calling`, rows `PB HiFi Revio`. | Check whether one call set (e.g. from full depth) was phased at every down-sampled coverage. If so, the 87% phased fraction at 10x is not comparable with nanopore (78%). |
| 3 | **Unphased-SNV counts do not reconcile** for the same 60x replicate: 60,267 (composition) vs 56,076 (T2T script); 549 removed sites inside the benchmark BED (413 variants) vs a net loss of 2,055 phased benchmark SNVs in `compare` vs 2,411 "heterozygous in benchmark" in the composition. | `UnphasedComposition.jsx`; `unphase_validation_results.txt`; `supplementary.xlsx` `SNV_Detail` 60x_1 phased SNV 2,193,366 → 2,191,311. | Write down the SNV filter and matching rule of each analysis (position only vs REF/ALT; inside vs outside the BED; multi-allelic handling) and recount from one site-level table. |
| 4 | **T2T validation script.** (a) Background sampled from all SNVs phased before correction, including the removed ones. (b) "No variant" means only that no assembly VCF record starts at that coordinate; alleles and overlapping complex variants are ignored. (c) chrX/chrY included. (d) chr19 "475-fold" rests on one control site and divides rounded rates (raw counts: ~483-fold). | `run_t2t_validation.sh`:80 (background drawn from `_phased.txt`), :106–110 (position-only lookup); `unphase_validation_results.txt` line for chr19. | Re-run with a control that excludes removed sites, autosomes only, allele-aware matching. |
| 5 | **GCphase looks misconfigured.** Hamming distance 32–40%, close to random phasing; switch error rate 21–26x LongPhase 2. | `supplementary.xlsx` `SNV_Detail`, `gcphase` columns. | Re-run with the authors' recommended nanopore parameters. |
| 6 | **Runtimes have no source.** 3/15 min (LongPhase 2), 26/95 (HapCUT2), 26/115 (WhatsHap) were read off an old pptx figure; the repo README times `phase` at 39–180 s. | `sections/results.tex` runtime sentence. | Supply wall-clock and peak memory per tool and coverage, with hardware and threads. JH commit `f7bd878` (2026-10-06) adds v2.1 timings to the longphase README; check whether they settle this. |
| 7 | **SV and 5mC phased fractions have no source** (>99% of 5mC, 68–70% of SVs). | Old pptx Fig. 4c,d; `supplementary.xlsx` has only called totals. | Add phased SV/5mC counts per run. |
| 8 | **Values in Supplementary Fig. 17** (old Fig. 6b,c: depth/informativeness, entropy 0 in 22–43% of removed hets) are plot-read. | `figures/supp/suppfig17_unphased_depth_entropy.png`. | Recompute from the source table. |
| 9 | **WhatsHap-only median depth (18x) and zero-entropy share (57.6%)** exist only in a commit message. | JHL commit `0025929`. | Add the per-set summary to Supplementary Data 1. |

## Code-level issues

| # | Suspicion | Evidence | How to verify |
|---|---|---|---|
| 10 | **Hamming distance includes indels** when the query phases indels, whereas switch errors are SNV-only. All co-phasing Hamming values (and WhatsHap-with-indels) therefore mix SNV and indel phasing. | `longphase/CompareProcess.cpp`:579–582 (Hamming over every common variant) vs the SNV-only switch block below it. | Re-score the indel-containing runs with SNV-only Hamming (the `onlySnvs` option, `CompareProcess.cpp`:348) and compare. |
| 11 | **`--regions` filters the query too**, so N50 would depend on the benchmark BED if the BED was passed to `compare`. | `longphase/CompareProcess.cpp`:353. N50 is identical under v4.2.1 and v5.0q in every run, which suggests the BED was applied to the truth VCF beforehand. | Record the exact `compare` commands. |
| 12 | **GNN training labels.** The truth parser accepts unphased genotypes and keeps no REF/ALT or truth phase set; labels compare phase within query phase sets only. Allele mismatches or truth-block crossings could mislabel windows. | `GNN source/prepare_gnn_data_10.py`:343 (parser), :440 (`compare_phase_relative`). Local only. | Audit the training records for allele mismatches, unphased truth and truth-block crossings; if any, correct the labels and retrain. |
| 13 | **Training/evaluation overlap.** Genome-wide rates include the 17 chromosomes that supplied training windows, on the same down-sampling replicates. | `sections/methods.tex`, "Hold-out design". | Report end-to-end metrics with and without GNN on the held-out chr17, chr21, chr22 (`longphase compare --regions`). |

## Resolved or superseded

- Small-variant caller: PEPPER-Margin-DeepVariant, not Clair3 (author, 2026-10-05); release and preset still missing.
- Supplementary Method 6 claimed switch rate and Hamming "share one denominator"; corrected.
- Several numerical overstatements in Results/Discussion (e.g. "at least halves", "exactly as accurate") corrected on 2026-10-05; see README.

## Missing analyses (not errors, but required)

Matched-retention comparison (GNN vs entropy/support thresholds, random removal, HapCUT2 pruning);
common-region vs benchmark-specific scoring; a second individual with frozen weights.
