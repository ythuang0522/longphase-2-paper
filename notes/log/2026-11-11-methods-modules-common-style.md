# Methods: module subsections rewritten in the common style of LongPhase-S and LongPhase-TO

Author, 2026-11-11: read the Methods of the LongPhase-S (Genome Research, final) and LongPhase-TO
(Genome Biology) papers, find their common elements, update `METHODS_WRITING_GUIDELINES.md` (new
section 10), then update the remaining Methods subsections.

Common elements found: an opening overview of the stages; module subsections in stage order with
sub-steps under their own labels; inside a module, reason -> definition in words -> formula with
"where" -> decision rule -> source of the threshold or model ("fixed and applied unchanged"); present
tense with the tool as subject for what the method does, past tense for what the study did; tool
versions and citations in line; evaluation in the last subsections.

`sections/methods.tex` (content unchanged; structure, tense and lead sentences only):

- Read-level allele observations and filtering: lead sentence with three steps; labels Alignment
  selection, Allele extraction, Copy-number-aware filter; reason for the filter and the reading of MR
  (both from Supplementary Method 1).
- Weighted phasing graph: lead sentence; reading of the ambiguity s (0 and 1).
- Haplotype resolution by multi-neighbour voting: lead; labels Votes, Haplotype assignment, Phase
  blocks; the single-read guard is named where it is defined.
- Read-based correction and phasing entropy: lead; labels Read-based correction, Phasing entropy.
- GNN-based detection of phase errors: lead; labels Windows and features, Architecture, Training,
  Selective unphasing; one sentence added ("After training, the model and its threshold were fixed and
  applied unchanged to all coverages and to PacBio HiFi data"), which repeats facts of the Comparison
  and Statistics subsections.
- Haplotagging: tool as subject.
- Internal calling of allele-specific methylation: step paragraphs changed to the present tense.
- All module subsections now use the present tense for the method; GNN training, the tuning sentence
  and the evaluation subsections keep the past tense.

New sentences that give a reason and were not in the Methods before:
"so that the phase of a variant does not depend on one neighbour only" (voting lead) and
"Reads from paralogous sequence that align to one locus can produce false heterozygous sites"
(copy-number filter; from Supplementary Method 1). Author to confirm the first.

The order of first citation of every Supplementary figure, table and method is unchanged (checked).
