# Shared switch-error comparison clarified using 60x, 2026-11-10

Author selected option 1, starting with "Under v4.2.1", and requested a single mention of 60x as the example throughout the selected comparison.

Replaced the shared-error sentences before the shared-benchmark-region analysis. Defined the shared positions, listed each tool's fraction (93%, 86%, 74%) and compared the same outputs against v5.0q (38%, 10%, 8%). Removed the 10x/63% detail. The following regional analysis is unchanged.

## Follow-up: merge with the preceding benchmark comparison

At the author's request, removed the paragraph break before "Under v4.2.1". The benchmark count ranges, Hamming-distance comparison and shared switch-error analysis now form one paragraph. Wording, numerical values and citations are unchanged.

## Follow-up: opening sentence supplied by the author

Replaced the opening sentence with "Under v4.2.1, many switch errors occurred at the same positions in all three tools (Fig. 4c)." Removed the 60x qualifier from that sentence and added the figure citation, using the manuscript's existing Fig. abbreviation and cross-reference syntax.

## Follow-up: distinguish shared error positions from shared benchmark regions

The author asked whether the regional counts were absolute versions of the preceding shared-error fractions and requested one coverage example. They are different analyses: Table 8c counts errors common to all three tools (1,555 under v4.2.1 and 182 under v5.0q at 60x), while Table 8a counts each tool's errors inside the intersection of the two benchmark region sets.

Added one 60x qualifier to the shared-position percentages. Replaced the 30–60x regional ranges with the same 60x example: v4.2.1 counts 1,180/1,245/1,435 and v5.0q counts 32/63/273 for LongPhase 2/WhatsHap/HapCUT2. Wrote "genomic regions covered by both benchmarks" to distinguish the region intersection from cross-tool error overlap.

## Follow-up: author-approved per-tool counts in shared regions

Replaced the pooled regional ranges with the approved two-sentence version:

> Differences between the benchmarks were also evident within genomic regions covered by both. For the same 60× outputs, LongPhase 2, WhatsHap and HapCUT2 had 1,180, 1,245 and 1,435 switch errors against v4.2.1, respectively, compared with 32, 63 and 273 against v5.0q (Supplementary Table 8).

The three tools are listed in the same order for both benchmarks. The surrounding paragraph is unchanged.

## Follow-up: approved interpretation of the lower shared-error fractions

Added "indicating less overlap in switch-error positions across tools than under v4.2.1" to the v5.0q percentage sentence. Removed that sentence's repeated Fig. 4c citation; the preceding v4.2.1 sentence retains it. The wording describes overlap rather than absolute error counts and makes no claim about the cause of benchmark differences.

## Follow-up: separate benchmark disagreement from validation limits

Author approved option 1:

> These results suggest that the two benchmarks assign different phases at many shared sites. The underlying reads have not been examined to determine which phase assignments are correct.

Replaced the former sentence about possible v4.2.1 phase-transfer errors. The new wording separates the inferred phase disagreement from the unresolved correctness of either benchmark. No numerical values or citations changed.
