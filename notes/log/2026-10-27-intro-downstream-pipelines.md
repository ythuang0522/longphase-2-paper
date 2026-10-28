# Introduction: downstream-pipeline passage rewritten, 2026-10-27 (author decision)

Second Introduction paragraph, from "We previously introduced LongPhase" to the end.
The author chose version C of four drafts (problem first), with two changes:

- LongPhase is named once, at its first mention, as "which we developed previously"
  (lin2022longphase). The clause on the weighted allele graph, chromosome-scale
  haplotypes and SNV-SV co-phasing (and its citations smolka2024sniffles2,
  jiang2020cutesv) was removed. cuteSV remains cited in Methods.
- The closing sentence now states the consequence for downstream tools: one switch
  reverses the haplotype labels of every later read in the block, and the
  small-variant, somatic and SV callers that use those labels carry the error into
  their output.

The "default"/"option" detail for Clair3 and ClairS was removed. The `[citation]`
comment on the downstream-use sentence was updated to match.

Later the same day (author): "(Supplementary Table 6)" was removed from the
downstream-use sentence. The main text no longer cites Supplementary Table 6.
