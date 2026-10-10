# Suspected errors to verify (2026-10-06)

Each item is a suspicion raised while redesigning the Results, not a confirmed bug. Every one is
also a red `\todo{}` in the manuscript. Paths into `longphase/` refer to
[twolinin/longphase](https://github.com/twolinin/longphase), release **v2.1** on `main` (`46ba470`; line numbers checked 2026-10-07).
`GNN source/` is local-only (gitignored); ask JHL for the files.

## Data and analysis inconsistencies

| # | Suspicion | Evidence | How to verify |
|---|---|---|---|
| 1 | ~~**MethPhaser output equals its input.**~~ Resolved 2026-10-10 (issue #5, `eed8109`, `5fb01f5`): 0.0.3 crashed in every `methphasing` call and the wrapper ignored the exit status; 0.0.4 with the PS-lookup patch joins blocks (no `PS=-1`, no overlapping blocks). Results, Fig. 2g–i, Supplementary Fig. 11 and the `MethPhaser` sheet of Supplementary Data 1 use its own output. | `notes/methphaser/README.md`. | Done. Open outside the paper: the `twolinin/longphase` README ("SNP+Methylation") still states a longer N50 than MethPhaser (3.09 vs 2.91 Mb at 60×); MethPhaser output is 5.49 Mb. |
| 2 | ~~**HiFi variant calls are coverage-independent.**~~ Resolved 2026-10-09 (issue #4): calls regenerated per coverage, `notes/hifi/README.md`. 2,367,609–2,367,619 het SNVs from 10x to 50x. | `supplementary.xlsx` → `Variant_Calling`, rows `PB HiFi Revio`. | Check whether one call set (e.g. from full depth) was phased at every down-sampled coverage. If so, the 87% phased fraction at 10x is not comparable with nanopore (78%). |
| 3 | **Benchmark-classification counts need the confirmed input set.** The author confirmed 56,076 total unphased SNVs at 60x (2026-10-06), resolving the total. The old composition categories still sum to 60,267 and need replacement. The 549 removed sites inside the benchmark BED (413 variants), net loss of 2,055 phased benchmark SNVs in `compare`, and old composition count of 2,411 heterozygotes use different eligibility/matching definitions. | `UnphasedComposition.jsx`; `unphase_validation_results.txt`; `supplementary.xlsx` `SNV_Detail` 60x_1 phased SNV 2,193,366 → 2,191,311. | Write down the SNV filter and matching rule of each analysis (position only vs REF/ALT; inside vs outside the BED; multi-allelic handling) and recount from one site-level table. |
| 4 | **T2T validation script.** (a) Background sampled from all SNVs phased before correction, including the removed ones. (b) "No variant" means only that no assembly VCF record starts at that coordinate; alleles and overlapping complex variants are ignored. (c) chrX/chrY included. (d) chr19 "475-fold" rests on one control site and divides rounded rates (raw counts: ~483-fold). | `run_t2t_validation.sh`:80 (background drawn from `_phased.txt`), :106–110 (position-only lookup); `unphase_validation_results.txt` line for chr19. | Re-run with a control that excludes removed sites, autosomes only, allele-aware matching. |
| 5 | **GCphase looks misconfigured.** Hamming distance 32–40%, close to random phasing; switch error rate 21–26x LongPhase 2. Checked 2026-10-10 (`notes/gcphase/`): (a) GCphase loads every record whose genotype does not start with `1` and ignores FILTER, so it phased PEPPER `0/0` `refCall` records as heterozygous (1,194,969 at 10x_1, 800,489 at 20x_1); (b) on chr20 at 20x this raises the Hamming distance from 16.0% to 35.0% and the switch error rate from 0.51% to 1.40% (the control reproduces the paper run); (c) with a heterozygous-only input GCphase still has 16.0% and 0.51%, against 3.4% and 0.21% for WhatsHap and 2.0% and 0.07% for LongPhase 2, from long flipped segments inside its own blocks (none at its block joins); no further code defect found. | `supplementary.xlsx` `SNV_Detail`, `gcphase` columns; `notes/gcphase/README.md`. | To be discussed: how much the GCphase result matters for this paper, and whether to re-run it genome-wide on a heterozygous-only input. |
| 7 | ~~**SV and 5mC phased fractions have no source** (>99% of 5mC, 68–70% of SVs).~~ Resolved 2026-10-10: counted from the `_SV.vcf` and `_mod.vcf` of every co-phasing run with SVs or 5mC, without and with GNN (`notes/sv_mod/`); `SV_5mC_phasing` sheet of Supplementary Data 1. Results now 5mC 99.1–99.4%, SV 68.1–70.0%, unphased by GNN 1.4–4.6% (5mC) and 2.4–3.5% (SV), replicate 1, all contigs (was 99.0–99.4%, 68.1–70.1%, 2.4–3.8% from the missing `q10_sv_mod.tsv`). | Old pptx Fig. 4c,d; `supplementary.xlsx` had only called totals. | Done. |
| 9 | ~~**WhatsHap-only median depth (18x) and zero-entropy share (57.6%)** exist only in a commit message.~~ Resolved 2026-10-10: `notes/unphased/unphased_sets.tsv` (reproduced from the VCFs on 2026-10-09) is now the `Unphased_sets` sheet of Supplementary Data 1; 60x `wh_only`: `dp_median` 18, `pe_zero_pct` 57.6. The manuscript no longer quotes either value. | JHL commit `0025929`. | Done. |

## Code-level issues

| # | Suspicion | Evidence | How to verify |
|---|---|---|---|
| 10 | **Hamming distance includes indels** when the query phases indels, whereas switch errors are SNV-only. All co-phasing Hamming values (and WhatsHap-with-indels) therefore mix SNV and indel phasing. | `longphase/CompareProcess.cpp`:579–582 (Hamming over every common variant) vs the SNV-only switch block below it. | Re-score the indel-containing runs with SNV-only Hamming (the `onlySnvs` option, `CompareProcess.cpp`:348) and compare. |
| 11 | ~~**`--regions` filters the query too**, so N50 would depend on the benchmark BED if the BED was passed to `compare`.~~ Resolved 2026-10-10 (author): no BED and no `--regions` were passed. Command: `longphase compare --ignore-sample-name TRUTH.vcf query.vcf`, with TRUTH = `HG002_GRCh38_v5.0q_smvar.chr1_22.vcf` (v5.0q) or `HG002_GRCh38_1_22_v4.2.1_benchmark_hifiasm_v11_phasetransfer.vcf.gz` (v4.2.1) (truth first, query second; `-t` and `-o` only set threads and the output prefix; the held-out rescoring of issue #2 is the only use of `--regions`). `HG002_GRCh38_v5.0q_smvar.chr1_22.vcf` holds exactly the chr1–22 records of `HG002_GRCh38_v5.0q_smvar.vcf.gz` (no BED filter). | `/disk/research/run_full_benchmark.sh` (`run_compare`). Block N50 is computed from the phased query records only (`CompareProcess.cpp`:487–503) and does not use the truth, so it is identical under v4.2.1 and v5.0q; only a `--regions` BED would change it (:350–353), and none was passed. | Done. |

## Resolved or superseded

- Runtimes without a source (former item 6): measured by JHL (issue #3, `notes/runtime/`, 2026-10-09). Abstract and Results now use the one-thread comparison (5.4–6.3-fold at 60×); Supplementary Table 16. Memory is reported in GiB (`/usr/bin/time` gives KiB; `notes/runtime/README.md` divides by 10^6 and labels it GB).
- Plot-read values of the old Supplementary Fig. 17 (former item 8): figure deleted on 2026-10-09 (author), with the two Results sentences that quoted its values (PE = 0 share; clustering and low-GQ shares of benchmark-absent calls). The Discussion claim about candidates an entropy threshold would miss is now worded as a possibility.
- Training/evaluation overlap (former item 13): held-out chr17/21/22 rescored by JHL (issue #2, `notes/heldout/`, 2026-10-09); Results, Supplementary Table 15 and Supplementary Method 4 report them. GNN correction removes 14–23% of switch errors there against 31–33% genome-wide; the advantage over WhatsHap/HapCUT2 is unchanged.
- Total SNVs unphased at 60x: **56,076**, confirmed by the author on 2026-10-06; the old 60,267 total is superseded.

- Small-variant caller: PEPPER-Margin-DeepVariant, not Clair3 (author, 2026-10-05); release and preset still missing.
- Supplementary Method 6 claimed switch rate and Hamming "share one denominator"; corrected.
- Several numerical overstatements in Results/Discussion (e.g. "at least halves", "exactly as accurate") corrected on 2026-10-05; see README.

## Missing analyses (not errors, but required)

Matched-retention comparison (GNN vs entropy/support thresholds, random removal, HapCUT2 pruning);
common-region vs benchmark-specific scoring; a second individual with frozen weights.
