# Supplementary Fig. 2 added: Fig. 2a,b inside the v5.0q benchmark regions; Supplementary Figs. 2–17 renumbered 3–18, 2026-11-10 (author decision, option A)

## Why

Reviewer-style reading of Figs. 2–5 (2026-11-10): Fig. 2 scores the v5.0q truth VCF in full, without a
benchmark BED, and the Fig. 4 text says that sites outside both benchmarks give 50–77% of the genome-wide
difference in switch-error counts. A reviewer would ask for Fig. 2 inside the benchmark regions. The author
chose option A after a draft PNG (genome-wide against in-benchmark): a new Supplementary figure and one
Results sentence; Fig. 2 unchanged. Options not taken: B, replace Fig. 2a,b; C, faint in-benchmark lines in Fig. 2a.

## What

- `figures-source/make_results_figs.py`: new `sfig_in_benchmark()` → `figures/supp/suppfig_in_benchmark.pdf`
  (1 × 2, axes as Fig. 2a,b). a nanopore SNVs (LongPhase 2, WhatsHap, HapCUT2; `item4_strata.tsv`, region
  `v5bed`, stratum `any`, truth v5); b nanopore SNVs and indels (LongPhase 2, WhatsHap; `item3_indel.tsv`,
  region `v5bed`; solid SNV pairs, dotted pairs with an indel). Mean of the replicate rates per coverage.
- `Supplementary.tex`: figure and legend inserted as Supplementary Fig. 2 (first citation directly after
  Supplementary Fig. 1b in the nanopore paragraph of the Fig. 2 Results).
- `sections/results.tex`: one sentence at the end of the nanopore paragraph. Values over all ten coverages:
  SNV-only WhatsHap / LongPhase 2 2.08–3.76, HapCUT2 / LongPhase 2 2.55–9.47; SNV + indel runs, SNV pairs
  2.39–3.83 (not quoted), indel pairs 9.12–56.45.
- Renumbering: old Supplementary Figs. 2–17 → 3–18 in every live reference of `sections/*.tex`,
  `Supplementary.tex`, the runtime-table caption written by `make_results_figs.py`, and the panel text of
  `make_supp_figs.py` ("GNN window (Supplementary Fig. 13)"; `suppfig2_voting` regenerated). `%` comments,
  script comments and dated notes keep their old numbers. CLAUDE.md and README updated.

## Not available

No in-benchmark scoring exists for PacBio HiFi (Fig. 2c,d) or for HapCUT2 with indels (Fig. 2b). Both need
`score_phase.py` on the lab-server VCFs (`data/vcf/`), which is a rescoring, not a new experiment.
