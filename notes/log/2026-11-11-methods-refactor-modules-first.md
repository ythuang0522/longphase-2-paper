# Methods refactored: modules first, evaluation detail to Supplementary Method 6

Author, 2026-11-11: the Methods gave more space to benchmark detail than to the tool, the GNN had two
long subsections, and several modules were only named, with the mechanism in the Supplementary.
Plan approved the same day ("Go, as recommended").

Words (text without equations and citations): 4,864 -> about 3,550. Tool modules 51% -> 60% of the
Methods (GNN 22% -> 14%); benchmark and evaluation 46% -> 36%.

## `sections/methods.tex`

| Subsection | Before | After | Change |
|---|---|---|---|
| Internal calling of allele-specific methylation | 192 | 285 | linking modes, depth bound, expansion, final neighbour filter (from Supplementary Method 1); "the basecaller (here Dorado)" |
| Read-level allele observations and filtering | 221 | 296 | allele rule of each class (from Supplementary Method 2) |
| GNN-based detection of phase errors (was two subsections) | 1,072 | about 510 | four paragraphs: windows and features, architecture, labels and training, selective unphasing |
| Haplotagging | 84 | 132 | evidence of each class, untagged cases, tags (from Supplementary Method 5) |
| Benchmark data and truth sets (was "Benchmark data") | 523 | 215 | sample, platforms, coverages, callers, truth sets |
| Comparison with other methods | 333 | 198 | tools, versions, design; MethPhaser paragraph unchanged |
| Evaluation metrics (now includes SV phase evaluation) | 601 | 364 | one definition for each metric |
| Analysis of unphased SNVs | 542 | 252 | call groups, classes, precision, GNN-unphased subset |

Unchanged: Overview, Input, Weighted phasing graph, Voting, Read-based correction, Runtime, Statistics,
Reporting summary, Data and Code availability.

## `Supplementary.tex`

- Supplementary Method 4: new paragraph "Training data" (window counts and chromosome split, verbatim
  from the Methods); scoring-zone sentence; seed ranges of the two label definitions; pointer to
  Supplementary Note 1 and Supplementary Fig. 17e.
- Supplementary Method 6, new title "Benchmark data, tool configurations and evaluation". The former
  Methods text was moved verbatim into new paragraphs: Sequencing data and down-sampling; Truth sets
  and region assignment; Tool configurations; Co-phasing summaries; SV phase evaluation; Analysis of
  unphased SNVs. The former content is under "Metric computation" and the paragraphs after it.

No Supplementary item was renumbered: the first citation of each Supplementary figure, table and method
in the main text keeps its order. Supplementary Fig. 17 and Supplementary Table 17 are cited only in the
Methods (GNN subsection); keep that sentence.

Copies before the change: scratchpad `methods.before_refactor.tex`, `Supplementary.before_refactor.tex`
(session only); use `git diff` for the record.

## Addition, same day (author)

Equations 1 and 2 (5mC calling) use symbols for the user-adjustable thresholds: alpha (`--heterRatio`,
default 0.6), beta (`--noiseRatio`, default 0.2) and gamma (`--connectConfidence`, default 0.9), with the
defaults in the text. Options checked in v2.1.2 `ModCall.cpp`. The Supplementary Fig. 10 legend keeps
the default values.
