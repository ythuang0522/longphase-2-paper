# Supplementary figure regeneration prompts

Generated with Codex's built-in image-generation tool in edit mode, using the
corresponding rendered legacy SVG as the reference image.

## Shared art direction

Use case: scientific-educational. Asset type: supplementary methods figure for
a methods manuscript. Fully redraw the supplied reference while
preserving its scientific content, topology, panel meanings, labels, formulas,
thresholds and numerical values. Use a clean white background, flat vector-like
geometry, crisp hairlines, Helvetica/Arial-like typography, a strict alignment
grid and generous whitespace. Use deep navy text, muted publication blue and
vermilion for the two haplotypes, cool greys for neutral structure, and amber
only for uncertain, filtered or thresholded elements. Maintain excellent
legibility at full manuscript width. Avoid invented content, changed values,
misspellings, gradients, shadows, 3D effects, decorative icons, logos and
watermarks.

## Figure-specific prompts

1. **Read observations and filters.** Preserve the five observation classes and
   sources; Q12 weighting; homopolymer length and distance thresholds; the
   overlapping-alignment ratio; and the tandem-repeat indel weight of 0.1.
   Compose a dominant observation panel at left with the three filters stacked
   at right.
2. **Pair support.** Preserve the four allele-pair weights, P=16, Q=1.1,
   similarity s=0.07, all five vote rules, the single-read guard and both DOT
   lines. Use a clear 2-by-2 allele graph, compact decision table and monospaced
   code inset.
3. **Voting and entropy.** Preserve k=35, 300 kb, vote weights 20/1/0.1,
   h1=22.1, h2=1, the entropy equation and PE values 0.257/0.811/0.985/1.000.
   Emphasize the PE >= 0.80 trigger without changing block-formation logic.
4. **Copy-number filter.** Preserve the start/end clipping detector (>=5,
   starts-minus-ends >0, <=200 kb), REF=0.7, ALT=4.7 and
   ALT/(REF+ALT)=0.87 >=0.7. Use a symmetric clipping plot and aligned read-level
   mismatch example.
5. **Read correction.** Preserve all five read patterns, the 0.65 tagging rule,
   the two-informative-allele minimum, class weights, and the worked v3 and v1
   examples with the 0.75 phase-confidence threshold.
6. **GNN window.** Preserve the +/-20 window, node limits, edge construction,
   center-zone coordinates, bridge feature and center-zone equation. Make the
   two allele rows and central prediction zone immediately readable.
7. **GNN architecture.** Preserve N x 31, N x N x 6, adjacency, 31-to-128
   projection, four GPS layers with four heads, local GATv2 and global
   self-attention branches, residual/normalization/FFN sequence, 130-feature
   concatenation, 128-to-2 classifier and per-variant averaging.
8. **Unphase and split.** Preserve P(error)=0.62 >=0.30, PS=1001, the unphased
   GT 0/1 without PS, the two surviving components and new PS=1436. Make clear
   that surviving DOT connectivity is recomputed and genotypes are never
   flipped.
9. **Methylation calling.** Preserve the ML probability thresholds 0.2/0.8,
   strand pooling, heterozygous ratio >=0.6, noise <=0.2, all three stacked-bar
   examples, strong/weak co-segregation criteria, iterative CpG expansion and
   VCF record fields.
10. **Evaluation metrics.** Preserve the truth/query bit strings, switch encoding,
    four switch errors, one flip at positions 7-8, two isolated switches and
    Hamming distance 5/10. Present intersected blocks, phased fraction, block
    N50 and switch error rate as aligned definitions.
