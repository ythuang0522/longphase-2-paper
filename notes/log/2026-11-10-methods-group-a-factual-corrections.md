# Methods review, group A: factual corrections

2026-11-10. Two reviews of the Methods (Claude, Codex); author-approved old | new draft. Checked against
the selection record (`notes/gnn_retrain/`), `notes/competitors/README.md` and the v2.1.2 source
(`git show v2.1.2:<file>` in `../longphase`, read only). No new measurements.

## A1 GNN label selection (author decision, option A)
`notes/gnn_retrain/README.md`: the position-matched labels were kept because they removed more switch
errors on the held-out chromosomes (23.0% against 21.6%). Supplementary Method 4 said "Neither the label
definition nor the threshold was selected on the held-out chromosomes".
- Methods (GNN): "this choice thus used results from the held-out chromosomes".
- Supplementary Method 4: seed and threshold on the validation chromosomes only; the label choice also
  used the held-out and whole-genome results.
- Discussion, paragraph 6: "contributed to the choice between two label definitions and to earlier
  tuning of the graph constants".
Validation means for reference (`seeds.tsv`, val_sw_removed): position 49.7%, REF/ALT 49.3%.

## A2 MethPhaser design
`modcall` removes the phase of the SNV VCF and `phase` makes a new graph (`ModCallParsingBam.cpp:1874`),
so the joint phasing does not start from the SNV-only phasing.
- Methods: "Both analyses used the same read alignments and SNV calls. LongPhase 2 phased SNVs and 5mC
  jointly in a new graph and did not reuse the SNV-only phasing."
- Results: "given the SNV-only phasing of LongPhase 2 from the same reads and SNV calls (Methods)".
- Supplementary Table 19, MethPhaser row: "same reads and SNV calls as the joint SNV+5mC run".

## A3 GNN unphasing rules
`PhasingProcess.cpp:32` (`GNN_KEEP_SV_LENGTH = 10000`), `:1117–1156` (variants left alone in their
phase set), `:1337` (deletions with PE 0 and votes keep their phase).
- Methods: the deletion exception and the left-alone rule added.
- Supplementary Method 4, phase-set update: the left-alone rule added (the deletion rule was there).

## A4 TinkerHap
SNV-only input VCF on HiFi data only (`notes/competitors/README.md`, rows 29–30). Methods and the
TinkerHap row of Supplementary Table 19.

## A5 Source details
- 35 variants in chromosome order, not 35 observations of the read (`PhasingGraph.cpp:932–939`).
- Single-read guard keeps votes with support above 1 (`PhasingGraph.cpp:285–289`).
- Mismatch load excludes SV alleles; MR needs two mean loads above zero; SVs are not removed
  (`PhasingGraph.cpp:593, 681, 727`).
- Supplementary Method 1: weak candidates use the bound max(6, (n1+n2)/4); "at least six reads" is the
  last neighbour-link filter (`ModCallParsingBam.cpp:1449, 1459, 1663–1720`).
- Supplementary Method 5: a read with a deletion supports the one-base allele
  (`HaplotagProcess.cpp:664–683`).
