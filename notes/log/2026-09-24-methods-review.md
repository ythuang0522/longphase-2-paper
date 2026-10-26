# Methods review, 2026-09-24 (text-only fixes)

**Methods review, 2026-09-24 (text-only fixes).** Fixed SV/indel/5mC observation
qualities stated as numbers (60; 30 for reference-allele SV reads, which still vote at
weight 1 under the default `--baseQuality 12`; `PhasingGraph.cpp:838–862`); modcall
stated to read only the 5mC (`m`) probability, so 5hmC counts as unmethylated
(`ModCallParsingBam.cpp:169`); the flip/unphase/break labels named in Methods;
cross-tool comparisons stated as SNV-only LongPhase 2 (WhatsHap/HapCUT2 *can* phase
indels); HapCUT2 pruning added to the command-line todo; the generalization
limitations moved from Methods ("Hold-out design") to the Discussion; asides cut and
procedural tense made past. Still open from that review, needing decisions or new
analysis (the v5.0q-without-BED item: on 2026-09-24 the authors said both truth sets
were scored within their benchmark BEDs and Methods was changed accordingly; **this was
wrong** — JHL's reproduction of all 1,024 runs on 2026-10-08 (issue #1) showed that every
table was scored without a BED, and Methods now says so): the
deployment threshold needed a separate selection rationale (resolved by the author on
2026-10-06: an end-to-end phasing cost trade-off, distinct from checkpoint criterion S); test
accuracy 0.941 is below the all-correct baseline 0.970; no statement that test
chromosomes were unused during architecture search; GNN applied outside its training
configuration (SNV-only, 30–60×); no dispersion at 30–60× (per-chromosome bootstrap
possible); SV/5mC phased-fraction denominator undefined (the truth sets carry no
SV/5mC). Author decisions, 2026-09-24, not to be re-raised: no Zenodo/DOI deposit
(the public repository is the only deposit for code, data and tables), and no
`longphase compare` vs `whatshap compare` validation in the paper.
