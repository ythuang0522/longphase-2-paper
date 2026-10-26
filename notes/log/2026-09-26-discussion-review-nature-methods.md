# Discussion review for Nature Methods, 2026-09-26

**Discussion review for Nature Methods, 2026-09-26.** Every number re-derived from
`20260924_v50q.txt`, `20260924_GIAB421.txt` and `GNN source/sw_*.log`. Four factual errors
fixed: (1) "every tool accumulates more switch errors under the T2T-based benchmark" was
false: corrected LongPhase 2 makes *fewer* under v5.0q (1,820 → 1,518 at 10×; 1,676 → 496 at
60×) and WhatsHap is level at 60× (1,801 vs 1,785); the paragraph now separates the
competitors' rise from a ~1,600-error floor shared by all tools under v4.2.1 that is more
plausibly benchmark discordance (new `[optional experiment]`: intersect those switch
positions); spread restated in rates (1.2–1.3 → 4.3–4.8-fold, matching Results);
(2) corrected four-class co-phasing is more accurate than *uncorrected* SNV-only only
(0.027% vs 0.034%; corrected SNV-only 0.023%); (3) the denominator defence of the GNN was a
non sequitur and is replaced by its price (~2,400 benchmark hets unphased for 247 fewer
switches at 60×); (4) "86–96%" was quoted for 10× alone, and clustered/low-GQ sites are about
half, not "most", of benchmark-absent calls. Uncertainty claims narrowed: `gnn` writes no
error probability (only `phase` writes PE/H1/H2, `ParsingBam.cpp:226–228`) and no link
entropy exists, entropy = 0 for 22–43% of removed genuine hets (Fig. 6c), and calibration is
untested (Supp. Fig. 9 placeholder); the genotype-quality analogy now appears only as a
goal. Limitations added: genome-wide rates include training chromosomes, single replicate at
30–60×, indel/SV/5mC phase accuracy not assessed, unsupervised SV/5mC corrections, polyploidy.
Indel trade-off stated once. Discussion now ~1,400 words (texcount), from ~1,300.
**Still open:** Results heading "A telomere-to-telomere benchmark exposes switch errors hidden
by the GRCh38 truth set" holds for WhatsHap/HapCUT2 only; re-scoring chr17/21/22 is now the
most important cheap analysis, because the Discussion names the train/test overlap as a limitation.
