# Methods review, group B: missing definitions

2026-11-10. Author-approved old | new draft. All changes in `sections/methods.tex`. No new measurements.

- B1 SV phase evaluation: scored set (heterozygous Sniffles2 DEL/INS, same records for every tool,
  replicate 1); nearest truth match; block orientation from SNVs matched to the truth by position;
  homozygous truth matches counted separately as genotype errors; these, SVs without a truth match and SVs
  in blocks that cannot be oriented are not in the error rate (`notes/sv_phasing/score_sv_phase.py`,
  categories `phased_hom_in_truth`, `phased_no_truth_match`, `phased_no_block_snv`).
- B2 Evaluation metrics: blocks joined (net decrease in block count against SNV-only phasing, same
  replicate and GNN setting; not tracked merge events), sites added, switch errors per join (as the
  Supplementary Table 6 legend).
- B3 Benchmark scoring: the remainder outside both sets of benchmark regions; GIAB v3.6 strata applied
  inside the v5.0q regions; a shared switch error is the same pair of SNV positions under one truth set,
  replicate 1 (`notes/benchmark_strata/item4_overlap.tsv`); not followed between truth sets.
- B4 Analysis of unphased SNVs: paragraphs in the order of Fig. 5 (comparison with WhatsHap first, then
  the subset unphased by GNN correction); "in replicate 1 at 10, 30 and 60x"; read depth = FORMAT/DP of
  the caller, capped near 125x (`notes/unphased/README.md`).
- B5 "left unphased at high phasing uncertainty" (Fig. 5h, Supplementary Fig. 6 legends) tied to the
  subset phased before and unphased after GNN correction; not every SNV in it has high entropy
  (scoring zone around the trigger; variants left alone in their phase set).
- B6 Precision defined as a benchmark-match fraction (author decision: operational definition, the name in
  Fig. 5e stays); F1 does not measure phase correctness; "Completeness (phased fraction)" defined once.
- B7 Statistics: analyses that use replicate 1 only; each configuration timed once.
